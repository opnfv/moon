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
DEFAULT_USER = uuid4().hex()  # default user_id for internal invocation


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


def filter_args(func):
    def wrapped(*args, **kwargs):
        _args = []
        for arg in args:
            if type(arg) in (unicode, str):
                arg = "".join(re.findall("[\w\-+]*", arg))
            _args.append(arg)
        for arg in kwargs:
            if type(kwargs[arg]) in (unicode, str):
                kwargs[arg] = "".join(re.findall("[\w\-+]*", kwargs[arg]))
        return func(*_args, **kwargs)
    return wrapped


def enforce(actions, object, **extra):
    _actions = actions

    def wrap(func):
        def wrapped(*args):
            # global actions
            self = args[0]
            user_name = args[1]
            intra_extension_uuid = args[2]
            _admin_extension_uuid = self.tenant_api.get_admin_extension_uuid(args[2])
            # func.func_globals["_admin_extension_uuid"] = _admin_extension_uuid
            if not _admin_extension_uuid:
                args[0].moonlog_api.warning("No admin IntraExtension found, authorization granted by default.")
                return func(*args)
            else:
                _authz = False
                if type(_actions) in (str, unicode):
                    actions = (_actions, )
                else:
                    actions = _actions
                for action in actions:
                    if self.admin_api.authz(
                            _admin_extension_uuid,
                            user_name,
                            object,
                            action):
                        _authz = True
                    else:
                        _authz = False
                        break
                if _authz:
                    return func(*args)
        return wrapped
    return wrap


def filter_input(data):
    if type(data) not in (str, unicode):
        return data
    try:
        return "".join(re.findall("[\w\-+*]", data))
    except TypeError:
        LOG.error("Error in filtering input data: {}".format(data))


@dependency.provider('configuration_api')
@dependency.requires('moonlog_api')  # TODO: log should be totally removed to exception.py
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
@dependency.requires('moonlog_api')  # TODO: log should be totally removed to exception.py
class TenantManager(manager.Manager):

    def __init__(self):
        super(TenantManager, self).__init__(CONF.moon.tenant_driver)

    def get_tenant_dict(self, user_id):
        """
        Return a dictionary with all tenants
        :return: dict
        """
        # TODO: check user right with user_id in SuperExtension
        return self.driver.get_tenant_dict()

    def add_tenant(self, user_id, tenant_name, intra_authz_ext_id, intra_admin_ext_id):
        # TODO: check user right with user_id in SuperExtension
        tenant_dict = self.driver.get_tenant_dict()
        for tenant_id in tenant_dict:
            if tenant_dict[tenant_id]['name'] is tenant_name:
                raise TenantAddedNameExisting()
        return self.driver.add_tenant(uuid4().hex, tenant_name, intra_authz_ext_id, intra_admin_ext_id)

    def get_tenant(self, user_id, tenant_id):
        # TODO: check user right with user_id in SuperExtension
        tenant_dict = self.driver.get_tenant_dict()
        if tenant_id not in tenant_dict:
            raise TenantUnknown()
        return tenant_dict[tenant_id]

    def del_tenant(self, user_id, tenant_id):
        # TODO: check user right with user_id in SuperExtension
        tenant_dict = self.driver.get_tenant_dict()
        if tenant_id not in tenant_dict:
            raise TenantUnknown()
        return self.driver.del_tenant(tenant_id)

    # def set_tenant_dict(self, user_id, tenant_id, tenant_name, intra_authz_ext_id, intra_admin_ext_id):
    #     # TODO: check user right with user_id in SuperExtension
    #     # TODO (dthom): Tenant must be checked against Keystone database.
    #     return self.driver.set_tenant(tenant_id, tenant_name, intra_authz_ext_id, intra_admin_ext_id)

    def get_tenant_name_from_id(self, user_id, tenant_id):
        # TODO: check user right with user_id in SuperExtension
        tenant_dict = self.driver.get_tenant_dict()
        if tenant_id not in tenant_dict:
            raise TenantUnknown()
        return tenant_dict[tenant_id]["name"]

    def set_tenant_name(self, user_id, tenant_id, tenant_name):
        # TODO: check user right with user_id in SuperExtension
        tenant_dict = self.driver.get_tenant_dict()
        if tenant_id not in tenant_dict:
            raise TenantUnknown()
        return self.driver.set_tenant(
            self,
            tenant_id,
            tenant_name,
            tenant_dict[tenant_id]['intra_authz_ext_id'],
            tenant_dict[tenant_id]['intra_admin_ext_id']
        )

    def get_tenant_id_from_name(self, user_id, tenant_name):
        # TODO: check user right with user_id in SuperExtension
        tenant_dict = self.driver.get_tenant_dict()
        for tenant_id in tenant_dict:
            if tenant_dict[tenant_id]["name"] is tenant_name:
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
        tenant_dict = self.driver.get_tenant_dict()
        if tenant_id not in tenant_dict:
            raise TenantUnknown()
        elif not tenant_dict[tenant_id][genre]:
            raise TenantNoIntraExtension()
        return tenant_dict[tenant_id][genre]

    # TODO: check if we need the func
    def get_tenant_uuid(self, extension_uuid):
        for _tenant_uuid, _tenant_value in six.iteritems(self.get_tenant_dict()):
            if extension_uuid == _tenant_value["authz"] or extension_uuid == _tenant_value["admin"]:
                return _tenant_uuid
        raise TenantIDNotFound()

    # TODO: check if we need the func
    def get_admin_extension_uuid(self, authz_extension_uuid):
        _tenants = self.get_tenant_dict()
        for _tenant_uuid in _tenants:
            if authz_extension_uuid == _tenants[_tenant_uuid]['authz'] and _tenants[_tenant_uuid]['admin']:
                    return _tenants[_tenant_uuid]['admin']
        self.moonlog_api.error(_("No IntraExtension found mapping this Authz IntraExtension: {}.".format(
                               authz_extension_uuid)))
        # FIXME (dthom): if AdminIntraExtensionNotFound, maybe we can add an option in configuration file
        # to allow or not the fact that Admin IntraExtension can be None
        # raise AdminIntraExtensionNotFound()

    # TODO: check if we need the func
    def delete(self, authz_extension_uuid):
        _tenants = self.get_tenant_dict()
        for _tenant_uuid in _tenants:
            if authz_extension_uuid == _tenants[_tenant_uuid]['authz']:
                return self.set_tenant_dict(_tenant_uuid, "", "", "")
        raise AuthzIntraExtensionNotFound(_("No IntraExtension found mapping this Authz IntraExtension: {}.".format(
            authz_extension_uuid)))


