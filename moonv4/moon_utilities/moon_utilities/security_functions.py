# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import copy
import re
import types
import requests
from oslo_log import log as logging
from oslo_config import cfg
import oslo_messaging
from moon_utilities import exceptions

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


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
    if not user:
        user = CONF.keystone.user
    if not password:
        password = CONF.keystone.password
    if not domain:
        domain = CONF.keystone.domain
    if not project:
        project = CONF.keystone.project
    if not url:
        url = CONF.keystone.url
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

    req = requests.post("{}/auth/tokens".format(url),
                        json=data_auth, headers=headers,
                        verify=CONF.keystone.server_crt)

    if req.status_code in (200, 201, 204):
        headers['X-Auth-Token'] = req.headers['X-Subject-Token']
        return headers
    LOG.error(req.text)
    raise exceptions.KeystoneError


def logout(headers, url=None):
    if not url:
        url = CONF.keystone.url
    headers['X-Subject-Token'] = headers['X-Auth-Token']
    req = requests.delete("{}/auth/tokens".format(url), headers=headers, verify=CONF.keystone.server_crt)
    if req.status_code in (200, 201, 204):
        return
    LOG.error(req.text)
    raise exceptions.KeystoneError

__transport_master = oslo_messaging.get_transport(cfg.CONF, CONF.slave.master_url)
__transport = oslo_messaging.get_transport(CONF)

__n_transport = oslo_messaging.get_notification_transport(CONF)
__n_notifier = oslo_messaging.Notifier(__n_transport,
                                       'router.host',
                                       driver='messagingv2',
                                       topics=['authz-workers'])
__n_notifier = __n_notifier.prepare(publisher_id='router')

__targets = {}


def notify(request_id, container_id, payload, event_type="authz"):
    ctxt = {
        'request_id': request_id,
        'container_id': container_id
    }
    __n_notifier.critical(ctxt, event_type, payload=payload)
    # FIXME (asteroide): the notification mus be done 2 times otherwise the notification
    #                    may not be sent (need to search why)
    __n_notifier.critical(ctxt, event_type, payload=payload)


def call(endpoint, ctx=None, method="route", **kwargs):
    if not ctx:
        ctx = dict()
    if endpoint not in __targets:
        __targets[endpoint] = dict()
        __targets[endpoint]["endpoint"] = oslo_messaging.Target(topic=endpoint, version='1.0')
        __targets[endpoint]["client"] = dict()
        __targets[endpoint]["client"]["internal"] = oslo_messaging.RPCClient(__transport,
                                                                             __targets[endpoint]["endpoint"])
        __targets[endpoint]["client"]["external"] = oslo_messaging.RPCClient(__transport_master,
                                                                             __targets[endpoint]["endpoint"])
    if 'call_master' in ctx and ctx['call_master'] and CONF.slave.master_url:
        client = __targets[endpoint]["client"]["external"]
        LOG.info("Calling master {} on {}...".format(method, endpoint))
    else:
        client = __targets[endpoint]["client"]["internal"]
        LOG.info("Calling {} on {}...".format(method, endpoint))
    result = copy.deepcopy(client.call(ctx, method, **kwargs))
    del client
    return result


