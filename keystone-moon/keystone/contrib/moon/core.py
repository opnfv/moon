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

from keystone.common import manager
from keystone import config
from oslo_log import log
from keystone.common import dependency
from keystone import exception
from oslo_config import cfg
from keystone.i18n import _

from keystone.contrib.moon.exception import *
from keystone.contrib.moon.algorithms import *

CONF = config.CONF
LOG = log.getLogger(__name__)
DEFAULT_USER = uuid4().hex  # default user_id for internal invocation


_OPTS = [
    cfg.StrOpt('configuration_driver',
               default='keystone.contrib.moon.backends.sql.ConfigurationConnector',
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
    cfg.StrOpt('superextension_driver',
               default='keystone.contrib.moon.backends.flat.SuperExtensionConnector',
               help='SuperExtension backend driver.'),
    cfg.StrOpt('log_driver',
               default='keystone.contrib.moon.backends.flat.LogConnector',
               help='Logs backend driver.'),
    cfg.StrOpt('policy_directory',
               default='/etc/keystone/policies',
               help='Local directory where all policies are stored.'),
    cfg.StrOpt('super_extension_directory',
               default='/etc/keystone/super_extension',
               help='Local directory where SuperExtension configuration is stored.'),
]
CONF.register_opts(_OPTS, group='moon')


def filter_input(func_or_str):

    def __filter(string):
        return "".join(re.findall("[\w\-+]*", string))

    def wrapped(*args, **kwargs):
        _args = []
        for arg in args:
            if isinstance(arg, str) or isinstance(arg, unicode):
                arg = __filter(arg)
            elif isinstance(arg, list):
                arg =  [__filter(item) for item in arg]
            elif isinstance(arg, tuple):
                arg =  (__filter(item) for item in arg)
            elif isinstance(arg, dict):
                arg =  {item: __filter(arg[item]) for item in arg.keys()}
            _args.append(arg)
        for arg in kwargs:
            if type(kwargs[arg]) in (unicode, str):
                kwargs[arg] = __filter(kwargs[arg])
            if isinstance(kwargs[arg], str) or isinstance(kwargs[arg], unicode):
                kwargs[arg] = __filter(kwargs[arg])
            elif isinstance(kwargs[arg], list):
                kwargs[arg] =  [__filter(item) for item in kwargs[arg]]
            elif isinstance(kwargs[arg], tuple):
                kwargs[arg] =  (__filter(item) for item in kwargs[arg])
            elif isinstance(kwargs[arg], dict):
                kwargs[arg] =  {item: __filter(kwargs[arg][item]) for item in kwargs[arg].keys()}
        return func_or_str(*_args, **kwargs)

    if isinstance(func_or_str, str) or isinstance(func_or_str, unicode):
        return __filter(func_or_str)
    if isinstance(func_or_str, list):
        return [__filter(item) for item in func_or_str]
    if isinstance(func_or_str, tuple):
        return (__filter(item) for item in func_or_str)
    if isinstance(func_or_str, dict):
        return {item: __filter(func_or_str[item]) for item in func_or_str.keys()}
    if isinstance(func_or_str, types.FunctionType):
        return wrapped
    return None


def enforce(action_names, object_name, **extra):
    _action_name_list = action_names

    def wrap(func):
        def wrapped(*args):
            # global actions
            self = args[0]
            user_name = args[1]
            intra_extension_id = args[2]
            if intra_extension_id not in self.admin_api.get_intra_extensions(DEFAULT_USER):
                raise IntraExtensionUnknown()

            tenants_dict = self.tenant_api.get_tenants_dict(DEFAULT_USER)
            intra_admin_extension_id = None
            tenant_name = None
            for tenant_id in tenants_dict:
                if tenants_dict[tenant_id]['intra_authz_extension_id'] is intra_extension_id:
                    intra_admin_extension_id = tenants_dict[tenant_id]['intra_admin_extension_id']
                    tenant_name = tenants_dict[tenant_id]['name']

            if not intra_admin_extension_id:
                args[0].moonlog_api.warning("No admin IntraExtension found, authorization granted by default.")
                return func(*args)
            else:
                authz_result = False
                if type(_action_name_list) in (str, unicode):
                    action_name_list = (_action_name_list, )
                else:
                    action_name_list = _action_name_list
                for action_name in action_name_list:
                    if self.authz_api.authz(tenant_name, user_name, object_name, action_name, 'admin'):
                        authz_result = True
                    else:
                        authz_result = False
                        break
                if authz_result:
                    return func(*args)
        return wrapped
    return wrap


@dependency.provider('configuration_api')
@dependency.requires('moonlog_api')
class ConfigurationManager(manager.Manager):

    def __init__(self):
        super(ConfigurationManager, self).__init__(CONF.moon.configuration_driver)

    def get_policy_template_dict(self, user_id):
        """
        Return a dictionary of all policy templates
        :return: {template_id: {name: temp_name, description: template_description}, ...}
        """
        # TODO: check user right with user_id in SuperExtension
        return self.driver.get_policy_template_dict()

    def get_policy_template_id_from_name(self, user_id, policy_template_name):
        # TODO: check user right with user_id in SuperExtension
        policy_template_dict = self.driver.get_policy_template_dict()
        for policy_template_id in policy_template_dict:
            if policy_template_dict[policy_template_id]['name'] is policy_template_name:
                return policy_template_id
        return None

    def get_aggregation_algorithm_dict(self, user_id):
        """
        Return a dictionary of all aggregation algorithm
        :return: {aggre_algo_id: {name: aggre_name, description: aggre_algo_description}, ...}
        """
        # TODO: check user right with user_id in SuperExtension
        return self.driver.get_aggregation_algorithm_dict()

    def get_aggregation_algorithm_id_from_name(self, user_id, aggregation_algorithm_name):
        # TODO: check user right with user_id in SuperExtension
        aggregation_algorithm_dict = self.driver.get_aggregation_algorithm_dict()
        for aggregation_algorithm_id in aggregation_algorithm_dict:
            if aggregation_algorithm_dict[aggregation_algorithm_id]['name'] is aggregation_algorithm_name:
                return aggregation_algorithm_id
        return None

    def get_sub_meta_rule_algorithm_dict(self, user_id):
        """
        Return a dictionary of sub_meta_rule algorithm
        :return: {sub_meta_rule_id: {name: sub_meta_rule_name, description: sub_meta_rule_description}, }
        """
        # TODO: check user right with user_id in SuperExtension
        return self.driver.get_sub_meta_rule_algorithm_dict()

    def get_sub_meta_rule_algorithm_id_from_name(self, sub_meta_rule_algorithm_name):
        # TODO: check user right with user_id in SuperExtension
        sub_meta_rule_algorithm_dict = self.driver.get_sub_meta_rule_algorithm_dict()
        for sub_meta_rule_algorithm_id in sub_meta_rule_algorithm_dict:
            if sub_meta_rule_algorithm_dict[sub_meta_rule_algorithm_id]['name'] is sub_meta_rule_algorithm_name:
                return sub_meta_rule_algorithm_id
        return None


@dependency.provider('tenant_api')
@dependency.requires('moonlog_api')
class TenantManager(manager.Manager):

    def __init__(self):
        super(TenantManager, self).__init__(CONF.moon.tenant_driver)

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
        # TODO: check user right with user_id in SuperExtension
        return self.driver.get_tenants_dict()

    def add_tenant_dict(self, user_id, tenant_dict):
        # TODO: check user right with user_id in SuperExtension
        tenants_dict = self.driver.get_tenants_dict()
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]['name'] is tenant_dict['name']:
                raise TenantAddedNameExisting()
        return self.driver.add_tenant_dict(uuid4().hex, tenant_dict)

    def get_tenant_dict(self, user_id, tenant_id):
        # TODO: check user right with user_id in SuperExtension
        tenants_dict = self.driver.get_tenants_dict()
        if tenant_id not in tenants_dict:
            raise TenantUnknown()
        return tenants_dict[tenant_id]

    def del_tenant(self, user_id, tenant_id):
        # TODO: check user right with user_id in SuperExtension
        if tenant_id not in self.driver.get_tenants_dict():
            raise TenantUnknown()
        self.driver.del_tenant(tenant_id)

    def set_tenant_dict(self, user_id, tenant_id, tenant_dict):
        # TODO: check user right with user_id in SuperExtension
        if tenant_id not in self.driver.get_tenants_dict():
            raise TenantUnknown()
        return self.driver.set_tenant_dict(tenant_id, tenant_dict)

    def get_tenant_name_from_id(self, user_id, tenant_id):
        # TODO: check user right with user_id in SuperExtension
        tenant_dict = self.driver.get_tenants_dict()
        if tenant_id not in tenant_dict:
            raise TenantUnknown()
        return tenant_dict[tenant_id]["name"]

    def set_tenant_name(self, user_id, tenant_id, tenant_name):
        # TODO: check user right with user_id in SuperExtension
        tenant_dict = self.driver.get_tenants_dict()
        if tenant_id not in tenant_dict:
            raise TenantUnknown()
        return self.driver.set_tenant(
            tenant_id,
            tenant_name,
            tenant_dict[tenant_id]['intra_authz_ext_id'],
            tenant_dict[tenant_id]['intra_admin_ext_id']
        )

    def get_tenant_id_from_name(self, user_id, tenant_name):
        # TODO: check user right with user_id in SuperExtension
        tenants_dict = self.driver.get_tenants_dict()
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]["name"] is tenant_name:
                return tenant_id
        return None

    def get_tenant_intra_extension_id(self, user_id, tenant_id, genre="authz"):
        """
        Return the UUID of the scoped extension for a particular tenant.
        :param tenant_id: UUID of the tenant
        :param genre: "admin" or "authz"
        :return (str): the UUID of the scoped extension
        """
        # 1 tenant only with 1 authz extension and 1 admin extension
        # TODO: check user right with user_id in SuperExtension
        tenant_dict = self.driver.get_tenants_dict()
        if tenant_id not in tenant_dict:
            raise TenantUnknown()
        elif not tenant_dict[tenant_id][genre]:
            raise TenantNoIntraExtension()
        return tenant_dict[tenant_id][genre]


