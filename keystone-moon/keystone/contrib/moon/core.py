# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
import os
import json
import copy
import re
import six
import time
import types
import requests

from keystone.common import manager
from keystone.exception import UserNotFound
from oslo_log import log
from keystone.common import dependency
from keystone import exception
from oslo_config import cfg
from keystone.i18n import _
from keystone.common import extension

from keystone.contrib.moon.exception import *
from keystone.contrib.moon.algorithms import *

CONF = cfg.CONF
LOG = log.getLogger(__name__)

OPTS = [
    cfg.StrOpt('configuration_driver',
               default='keystone.contrib.moon.backends.memory.ConfigurationConnector',
               help='Configuration backend driver.'),
    cfg.StrOpt('tenant_driver',
               default='keystone.contrib.moon.backends.sql.TenantConnector',
               help='Tenant backend driver.'),
    cfg.StrOpt('authz_driver',
               default='keystone.contrib.moon.backends.flat.SuperExtensionConnector',
               help='Authorisation backend driver.'),
    cfg.StrOpt('intraextension_driver',
               default='keystone.contrib.moon.backends.sql.IntraExtensionConnector',
               help='IntraExtension backend driver.'),
    cfg.StrOpt('interextension_driver',
               default='keystone.contrib.moon.backends.sql.InterExtensionConnector',
               help='InterExtension backend driver.'),
    cfg.StrOpt('log_driver',
               default='keystone.contrib.moon.backends.flat.LogConnector',
               help='Logs backend driver.'),
    cfg.StrOpt('policy_directory',
               default='/etc/keystone/policies',
               help='Local directory where all policies are stored.'),
    cfg.StrOpt('root_policy_directory',
               default='policy_root',
               help='Local directory where Root IntraExtension configuration is stored.'),
    cfg.StrOpt('master',
               default='http://localhost:35357/',
               help='Address of the Moon master (if empty, the current Moon is the master).'),
    cfg.StrOpt('master_login',
               default='admin',
               help='Login of the Moon master.'),
    cfg.StrOpt('master_password',
               default='nomoresecrete',
               help='Password of the Moon master.'),
]

for option in OPTS:
    CONF.register_opt(option, group="moon")


def filter_input(func_or_str):

    def __filter(string):
        if string and type(string) in (str, unicode):
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
        if string and type(string) in (str, unicode):
            return "".join(re.findall("[\w@\._\- +]*", string))
        return string

    def wrapped(*args, **kwargs):
        _args = []
        for arg in args:
            if isinstance(arg, str) or isinstance(arg, unicode):
                arg = __filter(arg)
            elif isinstance(arg, list):
                arg = [__filter(item) for item in arg]
            elif isinstance(arg, tuple):
                arg = (__filter(item) for item in arg)
            elif isinstance(arg, dict):
                arg = __filter_dict(arg)
            _args.append(arg)
        for arg in kwargs:
            if type(kwargs[arg]) in (unicode, str):
                kwargs[arg] = __filter(kwargs[arg])
            if isinstance(kwargs[arg], str) or isinstance(kwargs[arg], unicode):
                kwargs[arg] = __filter(kwargs[arg])
            elif isinstance(kwargs[arg], list):
                kwargs[arg] = [__filter(item) for item in kwargs[arg]]
            elif isinstance(kwargs[arg], tuple):
                kwargs[arg] = (__filter(item) for item in kwargs[arg])
            elif isinstance(kwargs[arg], dict):
                kwargs[arg] = __filter_dict(kwargs[arg])
        return func_or_str(*_args, **kwargs)

    if isinstance(func_or_str, str) or isinstance(func_or_str, unicode):
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

    def wrap(func):
        _action_name_list = action_names
        _object_name = object_name
        dependency.resolve_future_dependencies()

        def wrapped(*args, **kwargs):
            root_api = dependency._REGISTRY["root_api"][0]
            admin_api = dependency._REGISTRY["admin_api"][0]
            moonlog_api = dependency._REGISTRY["moonlog_api"][0]
            tenant_api = dependency._REGISTRY["tenant_api"][0]
            returned_value_for_func = None
            try:
                user_id = args[1]
            except IndexError:
                user_id = kwargs['user_id']
            intra_extension_id = None
            intra_admin_extension_id = None

            intra_root_extension_id = root_api.root_extension_id
            try:
                intra_extension_id = args[2]
            except IndexError:
                if 'intra_extension_id' in kwargs:
                    intra_extension_id = kwargs['intra_extension_id']
                else:
                    intra_extension_id = intra_root_extension_id

            tenants_dict = tenant_api.driver.get_tenants_dict()
            if root_api.is_admin_subject(user_id):
                # TODO: check if there is no security hole here
                # moonlog_api.driver.info("Authorizing because it is the user admin of the root intra-extension")
                returned_value_for_func = func(*args, **kwargs)
            else:
                intra_extensions_dict = admin_api.driver.get_intra_extensions_dict()
                if intra_extension_id not in intra_extensions_dict:
                    # if id is not an intra_extension, maybe it is a tenant id
                    intra_extension_id = intra_root_extension_id
                    if intra_extension_id in tenants_dict:
                        # id is in fact a tenant id so, we must check against the Root intra_extension
                        intra_extension_id = intra_root_extension_id
                        LOG.warning("intra_extension_id is a tenant ID ({})".format(intra_extension_id))
                    else:
                        # id is not a known tenant ID, so we must check against the Root intra_extension
                        intra_extension_id = intra_root_extension_id
                        LOG.warning("Cannot manage because the intra-extension is unknown (fallback to the root intraextension)")
                for _tenant_id in tenants_dict:
                    if tenants_dict[_tenant_id]['intra_authz_extension_id'] == intra_extension_id or \
                                    tenants_dict[_tenant_id]['intra_admin_extension_id'] == intra_extension_id:
                        intra_admin_extension_id = tenants_dict[_tenant_id]['intra_admin_extension_id']
                        break
                if not intra_admin_extension_id:
                    moonlog_api.driver.warning("No Intra_Admin_Extension found, authorization granted by default.")
                    returned_value_for_func = func(*args, **kwargs)
                else:
                    objects_dict = admin_api.driver.get_objects_dict(intra_admin_extension_id)
                    object_name = intra_extensions_dict[intra_extension_id]['genre'] + '.' + _object_name
                    object_id = None
                    for _object_id in objects_dict:
                        if objects_dict[_object_id]['name'] == object_name:
                            object_id = _object_id
                            break
                    if not object_id:
                        objects_dict = admin_api.driver.get_objects_dict(intra_root_extension_id)
                        object_name = object_name.split(".")[-1]
                        for _object_id in objects_dict:
                            if objects_dict[_object_id]['name'] == object_name:
                                object_id = _object_id
                                break
                        if not object_id:
                            raise ObjectUnknown("enforce: Unknown object name: {}".format(object_name))
                        # if we found the object in intra_root_extension_id, so we change the intra_admin_extension_id
                        # into intra_root_extension_id and we modify the ID of the subject
                        subjects_dict = admin_api.driver.get_subjects_dict(intra_admin_extension_id)
                        try:
                            subject_name = subjects_dict[user_id]["name"]
                        except KeyError:
                            subject_name = None
                            # Try if user_id is a Keystone ID
                            try:
                                for _subject_id in subjects_dict:
                                    if subjects_dict[_subject_id]["keystone_id"] == user_id:
                                        subject_name = subjects_dict[_subject_id]["name"]
                            except KeyError:
                                raise SubjectUnknown()
                        intra_admin_extension_id = intra_root_extension_id
                        subjects_dict = admin_api.driver.get_subjects_dict(intra_admin_extension_id)
                        user_id = None
                        for _subject_id in subjects_dict:
                            if subjects_dict[_subject_id]["name"] == subject_name:
                                user_id = _subject_id
                        if not user_id:
                            raise SubjectUnknown("Subject {} Unknown for Root IntraExtension...".format(subject_name))
                    if type(_action_name_list) in (str, unicode):
                        action_name_list = (_action_name_list, )
                    else:
                        action_name_list = _action_name_list
                    actions_dict = admin_api.driver.get_actions_dict(intra_admin_extension_id)
                    action_id_list = list()
                    for _action_name in action_name_list:
                        for _action_id in actions_dict:
                            if actions_dict[_action_id]['name'] == _action_name:
                                action_id_list.append(_action_id)
                                break

                    authz_result = False
                    action_id = ""
                    for action_id in action_id_list:
                        res = admin_api.authz(intra_admin_extension_id, user_id, object_id, action_id)
                        moonlog_api.info("res={}".format(res))
                        if res:
                            authz_result = True
                        else:
                            moonlog_api.authz("No authorization for ({} {}-{}-{})".format(
                                intra_admin_extension_id,
                                user_id,
                                object_name,
                                actions_dict[action_id]['name']))
                            authz_result = False
                            break
                    if authz_result:
                        returned_value_for_func = func(*args, **kwargs)
                    else:
                        raise AuthzException("No authorization for ({} {}-{}-{})".format(
                                intra_admin_extension_id,
                                user_id,
                                object_name,
                                actions_dict[action_id]['name']))
            return returned_value_for_func
        return wrapped
    return wrap


@dependency.provider('configuration_api')
class ConfigurationManager(manager.Manager):

    driver_namespace = 'keystone.moon.configuration'

    def __init__(self):
        super(ConfigurationManager, self).__init__(CONF.moon.configuration_driver)

    @enforce("read", "templates")
    def get_policy_templates_dict(self, user_id):
        """
        Return a dictionary of all policy templates
        :return: {
            template_id1: {name: template_name, description: template_description},
            template_id2: {name: template_name, description: template_description},
            ...
            }
        """
        return self.driver.get_policy_templates_dict()

    @enforce("read", "templates")
    def get_policy_template_id_from_name(self, user_id, policy_template_name):
        policy_templates_dict = self.driver.get_policy_templates_dict()
        for policy_template_id in policy_templates_dict:
            if policy_templates_dict[policy_template_id]['name'] == policy_template_name:
                return policy_template_id
        return None

    @enforce("read", "aggregation_algorithms")
    def get_aggregation_algorithms_dict(self, user_id):
        """
        Return a dictionary of all aggregation algorithms
        :return: {
            aggre_algo_id1: {name: aggre_name, description: aggre_algo_description},
            aggre_algo_id2: {name: aggre_name, description: aggre_algo_description},
            ...
            }
        """
        return self.driver.get_aggregation_algorithms_dict()

    @enforce("read", "aggregation_algorithms")
    def get_aggregation_algorithm_id_from_name(self, user_id, aggregation_algorithm_name):
        aggregation_algorithms_dict = self.driver.get_aggregation_algorithms_dict()
        for aggregation_algorithm_id in aggregation_algorithms_dict:
            if aggregation_algorithms_dict[aggregation_algorithm_id]['name'] == aggregation_algorithm_name:
                return aggregation_algorithm_id
        return None

    @enforce("read", "sub_meta_rule_algorithms")
    def get_sub_meta_rule_algorithms_dict(self, user_id):
        """
        Return a dictionary of sub_meta_rule algorithm
        :return: {
            sub_meta_rule_id1: {name: sub_meta_rule_name, description: sub_meta_rule_description},
            sub_meta_rule_id2: {name: sub_meta_rule_name, description: sub_meta_rule_description},
            ...
        }
        """
        return self.driver.get_sub_meta_rule_algorithms_dict()

    @enforce("read", "sub_meta_rule_algorithms")
    def get_sub_meta_rule_algorithm_id_from_name(self, sub_meta_rule_algorithm_name):
        sub_meta_rule_algorithms_dict = self.configuration_api.get_sub_meta_rule_algorithms_dict()
        for sub_meta_rule_algorithm_id in sub_meta_rule_algorithms_dict:
            if sub_meta_rule_algorithms_dict[sub_meta_rule_algorithm_id]['name'] == sub_meta_rule_algorithm_name:
                return sub_meta_rule_algorithm_id
        return None


@dependency.provider('tenant_api')
@dependency.requires('moonlog_api', 'admin_api', 'root_api', 'resource_api', 'admin_api')
class TenantManager(manager.Manager):

    driver_namespace = 'keystone.moon.tenant'

    def __init__(self):
        super(TenantManager, self).__init__(CONF.moon.tenant_driver)

    @filter_input
    @enforce("read", "tenants")
    def get_tenants_dict(self, user_id):
        """
        Return a dictionary with all tenants
        :return: {
            tenant_id1: {
                name: xxx,
                description: yyy,
                intra_authz_extension_id: zzz,
                intra_admin_extension_id: zzz,
                },
            tenant_id2: {...},
            ...
            }
        """
        return self.driver.get_tenants_dict()

    def __get_keystone_tenant_dict(self, tenant_id="", tenant_name=""):
        tenants = self.resource_api.list_projects()
        for tenant in tenants:
            if tenant_id and tenant_id == tenant['id']:
                return tenant
            if tenant_name and tenant_name == tenant['name']:
                return tenant
        if not tenant_id:
            tenant_id = uuid4().hex
        if not tenant_name:
            tenant_name = tenant_id
        tenant = {
            "id": tenant_id,
            "name": tenant_name,
            "description": "Auto generated tenant from Moon platform",
            "enabled": True,
            "domain_id": "default"
        }
        keystone_tenant = self.resource_api.create_project(tenant["id"], tenant)
        return keystone_tenant

    @filter_input
    @enforce(("read", "write"), "tenants")
    def add_tenant_dict(self, user_id, tenant_id, tenant_dict):
        tenants_dict = self.driver.get_tenants_dict()
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]['name'] == tenant_dict['name']:
                raise TenantAddedNameExisting()

        # Check (and eventually sync) Keystone tenant
        if 'id' not in tenant_dict:
            tenant_dict['id'] = None
        keystone_tenant = self.__get_keystone_tenant_dict(tenant_dict['id'], tenant_dict['name'])
        for att in keystone_tenant:
            if keystone_tenant[att]:
                tenant_dict[att] = keystone_tenant[att]
        # Sync users between intra_authz_extension and intra_admin_extension
        self.moonlog_api.debug("add_tenant_dict {}".format(tenant_dict))
        if 'intra_admin_extension_id' in tenant_dict and tenant_dict['intra_admin_extension_id']:
            if 'intra_authz_extension_id' in tenant_dict and tenant_dict['intra_authz_extension_id']:
                authz_subjects_dict = self.admin_api.get_subjects_dict(self.root_api.root_admin_id, tenant_dict['intra_authz_extension_id'])
                authz_subject_names_list = [authz_subjects_dict[subject_id]["name"] for subject_id in authz_subjects_dict]
                admin_subjects_dict = self.admin_api.get_subjects_dict(self.root_api.root_admin_id, tenant_dict['intra_admin_extension_id'])
                admin_subject_names_list = [admin_subjects_dict[subject_id]["name"] for subject_id in admin_subjects_dict]
                for _subject_id in authz_subjects_dict:
                    if authz_subjects_dict[_subject_id]["name"] not in admin_subject_names_list:
                        self.admin_api.add_subject_dict(self.root_api.root_admin_id, tenant_dict['intra_admin_extension_id'], authz_subjects_dict[_subject_id])
                for _subject_id in admin_subjects_dict:
                    if admin_subjects_dict[_subject_id]["name"] not in authz_subject_names_list:
                        self.admin_api.add_subject_dict(self.root_api.root_admin_id, tenant_dict['intra_authz_extension_id'], admin_subjects_dict[_subject_id])

        return self.driver.add_tenant_dict(tenant_dict['id'], tenant_dict)

    @filter_input
    @enforce("read", "tenants")
    def get_tenant_dict(self, user_id, tenant_id):
        tenants_dict = self.driver.get_tenants_dict()
        if tenant_id not in tenants_dict:
            raise TenantUnknown()
        return tenants_dict[tenant_id]

    @filter_input
    @enforce(("read", "write"), "tenants")
    def del_tenant(self, user_id, tenant_id):
        if tenant_id not in self.driver.get_tenants_dict():
            raise TenantUnknown()
        self.driver.del_tenant(tenant_id)

    @filter_input
    @enforce(("read", "write"), "tenants")
    def set_tenant_dict(self, user_id, tenant_id, tenant_dict):
        tenants_dict = self.driver.get_tenants_dict()
        if tenant_id not in tenants_dict:
            raise TenantUnknown()

        # Sync users between intra_authz_extension and intra_admin_extension
        if 'intra_admin_extension_id' in tenant_dict:
            if 'intra_authz_extension_id' in tenant_dict:
                authz_subjects_dict = self.admin_api.get_subjects_dict(self.root_api.root_admin_id, tenant_dict['intra_authz_extension_id'])
                authz_subject_names_list = [authz_subjects_dict[subject_id]["name"] for subject_id in authz_subjects_dict]
                admin_subjects_dict = self.admin_api.get_subjects_dict(self.root_api.root_admin_id, tenant_dict['intra_admin_extension_id'])
                admin_subject_names_list = [admin_subjects_dict[subject_id]["name"] for subject_id in admin_subjects_dict]
                for _subject_id in authz_subjects_dict:
                    if authz_subjects_dict[_subject_id]["name"] not in admin_subject_names_list:
                        self.admin_api.add_subject_dict(self.root_api.root_admin_id, tenant_dict['intra_admin_extension_id'], authz_subjects_dict[_subject_id])
                for _subject_id in admin_subjects_dict:
                    if admin_subjects_dict[_subject_id]["name"] not in authz_subject_names_list:
                        self.admin_api.add_subject_dict(self.root_api.root_admin_id, tenant_dict['intra_authz_extension_id'], admin_subjects_dict[_subject_id])

        return self.driver.set_tenant_dict(tenant_id, tenant_dict)