class Context:

    def __init__(self, _keystone_project_id, _subject, _object, _action, _request_id):
        from moon_db.core import PDPManager, ModelManager, PolicyManager
        self.PolicyManager = PolicyManager
        self.ModelManager = ModelManager
        self.PDPManager = PDPManager
        self.__keystone_project_id = _keystone_project_id
        self.__pdp_id = None
        self.__pdp_value = None
        for _pdp_key, _pdp_value in PDPManager.get_pdp("admin").items():
            if _pdp_value["keystone_project_id"] == _keystone_project_id:
                self.__pdp_id = _pdp_key
                self.__pdp_value = copy.deepcopy(_pdp_value)
                break
        self.__subject = _subject
        self.__object = _object
        self.__action = _action
        self.__current_request = None
        self.__request_id = _request_id
        self.__index = 0
        self.__init_initial_request()
        self.__headers = []
        policies = PolicyManager.get_policies("admin")
        models = ModelManager.get_models("admin")
        for policy_id in self.__pdp_value["security_pipeline"]:
            model_id = policies[policy_id]["model_id"]
            for meta_rule in models[model_id]["meta_rules"]:
                self.__headers.append(meta_rule)
        self.__meta_rules = ModelManager.get_meta_rules("admin")
        self.__pdp_set = {}
        self.__init_pdp_set()

    def __init_initial_request(self):
        subjects = self.PolicyManager.get_subjects("admin", policy_id=None)
        for _subject_id, _subject_dict in subjects.items():
            if _subject_dict["name"] == self.__subject:
                self.__subject = _subject_id
                break
        else:
            raise exceptions.SubjectUnknown("Cannot find subject {}".format(self.__subject))
        objects = self.PolicyManager.get_objects("admin", policy_id=None)
        for _object_id, _object_dict in objects.items():
            if _object_dict["name"] == self.__object:
                self.__object = _object_id
                break
        else:
            raise exceptions.ObjectUnknown("Cannot find object {}".format(self.__object))
        actions = self.PolicyManager.get_actions("admin", policy_id=None)
        for _action_id, _action_dict in actions.items():
            if _action_dict["name"] == self.__action:
                self.__action = _action_id
                break
        else:
            raise exceptions.ActionUnknown("Cannot find action {}".format(self.__action))
        self.__current_request = dict(self.initial_request)

    def __init_pdp_set(self):
        for header in self.__headers:
            self.__pdp_set[header] = dict()
            self.__pdp_set[header]["meta_rules"] = self.__meta_rules[header]
            self.__pdp_set[header]["target"] = self.__add_target(header)
            # TODO (asteroide): the following information must be retrieve somewhere
            self.__pdp_set[header]["effect"] = "unset"
        self.__pdp_set["effect"] = "deny"

    @staticmethod
    def update_target(context):
        from moon_db.core import PDPManager, ModelManager, PolicyManager
        # result = dict()
        current_request = context['current_request']
        _subject = current_request.get("subject")
        _object = current_request.get("object")
        _action = current_request.get("action")
        meta_rule_id = context['headers'][context['index']]
        policy_id = PolicyManager.get_policy_from_meta_rules("admin", meta_rule_id)
        meta_rules = ModelManager.get_meta_rules("admin")
        # for meta_rule_id in meta_rules:
        for sub_cat in meta_rules[meta_rule_id]['subject_categories']:
            if sub_cat not in context["pdp_set"][meta_rule_id]["target"]:
                context["pdp_set"][meta_rule_id]["target"][sub_cat] = []
            for assign in PolicyManager.get_subject_assignments("admin", policy_id, _subject, sub_cat).values():
                for assign in assign["assignments"]:
                    if assign not in context["pdp_set"][meta_rule_id]["target"][sub_cat]:
                        context["pdp_set"][meta_rule_id]["target"][sub_cat].append(assign)
        for obj_cat in meta_rules[meta_rule_id]['object_categories']:
            if obj_cat not in context["pdp_set"][meta_rule_id]["target"]:
                context["pdp_set"][meta_rule_id]["target"][obj_cat] = []
            for assign in PolicyManager.get_object_assignments("admin", policy_id, _object, obj_cat).values():
                for assign in assign["assignments"]:
                    if assign not in context["pdp_set"][meta_rule_id]["target"][obj_cat]:
                        context["pdp_set"][meta_rule_id]["target"][obj_cat].append(assign)
        for act_cat in meta_rules[meta_rule_id]['action_categories']:
            if act_cat not in context["pdp_set"][meta_rule_id]["target"]:
                context["pdp_set"][meta_rule_id]["target"][act_cat] = []
            for assign in PolicyManager.get_action_assignments("admin", policy_id, _action, act_cat).values():
                for assign in assign["assignments"]:
                    if assign not in context["pdp_set"][meta_rule_id]["target"][act_cat]:
                        context["pdp_set"][meta_rule_id]["target"][act_cat].append(assign)
        # context["pdp_set"][meta_rule_id]["target"].update(result)

    def __add_target(self, meta_rule_id):
        result = dict()
        _subject = self.__current_request["subject"]
        _object = self.__current_request["object"]
        _action = self.__current_request["action"]
        meta_rules = self.ModelManager.get_meta_rules("admin")
        policy_id = self.PolicyManager.get_policy_from_meta_rules("admin", meta_rule_id)
        for sub_cat in meta_rules[meta_rule_id]['subject_categories']:
            if sub_cat not in result:
                result[sub_cat] = []
            for assign in self.PolicyManager.get_subject_assignments("admin", policy_id, _subject, sub_cat).values():
                result[sub_cat].extend(assign["assignments"])
        for obj_cat in meta_rules[meta_rule_id]['object_categories']:
            if obj_cat not in result:
                result[obj_cat] = []
            for assign in self.PolicyManager.get_object_assignments("admin", policy_id, _object, obj_cat).values():
                result[obj_cat].extend(assign["assignments"])
        for act_cat in meta_rules[meta_rule_id]['action_categories']:
            if act_cat not in result:
                result[act_cat] = []
            for assign in self.PolicyManager.get_action_assignments("admin", policy_id, _action, act_cat).values():
                result[act_cat].extend(assign["assignments"])
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
        self.__index = 0

    @property
    def pdp_set(self):
        return self.__pdp_set

    @pdp_set.setter
    def pdp_set(self, value):
        raise Exception("You are not allowed to modify the pdp_set")

    @pdp_set.deleter
    def pdp_set(self):
        self.__pdp_set = {}
