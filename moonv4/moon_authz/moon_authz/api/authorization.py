# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import hashlib
import itertools
from oslo_log import log as logging
from oslo_config import cfg
import oslo_messaging
from moon_utilities.security_functions import call, Context, notify
from moon_utilities.misc import get_uuid_from_name
from moon_utilities import exceptions
from moon_db.core import PDPManager
from moon_db.core import ModelManager
from moon_db.core import PolicyManager

# TODO (asteroide):
# - end the dev of the context
# - rebuild the authorization function according to the context
# - call the next security function
# - call the master if an element is absent

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class PDP:

    def __init__(self, context):
        self.__context = context


class Authorization(object):
    """
    Retrieve the current status of all components.
    """

    __version__ = "0.1.0"
    pdp_id = None
    meta_rule_id = None
    keystone_project_id = None

    def __init__(self, component_desc):
        self.component_id = component_desc
        LOG.info("ext={}".format(component_desc))
        self.filter_rule = oslo_messaging.NotificationFilter(
            event_type='^authz$',
            context={'container_id': "authz_"+hashlib.sha224(component_desc.encode("utf-8")).hexdigest()}
        )

        for _id_value in component_desc.split("_"):
            _type, _id = _id_value.split(":")
            if _type == "pdp":
                self.pdp_id = _id
            elif _type == "metarule":
                self.meta_rule_id = _id
            elif _type == "project":
                self.keystone_project_id = _id

    def __check_rules(self, context):
        scopes_list = list()
        current_header_id = context['headers'][context['index']]
        current_pdp = context['pdp_set'][current_header_id]
        category_list = list()
        category_list.extend(current_pdp["meta_rules"]["subject_categories"])
        category_list.extend(current_pdp["meta_rules"]["object_categories"])
        category_list.extend(current_pdp["meta_rules"]["action_categories"])
        for category in category_list:
            # if not current_pdp['target'][category]:
            #     LOG.warning("Empty assignment detected: {} target={}".format(category, current_pdp['target']))
            scopes_list.append(current_pdp['target'][category])
        policy_id = PolicyManager.get_policy_from_meta_rules("admin", current_header_id)
        rules = PolicyManager.get_rules(user_id="admin",
                                        policy_id=policy_id,
                                        meta_rule_id=current_header_id)
        rules = list(map(lambda x: x['rule'], rules['rules']))
        for item in itertools.product(*scopes_list):
            req = list(item)
            if req in rules:
                return True, ""
        LOG.warning("No rule match the request...")
        return False, "No rule match the request..."

    def critical(self, ctxt, publisher_id, event_type, payload, metadata):
        """This is the authz endpoint
        but due to the oslo_messaging notification architecture, we must call it "critical"
        
        :param ctxt: context of the request
        :param publisher_id: ID of the publisher
        :param event_type: type of event ("authz" here)
        :param payload: content of the authz request
        :param metadata: metadata of the notification
        :return: result of the authorization for the current component
        """
        LOG.info("authz {} {}".format(ctxt, payload))
        keystone_project_id = payload["id"]
        try:
            if "authz_context" not in payload:
                payload["authz_context"] = Context(keystone_project_id,
                                                   payload["subject_name"],
                                                   payload["object_name"],
                                                   payload["action_name"],
                                                   payload["request_id"]).to_dict()
            else:
                payload["authz_context"]["index"] += 1
            result, message = self.__check_rules(payload["authz_context"])
            current_header_id = payload["authz_context"]['headers'][payload["authz_context"]['index']]
            # current_pdp = payload["authz_context"]['pdp_set'][current_header_id]
            if result:
                payload["authz_context"]['pdp_set'][current_header_id]["effect"] = "grant"
            if payload["authz_context"]["index"]+1 < len(payload["authz_context"]["headers"]):
                next_index = payload["authz_context"]["index"]+1
                notify(
                    request_id=payload["authz_context"]["request_id"],
                    container_id=payload["container_chaining"][next_index],
                    payload=payload)
            else:
                ret = call(endpoint="security_router",
                           ctx={"id": self.component_id,
                                "call_master": False,
                                "method": "return_authz",
                                "request_id": payload["authz_context"]["request_id"]},
                           method="route",
                           args=payload["authz_context"])
            del payload["authz_context"]
            return {"authz": result,
                    "error": message,
                    "pdp_id": self.pdp_id,
                    "ctx": ctxt, "args": payload}
        except Exception as e:
            try:
                LOG.error(payload["authz_context"])
                # del ctx["authz_context"]
            except KeyError:
                LOG.error("Cannot find \"authz_context\" in context")
            LOG.error(e, exc_info=True)
            return {"authz": False,
                    "error": str(e),
                    "pdp_id": self.pdp_id,
                    "ctx": ctxt, "args": payload}