@dependency.requires('identity_api', 'tenant_api', 'configuration_api', 'authz_api', 'admin_api', 'moonlog_api')
class IntraExtensionManager(manager.Manager):

    def __init__(self):
        self.__genre__ = None
        driver = CONF.moon.intraextension_driver
        super(IntraExtensionManager, self).__init__(driver)

    def __get_authz_buffer(self, intra_extension_id, subject_id, object_id, action_id):
        """
        :param intra_extension_id:
        :param subject_id:
        :param object_id:
        :param action_id:
        :return: authz_buffer = {
            'subject_uuid': xxx,
            'object_uuid': yyy,
            'action_uuid': zzz,
            'subject_assignments': {
                'subject_category1': [],
                'subject_category2': [],
                ...
                'subject_categoryn': []
            },
            'object_assignments': {},
            'action_assignments': {},
        }
        """
        authz_buffer = dict()
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
                intra_extension_id, subject_id)[category]
        object_assignment_dict = dict()
        for category in meta_data_dict["object_categories"]:
            object_assignment_dict[category] = self.driver.get_object_assignment_list(
                intra_extension_id, object_id)[category]
        action_assignment_dict = dict()
        for category in meta_data_dict["action_categories"]:
            action_assignment_dict[category] = self.driver.get_action_assignment_list(
                intra_extension_id, action_id)[category]
        authz_buffer['subject_attributes'] = dict()
        authz_buffer['object_attributes'] = dict()
        authz_buffer['action_attributes'] = dict()
        for _subject_category in meta_data_dict['subject_categories']:
            authz_buffer['subject_assignments'][_subject_category] = subject_assignment_dict[_subject_category]
        for _object_category in meta_data_dict['object_categories']:
            authz_buffer['object_assignments'][_object_category] = object_assignment_dict[_object_category]
        for _action_category in meta_data_dict['action_categories']:
            authz_buffer['action_assignments'][_action_category] = action_assignment_dict[_action_category]
        return authz_buffer

    def authz(self, intra_extension_id, subject_id, object_id, action_id):
        """Check authorization for a particular action.

        :param intra_extension_id: UUID of an IntraExtension
        :param subject_id: subject UUID of the request
        :param object_id: object UUID of the request
        :param action_id: action UUID of the request
        :return: True or False or raise an exception
        :raises: (in that order)
            IntraExtensionNotFound
            SubjectUnknown
            ObjectUnknown
            ActionUnknown
            SubjectCategoryAssignmentUnknown
            ObjectCategoryAssignmentUnknown
            ActionCategoryAssignmentUnknown
        """
        authz_buffer = self.__get_authz_buffer(intra_extension_id, subject_id, object_id, action_id)
        decision_buffer = dict()

        meta_rule_dict = self.driver.get_sub_meta_rules_dict(intra_extension_id)

        for sub_meta_rule_id in meta_rule_dict['sub_meta_rules']:
            if meta_rule_dict['sub_meta_rules'][sub_meta_rule_id]['algorithm'] == 'inclusion':
                decision_buffer[sub_meta_rule_id] = inclusion(
                    authz_buffer,
                    meta_rule_dict['sub_meta_rules'][sub_meta_rule_id],
                    self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id).values())
            elif meta_rule_dict['sub_meta_rules'][sub_meta_rule_id]['algorithm'] == 'comparison':
                decision_buffer[sub_meta_rule_id] = comparison(
                    authz_buffer,
                    meta_rule_dict['sub_meta_rules'][sub_meta_rule_id],
                    self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id).values())

        if meta_rule_dict['aggregation'] == 'all_true':
            return all_true(decision_buffer)

        return False

    def get_intra_extensions_dict(self, user_id):
        """
        :param user_id:
        :return: {
            intra_extension_id1: {
                name: xxx,
                model: yyy,
                description: zzz}
            },
            intra_extension_id2: {...},
            ...}
        """
        # TODO: check will be done through super_extension later
        return self.driver.get_intra_extensions_dict()

    # load policy from policy directory
    # TODO (dthom) re-check these funcs

    def __load_metadata_file(self, intra_extension_dict, policy_dir):

        metadata_path = os.path.join(policy_dir, 'metadata.json')
        f = open(metadata_path)
        json_perimeter = json.load(f)

        # subject_categories_dict = dict()
        for _cat in json_perimeter['subject_categories']:
            self.driver.set_subject_category_dict(intra_extension_dict["id"], uuid4().hex,
                                                  {"name": _cat, "description": _cat})
        # Initialize scope categories
        # for _cat in subject_categories_dict.keys():
        #     self.driver.set_subject_scope_dict(intra_extension_dict["id"], _cat, {})
        # intra_extension_dict['subject_categories'] = subject_categories_dict

        # object_categories_dict = dict()
        for _cat in json_perimeter['object_categories']:
            self.driver.set_object_category_dict(intra_extension_dict["id"], uuid4().hex,
                                                 {"name": _cat, "description": _cat})
        # Initialize scope categories
        # for _cat in object_categories_dict.keys():
        #     self.driver.set_object_scope_dict(intra_extension_dict["id"], _cat, {})
        # intra_extension_dict['object_categories'] = object_categories_dict

        # action_categories_dict = dict()
        for _cat in json_perimeter['action_categories']:
            self.driver.set_action_category_dict(intra_extension_dict["id"], uuid4().hex,
                                                 {"name": _cat, "description": _cat})
        # Initialize scope categories
        # for _cat in action_categories_dict.keys():
        #     self.driver.set_action_scope_dict(intra_extension_dict["id"], _cat, {})
        # intra_extension_dict['action_categories'] = action_categories_dict

    def __load_perimeter_file(self, intra_extension_dict, policy_dir):

        perimeter_path = os.path.join(policy_dir, 'perimeter.json')
        f = open(perimeter_path)
        json_perimeter = json.load(f)

        subject_dict = dict()
        # We suppose that all subjects can be mapped to a true user in Keystone
        for _subject in json_perimeter['subjects']:
            user = self.identity_api.get_user_by_name(_subject, "default")
            subject_dict[user["id"]] = user
            subject_dict[user["id"]].pop("id")
            self.driver.set_subject_dict(intra_extension_dict["id"], user["id"])
        intra_extension_dict["subjects"] = subject_dict

        # Copy all values for objects and actions
        object_dict = dict()
        for _object in json_perimeter['objects']:
            _id = uuid4().hex
            object_dict[_id] = {"name": _object, "description": _object}
            self.driver.set_object_dict(intra_extension_dict["id"], _id, object_dict[_id])
        intra_extension_dict["objects"] = object_dict

        action_dict = dict()
        for _action in json_perimeter['actions']:
            _id = uuid4().hex
            action_dict[_id] = {"name": _action, "description": _action}
            self.driver.set_action_dict(intra_extension_dict["id"], _id, action_dict[_id])
        intra_extension_dict["ations"] = action_dict

    def __load_scope_file(self, intra_extension_dict, policy_dir):

        metadata_path = os.path.join(policy_dir, 'scope.json')
        f = open(metadata_path)
        json_perimeter = json.load(f)

        intra_extension_dict['subject_category_scope'] = dict()
        for category, scope in json_perimeter["subject_category_scope"].iteritems():
            category_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], category, self.driver.SUBJECT_CATEGORY)
            _scope_dict = dict()
            for _scope in scope:
                _id = uuid4().hex
                _scope_dict[_id] = {"name": _scope, "description": _scope}
                self.driver.set_subject_scope_dict(intra_extension_dict["id"], category_id, _id, _scope_dict[_id])
            intra_extension_dict['subject_category_scope'][category] = _scope_dict

        intra_extension_dict['object_category_scope'] = dict()
        for category, scope in json_perimeter["object_category_scope"].iteritems():
            category_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], category, self.driver.OBJECT_CATEGORY)
            _scope_dict = dict()
            for _scope in scope:
                _id = uuid4().hex
                _scope_dict[_id] = {"name": _scope, "description": _scope}
                self.driver.set_object_scope_dict(intra_extension_dict["id"], category_id, _id, _scope_dict[_id])
            intra_extension_dict['object_category_scope'][category] = _scope_dict

        intra_extension_dict['action_category_scope'] = dict()
        for category, scope in json_perimeter["action_category_scope"].iteritems():
            category_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], category, self.driver.ACTION_CATEGORY)
            _scope_dict = dict()
            for _scope in scope:
                _id = uuid4().hex
                _scope_dict[_id] = {"name": _scope, "description": _scope}
                self.driver.set_action_scope_dict(intra_extension_dict["id"], category_id, _scope_dict[_id])
            intra_extension_dict['action_category_scope'][category] = _scope_dict

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
                if category_id not in object_assignments[object_name]:
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
                if category_id not in action_assignments[action_name]:
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
        # ie["meta_rules"] = copy.deepcopy(json_metarule)
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
                    metarule[[_id]][item].append(self.driver.get_uuid_from_name(intra_extension_dict["id"], element, categories[item]))
            metarule[[_id]]["algorithm"] = json_metarule["sub_meta_rules"][metarule_name]["algorithm"]
            self.driver.set_sub_meta_rule_dict(intra_extension_dict["id"], _id, metarule[[_id]])
        submetarules = {
            "aggregation": json_metarule["aggregation"],
            "sub_meta_rules": metarule
        }
        self.driver.set_aggregation_algorithm(intra_extension_dict["id"], uuid4().hex,
                                              {
                                                  "name": json_metarule["aggregation"],
                                                  "description": json_metarule["aggregation"],
                                              })

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
            # print(sub_rule_name)
            # print(self.get_sub_meta_rule_relations("admin", ie["id"]))
            # if sub_rule_name not in self.get_sub_meta_rule_relations("admin", ie["id"])["sub_meta_rule_relations"]:
            #     raise IntraExtensionException("Bad sub_rule_name name {} in rules".format(sub_rule_name))
            rules[sub_rule_id] = list()
            for rule in json_rules[sub_rule_name]:
                subrule = list()
                _rule = list(rule)
                for category_uuid in sub_meta_rules["rule"][sub_rule_name]["subject_categories"]:
                    scope_name = _rule.pop(0)
                    scope_uuid = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                                scope_name,
                                                                self.driver.SUBJECT_SCOPE,
                                                                category_uuid=category_uuid)
                    subrule.append(scope_uuid)
                for category_uuid in sub_meta_rules["rule"][sub_rule_name]["action_categories"]:
                    scope_name = _rule.pop(0)
                    scope_uuid = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                                scope_name,
                                                                self.driver.ACTION_SCOPE,
                                                                category_uuid=category_uuid)
                    subrule.append(scope_uuid)
                for category_uuid in sub_meta_rules["rule"][sub_rule_name]["object_categories"]:
                    scope_name = _rule.pop(0)
                    scope_uuid = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                                scope_name,
                                                                self.driver.OBJECT_SCOPE,
                                                                category_uuid=category_uuid)
                    subrule.append(scope_uuid)
                # if a positive/negative value exists, all item of rule have not be consumed
                if len(rule) >= 1 and type(rule[0]) is bool:
                    subrule.append(rule[0])
                else:
                    # if value doesn't exist add a default value
                    subrule.append(True)
                rules[sub_rule_id].append(subrule)
            self.driver.set_rule_dict(intra_extension_dict["id"], sub_rule_id, uuid4().hex, rules)

    def load_intra_extension_dict(self, user_id, intra_extension_dict):
        # TODO: check will be done through super_extension later
        ie_dict = dict()
        # TODO: clean some values
        ie_dict['id'] = uuid4().hex
        ie_dict["name"] = filter_input(intra_extension_dict["name"])
        ie_dict["model"] = filter_input(intra_extension_dict["policymodel"])
        ie_dict["description"] = filter_input(intra_extension_dict["description"])
        ref = self.driver.set_intra_extension_dict(ie_dict['id'], ie_dict)
        self.moonlog_api.debug("Creation of IE: {}".format(ref))
        # read the profile given by "policymodel" and populate default variables
        policy_dir = os.path.join(CONF.moon.policy_directory, ie_dict["model"])
        self.__load_metadata_file(ie_dict, policy_dir)
        self.__load_perimeter_file(ie_dict, policy_dir)
        self.__load_scope_file(ie_dict, policy_dir)
        self.__load_assignment_file(ie_dict, policy_dir)
        self.__load_metarule_file(ie_dict, policy_dir)
        self.__load_rule_file(ie_dict, policy_dir)
        return ref

    def get_intra_extension_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :return: {intra_extension_id: intra_extension_name, ...}
        """
        # TODO: check will be done through super_extension later
        if intra_extension_id not in self.driver.get_intra_extensions_dict():
            raise IntraExtensionUnknown()
        return self.driver.get_intra_extensions_dict()[intra_extension_id]

    def del_intra_extension(self, user_id, intra_extension_id):
        # TODO: check will be done through super_extension later
        if intra_extension_id not in self.driver.get_intra_extensions_dict():
            raise IntraExtensionUnknown()
        return self.driver.del_intra_extension(intra_extension_id)

    def set_intra_extension_dict(self, user_id, intra_extension_id, intra_extension_dict):
        # TODO: check will be done through super_extension later
        if intra_extension_id not in self.driver.get_intra_extensions_dict():
            raise IntraExtensionUnknown()
        return self.driver.set_intra_extension_dict(intra_extension_id, intra_extension_dict)

    # Metadata functions

    @filter_input  # TODO: check for each function if intra_entension_id exists
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
    def add_subject_category(self, user_id, intra_extension_id, subject_category_dict):
        subject_category_dict = self.driver.get_subject_categories_dict(intra_extension_id)
        for subject_category_id in subject_category_dict:
            if subject_category_dict[subject_category_id]['name'] is subject_category_dict['name']:
                raise SubjectCategoryNameExisting()
        return self.driver.set_subject_category(intra_extension_id, uuid4().hex, subject_category_dict)

    @filter_input
    @enforce("read", "subject_categories")
    def get_subject_category(self, user_id, intra_extension_id, subject_category_id):
        subject_category_dict = self.driver.get_subject_categories_dict(intra_extension_id)
        if subject_category_id not in subject_category_dict:
            raise SubjectCategoryUnknown()
        return subject_category_dict[subject_category_id]

    @filter_input
    @enforce(("read", "write"), "subject_categories")
    @enforce(("read", "write"), "subject_scopes")
    @enforce(("read", "write"), "subject_assignments")
    def del_subject_category(self, user_id, intra_extension_id, subject_category_id):
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        # Destroy scopes related to this category
        for scope in self.driver.get_subject_scope_dict(intra_extension_id, subject_category_id):
            self.del_subject_scope(intra_extension_id, subject_category_id, scope)
        # Destroy assignments related to this category
        for subject_id in self.driver.get_subjects_dict(intra_extension_id):
            for assignment_id in self.driver.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id):
                self.driver.del_subject_assignment(intra_extension_id, subject_id, subject_category_id, assignment_id)
        self.driver.del_subject_category(intra_extension_id, subject_category_id)

    @filter_input
    @enforce(("read", "write"), "subject_categories")
    def set_subject_category(self, user_id, intra_extension_id, subject_category_id, subject_category_dict):
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        return self.driver.set_subject_category(intra_extension_id, subject_category_id, subject_category_dict)

    @filter_input
    @enforce("read", "object_categories")
    def get_object_category_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :param intra_extension_id:
        :return:
        """
        return self.driver.get_object_categories_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "object_categories")
    @enforce(("read", "write"), "object_scopes")
    def add_object_category(self, user_id, intra_extension_id, object_category_name):
        object_category_dict = self.driver.get_object_categories_dict(intra_extension_id)
        for object_category_id in object_category_dict:
            if object_category_dict[object_category_id]["name"] is object_category_name:
                raise ObjectCategoryNameExisting()
        return self.driver.add_object_category(intra_extension_id, uuid4().hex, object_category_name)

    @filter_input
    @enforce("read", "object_categories")
    def get_object_category(self, user_id, intra_extension_id, object_category_id):
        object_category_dict = self.driver.get_object_categories_dict(intra_extension_id)
        if object_category_id not in object_category_dict:
            raise ObjectCategoryUnknown()
        return object_category_dict[object_category_id]

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
    @enforce("read", "action_categories")
    def get_action_category_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :param intra_extension_id:
        :return:
        """
        return self.driver.get_action_categories_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "action_categories")
    @enforce(("read", "write"), "action_scopes")
    def add_action_category(self, user_id, intra_extension_id, action_category_name):
        action_category_dict = self.driver.get_action_categories_dict(intra_extension_id)
        for action_category_id in action_category_dict:
            if action_category_dict[action_category_id]['name'] is action_category_name:
                raise ActionCategoryNameExisting()
        return self.driver.add_action_category(intra_extension_id, uuid4().hex, action_category_name)

    @filter_input
    @enforce("read", "action_categories")
    def get_action_category(self, user_id, intra_extension_id, action_category_id):
        action_category_dict = self.driver.get_action_categories_dict(intra_extension_id)
        if action_category_id not in action_category_dict:
            raise ActionCategoryUnknown()
        return self.driver.get_action_categories_dict(intra_extension_id)[action_category_id]

    @filter_input
    @enforce(("read", "write"), "action_categories")
    @enforce(("read", "write"), "action_category_scopes")
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
            if subjects_dict[subject_id]["name"] is subject_dict['name']:
                raise SubjectNameExisting()
        # Next line will raise an error if user is not present in Keystone database
        subject_item_dict = self.identity_api.get_user_by_name(subject_dict['name'], "default")
        return self.driver.set_subject_dict(intra_extension_id, subject_item_dict["id"], subject_dict)

    @filter_input
    @enforce("read", "subjects")
    def get_subject_dict(self, user_id, intra_extension_id, subject_id):
        subject_dict = self.driver.get_subjects_dict(intra_extension_id)
        if subject_id in subject_dict:
            raise SubjectUnknown()
        return subject_dict[subject_id]

    @filter_input
    @enforce(("read", "write"), "subjects")
    def del_subject(self, user_id, intra_extension_id, subject_id):
        if subject_id in self.driver.get_subjects_dict(intra_extension_id):
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
            if subjects_dict[subject_id]["name"] is subject_dict['name']:
                raise SubjectNameExisting()
        # Next line will raise an error if user is not present in Keystone database
        subject_item_dict = self.identity_api.get_user_by_name(subject_dict['name'], "default")
        return self.driver.set_subject_dict(intra_extension_id, subject_item_dict["id"], subject_dict)

    @filter_input
    @enforce("read", "objects")
    def get_objects_dict(self, user_id, intra_extension_id):
        return self.driver.get_objects_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "objects")
    def add_object_dict(self, user_id, intra_extension_id, object_name):
        object_dict = self.driver.get_objects_dict(intra_extension_id)
        for object_id in object_dict:
            if object_dict[object_id]["name"] is object_name:
                raise ObjectNameExisting()
        return self.driver.set_object_dict(intra_extension_id, uuid4().hex, object_name)

    @filter_input
    @enforce(("read", "write"), "objects")
    def set_object_dict(self, user_id, intra_extension_id, object_id, object_dict):
        objects_dict = self.driver.get_objects_dict(intra_extension_id)
        for object_id in objects_dict:
            if objects_dict[object_id]["name"] is object_dict['name']:
                raise ObjectNameExisting()
        return self.driver.set_object_dict(intra_extension_id, object_id, object_dict)

    @filter_input
    @enforce("read", "objects")
    def get_object_dict(self, user_id, intra_extension_id, object_id):
        object_dict = self.driver.get_objects_dict(intra_extension_id)
        if object_id in object_dict:
            raise ObjectUnknown()
        return object_dict[object_id]

    @filter_input
    @enforce(("read", "write"), "objects")
    def del_object(self, user_id, intra_extension_id, object_id):
        if object_id in self.driver.get_objects_dict(intra_extension_id):
            raise ObjectUnknown()
        # Destroy assignments related to this category
        for object_category_id in self.driver.get_object_categories_dict(intra_extension_id):
            for _object_id in self.driver.get_objects_dict(intra_extension_id):
                for assignment_id in self.driver.get_object_assignment_list(intra_extension_id, _object_id, object_category_id):
                    self.driver.del_object_assignment(intra_extension_id, _object_id, object_category_id, assignment_id)
        self.driver.del_object(intra_extension_id, object_id)

    @filter_input
    @enforce("read", "actions")
    def get_actions_dict(self, user_id, intra_extension_id):
        return self.driver.get_actions_dict(intra_extension_id)

    @filter_input
    @enforce(("read", "write"), "actions")
    def add_action_dict(self, user_id, intra_extension_id, action_name):
        action_dict = self.driver.get_actions_dict(intra_extension_id)
        for action_id in action_dict:
            if action_dict[action_id]["name"] is action_name:
                raise ActionNameExisting()
        return self.driver.add_action_dict(intra_extension_id, uuid4().hex, action_name)

    @filter_input
    @enforce(("read", "write"), "actions")
    def set_action_dict(self, user_id, intra_extension_id, action_id, action_dict):
        actions_dict = self.driver.get_actions_dict(intra_extension_id)
        for action_id in actions_dict:
            if actions_dict[action_id]["name"] is action_dict['name']:
                raise ActionNameExisting()
        return self.driver.set_action_dict(intra_extension_id, action_id, action_dict)

    @filter_input
    @enforce("read", "actions")
    def get_action_dict(self, user_id, intra_extension_id, action_id):
        action_dict = self.driver.get_actions_dict(intra_extension_id)
        if action_id in action_dict:
            raise ActionUnknown()
        return action_dict[action_id]

    @filter_input
    @enforce(("read", "write"), "actions")
    def del_action(self, user_id, intra_extension_id, action_id):
        if action_id in self.driver.get_actions_dict(intra_extension_id):
            raise ActionUnknown()
        # Destroy assignments related to this category
        for action_category_id in self.driver.get_action_categories_dict(intra_extension_id):
            for _action_id in self.driver.get_actions_dict(intra_extension_id):
                for assignment_id in self.driver.get_action_assignment_list(intra_extension_id, _action_id, action_category_id):
                    self.driver.del_action_assignment(intra_extension_id, _action_id, action_category_id, assignment_id)
        return self.driver.del_action(intra_extension_id, action_id)

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
            if subject_scope_dict['name'] is subject_scopes_dict[_subject_scope_id]['name']:
                raise SubjectScopeNameExisting()
        subject_scope_id = uuid4().hex
        return self.driver.add_subject_scope_dict(intra_extension_id, subject_category_id, subject_scope_id, subject_scope_dict)

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
        return self.driver.del_subject_scope(intra_extension_id, subject_category_id, subject_scope_id)

    @filter_input
    @enforce(("read", "write"), "subject_scopes")
    @enforce("read", "subject_categories")
    def set_subject_scope_dict(self, user_id, intra_extension_id, subject_category_id, subject_scope_id, subject_scope_name):
        if subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        subject_scope_dict = self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id)
        for _subject_scope_id in subject_scope_dict:
            if subject_scope_name is subject_scope_dict[_subject_scope_id]['name']:
                raise SubjectScopeNameExisting()
        return self.driver.set_subject_scope_dict(intra_extension_id, subject_category_id, uuid4().hex, subject_scope_dict)

    @filter_input
    @enforce("read", "object_category_scopes")
    @enforce("read", "object_categories")
    def get_object_scopes_dict(self, user_id, intra_extension_id, object_category_id):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        return self.driver.get_object_scopes_dict(intra_extension_id, object_category_id)

    @filter_input
    @enforce(("read", "write"), "object_scopes")
    @enforce("read", "object_categories")
    def add_object_scope_dict(self, user_id, intra_extension_id, object_category_id, object_scope_name):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        object_scope_dict = self.driver.get_object_scopes_dict(intra_extension_id, object_category_id)
        for _object_scope_id in object_scope_dict:
            if object_scope_name is object_scope_dict[_object_scope_id]['name']:
                raise ObjectScopeNameExisting()
        object_scope_id = uuid4().hex
        return self.driver.add_subject_scope_dict(
            intra_extension_id,
            object_category_id,
            object_scope_id,
            object_scope_name)

    @filter_input
    @enforce("read", "object_scopes")
    @enforce("read", "object_categories")
    def get_object_scope_dict(self, user_id, intra_extension_id, object_category_id, object_scope_id):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        object_scopte_dict = self.driver.get_object_scopes_dict(intra_extension_id, object_category_id)
        if object_scope_id not in object_scopte_dict:
            raise ObjectScopeUnknown()
        return object_scopte_dict[object_scope_id]

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
        return self.driver.del_object_scope(intra_extension_id, object_category_id, object_scope_id)

    @filter_input
    @enforce(("read", "write"), "object_scopes")
    @enforce("read", "object_categories")
    def set_object_scope_dict(self, user_id, intra_extension_id, object_category_id, object_scope_id, object_scope_name):
        if object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        object_scope_dict = self.driver.get_object_scopes_dict(intra_extension_id, object_category_id)
        for _object_scope_id in object_scope_dict:
            if object_scope_name is object_scope_dict[_object_scope_id]['name']:
                raise ObjectScopeNameExisting()
        return self.driver.set_object_scope_dict(intra_extension_id, object_category_id, uuid4().hex, object_scope_dict)

    @filter_input
    @enforce("read", "action_category_scopes")
    @enforce("read", "action_categories")
    def get_action_scopes_dict(self, user_id, intra_extension_id, action_category_id):
        if action_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        return self.driver.get_action_scopes_dict(intra_extension_id, action_category_id)

    @filter_input
    @enforce(("read", "write"), "action_scopes")
    @enforce("read", "action_categories")
    def add_action_scope_dict(self, user_id, intra_extension_id, action_category_id, action_scope_name):
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        action_scope_dict = self.driver.get_action_scopes_dict(intra_extension_id, action_category_id)
        for _action_scope_id in action_scope_dict:
            if action_scope_name is action_scope_dict[_action_scope_id]['name']:
                raise ActionScopeNameExisting()
        action_scope_id = uuid4().hex
        return self.driver.add_action_scope_dict(
            intra_extension_id,
            action_category_id,
            action_scope_id,
            action_scope_name)

    @filter_input
    @enforce("read", "action_scopes")
    @enforce("read", "action_categories")
    def get_action_scope_dict(self, user_id, intra_extension_id, action_category_id, action_scope_id):
        if action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        action_scopte_dict = self.driver.get_action_scopes_dict(intra_extension_id, action_category_id)
        if action_scope_id not in action_scopte_dict:
            raise ActionScopeUnknown()
        return action_scopte_dict[action_scope_id]

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
        return self.driver.del_action_scope(intra_extension_id, action_category_id, action_scope_id)

    # Assignment functions

    @filter_input
    @enforce("read", "subject_assignments")
    @enforce("read", "subjects")
    @enforce("read", "subject_categories")
    def get_subject_assignment_list(self, user_id, intra_extension_id, subject_id, subject_category_id):
        if subject_id not in self.driver.get_subjects_dict(user_id, intra_extension_id):
            raise SubjectUnknown()
        elif subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
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
        if subject_scope_id in self.driver.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id):
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
        elif subject_category_id not in self.driver.get_subject_categories_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        elif subject_scope_id not in self.driver.get_subject_scopes_dict(intra_extension_id, subject_category_id):
            raise SubjectScopeUnknown()
        elif subject_scope_id not in self.driver.get_subject_assignment_list(intra_extension_id, subject_id)[subject_category_id]:
            raise SubjectAssignmentUnknown()
        self.driver.del_subject_category_assignment(intra_extension_id, subject_id, subject_category_id, subject_scope_id)

    @filter_input
    @enforce("read", "object_assignments")
    @enforce("read", "objects")
    @enforce("read", "object_categories")
    def get_object_assignment_list(self, user_id, intra_extension_id, object_id, object_category_id):
        if object_id not in self.driver.get_objects_dict(user_id, intra_extension_id):
            raise ObjectUnknown()
        elif object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        return self.driver.get_object_assignment_list(intra_extension_id, object_id, object_category_id)

    @filter_input
    @enforce(("read", "write"), "object_assignments")
    @enforce("read", "objects")
    @enforce("read", "object_categories")
    def add_object_assignment_list(self, user_id, intra_extension_id, object_id, object_category_id, object_scope_id):
        if object_id not in self.driver.get_objects_dict(intra_extension_id):
            raise ObjectUnknown()
        elif object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        elif object_scope_id not in self.driver.get_object_scopes_dict(intra_extension_id, object_category_id):
            raise ObjectScopeUnknown()
        elif object_scope_id in self.driver.get_object_assignment_list(intra_extension_id, object_id)[object_category_id]:
            raise ObjectAssignmentExisting()
        return self.driver.add_object_assignment_list(intra_extension_id, object_id, object_category_id, object_scope_id)

    @filter_input
    @enforce(("read", "write"), "object_assignments")
    @enforce("read", "objects")
    @enforce("read", "object_categories")
    @enforce("read", "object_scopes")
    def del_object_assignment(self, user_id, intra_extension_id, object_id, object_category_id, object_scope_id):
        if object_id not in self.driver.get_objects_dict(intra_extension_id):
            raise ObjectUnknown()
        elif object_category_id not in self.driver.get_object_categories_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        elif object_scope_id not in self.driver.get_object_scopes_dict(intra_extension_id, object_category_id):
            raise ObjectScopeUnknown()
        elif object_scope_id not in self.driver.get_subject_assignment_list(intra_extension_id, object_id)[object_category_id]:
            raise ObjectAssignmentUnknown()
        return self.driver.del_object_assignment(intra_extension_id, object_id, object_category_id, object_scope_id)

    @filter_input
    @enforce("read", "action_assignments")
    @enforce("read", "actions")
    @enforce("read", "action_categories")
    def get_action_assignment_list(self, user_id, intra_extension_id, action_id, action_category_id):
        if action_id not in self.driver.get_actions_dict(user_id, intra_extension_id):
            raise ActionUnknown()
        elif action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        return self.driver.get_action_assignment_list(intra_extension_id, action_id, action_category_id)

    @filter_input
    @enforce(("read", "write"), "action_assignments")
    @enforce("read", "actions")
    @enforce("read", "action_categories")
    def add_action_assignment_list(self, user_id, intra_extension_id, action_id, action_category_id, action_scope_id):
        if action_id not in self.driver.get_actions_dict(intra_extension_id):
            raise ActionUnknown()
        elif action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        elif action_scope_id not in self.driver.get_action_scopes_dict(intra_extension_id, action_category_id):
            raise ActionScopeUnknown()
        elif action_scope_id in self.driver.get_action_assignment_list(intra_extension_id, action_id)[action_category_id]:
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
        elif action_category_id not in self.driver.get_action_categories_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        elif action_scope_id not in self.driver.get_action_scopes_dict(intra_extension_id, action_category_id):
            raise ActionScopeUnknown()
        elif action_scope_id not in self.driver.get_action_assignment_list(intra_extension_id, action_id)[action_category_id]:
            raise ActionAssignmentUnknown()
        return self.driver.del_action_assignment(intra_extension_id, action_id, action_category_id, action_scope_id)

    # Metarule functions

    @filter_input
    @enforce(("read", "write"), "aggregation_algorithm")
    def set_aggregation_algorithm_dict(self, user_id, intra_extension_id, aggregation_algorithm_id, aggregation_algorithm_dict):
        if aggregation_algorithm_id:
            if aggregation_algorithm_id not in self.configuration_api.get_aggregation_algorithms(DEFAULT_USER):
                raise AggregationAlgorithmUnknown()
        else:
            aggregation_algorithm_id = uuid4().hex
        return self.driver.set_aggregation_algorithm_dict(intra_extension_id, aggregation_algorithm_id, aggregation_algorithm_dict)

    @filter_input
    @enforce("read", "aggregation_algorithm")
    def get_aggregation_algorithm_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :param intra_extension_id:
        :return: {
            aggregation_algorithm_id: {
                 name: xxx,
                 description: yyy
                 }
            }
        """
        if not self.driver.get_aggregation_algorithm_dict(intra_extension_id):
            raise AggregationAlgorithmNotExisting()
        return self.driver.get_aggregation_algorithm_dict(intra_extension_id)

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
    @enforce("write", "rule")
    def add_sub_meta_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_dict):
        sub_meta_rules_dict = self.driver.get_sub_meta_rules_dict(intra_extension_id)
        for _sub_meta_rule_id in sub_meta_rules_dict:
            if sub_meta_rule_dict['name'] is sub_meta_rules_dict[_sub_meta_rule_id]["name"]:
                raise SubMetaRuleNameExisting()
            elif sub_meta_rule_dict['subject_categories'] is sub_meta_rules_dict[_sub_meta_rule_id]["subject_categories"] and \
                sub_meta_rule_dict['object_categories'] is sub_meta_rules_dict[_sub_meta_rule_id]["object_categories"] and \
                sub_meta_rule_dict['action_categories'] is sub_meta_rules_dict[_sub_meta_rule_id]["action_categories"] and \
                sub_meta_rule_dict['algorithm'] is sub_meta_rules_dict[_sub_meta_rule_id]["algorithm"]:
                raise SubMetaRuleExisting()
        sub_meta_rule_id = uuid4().hex()
        # TODO (dthom): add new sub-meta-rule to rule
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
    @enforce(("read", "write"), "rule")
    def del_sub_meta_rule(self, user_id, intra_extension_id, sub_meta_rule_id):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        # TODO (dthom): destroy sub-meta-rule-related rules
        # self.driver.del_rule(intra_extension_id, sub_meta_rule_id, "*")
        self.driver.del_sub_meta_rule(intra_extension_id, sub_meta_rule_id)

    @filter_input
    @enforce(("read", "write"), "sub_meta_rules")
    @enforce("write", "rule")
    def set_sub_meta_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id, sub_meta_rule_dict):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        # TODO (dthom): add new sub-meta-rule to rule
        # self.driver.add_rule(intra_extension_id, sub_meta_rule_id, [])
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
        rule_id = uuid4().hex
        return self.driver.set_rule_dict(intra_extension_id, sub_meta_rule_id, rule_id, rule_list)

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
        rules_dict = self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id)
        if rule_id not in rules_dict:
            raise RuleUnknown()
        self.driver.del_rule(intra_extension_id, sub_meta_rule_id, rule_id)

    @filter_input
    @enforce("read", "sub_meta_rules")
    @enforce(("read", "write"), "rules")
    def set_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id, rule_id, rule_list):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rules_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        rules_dict = self.driver.get_rules_dict(intra_extension_id, sub_meta_rule_id)
        if rule_id not in rules_dict:
            raise RuleUnknown()
        return self.driver.set_rule_dict(intra_extension_id, sub_meta_rule_id, rule_id, rule_list)


