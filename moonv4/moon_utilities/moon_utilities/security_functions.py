# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import copy
import re
import os
import types
import requests
import time
from functools import wraps
from flask import request
import logging
from moon_utilities import exceptions
from moon_utilities import configuration

LOG = logging.getLogger("moon.utilities." + __name__)

keystone_config = configuration.get_configuration("openstack/keystone")["openstack/keystone"]
# slave = configuration.get_configuration(configuration.SLAVE)["slave"]

__targets = {}


def filter_input(func_or_str):

    def __filter(string):
        if string and type(string) is str:
            return "".join(re.findall("[\w\- +]*", string))
        return string

    def __filter_dict(arg):
        result = dict()
        for key in arg.keys():
            if key == "email":
                result["email"] = __filter_email(arg[key])
            elif key == "password":
                result["password"] = arg['password']
            else:
                result[key] = __filter(arg[key])
        return result

    def __filter_email(string):
        if string and type(string) is str:
            return "".join(re.findall("[\w@\._\- +]*", string))
        return string

    def wrapped(*args, **kwargs):
        _args = []
        for arg in args:
            if isinstance(arg, str):
                arg = __filter(arg)
            elif isinstance(arg, list):
                arg = [__filter(item) for item in arg]
            elif isinstance(arg, tuple):
                arg = (__filter(item) for item in arg)
            elif isinstance(arg, dict):
                arg = __filter_dict(arg)
            _args.append(arg)
        for arg in kwargs:
            if type(kwargs[arg]) is str:
                kwargs[arg] = __filter(kwargs[arg])
            if isinstance(kwargs[arg], str):
                kwargs[arg] = __filter(kwargs[arg])
            elif isinstance(kwargs[arg], list):
                kwargs[arg] = [__filter(item) for item in kwargs[arg]]
            elif isinstance(kwargs[arg], tuple):
                kwargs[arg] = (__filter(item) for item in kwargs[arg])
            elif isinstance(kwargs[arg], dict):
                kwargs[arg] = __filter_dict(kwargs[arg])
        return func_or_str(*_args, **kwargs)

    if isinstance(func_or_str, str):
        return __filter(func_or_str)
    if isinstance(func_or_str, list):
        return [__filter(item) for item in func_or_str]
    if isinstance(func_or_str, tuple):
        return (__filter(item) for item in func_or_str)
    if isinstance(func_or_str, dict):
        return __filter_dict(func_or_str)
    if isinstance(func_or_str, types.FunctionType):
        return wrapped
    return None


def enforce(action_names, object_name, **extra):
    """Fake version of the enforce decorator"""
    def wrapper_func(func):
        def wrapper_args(*args, **kwargs):
            # LOG.info("kwargs={}".format(kwargs))
            # kwargs['user_id'] = kwargs.pop('user_id', "admin")
            # LOG.info("Calling enforce on {} with args={} kwargs={}".format(func.__name__, args, kwargs))
            return func(*args, **kwargs)
        return wrapper_args
    return wrapper_func


def login(user=None, password=None, domain=None, project=None, url=None):
    start_time = time.time()
    if not user:
        user = keystone_config['user']
    if not password:
        password = keystone_config['password']
    if not domain:
        domain = keystone_config['domain']
    if not project:
        project = keystone_config['project']
    if not url:
        url = keystone_config['url']
    headers = {
        "Content-Type": "application/json"
    }
    data_auth = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "id": domain
                        },
                        "name": user,
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "id": domain
                    },
                    "name": project
                }
            }
        }
    }

    while True:
        req = requests.post("{}/auth/tokens".format(url),
                            json=data_auth, headers=headers,
                            verify=keystone_config['certificate'])

        if req.status_code in (200, 201, 204):
            headers['X-Auth-Token'] = req.headers['X-Subject-Token']
            return headers
        LOG.warning("Waiting for Keystone...")
        if time.time() - start_time == 100:
            LOG.error(req.text)
            raise exceptions.KeystoneError
        time.sleep(5)


def logout(headers, url=None):
    if not url:
        url = keystone_config['url']
    headers['X-Subject-Token'] = headers['X-Auth-Token']
    req = requests.delete("{}/auth/tokens".format(url), headers=headers, verify=keystone_config['certificate'])
    if req.status_code in (200, 201, 204):
        return
    LOG.error(req.text)
    raise exceptions.KeystoneError