@dependency.requires('identity_api', 'tenant_api', 'configuration_api', 'authz_api', 'admin_api', 'moonlog_api')
class IntraExtensionManager(manager.Manager):

    __genre__ = None

    def __init__(self):
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
            'subject_attributes': {
                'subject_category1': [],
                'subject_category2': [],
                ...
                'subject_categoryn': []
            },
            'object_attributes': {},
            'action_attributes': {},
        }
        """
        authz_buffer = dict()
        authz_buffer['subject_id'] = subject_id
        authz_buffer['object_id'] = object_id
        authz_buffer['action_id'] = action_id
        meta_data_dict = dict()
        meta_data_dict["subject_categories"] = self.driver.get_subject_category_dict(intra_extension_id)["subject_categories"]
        meta_data_dict["object_categories"] = self.driver.get_object_category_dict(intra_extension_id)["object_categories"]
        meta_data_dict["action_categories"] = self.driver.get_action_category_dict(intra_extension_id)["action_categories"]
        subject_assignment_dict = dict()
        for category in meta_data_dict["subject_categories"]:
            subject_assignment_dict[category] = self.driver.get_subject_assignment_dict(
                intra_extension_id, category)["subject_category_assignments"]
        object_assignment_dict = dict()
        for category in meta_data_dict["object_categories"]:
            object_assignment_dict[category] = self.driver.get_object_assignment_dict(
                intra_extension_id, category)["object_category_assignments"]
        action_assignment_dict = dict()
        for category in meta_data_dict["action_categories"]:
            action_assignment_dict[category] = self.driver.get_action_assignment_dict(
                intra_extension_id, category)["action_category_assignments"]
        authz_buffer['subject_attributes'] = dict()
        authz_buffer['object_attributes'] = dict()
        authz_buffer['action_attributes'] = dict()
        for _subject_category in meta_data_dict['subject_categories']:
            authz_buffer['subject_attributes'][_subject_category] = subject_assignment_dict[_subject_category]
        for _object_category in meta_data_dict['object_categories']:
            authz_buffer['object_attributes'][_object_category] = object_assignment_dict[_object_category]
        for _action_category in meta_data_dict['action_categories']:
            authz_buffer['action_attributes'][_action_category] = action_assignment_dict[_action_category]
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

        meta_rule_dict = self.driver.get_meta_rule_dict(intra_extension_id)

        for sub_meta_rule_id in meta_rule_dict['sub_meta_rules']:
            if meta_rule_dict['sub_meta_rules'][sub_meta_rule_id]['algorithm'] == 'inclusion':
                decision_buffer[sub_meta_rule_id] = inclusion(
                    authz_buffer,
                    meta_rule_dict['sub_meta_rules'][sub_meta_rule_id],
                    self.driver.get_rule_dict(intra_extension_id, sub_meta_rule_id).values())
            elif meta_rule_dict['sub_meta_rules'][sub_meta_rule_id]['algorithm'] == 'comparison':
                decision_buffer[sub_meta_rule_id] = comparison(
                    authz_buffer,
                    meta_rule_dict['sub_meta_rules'][sub_meta_rule_id],
                    self.driver.get_rule_dict(intra_extension_id, sub_meta_rule_id).values())

        if meta_rule_dict['aggregation'] == 'all_true':
            return all_true(decision_buffer)

        return False

    def get_intra_extension_dict(self, user_id):
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
        return self.driver.get_intra_extension_dict()

    # load policy from policy directory
    # TODO (dthom) re-check these funcs

    def __load_metadata_file(self, intra_extension_dict, policy_dir):

        metadata_path = os.path.join(policy_dir, 'metadata.json')
        f = open(metadata_path)
        json_perimeter = json.load(f)

        subject_categories_dict = dict()
        for _cat in json_perimeter['subject_categories']:
            subject_categories_dict[uuid4().hex] = {"name": _cat}
        self.driver.set_subject_category_dict(intra_extension_dict["id"], subject_categories_dict)
        # Initialize scope categories
        for _cat in subject_categories_dict.keys():
            self.driver.set_subject_scope_dict(intra_extension_dict["id"], _cat, {})
        intra_extension_dict['subject_categories'] = subject_categories_dict

        object_categories_dict = dict()
        for _cat in json_perimeter['object_categories']:
            object_categories_dict[uuid4().hex] = {"name": _cat}
        self.driver.set_object_category_dict(intra_extension_dict["id"], object_categories_dict)
        # Initialize scope categories
        for _cat in object_categories_dict.keys():
            self.driver.set_object_scope_dict(intra_extension_dict["id"], _cat, {})
        intra_extension_dict['object_categories'] = object_categories_dict

        action_categories_dict = dict()
        for _cat in json_perimeter['action_categories']:
            action_categories_dict[uuid4().hex] = {"name": _cat}
        self.driver.set_action_category_dict(intra_extension_dict["id"], action_categories_dict)
        # Initialize scope categories
        for _cat in action_categories_dict.keys():
            self.driver.set_action_scope_dict(intra_extension_dict["id"], _cat, {})
        intra_extension_dict['action_categories'] = action_categories_dict

    def __load_perimeter_file(self, intra_extension_dict, policy_dir):

        perimeter_path = os.path.join(policy_dir, 'perimeter.json')
        f = open(perimeter_path)
        json_perimeter = json.load(f)

        subject_dict = dict()
        # We suppose that all subjects can be mapped to a true user in Keystone
        for _subject in json_perimeter['subjects']:
            user = self.identity_api.get_user_by_name(_subject, "default")
            subject_dict[user["id"]] = user
        self.driver.set_subject_dict(intra_extension_dict["id"], subject_dict)
        intra_extension_dict["subjects"] = subject_dict

        # Copy all values for objects and subjects
        object_dict = dict()
        for _object in json_perimeter['objects']:
            object_dict[uuid4().hex] = {"name": _object}
        self.driver.set_object_dict(intra_extension_dict["id"], object_dict)
        intra_extension_dict["objects"] = object_dict

        action_dict = dict()
        for _action in json_perimeter['actions']:
            action_dict[uuid4().hex] = {"name": _action}
        self.driver.set_action_dict(intra_extension_dict["id"], action_dict)
        intra_extension_dict["ations"] = action_dict

    def __load_scope_file(self, intra_extension_dict, policy_dir):

        metadata_path = os.path.join(policy_dir, 'scope.json')
        f = open(metadata_path)
        json_perimeter = json.load(f)

        intra_extension_dict['subject_category_scope'] = dict()
        for category, scope in json_perimeter["subject_category_scope"].iteritems():
            category = self.driver.get_uuid_from_name(intra_extension_dict["id"], category, self.driver.SUBJECT_CATEGORY)
            _scope_dict = dict()
            for _scope in scope:
                _scope_dict[uuid4().hex] = {"name": _scope}
            self.driver.set_subject_scope_dict(intra_extension_dict["id"], category, _scope_dict)
            intra_extension_dict['subject_category_scope'][category] = _scope_dict

        intra_extension_dict['object_category_scope'] = dict()
        for category, scope in json_perimeter["object_category_scope"].iteritems():
            category = self.driver.get_uuid_from_name(intra_extension_dict["id"], category, self.driver.OBJECT_CATEGORY)
            _scope_dict = dict()
            for _scope in scope:
                _scope_dict[uuid4().hex] = {"name": _scope}
            self.driver.set_object_scope_dict(intra_extension_dict["id"], category, _scope_dict)
            intra_extension_dict['object_category_scope'][category] = _scope_dict

        intra_extension_dict['action_category_scope'] = dict()
        for category, scope in json_perimeter["action_category_scope"].iteritems():
            category = self.driver.get_uuid_from_name(intra_extension_dict["id"], category, self.driver.ACTION_CATEGORY)
            _scope_dict = dict()
            for _scope in scope:
                _scope_dict[uuid4().hex] = {"name": _scope}
            self.driver.set_action_scope_dict(intra_extension_dict["id"], category, _scope_dict)
            intra_extension_dict['action_category_scope'][category] = _scope_dict

    def __load_assignment_file(self, intra_extension_dict, policy_dir):

        f = open(os.path.join(policy_dir, 'assignment.json'))
        json_assignments = json.load(f)

        subject_assignments = dict()
        for category_name, value in json_assignments['subject_assignments'].iteritems():
            category = self.driver.get_uuid_from_name(intra_extension_dict["id"], category_name, self.driver.SUBJECT_CATEGORY)
            for user_name in value:
                user_id = self.driver.get_uuid_from_name(intra_extension_dict["id"], user_name, self.driver.SUBJECT)
                if user_id not in subject_assignments:
                    subject_assignments[user_id] = dict()
                if category not in subject_assignments[user_id]:
                    subject_assignments[user_id][category] = \
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.SUBJECT_SCOPE, category_name),
                            value[user_name])
                else:
                    subject_assignments[user_id][category].extend(
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.SUBJECT_SCOPE, category_name),
                            value[user_name])
                    )
        # Note (dthom): subject_category_assignment must be initialized because when there is no data in json
        # we will not go through the for loop
        self.driver.set_subject_assignment_dict(intra_extension_dict["id"])
        for subject in subject_assignments:
            self.driver.set_subject_assignment_dict(intra_extension_dict["id"], subject, subject_assignments[subject])

        object_assignments = dict()
        for category_name, value in json_assignments["object_assignments"].iteritems():
            category = self.driver.get_uuid_from_name(intra_extension_dict["id"], category_name, self.driver.OBJECT_CATEGORY)
            for object_name in value:
                if object_name not in object_assignments:
                    object_assignments[object_name] = dict()
                if category not in object_assignments[object_name]:
                    object_assignments[object_name][category] = \
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.OBJECT_SCOPE, category_name),
                            value[object_name])
                else:
                    object_assignments[object_name][category].extend(
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.OBJECT_SCOPE, category_name),
                            value[object_name])
                    )
        # Note (dthom): object_category_assignment must be initialized because when there is no data in json
        # we will not go through the for loop
        self.driver.set_object_assignment_dict(intra_extension_dict["id"])
        for object in object_assignments:
            self.driver.set_object_assignment_dict(intra_extension_dict["id"], object, object_assignments[object])

        action_assignments = dict()
        for category_name, value in json_assignments["action_assignments"].iteritems():
            category = self.driver.get_uuid_from_name(intra_extension_dict["id"], category_name, self.driver.ACTION_CATEGORY)
            for action_name in value:
                if action_name not in action_assignments:
                    action_assignments[action_name] = dict()
                if category not in action_assignments[action_name]:
                    action_assignments[action_name][category] = \
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.ACTION_SCOPE, category_name),
                            value[action_name])
                else:
                    action_assignments[action_name][category].extend(
                        map(lambda x: self.driver.get_uuid_from_name(intra_extension_dict["id"], x, self.driver.ACTION_SCOPE, category_name),
                            value[action_name])
                    )
        # Note (dthom): action_category_assignment must be initialized because when there is no data in json
        # we will not go through the for loop
        self.driver.set_action_assignment_dict(intra_extension_dict["id"])
        for action in action_assignments:
            self.driver.set_action_assignment_dict(intra_extension_dict["id"], action, action_assignments[action])

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
        for relation in json_metarule["sub_meta_rules"]:
            metarule[relation] = dict()
            for item in ("subject_categories", "object_categories", "action_categories"):
                metarule[relation][item] = list()
                for element in json_metarule["sub_meta_rules"][relation][item]:
                    metarule[relation][item].append(self.driver.get_uuid_from_name(intra_extension_dict["id"], element, categories[item]))
            metarule[relation]["algorithm"] = json_metarule["sub_meta_rules"][relation]["algorithm"]
        submetarules = {
            "aggregation": json_metarule["aggregation"],
            "sub_meta_rules": metarule
        }
        self.driver.set_meta_rule_dict(intra_extension_dict["id"], submetarules)

    def __load_rule_file(self, intra_extension_dict, policy_dir):

        metadata_path = os.path.join(policy_dir, 'rule.json')
        f = open(metadata_path)
        json_rules = json.load(f)
        intra_extension_dict["rule"] = {"rule": copy.deepcopy(json_rules)}
        # Translate value from JSON file to UUID for Database
        rules = dict()
        sub_meta_rules = self.driver.get_meta_rule_dict(intra_extension_dict["id"])
        for relation in json_rules:
            # print(relation)
            # print(self.get_sub_meta_rule_relations("admin", ie["id"]))
            # if relation not in self.get_sub_meta_rule_relations("admin", ie["id"])["sub_meta_rule_relations"]:
            #     raise IntraExtensionException("Bad relation name {} in rules".format(relation))
            rules[relation] = list()
            for rule in json_rules[relation]:
                subrule = list()
                _rule = list(rule)
                for category_uuid in sub_meta_rules["rule"][relation]["subject_categories"]:
                    scope_name = _rule.pop(0)
                    scope_uuid = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                                scope_name,
                                                                self.driver.SUBJECT_SCOPE,
                                                                category_uuid=category_uuid)
                    subrule.append(scope_uuid)
                for category_uuid in sub_meta_rules["rule"][relation]["action_categories"]:
                    scope_name = _rule.pop(0)
                    scope_uuid = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                                scope_name,
                                                                self.driver.ACTION_SCOPE,
                                                                category_uuid=category_uuid)
                    subrule.append(scope_uuid)
                for category_uuid in sub_meta_rules["rule"][relation]["object_categories"]:
                    scope_name = _rule.pop(0)
                    scope_uuid = self.driver.get_uuid_from_name(intra_extension_dict["id"],
                                                                scope_name,
                                                                self.driver.OBJECT_SCOPE,
                                                                category_uuid=category_uuid)
                    subrule.append(scope_uuid)
                # for cat, cat_func, cat_func_cat in (
                #     ("subject_categories", self.driver.get_uuid_from_name, self.driver.SUBJECT_SCOPE),
                #     ("action_categories", self.driver.ACTION_SCOPE),
                #     ("object_categories", self.driver.OBJECT_SCOPE),
                # ):
                #     for cat_value in sub_meta_rules["sub_meta_rules"][relation][cat]:
                #         scope = cat_func(
                #             ie["id"],
                #             cat_value,
                #             cat_func_cat
                #         )[cat_func.__name__.replace("get_", "").replace("_dict", "")]
                #
                #         _ = rule.pop(0)
                #         a_scope = self.driver.get_uuid_from_name(ie["id"], _, scope[cat_value])
                #         subrule.append(a_scope)
                # if a positive/negative value exists, all item of rule have not be consumed
                if len(rule) >= 1 and type(rule[0]) is bool:
                    subrule.append(rule[0])
                else:
                    # if value doesn't exist add a default value
                    subrule.append(True)
                rules[relation].append(subrule)
        self.driver.set_rule_dict(intra_extension_dict["id"], rules)

    def load_intra_extension_dict(self, user_id, intra_extension_dict):
        # TODO: check will be done through super_extension later
        ie_dict = dict()
        # TODO: clean some values
        ie_dict['id'] = uuid4().hex
        ie_dict["name"] = filter_input(intra_extension_dict["name"])
        ie_dict["model"] = filter_input(intra_extension_dict["policymodel"])
        ie_dict["description"] = filter_input(intra_extension_dict["description"])
        ref = self.driver.set_intra_extension(ie_dict['id'], ie_dict)
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

    def get_intra_extension(self, user_id, intra_extension_id):
        """
        :param user_id:
        :return: {intra_extension_id: intra_extension_name, ...}
        """
        # TODO: check will be done through super_extension later
        if intra_extension_id not in self.driver.get_intra_extension_dict():
            raise IntraExtensionUnknown()
        return self.driver.get_intra_extension_dict()[intra_extension_id]

    def del_intra_extension(self, user_id, intra_extension_id):
        # TODO: check will be done through super_extension later
        if intra_extension_id not in self.driver.get_intra_extension_dict():
            raise IntraExtensionUnknown()
        return self.driver.del_intra_extension(intra_extension_id)

    # Metadata functions

    @filter_args  # TODO: check for each function if intra_entension_id exists
    @enforce("read", "subject_categories")
    def get_subject_category_dict(self, user_id, intra_extension_id):
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
        return self.driver.get_subject_category_dict(intra_extension_id)

    @filter_args
    @enforce(("read", "write"), "subject_categories")
    @enforce(("read", "write"), "subject_scopes")
    def add_subject_category(self, user_id, intra_extension_id, subject_category_name):
        subject_category_dict = self.driver.get_subject_category_dict(intra_extension_id)
        for subject_category_id in subject_category_dict:
            if subject_category_dict[subject_category_id]['name'] is subject_category_name:
                raise SubjectCategoryNameExisting()
        subject_category_id = uuid4().hex
        # TODO (dthom): create category in scope
        # self.driver.create_subject_category_in_scope(intra_extension_id, subject_category_id)
        return self.driver.add_subject_category(intra_extension_id, subject_category_id, subject_category_name)

    @filter_args
    @enforce("read", "subject_categories")
    def get_subject_category(self, user_id, intra_extension_id, subject_category_id):
        subject_category_dict = self.driver.get_subject_category_dict(intra_extension_id)
        if subject_category_id not in subject_category_dict:
            raise SubjectCategoryUnknown()
        return subject_category_dict[subject_category_id]

    @filter_args
    @enforce(("read", "write"), "subject_categories")
    @enforce(("read", "write"), "subject_scopes")
    @enforce(("read", "write"), "subject_assignments")
    def del_subject_category(self, user_id, intra_extension_id, subject_category_id):
        if subject_category_id not in self.driver.get_subject_category_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        # TODO (dthom): destroy category in scope
        # self.driver.destroy_subject_category_in_scope(intra_extension_id, subject_category_id)
        # TODO (dthom): destroy category-related assignment in assignments
        # self.driver.destroy_subject_category_in_assignement(intra_extension_id, subject_category_id)
        return self.driver.del_subject_category(intra_extension_id, subject_category_id)

    @filter_args
    @enforce("read", "object_categories")
    def get_object_category_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :param intra_extension_id:
        :return:
        """
        return self.driver.get_object_category_dict(intra_extension_id)

    @filter_args
    @enforce(("read", "write"), "object_categories")
    @enforce(("read", "write"), "object_scopes")
    def add_object_category(self, user_id, intra_extension_id, object_category_name):
        object_category_dict = self.driver.get_object_category_dict(intra_extension_id)
        for object_category_id in object_category_dict:
            if object_category_dict[object_category_id]["name"] is object_category_name:
                raise ObjectCategoryNameExisting()
        object_category_id = uuid4().hex
        # TODO (dthom): create category in scope
        # self.driver.create_object_category_in_scope(intra_extension_id, object_category_id)
        return self.driver.add_object_category(intra_extension_id, object_category_id, object_category_name)

    @filter_args
    @enforce("read", "object_categories")
    def get_object_category(self, user_id, intra_extension_id, object_category_id):
        object_category_dict = self.driver.get_object_category_dict(intra_extension_id)
        if object_category_id not in object_category_dict:
            raise ObjectCategoryUnknown()
        return object_category_dict[object_category_id]

    @filter_args
    @enforce(("read", "write"), "object_categories")
    @enforce(("read", "write"), "object_scopes")
    @enforce(("read", "write"), "object_assignments")
    def del_object_category(self, user_id, intra_extension_id, object_category_id):
        object_category_dict = self.driver.get_object_category_dict(intra_extension_id)
        if object_category_id not in object_category_dict:
            raise ObjectCategoryUnknown()
        # TODO (dthom): destroy category in scope
        # self.driver.destroy_object_category_in_scope(intra_extension_id, object_category_id)
        # TODO (dthom): destroy category-related assignment in assignments
        # self.driver.destroy_object_category_in_assignement(intra_extension_id, object_category_id)
        return self.driver.del_object_category(intra_extension_id, object_category_id)

    @filter_args
    @enforce("read", "action_categories")
    def get_action_category_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :param intra_extension_id:
        :return:
        """
        return self.driver.get_action_category_dict(intra_extension_id)

    @filter_args
    @enforce(("read", "write"), "action_categories")
    @enforce(("read", "write"), "action_scopes")
    def add_action_category(self, user_id, intra_extension_id, action_category_name):
        action_category_dict = self.driver.get_action_category_dict(intra_extension_id)
        for action_category_id in action_category_dict:
            if action_category_dict[action_category_id]['name'] is action_category_name:
                raise ActionCategoryNameExisting()
        action_category_id = uuid4().hex
        # TODO (dthom): create category in scope
        # self.driver.create_action_category_in_scope(intra_extension_id, action_category_id)
        return self.driver.add_action_category(intra_extension_id, action_category_id, action_category_name)

    @filter_args
    @enforce("read", "action_categories")
    def get_action_category(self, user_id, intra_extension_id, action_category_id):
        action_category_dict = self.driver.get_action_category_dict(intra_extension_id)
        if action_category_id not in action_category_dict:
            raise ActionCategoryUnknown()
        return self.driver.get_action_category_dict(intra_extension_id)[action_category_id]

    @filter_args
    @enforce(("read", "write"), "action_categories")
    @enforce(("read", "write"), "action_category_scopes")
    def del_action_category(self, user_id, intra_extension_id, action_category_id):
        action_category_dict = self.driver.get_action_category_dict(intra_extension_id)
        if action_category_id not in action_category_dict:
            raise ActionCategoryUnknown()
        # TODO (dthom): destroy category in scope
        # self.driver.destroy_action_category_in_scope(intra_extension_id, action_category_id)
        # TODO (dthom): destroy category-related assignment in assignement
        # self.driver.destroy_action_category_in_assignement(intra_extension_id, action_category_id)
        return self.driver.del_action_category(intra_extension_id, action_category_id)

    # Perimeter functions

    @filter_args
    @enforce("read", "subjects")
    def get_subject_dict(self, user_id, intra_extension_id):
        """
        :param user_id:
        :param intra_extension_id:
        :return: {
            subject_id1: {
                name: xxx,
                description: yyy,
                 ...},
            subject_id2: {...},
            ...}
        """
        return self.driver.get_subject_dict(intra_extension_id)

    @filter_args
    @enforce(("read", "write"), "subjects")
    def add_subject(self, user_id, intra_extension_id, subject_name):
        subject_dict = self.driver.get_subject_dict(intra_extension_id)
        for subject_id in subject_dict:
            if subject_dict[subject_id]["name"] is subject_name:
                raise SubjectNameExisting()
        # Next line will raise an error if user is not present in Keystone database
        subject_item_dict = self.identity_api.get_user_by_name(subject_name, "default")
        return self.driver.add_subject(intra_extension_id, subject_item_dict["id"], subject_name)

    @filter_args
    @enforce("read", "subjects")
    def get_subject(self, user_id, intra_extension_id, subject_id):
        subject_dict = self.driver.get_subject_dict(intra_extension_id)
        if subject_id in subject_dict:
            raise SubjectUnknown()
        return subject_dict[subject_id]

    @filter_args
    @enforce(("read", "write"), "subjects")
    def del_subject(self, user_id, intra_extension_id, subject_id):
        if subject_id in self.driver.get_subject_dict(intra_extension_id):
            raise SubjectUnknown()
        # TODO (dthom): destroy item-related assignment
        return self.driver.del_subject(intra_extension_id, subject_id)

    @filter_args
    @enforce("read", "objects")
    def get_object_dict(self, user_id, intra_extension_id):
        return self.driver.get_object_dict(intra_extension_id)

    @filter_args
    @enforce(("read", "write"), "objects")
    def add_object(self, user_id, intra_extension_id, object_name):
        object_dict = self.driver.get_object_dict(intra_extension_id)
        for object_id in object_dict:
            if object_dict[object_id]["name"] is object_name:
                raise ObjectNameExisting()
        object_id = uuid4().hex
        return self.driver.add_object(intra_extension_id, object_id, object_name)

    @filter_args
    @enforce("read", "objects")
    def get_object(self, user_id, intra_extension_id, object_id):
        object_dict = self.driver.get_object_dict(intra_extension_id)
        if object_id in object_dict:
            raise ObjectUnknown()
        return object_dict[object_id]

    @filter_args
    @enforce(("read", "write"), "objects")
    def del_object(self, user_id, intra_extension_id, object_id):
        if object_id in self.driver.get_object_dict(intra_extension_id):
            raise ObjectUnknown()
        # TODO (dthom): destroy item-related assignment
        return self.driver.del_object(intra_extension_id, object_id)

    @filter_args
    @enforce("read", "actions")
    def get_action_dict(self, user_id, intra_extension_id):
        return self.driver.get_action_dict(intra_extension_id)

    @filter_args
    @enforce(("read", "write"), "actions")
    def add_action(self, user_id, intra_extension_id, action_name):
        action_dict = self.driver.get_action_dict(intra_extension_id)
        for action_id in action_dict:
            if action_dict[action_id]["name"] is action_name:
                raise ActionNameExisting()
        action_id = uuid4().hex
        return self.driver.add_action(intra_extension_id, action_id, action_name)

    @filter_args
    @enforce("read", "actions")
    def get_action(self, user_id, intra_extension_id, action_id):
        action_dict = self.driver.get_action_dict(intra_extension_id)
        if action_id in action_dict:
            raise ActionUnknown()
        return action_dict[action_id]

    @filter_args
    @enforce(("read", "write"), "actions")
    def del_action(self, user_id, intra_extension_id, action_id):
        if action_id in self.driver.get_action_dict(intra_extension_id):
            raise ActionUnknown()
        # TODO (dthom): destroy item-related assignment
        return self.driver.del_action(intra_extension_id, action_id)

    # Scope functions

    @filter_args
    @enforce("read", "subject_scopes")
    @enforce("read", "subject_categories")
    def get_subject_scope_dict(self, user_id, intra_extension_id, subject_category_id):
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
        if subject_category_id not in self.driver.get_subject_category_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        return self.driver.get_subject_scope_dict(intra_extension_id, subject_category_id)

    @filter_args
    @enforce(("read", "write"), "subject_scopes")
    @enforce("read", "subject_categories")
    def add_subject_scope(self, user_id, intra_extension_id, subject_category_id, subject_scope_name):
        if subject_category_id not in self.driver.get_subject_category_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        subject_scope_dict = self.driver.get_subject_scope_dict(intra_extension_id, subject_category_id)
        for _subject_scope_id in subject_scope_dict:
            if subject_scope_name is subject_scope_dict[_subject_scope_id]['name']:
                raise SubjectScopeNameExisting()
        subject_scope_id = uuid4().hex
        return self.driver.add_subject_scope(
            intra_extension_id,
            subject_category_id,
            subject_scope_id,
            subject_scope_name)

    @filter_args
    @enforce("read", "subject_scopes")
    @enforce("read", "subject_categories")
    def get_subject_scope(self, user_id, intra_extension_id, subject_category_id, subject_scope_id):
        if subject_category_id not in self.driver.get_subject_category_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        subject_scopte_dict = self.driver.get_subject_scope_dict(intra_extension_id, subject_category_id)
        if subject_scope_id not in subject_scopte_dict:
            raise SubjectScopeUnknown()
        return subject_scopte_dict[subject_scope_id]

    @filter_args
    @enforce(("read", "write"), "subject_scopes")
    @enforce("read", "subject_categories")
    def del_subject_scope(self, user_id, intra_extension_id, subject_category_id, subject_scope_id):
        if subject_category_id not in self.driver.get_subject_category_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        if subject_scope_id not in self.driver.get_subject_scope_dict(intra_extension_id, subject_category_id):
            raise SubjectScopeUnknown()
        # TODO (dthom): destroy scope-related assignment
        # TODO (dthom): destroy scope-related rule
        return self.driver.del_subject_scope(intra_extension_id, subject_category_id, subject_scope_id)

    @filter_args
    @enforce("read", "object_category_scopes")
    @enforce("read", "object_categories")
    def get_object_scope_dict(self, user_id, intra_extension_id, object_category_id):
        if object_category_id not in self.driver.get_object_category_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        return self.driver.get_object_scope_dict(intra_extension_id, object_category_id)

    @filter_args
    @enforce(("read", "write"), "object_scopes")
    @enforce("read", "object_categories")
    def add_object_scope(self, user_id, intra_extension_id, object_category_id, object_scope_name):
        if object_category_id not in self.driver.get_object_category_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        object_scope_dict = self.driver.get_object_scope_dict(intra_extension_id, object_category_id)
        for _object_scope_id in object_scope_dict:
            if object_scope_name is object_scope_dict[_object_scope_id]['name']:
                raise ObjectScopeNameExisting()
        object_scope_id = uuid4().hex
        return self.driver.add_subject_scope(
            intra_extension_id,
            object_category_id,
            object_scope_id,
            object_scope_name)

    @filter_args
    @enforce("read", "object_scopes")
    @enforce("read", "object_categories")
    def get_object_scope(self, user_id, intra_extension_id, object_category_id, object_scope_id):
        if object_category_id not in self.driver.get_object_category_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        object_scopte_dict = self.driver.get_object_scope_dict(intra_extension_id, object_category_id)
        if object_scope_id not in object_scopte_dict:
            raise ObjectScopeUnknown()
        return object_scopte_dict[object_scope_id]

    @filter_args
    @enforce(("read", "write"), "object_scopes")
    @enforce("read", "object_categories")
    def del_object_scope(self, user_id, intra_extension_id, object_category_id, object_scope_id):
        if object_category_id not in self.driver.get_object_category_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        if object_scope_id not in self.driver.get_object_scope_dict(intra_extension_id, object_category_id):
            raise ObjectScopeUnknown()
        # TODO (dthom): destroy scope-related assignment
        # TODO (dthom): destroy scope-related rule
        return self.driver.del_object_scope(intra_extension_id, object_category_id, object_scope_id)

    @filter_args
    @enforce("read", "action_category_scopes")
    @enforce("read", "action_categories")
    def get_action_scope_dict(self, user_id, intra_extension_id, action_category_id):
        if action_category_id not in self.driver.get_object_category_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        return self.driver.get_action_scope_dict(intra_extension_id, action_category_id)

    @filter_args
    @enforce(("read", "write"), "action_scopes")
    @enforce("read", "action_categories")
    def add_action_scope(self, user_id, intra_extension_id, action_category_id, action_scope_name):
        if action_category_id not in self.driver.get_action_category_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        action_scope_dict = self.driver.get_action_scope_dict(intra_extension_id, action_category_id)
        for _action_scope_id in action_scope_dict:
            if action_scope_name is action_scope_dict[_action_scope_id]['name']:
                raise ActionScopeNameExisting()
        action_scope_id = uuid4().hex
        return self.driver.add_action_scope(
            intra_extension_id,
            action_category_id,
            action_scope_id,
            action_scope_name)

    @filter_args
    @enforce("read", "action_scopes")
    @enforce("read", "action_categories")
    def get_action_scope(self, user_id, intra_extension_id, action_category_id, action_scope_id):
        if action_category_id not in self.driver.get_action_category_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        action_scopte_dict = self.driver.get_action_scope_dict(intra_extension_id, action_category_id)
        if action_scope_id not in action_scopte_dict:
            raise ActionScopeUnknown()
        return action_scopte_dict[action_scope_id]

    @filter_args
    @enforce(("read", "write"), "action_scopes")
    @enforce("read", "action_categories")
    def del_action_scope(self, user_id, intra_extension_id, action_category_id, action_scope_id):
        if action_category_id not in self.driver.get_action_category_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        if action_scope_id not in self.driver.get_action_scope_dict(intra_extension_id, action_category_id):
            raise ActionScopeUnknown()
        # TODO (dthom): destroy scope-related assignment
        # TODO (dthom): destroy scope-related rule
        return self.driver.del_action_scope(intra_extension_id, action_category_id, action_scope_id)

    # Assignment functions

    @filter_args
    @enforce("read", "subject_assignments")
    @enforce("read", "subjects")
    def get_subject_assignment_dict(self, user_id, intra_extension_id, subject_id):
        """
        :param user_id:
        :param intra_extension_id:
        :param subject_id:
        :return: {
            subject_category_id1: [subject_scope_id1, subject_scope_id2, ...],
            subject_category_id2: [subject_scope_id1, subject_scope_id2, ...],
            ...
        }
        """
        if subject_id not in self.driver.get_subject_dict(user_id, intra_extension_id):
            raise SubjectUnknown()
        return self.driver.get_subject_assignment_dict(intra_extension_id, subject_id)

    @filter_args
    @enforce(("read", "write"), "subject_assignments")
    @enforce("read", "subjects")
    @enforce("read", "subject_categories")
    @enforce("read", "subject_scopes")
    def add_subject_assignment(self, user_id, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        if subject_id not in self.driver.get_subject_dict(intra_extension_id):
            raise SubjectUnknown()
        elif subject_category_id not in self.driver.get_subject_category_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        elif subject_scope_id not in self.driver.get_subject_scope_dict(intra_extension_id, subject_category_id):
            raise SubjectScopeUnknown()
        elif subject_scope_id in self.driver.get_subject_assignment_dict(intra_extension_id, subject_id)[subject_category_id]:
            raise SubjectAssignmentExisting()
        return self.driver.add_subject_assignment(intra_extension_id, subject_id, subject_category_id, subject_scope_id)

    @filter_args
    @enforce("read", "subject_assignments")
    @enforce("read", "subjects")
    @enforce("read", "subject_categories")
    def get_subject_assignment(self, user_id, intra_extension_id, subject_id, subject_category_id):
        if subject_id not in self.driver.get_subject_dict(user_id, intra_extension_id):
            raise SubjectUnknown()
        elif subject_category_id not in self.driver.get_subject_category_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        return self.driver.get_subject_assignment_dict(intra_extension_id, subject_id)[subject_category_id]

    @filter_args
    @enforce(("read", "write"), "subject_assignments")
    @enforce("read", "subjects")
    @enforce("read", "subject_categories")
    @enforce("read", "subject_scopes")
    def del_subject_assignment(self, user_id, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        if subject_id not in self.driver.get_subject_dict(intra_extension_id):
            raise SubjectUnknown()
        elif subject_category_id not in self.driver.get_subject_category_dict(intra_extension_id):
            raise SubjectCategoryUnknown()
        elif subject_scope_id not in self.driver.get_subject_scope_dict(intra_extension_id, subject_category_id):
            raise SubjectScopeUnknown()
        elif subject_scope_id not in self.driver.get_subject_assignment_dict(intra_extension_id, subject_id)[subject_category_id]:
            raise SubjectAssignmentUnknown()
        return self.driver.del_subject_category_assignment(intra_extension_id, subject_id, subject_category_id, subject_scope_id)

    @filter_args
    @enforce("read", "object_assignments")
    @enforce("read", "objects")
    def get_object_assignment_dict(self, user_id, intra_extension_id, object_id):
        if object_id not in self.get_object_dict(user_id, intra_extension_id):
            raise ObjectUnknown()
        return self.driver.get_object_assignment_dict(intra_extension_id, object_id)

    @filter_args
    @enforce(("read", "write"), "object_assignments")
    @enforce("read", "objects")
    @enforce("read", "object_categories")
    def add_object_assignment(self, user_id, intra_extension_id, object_id, object_category_id, object_scope_id):
        if object_id not in self.driver.get_object_dict(intra_extension_id):
            raise ObjectUnknown()
        elif object_category_id not in self.driver.get_object_category_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        elif object_scope_id not in self.driver.get_object_scope_dict(intra_extension_id, object_category_id):
            raise ObjectScopeUnknown()
        elif object_scope_id in self.driver.get_object_assignment_dict(intra_extension_id, object_id)[object_category_id]:
            raise ObjectAssignmentExisting()
        return self.driver.add_object_assignment(intra_extension_id, object_id, object_category_id, object_scope_id)

    @filter_args
    @enforce("read", "object_assignments")
    @enforce("read", "objects")
    @enforce("read", "object_categories")
    def get_object_assignment(self, user_id, intra_extension_id, object_id, object_category_id):
        if object_id not in self.driver.get_object_dict(user_id, intra_extension_id):
            raise ObjectUnknown()
        elif object_category_id not in self.driver.get_object_category_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        return self.driver.get_object_assignment_dict(intra_extension_id, object_id)[object_category_id]

    @filter_args
    @enforce(("read", "write"), "object_assignments")
    @enforce("read", "objects")
    @enforce("read", "object_categories")
    @enforce("read", "object_scopes")
    def del_object_assignment(self, user_id, intra_extension_id, object_id, object_category_id, object_scope_id):
        if object_id not in self.driver.get_object_dict(intra_extension_id):
            raise ObjectUnknown()
        elif object_category_id not in self.driver.get_object_category_dict(intra_extension_id):
            raise ObjectCategoryUnknown()
        elif object_scope_id not in self.driver.get_object_scope_dict(intra_extension_id, object_category_id):
            raise ObjectScopeUnknown()
        elif object_scope_id not in self.driver.get_subject_assignment_dict(intra_extension_id, object_id)[object_category_id]:
            raise ObjectAssignmentUnknown()
        return self.driver.del_object_assignment(intra_extension_id, object_id, object_category_id, object_scope_id)

    @filter_args
    @enforce("read", "action_assignments")
    @enforce("read", "actions")
    def get_action_assignment_dict(self, user_id, intra_extension_id, action_id):
        if action_id not in self.get_action_dict(user_id, intra_extension_id):
            raise ActionUnknown()
        return self.driver.get_action_assignment_dict(intra_extension_id, action_id)

    @filter_args
    @enforce(("read", "write"), "action_assignments")
    @enforce("read", "actions")
    @enforce("read", "action_categories")
    def add_action_assignment(self, user_id, intra_extension_id, action_id, action_category_id, action_scope_id):
        if action_id not in self.driver.get_action_dict(intra_extension_id):
            raise ActionUnknown()
        elif action_category_id not in self.driver.get_action_category_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        elif action_scope_id not in self.driver.get_action_scope_dict(intra_extension_id, action_category_id):
            raise ActionScopeUnknown()
        elif action_scope_id in self.driver.get_action_assignment_dict(intra_extension_id, action_id)[action_category_id]:
            raise ObjectAssignmentExisting()
        return self.driver.add_action_assignment(intra_extension_id, action_id, action_category_id, action_scope_id)

    @filter_args
    @enforce("read", "action_assignments")
    @enforce("read", "actions")
    @enforce("read", "action_categories")
    def get_action_assignment(self, user_id, intra_extension_id, action_id, action_category_id):
        if action_id not in self.driver.get_action_dict(user_id, intra_extension_id):
            raise ActionUnknown()
        elif action_category_id not in self.driver.get_action_category_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        return self.driver.get_action_assignment_dict(intra_extension_id, action_id)[action_category_id]

    @filter_args
    @enforce(("read", "write"), "action_assignments")
    @enforce("read", "actions")
    @enforce("read", "action_categories")
    @enforce("read", "action_scopes")
    def del_action_assignment(self, user_id, intra_extension_id, action_id, action_category_id, action_scope_id):
        if action_id not in self.driver.get_action_dict(intra_extension_id):
            raise ActionUnknown()
        elif action_category_id not in self.driver.get_action_category_dict(intra_extension_id):
            raise ActionCategoryUnknown()
        elif action_scope_id not in self.driver.get_action_scope_dict(intra_extension_id, action_category_id):
            raise ActionScopeUnknown()
        elif action_scope_id not in self.driver.get_action_assignment_dict(intra_extension_id, action_id)[action_category_id]:
            raise ActionAssignmentUnknown()
        return self.driver.del_action_assignment(intra_extension_id, action_id, action_category_id, action_scope_id)

    # Metarule functions

    @filter_args
    @enforce(("read", "write"), "aggregation_algorithm")
    def add_aggregation_algorithm(self, user_id, intra_extension_id, aggregation_algorithm_id):
        if aggregation_algorithm_id not in self.configuration_api.get_aggregation_algorithms:
            raise AggregationAlgorithmUnknown()
        elif self.dirver.get_aggregation_algorithm(intra_extension_id):
            raise AggregationAlgorithmExisting()
        return self.driver.add_aggregation_algorithm(intra_extension_id, aggregation_algorithm_id)

    @filter_args
    @enforce("read", "aggregation_algorithm")
    def get_aggregation_algorithm(self, user_id, intra_extension_id):
        if not self.dirver.get_aggregation_algorithm(intra_extension_id):
            raise AggregationAlgorithmNotExisting()
        return self.driver.get_aggregation_algorithm(intra_extension_id)

    @filter_args
    @enforce("write", "aggregation_algorithm")
    def del_aggregation_algorithm(self, user_id, intra_extension_id, aggregation_algorithm_id):
        if aggregation_algorithm_id is not self.dirver.get_aggregation_algorithm(intra_extension_id):
            raise AggregationAlgorithmNotExisting()
        return self.driver.del_aggregation_algorithm(intra_extension_id, aggregation_algorithm_id)

    @filter_args
    @enforce("read", "sub_meta_rules")
    def get_sub_meta_rule_dict(self, user_id, intra_extension_id):
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
        return self.driver.get_sub_meta_rule_dict(intra_extension_id)

    @filter_args
    @enforce(("read", "write"), "sub_meta_rules")
    @enforce("write", "rule")
    def add_sub_meta_rule(self,
                          user_id,
                          intra_extension_id,
                          sub_meta_rule_name,
                          subject_category_list,
                          object_category_list,
                          action_category_list,
                          sub_meta_rule_algorithm):
        sub_meta_rule_dict = self.driver.get_sub_meta_rule_dict(intra_extension_id)
        for _sub_meta_rule_id in sub_meta_rule_dict:
            if sub_meta_rule_name is sub_meta_rule_dict[_sub_meta_rule_id]["name"]:
                raise SubMetaRuleNameExisting()
            elif subject_category_list is sub_meta_rule_dict[_sub_meta_rule_id]["subject_categories"] and \
                            object_category_list is sub_meta_rule_dict[_sub_meta_rule_id]["object_categories"] and \
                            action_category_list is sub_meta_rule_dict[_sub_meta_rule_id]["action_categories"] and \
                            sub_meta_rule_algorithm is sub_meta_rule_dict[_sub_meta_rule_id]["algorithm"]:
                raise SubMetaRuleExisting()
        sub_meta_rule_id = uuid4().hex()
        # TODO (dthom): add new sub-meta-rule to rule
        # self.driver.add_rule(intra_extension_id, sub_meta_rule_id, [])
        return self.driver.add_sub_meta_rule(
            intra_extension_id,
            sub_meta_rule_id,
            sub_meta_rule_name,
            subject_category_list,
            object_category_list,
            action_category_list,
            sub_meta_rule_algorithm)

    @filter_args
    @enforce(("read", "write"), "sub_meta_rules")
    def get_sub_meta_rule(self, user_id, intra_extension_id, sub_meta_rule_id):
        sub_meta_rule_dict = self.driver.get_sub_meta_rule_dict(intra_extension_id)
        if sub_meta_rule_id not in sub_meta_rule_dict:
            raise SubMetaRuleUnknown()
        return sub_meta_rule_dict[sub_meta_rule_id]

    @filter_args
    @enforce(("read", "write"), "sub_meta_rules")
    @enforce(("read", "write"), "rule")
    def del_sub_meta_rule(self, user_id, intra_extension_id, sub_meta_rule_id):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rule_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        # TODO (dthom): destroy sub-meta-rule-related rules
        # self.driver.del_rule(intra_extension_id, sub_meta_rule_id, "*")
        return self.driver.del_sub_meta_rule(intra_extension_id, sub_meta_rule_id)

    # Rule functions
    @filter_args
    @enforce("read", "rule")
    def get_rule_dict(self, user_id, intra_extension_id, sub_meta_rule_id):
        """
        :param user_id:
        :param intra_extension_id:
        :param sub_meta_rule_id:
        :return: {
            rule_id1: [subject_scope1, subject_scope2, ..., action_scope1, ..., object_scope1, ... ],
            rule_id2: [subject_scope3, subject_scope4, ..., action_scope3, ..., object_scope3, ... ],
            ...}
        """
        return self.driver.get_rule_dict(intra_extension_id, sub_meta_rule_id)

    @filter_args
    @enforce("read", "sub_meta_rules")
    @enforce(("read", "write"), "rule")
    def add_rule(self, user_id, intra_extension_id, sub_meta_rule_id, rule_list):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rule_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        elif rule_list in self.driver.get_rule_dict(intra_extension_id, sub_meta_rule_id).values():
            raise RuleExisting()
        rule_id = uuid4().hex()
        return self.driver.add_rule(intra_extension_id, sub_meta_rule_id, rule_id, rule_list)

    @filter_args
    @enforce("read", "sub_meta_rules")
    @enforce("read", "rule")
    def get_rule(self, user_id, intra_extension_id, sub_meta_rule_id, rule_id):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rule_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        rule_dict = self.driver.get_rule_dict(intra_extension_id)
        if rule_id not in rule_dict[sub_meta_rule_id]:
            raise RuleUnknown()
        return rule_dict[rule_id]

    @filter_args
    @enforce("read", "sub_meta_rules")
    @enforce(("read", "write"), "rule")
    def del_rule(self, user_id, intra_extension_id, sub_meta_rule_id, rule_id):
        if sub_meta_rule_id not in self.driver.get_sub_meta_rule_dict(intra_extension_id):
            raise SubMetaRuleUnknown()
        rule_dict = self.driver.get_rule_dict(intra_extension_id, sub_meta_rule_id)
        if rule_id not in rule_dict:
            raise RuleUnknown()
        return self.driver.del_rule(intra_extension_id, sub_meta_rule_id, rule_id)


@dependency.provider('authz_api')
@dependency.requires('identity_api', 'tenant_api', 'moonlog_api')
class IntraExtensionAuthzManager(IntraExtensionManager):

    __genre__ = "authz"

    def authz(self, tenant_name, subject_name, object_name, action_name):
        # TODO (dthom) add moon log
        """Check authorization for a particular action.
        :return: True or False or raise an exception
        """
        tenant_id = self.tenant_api.get_tenant_id_from_name(DEFAULT_USER, tenant_name)
        intra_extension_id = self.tenant_api.get_tenant_intra_extension_id(DEFAULT_USER, tenant_id, self.__genre__)
        subject_dict = self.driver.get_subject_dict(intra_extension_id)
        subject_id = None
        for _subject_id in subject_dict:
            if subject_dict[_subject_id]['name'] is subject_name:
                subject_id = _subject_id
        if not subject_id:
            raise SubjectUnknown()
        object_dict = self.driver.get_object_dict(intra_extension_id)
        object_id = None
        for _object_id in object_dict:
            if object_dict[_object_id]['name'] is object_name:
                object_id = _object_id
        if not object_id:
            raise ObjectUnknown()
        action_dict = self.driver.get_action_dict(intra_extension_id)
        action_id = None
        for _action_id in action_dict:
            if action_dict[_action_id] is action_name:
                action_id = _action_id
        if not action_id:
            raise ActionUnknown()
        return super(IntraExtensionAuthzManager, self).authz(intra_extension_id, subject_id, object_id, action_id)

    def del_intra_extension(self, intra_extension_id):
        raise AdminException()

    def set_subject_dict(self, user_id, intra_extension_uuid, subject_dict):
        raise SubjectAddNotAuthorized()

    def add_subject(self, user_id, intra_extension_uuid, subject_name):
        raise SubjectAddNotAuthorized()

    def del_subject(self, user_id, intra_extension_uuid, subject_name):
        raise SubjectDelNotAuthorized()

    def set_object_dict(self, user_id, intra_extension_uuid, object_dict):
        raise ObjectAddNotAuthorized()

    def add_object(self, user_id, intra_extension_uuid, object_name):
        raise ObjectAddNotAuthorized()

    def del_object(self, user_id, intra_extension_uuid, object_uuid):
        raise ObjectDelNotAuthorized()

    def set_action_dict(self, user_id, intra_extension_uuid, action_dict):
        raise ActionAddNotAuthorized()

    def add_action(self, user_id, intra_extension_uuid, action_dict):
        raise ActionAddNotAuthorized()

    def del_action(self, user_id, intra_extension_uuid, action_uuid):
        raise ActionDelNotAuthorized()

    def set_subject_category_dict(self, user_id, intra_extension_uuid, subject_category):
        raise SubjectCategoryAddNotAuthorized()

    def add_subject_category(self, user_id, intra_extension_uuid, subject_category_name):
        raise SubjectCategoryAddNotAuthorized()

    def del_subject_category(self, user_id, intra_extension_uuid, subject_uuid):
        raise SubjectCategoryDelNotAuthorized()

    def set_object_category_dict(self, user_id, intra_extension_uuid, object_category):
        raise ObjectCategoryAddNotAuthorized()

    def add_object_category(self, user_id, intra_extension_uuid, object_category_name):
        raise ObjectCategoryAddNotAuthorized()

    def del_object_category(self, user_id, intra_extension_uuid, object_uuid):
        raise ObjectCategoryDelNotAuthorized()

    def set_action_category_dict(self, user_id, intra_extension_uuid, action_category):
        raise ActionCategoryAddNotAuthorized()

    def add_action_category(self, user_id, intra_extension_uuid, action_category_name):
        raise ActionCategoryAddNotAuthorized()

    def del_action_category(self, user_id, intra_extension_uuid, action_uuid):
        raise ActionCategoryDelNotAuthorized()

    def set_subject_scope_dict(self, user_id, intra_extension_uuid, category, scope):
        raise SubjectCategoryScopeAddNotAuthorized()

    def add_subject_scope(self, user_id, intra_extension_uuid, subject_category, scope_name):
        raise SubjectCategoryScopeAddNotAuthorized()

    def del_subject_scope(self, user_id, intra_extension_uuid, subject_category, subject_category_scope):
        raise SubjectCategoryScopeDelNotAuthorized()

    def set_object_scope_dict(self, user_id, intra_extension_uuid, category, scope):
        raise ObjectCategoryScopeAddNotAuthorized()

    def add_object_scope(self, user_id, intra_extension_uuid, object_category, scope_name):
        raise ObjectCategoryScopeAddNotAuthorized()

    def del_object_scope(self, user_id, intra_extension_uuid, object_category, object_category_scope):
        raise ObjectCategoryScopeDelNotAuthorized()

    def set_action_scope_dict(self, user_id, intra_extension_uuid, category, scope):
        raise ActionCategoryScopeAddNotAuthorized()

    def add_action_scope(self, user_id, intra_extension_uuid, action_category, scope_name):
        raise ActionCategoryScopeAddNotAuthorized()

    def del_action_scope(self, user_id, intra_extension_uuid, action_category, action_category_scope):
        raise ActionCategoryScopeDelNotAuthorized()

    def set_subject_assignment_dict(self, user_id, intra_extension_uuid, subject_uuid, assignment_dict):
        raise SubjectCategoryAssignmentAddNotAuthorized()

    def del_subject_assignment(self, user_id, intra_extension_uuid, subject_uuid, category_uuid, scope_uuid):
        raise SubjectCategoryAssignmentAddNotAuthorized()

    def add_subject_assignment(self, user_id, intra_extension_uuid, subject_uuid, category_uuid, scope_uuid):
        raise SubjectCategoryAssignmentDelNotAuthorized()

    def set_object_category_assignment_dict(self, user_id, intra_extension_uuid, object_uuid, assignment_dict):
        raise ObjectCategoryAssignmentAddNotAuthorized()

    def del_object_assignment(self, user_id, intra_extension_uuid, object_uuid, category_uuid, scope_uuid):
        raise ObjectCategoryAssignmentAddNotAuthorized()

    def add_object_assignment(self, user_id, intra_extension_uuid, object_uuid, category_uuid, scope_uuid):
        raise ObjectCategoryAssignmentDelNotAuthorized()

    def set_action_assignment_dict(self, user_id, intra_extension_uuid, action_uuid, assignment_dict):
        raise ActionCategoryAssignmentAddNotAuthorized()

    def del_action_assignment(self, user_id, intra_extension_uuid, action_uuid, category_uuid, scope_uuid):
        raise ActionCategoryAssignmentAddNotAuthorized()

    def add_action_assignment(self, user_id, intra_extension_uuid, action_uuid, category_uuid, scope_uuid):
        raise ActionCategoryAssignmentDelNotAuthorized()

    def set_aggregation_algorithm(self, user_id, intra_extension_uuid, aggregation_algorithm):
        raise MetaRuleAddNotAuthorized()

    def get_sub_meta_rule(self, user_id, intra_extension_uuid, sub_meta_rules):
        raise MetaRuleAddNotAuthorized()

    def set_sub_rule(self, user_id, intra_extension_uuid, relation, sub_rule):
        raise RuleAddNotAuthorized()

    def del_sub_rule(self, user_id, intra_extension_uuid, relation_name, rule):
        raise RuleAddNotAuthorized()


@dependency.provider('admin_api')
@dependency.requires('identity_api', 'tenant_api', 'moonlog_api')
class IntraExtensionAdminManager(IntraExtensionManager):

    __genre__ = "admin"


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

    def get_tenant_dict(self):
        # TODO: should implement TenantListEmpty exception
        raise exception.NotImplemented()  # pragma: no cover

    def set_tenant(self, tenant_id, tenant_name, intra_authz_ext_id, intra_admin_ext_id):
        # if tenant_id exists, then modify; if the tenant_id not exists, then add the tenant
        # TODO: should implement AddedTenantNameExist exception
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
            data_values = self.get_subject_dict(intra_extension_uuid)["subjects"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise SubjectUnknown()
        elif data_name == self.OBJECT:
            data_values = self.get_object_dict(intra_extension_uuid)["objects"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ObjectUnknown()
        elif data_name == self.ACTION:
            data_values = self.get_action_dict(intra_extension_uuid)["actions"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ActionUnknown()
        elif data_name == self.SUBJECT_CATEGORY:
            data_values = self.get_subject_category_dict(intra_extension_uuid)["subject_categories"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise SubjectCategoryUnknown()
        elif data_name == self.OBJECT_CATEGORY:
            data_values = self.get_object_category_dict(intra_extension_uuid)["object_categories"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ObjectCategoryUnknown()
        elif data_name == self.ACTION_CATEGORY:
            data_values = self.get_action_category_dict(intra_extension_uuid)["action_categories"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ActionCategoryUnknown()
        elif data_name == self.SUBJECT_SCOPE:
            if not category_uuid:
                category_uuid = self.get_uuid_from_name(intra_extension_uuid, category_name, self.SUBJECT_CATEGORY)
            data_values = self.get_subject_category_scope_dict(intra_extension_uuid,
                                                               category_uuid)["subject_category_scope"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise SubjectScopeUnknown()
        elif data_name == self.OBJECT_SCOPE:
            if not category_uuid:
                category_uuid = self.get_uuid_from_name(intra_extension_uuid, category_name, self.OBJECT_CATEGORY)
            data_values = self.get_object_scope_dict(intra_extension_uuid,
                                                              category_uuid)["object_category_scope"]
            if (name and name not in extract_name(data_values)) or \
                (uuid and uuid not in data_values.keys()):
                raise ObjectScopeUnknown()
        elif data_name == self.ACTION_SCOPE:
            if not category_uuid:
                category_uuid = self.get_uuid_from_name(intra_extension_uuid, category_name, self.ACTION_CATEGORY)
            data_values = self.get_action_scope_dict(intra_extension_uuid,
                                                              category_uuid)["action_category_scope"]
            if (name and name not in extract_name(data_values)) or \
                    (uuid and uuid not in data_values.keys()):
                raise ActionScopeUnknown()
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

    def get_intra_extension_dict(self):
        """Get a list of IntraExtension
        :return: {"intra_extension_id": "intra_extension_name", }
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_intra_extension(self, intra_extension_id):
        """Get a description of an IntraExtension
        :param intra_extension_id: the IntraExtension UUID
        :return: {intra_extension_id: intra_extension_name, ...}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_intra_extension(self, intra_extension_id, intra_extension_dict):
        """Set a new IntraExtension

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param intra_extension_dict: a dictionary withe the description of the IntraExtension (see below)
        :type intra_extension_dict: dict
        :return: the IntraExtension dictionary, example:
        {
            "id": "uuid1",
            "name": "Name of the intra_extension",
            "model": "Model of te intra_extension (admin or authz)"
            "description": "a description of the intra_extension"
        }
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_intra_extension(self, intra_extension_id):
        """Delete an IntraExtension

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Metadata functions

    def get_subject_category_dict(self, intra_extension_id):
        """Get a list of all subject categories

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :return: a dictionary containing all subject categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_category_dict(self, intra_extension_id, subject_category_dict):
        """Set the list of all subject categories

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_category_dict: dict of subject categories {"uuid1": "name1", "uuid2": "name2"}
        :type subject_category_dict: dict
        :return: a dictionary containing all subject categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_subject_category(self, intra_extension_id, subject_category_id, subject_category_name):
        """Add a subject category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_category_id: the UUID of the subject category
        :type subject_category_id: string
        :param subject_category_name: the name of the subject category
        :type subject_category_name: string
        :return: a dictionnary with the subject catgory added {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_subject_category(self, intra_extension_id, subject_category_id):
        """Remove one subject category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_category_id: the UUID of subject category to remove
        :type subject_category_id: string
        :return: a dictionary containing all subject categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_object_category_dict(self, intra_extension_id):
        """Get a list of all object categories

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :return: a dictionary containing all object categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_category_dict(self, intra_extension_id, object_category_dict):
        """Set the list of all object categories

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_category_dict: dict of object categories {"uuid1": "name1", "uuid2": "name2"}
        :type object_category_dict: dict
        :return: a dictionary containing all object categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_object_category(self, intra_extension_id, object_category_id, object_category_name):
        """Add a object category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_category_id: the UUID of the object category
        :type object_category_id: string
        :param object_category_name: the name of the object category
        :type object_category_name: string
        :return: a dictionnary with the object catgory added {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_object_category(self, intra_extension_id, object_category_id):
        """Remove one object category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_category_id: the UUID of object category to remove
        :type object_category_id: string
        :return: a dictionary containing all object categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_action_category_dict(self, intra_extension_id):
        """Get a list of all action categories

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :return: a dictionary containing all action categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_category_dict(self, intra_extension_id, action_category_dict):
        """Set the list of all action categories

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_category_dict: dict of action categories {"uuid1": "name1", "uuid2": "name2"}
        :type action_category_dict: dict
        :return: a dictionary containing all action categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_action_category(self, intra_extension_id, action_category_id, action_category_name):
        """Add a action category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_category_id: the UUID of the action category
        :type action_category_id: string
        :param action_category_name: the name of the action category
        :type action_category_name: string
        :return: a dictionnary with the action catgory added {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_action_category(self, intra_extension_id, action_category_id):
        """Remove one action category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_category_id: the UUID of action category to remove
        :type action_category_id: string
        :return: a dictionary containing all action categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    #  Perimeter functions

    def get_subject_dict(self, intra_extension_id):
        """Get the list of subject for that IntraExtension

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :return: a dictionary containing all subjects for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_dict(self, intra_extension_id, subject_dict):
        """Set the list of subject for that IntraExtension

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_dict: dict of subject: {"uuid1": "name1", "uuid2": "name2"}
        :type subject_dict: dict
        :return: a dictionary containing all subjects for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_subject(self, intra_extension_id, subject_id, subject_name):
        """Add a subject

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_id: Subject UUID
        :type subject_id: string
        :param subject_name: Subject name
        :type subject_name: string
        :return: the added subject {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_subject(self, intra_extension_id, subject_id):
        """Remove a subject

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_id: Subject UUID
        :type subject_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_object_dict(self, intra_extension_id):
        """Get the list of object for that IntraExtension

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :return: a dictionary containing all objects for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_dict(self, intra_extension_id, object_dict):
        """Set the list of object for that IntraExtension

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_dict: dict of object: {"uuid1": "name1", "uuid2": "name2"}
        :type object_dict: dict
        :return: a dictionary containing all objects for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_object(self, intra_extension_id, object_id, object_name):
        """Ad an object

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_id: Object UUID
        :type object_id: string
        :param object_name: Object name
        :type object_name: string
        :return: the added object {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_object(self, intra_extension_id, object_id):
        """Remove an object

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_id: Object UUID
        :type object_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_action_dict(self, intra_extension_id):
        """ Get the list of action for that IntraExtension

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :return: a dictionary containing all actions for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_dict(self, intra_extension_id, action_dict):
        """ Set the list of action for that IntraExtension

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_dict: dict of actions: {"uuid1": "name1", "uuid2": "name2"}
        :type action_dict: dict
        :return: a dictionary containing all actions for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_action(self, intra_extension_id, action_id, action_name):
        """Ad an action

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_id: Action UUID
        :type action_id: string
        :param action_name: Action name
        :type action_name: string
        :return: the added action {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_action(self, intra_extension_id, action_id):
        """Remove an action

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_id: Action UUID
        :type action_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Scope functions

    def get_subject_scope_dict(self, intra_extension_id, subject_category_id):
        """Get a list of all subject category scope

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_category_id: the category UUID where the scope values are
        :type subject_category_id: string
        :return: a dictionary containing all subject category scope {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_scope_dict(self, intra_extension_id, subject_category_id, subject_scope_dict):
        """Set the list of all scope for that subject category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_category_id: the UUID of the subject category where this scope will be set
        :type subject_category_id: string
        :return: a dictionary containing all scope {"scope_uuid1": "scope_name1, "scope_uuid2": "scope_name2}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_subject_scope(self, intra_extension_id, subject_category_id, subject_scope_id, subject_scope_name):
        """Add a subject category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_category_id: the subject category UUID where the scope will be added
        :type subject_category_id: string
        :param subject_scope_id: the UUID of the subject category
        :type subject_scope_id: string
        :param subject_scope_name: the name of the subject category
        :type subject_scope_name: string
        :return: a dictionary containing the subject category scope added {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_subject_scope(self, intra_extension_id, subject_category_id, subject_scope_id):
        """Remove one scope belonging to a subject category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_category_id: the UUID of subject categorywhere we can find the scope to remove
        :type subject_category_id: string
        :param subject_scope_id: the UUID of the scope to remove
        :type subject_scope_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_object_scope_dict(self, intra_extension_id, object_category_id):
        """Get a list of all object category scope

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_category_id: the category UUID where the scope values are
        :type object_category_id: string
        :return: a dictionary containing all object category scope {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_scope_dict(self, intra_extension_id, object_category_id, object_scope_dict):
        """Set the list of all scope for that object category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_category_id: the UUID of the object category where this scope will be set
        :type object_category_id: string
        :return: a dictionary containing all scope {"scope_uuid1": "scope_name1, "scope_uuid2": "scope_name2}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_object_scope(self, intra_extension_id, object_category_id, object_scope_id, object_scope_name):
        """Add a object category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_category_id: the object category UUID where the scope will be added
        :type object_category_id: string
        :param object_scope_id: the UUID of the object category
        :type object_scope_id: string
        :param object_scope_name: the name of the object category
        :type object_scope_name: string
        :return: a dictionary containing the object category scope added {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_object_scope(self, intra_extension_id, object_category_id, object_scope_id):
        """Remove one scope belonging to a object category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_category_id: the UUID of object categorywhere we can find the scope to remove
        :type object_category_id: string
        :param object_scope_id: the UUID of the scope to remove
        :type object_scope_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_action_scope_dict(self, intra_extension_id, action_category_id):
        """Get a list of all action category scope

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_category_id: the category UUID where the scope values are
        :type action_category_id: string
        :return: a dictionary containing all action category scope {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_scope_dict(self, intra_extension_id, action_category_id, action_scope_id):
        """Set the list of all scope for that action category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_category_id: the UUID of the action category where this scope will be set
        :type action_category_id: string
        :return: a dictionary containing all scope {"scope_uuid1": "scope_name1, "scope_uuid2": "scope_name2}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_action_scope(self, intra_extension_id, action_category_id, action_scope_id, action_scope_name):
        """Add a action category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_category_id: the action category UUID where the scope will be added
        :type action_category_id: string
        :param action_scope_id: the UUID of the action category
        :type action_scope_id: string
        :param action_scope_name: the name of the action category
        :type action_scope_name: string
        :return: a dictionary containing the action category scope added {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_action_scope(self, intra_extension_id, action_category_id, action_scope_id):
        """Remove one scope belonging to a action category

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_category_id: the UUID of action categorywhere we can find the scope to remove
        :type action_category_id: string
        :param action_scope_id: the UUID of the scope to remove
        :type action_scope_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Assignment functions

    def get_subject_assignment_dict(self, intra_extension_id, subject_id):
        """Get the assignment for a given subject_uuid

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_id: subject UUID
        :type subject_id: string
        :return: a dictionary of assignment for the given subject {"cat1": ["scope_uuid1", "scope_uuid2"]}
        :raises: IntraExtensionNotFound, SubjectUnknown, SubjectCategoryAssignmentUnknown, SubjectCategoryAssignmentOutOfScope
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_assignment_dict(self, intra_extension_id, subject_id, subject_assignment_dict):
        """Set the assignment for a given subject_uuid

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_id: subject UUID
        :type subject_id: string
        :param subject_assignment_dict: the assignment dictionary {"cat1": ["scope_uuid1", "scope_uuid2"]}
        :type subject_assignment_dict: dict
        :return: a dictionary of assignment for the given subject {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_subject_assignment(self, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        """Add a scope to a category and to a subject

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_id: the subject UUID
        :type subject_id: string
        :param subject_category_id: the category UUID
        :type subject_category_id: string
        :param subject_scope_id: the scope UUID
        :type subject_scope_id: string
        :return: a dictionary of assignment for the given subject {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_subject_assignment(self, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        """Remove a scope from a category and from a subject

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param subject_id: the subject UUID
        :type subject_id: string
        :param subject_category_id: the category UUID
        :type subject_category_id: string
        :param subject_scope_id: the scope UUID
        :type subject_scope_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_object_assignment_dict(self, intra_extension_id, object_id):
        """Get the assignment for a given object_uuid

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_id: object UUID
        :type object_id: string
        :return: a dictionary of assignment for the given object {"cat1": ["scope_uuid1", "scope_uuid2"]}
        :raises: IntraExtensionNotFound, ObjectUnknown, ObjectCategoryAssignmentUnknown, ObjectCategoryAssignmentOutOfScope
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_assignment_dict(self, intra_extension_id, object_id, object_assignment_dict):
        """Set the assignment for a given object_uuid

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_id: object UUID
        :type object_id: string
        :param object_assignment_dict: the assignment dictionary {"cat1": ["scope_uuid1", "scope_uuid2"]}
        :type object_assignment_dict: dict
        :return: a dictionary of assignment for the given object {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_object_assignment(self, intra_extension_id, object_id, object_category_id, object_scope_id):
        """Add a scope to a category and to a object

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_id: the object UUID
        :type object_id: string
        :param object_category_id: the category UUID
        :type object_category_id: string
        :param object_scope_id: the scope UUID
        :type object_scope_id: string
        :return: a dictionary of assignment for the given object {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_object_assignment(self, intra_extension_id, object_id, object_category_id, object_scope_id):
        """Remove a scope from a category and from a object

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param object_id: the object UUID
        :type object_id: string
        :param object_category_id: the category UUID
        :type object_category_id: string
        :param object_scope_id: the scope UUID
        :type object_scope_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_action_assignment_dict(self, intra_extension_id, action_id):
        """Get the assignment for a given action_uuid

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_id: action UUID
        :type action_id: string
        :return: a dictionary of assignment for the given action {"cat1": ["scope_uuid1", "scope_uuid2"]}
        :raises: IntraExtensionNotFound, ActionUnknown, ActionCategoryAssignmentUnknown, ActionCategoryAssignmentOutOfScope
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_assignment_dict(self, intra_extension_id, action_id, action_assignment_dict):
        """Set the assignment for a given action_uuid

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_id: action UUID
        :type action_id: string
        :param action_assignment_dict: the assignment dictionary {"cat1": ["scope_uuid1", "scope_uuid2"]}
        :type action_assignment_dict: dict
        :return: a dictionary of assignment for the given action {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_action_assignment(self, intra_extension_id, action_id, action_category_id, action_scope_id):
        """Add a scope to a category and to a action

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_id: the action UUID
        :type action_id: string
        :param action_category_id: the category UUID
        :type action_category_id: string
        :param action_scope_id: the scope UUID
        :type action_scope_id: string
        :return: a dictionary of assignment for the given action {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def del_action_assignment(self, intra_extension_id, action_id, action_category_id, action_scope_id):
        """Remove a scope from a category and from a action

        :param intra_extension_id: IntraExtension UUID
        :type intra_extension_id: string
        :param action_id: the action UUID
        :type action_id: string
        :param action_category_id: the category UUID
        :type action_category_id: string
        :param action_scope_id: the scope UUID
        :type action_scope_id: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Meta_rule functions

    def get_meta_rule_dict(self, extension_uuid):
        """Get the Meta rule

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :return: a dictionary containing the meta_rule

        Here is an example of a meta_rule:
        {
          "sub_meta_rules": {
            "relation_super": {
              "subject_categories": ["role"],
              "action_categories": ["computing_action"],
              "object_categories": ["id"],
              "relation": "relation_super"
            }
          },
          "aggregation": "and_true_aggregation"
        }
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_meta_rule_dict(self, extension_uuid, meta_rule_dict):
        """Set the Meta rule

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param meta_rule: a dictionary representing the meta_rule (see below)
        :return:a dictionary containing the meta_rule

        Here is an example of a meta_rule:
        {
          "sub_meta_rules": {
            "relation_super": {
              "subject_categories": ["role"],
              "action_categories": ["computing_action"],
              "object_categories": ["id"],
              "relation": "relation_super"
            }
          },
          "aggregation": "and_true_aggregation"
        }
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Rule functions

    def get_rule_dict(self, extension_uuid):
        """Get all rules

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :return: a dictionary containing rules ie.
        {
            "relation_super":[
            ["admin", "vm_admin", "servers", True],
            ["admin", "vm_access", "servers", True]
            ]
        }
        All items will be UUID.
        The last boolean item is the positive/negative value. If True, request that conforms to that rule
        will be authorized, if false, request will be rejected.
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_rule_dict(self, extension_uuid, rule_dict):
        """Set all rules

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param rules: a dictionary containing rules (see below)
        :type rules: dict
        :return: a dictionary containing rules ie.
        {
            "relation_super":[
            ["admin", "vm_admin", "servers", True],
            ["admin", "vm_access", "servers", True]
            ]
        }
        All items will be UUID.
        The last boolean item is the positive/negative value. If True, request that conforms to that rule
        will be authorized, if false, request will be rejected.
        """
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

