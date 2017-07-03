# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import copy
import time
import itertools
from uuid import uuid4
from oslo_log import log as logging
from moon_utilities.security_functions import call, notify
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
        "delete_rule",
        "update_from_master"
    ),
    "function": (
        "authz",
        "return_authz",
    ),
}


class Cache(object):

    # TODO (asteroide): set cache integer in CONF file
    __UPDATE_INTERVAL = 10
    
    __CONTAINERS = {}
    __CONTAINERS_UPDATE = 0

    __CONTAINER_CHAINING_UPDATE = 0
    __CONTAINER_CHAINING = {}

    __PDP = {}
    __PDP_UPDATE = 0
    
    __POLICIES = {}
    __POLICIES_UPDATE = 0
    
    __MODELS = {}
    __MODELS_UPDATE = 0
    
    __AUTHZ_REQUESTS = {}

    def update(self, component=None):
        self.__update_container()
        self.__update_pdp()
        self.__update_policies()
        self.__update_models()
        for key, value in self.__PDP.items():
            LOG.info("Updating container_chaining with {}".format(value["keystone_project_id"]))
            self.__update_container_chaining(value["keystone_project_id"])

    @property
    def authz_requests(self):
        return self.__AUTHZ_REQUESTS

    def __update_pdp(self):
        pdp = call("moon_manager", method="get_pdp", ctx={"user_id": "admin"}, args={})
        if not pdp["pdps"]:
            LOG.info("Updating PDP through master")
            pdp = call("moon_manager", method="get_pdp",
                       ctx={
                           "user_id": "admin",
                           'call_master': True
                        },
                       args={})
        for _pdp in pdp["pdps"].values():
            if _pdp['keystone_project_id'] not in self.__CONTAINER_CHAINING:
                self.__CONTAINER_CHAINING[_pdp['keystone_project_id']] = {}
                # Note (asteroide): force update of chaining
                self.__update_container_chaining(_pdp['keystone_project_id'])
        for key, value in pdp["pdps"].items():
            self.__PDP[key] = value

    @property
    def pdp(self):
        current_time = time.time()
        if self.__PDP_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_pdp()
        self.__PDP_UPDATE = current_time
        return self.__PDP

    def __update_policies(self):
        policies = call("moon_manager", method="get_policies", ctx={"user_id": "admin"}, args={})
        for key, value in policies["policies"].items():
            self.__POLICIES[key] = value

    @property
    def policies(self):
        current_time = time.time()
        if self.__POLICIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_policies()
        self.__POLICIES_UPDATE = current_time
        return self.__POLICIES

    def __update_models(self):
        models = call("moon_manager", method="get_models", ctx={"user_id": "admin"}, args={})
        for key, value in models["models"].items():
            self.__MODELS[key] = value

    @property
    def models(self):
        current_time = time.time()
        if self.__MODELS_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_models()
        self.__MODELS_UPDATE = current_time
        return self.__MODELS

    def __update_container(self):
        containers = call("orchestrator", method="get_container", ctx={}, args={})
        for key, value in containers["containers"].items():
            self.__CONTAINERS[key] = value

    @property
    def container_chaining(self):
        current_time = time.time()
        if self.__CONTAINER_CHAINING_UPDATE + self.__UPDATE_INTERVAL < current_time:
            for key, value in self.pdp.items():
                self.__update_container_chaining(value["keystone_project_id"])
        self.__CONTAINER_CHAINING_UPDATE = current_time
        return self.__CONTAINER_CHAINING

    def __update_container_chaining(self, keystone_project_id):
        container_ids = []
        for pdp_id, pdp_value, in CACHE.pdp.items():
            LOG.info("pdp_id, pdp_value = {}, {}".format(pdp_id, pdp_value))
            if pdp_value:
                if pdp_value["keystone_project_id"] == keystone_project_id:
                    for policy_id in pdp_value["security_pipeline"]:
                        model_id = CACHE.policies[policy_id]['model_id']
                        LOG.info("model_id = {}".format(model_id))
                        LOG.info("CACHE = {}".format(CACHE.models[model_id]))
                        for meta_rule_id in CACHE.models[model_id]["meta_rules"]:
                            LOG.info("CACHE.containers = {}".format(CACHE.containers))
                            for container_id, container_values, in CACHE.containers.items():
                                LOG.info("container_id, container_values = {}".format(container_id, container_values))
                                for container_value in container_values:
                                    LOG.info("container_value[\"meta_rule_id\"] == meta_rule_id = {} {}".format(container_value["meta_rule_id"], meta_rule_id))
                                    if container_value["meta_rule_id"] == meta_rule_id:
                                        container_ids.append(
                                            {
                                                "container_id": container_value["container_id"],
                                                "genre": container_value["genre"]
                                            }
                                        )
                                        break
        self.__CONTAINER_CHAINING[keystone_project_id] = container_ids

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
        if self.__CONTAINERS_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_container()
        self.__CONTAINERS_UPDATE = current_time
        return self.__CONTAINERS


CACHE = Cache()