@dependency.provider('authz_api')
@dependency.requires('identity_api', 'tenant_api', 'moonlog_api')
class IntraExtensionAuthzManager(IntraExtensionManager):

    def __init__(self):
        self.__genre__ = "authz"
        super(IntraExtensionAuthzManager, self).__init__()

    def authz(self, tenant_name, subject_name, object_name, action_name, genre="authz"):
        # TODO (dthom) add moon log
        """Check authorization for a particular action.
        :return: True or False or raise an exception
        """
        tenant_id = self.tenant_api.get_tenant_id_from_name(DEFAULT_USER, tenant_name)
        intra_extension_id = self.tenant_api.get_tenant_intra_extension_id(DEFAULT_USER, tenant_id, genre)
        subjects_dict = self.driver.get_subjects_dict(intra_extension_id)
        subject_id = None
        for _subject_id in subjects_dict:
            if subjects_dict[_subject_id]['name'] is subject_name:
                subject_id = _subject_id
        if not subject_id:
            raise SubjectUnknown()
        objects_dict = self.driver.get_objects_dict(intra_extension_id)
        object_id = None
        for _object_id in objects_dict:
            if objects_dict[_object_id]['name'] is object_name:
                object_id = _object_id
        if not object_id:
            raise ObjectUnknown()
        actions_dict = self.driver.get_actions_dict(intra_extension_id)
        action_id = None
        for _action_id in actions_dict:
            if actions_dict[_action_id] is action_name:
                action_id = _action_id
        if not action_id:
            raise ActionUnknown()
        return super(IntraExtensionAuthzManager, self).authz(intra_extension_id, subject_id, object_id, action_id)


