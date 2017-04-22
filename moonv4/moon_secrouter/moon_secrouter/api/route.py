# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import copy
import time
from oslo_log import log as logging
from moon_utilities.security_functions import call
from oslo_config import cfg
from moon_secrouter.api.generic import Status, Logs

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

API = {
    "orchestrator": (
        "add_container",
        "delete_container",
        "add_slave",
        "get_slaves",
        "delete_slave"
    ),
    # TODO (asteroide): need to check if some of those calls need (or not) to be called "update_"
    "manager": (
        "get_subject_assignments",
        "set_subject_assignment",
        "delete_subject_assignment",
        "get_object_assignments",
        "set_object_assignment",
        "delete_object_assignment",
        "get_action_assignments",
        "set_action_assignment",
        "delete_action_assignment",
        "get_subject_data",
        "add_subject_data",
        "delete_subject_data",
        "get_object_data",
        "add_object_data",
        "delete_object_data",
        "get_action_data",
        "add_action_data",
        "delete_action_data",
        "get_subject_categories",
        "set_subject_category",
        "delete_subject_category",
        "get_object_categories",
        "set_object_category",
        "delete_object_category",
        "get_action_categories",
        "set_action_category",
        "delete_action_category",
        "add_meta_rules",
        "delete_meta_rules",
        "get_meta_rules",
        "set_meta_rules",
        "get_models",
        "add_model",
        "delete_model",
        "update_model",
        "get_pdp",
        "add_pdp",
        "delete_pdp",
        "update_pdp",
        "get_subjects",
        "set_subject",
        "delete_subject",
        "get_objects",
        "set_object",
        "delete_object",
        "get_actions",
        "set_action",
        "delete_action",
        "get_policies",
        "add_policy",
        "delete_policy",
        "update_policy",
        "get_subject_assignments",
        "update_subject_assignment",
        "delete_subject_assignment",
        "get_object_assignments",
        "update_object_assignment",
        "delete_object_assignment",
        "get_action_assignments",
        "update_action_assignment",
        "delete_action_assignment",
        "get_rules",
        "add_rule",
        "delete_rule"
    ),
    "function": (
        "authz",
    ),
}


class Cache(object):

    # TODO (asteroide): set cache integer in CONF file
    __UPDATE_INTERVAL = 300
    __CONTAINERS = {}
    __LAST_UPDATE = 0

    def __update_container(self):
        containers = call("orchestrator", method="get_container", ctx={}, args={})
        LOG.info("container={}".format(containers))
        for key, value in containers["containers"].items():
            self.__CONTAINERS[key] = value

    def update(self, component=None):
        self.__update_container()

    @property
    def containers(self):
        """intra_extensions cache
        example of content :
        {
            "pdp_uuid1": "component_uuid1",
            "pdp_uuid2": "component_uuid2",
        }
        :return:
        """
        current_time = time.time()
        if self.__LAST_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_container()
        self.__LAST_UPDATE = current_time
        return self.__CONTAINERS


CACHE = Cache()


