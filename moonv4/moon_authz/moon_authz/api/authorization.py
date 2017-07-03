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


class Authorization(object):
    """
    Retrieve the current status of all components.
    """

    __version__ = "0.1.0"
    pdp_id = None
    meta_rule_id = None
    keystone_project_id = None
    payload = None

    def __init__(self, component_desc):
        self.component_id = component_desc
        LOG.info("ext={}".format(component_desc))
        self.filter_rule = oslo_messaging.NotificationFilter(
            event_type='^authz$',
            context={'container_id': "\w+_"+hashlib.sha224(component_desc.encode("utf-8")).hexdigest()}
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
        Context.update_target(context)
        current_pdp = context['pdp_set'][current_header_id]
        category_list = list()
        category_list.extend(current_pdp["meta_rules"]["subject_categories"])
        category_list.extend(current_pdp["meta_rules"]["object_categories"])
        category_list.extend(current_pdp["meta_rules"]["action_categories"])
        for category in category_list:
            scope = list(current_pdp['target'][category])
            scopes_list.append(scope)
        policy_id = PolicyManager.get_policy_from_meta_rules("admin", current_header_id)
        rules = PolicyManager.get_rules(user_id="admin",
                                        policy_id=policy_id,
                                        meta_rule_id=current_header_id)
        for item in itertools.product(*scopes_list):
            req = list(item)
            for rule in rules['rules']:
                if req == rule['rule']:
                    return rule['instructions'], ""
        LOG.warning("No rule match the request...")
        return False, "No rule match the request..."

    def __update_subject_category_in_policy(self, operation, target):
        result = False
        try:
            policy_name, category_name, data_name = target.split(":")
        except ValueError:
            LOG.error("Cannot understand value in instruction ({})".format(target))
            return False
        pdp_set = self.payload["authz_context"]['pdp_set']
        for meta_rule_id in self.payload["authz_context"]['pdp_set']:
            policy_id = PolicyManager.get_policy_from_meta_rules("admin", meta_rule_id)
            if meta_rule_id == "effect":
                continue
            if pdp_set[meta_rule_id]["meta_rules"]["name"] == policy_name:
                for category_id, category_value in ModelManager.get_subject_categories("admin").items():
                    if category_value["name"] == "role":
                        subject_category_id = category_id
                        break
                else:
                    LOG.error("Cannot understand category in instruction ({})".format(target))
                    return False
                subject_data_id = None
                for data in PolicyManager.get_subject_data("admin", policy_id, category_id=subject_category_id):
                    for data_id, data_value in data['data'].items():
                        if data_value["name"] == data_name:
                            subject_data_id = data_id
                            break
                    if subject_data_id:
                        break
                else:
                    LOG.error("Cannot understand data in instruction ({})".format(target))
                    return False
                if operation == "add":
                    self.payload["authz_context"]['pdp_set'][meta_rule_id]['target'][subject_category_id].append(
                        subject_data_id)
                elif operation == "delete":
                    try:
                        self.payload["authz_context"]['pdp_set'][meta_rule_id]['target'][subject_category_id].remove(
                            subject_data_id)
                    except ValueError:
                        LOG.warning("Cannot remove role {} from target".format(data_name))
                result = True
                break
        return result

    def __update_container_chaining(self):
        for index in range(len(self.payload["authz_context"]['headers'])):
            self.payload["container_chaining"][index]["meta_rule_id"] = self.payload["authz_context"]['headers'][index]

    def __get_container_from_meta_rule(self, meta_rule_id):
        for index in range(len(self.payload["authz_context"]['headers'])):
            if self.payload["container_chaining"][index]["meta_rule_id"] == meta_rule_id:
                return self.payload["container_chaining"][index]

    def __update_headers(self, name):
        context = self.payload["authz_context"]
        for meta_rule_id, meta_rule_value in context["pdp_set"].items():
            if meta_rule_id == "effect":
                continue
            if meta_rule_value["meta_rules"]["name"] == name:
                self.payload["authz_context"]['headers'].append(meta_rule_id)
                return True
        return False

    def __exec_next_state(self, rule_found):
        index = self.payload["authz_context"]['index']
        current_meta_rule = self.payload["authz_context"]['headers'][index]
        current_container = self.__get_container_from_meta_rule(current_meta_rule)
        current_container_genre = current_container["genre"]
        try:
            next_meta_rule = self.payload["authz_context"]['headers'][index+1]
        except IndexError:
            next_meta_rule = None
        if current_container_genre == "authz":
            if rule_found:
                return self.__return_to_router()
            pass
            if next_meta_rule:
                # next will be session if current is deny and session is unset
                if self.payload["authz_context"]['pdp_set'][next_meta_rule]['effect'] == "unset":
                    return notify(
                        request_id=self.payload["authz_context"]["request_id"],
                        container_id=self.__get_container_from_meta_rule(next_meta_rule)['container_id'],
                        payload=self.payload)
                # next will be delegation if current is deny and session is passed or deny and delegation is unset
                else:
                    LOG.error("Delegation is not developed!")

            else:
                # else next will be None and the request is sent to router
                return self.__return_to_router()
        elif current_container_genre == "session":
            pass
            # next will be next container in headers if current is passed
            if self.payload["authz_context"]['pdp_set'][current_meta_rule]['effect'] == "passed":
                return notify(
                    request_id=self.payload["authz_context"]["request_id"],
                    container_id=self.__get_container_from_meta_rule(next_meta_rule)['container_id'],
                    payload=self.payload)
            # next will be None if current is grant and the request is sent to router
            else:
                return self.__return_to_router()
        elif current_container_genre == "delegation":
            LOG.error("Delegation is not developed!")
            # next will be authz if current is deny
            # next will be None if current is grant and the request is sent to router

    def __return_to_router(self):
        call(endpoint="security_router",
             ctx={"id": self.component_id,
                  "call_master": False,
                  "method": "return_authz",
                  "request_id": self.payload["authz_context"]["request_id"]},
             method="route",
             args=self.payload["authz_context"])

    def __exec_instructions(self, instructions):
        current_header_id = self.payload["authz_context"]['headers'][self.payload["authz_context"]['index']]
        for instruction in instructions:
            for key in instruction:
                if key == "decision":
                    if instruction["decision"] == "grant":
                        self.payload["authz_context"]['pdp_set'][current_header_id]["effect"] = "grant"
                        self.__return_to_router()
                    else:
                        self.payload["authz_context"]['pdp_set'][current_header_id]["effect"] = instruction["decision"]
                elif key == "chain":
                    result = self.__update_headers(**instruction["chain"])
                    if not result:
                        self.payload["authz_context"]['pdp_set'][current_header_id]["effect"] = "deny"
                    else:
                        self.payload["authz_context"]['pdp_set'][current_header_id]["effect"] = "passed"
                elif key == "update":
                    result = self.__update_subject_category_in_policy(**instruction["update"])
                    if not result:
                        self.payload["authz_context"]['pdp_set'][current_header_id]["effect"] = "deny"
                    else:
                        self.payload["authz_context"]['pdp_set'][current_header_id]["effect"] = "passed"
        # LOG.info("__exec_instructions {}".format(self.payload["authz_context"]))

    def __update_current_request(self):
        index = self.payload["authz_context"]["index"]
        current_header_id = self.payload["authz_context"]['headers'][index]
        previous_header_id = self.payload["authz_context"]['headers'][index-1]
        current_policy_id = PolicyManager.get_policy_from_meta_rules("admin", current_header_id)
        previous_policy_id = PolicyManager.get_policy_from_meta_rules("admin", previous_header_id)
        # FIXME (asteroide): must change those lines to be ubiquitous against any type of policy
        if self.payload["authz_context"]['pdp_set'][current_header_id]['meta_rules']['name'] == "session":
            subject = self.payload["authz_context"]['current_request'].get("subject")
            subject_category_id = None
            role_names = []
            for category_id, category_value in ModelManager.get_subject_categories("admin").items():
                if category_value["name"] == "role":
                    subject_category_id = category_id
                    break
            for assignment_id, assignment_value in PolicyManager.get_subject_assignments(
                    "admin", previous_policy_id, subject, subject_category_id).items():
                    for data_id in assignment_value["assignments"]:
                        data = PolicyManager.get_subject_data("admin", previous_policy_id, data_id, subject_category_id)
                        for _data in data:
                            for key, value in _data["data"].items():
                                role_names.append(value["name"])
            new_role_ids = []
            for perimeter_id, perimeter_value in PolicyManager.get_objects("admin", current_policy_id).items():
                if perimeter_value["name"] in role_names:
                    new_role_ids.append(perimeter_id)
                    break
            perimeter_id = None
            for perimeter_id, perimeter_value in PolicyManager.get_actions("admin", current_policy_id).items():
                if perimeter_value["name"] == "*":
                    break

            self.payload["authz_context"]['current_request']['object'] = new_role_ids[0]
            self.payload["authz_context"]['current_request']['action'] = perimeter_id
        elif self.payload["authz_context"]['pdp_set'][current_header_id]['meta_rules']['name'] == "rbac":
            self.payload["authz_context"]['current_request']['subject'] = self.payload["authz_context"]['initial_request']['subject']
            self.payload["authz_context"]['current_request']['object'] = self.payload["authz_context"]['initial_request']['object']
            self.payload["authz_context"]['current_request']['action'] = self.payload["authz_context"]['initial_request']['action']

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
        LOG.info("calling authz {} {}".format(ctxt, payload))
        self.keystone_project_id = payload["id"]
        self.payload = payload
        try:
            if "authz_context" not in payload:
                try:
                    self.payload["authz_context"] = Context(self.keystone_project_id,
                                                            self.payload["subject_name"],
                                                            self.payload["object_name"],
                                                            self.payload["action_name"],
                                                            self.payload["request_id"]).to_dict()
                except exceptions.SubjectUnknown:
                    ctx = {
                        "subject_name": self.payload["subject_name"],
                        "object_name": self.payload["object_name"],
                        "action_name": self.payload["action_name"],
                    }
                    call("moon_manager", method="update_from_master", ctx=ctx, args={})
                    self.payload["authz_context"] = Context(self.keystone_project_id,
                                                            self.payload["subject_name"],
                                                            self.payload["object_name"],
                                                            self.payload["action_name"],
                                                            self.payload["request_id"]).to_dict()
                except exceptions.ObjectUnknown:
                    ctx = {
                        "subject_name": self.payload["subject_name"],
                        "object_name": self.payload["object_name"],
                        "action_name": self.payload["action_name"],
                    }
                    call("moon_manager", method="update_from_master", ctx=ctx, args={})
                    self.payload["authz_context"] = Context(self.keystone_project_id,
                                                            self.payload["subject_name"],
                                                            self.payload["object_name"],
                                                            self.payload["action_name"],
                                                            self.payload["request_id"]).to_dict()
                except exceptions.ActionUnknown:
                    ctx = {
                        "subject_name": self.payload["subject_name"],
                        "object_name": self.payload["object_name"],
                        "action_name": self.payload["action_name"],
                    }
                    call("moon_manager", method="update_from_master", ctx=ctx, args={})
                    self.payload["authz_context"] = Context(self.keystone_project_id,
                                                            self.payload["subject_name"],
                                                            self.payload["object_name"],
                                                            self.payload["action_name"],
                                                            self.payload["request_id"]).to_dict()
                self.__update_container_chaining()
            else:
                self.payload["authz_context"]["index"] += 1
                self.__update_current_request()
            result, message = self.__check_rules(self.payload["authz_context"])
            current_header_id = self.payload["authz_context"]['headers'][self.payload["authz_context"]['index']]
            if result:
                self.__exec_instructions(result)
            else:
                self.payload["authz_context"]['pdp_set'][current_header_id]["effect"] = "deny"
            self.__exec_next_state(result)
            return {"authz": result,
                    "error": message,
                    "pdp_id": self.pdp_id,
                    "ctx": ctxt, "args": self.payload}
        except Exception as e:
            try:
                LOG.error(self.payload["authz_context"])
            except KeyError:
                LOG.error("Cannot find \"authz_context\" in context")
            LOG.error(e, exc_info=True)
            return {"authz": False,
                    "error": str(e),
                    "pdp_id": self.pdp_id,
                    "ctx": ctxt, "args": self.payload}