class AuthzRequest:

    result = None
    req_max_delay = 2

    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args
        self.request_id = ctx["request_id"]
        if self.ctx['id'] not in CACHE.container_chaining:
            LOG.warning("Unknown Project ID {}".format(self.ctx['id']))
            # TODO (asteroide): add a better exception handler
            raise Exception("Unknown Project ID {}".format(self.ctx['id']))
        self.container_chaining = CACHE.container_chaining[self.ctx['id']]
        ctx["container_chaining"] = copy.deepcopy(self.container_chaining)
        LOG.info("self.container_chaining={}".format(self.container_chaining))
        self.pdp_container = self.container_chaining[0]["container_id"]
        self.run()

    def run(self):
        notify(request_id=self.request_id, container_id=self.pdp_container, payload=self.ctx)
        cpt = 0
        while cpt < self.req_max_delay*10:
            time.sleep(0.1)
            cpt += 1
            if CACHE.authz_requests[self.request_id]:
                self.result = CACHE.authz_requests[self.request_id]
                return
        LOG.warning("Request {} has timed out".format(self.request_id))

    def is_authz(self):
        if not self.result:
            return False
        authz_results = []
        for key in self.result["pdp_set"]:
            if "effect" in self.result["pdp_set"][key]:
                if self.result["pdp_set"][key]["effect"] == "grant":
                    # the pdp is a authorization PDP and grant the request
                    authz_results.append(True)
                elif self.result["pdp_set"][key]["effect"] == "passed":
                    # the pdp is not a authorization PDP (session or delegation) and had run normally
                    authz_results.append(True)
                elif self.result["pdp_set"][key]["effect"] == "unset":
                    # the pdp is not a authorization PDP (session or delegation) and had not yep run
                    authz_results.append(True)
                else:
                    # the pdp is (or not) a authorization PDP and had run badly
                    authz_results.append(False)
        if list(itertools.accumulate(authz_results, lambda x, y: x & y))[-1]:
            self.result["pdp_set"]["effect"] = "grant"
        if self.result:
            if "pdp_set" in self.result and self.result["pdp_set"]["effect"] == "grant":
                return True
        return False


class Router(object):
    """
    Route requests to all components.
    """

    __version__ = "0.1.0"
    cache_requests = {}

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
    def check_pdp(ctx):
        _ctx = copy.deepcopy(ctx)
        keystone_id = _ctx.pop('id')
        # LOG.info("_ctx {}".format(_ctx))
        ext = call("moon_manager", method="get_pdp", ctx=_ctx, args={})
        # LOG.info("check_pdp {}".format(ext))
        if "error" in ext:
            return False
        keystone_id_list = map(lambda x: x["keystone_project_id"], ext['pdps'].values())
        if not ext['pdps'] or keystone_id not in keystone_id_list:
            if CONF.slave.slave_name:
                _ctx['call_master'] = True
                # update from master if exist and test again
                LOG.info("Need to update from master {}".format(keystone_id))
                ext = call("moon_manager", method="get_pdp", ctx=_ctx, args={})
                if "error" in ext:
                    return False
                keystone_id_list = map(lambda x: x["keystone_project_id"], ext['pdps'].values())
                if not ext['pdps'] or keystone_id not in keystone_id_list:
                    return False
                else:
                    # Must update from Master
                    _ctx["keystone_id"] = keystone_id
                    _ctx["pdp_id"] = None
                    _ctx["security_pipeline"] = None
                    _ctx['call_master'] = False
                    pdp_value = {}
                    for pdp_id, pdp_value in ext["pdps"].items():
                        if keystone_id == pdp_value["keystone_project_id"]:
                            _ctx["pdp_id"] = keystone_id
                            _ctx["security_pipeline"] = pdp_value["security_pipeline"]
                            break
                    call("moon_manager", method="update_from_master", ctx=_ctx, args=pdp_value)
                    CACHE.update()
                    return True
            else:
                # return False otherwise
                return False
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
                    result = call("moon_manager", method=ctx["method"], ctx=ctx, args=args)
                    if ctx["method"] == "get_pdp":
                        _ctx = copy.deepcopy(ctx)
                        _ctx["call_master"] = True
                        result2 = call("moon_manager", method=ctx["method"], ctx=_ctx, args=args)
                        result["pdps"].update(result2["pdps"])
                    self.send_update(api=ctx["method"], ctx=ctx, args=args)
                    return result
                if component == "function":
                    if ctx["method"] == "return_authz":
                        request_id = ctx["request_id"]
                        CACHE.authz_requests[request_id] = args
                        return args
                    elif self.check_pdp(ctx):
                        req_id = uuid4().hex
                        CACHE.authz_requests[req_id] = {}
                        ctx["request_id"] = req_id
                        req = AuthzRequest(ctx, args)
                        # result = copy.deepcopy(req.result)
                        if req.is_authz():
                            return {"authz": True,
                                    "pdp_id": ctx["id"],
                                    "ctx": ctx, "args": args}
                        return {"authz": False,
                                "error": {'code': 403, 'title': 'Authz Error',
                                          'description': "The authz request is refused."},
                                "pdp_id": ctx["id"],
                                "ctx": ctx, "args": args}
                    return {"result": False,
                            "error": {'code': 500, 'title': 'Moon Error',
                                      'description': "Function component not found."},
                            "pdp_id": ctx["id"],
                            "ctx": ctx, "args": args}

        # TODO (asteroide): must raise an exception here ?
        return {"result": False,
                "error": {'code': 500, 'title': 'Moon Error', 'description': "Endpoint method not found."},
                "intra_extension_id": ctx["id"],
                "ctx": ctx, "args": args}