@dependency.requires('identity_api', 'tenant_api', 'configuration_api', 'moonlog_api')
class IntraExtensionManager(manager.Manager):

    driver_namespace = 'keystone.moon.intraextension'

    def __init__(self):
        super(IntraExtensionManager, self).__init__(CONF.moon.intraextension_driver)
        self._root_admin_id = None
        self._root_extension_id = None

    def __init_root(self, root_extension_id=None):
        if root_extension_id:
            self._root_extension_id = root_extension_id
        else:
            try:
                self._root_extension_id = self.get_root_extension_id()
                self.aggregation_algorithm_dict = self.configuration_api.driver.get_aggregation_algorithms_dict()
            except AttributeError as e:
                LOG.warning("Error on root intraextension initialization ({})".format(e))
                self._root_extension_id = None
                self.aggregation_algorithm_dict = {}
        if self._root_extension_id:
            for subject_id, subject_dict in self.driver.get_subjects_dict(self.root_extension_id).iteritems():
                if subject_dict["name"] == "admin":
                    self._root_admin_id = subject_id
                    return
            raise RootExtensionNotInitialized()

    @property
    def root_extension_id(self):
        if not self._root_extension_id:
            self.__init_root()
        return self._root_extension_id

    @root_extension_id.setter
    def root_extension_id(self, value):
        self._root_extension_id = value
        LOG.info("set root_extension_id={}".format(self._root_extension_id))

    @property
    def root_admin_id(self):
        if not self._root_admin_id:
            self.__init_root()
        return self._root_admin_id

    def get_root_extension_dict(self):
        """

        :return: {id: {"name": "xxx"}}
        """
        return {self.root_extension_id: self.driver.get_intra_extensions_dict()[self.root_extension_id]}

    def get_root_extension_id(self):
        extensions = self.driver.get_intra_extensions_dict()
        for extension_id, extension_dict in extensions.iteritems():
            if extension_dict["name"] == CONF.moon.root_policy_directory:
                return extension_id
        else:
            extension = self.load_root_intra_extension_dict(CONF.moon.root_policy_directory)
            if not extension:
                raise IntraExtensionCreationError("The root extension is not created.")
            return extension['id']

    def __get_authz_buffer(self, intra_extension_id, subject_id, object_id, action_id):
        """
        :param intra_extension_id:
        :param subject_id:
        :param object_id:
        :param action_id:
        :return: authz_buffer = {
            'subject_id': xxx,
            'object_id': yyy,
            'action_id': zzz,
            'subject_assignments': {
                'subject_category1': [],
                'subject_category2': [],
                ...
            },
            'object_assignments': {},
            'action_assignments': {},
        }
        """
        authz_buffer = dict()
        # Sometimes it is not the subject ID but the User Keystone ID, so, we have to check
        subjects_dict = self.driver.get_subjects_dict(intra_extension_id)
        if subject_id not in subjects_dict.keys():
            for _subject_id in subjects_dict:
                if subjects_dict[_subject_id]['keystone_id']:
                    subject_id = _subject_id
                    break
        authz_buffer['subject_id'] = subject_id
        authz_buffer['object_id'] = object_id
        authz_buffer['action_id'] = action_id
        meta_data_dict = dict()
        meta_data_dict["subject_categories"] = self.driver.get_subject_categories_dict(intra_extension_id)
        meta_data_dict["object_categories"] = self.driver.get_object_categories_dict(intra_extension_id)
        meta_data_dict["action_categories"] = self.driver.get_action_categories_dict(intra_extension_id)
        subject_assignment_dict = dict()
        for category in meta_data_dict["subject_categories"]:
            subject_assignment_dict[category] = self.driver.get_subject_assignment_list(
                intra_extension_id, subject_id, category)
        object_assignment_dict = dict()
        for category in meta_data_dict["object_categories"]:
            object_assignment_dict[category] = self.driver.get_object_assignment_list(
                intra_extension_id, object_id, category)
        action_assignment_dict = dict()
        for category in meta_data_dict["action_categories"]:
            action_assignment_dict[category] = self.driver.get_action_assignment_list(
                intra_extension_id, action_id, category)
        authz_buffer['subject_assignments'] = dict()
        authz_buffer['object_assignments'] = dict()
        authz_buffer['action_assignments'] = dict()

        for _subject_category in meta_data_dict['subject_categories']:
            authz_buffer['subject_assignments'][_subject_category] = list(subject_assignment_dict[_subject_category])
        for _object_category in meta_data_dict['object_categories']:
            authz_buffer['object_assignments'][_object_category] = list(object_assignment_dict[_object_category])
        for _action_category in meta_data_dict['action_categories']:
            authz_buffer['action_assignments'][_action_category] = list(action_assignment_dict[_action_category])
        return authz_buffer

    def __authz(self, intra_extension_id, subject_id, object_id, action_id):
        """Check authorization for a particular action.

        :param intra_extension_id: UUID of an IntraExtension
        :param subject_id: subject UUID of the request
        :param object_id: object UUID of the request
        :param action_id: action UUID of the request
        :return: True or False or raise an exception
        :raises:
        """
        authz_buffer = self.__get_authz_buffer(intra_extension_id, subject_id, object_id, action_id)
        decision_buffer = dict()
        decision = False

        meta_rule_dict = self.driver.get_sub_meta_rules_dict(intra_extension_id)

        for sub_meta_rule_id in meta_rule_dict:
            if meta_rule_dict[sub_meta_rule_id]['algorithm'] == 'inclusion':
                decision_buffer[sub_meta_rule_id] = inclusion(
                    authz_buffer,
                    meta_rule_dict[sub_meta_rule_id],
                    self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id).values())
            elif meta_rule_dict[sub_meta_rule_id]['algorithm'] == 'comparison':
                decision_buffer[sub_meta_rule_id] = comparison(
                    authz_buffer,
                    meta_rule_dict[sub_meta_rule_id],
                    self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id).values())

        try:
            aggregation_algorithm_id = self.driver.get_aggregation_algorithm_id(intra_extension_id)['aggregation_algorithm']
        except TypeError:
            return {
                'authz': False,
                'comment': "Aggregation algorithm not set"
            }
        if self.aggregation_algorithm_dict[aggregation_algorithm_id]['name'] == 'all_true':
            decision = all_true(decision_buffer)
        elif self.aggregation_algorithm_dict[aggregation_algorithm_id]['name'] == 'one_true':
            decision = one_true(decision_buffer)
        if not decision:
            raise AuthzException("{} {}-{}-{}".format(intra_extension_id, subject_id, action_id, object_id))
        return {
            'authz': decision,
            'comment': "{} {}-{}-{}".format(intra_extension_id, subject_id, action_id, object_id)
        }

    def authz(self, intra_extension_id, subject_id, object_id, action_id):
        decision_dict = dict()
        try:
            decision_dict = self.__authz(intra_extension_id, subject_id, object_id, action_id)
        except (SubjectUnknown, ObjectUnknown, ActionUnknown) as e:
            # maybe we need to synchronize with the master
            if CONF.moon.master:
                self.get_data_from_master()
                decision_dict = self.__authz(intra_extension_id, subject_id, object_id, action_id)
        if not decision_dict["authz"]:
            raise AuthzException(decision_dict["comment"])
        return {'authz': decision_dict["authz"], 'comment': ''}

    def get_data_from_master(self, subject=None, object=None, action=None):
        LOG.info("Synchronising with master")
        master_url = CONF.moon.master
        master_login = CONF.moon.master_login
        master_password = CONF.moon.master_password
        headers = {
            'content-type': 'application/json',
            'Accept': 'text/plain,text/html,application/xhtml+xml,application/xml'
        }
        post = {
            'auth': {
                'scope': {
                    'project': {
                        'domain': {'id': 'Default'},
                        'name': 'demo'}
                },
                'identity': {
                    'password': {
                        'user': {
                            'domain': {'id': 'Default'},
                            'password': 'nomoresecrete',
                            'name': 'admin'}
                    },
                    'methods': ['password']
                }
            }
        }
        post["auth"]["identity"]["password"]["user"]["name"] = master_login
        post["auth"]["identity"]["password"]["user"]["password"] = master_password
        req = requests.post('{}/v3/auth/tokens'.format(master_url), data=json.dumps(post), headers=headers)
        if req.status_code not in (200, 201):
            raise IntraExtensionException("Cannot connect to the Master.")
        headers["X-Auth-Token"] = req.headers["x-subject-token"]
        # get all intra-extensions
        req = requests.get('{}/moon/intra_extensions/'.format(master_url), headers=headers)
        extensions = req.json()
        for intra_extension_id, intra_extension_value in extensions.iteritems():
            if intra_extension_value["model"] == "policy_root":
                continue

            # add the intra-extension
            intra_extension_dict = dict()
            # Force the id of the intra-extension
            intra_extension_dict['id'] = intra_extension_id
            intra_extension_dict['name'] = intra_extension_value["name"]
            intra_extension_dict['model'] = intra_extension_value["model"]
            intra_extension_dict['genre'] = intra_extension_value["genre"]
            intra_extension_dict['description'] = intra_extension_value["description"]
            try:
                ref = self.load_intra_extension_dict(self.root_admin_id, intra_extension_dict=intra_extension_dict)
            except Exception as e:
                LOG.error("(load_intra_extension_dict) Got an unhandled exception: {}".format(e))
                import traceback, sys
                traceback.print_exc(file=sys.stdout)

            # Note (asteroide): we use the driver API to bypass authorizations of the internal API
            # but in we force overwriting data every time

            # get all categories from master
            _url = '{}/moon/intra_extensions/{}/subject_categories'.format(master_url, intra_extension_id)
            req = requests.get(_url, headers=headers)
            cat = req.json()
            _categories_name = map(lambda x: x["name"],
                                   self.driver.get_subject_categories_dict(intra_extension_id).values())
            for _cat_key, _cat_value in cat.iteritems():
                if _cat_value['name'] in _categories_name:
                    continue
                self.driver.set_subject_category_dict(intra_extension_id, _cat_key, _cat_value)
            _url = '{}/moon/intra_extensions/{}/object_categories'.format(master_url, intra_extension_id)
            req = requests.get(_url, headers=headers)
            cat = req.json()
            _categories_name = map(lambda x: x["name"],
                                   self.driver.get_object_categories_dict(intra_extension_id).values())
            for _cat_key, _cat_value in cat.iteritems():
                if _cat_value['name'] in _categories_name:
                    continue
                self.driver.set_object_category_dict(intra_extension_id, _cat_key, _cat_value)
            _url = '{}/moon/intra_extensions/{}/action_categories'.format(master_url, intra_extension_id)
            req = requests.get(_url, headers=headers)
            cat = req.json()
            _categories_name = map(lambda x: x["name"],
                                   self.driver.get_action_categories_dict(intra_extension_id).values())
            for _cat_key, _cat_value in cat.iteritems():
                if _cat_value['name'] in _categories_name:
                    continue
                self.driver.set_action_category_dict(intra_extension_id, _cat_key, _cat_value)

            # get part of subjects, objects, actions from master
            _url = '{}/moon/intra_extensions/{}/subjects'.format(master_url, intra_extension_id)
            req = requests.get(_url, headers=headers)
            sub = req.json()
            _subjects_name = map(lambda x: x["name"], self.driver.get_subjects_dict(intra_extension_id).values())
            for _sub_key, _sub_value in sub.iteritems():
                if _sub_value['name'] in _subjects_name:
                    continue
                keystone_user = self.identity_api.get_user_by_name(_sub_value['keystone_name'], "default")
                _sub_value['keystone_id'] = keystone_user['id']
                self.driver.set_subject_dict(intra_extension_id, _sub_key, _sub_value)
            _url = '{}/moon/intra_extensions/{}/objects'.format(master_url, intra_extension_id)
            req = requests.get(_url, headers=headers)
            obj = req.json()
            _objects_name = map(lambda x: x["name"], self.driver.get_objects_dict(intra_extension_id).values())
            for _obj_key, _obj_value in obj.iteritems():
                if _obj_value['name'] in _objects_name:
                    continue
                _obj_value['id'] = _obj_key
                self.driver.set_object_dict(intra_extension_id, _obj_key, _obj_value)
            _url = '{}/moon/intra_extensions/{}/actions'.format(master_url, intra_extension_id)
            req = requests.get(_url, headers=headers)
            act = req.json()
            _actions_name = map(lambda x: x["name"], self.driver.get_actions_dict(intra_extension_id).values())
            for _act_key, _act_value in act.iteritems():
                if _act_value['name'] in _actions_name:
                    continue
                self.driver.set_action_dict(intra_extension_id, _act_key, _act_value)

            # get all scopes from master
            for s_cat, _value in self.driver.get_subject_categories_dict(intra_extension_id).iteritems():
                _url = '{}/moon/intra_extensions/{}/subject_scopes/{}'.format(master_url, intra_extension_id, s_cat)
                req = requests.get(_url, headers=headers)
                scopes = req.json()
                _scopes_name = map(lambda x: x["name"],
                                   self.driver.get_subject_scopes_dict(intra_extension_id, s_cat).values())
                if not _scopes_name:
                    continue
                for _scope_key, _scope_value in scopes.iteritems():
                    if _scope_value['name'] in _scopes_name:
                        continue
                    self.driver.set_subject_scope_dict(intra_extension_id, s_cat, _scope_key, _scope_value)
            for o_cat in self.driver.get_subject_categories_dict(intra_extension_id):
                _url = '{}/moon/intra_extensions/{}/object_scopes/{}'.format(master_url, intra_extension_id, o_cat)
                req = requests.get(_url, headers=headers)
                scopes = req.json()
                _scopes_name = map(lambda x: x["name"],
                                   self.driver.get_object_scopes_dict(intra_extension_id, o_cat).values())
                if not _scopes_name:
                    continue
                for _scope_key, _scope_value in scopes.iteritems():
                    if _scope_value['name'] in _scopes_name:
                        continue
                    self.driver.set_object_scope_dict(intra_extension_id, o_cat, _scope_key, _scope_value)
            for a_cat in self.driver.get_subject_categories_dict(intra_extension_id):
                _url = '{}/moon/intra_extensions/{}/action_scopes/{}'.format(master_url, intra_extension_id, a_cat)
                req = requests.get(_url, headers=headers)
                scopes = req.json()
                _scopes_name = map(lambda x: x["name"],
                                   self.driver.get_action_scopes_dict(intra_extension_id, a_cat ).values())
                if not _scopes_name:
                    continue
                for _scope_key, _scope_value in scopes.iteritems():
                    if _scope_value['name'] in _scopes_name:
                        continue
                    self.add_action_scope_dict(intra_extension_id, a_cat, _scope_key, _scope_value)

            # get aggregation algorithm from master
            _url = '{}/moon/intra_extensions/{}/aggregation_algorithm'.format(master_url, intra_extension_id)
            req = requests.get(_url, headers=headers)
            algo = req.json()
            self.driver.set_aggregation_algorithm_id(intra_extension_id, algo['aggregation_algorithm'])

            # get meta-rule from master
            _url = '{}/moon/intra_extensions/{}/sub_meta_rules'.format(master_url, intra_extension_id)
            req = requests.get(_url, headers=headers)
            sub_meta_rules = req.json()
            _sub_meta_rules_name = map(lambda x: x["name"], self.driver.get_sub_meta_rules_dict(intra_extension_id).values())
            for _sub_meta_rules_key, _sub_meta_rules_value in sub_meta_rules.iteritems():
                if _sub_meta_rules_value['name'] in _sub_meta_rules_name:
                    continue
                self.driver.set_sub_meta_rule_dict(intra_extension_id, _sub_meta_rules_key, _sub_meta_rules_value)

            # get all rules from master
            _sub_meta_rules_ids = self.driver.get_sub_meta_rules_dict(intra_extension_id).keys()
            for _sub_meta_rules_id in _sub_meta_rules_ids:
                _url = '{}/moon/intra_extensions/{}/rule/{}'.format(master_url, intra_extension_id, _sub_meta_rules_id)
                req = requests.get(_url, headers=headers)
                rules = req.json()
                _rules = self.driver.get_rules_dict(intra_extension_id, _sub_meta_rules_id).values()
                for _rules_key, _rules_value in rules.iteritems():
                    if _rules_value in _rules:
                        continue
                    self.driver.set_rule_dict(intra_extension_id, _sub_meta_rules_id, _rules_key, _rules_value)

            # get part of assignments from master
            _subject_ids = self.driver.get_subjects_dict(intra_extension_id).keys()
            _subject_category_ids = self.driver.get_subject_categories_dict(intra_extension_id).keys()

            for _subject_id in _subject_ids:
                for _subject_category_id in _subject_category_ids:
                    _url = '{}/moon/intra_extensions/{}/subject_assignments/{}/{}'.format(
                        master_url,
                        intra_extension_id,
                        _subject_id,
                        _subject_category_id
                    )
                    req = requests.get(_url, headers=headers)
                    subject_assignments = req.json()
                    _assignments = self.driver.get_subject_assignment_list(
                        intra_extension_id,
                        _subject_id,
                        _subject_category_id
                    )
                    for _assignment in subject_assignments:
                        if _assignment in _assignments:
                            continue
                        self.driver.add_subject_assignment_list(
                            intra_extension_id,
                            _subject_id,
                            _subject_category_id,
                            _assignment
                        )

            _object_ids = self.driver.get_objects_dict(intra_extension_id).keys()
            _object_category_ids = self.driver.get_object_categories_dict(intra_extension_id).keys()

            for _object_id in _object_ids:
                for _object_category_id in _object_category_ids:
                    _url = '{}/moon/intra_extensions/{}/object_assignments/{}/{}'.format(
                        master_url,
                        intra_extension_id,
                        _object_id,
                        _object_category_id
                    )
                    req = requests.get(_url, headers=headers)
                    object_assignments = req.json()
                    _assignments = self.driver.get_object_assignment_list(
                        intra_extension_id,
                        _object_id,
                        _object_category_id
                    )
                    for _assignment in object_assignments:
                        if _assignment in _assignments:
                            continue
                        self.driver.add_object_assignment_list(
                            intra_extension_id,
                            _object_id,
                            _object_category_id,
                            _assignment
                        )

            _action_ids = self.driver.get_actions_dict(intra_extension_id).keys()
            _action_category_ids = self.driver.get_action_categories_dict(intra_extension_id).keys()

            for _action_id in _action_ids:
                for _action_category_id in _action_category_ids:
                    _url = '{}/moon/intra_extensions/{}/action_assignments/{}/{}'.format(
                        master_url,
                        intra_extension_id,
                        _action_id,
                        _action_category_id
                    )
                    req = requests.get(_url, headers=headers)
                    action_assignments = req.json()
                    _assignments = self.driver.get_action_assignment_list(
                        intra_extension_id,
                        _action_id,
                        _action_category_id
                    )
                    for _assignment in action_assignments:
                        if _assignment in _assignments:
                            continue
                        self.driver.add_action_assignment_list(
                            intra_extension_id,
                            _action_id,
                            _action_category_id,
                            _assignment
                        )

    @enforce("read", "intra_extensions")
    def get_intra_extensions_dict(self, user_id):
        """
        :param user_id:
        :return: {
            intra_extension_id1: {
                name: xxx,
                model: yyy,
                genre, authz,
                description: zzz}
            },
            intra_extension_id2: {...},
            ...}
        """
        return self.driver.get_intra_extensions_dict()

    # load policy from policy directory

    def __load_metadata_file(self, intra_extension_dict, policy_dir):

        metadata_path = os.path.join(policy_dir, 'metadata.json')
        f = open(metadata_path)
        json_perimeter = json.load(f)

        subject_categories = map(lambda x: x["name"],
                                 self.driver.get_subject_categories_dict(intra_extension_dict["id"]).values())
        for _cat in json_perimeter['subject_categories']:
            if _cat not in subject_categories:
                self.driver.set_subject_category_dict(intra_extension_dict["id"], uuid4().hex,
                                                      {"name": _cat, "description": _cat})
        object_categories = map(lambda x: x["name"],
                                self.driver.get_object_categories_dict(intra_extension_dict["id"]).values())
        for _cat in json_perimeter['object_categories']:
            if _cat not in object_categories:
                self.driver.set_object_category_dict(intra_extension_dict["id"], uuid4().hex,
                                                     {"name": _cat, "description": _cat})
        action_categories = map(lambda x: x["name"],
                                self.driver.get_action_categories_dict(intra_extension_dict["id"]).values())
        for _cat in json_perimeter['action_categories']:
            if _cat not in action_categories:
                self.driver.set_action_category_dict(intra_extension_dict["id"], uuid4().hex,
                                                     {"name": _cat, "description": _cat})

    def __load_perimeter_file(self, intra_extension_dict, policy_dir):

        perimeter_path = os.path.join(policy_dir, 'perimeter.json')
        f = open(perimeter_path)
        json_perimeter = json.load(f)

        subjects_name_list = map(lambda x: x["name"], self.driver.get_subjects_dict(intra_extension_dict["id"]).values())
        subject_dict = dict()
        # We suppose that all subjects can be mapped to a true user in Keystone
        for _subject in json_perimeter['subjects']:
            if _subject in subjects_name_list:
                continue
            try:
                keystone_user = self.identity_api.get_user_by_name(_subject, "default")
            except exception.UserNotFound:
                # TODO (asteroide): must add a configuration option to allow that exception
                # maybe a debug option for unittest
                keystone_user = {'id': uuid4().hex, 'name': _subject}
                self.moonlog_api.error("Keystone user not found ({})".format(_subject))
            subject_id = uuid4().hex
            subject_dict[subject_id] = keystone_user
            subject_dict[subject_id]['keystone_id'] = keystone_user["id"]
            subject_dict[subject_id]['keystone_name'] = keystone_user["name"]
            self.driver.set_subject_dict(intra_extension_dict["id"], subject_id, subject_dict[subject_id])
        intra_extension_dict["subjects"] = subject_dict

        # Copy all values for objects and actions
        objects_name_list = map(lambda x: x["name"], self.driver.get_objects_dict(intra_extension_dict["id"]).values())
        object_dict = dict()
        for _object in json_perimeter['objects']:
            if _object in objects_name_list:
                continue
            _id = uuid4().hex
            object_dict[_id] = {"name": _object, "description": _object}
            self.driver.set_object_dict(intra_extension_dict["id"], _id, object_dict[_id])
        intra_extension_dict["objects"] = object_dict

        actions_name_list = map(lambda x: x["name"], self.driver.get_objects_dict(intra_extension_dict["id"]).values())
        action_dict = dict()
        for _action in json_perimeter['actions']:
            if _action in actions_name_list:
                continue
            _id = uuid4().hex
            action_dict[_id] = {"name": _action, "description": _action}
            self.driver.set_action_dict(intra_extension_dict["id"], _id, action_dict[_id])
        intra_extension_dict["actions"] = action_dict

    def __load_scope_file(self, intra_extension_dict, policy_dir):

        metadata_path = os.path.join(policy_dir, 'scope.json')
        f = open(metadata_path)
        json_perimeter = json.load(f)

        intra_extension_dict['subject_scopes'] = dict()
        for category, scope in json_perimeter["subject_scopes"].iteritems():
            category_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], category, self.driver.SUBJECT_CATEGORY)
            _scope_dict = dict()
            for _scope in scope:
                _id = uuid4().hex
                _scope_dict[_id] = {"name": _scope, "description": _scope}
                self.driver.set_subject_scope_dict(intra_extension_dict["id"], category_id, _id, _scope_dict[_id])
            intra_extension_dict['subject_scopes'][category] = _scope_dict

        intra_extension_dict['object_scopes'] = dict()
        for category, scope in json_perimeter["object_scopes"].iteritems():
            category_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], category, self.driver.OBJECT_CATEGORY)
            _scope_dict = dict()
            for _scope in scope:
                _id = uuid4().hex
                _scope_dict[_id] = {"name": _scope, "description": _scope}
                self.driver.set_object_scope_dict(intra_extension_dict["id"], category_id, _id, _scope_dict[_id])
            intra_extension_dict['object_scopes'][category] = _scope_dict

        intra_extension_dict['action_scopes'] = dict()
        for category, scope in json_perimeter["action_scopes"].iteritems():
            category_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], category, self.driver.ACTION_CATEGORY)
            _scope_dict = dict()
            for _scope in scope:
                _id = uuid4().hex
                _scope_dict[_id] = {"name": _scope, "description": _scope}
                self.driver.set_action_scope_dict(intra_extension_dict["id"], category_id, _id, _scope_dict[_id])
            intra_extension_dict['action_scopes'][category] = _scope_dict

    def __load_assignment_file(self, intra_extension_dict, policy_dir):

        f = open(os.path.join(policy_dir, 'assignment.json'))
        json_assignments = json.load(f)

        subject_assignments = dict()
        for category_name, value in json_assignments['subject_assignments'].iteritems():
            category_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], category_name, self.driver.SUBJECT_CATEGORY)
            for user_name in value:
                subject_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], user_name, self.driver.SUBJECT)
                if subject_id not in subject_assignments:
                    subject_assignments[subject_id] = dict()
                if category_id not in subject_assignments[subject_id]:
                    subject_assignments[subject_id][category_id] = \
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.SUBJECT_SCOPE, category_name),
                            value[user_name])
                else:
                    subject_assignments[subject_id][category_id].extend(
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.SUBJECT_SCOPE, category_name),
                            value[user_name])
                    )
                self.driver.set_subject_assignment_list(intra_extension_dict["id"], subject_id, category_id,
                                                        subject_assignments[subject_id][category_id])

        object_assignments = dict()
        for category_name, value in json_assignments["object_assignments"].iteritems():
            category_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], category_name, self.driver.OBJECT_CATEGORY)
            for object_name in value:
                object_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], object_name, self.driver.OBJECT)
                if object_name not in object_assignments:
                    object_assignments[object_id] = dict()
                if category_id not in object_assignments[object_id]:
                    object_assignments[object_id][category_id] = \
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.OBJECT_SCOPE, category_name),
                            value[object_name])
                else:
                    object_assignments[object_id][category_id].extend(
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.OBJECT_SCOPE, category_name),
                            value[object_name])
                    )
                self.driver.set_object_assignment_list(intra_extension_dict["id"], object_id, category_id,
                                                        object_assignments[object_id][category_id])

        action_assignments = dict()
        for category_name, value in json_assignments["action_assignments"].iteritems():
            category_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], category_name, self.driver.ACTION_CATEGORY)
            for action_name in value:
                action_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], action_name, self.driver.ACTION)
                if action_name not in action_assignments:
                    action_assignments[action_id] = dict()
                if category_id not in action_assignments[action_id]:
                    action_assignments[action_id][category_id] = \
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.ACTION_SCOPE, category_name),
                            value[action_name])
                else:
                    action_assignments[action_id][category_id].extend(
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.ACTION_SCOPE, category_name),
                            value[action_name])
                    )
                self.driver.set_action_assignment_list(intra_extension_dict["id"], action_id, category_id,
                                                        action_assignments[action_id][category_id])

    def __load_metarule_file(self, intra_extension_dict, policy_dir):

        metadata_path = os.path.join(policy_dir, 'metarule.json')
        f = open(metadata_path)
        json_metarule = json.load(f)
        metarule = dict()
        categories = {
            "subject_categories": self.driver.SUBJECT_CATEGORY,
            "object_categories": self.driver.OBJECT_CATEGORY,
            "action_categories": self.driver.ACTION_CATEGORY
        }
        # Translate value from JSON file to UUID for Database
        for metarule_name in json_metarule["sub_meta_rules"]:
            _id = uuid4().hex
            metarule[_id] = dict()
            metarule[_id]["name"] = metarule_name
            for item in ("subject_categories", "object_categories", "action_categories"):
                metarule[_id][item] = list()
                for element in json_metarule["sub_meta_rules"][metarule_name][item]:
                    metarule[_id][item].append(self.driver.get_uuid_from_name(intra_extension_dict["id"], element, categories[item]))
            metarule[_id]["algorithm"] = json_metarule["sub_meta_rules"][metarule_name]["algorithm"]
            self.driver.set_sub_meta_rule_dict(intra_extension_dict["id"], _id, metarule[_id])
        submetarules = {
            "aggregation": json_metarule["aggregation"],
            "sub_meta_rules": metarule
        }
        for _id, _value in self.configuration_api.driver.get_aggregation_algorithms_dict().iteritems():
            if _value["name"] == json_metarule["aggregation"]:
                self.driver.set_aggregation_algorithm_id(intra_extension_dict["id"], _id)
                break
        else:
            LOG.warning("No aggregation_algorithm found for '{}'".format(json_metarule["aggregation"]))

    def __load_rule_file(self, intra_extension_dict, policy_dir):

        metadata_path = os.path.join(policy_dir, 'rule.json')
        f = open(metadata_path)
        json_rules = json.load(f)
        intra_extension_dict["rule"] = {"rule": copy.deepcopy(json_rules)}
        # Translate value from JSON file to UUID for Database
        rules = dict()
        sub_meta_rules = self.driver.get_sub_meta_rules_dict(intra_extension_dict["id"])
        for sub_rule_name in json_rules:
            sub_rule_id = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                         sub_rule_name,
                                                         self.driver.SUB_META_RULE)
            rules[sub_rule_id] = list()
            for rule in json_rules[sub_rule_name]:
                subrule = list()
                _rule = list(rule)
                for category_uuid in sub_meta_rules[sub_rule_id]["subject_categories"]:
                    scope_name = _rule.pop(0)
                    scope_uuid = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                                scope_name,
                                                                self.driver.SUBJECT_SCOPE,
                                                                category_uuid=category_uuid)
                    subrule.append(scope_uuid)
                for category_uuid in sub_meta_rules[sub_rule_id]["action_categories"]:
                    scope_name = _rule.pop(0)
                    scope_uuid = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                                scope_name,
                                                                self.driver.ACTION_SCOPE,
                                                                category_uuid=category_uuid)
                    subrule.append(scope_uuid)
                for category_uuid in sub_meta_rules[sub_rule_id]["object_categories"]:
                    scope_name = _rule.pop(0)
                    scope_uuid = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                                scope_name,
                                                                self.driver.OBJECT_SCOPE,
                                                                category_uuid=category_uuid)
                    subrule.append(scope_uuid)
                # if a positive/negative value exists, all item of rule have not be consumed
                if len(rule) >= 1 and isinstance(rule[0], bool):
                    subrule.append(rule[0])
                else:
                    # if value doesn't exist add a default value
                    subrule.append(True)
                self.driver.set_rule_dict(intra_extension_dict["id"], sub_rule_id, uuid4().hex, subrule)

    @enforce(("read", "write"), "intra_extensions")
    def load_intra_extension_dict(self, user_id, intra_extension_dict):
        ie_dict = dict()
        if "id" in intra_extension_dict:
            ie_dict['id'] = filter_input(intra_extension_dict["id"])
        else:
            ie_dict['id'] = uuid4().hex

        intraextensions = self.get_intra_extensions_dict(user_id)

        ie_dict["name"] = filter_input(intra_extension_dict["name"])
        ie_dict["model"] = filter_input(intra_extension_dict["model"])
        ie_dict["genre"] = filter_input(intra_extension_dict["genre"])
        if not ie_dict["genre"]:
            if "admin" in ie_dict["model"] or "root" in ie_dict["model"]:
                ie_dict["genre"] = "admin"
            else:
                ie_dict["genre"] = "authz"
        ie_dict["description"] = filter_input(intra_extension_dict["description"])
        ref = self.driver.set_intra_extension_dict(ie_dict['id'], ie_dict)

        # if ie_dict['id'] in intraextensions:
        #     # note (dthom): if id was in intraextensions, it implies that the intraextension was already there
        #     # so we don't have to populate with default values
        return ref

    def populate_default_data(self, ref):
        self.moonlog_api.debug("Creation of IE: {}".format(ref))
        # read the template given by "model" and populate default variables
        template_dir = os.path.join(CONF.moon.policy_directory, ref['intra_extension']["model"])
        self.__load_metadata_file(ref['intra_extension'], template_dir)
        self.__load_perimeter_file(ref['intra_extension'], template_dir)
        self.__load_scope_file(ref['intra_extension'], template_dir)
        self.__load_assignment_file(ref['intra_extension'], template_dir)
        self.__load_metarule_file(ref['intra_extension'], template_dir)
        self.__load_rule_file(ref['intra_extension'], template_dir)
        return ref

    def load_root_intra_extension_dict(self, policy_template=CONF.moon.root_policy_directory):
        # Note (asteroide): Only one root Extension is authorized
        # and this extension is created at the very beginning of the server
        # so we don't need to use enforce here
        extensions = self.driver.get_intra_extensions_dict()
        for extension_id, extension_dict in extensions.iteritems():
            if extension_dict["name"] == CONF.moon.root_policy_directory:
                return {'id': extension_id}
        ie_dict = dict()
        ie_dict['id'] = uuid4().hex
        ie_dict["name"] = "policy_root"
        ie_dict["model"] = filter_input(policy_template)
        ie_dict["genre"] = "admin"
        ie_dict["description"] = "policy_root"
        ref = self.driver.set_intra_extension_dict(ie_dict['id'], ie_dict)
        logging.debug("Creation of root IE: {}".format(ref))
        self.moonlog_api.debug("Creation of root IE: {}".format(ref))

        # read the template given by "model" and populate default variables
        template_dir = os.path.join(CONF.moon.policy_directory, ie_dict["model"])
        self.__load_metadata_file(ie_dict, template_dir)
        self.__load_perimeter_file(ie_dict, template_dir)
        self.__load_scope_file(ie_dict, template_dir)
        self.__load_assignment_file(ie_dict, template_dir)
        self.__load_metarule_file(ie_dict, template_dir)
        self.__load_rule_file(ie_dict, template_dir)
        self.__init_root(root_extension_id=ie_dict['id'])
        if CONF.moon.master:
            LOG.info("Master address: {}".format(CONF.moon.master))
            self.get_data_from_master()
        return ref

    @enforce("read", "intra_extensions")
    def get_intra_extension_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :return: {
            intra_extension_id: {
                name: xxx,
                model: yyy,
                genre: authz,
                description: xxx}
            }
        """
        intra_extensions_dict = self.driver.get_intra_extensions_dict()
        if intra_extension_id not in intra_extensions_dict:
            raise IntraExtensionUnknown()
        return intra_extensions_dict[intra_extension_id]

    @enforce(("read", "write"), "intra_extensions")
    def del_intra_extension(self, user_id, intra_extension_id):
        if intra_extension_id not in self.driver.get_intra_extensions_dict():
            raise IntraExtensionUnknown()
        for sub_meta_rule_id in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            for rule_id in self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id):
                self.driver.del_rule(intra_extension_id, sub_meta_rule_id, rule_id)
            self.driver.del_sub_meta_rule(intra_extension_id, sub_meta_rule_id)
        self.driver.del_aggregation_algorithm(intra_extension_id)
        for subject_id in self.driver.get_subjects_dict(intra_extension_id):
            for subject_category_id in self.driver.get_subject_categories_dict(intra_extension_id):
                self.driver.del_subject_scope(intra_extension_id, None, None)
                self.driver.del_subject_assignment(intra_extension_id, None, None, None)
                self.driver.del_subject_category(intra_extension_id, subject_category_id)
        for object_id in self.driver.get_objects_dict(intra_extension_id):
            for object_category_id in self.driver.get_object_categories_dict(intra_extension_id):
                self.driver.del_object_scope(intra_extension_id, None, None)
                self.driver.del_object_assignment(intra_extension_id, None, None, None)
                self.driver.del_object_category(intra_extension_id, object_category_id)
        for action_id in self.driver.get_actions_dict(intra_extension_id):
            for action_category_id in self.driver.get_action_categories_dict(intra_extension_id):
                self.driver.del_action_scope(intra_extension_id, None, None)
                self.driver.del_action_assignment(intra_extension_id, None, None, None)
                self.driver.del_action_category(intra_extension_id, action_category_id)
        for subject_id in self.driver.get_subjects_dict(intra_extension_id):
            self.driver.del_subject(intra_extension_id, subject_id)
        for object_id in self.driver.get_objects_dict(intra_extension_id):
            self.driver.del_object(intra_extension_id, object_id)
        for action_id in self.driver.get_actions_dict(intra_extension_id):
            self.driver.del_action(intra_extension_id, action_id)
        return self.driver.del_intra_extension(intra_extension_id)

    @enforce(("read", "write"), "intra_extensions")
    def set_intra_extension_dict(self, user_id, intra_extension_id, intra_extension_dict):
        if intra_extension_id not in self.driver.get_intra_extensions_dict():
            raise IntraExtensionUnknown()
        return self.driver.set_intra_extension_dict(intra_extension_id, intra_extension_dict)

    # Metadata functions

    @filter_input
    @enforce("read", "subject_categories")
    def get_subject_categories_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :param intra_extension_id:
        :return: {
            subject_category_id1: {
                name: xxx,
                description: yyy},
            subject_category_id2: {...},
            ...}
        """
        return self.driver.get_subject_categories_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "subject_categories")
    def add_subject_category_dict(self, user_id, intra_extension_id, subject_category_dict):
        subject_categories_dict = self.driver.get_subject_categories_dict(intra_extension_id)
        for subject_category_id in subject_categories_dict:
            if subject_categories_dict[subject_category_id]['name'] == subject_category_dict['name']:
                raise SubjectCategoryNameExisting("Subject category {} already exists!".format(subject_category_dict['name']))
        _id = subject_category_dict.get('id', uuid4().hex)
        return self.driver.set_subject_category_dict(intra_extension_id, _id, subject_category_dict)

    @filter_input
    @enforce("read", "subject_categories")
    def get_subject_category_dict(self, user_id, intra_extension_id, subject_category_id):
        subject_categories_dict = self.driver.get_subject_categories_dict(intra_extension_id)
        if subject_category_id not in subject_categories_dict:
            raise SubjectCategoryUnknown()
        return subject_categories_dict[subject_category_id]

    @filter_input
    @enforce(("read", "write"), "subject_categories")
    @enforce(("read", "write"), "subject_scopes")
    @enforce(("read", "write"), "subject_assignments")
    def del_subject_category(self, user_id, intra_extension_id, subject_category_id):
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        # Destroy scopes related to this category
        for scope in self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id):
            self.del_subject_scope(intra_extension_id, subject_category_id, scope)
        # Destroy assignments related to this category
        for subject_id in self.driver.get_subjects_dict(intra_extension_id):
            for assignment_id in self.driver.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id):
                self.driver.del_subject_assignment(intra_extension_id, subject_id, subject_category_id, assignment_id)
        self.driver.del_subject_category(intra_extension_id, subject_category_id)

    @filter_input
    @enforce(("read", "write"), "subject_categories")
    def set_subject_category_dict(self, user_id, intra_extension_id, subject_category_id, subject_category_dict):
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        return self.driver.set_subject_category_dict(intra_extension_id, subject_category_id, subject_category_dict)

    @filter_input
    @enforce("read", "object_categories")
    def get_object_categories_dict(self, user_id, intra_extension_id):
        return self.driver.get_object_categories_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "object_categories")
    @enforce(("read", "write"), "object_scopes")
    def add_object_category_dict(self, user_id, intra_extension_id, object_category_dict):
        object_categories_dict = self.driver.get_object_categories_dict(intra_extension_id)
        for object_category_id in object_categories_dict:
            if object_categories_dict[object_category_id]["name"] == object_category_dict['name']:
                raise ObjectCategoryNameExisting()
        _id = object_category_dict.get('id', uuid4().hex)
        return self.driver.set_object_category_dict(intra_extension_id, _id, object_category_dict)

    @filter_input
    @enforce("read", "object_categories")
    def get_object_category_dict(self, user_id, intra_extension_id, object_category_id):
        object_categories_dict = self.driver.get_object_categories_dict(intra_extension_id)
        if object_category_id not in object_categories_dict:
            raise ObjectCategoryUnknown()
        return object_categories_dict[object_category_id]

    @filter_input
    @enforce(("read", "write"), "object_categories")
    @enforce(("read", "write"), "object_scopes")
    @enforce(("read", "write"), "object_assignments")
    def del_object_category(self, user_id, intra_extension_id, object_category_id):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        # Destroy scopes related to this category
        for scope in self.driver.get_object_scopes_dict(intra_extension_id, object_category_id):
            self.del_object_scope(intra_extension_id, object_category_id, scope)
        # Destroy assignments related to this category
        for object_id in self.driver.get_objects_dict(intra_extension_id):
            for assignment_id in self.driver.get_object_assignment_list(intra_extension_id, object_id, object_category_id):
                self.driver.del_object_assignment(intra_extension_id, object_id, object_category_id, assignment_id)
        self.driver.del_object_category(intra_extension_id, object_category_id)

    @filter_input
    @enforce(("read", "write"), "object_categories")
    def set_object_category_dict(self, user_id, intra_extension_id, object_category_id, object_category_dict):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        return self.driver.set_object_category_dict(intra_extension_id, object_category_id, object_category_dict)

    @filter_input
    @enforce("read", "action_categories")
    def get_action_categories_dict(self, user_id, intra_extension_id):
        return self.driver.get_action_categories_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "action_categories")
    @enforce(("read", "write"), "action_scopes")
    def add_action_category_dict(self, user_id, intra_extension_id, action_category_dict):
        action_categories_dict = self.driver.get_action_categories_dict(intra_extension_id)
        for action_category_id in action_categories_dict:
            if action_categories_dict[action_category_id]['name'] == action_category_dict['name']:
                raise ActionCategoryNameExisting()
        _id = action_category_dict.get('id', uuid4().hex)
        return self.driver.set_action_category_dict(intra_extension_id, _id, action_category_dict)

    @filter_input
    @enforce("read", "action_categories")
    def get_action_category_dict(self, user_id, intra_extension_id, action_category_id):
        action_categories_dict = self.driver.get_action_categories_dict(intra_extension_id)
        if action_category_id not in action_categories_dict:
            raise ActionCategoryUnknown()
        return action_categories_dict[action_category_id]

    @filter_input
    @enforce(("read", "write"), "action_categories")
    @enforce(("read", "write"), "action_scopes")
    def del_action_category(self, user_id, intra_extension_id, action_category_id):
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        # Destroy scopes related to this category
        for scope in self.driver.get_action_scopes_dict(intra_extension_id, action_category_id):
            self.del_action_scope(intra_extension_id, action_category_id, scope)
        # Destroy assignments related to this category
        for action_id in self.driver.get_actions_dict(intra_extension_id):
            for assignment_id in self.driver.get_action_assignment_list(intra_extension_id, action_id, action_category_id):
                self.driver.del_action_assignment(intra_extension_id, action_id, action_category_id, assignment_id)
        self.driver.del_action_category(intra_extension_id, action_category_id)

    @filter_input
    @enforce(("read", "write"), "action_categories")
    def set_action_category_dict(self, user_id, intra_extension_id, action_category_id, action_category_dict):
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        return self.driver.set_action_category_dict(intra_extension_id, action_category_id, action_category_dict)

    # Perimeter functions

    @filter_input
    @enforce("read", "subjects")
    def get_subjects_dict(self, user_id, intra_extension_id):
        return self.driver.get_subjects_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "subjects")
    def add_subject_dict(self, user_id, intra_extension_id, subject_dict):
        subjects_dict = self.driver.get_subjects_dict(intra_extension_id)
        for subject_id in subjects_dict:
            if subjects_dict[subject_id]["name"] == subject_dict['name']:
                raise SubjectNameExisting("Subject {} already exists! [add_subject_dict]".format(subject_dict['name']))
        try:
            subject_keystone_dict = self.identity_api.get_user_by_name(subject_dict['name'], "default")
        except UserNotFound as e:
            if 'domain_id' not in subject_dict:
                subject_dict['domain_id'] = "default"
            if 'project_id' not in subject_dict:
                tenants = self.tenant_api.get_tenants_dict(user_id)
                # Get the tenant ID for that intra_extension
                for tenant_id, tenant_value in tenants.iteritems():
                    if intra_extension_id == tenant_value['intra_admin_extension_id'] or \
                        intra_extension_id == tenant_value['intra_authz_extension_id']:
                        subject_dict['project_id'] = tenant_value['id']
                        break
                else:
                    # If no tenant is found default to the admin tenant
                    for tenant_id, tenant_value in tenants.iteritems():
                        if tenant_value['name'] == 'admin':
                            subject_dict['project_id'] = tenant_value['id']
            if 'email' not in subject_dict:
                subject_dict['email'] = ""
            if 'password' not in subject_dict:
                # Default passord to the name of the new user
                subject_dict['password'] = subject_dict['name']
            subject_keystone_dict = self.identity_api.create_user(subject_dict)
        subject_dict["keystone_id"] = subject_keystone_dict["id"]
        subject_dict["keystone_name"] = subject_keystone_dict["name"]
        return self.driver.set_subject_dict(intra_extension_id, uuid4().hex, subject_dict)

    @filter_input
    @enforce("read", "subjects")
    def get_subject_dict(self, user_id, intra_extension_id, subject_id):
        subjects_dict = self.driver.get_subjects_dict(intra_extension_id)
        if subject_id not in subjects_dict:
            raise SubjectUnknown()
        return subjects_dict[subject_id]

    @filter_input
    @enforce(("read", "write"), "subjects")
    def del_subject(self, user_id, intra_extension_id, subject_id):
        if subject_id not in self.driver.get_subjects_dict(intra_extension_id):
            raise SubjectUnknown()
        # Destroy assignments related to this category
        for subject_category_id in self.driver.get_subject_categories_dict(intra_extension_id):
            for _subject_id in self.driver.get_subjects_dict(intra_extension_id):
                for assignment_id in self.driver.get_subject_assignment_list(intra_extension_id, _subject_id, subject_category_id):
                    self.driver.del_subject_assignment(intra_extension_id, _subject_id, subject_category_id, assignment_id)
        self.driver.del_subject(intra_extension_id, subject_id)

    @filter_input
    @enforce(("read", "write"), "subjects")
    def set_subject_dict(self, user_id, intra_extension_id, subject_id, subject_dict):
        subjects_dict = self.driver.get_subjects_dict(intra_extension_id)
        for subject_id in subjects_dict:
            if subjects_dict[subject_id]["name"] == subject_dict['name']:
                raise SubjectNameExisting("Subject {} already exists!".format(subject_dict['name']))
        # Next line will raise an error if user is not present in Keystone database
        subject_keystone_dict = self.identity_api.get_user_by_name(subject_dict['name'], "default")
        subject_dict["keystone_id"] = subject_keystone_dict["id"]
        subject_dict["keystone_name"] = subject_keystone_dict["name"]
        return self.driver.set_subject_dict(intra_extension_id, subject_dict["id"], subject_dict)

    @filter_input
    def get_subject_dict_from_keystone_id(self, tenant_id, intra_extension_id, keystone_id):
        tenants_dict = self.tenant_api.driver.get_tenants_dict()
        if tenant_id not in tenants_dict:
            raise TenantUnknown()
        if intra_extension_id not in (tenants_dict[tenant_id]['intra_authz_extension_id'],
                                      tenants_dict[tenant_id]['intra_admin_extension_id'], ):
            raise IntraExtensionUnknown()
        # Note (asteroide): We used self.root_admin_id because the user requesting this information
        # may only know his keystone_id and not the subject ID in the requested intra_extension.
        subjects_dict = self.get_subjects_dict(self.root_admin_id, intra_extension_id)
        for subject_id in subjects_dict:
            if keystone_id == subjects_dict[subject_id]['keystone_id']:
                return {subject_id: subjects_dict[subject_id]}

    @filter_input
    def get_subject_dict_from_keystone_name(self, tenant_id, intra_extension_id, keystone_name):
        tenants_dict = self.tenant_api.driver.get_tenants_dict()
        if tenant_id not in tenants_dict:
            raise TenantUnknown()
        if intra_extension_id not in (tenants_dict[tenant_id]['intra_authz_extension_id'],
                                      tenants_dict[tenant_id]['intra_admin_extension_id'], ):
            raise IntraExtensionUnknown()
        # Note (asteroide): We used self.root_admin_id because the user requesting this information
        # may only know his keystone_name and not the subject ID in the requested intra_extension.
        subjects_dict = self.get_subjects_dict(self.root_admin_id, intra_extension_id)
        for subject_id in subjects_dict:
            if keystone_name == subjects_dict[subject_id]['keystone_name']:
                return {subject_id: subjects_dict[subject_id]}

    @filter_input
    @enforce("read", "objects")
    def get_objects_dict(self, user_id, intra_extension_id):
        return self.driver.get_objects_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "objects")
    def add_object_dict(self, user_id, intra_extension_id, object_dict):
        objects_dict = self.driver.get_objects_dict(intra_extension_id)
        object_id = uuid4().hex
        if "id" in object_dict:
            object_id = object_dict['id']
        for _object_id in objects_dict:
            if objects_dict[_object_id]["name"] == object_dict['name']:
                raise ObjectNameExisting("Object {} already exist!".format(object_dict['name']))
        return self.driver.set_object_dict(intra_extension_id, object_id, object_dict)

    @filter_input
    @enforce("read", "objects")
    def get_object_dict(self, user_id, intra_extension_id, object_id):
        objects_dict = self.driver.get_objects_dict(intra_extension_id)
        if object_id not in objects_dict:
            raise ObjectUnknown("Unknown object id: {}".format(object_id))
        return objects_dict[object_id]

    @filter_input
    @enforce(("read", "write"), "objects")
    def del_object(self, user_id, intra_extension_id, object_id):
        if object_id not in self.driver.get_objects_dict(intra_extension_id):
            raise ObjectUnknown("Unknown object id: {}".format(object_id))
        # Destroy assignments related to this category
        for object_category_id in self.driver.get_object_categories_dict(intra_extension_id):
            for _object_id in self.driver.get_objects_dict(intra_extension_id):
                for assignment_id in self.driver.get_object_assignment_list(intra_extension_id, _object_id, object_category_id):
                    self.driver.del_object_assignment(intra_extension_id, _object_id, object_category_id, assignment_id)
        self.driver.del_object(intra_extension_id, object_id)

    @filter_input
    @enforce(("read", "write"), "objects")
    def set_object_dict(self, user_id, intra_extension_id, object_id, object_dict):
        objects_dict = self.driver.get_objects_dict(intra_extension_id)
        for object_id in objects_dict:
            if objects_dict[object_id]["name"] == object_dict['name']:
                raise ObjectNameExisting()
        return self.driver.set_object_dict(intra_extension_id, object_id, object_dict)

    @filter_input
    @enforce("read", "actions")
    def get_actions_dict(self, user_id, intra_extension_id):
        return self.driver.get_actions_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "actions")
    def add_action_dict(self, user_id, intra_extension_id, action_dict):
        actions_dict = self.driver.get_actions_dict(intra_extension_id)
        for action_id in actions_dict:
            if actions_dict[action_id]["name"] == action_dict['name']:
                raise ActionNameExisting()
        return self.driver.set_action_dict(intra_extension_id, uuid4().hex, action_dict)

    @filter_input
    @enforce("read", "actions")
    def get_action_dict(self, user_id, intra_extension_id, action_id):
        actions_dict = self.driver.get_actions_dict(intra_extension_id)
        if action_id not in actions_dict:
            raise ActionUnknown()
        return actions_dict[action_id]

    @filter_input
    @enforce(("read", "write"), "actions")
    def del_action(self, user_id, intra_extension_id, action_id):
        if action_id not in self.driver.get_actions_dict(intra_extension_id):
            raise ActionUnknown()
        # Destroy assignments related to this category
        for action_category_id in self.driver.get_action_categories_dict(intra_extension_id):
            for _action_id in self.driver.get_actions_dict(intra_extension_id):
                for assignment_id in self.driver.get_action_assignment_list(intra_extension_id, _action_id, action_category_id):
                    self.driver.del_action_assignment(intra_extension_id, _action_id, action_category_id, assignment_id)
        return self.driver.del_action(intra_extension_id, action_id)

    @filter_input
    @enforce(("read", "write"), "actions")
    def set_action_dict(self, user_id, intra_extension_id, action_id, action_dict):
        actions_dict = self.driver.get_actions_dict(intra_extension_id)
        for action_id in actions_dict:
            if actions_dict[action_id]["name"] == action_dict['name']:
                raise ActionNameExisting()
        return self.driver.set_action_dict(intra_extension_id, action_id, action_dict)

    # Scope functions

    @filter_input
    @enforce("read", "subject_scopes")
    @enforce("read", "subject_categories")
    def get_subject_scopes_dict(self, user_id, intra_extension_id, subject_category_id):
        """
        :param user_id:
        :param intra_extension_id:
        :param subject_category_id:
        :return: {
            subject_scope_id1: {
                name: xxx,
                des: aaa},
            subject_scope_id2: {
                name: yyy,
                des: bbb},
            ...}
        """
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        return self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id)

    @filter_input
    @enforce(("read", "write"), "subject_scopes")
    @enforce("read", "subject_categories")
    def add_subject_scope_dict(self, user_id, intra_extension_id, subject_category_id, subject_scope_dict):
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        subject_scopes_dict = self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id)
        for _subject_scope_id in subject_scopes_dict:
            if subject_scope_dict['name'] == subject_scopes_dict[_subject_scope_id]['name']:
                raise SubjectScopeNameExisting()
        return self.driver.set_subject_scope_dict(intra_extension_id, subject_category_id, uuid4().hex, subject_scope_dict)

    @filter_input
    @enforce("read", "subject_scopes")
    @enforce("read", "subject_categories")
    def get_subject_scope_dict(self, user_id, intra_extension_id, subject_category_id, subject_scope_id):
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        subject_scopes_dict = self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id)
        if subject_scope_id not in subject_scopes_dict:
            raise SubjectScopeUnknown()
        return subject_scopes_dict[subject_scope_id]

    @filter_input
    @enforce(("read", "write"), "subject_scopes")
    @enforce("read", "subject_categories")
    def del_subject_scope(self, user_id, intra_extension_id, subject_category_id, subject_scope_id):
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        if subject_scope_id not in self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id):
            raise SubjectScopeUnknown()
        # Destroy scope-related assignment
        for subject_id in self.driver.get_subjects_dict(intra_extension_id):
            for assignment_id in self.driver.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id):
                self.driver.del_subject_assignment(intra_extension_id, subject_id, subject_category_id, assignment_id)
        # Destroy scope-related rule
        for sub_meta_rule_id in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            rules_dict = self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id)
            for rule_id in rules_dict:
                if subject_scope_id in rules_dict[rule_id]:
                    self.driver.del_rule(intra_extension_id, sub_meta_rule_id, rule_id)
        self.driver.del_subject_scope(intra_extension_id, subject_category_id, subject_scope_id)

    @filter_input
    @enforce(("read", "write"), "subject_scopes")
    @enforce("read", "subject_categories")
    def set_subject_scope_dict(self, user_id, intra_extension_id, subject_category_id, subject_scope_id, subject_scope_dict):
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        subject_scopes_dict = self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id)
        for _subject_scope_id in subject_scopes_dict:
            if subject_scopes_dict[_subject_scope_id]['name'] == subject_scope_dict['name']:
                raise SubjectScopeNameExisting()
        return self.driver.set_subject_scope_dict(intra_extension_id, subject_category_id, subject_scope_id, subject_scope_dict)

    @filter_input
    @enforce("read", "object_scopes")
    @enforce("read", "object_categories")
    def get_object_scopes_dict(self, user_id, intra_extension_id, object_category_id):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        return self.driver.get_object_scopes_dict(intra_extension_id, object_category_id)

    @filter_input
    @enforce(("read", "write"), "object_scopes")
    @enforce("read", "object_categories")
    def add_object_scope_dict(self, user_id, intra_extension_id, object_category_id, object_scope_dict):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        object_scopes_dict = self.driver.get_object_scopes_dict(intra_extension_id, object_category_id)
        for _object_scope_id in object_scopes_dict:
            if object_scopes_dict[_object_scope_id]['name'] == object_scope_dict['name']:
                raise ObjectScopeNameExisting()
        return self.driver.set_object_scope_dict(intra_extension_id, object_category_id, uuid4().hex, object_scope_dict)

    @filter_input
    @enforce("read", "object_scopes")
    @enforce("read", "object_categories")
    def get_object_scope_dict(self, user_id, intra_extension_id, object_category_id, object_scope_id):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        object_scopes_dict = self.driver.get_object_scopes_dict(intra_extension_id, object_category_id)
        if object_scope_id not in object_scopes_dict:
            raise ObjectScopeUnknown()
        return object_scopes_dict[object_scope_id]

    @filter_input
    @enforce(("read", "write"), "object_scopes")
    @enforce("read", "object_categories")
    def del_object_scope(self, user_id, intra_extension_id, object_category_id, object_scope_id):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        if object_scope_id not in self.driver.get_object_scopes_dict(intra_extension_id, object_category_id):
            raise ObjectScopeUnknown()
        # Destroy scope-related assignment
        for object_id in self.driver.get_objects_dict(intra_extension_id):
            for assignment_id in self.driver.get_object_assignment_list(intra_extension_id, object_id, object_category_id):
                self.driver.del_object_assignment(intra_extension_id, object_id, object_category_id, assignment_id)
        # Destroy scope-related rule
        for sub_meta_rule_id in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            rules_dict = self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id)
            for rule_id in rules_dict:
                if object_scope_id in rules_dict[rule_id]:
                    self.driver.del_rule(intra_extension_id, sub_meta_rule_id, rule_id)
        self.driver.del_object_scope(intra_extension_id, object_category_id, object_scope_id)

    @filter_input
    @enforce(("read", "write"), "object_scopes")
    @enforce("read", "object_categories")
    def set_object_scope_dict(self, user_id, intra_extension_id, object_category_id, object_scope_id, object_scope_dict):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        object_scopes_dict = self.driver.get_object_scopes_dict(intra_extension_id, object_category_id)
        for _object_scope_id in object_scopes_dict:
            if object_scopes_dict[_object_scope_id]['name'] == object_scope_dict['name']:
                raise ObjectScopeNameExisting()
        return self.driver.set_object_scope_dict(intra_extension_id, object_category_id, object_scope_id, object_scope_dict)

    @filter_input
    @enforce("read", "action_scopes")
    @enforce("read", "action_categories")
    def get_action_scopes_dict(self, user_id, intra_extension_id, action_category_id):
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        return self.driver.get_action_scopes_dict(intra_extension_id, action_category_id)

    @filter_input
    @enforce(("read", "write"), "action_scopes")
    @enforce("read", "action_categories")
    def add_action_scope_dict(self, user_id, intra_extension_id, action_category_id, action_scope_dict):
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        action_scopes_dict = self.driver.get_action_scopes_dict(intra_extension_id, action_category_id)
        for _action_scope_id in action_scopes_dict:
            if action_scopes_dict[_action_scope_id]['name'] == action_scope_dict['name']:
                raise ActionScopeNameExisting()
        return self.driver.set_action_scope_dict(intra_extension_id, action_category_id, uuid4().hex, action_scope_dict)

    @filter_input
    @enforce("read", "action_scopes")
    @enforce("read", "action_categories")
    def get_action_scope_dict(self, user_id, intra_extension_id, action_category_id, action_scope_id):
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        action_scopes_dict = self.driver.get_action_scopes_dict(intra_extension_id, action_category_id)
        if action_scope_id not in action_scopes_dict:
            raise ActionScopeUnknown()
        return action_scopes_dict[action_scope_id]

    @filter_input
    @enforce(("read", "write"), "action_scopes")
    @enforce("read", "action_categories")
    def del_action_scope(self, user_id, intra_extension_id, action_category_id, action_scope_id):
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        if action_scope_id not in self.driver.get_action_scopes_dict(intra_extension_id, action_category_id):
            raise ActionScopeUnknown()
        # Destroy scope-related assignment
        for action_id in self.driver.get_actions_dict(intra_extension_id):
            for assignment_id in self.driver.get_action_assignment_list(intra_extension_id, action_id, action_category_id):
                self.driver.del_action_assignment(intra_extension_id, action_id, action_category_id, assignment_id)
        # Destroy scope-related rule
        for sub_meta_rule_id in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            rules_dict = self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id)
            for rule_id in rules_dict:
                if action_scope_id in rules_dict[rule_id]:
                    self.driver.del_rule(intra_extension_id, sub_meta_rule_id, rule_id)
        self.driver.del_action_scope(intra_extension_id, action_category_id, action_scope_id)

    @filter_input
    @enforce(("read", "write"), "action_scopes")
    @enforce("read", "action_categories")
    def set_action_scope_dict(self, user_id, intra_extension_id, action_category_id, action_scope_id, action_scope_dict):
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        action_scopes_dict = self.driver.get_action_scopes_dict(intra_extension_id, action_category_id)
        for _action_scope_id in action_scopes_dict:
            if action_scopes_dict[_action_scope_id]['name'] == action_scope_dict['name']:
                raise ActionScopeNameExisting()
        return self.driver.set_action_scope_dict(intra_extension_id, action_category_id, action_scope_id, action_scope_dict)

    # Assignment functions

    @filter_input
    @enforce("read", "subject_assignments")
    @enforce("read", "subjects")
    @enforce("read", "subject_categories")
    def get_subject_assignment_list(self, user_id, intra_extension_id, subject_id, subject_category_id):
        """
        :param user_id:
        :param intra_extension_id:
        :param subject_id:
        :param subject_category_id:
        :return: [
            subject_scope_id1, ..., subject_scope_idn
        ]
        """
        if subject_id not in self.driver.get_subjects_dict(intra_extension_id):
            raise SubjectUnknown()
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        return self.driver.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id)

    @filter_input
    @enforce(("read", "write"), "subject_assignments")
    @enforce("read", "subjects")
    @enforce("read", "subject_categories")
    @enforce("read", "subject_scopes")
    def add_subject_assignment_list(self, user_id, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        if subject_id not in self.driver.get_subjects_dict(intra_extension_id):
            raise SubjectUnknown()
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        if subject_scope_id not in self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id):
            raise SubjectScopeUnknown()
        elif subject_scope_id in self.driver.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id):
            raise SubjectAssignmentExisting()
        return self.driver.add_subject_assignment_list(intra_extension_id, subject_id, subject_category_id, subject_scope_id)

    @filter_input
    @enforce(("read", "write"), "subject_assignments")
    @enforce("read", "subjects")
    @enforce("read", "subject_categories")
    @enforce("read", "subject_scopes")
    def del_subject_assignment(self, user_id, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        if subject_id not in self.driver.get_subjects_dict(intra_extension_id):
            raise SubjectUnknown()
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        if subject_scope_id not in self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id):
            raise SubjectScopeUnknown()
        elif subject_scope_id not in self.driver.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id):
            raise SubjectAssignmentUnknown()
        self.driver.del_subject_assignment(intra_extension_id, subject_id, subject_category_id, subject_scope_id)

    @filter_input
    @enforce("read", "object_assignments")
    @enforce("read", "objects")
    @enforce("read", "object_categories")
    def get_object_assignment_list(self, user_id, intra_extension_id, object_id, object_category_id):
        if object_id not in self.driver.get_objects_dict(intra_extension_id):
            raise ObjectUnknown("Unknown object id: {}".format(object_id))
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        return self.driver.get_object_assignment_list(intra_extension_id, object_id, object_category_id)

    @filter_input
    @enforce(("read", "write"), "object_assignments")
    @enforce("read", "objects")
    @enforce("read", "object_categories")
    def add_object_assignment_list(self, user_id, intra_extension_id, object_id, object_category_id, object_scope_id):
        if object_id not in self.driver.get_objects_dict(intra_extension_id):
            raise ObjectUnknown("Unknown object id: {}".format(object_id))
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        if object_scope_id not in self.driver.get_object_scopes_dict(intra_extension_id, object_category_id):
            raise ObjectScopeUnknown()
        elif object_scope_id in self.driver.get_object_assignment_list(intra_extension_id, object_id, object_category_id):
            raise ObjectAssignmentExisting()
        return self.driver.add_object_assignment_list(intra_extension_id, object_id, object_category_id, object_scope_id)

    @filter_input
    @enforce(("read", "write"), "object_assignments")
    @enforce("read", "objects")
    @enforce("read", "object_categories")
    @enforce("read", "object_scopes")
    def del_object_assignment(self, user_id, intra_extension_id, object_id, object_category_id, object_scope_id):
        if object_id not in self.driver.get_objects_dict(intra_extension_id):
            raise ObjectUnknown("Unknown object id: {}".format(object_id))
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        if object_scope_id not in self.driver.get_object_scopes_dict(intra_extension_id, object_category_id):
            raise ObjectScopeUnknown()
        elif object_scope_id not in self.driver.get_object_assignment_list(intra_extension_id, object_id, object_category_id):
            raise ObjectAssignmentUnknown()
        self.driver.del_object_assignment(intra_extension_id, object_id, object_category_id, object_scope_id)

    @filter_input
    @enforce("read", "action_assignments")
    @enforce("read", "actions")
    @enforce("read", "action_categories")
    def get_action_assignment_list(self, user_id, intra_extension_id, action_id, action_category_id):
        if action_id not in self.driver.get_actions_dict(intra_extension_id):
            raise ActionUnknown()
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        return self.driver.get_action_assignment_list(intra_extension_id, action_id, action_category_id)

    @filter_input
    @enforce(("read", "write"), "action_assignments")
    @enforce("read", "actions")
    @enforce("read", "action_categories")
    def add_action_assignment_list(self, user_id, intra_extension_id, action_id, action_category_id, action_scope_id):
        if action_id not in self.driver.get_actions_dict(intra_extension_id):
            raise ActionUnknown()
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        if action_scope_id not in self.driver.get_action_scopes_dict(intra_extension_id, action_category_id):
            raise ActionScopeUnknown()
        elif action_scope_id in self.driver.get_action_assignment_list(intra_extension_id, action_id, action_category_id):
            raise ObjectAssignmentExisting()
        return self.driver.add_action_assignment_list(intra_extension_id, action_id, action_category_id, action_scope_id)

    @filter_input
    @enforce(("read", "write"), "action_assignments")
    @enforce("read", "actions")
    @enforce("read", "action_categories")
    @enforce("read", "action_scopes")
    def del_action_assignment(self, user_id, intra_extension_id, action_id, action_category_id, action_scope_id):
        if action_id not in self.driver.get_actions_dict(intra_extension_id):
            raise ActionUnknown()
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        if action_scope_id not in self.driver.get_action_scopes_dict(intra_extension_id, action_category_id):
            raise ActionScopeUnknown()
        elif action_scope_id not in self.driver.get_action_assignment_list(intra_extension_id, action_id, action_category_id):
            raise ActionAssignmentUnknown()
        self.driver.del_action_assignment(intra_extension_id, action_id, action_category_id, action_scope_id)

    # Metarule functions

    @filter_input
    @enforce("read", "aggregation_algorithm")
    def get_aggregation_algorithm_id(self, user_id, intra_extension_id):
        """
        :param user_id:
        :param intra_extension_id:
        :return: {
            aggregation_algorithm_id: {name: xxx, description: yyy}
            }
        """
        aggregation_algorithm_id = self.driver.get_aggregation_algorithm_id(intra_extension_id)
        if not aggregation_algorithm_id:
            raise AggregationAlgorithmNotExisting()
        return aggregation_algorithm_id

    @filter_input
    @enforce(("read", "write"), "aggregation_algorithm")
    def set_aggregation_algorithm_id(self, user_id, intra_extension_id, aggregation_algorithm_id):
        if aggregation_algorithm_id:
            if aggregation_algorithm_id not in self.configuration_api.get_aggregation_algorithms_dict(
                    self.root_admin_id):
                raise AggregationAlgorithmUnknown()
        return self.driver.set_aggregation_algorithm_id(intra_extension_id, aggregation_algorithm_id)

    @filter_input
    @enforce("read", "sub_meta_rules")
    def get_sub_meta_rules_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :param intra_extension_id:
        :return: {
            sub_meta_rule_id_1: {
                "name": xxx,
                "algorithm": yyy,
                "subject_categories": [subject_category_id1, subject_category_id2,...],
                "object_categories": [object_category_id1, object_category_id2,...],
                "action_categories": [action_category_id1, action_category_id2,...]
            sub_meta_rule_id_2: {...}
            ...
        }
        """
        return self.driver.get_sub_meta_rules_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "sub_meta_rules")
    @enforce("write", "rules")
    def add_sub_meta_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_dict):
        LOG.info("add_sub_meta_rule_dict = {}".format(self.driver.get_sub_meta_rules_dict(intra_extension_id)))
        LOG.info("add_sub_meta_rule_dict = {}".format(sub_meta_rule_dict))
        sub_meta_rules_dict = self.driver.get_sub_meta_rules_dict(intra_extension_id)
        for _sub_meta_rule_id in sub_meta_rules_dict:
            if sub_meta_rule_dict['name'] == sub_meta_rules_dict[_sub_meta_rule_id]["name"]:
                raise SubMetaRuleNameExisting()
            if sub_meta_rule_dict['subject_categories'] == sub_meta_rules_dict[_sub_meta_rule_id]["subject_categories"] and \
                sub_meta_rule_dict['object_categories'] == sub_meta_rules_dict[_sub_meta_rule_id]["object_categories"] and \
                sub_meta_rule_dict['action_categories'] == sub_meta_rules_dict[_sub_meta_rule_id]["action_categories"] and \
                sub_meta_rule_dict['algorithm'] == sub_meta_rules_dict[_sub_meta_rule_id]["algorithm"]:
                raise SubMetaRuleExisting()
        algorithm_names = map(lambda x: x['name'],
                                 self.configuration_api.get_sub_meta_rule_algorithms_dict(user_id).values())
        if sub_meta_rule_dict['algorithm'] not in algorithm_names:
            raise SubMetaRuleAlgorithmNotExisting()
        sub_meta_rule_id = uuid4().hex
        # TODO (dthom): add new sub-meta-rule to rule dict
        # self.driver.add_rule(intra_extension_id, sub_meta_rule_id, [])
        return self.driver.set_sub_meta_rule_dict(intra_extension_id, sub_meta_rule_id, sub_meta_rule_dict)

    @filter_input
    @enforce(("read", "write"), "sub_meta_rules")
    def get_sub_meta_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id):
        sub_meta_rule_dict = self.driver.get_sub_meta_rules_dict(intra_extension_id)
        if sub_meta_rule_id not in sub_meta_rule_dict:
            raise SubMetaRuleUnknown()
        return sub_meta_rule_dict[sub_meta_rule_id]

    @filter_input
    @enforce(("read", "write"), "sub_meta_rules")
    @enforce(("read", "write"), "rules")
    def del_sub_meta_rule(self, user_id, intra_extension_id, sub_meta_rule_id):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        for rule_id in self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id):
            self.del_rule(intra_extension_id, sub_meta_rule_id, rule_id)
        self.driver.del_sub_meta_rule(intra_extension_id, sub_meta_rule_id)

    @filter_input
    @enforce(("read", "write"), "sub_meta_rules")
    @enforce("write", "rules")
    def set_sub_meta_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id, sub_meta_rule_dict):
        LOG.info("set_sub_meta_rule_dict = {}".format(self.driver.get_sub_meta_rules_dict(intra_extension_id)))
        LOG.info("set_sub_meta_rule_dict = {} {}".format(sub_meta_rule_id, sub_meta_rule_dict))
        if sub_meta_rule_id not in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        for attribute in sub_meta_rule_dict.keys():
            if not sub_meta_rule_dict[attribute]:
                sub_meta_rule_dict.pop(attribute)
        return self.driver.set_sub_meta_rule_dict(intra_extension_id, sub_meta_rule_id, sub_meta_rule_dict)

    # Rule functions
    @filter_input
    @enforce("read", "rules")
    def get_rules_dict(self, user_id, intra_extension_id, sub_meta_rule_id):
        """
        :param user_id:
        :param intra_extension_id:
        :param sub_meta_rule_id:
        :return: {
            rule_id1: [subject_scope1, subject_scope2, ..., action_scope1, ..., object_scope1, ... ],
            rule_id2: [subject_scope3, subject_scope4, ..., action_scope3, ..., object_scope3, ... ],
            ...}
        """
        return self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id)

    @filter_input
    @enforce("read", "sub_meta_rules")
    @enforce(("read", "write"), "rules")
    def add_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id, rule_list):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        if rule_list in self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id).values():
            raise RuleExisting()
        return self.driver.set_rule_dict(intra_extension_id, sub_meta_rule_id, uuid4().hex, rule_list)

    @filter_input
    @enforce("read", "sub_meta_rules")
    @enforce("read", "rules")
    def get_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id, rule_id):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        rules_dict = self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id)
        if rule_id not in rules_dict:
            raise RuleUnknown()
        return rules_dict[rule_id]

    @filter_input
    @enforce("read", "sub_meta_rules")
    @enforce(("read", "write"), "rules")
    def del_rule(self, user_id, intra_extension_id, sub_meta_rule_id, rule_id):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        if rule_id not in self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id):
            raise RuleUnknown()
        self.driver.del_rule(intra_extension_id, sub_meta_rule_id, rule_id)

    @filter_input
    @enforce("read", "sub_meta_rules")
    @enforce(("read", "write"), "rules")
    def set_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id, rule_id, rule_list):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        if rule_id not in self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id):
            raise RuleUnknown()
        return self.driver.set_rule_dict(intra_extension_id, sub_meta_rule_id, rule_id, rule_list)


@dependency.provider('authz_api')
class IntraExtensionAuthzManager(IntraExtensionManager):

    def __init__(self):
        super(IntraExtensionAuthzManager, self).__init__()

    def __authz(self, tenant_id, subject_k_id, object_name, action_name, genre="authz"):
        """Check authorization for a particular action.
        :return: True or False or raise an exception
        """
        if genre == "authz":
            genre = "intra_authz_extension_id"
        elif genre == "admin":
            genre = "intra_admin_extension_id"

        tenants_dict = self.tenant_api.get_tenants_dict(self.root_admin_id)

        if tenant_id not in tenants_dict:
            # raise TenantUnknown("Cannot authz because Tenant is unknown {}".format(tenant_id))
            LOG.warning("Cannot authz because Tenant is not managed by Moon {}".format(tenant_id))
            return {'authz': True, 'comment': "Cannot authz because Tenant is not managed by Moon {}".format(tenant_id)}
        intra_extension_id = tenants_dict[tenant_id][genre]
        if not intra_extension_id:
            raise TenantNoIntraExtension()
        subjects_dict = self.driver.get_subjects_dict(intra_extension_id)
        subject_id = None
        for _subject_id in subjects_dict:
            if subjects_dict[_subject_id]['keystone_id'] == subject_k_id:
                subject_id = _subject_id
                break
        if not subject_id:
            raise SubjectUnknown("Unknown subject id: {}".format(subject_k_id))
        objects_dict = self.driver.get_objects_dict(intra_extension_id)
        object_id = None
        for _object_id in objects_dict:
            if objects_dict[_object_id]['name'] == object_name:
                object_id = _object_id
                break
        if not object_id:
            raise ObjectUnknown("Unknown object name: {}".format(object_name))

        actions_dict = self.driver.get_actions_dict(intra_extension_id)
        action_id = None
        for _action_id in actions_dict:
            if actions_dict[_action_id]['name'] == action_name:
                action_id = _action_id
                break
        if not action_id:
            raise ActionUnknown("Unknown action name: {}".format(action_name))
        return super(IntraExtensionAuthzManager, self).authz(intra_extension_id, subject_id, object_id, action_id)

    def authz(self, tenant_id, subject_k_id, object_name, action_name, genre="authz"):
        try:
            return self.__authz(tenant_id, subject_k_id, object_name, action_name, genre="authz")
        except (SubjectUnknown, ObjectUnknown, ActionUnknown) as e:
            # maybe we need to synchronize with the master
            if CONF.moon.master:
                self.get_data_from_master()
                return self.__authz(tenant_id, subject_k_id, object_name, action_name, genre="authz")
            raise e
        except TenantNoIntraExtension:
            return {'authz': True, 'comment': "Cannot authz because Tenant is not managed by Moon {}".format(tenant_id)}

    def add_subject_dict(self, user_id, intra_extension_id, subject_dict):
        subject = super(IntraExtensionAuthzManager, self).add_subject_dict(user_id, intra_extension_id, subject_dict)
        subject_id,  subject_value = subject.iteritems().next()
        tenants_dict = self.tenant_api.get_tenants_dict(self.root_admin_id)
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]["intra_admin_extension_id"] and \
                            tenants_dict[tenant_id]["intra_authz_extension_id"] == intra_extension_id:
                _subjects = self.driver.get_subjects_dict(tenants_dict[tenant_id]["intra_admin_extension_id"])
                if subject_value["name"] not in [_subjects[_id]["name"] for _id in _subjects]:
                    self.driver.set_subject_dict(tenants_dict[tenant_id]["intra_admin_extension_id"], uuid4().hex, subject_value)
                break
            if tenants_dict[tenant_id]["intra_authz_extension_id"] and \
                            tenants_dict[tenant_id]["intra_admin_extension_id"] == intra_extension_id:
                _subjects = self.driver.get_subjects_dict(tenants_dict[tenant_id]["intra_authz_extension_id"])
                if subject_value["name"] not in [_subjects[_id]["name"] for _id in _subjects]:
                    self.driver.set_subject_dict(tenants_dict[tenant_id]["intra_authz_extension_id"], uuid4().hex, subject_value)
                break
        return subject

    def del_subject(self, user_id, intra_extension_id, subject_id):
        subject_name = self.driver.get_subjects_dict(intra_extension_id)[subject_id]["name"]
        super(IntraExtensionAuthzManager, self).del_subject(user_id, intra_extension_id, subject_id)
        tenants_dict = self.tenant_api.get_tenants_dict(self.root_admin_id)
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]["intra_authz_extension_id"] == intra_extension_id and \
                tenants_dict[tenant_id]["intra_admin_extension_id"]:
                subject_id = self.driver.get_uuid_from_name(tenants_dict[tenant_id]["intra_admin_extension_id"],
                                                            subject_name,
                                                            self.driver.SUBJECT)
                self.driver.del_subject(tenants_dict[tenant_id]["intra_admin_extension_id"], subject_id)
                break
            if tenants_dict[tenant_id]["intra_admin_extension_id"] == intra_extension_id and \
                tenants_dict[tenant_id]["intra_authz_extension_id"]:
                subject_id = self.driver.get_uuid_from_name(tenants_dict[tenant_id]["intra_authz_extension_id"],
                                                            subject_name,
                                                            self.driver.SUBJECT)
                self.driver.del_subject(tenants_dict[tenant_id]["intra_authz_extension_id"], subject_id)
                break

    def set_subject_dict(self, user_id, intra_extension_id, subject_id, subject_dict):
        subject = super(IntraExtensionAuthzManager, self).set_subject_dict(user_id, intra_extension_id, subject_dict)
        subject_id,  subject_value = subject.iteritems().next()
        tenants_dict = self.tenant_api.get_tenants_dict(self.root_admin_id)
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]["intra_authz_extension_id"] == intra_extension_id:
                self.driver.set_subject_dict(tenants_dict[tenant_id]["intra_admin_extension_id"], uuid4().hex, subject_value)
                break
            if tenants_dict[tenant_id]["intra_admin_extension_id"] == intra_extension_id:
                self.driver.set_subject_dict(tenants_dict[tenant_id]["intra_authz_extension_id"], uuid4().hex, subject_value)
                break
        return subject

    def add_subject_category(self, user_id, intra_extension_id, subject_category_dict):
        raise AuthzException("add_subject_category")

    def del_subject_category(self, user_id, intra_extension_id, subject_category_id):
        raise AuthzException("del_subject_category")

    def set_subject_category(self, user_id, intra_extension_id, subject_category_id, subject_category_dict):
        raise AuthzException("set_subject_category")

    def add_object_category(self, user_id, intra_extension_id, object_category_dict):
        raise AuthzException("add_object_category")

    def del_object_category(self, user_id, intra_extension_id, object_category_id):
        raise AuthzException("del_object_category")

    def add_action_category(self, user_id, intra_extension_id, action_category_name):
        raise AuthzException("add_action_category")

    def del_action_category(self, user_id, intra_extension_id, action_category_id):
        raise AuthzException("del_action_category")

    def add_object_dict(self, user_id, intra_extension_id, object_name):
        raise AuthzException("add_object_dict")

    def set_object_dict(self, user_id, intra_extension_id, object_id, object_dict):
        raise AuthzException("set_object_dict")

    def del_object(self, user_id, intra_extension_id, object_id):
        raise AuthzException("del_object")

    def add_action_dict(self, user_id, intra_extension_id, action_name):
        raise AuthzException("add_action_dict")

    def set_action_dict(self, user_id, intra_extension_id, action_id, action_dict):
        raise AuthzException("set_action_dict")

    def del_action(self, user_id, intra_extension_id, action_id):
        raise AuthzException("del_action")

    def add_subject_scope_dict(self, user_id, intra_extension_id, subject_category_id, subject_scope_dict):
        raise AuthzException("add_subject_scope_dict")

    def del_subject_scope(self, user_id, intra_extension_id, subject_category_id, subject_scope_id):
        raise AuthzException("del_subject_scope")

    def set_subject_scope_dict(self, user_id, intra_extension_id, subject_category_id, subject_scope_id, subject_scope_name):
        raise AuthzException("set_subject_scope_dict")

    def add_object_scope_dict(self, user_id, intra_extension_id, object_category_id, object_scope_name):
        raise AuthzException("add_object_scope_dict")

    def del_object_scope(self, user_id, intra_extension_id, object_category_id, object_scope_id):
        raise AuthzException("del_object_scope")

    def set_object_scope_dict(self, user_id, intra_extension_id, object_category_id, object_scope_id, object_scope_name):
        raise AuthzException("set_object_scope_dict")

    def add_action_scope_dict(self, user_id, intra_extension_id, action_category_id, action_scope_name):
        raise AuthzException("add_action_scope_dict")

    def del_action_scope(self, user_id, intra_extension_id, action_category_id, action_scope_id):
        raise AuthzException("del_action_scope")

    def add_subject_assignment_list(self, user_id, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        raise AuthzException("add_subject_assignment_list")

    def del_subject_assignment(self, user_id, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        raise AuthzException("del_subject_assignment")

    def add_object_assignment_list(self, user_id, intra_extension_id, object_id, object_category_id, object_scope_id):
        raise AuthzException("add_object_assignment_list")

    def del_object_assignment(self, user_id, intra_extension_id, object_id, object_category_id, object_scope_id):
        raise AuthzException("del_object_assignment")

    def add_action_assignment_list(self, user_id, intra_extension_id, action_id, action_category_id, action_scope_id):
        raise AuthzException("add_action_assignment_list")

    def del_action_assignment(self, user_id, intra_extension_id, action_id, action_category_id, action_scope_id):
        raise AuthzException("del_action_assignment")

    def set_aggregation_algorithm_id(self, user_id, intra_extension_id, aggregation_algorithm_id):
        raise AuthzException("set_aggregation_algorithm_id")

    def del_aggregation_algorithm_(self, user_id, intra_extension_id):
        raise AuthzException("del_aggregation_algorithm_")

    def add_sub_meta_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_dict):
        raise AuthzException("add_sub_meta_rule_dict")

    def del_sub_meta_rule(self, user_id, intra_extension_id, sub_meta_rule_id):
        raise AuthzException("del_sub_meta_rule")

    def set_sub_meta_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id, sub_meta_rule_dict):
        raise AuthzException("set_sub_meta_rule_dict")

    def add_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id, rule_list):
        raise AuthzException("add_rule_dict")

    def del_rule(self, user_id, intra_extension_id, sub_meta_rule_id, rule_id):
        raise AuthzException("del_rule")

    def set_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id, rule_id, rule_list):
        raise AuthzException("set_rule_dict")


@dependency.provider('admin_api')
class IntraExtensionAdminManager(IntraExtensionManager):

    def __init__(self):
        super(IntraExtensionAdminManager, self).__init__()

    def add_subject_dict(self, user_id, intra_extension_id, subject_dict):
        subject = super(IntraExtensionAdminManager, self).add_subject_dict(user_id, intra_extension_id, subject_dict)
        subject_id,  subject_value = subject.iteritems().next()
        tenants_dict = self.tenant_api.get_tenants_dict(self.root_admin_id)
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]["intra_admin_extension_id"] and \
                            tenants_dict[tenant_id]["intra_authz_extension_id"] == intra_extension_id:
                _subjects = self.driver.get_subjects_dict(tenants_dict[tenant_id]["intra_admin_extension_id"])
                if subject_value["name"] not in [_subjects[_id]["name"] for _id in _subjects]:
                    self.driver.set_subject_dict(tenants_dict[tenant_id]["intra_admin_extension_id"], uuid4().hex, subject_value)
                break
            if tenants_dict[tenant_id]["intra_authz_extension_id"] and \
                            tenants_dict[tenant_id]["intra_admin_extension_id"] == intra_extension_id:
                _subjects = self.driver.get_subjects_dict(tenants_dict[tenant_id]["intra_authz_extension_id"])
                if subject_value["name"] not in [_subjects[_id]["name"] for _id in _subjects]:
                    self.driver.set_subject_dict(tenants_dict[tenant_id]["intra_authz_extension_id"], uuid4().hex, subject_value)
                break
        return subject

    def del_subject(self, user_id, intra_extension_id, subject_id):
        subject_name = self.driver.get_subjects_dict(intra_extension_id)[subject_id]["name"]
        super(IntraExtensionAdminManager, self).del_subject(user_id, intra_extension_id, subject_id)
        tenants_dict = self.tenant_api.get_tenants_dict(self.root_admin_id)
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]["intra_authz_extension_id"] == intra_extension_id and \
                tenants_dict[tenant_id]["intra_admin_extension_id"]:
                subject_id = self.driver.get_uuid_from_name(tenants_dict[tenant_id]["intra_admin_extension_id"],
                                                            subject_name,
                                                            self.driver.SUBJECT)
                self.driver.del_subject(tenants_dict[tenant_id]["intra_admin_extension_id"], subject_id)
                break
            if tenants_dict[tenant_id]["intra_admin_extension_id"] == intra_extension_id and \
                tenants_dict[tenant_id]["intra_authz_extension_id"]:
                subject_id = self.driver.get_uuid_from_name(tenants_dict[tenant_id]["intra_authz_extension_id"],
                                                            subject_name,
                                                            self.driver.SUBJECT)
                self.driver.del_subject(tenants_dict[tenant_id]["intra_authz_extension_id"], subject_id)
                break

    def set_subject_dict(self, user_id, intra_extension_id, subject_id, subject_dict):
        subject = super(IntraExtensionAdminManager, self).set_subject_dict(user_id, intra_extension_id, subject_dict)
        subject_id,  subject_value = subject.iteritems().next()
        tenants_dict = self.tenant_api.get_tenants_dict(self.root_admin_id)
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]["intra_authz_extension_id"] == intra_extension_id:
                self.driver.set_subject_dict(tenants_dict[tenant_id]["intra_admin_extension_id"], uuid4().hex, subject_value)
                break
            if tenants_dict[tenant_id]["intra_admin_extension_id"] == intra_extension_id:
                self.driver.set_subject_dict(tenants_dict[tenant_id]["intra_authz_extension_id"], uuid4().hex, subject_value)
                break
        return subject

    def add_object_dict(self, user_id, intra_extension_id, object_name):
        if "admin" == self.get_intra_extension_dict(self.root_admin_id, intra_extension_id)['genre']:
            raise ObjectsWriteNoAuthorized()
        return super(IntraExtensionAdminManager, self).add_object_dict(user_id, intra_extension_id, object_name)

    def set_object_dict(self, user_id, intra_extension_id, object_id, object_dict):
        if "admin" == self.get_intra_extension_dict(self.root_admin_id, intra_extension_id)['genre']:
            raise ObjectsWriteNoAuthorized()
        return super(IntraExtensionAdminManager, self).set_object_dict(user_id, intra_extension_id, object_id, object_dict)

    def del_object(self, user_id, intra_extension_id, object_id):
        if "admin" == self.get_intra_extension_dict(self.root_admin_id, intra_extension_id)['genre']:
            raise ObjectsWriteNoAuthorized()
        return super(IntraExtensionAdminManager, self).del_object(user_id, intra_extension_id, object_id)

    def add_action_dict(self, user_id, intra_extension_id, action_name):
        if "admin" == self.get_intra_extension_dict(self.root_admin_id, intra_extension_id)['genre']:
            raise ActionsWriteNoAuthorized()
        return super(IntraExtensionAdminManager, self).add_action_dict(user_id, intra_extension_id, action_name)

    def set_action_dict(self, user_id, intra_extension_id, action_id, action_dict):
        if "admin" == self.get_intra_extension_dict(self.root_admin_id, intra_extension_id)['genre']:
            raise ActionsWriteNoAuthorized()
        return super(IntraExtensionAdminManager, self).set_action_dict(user_id, intra_extension_id, action_id, action_dict)

    def del_action(self, user_id, intra_extension_id, action_id):
        if "admin" == self.get_intra_extension_dict(self.root_admin_id, intra_extension_id)['genre']:
            raise ActionsWriteNoAuthorized()
        return super(IntraExtensionAdminManager, self).del_action(user_id, intra_extension_id, action_id)


@dependency.provider('root_api')
class IntraExtensionRootManager(IntraExtensionManager):

    def __init__(self):
        super(IntraExtensionRootManager, self).__init__()

    def is_admin_subject(self, keystone_id):
        for subject_id, subject_dict in self.driver.get_subjects_dict(self.root_extension_id).iteritems():
            if subject_id == keystone_id:
                # subject_id may be a true id from an intra_extension
                return True
            if subject_dict["name"] == "admin" and subject_dict["keystone_id"] == keystone_id:
                return True
        return False


@dependency.provider('moonlog_api')
class LogManager(manager.Manager):

    driver_namespace = 'keystone.moon.log'

    def __init__(self):
        driver = CONF.moon.log_driver
        super(LogManager, self).__init__(driver)

    def get_logs(self, logger="authz", options="", event_number=None, time_from=None, time_to=None, filter_str=None):

        if len(options) > 0:
            options = options.split(",")
            event_number = None
            time_from = None
            time_to = None
            filter_str = None
            for opt in options:
                if "event_number" in opt:
                    event_number = "".join(re.findall("\d*", opt.split("=")[-1]))
                    try:
                        event_number = int(event_number)
                    except ValueError:
                        event_number = None
                elif "from" in opt:
                    time_from = "".join(re.findall("[\w\-:]*", opt.split("=")[-1]))
                    try:
                        time_from = time.strptime(time_from, self.TIME_FORMAT)
                    except ValueError:
                        time_from = None
                elif "to" in opt:
                    time_to = "".join(re.findall("[\w\-:] *", opt.split("=")[-1]))
                    try:
                        time_to = time.strptime(time_to, self.TIME_FORMAT)
                    except ValueError:
                        time_to = None
                elif "filter" in opt:
                    filter_str = "".join(re.findall("\w*", opt.split("=")[-1]))
        return self.driver.get_logs(logger, event_number, time_from, time_to, filter_str)

    def get_authz_logs(self, options="", event_number=None, time_from=None, time_to=None, filter_str=None):
        return self.get_logs(
            logger="authz",
            options="",
            event_number=None,
            time_from=None,
            time_to=None,
            filter_str=None)

    def get_sys_logs(self, options="", event_number=None, time_from=None, time_to=None, filter_str=None):
        return self.get_logs(
            logger="sys",
            options="",
            event_number=None,
            time_from=None,
            time_to=None,
            filter_str=None)

    def authz(self, message):
        return self.driver.authz(message)

    def debug(self, message):
        return self.driver.debug(message)

    def info(self, message):
        return self.driver.info(message)

    def warning(self, message):
        return self.driver.warning(message)

    def error(self, message):
        return self.driver.error(message)

    def critical(self, message):
        return self.driver.critical(message)


class ConfigurationDriver(object):

    def get_policy_templates_dict(self):
        raise exception.NotImplemented()  # pragma: no cover

    def get_aggregation_algorithm_id(self):
        raise exception.NotImplemented()  # pragma: no cover

    def get_sub_meta_rule_algorithms_dict(self):
        raise exception.NotImplemented()  # pragma: no cover


class TenantDriver(object):

    def get_tenants_dict(self):
        raise exception.NotImplemented()  # pragma: no cover

    def add_tenant_dict(self, tenant_id, tenant_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_tenant_dict(self, tenant_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_tenant_dict(self, tenant_id, tenant_dict):
        raise exception.NotImplemented()  # pragma: no cover


class IntraExtensionDriver(object):

    SUBJECT = 'subject'
    OBJECT = 'object'
    ACTION = 'action'
    SUBJECT_CATEGORY = 'subject_category'
    OBJECT_CATEGORY = 'object_category'
    ACTION_CATEGORY = 'action_category'
    SUBJECT_SCOPE = 'subject_scope'
    OBJECT_SCOPE = 'object_scope'
    ACTION_SCOPE = 'action_scope'
    SUB_META_RULE = 'sub_meta_rule'

    def __get_data_from_type(self,
                             intra_extension_uuid,
                             name=None,
                             uuid=None,
                             data_name=None,
                             category_name=None,
                             category_uuid=None):

        def extract_name(data_dict):
            for key in data_dict:
                try:
                    yield data_dict[key]["name"]
                except KeyError:
                    for key2 in data_dict[key]:
                        yield data_dict[key][key2]["name"]

        data_values = list()

        if data_name == self.SUBJECT:
            data_values = self.get_subjects_dict(intra_extension_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise SubjectUnknown("{} / {}".format(name, data_values))
        elif data_name == self.OBJECT:
            data_values = self.get_objects_dict(intra_extension_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise ObjectUnknown("{} / {}".format(name, data_values))
        elif data_name == self.ACTION:
            data_values = self.get_actions_dict(intra_extension_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise ActionUnknown("{} / {}".format(name, data_values))
        elif data_name == self.SUBJECT_CATEGORY:
            data_values = self.get_subject_categories_dict(intra_extension_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise SubjectCategoryUnknown("{} / {}".format(name, data_values))
        elif data_name == self.OBJECT_CATEGORY:
            data_values = self.get_object_categories_dict(intra_extension_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise ObjectCategoryUnknown("{} / {}".format(name, data_values))
        elif data_name == self.ACTION_CATEGORY:
            data_values = self.get_action_categories_dict(intra_extension_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise ActionCategoryUnknown("{} / {}".format(name, data_values))
        elif data_name == self.SUBJECT_SCOPE:
            if not category_uuid:
                category_uuid = self.get_uuid_from_name(intra_extension_uuid, category_name, self.SUBJECT_CATEGORY)
            data_values = self.get_subject_scopes_dict(intra_extension_uuid,
                                                       category_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise SubjectScopeUnknown("{} / {}".format(name, data_values))
        elif data_name == self.OBJECT_SCOPE:
            if not category_uuid:
                category_uuid = self.get_uuid_from_name(intra_extension_uuid, category_name, self.OBJECT_CATEGORY)
            data_values = self.get_object_scopes_dict(intra_extension_uuid,
                                                      category_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise ObjectScopeUnknown("{} / {}".format(name, data_values))
        elif data_name == self.ACTION_SCOPE:
            if not category_uuid:
                category_uuid = self.get_uuid_from_name(intra_extension_uuid, category_name, self.ACTION_CATEGORY)
            data_values = self.get_action_scopes_dict(intra_extension_uuid,
                                                      category_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise ActionScopeUnknown("{} / {}".format(name, data_values))
        elif data_name == self.SUB_META_RULE:
            data_values = self.get_sub_meta_rules_dict(intra_extension_uuid)
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise SubMetaRuleUnknown("{} / {}".format(name, data_values))
        # if data_name in (
        #     self.SUBJECT_SCOPE,
        #     self.OBJECT_SCOPE,
        #     self.ACTION_SCOPE
        # ):
        #     return data_values[category_uuid]
        return data_values

    def get_uuid_from_name(self, intra_extension_uuid, name, data_name, category_name=None, category_uuid=None):
        data_values = self.__get_data_from_type(
            intra_extension_uuid=intra_extension_uuid,
            name=name,
            data_name=data_name,
            category_name=category_name,
            category_uuid=category_uuid,
        )
        return filter(lambda v: v[1]["name"] == name, data_values.iteritems())[0][0]

    def get_name_from_uuid(self, intra_extension_uuid, uuid, data_name, category_name=None, category_uuid=None):
        data_values = self.__get_data_from_type(
            intra_extension_uuid=intra_extension_uuid,
            uuid=uuid,
            data_name=data_name,
            category_name=category_name,
            category_uuid=category_uuid,
        )
        return data_values[uuid]

    # Getter and Setter for intra_extension

    def get_intra_extensions_dict(self):
        raise exception.NotImplemented()  # pragma: no cover

    def del_intra_extension(self, intra_extension_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_intra_extension_dict(self, intra_extension_id, intra_extension_dict):
        raise exception.NotImplemented()  # pragma: no cover

    # Metadata functions

    def get_subject_categories_dict(self, intra_extension_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_category_dict(self, intra_extension_id, subject_category_id, subject_category_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_subject_category(self, intra_extension_id, subject_category_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_object_categories_dict(self, intra_extension_id):
        """Get a list of all object categories

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :return: a dictionary containing all object categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_category_dict(self, intra_extension_id, object_category_id, object_category_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_object_category(self, intra_extension_id, object_category_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_action_categories_dict(self, intra_extension_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_category_dict(self, intra_extension_id, action_category_id, action_category_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_action_category(self, intra_extension_id, action_category_id):
        raise exception.NotImplemented()  # pragma: no cover

    #  Perimeter functions

    def get_subjects_dict(self, intra_extension_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_dict(self, intra_extension_id, subject_id, subject_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_subject(self, intra_extension_id, subject_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_objects_dict(self, intra_extension_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_dict(self, intra_extension_id, object_id, object_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_object(self, intra_extension_id, object_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_actions_dict(self, intra_extension_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_dict(self, intra_extension_id, action_id, action_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_action(self, intra_extension_id, action_id):
        raise exception.NotImplemented()  # pragma: no cover

    # Scope functions

    def get_subject_scopes_dict(self, intra_extension_id, subject_category_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_scope_dict(self, intra_extension_id, subject_category_id, subject_scope_id, subject_scope_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_subject_scope(self, intra_extension_id, subject_category_id, subject_scope_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_object_scopes_dict(self, intra_extension_id, object_category_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_scope_dict(self, intra_extension_id, object_category_id, object_scope_id, object_scope_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_object_scope(self, intra_extension_id, object_category_id, object_scope_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_action_scopes_dict(self, intra_extension_id, action_category_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_scope_dict(self, intra_extension_id, action_category_id, action_scope_id, action_scope_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_action_scope(self, intra_extension_id, action_category_id, action_scope_id):
        raise exception.NotImplemented()  # pragma: no cover

    # Assignment functions

    def get_subject_assignment_list(self, intra_extension_id, subject_id, subject_category_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_assignment_list(self, intra_extension_id, subject_id, subject_category_id, subject_assignment_list):
        raise exception.NotImplemented()  # pragma: no cover

    def add_subject_assignment_list(self, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        raise exception.NotImplemented()  # pragma: no cover

    def del_subject_assignment(self, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_object_assignment_list(self, intra_extension_id, object_id, object_category_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_assignment_list(self, intra_extension_id, object_id, object_category_id, object_assignment_list):
        raise exception.NotImplemented()  # pragma: no cover

    def add_object_assignment_list(self, intra_extension_id, object_id, object_category_id, object_scope_id):
        raise exception.NotImplemented()  # pragma: no cover

    def del_object_assignment(self, intra_extension_id, object_id, object_category_id, object_scope_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_action_assignment_list(self, intra_extension_id, action_id, action_category_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_assignment_list(self, intra_extension_id, action_id, action_category_id, action_assignment_list):
        raise exception.NotImplemented()  # pragma: no cover

    def add_action_assignment_list(self, intra_extension_id, action_id, action_category_id, action_scope_id):
        raise exception.NotImplemented()  # pragma: no cover

    def del_action_assignment(self, intra_extension_id, action_id, action_category_id, action_scope_id):
        raise exception.NotImplemented()  # pragma: no cover

    # Meta_rule functions

    def set_aggregation_algorithm_id(self, intra_extension_id, aggregation_algorithm_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_aggregation_algorithm_id(self, intra_extension_id):
        raise exception.NotImplemented()  # pragma: no cover

    def del_aggregation_algorithm(self, intra_extension_id):
        raise exception.NotImplemented()  # pragma: no cover

    def get_sub_meta_rules_dict(self, intra_extension_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_sub_meta_rule_dict(self, intra_extension_id, sub_meta_rule_id, meta_rule_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def del_sub_meta_rule(self, intra_extension_id, sub_meta_rule_id):
        raise exception.NotImplemented()  # pragma: no cover

    # Rule functions

    def get_rules_dict(self, intra_extension_id, sub_meta_rule_id):
        raise exception.NotImplemented()  # pragma: no cover

    def set_rule_dict(self, intra_extension_id, sub_meta_rule_id, rule_id, rule_list):
        raise exception.NotImplemented()  # pragma: no cover

    def del_rule(self, intra_extension_id, sub_meta_rule_id, rule_id):
        raise exception.NotImplemented()  # pragma: no cover


class LogDriver(object):

    def authz(self, message):
        """Log authorization message

        :param message: the message to log
        :type message: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def debug(self, message):
        """Log debug message

        :param message: the message to log
        :type message: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def info(self, message):
        """Log informational message

        :param message: the message to log
        :type message: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def warning(self, message):
        """Log warning message

        :param message: the message to log
        :type message: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def error(self, message):
        """Log error message

        :param message: the message to log
        :type message: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def critical(self, message):
        """Log critical message

        :param message: the message to log
        :type message: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_logs(self, options):
        """Get logs

        :param options: options to filter log events
        :type options: string eg: "event_number=10,from=2014-01-01-10:10:10,to=2014-01-01-12:10:10,filter=expression"
        :return: a list of log events

        TIME_FORMAT is '%Y-%m-%d-%H:%M:%S'
        """
        raise exception.NotImplemented()  # pragma: no cover


# @dependency.provider('interextension_api')
# @dependency.requires('identity_api')
# class InterExtensionManager(manager.Manager):
#
#     def __init__(self):
#         driver = CONF.moon.interextension_driver
#         super(InterExtensionManager, self).__init__(driver)
#
#     def check_inter_extension(self, uuid):
#         if uuid not in self.get_inter_extensions():
#             LOG.error("Unknown InterExtension {}".format(uuid))
#             raise exception.NotFound("InterExtension not found.")
#
#     def get_inter_extensions(self):
#         return self.driver.get_inter_extensions()
#
#     def get_inter_extension(self, uuid):
#         return self.driver.get_inter_extension(uuid)
#
#     def create_inter_extension(self, inter_extension):
#         ie = dict()
#         ie['id'] = uuid4().hex
#         ie["requesting_intra_extension_uuid"] = filter_input(inter_extension["requesting_intra_extension_uuid"])
#         ie["requested_intra_extension_uuid"] = filter_input(inter_extension["requested_intra_extension_uuid"])
#         ie["description"] = filter_input(inter_extension["description"])
#         ie["virtual_entity_uuid"] = filter_input(inter_extension["virtual_entity_uuid"])
#         ie["genre"] = filter_input(inter_extension["genre"])
#
#         ref = self.driver.create_inter_extensions(ie['id'], ie)
#         return ref
#
#     def delete_inter_extension(self, inter_extension_id):
#         LOG.error("Deleting {}".format(inter_extension_id))
#         ref = self.driver.delete_inter_extensions(inter_extension_id)
#         return ref
#
#
# class InterExtensionDriver(object):
#
#     # Getter and Setter for InterExtensions
#
#     def get_inter_extensions(self):
#         raise exception.NotImplemented()  # pragma: no cover
#
#     def get_inter_extension(self, uuid):
#         raise exception.NotImplemented()  # pragma: no cover
#
#     def create_inter_extensions(self, intra_id, intra_extension):
#         raise exception.NotImplemented()  # pragma: no cover
#
#     def delete_inter_extensions(self, intra_extension_id):
#         raise exception.NotImplemented()  # pragma: no cover
#
#
# class VirtualEntityDriver(object):
#
#     # Getter and Setter for InterExtensions
#
#     def get_virtual_entities(self):
#         raise exception.NotImplemented()  # pragma: no cover
#
#     def create_virtual_entities(self, ve_id, virtual_entity):
#         raise exception.NotImplemented()  # pragma: no cover