class Router(object):
    """
    Route requests to all components.
    """

    __version__ = "0.1.0"

    def __init__(self, add_master_cnx):
        if CONF.slave.slave_name and add_master_cnx:
            result = call('security_router', method="route",
                          ctx={
                              "name": CONF.slave.slave_name,
                              "description": CONF.slave.slave_name,
                              "call_master": True,
                              "method": "add_slave"}, args={})
            if "result" in result and not result["result"]:
                LOG.error("An error occurred when sending slave name {} {}".format(
                    CONF.slave.slave_name, result
                ))
            self.slave_id = list(result['slaves'].keys())[0]
            result = call('security_router', method="route",
                          ctx={
                              "name": CONF.slave.slave_name,
                              "description": CONF.slave.slave_name,
                              "call_master": True,
                              "method": "get_slaves"}, args={})
            if "result" in result and not result["result"]:
                LOG.error("An error occurred when receiving slave names {} {}".format(
                    CONF.slave.slave_name, result
                ))
            LOG.info("SLAVES: {}".format(result))

    def delete(self):
        if CONF.slave.slave_name and self.slave_id:
            result = call('security_router', method="route",
                          ctx={
                              "name": CONF.slave.slave_name,
                              "description": CONF.slave.slave_name,
                              "call_master": True,
                              "method": "delete_slave",
                              "id": self.slave_id}, args={})
            if "result" in result and not result["result"]:
                LOG.error("An error occurred when sending slave name {} {}".format(
                    CONF.slave.slave_name, result
                ))
            LOG.info("SLAVE CONNECTION ENDED!")
            LOG.info(result)

    @staticmethod
    def __get_first_container(keystone_project_id):
        for container_id, container_value, in CACHE.containers.items():
            if container_value:
                if container_value[0]["keystone_project_id"] == keystone_project_id:
                    return container_value[0]["container_id"]

    @staticmethod
    def check_pdp(ctx):
        _ctx = copy.deepcopy(ctx)
        if CONF.slave.slave_name:
            _ctx['call_master'] = True
        ext = call("moon_manager", method="get_pdp", ctx=_ctx, args={})
        if "error" not in ext:
            return True

    def send_update(self, api, ctx={}, args={}):
        # TODO (asteroide): add threads here
        if not CONF.slave.slave_name:
            # Note (asteroide):
            # if adding or setting an element: do nothing
            # if updating or deleting an element: force deletion in the slave
            if "update_" in api or "delete_" in api:
                for slave_id, slave_dict in call("orchestrator", method="get_slaves", ctx={}, args={})['slaves'].items():
                    LOG.info('send_update slave_id={}'.format(slave_id))
                    LOG.info('send_update slave_dict={}'.format(slave_dict))
                    ctx['method'] = api.replace("update", "delete")
                    # TODO (asteroide): force data_id to None to force the deletion in the slave
                    result = call("security_router_"+slave_dict['name'], method="route", ctx=ctx, args=args)
                    if "result" in result and not result["result"]:
                        LOG.error("An error occurred when sending update to {} {}".format(
                            "security_router_"+slave_dict['name'], result
                        ))

    def route(self, ctx, args):
        """Route the request to the right endpoint

        :param ctx: dictionary depending of the real destination
        :param args: dictionary depending of the real destination
        :return: dictionary depending of the real destination
        """
        if ctx["method"] == "get_status":
            return Status().get_status(ctx=ctx, args=args)
        if ctx["method"] == "get_logs":
            return Logs().get_logs(ctx=ctx, args=args)
        for component in API:
            if ctx["method"] in API[component]:
                if component == "orchestrator":
                    return call(component, method=ctx["method"], ctx=ctx, args=args)
                if component == "manager":
                    LOG.info("Call Manager {}".format(ctx))
                    result = call("moon_manager", method=ctx["method"], ctx=ctx, args=args)
                    self.send_update(api=ctx["method"], ctx=ctx, args=args)
                    return result
                if component == "function":
                    if self.check_pdp(ctx):
                        LOG.info("Tenant ID={}".format(ctx['id']))
                        pdp_container = self.__get_first_container(ctx['id'])
                        LOG.info("pdp_container={}".format(pdp_container))
                        # TODO (asteroide): call the first security function through a notification
                        # and not an RPC call (need to play with ID in context)
                        result = call(pdp_container, method=ctx["method"], ctx=ctx, args=args)
                        return result
                    return {"result": False,
                            "error": {'code': 500, 'title': 'Moon Error', 'description': "Function component not found."},
                            "pdp_id": ctx["id"],
                            "ctx": ctx, "args": args}

        # TODO (asteroide): must raise an exception here ?
        return {"result": False,
                "error": {'code': 500, 'title': 'Moon Error', 'description': "Endpoint method not found."},
                "intra_extension_id": ctx["id"],
                "ctx": ctx, "args": args}

