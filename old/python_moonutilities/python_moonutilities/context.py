# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import copy
import logging
from python_moonutilities import exceptions

logger = logging.getLogger("moon.utilities." + __name__)


class Context:

    def __init__(self, init_context, cache):
        if init_context is None:
            raise Exception("Invalid context content object")

        self.cache = cache
        self.__keystone_project_id = init_context.get("project_id")
        self.__pdp_id = self.cache.get_pdp_from_keystone_project(self.__keystone_project_id)

        if not self.__pdp_id:
            raise exceptions.AuthzException(
                "Cannot create context for authz "
                "with Keystone project ID {}".format(
                    self.__keystone_project_id
                ))
        self.__pdp_value = copy.deepcopy(self.cache.pdp[self.__pdp_id])

        self.__subject = init_context.get("subject_name")
        self.__object = init_context.get("object_name")
        self.__action = init_context.get("action_name")
        self.__request_id = init_context.get("req_id")
        self.__cookie = init_context.get("cookie")
        self.__manager_url = init_context.get("manager_url")
        self.__interface_name = init_context.get("interface_name")
        self.__current_request = None

        self.__index = -1
        # self.__init_initial_request()
        self.__meta_rule_ids = self.cache.get_meta_rule_ids_from_pdp_value(self.__pdp_value)
        self.__meta_rules = self.cache.meta_rules

        self.__pdp_set = {}
        # self.__init_pdp_set()

    def delete_cache(self):
        self.cache = {}

    def set_cache(self, cache):
        self.cache = cache

    def increment_index(self):
        self.__index += 1
        self.__init_current_request()
        self.__init_pdp_set()

    @property
    def current_state(self):
        self.__validate_meta_rule_content(self.__pdp_set[self.__meta_rule_ids[self.__index]])
        return self.__pdp_set[self.__meta_rule_ids[self.__index]]['effect']

    @current_state.setter
    def current_state(self, state):
        if state not in ("grant", "deny", "passed"):
            state = "passed"
        self.__validate_meta_rule_content(self.__pdp_set[self.__meta_rule_ids[self.__index]])
        self.__pdp_set[self.__meta_rule_ids[self.__index]]['effect'] = state

    @current_state.deleter
    def current_state(self):
        self.__validate_meta_rule_content(self.__pdp_set[self.__meta_rule_ids[self.__index]])
        self.__pdp_set[self.__meta_rule_ids[self.__index]]['effect'] = "unset"

    @property
    def current_policy_id(self):
        if "security_pipeline" not in self.__pdp_value:
            raise exceptions.AuthzException('Cannot find security_pipeline key within pdp.')
        return self.__pdp_value["security_pipeline"][self.__index]

    @current_policy_id.setter
    def current_policy_id(self, value):
        pass

    @current_policy_id.deleter
    def current_policy_id(self):
        pass

    def __init_current_request(self):
        if "security_pipeline" not in self.__pdp_value:
            raise exceptions.PdpContentError
        self.__subject = self.cache.get_subject(
            self.__pdp_value["security_pipeline"][self.__index],
            self.__subject)
        self.__object = self.cache.get_object(
            self.__pdp_value["security_pipeline"][self.__index],
            self.__object)
        self.__action = self.cache.get_action(
            self.__pdp_value["security_pipeline"][self.__index],
            self.__action)
        self.__current_request = dict(self.initial_request)

    def __init_pdp_set(self):
        for meta_rule_id in self.__meta_rule_ids:
            self.__pdp_set[meta_rule_id] = dict()
            self.__pdp_set[meta_rule_id]["meta_rules"] = self.__meta_rules[meta_rule_id]
            self.__pdp_set[meta_rule_id]["target"] = self.__add_target(meta_rule_id)
            self.__pdp_set[meta_rule_id]["effect"] = "unset"
        self.__pdp_set["effect"] = "deny"

    def update_target(self):
        for meta_rule_id in self.__meta_rule_ids:
            result = dict()
            _subject = self.__current_request["subject"]
            _object = self.__current_request["object"]
            _action = self.__current_request["action"]

            meta_rules = self.cache.meta_rules
            policy_id = self.cache.get_policy_from_meta_rules(meta_rule_id)

            if 'subject_categories' not in meta_rules[meta_rule_id]:
                raise exceptions.MetaRuleContentError(" 'subject_categories' key not found ")

            self.cache.update_assignments(policy_id)

            for sub_cat in meta_rules[meta_rule_id]['subject_categories']:
                if sub_cat not in result:
                    result[sub_cat] = []
                result[sub_cat].extend(
                    self.cache.get_subject_assignments(policy_id, _subject, sub_cat))

            if 'object_categories' not in meta_rules[meta_rule_id]:
                raise exceptions.MetaRuleContentError(" 'object_categories' key not found ")

            for obj_cat in meta_rules[meta_rule_id]['object_categories']:
                if obj_cat not in result:
                    result[obj_cat] = []
                result[obj_cat].extend(
                    self.cache.get_object_assignments(policy_id, _object, obj_cat))

            if 'action_categories' not in meta_rules[meta_rule_id]:
                raise exceptions.MetaRuleContentError(" 'action_categories' key not found ")

            for act_cat in meta_rules[meta_rule_id]['action_categories']:
                if act_cat not in result:
                    result[act_cat] = []
                result[act_cat].extend(
                    self.cache.get_action_assignments(policy_id, _action, act_cat))

            self.__pdp_set[meta_rule_id]["target"] = result

    def __add_target(self, meta_rule_id):
        """build target from meta_rule

        Target is dict of categories as keys ; and the value of each category
        will be a list of assignments

        """
        result = dict()
        _subject = self.__current_request["subject"]
        _object = self.__current_request["object"]
        _action = self.__current_request["action"]

        meta_rules = self.cache.meta_rules
        policy_id = self.cache.get_policy_from_meta_rules(meta_rule_id)

        if 'subject_categories' not in meta_rules[meta_rule_id]:
            raise exceptions.MetaRuleContentError(" 'subject_categories' key not found ")

        for sub_cat in meta_rules[meta_rule_id]['subject_categories']:
            if sub_cat not in result:
                result[sub_cat] = []
            result[sub_cat].extend(
                self.cache.get_subject_assignments(policy_id, _subject, sub_cat))

        if 'object_categories' not in meta_rules[meta_rule_id]:
            raise exceptions.MetaRuleContentError(" 'object_categories' key not found ")

        for obj_cat in meta_rules[meta_rule_id]['object_categories']:
            if obj_cat not in result:
                result[obj_cat] = []
            result[obj_cat].extend(
                self.cache.get_object_assignments(policy_id, _object, obj_cat))

        if 'action_categories' not in meta_rules[meta_rule_id]:
            raise exceptions.MetaRuleContentError(" 'action_categories' key not found ")

        for act_cat in meta_rules[meta_rule_id]['action_categories']:
            if act_cat not in result:
                result[act_cat] = []
            result[act_cat].extend(
                self.cache.get_action_assignments(policy_id, _action, act_cat))

        return result

    def __repr__(self):
        return """PDP ID: {id}
current_request: {current_request}
request_id: {request_id}
index: {index}
headers: {headers}
pdp_set: {pdp_set}
        """.format(
            id=self.__pdp_id,
            current_request=self.__current_request,
            request_id=self.__request_id,
            headers=self.__meta_rule_ids,
            pdp_set=self.__pdp_set,
            index=self.__index
        )

    def to_dict(self):
        return {
            "initial_request": copy.deepcopy(self.initial_request),
            "current_request": copy.deepcopy(self.__current_request),
            "headers": copy.deepcopy(self.__meta_rule_ids),
            "index": copy.deepcopy(self.__index),
            "pdp_set": copy.deepcopy(self.__pdp_set),
            "request_id": copy.deepcopy(self.__request_id),
            "manager_url": copy.deepcopy(self.__manager_url),
            "interface_name": copy.deepcopy(self.__interface_name),
        }

    @property
    def request_id(self):
        return self.__request_id

    @request_id.setter
    def request_id(self, value):
        raise Exception("You cannot update the request_id")

    @request_id.deleter
    def request_id(self):
        raise Exception("You cannot update the request_id")

    @property
    def manager_url(self):
        return self.__manager_url

    @manager_url.setter
    def manager_url(self, value):
        raise Exception("You cannot update the manager_url")

    @manager_url.deleter
    def manager_url(self):
        raise Exception("You cannot update the manager_url")

    @property
    def interface_name(self):
        return self.__interface_name

    @interface_name.setter
    def interface_name(self, value):
        raise Exception("You cannot update the interface_name")

    @interface_name.deleter
    def interface_name(self):
        raise Exception("You cannot update the interface_name")

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, value):
        raise Exception("You cannot update the cookie")

    @cookie.deleter
    def cookie(self):
        raise Exception("You cannot delete the cookie")

    @property
    def initial_request(self):
        return {
            "subject": self.__subject,
            "object": self.__object,
            "action": self.__action,
        }

    @initial_request.setter
    def initial_request(self, value):
        raise Exception("You are not allowed to update the initial_request")

    @initial_request.deleter
    def initial_request(self):
        raise Exception("You are not allowed to delete the initial_request")

    @property
    def current_request(self):
        if not self.__current_request:
            self.__current_request = dict(self.initial_request)
        return self.__current_request

    @current_request.setter
    def current_request(self, value):

        self.__current_request = copy.deepcopy(value)
        # Note (asteroide): if the current request is modified,
        # we must update the PDP Set.
        self.__init_pdp_set()

    @current_request.deleter
    def current_request(self):
        self.__current_request = {}
        self.__pdp_set = {}

    '''
        [Note ] Refactor name of headers to meta_rule_ids done ,
         may need to refactor getter and setter of headers
    '''

    @property
    def headers(self):
        return self.__meta_rule_ids

    @headers.setter
    def headers(self, meta_rule_ids):
        self.__meta_rule_ids = meta_rule_ids

    @headers.deleter
    def headers(self):
        self.__meta_rule_ids = list()

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, index):
        self.__index += 1

    @index.deleter
    def index(self):
        self.__index = -1

    @property
    def pdp_set(self):
        return self.__pdp_set

    @pdp_set.setter
    def pdp_set(self, value):
        raise Exception("You are not allowed to modify the pdp_set")

    @pdp_set.deleter
    def pdp_set(self):
        self.__pdp_set = {}

    def __validate_meta_rule_content(self, meta_rules):
        if 'effect' not in meta_rules:
            logger.error("meta_rules={}".format(meta_rules))
            raise exceptions.PdpContentError("effect not in meta_rules")