@dependency.provider('admin_api')
@dependency.requires('identity_api', 'tenant_api', 'moonlog_api')
class IntraExtensionAdminManager(IntraExtensionManager):

    def __init__(self):
        self.__genre__ = "admin"
        super(IntraExtensionAdminManager, self).__init__()


@dependency.provider('moonlog_api')
class LogManager(manager.Manager):

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

    def get_policy_template_dict(self):
        raise exception.NotImplemented()  # pragma: no cover

    def get_aggregation_algorithm_dict(self):
        raise exception.NotImplemented()  # pragma: no cover

    def get_sub_meta_rule_algorithm_dict(self):
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
            data_values = self.get_subjects_dict(intra_extension_uuid)["subjects"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise SubjectUnknown()
        elif data_name == self.OBJECT:
            data_values = self.get_objects_dict(intra_extension_uuid)["objects"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ObjectUnknown()
        elif data_name == self.ACTION:
            data_values = self.get_actions_dict(intra_extension_uuid)["actions"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ActionUnknown()
        elif data_name == self.SUBJECT_CATEGORY:
            data_values = self.get_subject_categories_dict(intra_extension_uuid)["subject_categories"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise SubjectCategoryUnknown()
        elif data_name == self.OBJECT_CATEGORY:
            data_values = self.get_object_categories_dict(intra_extension_uuid)["object_categories"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ObjectCategoryUnknown()
        elif data_name == self.ACTION_CATEGORY:
            data_values = self.get_action_categories_dict(intra_extension_uuid)["action_categories"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ActionCategoryUnknown()
        elif data_name == self.SUBJECT_SCOPE:
            if not category_uuid:
                category_uuid = self.get_uuid_from_name(intra_extension_uuid, category_name, self.SUBJECT_CATEGORY)
            data_values = self.get_subject_scopes_dict(intra_extension_uuid,
                                                       category_uuid)["subject_category_scope"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise SubjectScopeUnknown()
        elif data_name == self.OBJECT_SCOPE:
            if not category_uuid:
                category_uuid = self.get_uuid_from_name(intra_extension_uuid, category_name, self.OBJECT_CATEGORY)
            data_values = self.get_object_scopes_dict(intra_extension_uuid,
                                                      category_uuid)["object_category_scope"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ObjectScopeUnknown()
        elif data_name == self.ACTION_SCOPE:
            if not category_uuid:
                category_uuid = self.get_uuid_from_name(intra_extension_uuid, category_name, self.ACTION_CATEGORY)
            data_values = self.get_action_scopes_dict(intra_extension_uuid,
                                                      category_uuid)["action_category_scope"]
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise ActionScopeUnknown()
        elif data_name == self.SUB_META_RULE:
            data_values = self.get_sub_meta_rules_dict(intra_extension_uuid)["sub_meta_rule"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise SubMetaRuleUnknown()
        if category_uuid:
            return data_values[category_uuid]
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

    # TODO: check with load
    # def add_intra_extensions_dict(self):
    #     raise exception.NotImplemented()  # pragma: no cover

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

    def set_aggregation_algorithm(self, intra_extension_id, aggregation_algorithm_id, aggregation_algorithm_dict):
        raise exception.NotImplemented()  # pragma: no cover

    def get_aggregation_algorithm(self, intra_extension_id):
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


# @dependency.provider('superextension_api')
# class SuperExtensionManager(manager.Manager):
#
#     def __init__(self):
#         driver = CONF.moon.superextension_driver
#         super(SuperExtensionManager, self).__init__(driver)
#
#     def authz(self, sub, obj, act):
#         #return self.driver.admin(sub, obj, act)
#         return True


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
# class SuperExtensionDriver(object):
#
#     def __init__(self):
#         self.__super_extension = None
#
#     def admin(self, sub, obj, act):
#         return self.__super_extension.authz(sub, obj, act)
#
#     def delegate(self, delegating_uuid, delegated_uuid, privilege):  # TODO later
#         pass
#
#     # Getter and Setter for SuperExtensions
#
#     def get_super_extensions(self):
#         raise exception.NotImplemented()  # pragma: no cover
#
#     def create_super_extensions(self, super_id, super_extension):
#         raise exception.NotImplemented()  # pragma: no cover
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