class Context:

    def __init__(self, init_context, cache):
        self.cache = cache
        self.__keystone_project_id = init_context.get("project_id")
        self.__pdp_id = None
        self.__pdp_value = None
        for _pdp_key, _pdp_value in self.cache.pdp.items():
            if _pdp_value["keystone_project_id"] == self.__keystone_project_id:
                self.__pdp_id = _pdp_key
                self.__pdp_value = copy.deepcopy(_pdp_value)
                break
        if not self.__pdp_value:
            raise exceptions.AuthzException(
                "Cannot create context for authz "
                "with Keystone project ID {}".format(
                    self.__keystone_project_id
            ))
        self.__subject = init_context.get("subject_name")
        self.__object = init_context.get("object_name")
        self.__action = init_context.get("action_name")
        self.__current_request = None
        self.__request_id = init_context.get("req_id")
        self.__cookie = init_context.get("cookie")
        self.__manager_url = init_context.get("manager_url")
        self.__interface_name = init_context.get("interface_name")
        self.__index = -1
        # self.__init_initial_request()
        self.__headers = []
        policies = self.cache.policies
        models = self.cache.models
        for policy_id in self.__pdp_value["security_pipeline"]:
            model_id = policies[policy_id]["model_id"]
            for meta_rule in models[model_id]["meta_rules"]:
                self.__headers.append(meta_rule)
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
        return self.__pdp_set[self.__headers[self.__index]]['effect']

    @current_state.setter
    def current_state(self, state):
        if state not in ("grant", "deny", "passed"):
            state = "passed"
        self.__pdp_set[self.__headers[self.__index]]['effect'] = state

    @current_state.deleter
    def current_state(self):
        self.__pdp_set[self.__headers[self.__index]]['effect'] = "unset"

    @property
    def current_policy_id(self):
        return self.__pdp_value["security_pipeline"][self.__index]

    @current_policy_id.setter
    def current_policy_id(self, value):
        pass

    @current_policy_id.deleter
    def current_policy_id(self):
        pass

    def __init_current_request(self):
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
        for header in self.__headers:
            self.__pdp_set[header] = dict()
            self.__pdp_set[header]["meta_rules"] = self.__meta_rules[header]
            self.__pdp_set[header]["target"] = self.__add_target(header)
            self.__pdp_set[header]["effect"] = "unset"
        self.__pdp_set["effect"] = "deny"

    # def update_target(self, context):
    #     # result = dict()
    #     current_request = context['current_request']
    #     _subject = current_request.get("subject")
    #     _object = current_request.get("object")
    #     _action = current_request.get("action")
    #     meta_rule_id = context['headers'][context['index']]
    #     policy_id = self.cache.get_policy_from_meta_rules(meta_rule_id)
    #     meta_rules = self.cache.meta_rules()
    #     # for meta_rule_id in meta_rules:
    #     for sub_cat in meta_rules[meta_rule_id]['subject_categories']:
    #         if sub_cat not in context["pdp_set"][meta_rule_id]["target"]:
    #             context["pdp_set"][meta_rule_id]["target"][sub_cat] = []
    #         for assign in self.cache.get_subject_assignments(policy_id, _subject, sub_cat).values():
    #             for assign in assign["assignments"]:
    #                 if assign not in context["pdp_set"][meta_rule_id]["target"][sub_cat]:
    #                     context["pdp_set"][meta_rule_id]["target"][sub_cat].append(assign)
    #     for obj_cat in meta_rules[meta_rule_id]['object_categories']:
    #         if obj_cat not in context["pdp_set"][meta_rule_id]["target"]:
    #             context["pdp_set"][meta_rule_id]["target"][obj_cat] = []
    #         for assign in self.cache.get_object_assignments(policy_id, _object, obj_cat).values():
    #             for assign in assign["assignments"]:
    #                 if assign not in context["pdp_set"][meta_rule_id]["target"][obj_cat]:
    #                     context["pdp_set"][meta_rule_id]["target"][obj_cat].append(assign)
    #     for act_cat in meta_rules[meta_rule_id]['action_categories']:
    #         if act_cat not in context["pdp_set"][meta_rule_id]["target"]:
    #             context["pdp_set"][meta_rule_id]["target"][act_cat] = []
    #         for assign in self.cache.get_action_assignments(policy_id, _action, act_cat).values():
    #             for assign in assign["assignments"]:
    #                 if assign not in context["pdp_set"][meta_rule_id]["target"][act_cat]:
    #                     context["pdp_set"][meta_rule_id]["target"][act_cat].append(assign)
    #     # context["pdp_set"][meta_rule_id]["target"].update(result)

    """build target from meta_rule
    
    Target is dict of categories as keys ; and the value of each category will be 
    a list of assignments
    
    """
    def __add_target(self, meta_rule_id):
        result = dict()
        _subject = self.__current_request["subject"]
        _object = self.__current_request["object"]
        _action = self.__current_request["action"]
        meta_rules = self.cache.meta_rules
        policy_id = self.cache.get_policy_from_meta_rules(meta_rule_id)
        for sub_cat in meta_rules[meta_rule_id]['subject_categories']:
            if sub_cat not in result:
                result[sub_cat] = []
            result[sub_cat].extend(
                self.cache.get_subject_assignments(policy_id, _subject, sub_cat))
        for obj_cat in meta_rules[meta_rule_id]['object_categories']:
            if obj_cat not in result:
                result[obj_cat] = []
            result[obj_cat].extend(
                self.cache.get_object_assignments(policy_id, _object, obj_cat))
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
            headers=self.__headers,
            pdp_set=self.__pdp_set,
            index=self.__index
        )

    def to_dict(self):
        return {
            "initial_request": copy.deepcopy(self.initial_request),
            "current_request": copy.deepcopy(self.__current_request),
            "headers": copy.deepcopy(self.__headers),
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
            self.__current_request = copy.deepcopy(self.initial_request)
        return self.__current_request

    @current_request.setter
    def current_request(self, value):
        self.__current_request = copy.deepcopy(value)
        # Note (asteroide): if the current request is modified, we must update the PDP Set.
        self.__init_pdp_set()

    @current_request.deleter
    def current_request(self):
        self.__current_request = {}
        self.__pdp_set = {}

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        self.__headers = headers

    @headers.deleter
    def headers(self):
        self.__headers = list()

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

TOKENS = {}


def check_token(token, url=None):
    _verify = False
    if keystone_config['certificate']:
        _verify = keystone_config['certificate']
    try:
        os.environ.pop("http_proxy")
        os.environ.pop("https_proxy")
    except KeyError:
        pass
    if not url:
        url = keystone_config['url']
    headers = {
        "Content-Type": "application/json",
        'X-Subject-Token': token,
        'X-Auth-Token': token,
    }
    if not keystone_config['check_token']:
        # TODO (asteroide): must send the admin id
        return "admin" if not token else token
    elif keystone_config['check_token'].lower() in ("false", "no", "n"):
        # TODO (asteroide): must send the admin id
        return "admin" if not token else token
    if keystone_config['check_token'].lower() in ("yes", "y", "true"):
        if token in TOKENS:
            delta = time.mktime(TOKENS[token]["expires_at"]) - time.mktime(time.gmtime())
            if delta > 0:
                return TOKENS[token]["user"]
            raise exceptions.KeystoneError
        else:
            req = requests.get("{}/auth/tokens".format(url), headers=headers, verify=_verify)
            if req.status_code in (200, 201):
                # Note (asteroide): the time stamps is not in ISO 8601, so it is necessary to delete
                # characters after the dot
                token_time = req.json().get("token").get("expires_at").split(".")
                TOKENS[token] = dict()
                TOKENS[token]["expires_at"] = time.strptime(token_time[0], "%Y-%m-%dT%H:%M:%S")
                TOKENS[token]["user"] = req.json().get("token").get("user").get("id")
                return TOKENS[token]["user"]
            LOG.error("{} - {}".format(req.status_code, req.text))
            raise exceptions.KeystoneError
    elif keystone_config['check_token'].lower() == "strict":
        req = requests.head("{}/auth/tokens".format(url), headers=headers, verify=_verify)
        if req.status_code in (200, 201):
            return token
        LOG.error("{} - {}".format(req.status_code, req.text))
        raise exceptions.KeystoneError
    raise exceptions.KeystoneError


def check_auth(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-Auth-Token')
        token = check_token(token)
        if not token:
            raise exceptions.AuthException
        user_id = kwargs.pop("user_id", token)
        result = function(*args, **kwargs, user_id=user_id)
        return result
    return wrapper
