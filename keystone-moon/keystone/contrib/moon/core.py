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

_OPTS = [
    cfg.StrOpt('authz_driver',
               default='keystone.contrib.moon.backends.flat.SuperExtensionConnector',
               help='Authorisation backend driver.'),
    cfg.StrOpt('log_driver',
               default='keystone.contrib.moon.backends.flat.LogConnector',
               help='Logs backend driver.'),
    cfg.StrOpt('superextension_driver',
               default='keystone.contrib.moon.backends.flat.SuperExtensionConnector',
               help='SuperExtension backend driver.'),
    cfg.StrOpt('intraextension_driver',
               default='keystone.contrib.moon.backends.sql.IntraExtensionConnector',
               help='IntraExtension backend driver.'),
    cfg.StrOpt('tenant_driver',
               default='keystone.contrib.moon.backends.sql.TenantConnector',
               help='Tenant backend driver.'),
    cfg.StrOpt('interextension_driver',
               default='keystone.contrib.moon.backends.sql.InterExtensionConnector',
               help='InterExtension backend driver.'),
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
                            intra_extension_uuid,
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


@dependency.provider('tenant_api')
@dependency.requires('moonlog_api')
class TenantManager(manager.Manager):

    def __init__(self):
        super(TenantManager, self).__init__(CONF.moon.tenant_driver)

    def get_tenant_dict(self):
        """
        Return a dictionnary with all tenants
        :return: dict
        """
        try:
            return self.driver.get_tenant_dict()
        except TenantListEmpty:
            self.moonlog_api.error(_("Tenant Mapping list is empty."))
            return {}

    def get_tenant_name(self, tenant_uuid):
        _tenant_dict = self.get_tenant_dict()
        if tenant_uuid not in _tenant_dict:
            raise TenantNotFound(_("Tenant UUID ({}) was not found.".format(tenant_uuid)))
        return _tenant_dict[tenant_uuid]["name"]

    def set_tenant_name(self, tenant_uuid, tenant_name):
        _tenant_dict = self.get_tenant_dict()
        if tenant_uuid not in _tenant_dict:
            raise TenantNotFound(_("Tenant UUID ({}) was not found.".format(tenant_uuid)))
        _tenant_dict[tenant_uuid]['name'] = tenant_name
        return self.driver.set_tenant_dict(_tenant_dict)

    def get_extension_uuid(self, tenant_uuid, scope="authz"):
        """
        Return the UUID of the scoped extension for a particular tenant.
        :param tenant_uuid: UUID of the tenant
        :param scope: "admin" or "authz"
        :return (str): the UUID of the scoped extension
        """
        # 1 tenant only with 1 authz extension and 1 admin extension
        _tenant_dict = self.get_tenant_dict()
        if tenant_uuid not in _tenant_dict:
            raise TenantNotFound(_("Tenant UUID ({}) was not found.".format(tenant_uuid)))
        if not _tenant_dict[tenant_uuid][scope]:
            raise IntraExtensionNotFound(_("No IntraExtension found for Tenant {}.".format(tenant_uuid)))
        return _tenant_dict[tenant_uuid][scope]

    def get_tenant_uuid(self, extension_uuid):
        for _tenant_uuid, _tenant_value in six.iteritems(self.get_tenant_dict()):
            if extension_uuid == _tenant_value["authz"] or extension_uuid == _tenant_value["admin"]:
                return _tenant_uuid
        raise TenantNotFound()

    def get_admin_extension_uuid(self, authz_extension_uuid):
        _tenants = self.get_tenant_dict()
        for _tenant_uuid in _tenants:
            if authz_extension_uuid == _tenants[_tenant_uuid]['authz']and _tenants[_tenant_uuid]['admin']:
                    return _tenants[_tenant_uuid]['admin']
        self.moonlog_api.error(_("No IntraExtension found mapping this Authz IntraExtension: {}.".format(
                               authz_extension_uuid)))
        # FIXME (dthom): if AdminIntraExtensionNotFound, maybe we can add an option in configuration file
        # to allow or not the fact that Admin IntraExtension can be None
        # raise AdminIntraExtensionNotFound()

    def delete(self, authz_extension_uuid):
        _tenants = self.get_tenant_dict()
        for _tenant_uuid in _tenants:
            if authz_extension_uuid == _tenants[_tenant_uuid]['authz']:
                return self.set_tenant_dict(_tenant_uuid, "", "", "")
        raise AuthzIntraExtensionNotFound(_("No IntraExtension found mapping this Authz IntraExtension: {}.".format(
            authz_extension_uuid)))

    def set_tenant_dict(self, tenant_uuid, name, authz_extension_uuid, admin_extension_uuid):
        tenant = {
            tenant_uuid: {
                "name": name,
                "authz": authz_extension_uuid,
                "admin": admin_extension_uuid
            }
        }
        # TODO (dthom): Tenant must be checked against Keystone database.
        return self.driver.set_tenant_dict(tenant)


class TenantDriver:

    def get_tenant_dict(self):
        raise exception.NotImplemented()  # pragma: no cover

    def set_tenant_dict(self, tenant):
        raise exception.NotImplemented()  # pragma: no cover


@dependency.requires('identity_api', 'moonlog_api', 'tenant_api', 'authz_api', 'admin_api')
class IntraExtensionManager(manager.Manager):

    __genre__ = None

    def __init__(self):
        driver = CONF.moon.intraextension_driver
        super(IntraExtensionManager, self).__init__(driver)

    def __get_authz_buffer(self, intra_extension_uuid, subject_uuid, object_uuid, action_uuid):
        """
        :param intra_extension_uuid:
        :param subject_uuid:
        :param object_uuid:
        :param action_uuid:
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

        if not self.driver.get_intra_extension(intra_extension_uuid):
            raise IntraExtensionNotFound()

        _authz_buffer = dict()
        _authz_buffer['subject_uuid'] = subject_uuid
        _authz_buffer['object_uuid'] = object_uuid
        _authz_buffer['action_uuid'] = action_uuid

        try:
            _meta_data_dict = self.driver.get_meta_data_dict(intra_extension_uuid)
            _subject_assignment_dict = self.driver.get_subject_category_assignment_dict(intra_extension_uuid, subject_uuid)
            _object_assignment_dict = self.driver.get_object_category_assignment_dict(intra_extension_uuid, object_uuid)
            _action_assignment_dict = self.driver.get_action_category_assignment_dict(intra_extension_uuid, action_uuid)
        except exception:  # Execption for ItemUnknow, ItemCategoryAssignmentOutOfScope, ItemCategoryAssignmentUnknown
             pass

        _authz_buffer['subject_attributes'] = dict()
        _authz_buffer['object_attributes'] = dict()
        _authz_buffer['action_attributes'] = dict()

        for _subject_category in _meta_data_dict['subject_categories']:
            _authz_buffer['subject_attributes'][_subject_category] = _subject_assignment_dict[_subject_category]
        for _object_category in _meta_data_dict['object_categories']:
            _authz_buffer['object_attributes'][_object_category] = _object_assignment_dict[_object_category]
        for _action_category in _meta_data_dict['action_categories']:
            _authz_buffer['action_attributes'][_action_category] = _action_assignment_dict[_action_category]

        return _authz_buffer

    def authz(self, intra_extension_uuid, subject_uuid, object_uuid, action_uuid):
        """Check authorization for a particular action.

        :param intra_extension_uuid: UUID of an IntraExtension
        :param subject_uuid: subject UUID of the request
        :param object_uuid: object UUID of the request
        :param action_uuid: action UUID of the request
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

        _authz_buffer = self.__get_authz_buffer(intra_extension_uuid, subject_uuid, object_uuid, action_uuid)
        _decision_buffer = dict()

        try:
            _meta_rule_dict = self.driver.get_meta_rule_dict(intra_extension_uuid)
            _rule_dict = self.driver.get_rule_dict(intra_extension_uuid)
        except exception:  # Execption for rule
             pass

        for _rule in _meta_rule_dict['sub_meta_rules']:
            if _meta_rule_dict['sub_meta_rules'][_rule]['algorithm'] == 'inclusion':
                _decision_buffer[_rule] = algo_inclusion(_authz_buffer, _meta_rule_dict['sub_meta_rules'][_rule], _rule_dict[_rule])
            elif _meta_rule_dict['sub_meta_rules'][_rule]['algorithm'] == 'comparison':
                _decision_buffer[_rule] = algo_comparison(_authz_buffer, _meta_rule_dict['sub_meta_rules'][_rule], _rule_dict[_rule])

        if _meta_rule_dict['aggregation'] == 'all_true':
            return aggr_all_true(_decision_buffer)

        return False

    def __get_key_from_value(self, value, values_dict):
        return filter(lambda v: v[1] == value, values_dict.iteritems())[0][0]

    def get_intra_extension_list(self):
        # TODO: check will be done through super_extension later
        return self.driver.get_intra_extension_list()

    def get_intra_extension_id_for_tenant(self, tenant_id):
        for intra_extension_id in self.driver.get_intra_extension_list():
            if self.driver.get_intra_extension(intra_extension_id)["tenant"] == tenant_id:
                return intra_extension_id
        LOG.error("IntraExtension not found for tenant {}".format(tenant_id))
        raise exception.NotFound

    def get_intra_extension(self, uuid):
        return self.driver.get_intra_extension(uuid)

    def set_perimeter_values(self, ie, policy_dir):

        perimeter_path = os.path.join(policy_dir, 'perimeter.json')
        f = open(perimeter_path)
        json_perimeter = json.load(f)

        subject_dict = dict()
        # We suppose that all subjects can be mapped to a true user in Keystone
        for _subject in json_perimeter['subjects']:
            user = self.identity_api.get_user_by_name(_subject, "default")
            subject_dict[user["id"]] = user["name"]
        self.driver.set_subject_dict(ie["id"], subject_dict)
        ie["subjects"] = subject_dict

        # Copy all values for objects and subjects
        object_dict = dict()
        for _object in json_perimeter['objects']:
            object_dict[uuid4().hex] = _object
        self.driver.set_object_dict(ie["id"], object_dict)
        ie["objects"] = object_dict

        action_dict = dict()
        for _action in json_perimeter['actions']:
            action_dict[uuid4().hex] = _action
        self.driver.set_action_dict(ie["id"], action_dict)
        ie["ations"] = action_dict

    def set_metadata_values(self, ie, policy_dir):

        metadata_path = os.path.join(policy_dir, 'metadata.json')
        f = open(metadata_path)
        json_perimeter = json.load(f)

        subject_categories_dict = dict()
        for _cat in json_perimeter['subject_categories']:
            subject_categories_dict[uuid4().hex] = _cat
        self.driver.set_subject_category_dict(ie["id"], subject_categories_dict)
        # Initialize scope categories
        for _cat in subject_categories_dict.keys():
            self.driver.set_subject_category_scope_dict(ie["id"], _cat, {})
        ie['subject_categories'] = subject_categories_dict

        object_categories_dict = dict()
        for _cat in json_perimeter['object_categories']:
            object_categories_dict[uuid4().hex] = _cat
        self.driver.set_object_category_dict(ie["id"], object_categories_dict)
        # Initialize scope categories
        for _cat in object_categories_dict.keys():
            self.driver.set_object_category_scope_dict(ie["id"], _cat, {})
        ie['object_categories'] = object_categories_dict

        action_categories_dict = dict()
        for _cat in json_perimeter['action_categories']:
            action_categories_dict[uuid4().hex] = _cat
        self.driver.set_action_category_dict(ie["id"], action_categories_dict)
        # Initialize scope categories
        for _cat in action_categories_dict.keys():
            self.driver.set_action_category_scope_dict(ie["id"], _cat, {})
        ie['action_categories'] = action_categories_dict

    def set_scope_values(self, ie, policy_dir):

        metadata_path = os.path.join(policy_dir, 'scope.json')
        f = open(metadata_path)
        json_perimeter = json.load(f)

        ie['subject_category_scope'] = dict()
        for category, scope in json_perimeter["subject_category_scope"].iteritems():
            category = self.__get_key_from_value(
                category,
                self.driver.get_subject_category_dict(ie["id"])["subject_categories"])
            _scope_dict = dict()
            for _scope in scope:
                _scope_dict[uuid4().hex] = _scope
            self.driver.set_subject_category_scope_dict(ie["id"], category, _scope_dict)
            ie['subject_category_scope'][category] = _scope_dict

        ie['object_category_scope'] = dict()
        for category, scope in json_perimeter["object_category_scope"].iteritems():
            category = self.__get_key_from_value(
                category,
                self.driver.get_object_category_dict(ie["id"])["object_categories"])
            _scope_dict = dict()
            for _scope in scope:
                _scope_dict[uuid4().hex] = _scope
            self.driver.set_object_category_scope_dict(ie["id"], category, _scope_dict)
            ie['object_category_scope'][category] = _scope_dict

        ie['action_category_scope'] = dict()
        for category, scope in json_perimeter["action_category_scope"].iteritems():
            category = self.__get_key_from_value(
                category,
                self.driver.get_action_category_dict(ie["id"])["action_categories"])
            _scope_dict = dict()
            for _scope in scope:
                _scope_dict[uuid4().hex] = _scope
            self.driver.set_action_category_scope_dict(ie["id"], category, _scope_dict)
            ie['action_category_scope'][category] = _scope_dict

    def set_assignments_values(self, ie, policy_dir):

        f = open(os.path.join(policy_dir, 'assignment.json'))
        json_assignments = json.load(f)

        subject_assignments = dict()
        for category, value in json_assignments['subject_assignments'].iteritems():
            category = self.__get_key_from_value(
                category,
                self.driver.get_subject_category_dict(ie["id"])["subject_categories"])
            for user in value:
                if user not in subject_assignments:
                    subject_assignments[user] = dict()
                    subject_assignments[user][category] = \
                        map(lambda x: self.__get_key_from_value(x, ie['subject_category_scope'][category]), value[user])
                else:
                    subject_assignments[user][category].extend(
                        map(lambda x: self.__get_key_from_value(x, ie['subject_category_scope'][category]), value[user])
                    )
        # Note (dthom): subject_category_assignment must be initialized because when there is no data in json
        # we will not go through the for loop
        self.driver.set_subject_category_assignment_dict(ie["id"])
        for subject in subject_assignments:
            self.driver.set_subject_category_assignment_dict(ie["id"], subject, subject_assignments[subject])

        object_assignments = dict()
        for category, value in json_assignments["object_assignments"].iteritems():
            category = self.__get_key_from_value(
                category,
                self.driver.get_object_category_dict(ie["id"])["object_categories"])
            for object_name in value:
                if object_name not in object_assignments:
                    object_assignments[object_name] = dict()
                    object_assignments[object_name][category] = \
                        map(lambda x: self.__get_key_from_value(x, ie['object_category_scope'][category]),
                            value[object_name])
                else:
                    object_assignments[object_name][category].extend(
                        map(lambda x: self.__get_key_from_value(x, ie['object_category_scope'][category]),
                            value[object_name])
                    )
        # Note (dthom): object_category_assignment must be initialized because when there is no data in json
        # we will not go through the for loop
        self.driver.set_object_category_assignment_dict(ie["id"])
        for object in object_assignments:
            self.driver.set_object_category_assignment_dict(ie["id"], object, object_assignments[object])

        action_assignments = dict()
        for category, value in json_assignments["action_assignments"].iteritems():
            category = self.__get_key_from_value(
                category,
                self.driver.get_action_category_dict(ie["id"])["action_categories"])
            for action_name in value:
                if action_name not in action_assignments:
                    action_assignments[action_name] = dict()
                    action_assignments[action_name][category] = \
                        map(lambda x: self.__get_key_from_value(x, ie['action_category_scope'][category]),
                            value[action_name])
                else:
                    action_assignments[action_name][category].extend(
                        map(lambda x: self.__get_key_from_value(x, ie['action_category_scope'][category]),
                            value[action_name])
                    )
        # Note (dthom): action_category_assignment must be initialized because when there is no data in json
        # we will not go through the for loop
        self.driver.set_action_category_assignment_dict(ie["id"])
        for action in action_assignments:
            self.driver.set_action_category_assignment_dict(ie["id"], action, action_assignments[action])

    def set_metarule_values(self, ie, policy_dir):

        metadata_path = os.path.join(policy_dir, 'metarule.json')
        f = open(metadata_path)
        json_metarule = json.load(f)
        # ie["meta_rules"] = copy.deepcopy(json_metarule)
        metarule = dict()
        categories = {
            "subject_categories": self.driver.get_subject_category_dict(ie["id"]),
            "object_categories": self.driver.get_object_category_dict(ie["id"]),
            "action_categories": self.driver.get_action_category_dict(ie["id"])
        }
        # Translate value from JSON file to UUID for Database
        for relation in json_metarule["sub_meta_rules"]:
            metarule[relation] = dict()
            for item in ("subject_categories", "object_categories", "action_categories"):
                metarule[relation][item] = list()
                for element in json_metarule["sub_meta_rules"][relation][item]:
                    metarule[relation][item].append(self.__get_key_from_value(
                        element,
                        categories[item][item]
                    ))
        submetarules = {
            "aggregation": json_metarule["aggregation"],
            "sub_meta_rules": metarule
        }
        self.driver.set_meta_rule_dict(ie["id"], submetarules)

    def set_subrules_values(self, ie, policy_dir):

        metadata_path = os.path.join(policy_dir, 'rules.json')
        f = open(metadata_path)
        json_rules = json.load(f)
        ie["sub_rules"] = {"rules": copy.deepcopy(json_rules)}
        # Translate value from JSON file to UUID for Database
        rules = dict()
        sub_meta_rules = self.driver.get_meta_rule_dict(ie["id"])
        for relation in json_rules:
            if relation not in self.get_sub_meta_rule_relations("admin", ie["id"])["sub_meta_rule_relations"]:
                raise IntraExtensionError("Bad relation name {} in rules".format(relation))
            rules[relation] = list()
            for rule in json_rules[relation]:
                subrule = list()
                for cat, cat_func in (
                    ("subject_categories", self.driver.get_subject_category_scope_dict),
                    ("action_categories", self.driver.get_action_category_scope_dict),
                    ("object_categories", self.driver.get_object_category_scope_dict),
                ):
                    for cat_value in sub_meta_rules["sub_meta_rules"][relation][cat]:
                        scope = cat_func(
                            ie["id"],
                            cat_value
                        )[cat_func.__name__.replace("get_", "").replace("_dict", "")]

                        _ = rule.pop(0)
                        a_scope = self.__get_key_from_value(_, scope[cat_value])
                        subrule.append(a_scope)
                # if a positive/negative value exists, all titem of rule have not be consumed
                if len(rule) >= 1 and type(rule[0]) is bool:
                    subrule.append(rule[0])
                else:
                    # if value doesn't exist add a default value
                    subrule.append(True)
                rules[relation].append(subrule)
        self.driver.set_rules(ie["id"], rules)

    def load_intra_extension(self, intra_extension):
        ie = dict()
        # TODO: clean some values
        ie['id'] = uuid4().hex
        ie["name"] = filter_input(intra_extension["name"])
        ie["model"] = filter_input(intra_extension["policymodel"])
        ie["description"] = filter_input(intra_extension["description"])
        ref = self.driver.set_intra_extension(ie['id'], ie)
        self.moonlog_api.debug("Creation of IE: {}".format(ref))
        # read the profile given by "policymodel" and populate default variables
        policy_dir = os.path.join(CONF.moon.policy_directory, ie["model"])
        self.set_perimeter_values(ie, policy_dir)
        self.set_metadata_values(ie, policy_dir)
        self.set_scope_values(ie, policy_dir)
        self.set_assignments_values(ie, policy_dir)
        self.set_metarule_values(ie, policy_dir)
        self.set_subrules_values(ie, policy_dir)
        return ref

    def delete_intra_extension(self, intra_extension_id):
        ref = self.driver.delete_intra_extension(intra_extension_id)
        return ref

    # Perimeter functions

    @filter_args
    @enforce("read", "subjects")
    def get_subject_dict(self, user_uuid, intra_extension_uuid):
        return self.driver.get_subject_dict(intra_extension_uuid)

    @filter_args
    @enforce(("read", "write"), "subjects")
    def set_subject_dict(self, user_uuid, intra_extension_uuid, subject_dict):
        for uuid in subject_dict:
            # Next line will raise an error if user is not present in Keystone database
            self.identity_api.get_user(uuid)
        return self.driver.set_subject_dict(intra_extension_uuid, subject_dict)

    @filter_args
    @enforce(("read", "write"), "subjects")
    def add_subject_dict(self, user_uuid, intra_extension_uuid, subject_uuid):
        # Next line will raise an error if user is not present in Keystone database
        user = self.identity_api.get_user(subject_uuid)
        return self.driver.add_subject(intra_extension_uuid, subject_uuid, user["name"])

    @filter_args
    @enforce("write", "subjects")
    def del_subject(self, user_uuid, intra_extension_uuid, subject_uuid):
        self.driver.remove_subject(intra_extension_uuid, subject_uuid)

    @filter_args
    @enforce("read", "objects")
    def get_object_dict(self, user_uuid, intra_extension_uuid):
        return self.driver.get_object_dict(intra_extension_uuid)

    @filter_args
    @enforce(("read", "write"), "objects")
    def set_object_dict(self, user_uuid, intra_extension_uuid, object_dict):
        return self.driver.set_object_dict(intra_extension_uuid, object_dict)

    @filter_args
    @enforce(("read", "write"), "objects")
    def add_object_dict(self, user_uuid, intra_extension_uuid, object_name):
        object_uuid = uuid4().hex
        return self.driver.add_object(intra_extension_uuid, object_uuid, object_name)

    @filter_args
    @enforce("write", "objects")
    def del_object(self, user_uuid, intra_extension_uuid, object_uuid):
        self.driver.remove_object(intra_extension_uuid, object_uuid)

    @filter_args
    @enforce("read", "actions")
    def get_action_dict(self, user_uuid, intra_extension_uuid):
        return self.driver.get_action_dict(intra_extension_uuid)

    @filter_args
    @enforce(("read", "write"), "actions")
    def set_action_dict(self, user_uuid, intra_extension_uuid, action_dict):
        return self.driver.set_action_dict(intra_extension_uuid, action_dict)

    @filter_args
    @enforce(("read", "write"), "actions")
    def add_action_dict(self, user_uuid, intra_extension_uuid, action_name):
        action_uuid = uuid4().hex
        return self.driver.add_action(intra_extension_uuid, action_uuid, action_name)

    @filter_args
    @enforce("write", "actions")
    def del_action(self, user_uuid, intra_extension_uuid, action_uuid):
        self.driver.remove_action(intra_extension_uuid, action_uuid)

    # Metadata functions

    @filter_args
    @enforce("read", "subject_categories")
    def get_subject_category_dict(self, user_uuid, intra_extension_uuid):
        return self.driver.get_subject_category_dict(intra_extension_uuid)

    @filter_args
    @enforce("read", "subject_categories")
    @enforce("read", "subject_category_scope")
    @enforce("write", "subject_category_scope")
    def set_subject_category_dict(self, user_uuid, intra_extension_uuid, subject_category):
        subject_category_dict = self.driver.set_subject_category_dict(intra_extension_uuid, subject_category)
        # if we add a new category, we must add it to the subject_category_scope
        for _cat in subject_category.keys():
            try:
                _ = self.driver.get_subject_category_scope_dict(intra_extension_uuid, _cat)
            except AuthzMetadata:
                self.driver.set_subject_category_scope_dict(intra_extension_uuid, _cat, {})
        return subject_category_dict

    @filter_args
    @enforce("read", "subject_categories")
    @enforce("write", "subject_categories")
    def add_subject_category_dict(self, user_uuid, intra_extension_uuid, subject_category_name):
        subject_category_uuid = uuid4().hex
        return self.driver.add_subject_category_dict(intra_extension_uuid, subject_category_uuid, subject_category_name)

    @filter_args
    @enforce("write", "subject_categories")
    def del_subject_category(self, user_uuid, intra_extension_uuid, subject_uuid):
        return self.driver.remove_subject_category(intra_extension_uuid, subject_uuid)

    @filter_args
    @enforce("read", "object_categories")
    def get_object_category_dict(self, user_uuid, intra_extension_uuid):
        return self.driver.get_object_category_dict(intra_extension_uuid)

    @filter_args
    @enforce("read", "object_categories")
    @enforce("read", "object_category_scope")
    @enforce("write", "object_category_scope")
    def set_object_category_dict(self, user_uuid, intra_extension_uuid, object_category):
        object_category_dict = self.driver.set_object_category_dict(intra_extension_uuid, object_category)
        # if we add a new category, we must add it to the object_category_scope
        for _cat in object_category.keys():
            try:
                _ = self.driver.get_object_category_scope_dict(intra_extension_uuid, _cat)
            except AuthzMetadata:
                self.driver.set_object_category_scope_dict(intra_extension_uuid, _cat, {})
        return object_category_dict

    @filter_args
    @enforce("read", "object_categories")
    @enforce("write", "object_categories")
    def add_object_category_dict(self, user_uuid, intra_extension_uuid, object_category_name):
        object_category_uuid = uuid4().hex
        return self.driver.add_object_category_dict(intra_extension_uuid, object_category_uuid, object_category_name)

    @filter_args
    @enforce("write", "object_categories")
    def del_object_category(self, user_uuid, intra_extension_uuid, object_uuid):
        return self.driver.remove_object_category(intra_extension_uuid, object_uuid)

    @filter_args
    @enforce("read", "action_categories")
    def get_action_category_dict(self, user_uuid, intra_extension_uuid):
        return self.driver.get_action_category_dict(intra_extension_uuid)

    @filter_args
    @enforce("read", "action_categories")
    @enforce("read", "action_category_scope")
    @enforce("write", "action_category_scope")
    def set_action_category_dict(self, user_uuid, intra_extension_uuid, action_category):
        action_category_dict = self.driver.set_action_category_dict(intra_extension_uuid, action_category)
        # if we add a new category, we must add it to the action_category_scope
        for _cat in action_category.keys():
            try:
                _ = self.driver.get_action_category_scope_dict(intra_extension_uuid, _cat)
            except AuthzMetadata:
                self.driver.set_action_category_scope_dict(intra_extension_uuid, _cat, {})
        return action_category_dict

    @filter_args
    @enforce("read", "action_categories")
    @enforce("write", "action_categories")
    def add_action_category_dict(self, user_uuid, intra_extension_uuid, action_category_name):
        action_category_uuid = uuid4().hex
        return self.driver.add_action_category_dict(intra_extension_uuid, action_category_uuid, action_category_name)

    @filter_args
    @enforce("write", "action_categories")
    def del_action_category(self, user_uuid, intra_extension_uuid, action_uuid):
        return self.driver.remove_action_category(intra_extension_uuid, action_uuid)

    # Scope functions
    @filter_args
    @enforce("read", "subject_category_scope")
    @enforce("read", "subject_category")
    def get_subject_category_scope_dict(self, user_uuid, intra_extension_uuid, category):
        if category not in self.get_subject_category_dict(user_uuid, intra_extension_uuid)["subject_categories"]:
            raise IntraExtensionError("Subject category {} is unknown.".format(category))
        return self.driver.get_subject_category_scope_dict(intra_extension_uuid, category)

    @filter_args
    @enforce("read", "subject_category_scope")
    @enforce("read", "subject_category")
    def set_subject_category_scope_dict(self, user_uuid, intra_extension_uuid, category, scope):
        if category not in self.get_subject_category_dict(user_uuid, intra_extension_uuid)["subject_categories"]:
            raise IntraExtensionError("Subject category {} is unknown.".format(category))
        return self.driver.set_subject_category_scope_dict(intra_extension_uuid, category, scope)

    @filter_args
    @enforce(("read", "write"), "subject_category_scope")
    @enforce("read", "subject_category")
    def add_subject_category_scope_dict(self, user_uuid, intra_extension_uuid, subject_category, scope_name):
        subject_categories = self.get_subject_category_dict(user_uuid, intra_extension_uuid)
        # check if subject_category exists in database
        if subject_category not in subject_categories["subject_categories"]:
            raise IntraExtensionError("Subject category {} is unknown.".format(subject_category))
        scope_uuid = uuid4().hex
        return self.driver.add_subject_category_scope_dict(
            intra_extension_uuid,
            subject_category,
            scope_uuid,
            scope_name)

    @filter_args
    @enforce("write", "subject_category_scope")
    @enforce("read", "subject_category")
    def del_subject_category_scope(self, user_uuid, intra_extension_uuid, subject_category, subject_category_scope):
        subject_categories = self.get_subject_category_dict(user_uuid, intra_extension_uuid)
        # check if subject_category exists in database
        if subject_category not in subject_categories["subject_categories"]:
            raise IntraExtensionError("Subject category {} is unknown.".format(subject_category))
        return self.driver.remove_subject_category_scope_dict(
            intra_extension_uuid,
            subject_category,
            subject_category_scope)

    @filter_args
    @enforce("read", "object_category_scope")
    @enforce("read", "object_category")
    def get_object_category_scope_dict(self, user_uuid, intra_extension_uuid, category):
        if category not in self.get_object_category_dict(user_uuid, intra_extension_uuid)["object_categories"]:
            raise IntraExtensionError("Object category {} is unknown.".format(category))
        return self.driver.get_object_category_scope_dict(intra_extension_uuid, category)

    @filter_args
    @enforce("read", "object_category_scope")
    @enforce("read", "object_category")
    def set_object_category_scope_dict(self, user_uuid, intra_extension_uuid, category, scope):
        if category not in self.get_object_category_dict(user_uuid, intra_extension_uuid)["object_categories"]:
            raise IntraExtensionError("Object category {} is unknown.".format(category))
        return self.driver.set_object_category_scope_dict(intra_extension_uuid, category, scope)

    @filter_args
    @enforce(("read", "write"), "object_category_scope")
    @enforce("read", "object_category")
    def add_object_category_scope_dict(self, user_uuid, intra_extension_uuid, object_category, scope_name):
        object_categories = self.get_object_category_dict(user_uuid, intra_extension_uuid)
        # check if object_category exists in database
        if object_category not in object_categories["object_categories"]:
            raise IntraExtensionError("Object category {} is unknown.".format(object_category))
        scope_uuid = uuid4().hex
        return self.driver.add_object_category_scope_dict(
            intra_extension_uuid,
            object_category,
            scope_uuid,
            scope_name)

    @filter_args
    @enforce("write", "object_category_scope")
    @enforce("read", "object_category")
    def del_object_category_scope(self, user_uuid, intra_extension_uuid, object_category, object_category_scope):
        object_categories = self.get_object_category_dict(user_uuid, intra_extension_uuid)
        # check if object_category exists in database
        if object_category not in object_categories["object_categories"]:
            raise IntraExtensionError("Object category {} is unknown.".format(object_category))
        return self.driver.remove_object_category_scope_dict(
            intra_extension_uuid,
            object_category,
            object_category_scope)

    @filter_args
    @enforce("read", "action_category_scope")
    @enforce("read", "action_category")
    def get_action_category_scope_dict(self, user_uuid, intra_extension_uuid, category):
        if category not in self.get_action_category_dict(user_uuid, intra_extension_uuid)["action_categories"]:
            raise IntraExtensionError("Action category {} is unknown.".format(category))
        return self.driver.get_action_category_scope_dict(intra_extension_uuid, category)

    @filter_args
    @enforce(("read", "write"), "action_category_scope")
    @enforce("read", "action_category")
    def set_action_category_scope_dict(self, user_uuid, intra_extension_uuid, category, scope):
        if category not in self.get_action_category_dict(user_uuid, intra_extension_uuid)["action_categories"]:
            raise IntraExtensionError("Action category {} is unknown.".format(category))
        return self.driver.set_action_category_scope_dict(intra_extension_uuid, category, scope)

    @filter_args
    @enforce(("read", "write"), "action_category_scope")
    @enforce("read", "action_category")
    def add_action_category_scope_dict(self, user_uuid, intra_extension_uuid, action_category, scope_name):
        action_categories = self.get_action_category_dict(user_uuid, intra_extension_uuid)
        # check if action_category exists in database
        if action_category not in action_categories["action_categories"]:
            raise IntraExtensionError("Action category {} is unknown.".format(action_category))
        scope_uuid = uuid4().hex
        return self.driver.add_action_category_scope_dict(
            intra_extension_uuid,
            action_category,
            scope_uuid,
            scope_name)

    @filter_args
    @enforce("write", "action_category_scope")
    @enforce("read", "action_category")
    def del_action_category_scope(self, user_uuid, intra_extension_uuid, action_category, action_category_scope):
        action_categories = self.get_action_category_dict(user_uuid, intra_extension_uuid)
        # check if action_category exists in database
        if action_category not in action_categories["action_categories"]:
            raise IntraExtensionError("Action category {} is unknown.".format(action_category))
        return self.driver.remove_action_category_scope_dict(
            intra_extension_uuid,
            action_category,
            action_category_scope)

    # Assignment functions

    @filter_args
    @enforce("read", "subject_category_assignment")
    @enforce("read", "subjects")
    def get_subject_category_assignment_dict(self, user_uuid, intra_extension_uuid, subject_uuid):
        # check if subject exists in database
        if subject_uuid not in self.get_subject_dict(user_uuid, intra_extension_uuid)["subjects"]:
            LOG.error("add_subject_assignment: unknown subject_id {}".format(subject_uuid))
            raise IntraExtensionError("Bad input data")
        return self.driver.get_subject_category_assignment_dict(intra_extension_uuid, subject_uuid)

    @filter_args
    @enforce("read", "subject_category_assignment")
    @enforce("write", "subject_category_assignment")
    @enforce("read", "subjects")
    def set_subject_category_assignment_dict(self, user_uuid, intra_extension_uuid, subject_uuid, assignment_dict):
        # check if subject exists in database
        if subject_uuid not in self.get_subject_dict(user_uuid, intra_extension_uuid)["subjects"]:
            LOG.error("add_subject_assignment: unknown subject_id {}".format(subject_uuid))
            raise IntraExtensionError("Bad input data")
        return self.driver.set_subject_category_assignment_dict(intra_extension_uuid, subject_uuid, assignment_dict)

    @filter_args
    @enforce("read", "subject_category_assignment")
    @enforce("write", "subject_category_assignment")
    @enforce("read", "subjects")
    @enforce("read", "subject_category")
    def del_subject_category_assignment(self, user_uuid, intra_extension_uuid, subject_uuid, category_uuid, scope_uuid):
        # check if category exists in database
        if category_uuid not in self.get_subject_category_dict(user_uuid, intra_extension_uuid)["subject_categories"]:
            LOG.error("add_subject_category_scope: unknown subject_category {}".format(category_uuid))
            raise IntraExtensionError("Bad input data")
        # check if subject exists in database
        if subject_uuid not in self.get_subject_dict(user_uuid, intra_extension_uuid)["subjects"]:
            LOG.error("add_subject_assignment: unknown subject_id {}".format(subject_uuid))
            raise IntraExtensionError("Bad input data")
        self.driver.remove_subject_category_assignment(intra_extension_uuid, subject_uuid, category_uuid, scope_uuid)

    @filter_args
    @enforce("write", "subject_category_assignment")
    @enforce("read", "subjects")
    @enforce("read", "subject_category")
    def add_subject_category_assignment_dict(self, user_uuid, intra_extension_uuid, subject_uuid, category_uuid, scope_uuid):
        # check if category exists in database
        if category_uuid not in self.get_subject_category_dict(user_uuid, intra_extension_uuid)["subject_categories"]:
            LOG.error("add_subject_category_scope: unknown subject_category {}".format(category_uuid))
            raise IntraExtensionError("Bad input data")
        # check if subject exists in database
        if subject_uuid not in self.get_subject_dict(user_uuid, intra_extension_uuid)["subjects"]:
            LOG.error("add_subject_assignment: unknown subject_id {}".format(subject_uuid))
            raise IntraExtensionError("Bad input data")
        return self.driver.add_subject_category_assignment_dict(intra_extension_uuid, subject_uuid, category_uuid, scope_uuid)

    @filter_args
    @enforce("read", "object_category_assignment")
    @enforce("read", "objects")
    def get_object_category_assignment_dict(self, user_uuid, intra_extension_uuid, object_uuid):
        # check if object exists in database
        if object_uuid not in self.get_object_dict(user_uuid, intra_extension_uuid)["objects"]:
            LOG.error("add_object_assignment: unknown object_id {}".format(object_uuid))
            raise IntraExtensionError("Bad input data")
        return self.driver.get_object_category_assignment_dict(intra_extension_uuid, object_uuid)

    @filter_args
    @enforce("read", "object_category_assignment")
    @enforce("write", "object_category_assignment")
    @enforce("read", "objects")
    def set_object_category_assignment_dict(self, user_uuid, intra_extension_uuid, object_uuid, assignment_dict):
        # check if object exists in database
        if object_uuid not in self.get_object_dict(user_uuid, intra_extension_uuid)["objects"]:
            LOG.error("add_object_assignment: unknown object_id {}".format(object_uuid))
            raise IntraExtensionError("Bad input data")
        return self.driver.set_object_category_assignment_dict(intra_extension_uuid, object_uuid, assignment_dict)

    @filter_args
    @enforce("read", "object_category_assignment")
    @enforce("write", "object_category_assignment")
    @enforce("read", "objects")
    @enforce("read", "object_category")
    def del_object_category_assignment(self, user_uuid, intra_extension_uuid, object_uuid, category_uuid, scope_uuid):
        # check if category exists in database
        if category_uuid not in self.get_object_category_dict(user_uuid, intra_extension_uuid)["object_categories"]:
            LOG.error("add_object_category_scope: unknown object_category {}".format(category_uuid))
            raise IntraExtensionError("Bad input data")
        # check if object exists in database
        if object_uuid not in self.get_object_dict(user_uuid, intra_extension_uuid)["objects"]:
            LOG.error("add_object_assignment: unknown object_id {}".format(object_uuid))
            raise IntraExtensionError("Bad input data")
        self.driver.remove_object_category_assignment(intra_extension_uuid, object_uuid, category_uuid, scope_uuid)

    @filter_args
    @enforce("write", "object_category_assignment")
    @enforce("read", "objects")
    @enforce("read", "object_category")
    def add_object_category_assignment_dict(self, user_uuid, intra_extension_uuid, object_uuid, category_uuid, scope_uuid):
        # check if category exists in database
        if category_uuid not in self.get_object_category_dict(user_uuid, intra_extension_uuid)["object_categories"]:
            LOG.error("add_object_category_scope: unknown object_category {}".format(category_uuid))
            raise IntraExtensionError("Bad input data")
        # check if object exists in database
        if object_uuid not in self.get_object_dict(user_uuid, intra_extension_uuid)["objects"]:
            LOG.error("add_object_assignment: unknown object_id {}".format(object_uuid))
            raise IntraExtensionError("Bad input data")
        return self.driver.add_object_category_assignment_dict(intra_extension_uuid, object_uuid, category_uuid, scope_uuid)

    @filter_args
    @enforce("read", "action_category_assignment")
    @enforce("read", "actions")
    def get_action_category_assignment_dict(self, user_uuid, intra_extension_uuid, action_uuid):
        # check if action exists in database
        if action_uuid not in self.get_action_dict(user_uuid, intra_extension_uuid)["actions"]:
            LOG.error("add_action_assignment: unknown action_id {}".format(action_uuid))
            raise IntraExtensionError("Bad input data")
        return self.driver.get_action_category_assignment_dict(intra_extension_uuid, action_uuid)

    @filter_args
    @enforce("read", "action_category_assignment")
    @enforce("write", "action_category_assignment")
    @enforce("read", "actions")
    def set_action_category_assignment_dict(self, user_uuid, intra_extension_uuid, action_uuid, assignment_dict):
        # check if action exists in database
        if action_uuid not in self.get_action_dict(user_uuid, intra_extension_uuid)["actions"]:
            LOG.error("add_action_assignment: unknown action_id {}".format(action_uuid))
            raise IntraExtensionError("Bad input data")
        return self.driver.set_action_category_assignment_dict(intra_extension_uuid, action_uuid, assignment_dict)

    @filter_args
    @enforce("read", "action_category_assignment")
    @enforce("write", "action_category_assignment")
    @enforce("read", "actions")
    @enforce("read", "action_category")
    def del_action_category_assignment(self, user_uuid, intra_extension_uuid, action_uuid, category_uuid, scope_uuid):
        # check if category exists in database
        if category_uuid not in self.get_action_category_dict(user_uuid, intra_extension_uuid)["action_categories"]:
            LOG.error("add_action_category_scope: unknown action_category {}".format(category_uuid))
            raise IntraExtensionError("Bad input data")
        # check if action exists in database
        if action_uuid not in self.get_action_dict(user_uuid, intra_extension_uuid)["actions"]:
            LOG.error("add_action_assignment: unknown action_id {}".format(action_uuid))
            raise IntraExtensionError("Bad input data")
        self.driver.remove_action_category_assignment(intra_extension_uuid, action_uuid, category_uuid, scope_uuid)

    @filter_args
    @enforce("write", "action_category_assignment")
    @enforce("read", "actions")
    @enforce("read", "action_category")
    def add_action_category_assignment_dict(self, user_uuid, intra_extension_uuid, action_uuid, category_uuid, scope_uuid):
        # check if category exists in database
        if category_uuid not in self.get_action_category_dict(user_uuid, intra_extension_uuid)["action_categories"]:
            LOG.error("add_action_category_scope: unknown action_category {}".format(category_uuid))
            raise IntraExtensionError("Bad input data")
        # check if action exists in database
        if action_uuid not in self.get_action_dict(user_uuid, intra_extension_uuid)["actions"]:
            LOG.error("add_action_assignment: unknown action_id {}".format(action_uuid))
            raise IntraExtensionError("Bad input data")
        return self.driver.add_action_category_assignment_dict(
            intra_extension_uuid,
            action_uuid,
            category_uuid,
            scope_uuid
        )

    # Metarule functions
    @filter_args
    def get_aggregation_algorithms(self, user_uuid, intra_extension_uuid):
        # TODO: check which algorithms are really usable
        return {"aggregation_algorithms": ["and_true_aggregation", "test_aggregation"]}

    @filter_args
    @enforce("read", "aggregation_algorithms")
    def get_aggregation_algorithm(self, user_uuid, intra_extension_uuid):
        return self.driver.get_meta_rule_dict(intra_extension_uuid)

    @filter_args
    @enforce("read", "aggregation_algorithms")
    @enforce("write", "aggregation_algorithms")
    def set_aggregation_algorithm(self, user_uuid, intra_extension_uuid, aggregation_algorithm):
        if aggregation_algorithm not in self.get_aggregation_algorithms(
                user_uuid, intra_extension_uuid)["aggregation_algorithms"]:
            raise IntraExtensionError("Unknown aggregation_algorithm: {}".format(aggregation_algorithm))
        meta_rule = self.driver.get_meta_rule_dict(intra_extension_uuid)
        meta_rule["aggregation"] = aggregation_algorithm
        return self.driver.set_meta_rule_dict(intra_extension_uuid, meta_rule)

    @filter_args
    @enforce("read", "sub_meta_rule")
    def get_sub_meta_rule(self, user_uuid, intra_extension_uuid):
        return self.driver.get_meta_rule_dict(intra_extension_uuid)

    @filter_args
    @enforce("read", "sub_meta_rule")
    @enforce("write", "sub_meta_rule")
    def set_sub_meta_rule(self, user_uuid, intra_extension_uuid, sub_meta_rules):
        # TODO (dthom): When sub_meta_rule is set, all rules must be dropped
        # because the previous rules cannot be mapped to the new sub_meta_rule.
        for relation in sub_meta_rules.keys():
            if relation not in self.get_sub_meta_rule_relations(user_uuid, intra_extension_uuid)["sub_meta_rule_relations"]:
                LOG.error("set_sub_meta_rule unknown MetaRule relation {}".format(relation))
                raise IntraExtensionError("Bad input data.")
            for cat in ("subject_categories", "object_categories", "action_categories"):
                if cat not in sub_meta_rules[relation]:
                    LOG.error("set_sub_meta_rule category {} missed".format(cat))
                    raise IntraExtensionError("Bad input data.")
                if type(sub_meta_rules[relation][cat]) is not list:
                    LOG.error("set_sub_meta_rule category {} is not a list".format(cat))
                    raise IntraExtensionError("Bad input data.")
            subject_categories = self.get_subject_category_dict(user_uuid, intra_extension_uuid)
            for data in sub_meta_rules[relation]["subject_categories"]:
                    if data not in subject_categories["subject_categories"]:
                        LOG.error("set_sub_meta_rule category {} is not part of subject_categories {}".format(
                            data, subject_categories))
                        raise IntraExtensionError("Bad input data.")
            object_categories = self.get_object_category_dict(user_uuid, intra_extension_uuid)
            for data in sub_meta_rules[relation]["object_categories"]:
                    if data not in object_categories["object_categories"]:
                        LOG.error("set_sub_meta_rule category {} is not part of object_categories {}".format(
                            data, object_categories))
                        raise IntraExtensionError("Bad input data.")
            action_categories = self.get_action_category_dict(user_uuid, intra_extension_uuid)
            for data in sub_meta_rules[relation]["action_categories"]:
                    if data not in action_categories["action_categories"]:
                        LOG.error("set_sub_meta_rule category {} is not part of action_categories {}".format(
                            data, action_categories))
                        raise IntraExtensionError("Bad input data.")
        aggregation = self.driver.get_meta_rule_dict(intra_extension_uuid)["aggregation"]
        return self.driver.set_meta_rule_dict(
            intra_extension_uuid,
            {
                "aggregation": aggregation,
                "sub_meta_rules": sub_meta_rules
            })

    # Sub-rules functions
    @filter_args
    @enforce("read", "sub_rules")
    def get_sub_rules(self, user_uuid, intra_extension_uuid):
        return self.driver.get_rules(intra_extension_uuid)

    @filter_args
    @enforce("read", "sub_rules")
    @enforce("write", "sub_rules")
    def set_sub_rule(self, user_uuid, intra_extension_uuid, relation, sub_rule):
        for item in sub_rule:
            if type(item) not in (str, unicode, bool):
                raise IntraExtensionError("Bad input data (sub_rule).")
        ref_rules = self.driver.get_rules(intra_extension_uuid)
        _sub_rule = list(sub_rule)
        if relation not in self.get_sub_meta_rule_relations(user_uuid, intra_extension_uuid)["sub_meta_rule_relations"]:
            raise IntraExtensionError("Bad input data (rules).")
        # filter strings in sub_rule
        sub_rule = [filter_input(x) for x in sub_rule]
        # check if length of sub_rule is correct from metadata_sub_rule
        metadata_sub_rule = self.get_sub_meta_rule(user_uuid, intra_extension_uuid)
        metadata_sub_rule_length = len(metadata_sub_rule['sub_meta_rules'][relation]["subject_categories"]) + \
                                   len(metadata_sub_rule['sub_meta_rules'][relation]["action_categories"]) + \
                                   len(metadata_sub_rule['sub_meta_rules'][relation]["object_categories"]) + 1
        if metadata_sub_rule_length != len(sub_rule):
            raise IntraExtensionError("Bad number of argument in sub_rule {}/{}".format(sub_rule,
                                                                                        metadata_sub_rule_length))
        # check if each item in sub_rule match a corresponding scope value
        for category in metadata_sub_rule['sub_meta_rules'][relation]["subject_categories"]:
            item = _sub_rule.pop(0)
            if item not in self.get_subject_category_scope_dict(
                    user_uuid,
                    intra_extension_uuid, category)["subject_category_scope"][category].keys():
                raise IntraExtensionError("Bad subject value in sub_rule {}/{}".format(category, item))
        for category in metadata_sub_rule['sub_meta_rules'][relation]["action_categories"]:
            action_categories = self.get_action_category_scope_dict(
                        user_uuid,
                        intra_extension_uuid, category)["action_category_scope"][category]
            item = _sub_rule.pop(0)
            if item not in action_categories.keys():
                self.moonlog_api.warning("set_sub_rule bad action value in sub_rule {}/{}".format(category, item))
                raise IntraExtensionError("Bad input data.")
        for category in metadata_sub_rule['sub_meta_rules'][relation]["object_categories"]:
            item = _sub_rule.pop(0)
            if item not in self.get_object_category_scope_dict(
                    user_uuid,
                    intra_extension_uuid, category)["object_category_scope"][category].keys():
                raise IntraExtensionError("Bad object value in sub_rule {}/{}".format(category, item))
        # check if relation is already there
        if relation not in ref_rules["rules"]:
            ref_rules["rules"][relation] = list()
        # add sub_rule
        ref_rules["rules"][relation].append(sub_rule)
        return self.driver.set_rules(intra_extension_uuid, ref_rules["rules"])

    @filter_args
    @enforce("read", "sub_rules")
    @enforce("write", "sub_rules")
    def del_sub_rule(self, user_uuid, intra_extension_uuid, relation_name, rule):
        ref_rules = self.driver.get_rules(intra_extension_uuid)
        rule = rule.split("+")
        for index, _item in enumerate(rule):
            if "True" in _item:
                rule[index] = True
            if "False" in _item:
                rule[index] = False
        if relation_name in ref_rules["rules"]:
            if rule in ref_rules["rules"][relation_name]:
                ref_rules["rules"][relation_name].remove(rule)
            else:
                self.moonlog_api.error("Unknown rule: {}".format(rule))
        else:
            self.moonlog_api.error("Unknown relation name for rules: {}".format(relation_name))
        return self.driver.set_rules(intra_extension_uuid, ref_rules["rules"])


@dependency.provider('authz_api')
@dependency.requires('identity_api', 'moonlog_api', 'tenant_api')
class IntraExtensionAuthzManager(IntraExtensionManager):

    __genre__ = "authz"

    def authz(self, tenant_uuid, sub, obj, act):
        """Check authorization for a particular action.

        :param tenant_uuid: UUID of a tenant
        :param sub: subject of the request
        :param obj: object of the request
        :param act: action of the request
        :return: True or False or raise an exception
        """
        _intra_authz_extention_uuid = self.tenant_api.get_extension_uuid(tenant_uuid, "authz")
        return super(IntraExtensionAuthzManager, self).authz(_intra_authz_extention_uuid, sub, obj, act)

    def delete_intra_extension(self, intra_extension_id):
        raise AdminException()

    def set_subject_dict(self, user_uuid, intra_extension_uuid, subject_dict):
        raise SubjectAddNotAuthorized()

    def add_subject_dict(self, user_uuid, intra_extension_uuid, subject_uuid):
        raise SubjectAddNotAuthorized()

    def del_subject(self, user_uuid, intra_extension_uuid, subject_uuid):
        raise SubjectDelNotAuthorized()

    def set_object_dict(self, user_uuid, intra_extension_uuid, object_dict):
        raise ObjectAddNotAuthorized()

    def add_object_dict(self, user_uuid, intra_extension_uuid, object_name):
        raise ObjectAddNotAuthorized()

    def del_object(self, user_uuid, intra_extension_uuid, object_uuid):
        raise ObjectDelNotAuthorized()

    def set_action_dict(self, user_uuid, intra_extension_uuid, action_dict):
        raise ActionAddNotAuthorized()

    def add_action_dict(self, user_uuid, intra_extension_uuid, action_name):
        raise ActionAddNotAuthorized()

    def del_action(self, user_uuid, intra_extension_uuid, action_uuid):
        raise ActionDelNotAuthorized()

    def set_subject_category_dict(self, user_uuid, intra_extension_uuid, subject_category):
        raise SubjectCategoryAddNotAuthorized()

    def add_subject_category_dict(self, user_uuid, intra_extension_uuid, subject_category_name):
        raise SubjectCategoryAddNotAuthorized()

    def del_subject_category(self, user_uuid, intra_extension_uuid, subject_uuid):
        raise SubjectCategoryDelNotAuthorized()

    def set_object_category_dict(self, user_uuid, intra_extension_uuid, object_category):
        raise ObjectCategoryAddNotAuthorized()

    def add_object_category_dict(self, user_uuid, intra_extension_uuid, object_category_name):
        raise ObjectCategoryAddNotAuthorized()

    def del_object_category(self, user_uuid, intra_extension_uuid, object_uuid):
        raise ObjectCategoryDelNotAuthorized()

    def set_action_category_dict(self, user_uuid, intra_extension_uuid, action_category):
        raise ActionCategoryAddNotAuthorized()

    def add_action_category_dict(self, user_uuid, intra_extension_uuid, action_category_name):
        raise ActionCategoryAddNotAuthorized()

    def del_action_category(self, user_uuid, intra_extension_uuid, action_uuid):
        raise ActionCategoryDelNotAuthorized()

    def set_subject_category_scope_dict(self, user_uuid, intra_extension_uuid, category, scope):
        raise SubjectCategoryScopeAddNotAuthorized()

    def add_subject_category_scope_dict(self, user_uuid, intra_extension_uuid, subject_category, scope_name):
        raise SubjectCategoryScopeAddNotAuthorized()

    def del_subject_category_scope(self, user_uuid, intra_extension_uuid, subject_category, subject_category_scope):
        raise SubjectCategoryScopeDelNotAuthorized()

    def set_object_category_scope_dict(self, user_uuid, intra_extension_uuid, category, scope):
        raise ObjectCategoryScopeAddNotAuthorized()

    def add_object_category_scope_dict(self, user_uuid, intra_extension_uuid, object_category, scope_name):
        raise ObjectCategoryScopeAddNotAuthorized()

    def del_object_category_scope(self, user_uuid, intra_extension_uuid, object_category, object_category_scope):
        raise ObjectCategoryScopeDelNotAuthorized()

    def set_action_category_scope_dict(self, user_uuid, intra_extension_uuid, category, scope):
        raise ActionCategoryScopeAddNotAuthorized()

    def add_action_category_scope_dict(self, user_uuid, intra_extension_uuid, action_category, scope_name):
        raise ActionCategoryScopeAddNotAuthorized()

    def del_action_category_scope(self, user_uuid, intra_extension_uuid, action_category, action_category_scope):
        raise ActionCategoryScopeDelNotAuthorized()

    def set_subject_category_assignment_dict(self, user_uuid, intra_extension_uuid, subject_uuid, assignment_dict):
        raise SubjectCategoryAssignmentAddNotAuthorized()

    def del_subject_category_assignment(self, user_uuid, intra_extension_uuid, subject_uuid, category_uuid, scope_uuid):
        raise SubjectCategoryAssignmentAddNotAuthorized()

    def add_subject_category_assignment_dict(self, user_uuid, intra_extension_uuid, subject_uuid, category_uuid, scope_uuid):
        raise SubjectCategoryAssignmentDelNotAuthorized()

    def set_object_category_assignment_dict(self, user_uuid, intra_extension_uuid, object_uuid, assignment_dict):
        raise ObjectCategoryAssignmentAddNotAuthorized()

    def del_object_category_assignment(self, user_uuid, intra_extension_uuid, object_uuid, category_uuid, scope_uuid):
        raise ObjectCategoryAssignmentAddNotAuthorized()

    def add_object_category_assignment_dict(self, user_uuid, intra_extension_uuid, object_uuid, category_uuid, scope_uuid):
        raise ObjectCategoryAssignmentDelNotAuthorized()

    def set_action_category_assignment_dict(self, user_uuid, intra_extension_uuid, action_uuid, assignment_dict):
        raise ActionCategoryAssignmentAddNotAuthorized()

    def del_action_category_assignment(self, user_uuid, intra_extension_uuid, action_uuid, category_uuid, scope_uuid):
        raise ActionCategoryAssignmentAddNotAuthorized()

    def add_action_category_assignment_dict(self, user_uuid, intra_extension_uuid, action_uuid, category_uuid, scope_uuid):
        raise ActionCategoryAssignmentDelNotAuthorized()

    def set_aggregation_algorithm(self, user_uuid, intra_extension_uuid, aggregation_algorithm):
        raise MetaRuleAddNotAuthorized()

    def set_sub_meta_rule(self, user_uuid, intra_extension_uuid, sub_meta_rules):
        raise MetaRuleAddNotAuthorized()

    def set_sub_rule(self, user_uuid, intra_extension_uuid, relation, sub_rule):
        raise RuleAddNotAuthorized()

    def del_sub_rule(self, user_uuid, intra_extension_uuid, relation_name, rule):
        raise RuleAddNotAuthorized()

@dependency.provider('admin_api')
@dependency.requires('identity_api', 'moonlog_api', 'tenant_api')
class IntraExtensionAdminManager(IntraExtensionManager):

    __genre__ = "admin"

    # def set_perimeter_values(self, ie, policy_dir):
    #
    #     # Check if object like "subjects", "objects", "actions" exist...
    #     perimeter_path = os.path.join(policy_dir, 'perimeter.json')
    #     f = open(perimeter_path)
    #     json_perimeter = json.load(f)
    #     for item in ("subjects", "objects", "actions"):
    #         if item not in json_perimeter["objects"]:
    #             raise AdminIntraExtensionCreationError()
    #
    #     super(IntraExtensionAdminManager, self).set_perimeter_values(ie, policy_dir)
    #
    # @filter_args
    # def add_subject_dict(self, user_name, uuid, subject_uuid):
    #     raise AdminIntraExtensionModificationNotAuthorized()
    #
    # @filter_args
    # def del_subject(self, user_name, uuid, subject_uuid):
    #     raise AdminIntraExtensionModificationNotAuthorized()


class AuthzDriver(object):

    def get_subject_category_list(self, extension_uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def get_object_category_list(self, extension_uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def get_action_category_list(self, extension_uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def get_subject_category_value_dict(self, extension_uuid, subject_uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def get_object_category_value_dict(self, extension_uuid, object_uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def get_action_category_value_dict(self, extension_uuid, action_uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def get_meta_rule(self, extension_uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def get_rules(self, extension_uuid):
        raise exception.NotImplemented()  # pragma: no cover


class UpdateDriver(object):

    def get_intra_extensions(self):
        raise exception.NotImplemented()  # pragma: no cover

    def get_intra_extension(self, extension_uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def create_intra_extensions(self, extension_uuid, intra_extension):
        raise exception.NotImplemented()  # pragma: no cover

    def delete_intra_extensions(self, extension_uuid):
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and setter for tenant

    def get_tenant(self, uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def set_tenant(self, uuid, tenant_id):
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and setter for name

    def get_name(self, uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def set_name(self, uuid, name):
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and setter for model

    def get_model(self, uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def set_model(self, uuid, model):
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and setter for genre

    def get_genre(self, uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def set_genre(self, uuid, genre):
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and setter for description

    def get_description(self, uuid):
        raise exception.NotImplemented()  # pragma: no cover

    def set_description(self, uuid, args):
        raise exception.NotImplemented()  # pragma: no cover


class IntraExtensionDriver(object):

    # Getter ad Setter for subjects

    def get_subject_dict(self, extension_uuid):
        """Get the list of subject for that IntraExtension

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :return: a dictionary containing all subjects for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_dict(self, extension_uuid, subject_dict):
        """Set the list of subject for that IntraExtension

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_dict: dict of subject: {"uuid1": "name1", "uuid2": "name2"}
        :type subject_dict: dict
        :return: a dictionary containing all subjects for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_subject(self, extension_uuid, subject_uuid, subject_name):
        """Add a subject

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_uuid: Subject UUID
        :type subject_uuid: string
        :param subject_name: Subject name
        :type subject_name: string
        :return: the added subject {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_subject(self, extension_uuid, subject_uuid):
        """Remove a subject

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_uuid: Subject UUID
        :type subject_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter ad Setter for objects

    def get_object_dict(self, extension_uuid):
        """Get the list of object for that IntraExtension

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :return: a dictionary containing all objects for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_dict(self, extension_uuid, object_dict):
        """Set the list of object for that IntraExtension

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_dict: dict of object: {"uuid1": "name1", "uuid2": "name2"}
        :type object_dict: dict
        :return: a dictionary containing all objects for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_object(self, extension_uuid, object_uuid, object_name):
        """Ad an object

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_uuid: Object UUID
        :type object_uuid: string
        :param object_name: Object name
        :type object_name: string
        :return: the added object {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_object(self, extension_uuid, object_uuid):
        """Remove an object

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_uuid: Object UUID
        :type object_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter ad Setter for actions

    def get_action_dict(self, extension_uuid):
        """ Get the list of action for that IntraExtension

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :return: a dictionary containing all actions for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_dict(self, extension_uuid, action_dict):
        """ Set the list of action for that IntraExtension

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_dict: dict of actions: {"uuid1": "name1", "uuid2": "name2"}
        :type action_dict: dict
        :return: a dictionary containing all actions for that IntraExtension, eg. {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_action(self, extension_uuid, action_uuid, action_name):
        """Ad an action

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_uuid: Action UUID
        :type action_uuid: string
        :param action_name: Action name
        :type action_name: string
        :return: the added action {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_action(self, extension_uuid, action_uuid):
        """Remove an action

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_uuid: Action UUID
        :type action_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter ad Setter for subject_category

    def get_subject_category_dict(self, extension_uuid):
        """Get a list of all subject categories

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :return: a dictionary containing all subject categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_category_dict(self, extension_uuid, subject_categories):
        """Set the list of all subject categories

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_categories: dict of subject categories {"uuid1": "name1", "uuid2": "name2"}
        :type subject_categories: dict
        :return: a dictionary containing all subject categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_subject_category_dict(self, extension_uuid, subject_category_uuid, subject_category_name):
        """Add a subject category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_category_uuid: the UUID of the subject category
        :type subject_category_uuid: string
        :param subject_category_name: the name of the subject category
        :type subject_category_name: string
        :return: a dictionnary with the subject catgory added {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_subject_category(self, extension_uuid, subject_category_uuid):
        """Remove one subject category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_category_uuid: the UUID of subject category to remove
        :type subject_category_uuid: string
        :return: a dictionary containing all subject categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter ad Setter for object_category

    def get_object_category_dict(self, extension_uuid):
        """Get a list of all object categories

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :return: a dictionary containing all object categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_category_dict(self, extension_uuid, object_categories):
        """Set the list of all object categories

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_categories: dict of object categories {"uuid1": "name1", "uuid2": "name2"}
        :type object_categories: dict
        :return: a dictionary containing all object categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_object_category_dict(self, extension_uuid, object_category_uuid, object_category_name):
        """Add a object category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_category_uuid: the UUID of the object category
        :type object_category_uuid: string
        :param object_category_name: the name of the object category
        :type object_category_name: string
        :return: a dictionnary with the object catgory added {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_object_category(self, extension_uuid, object_category_uuid):
        """Remove one object category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_category_uuid: the UUID of object category to remove
        :type object_category_uuid: string
        :return: a dictionary containing all object categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter ad Setter for action_category

    def get_action_category_dict(self, extension_uuid):
        """Get a list of all action categories

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :return: a dictionary containing all action categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_category_dict(self, extension_uuid, action_categories):
        """Set the list of all action categories

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_categories: dict of action categories {"uuid1": "name1", "uuid2": "name2"}
        :type action_categories: dict
        :return: a dictionary containing all action categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_action_category_dict(self, extension_uuid, action_category_uuid, action_category_name):
        """Add a action category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_category_uuid: the UUID of the action category
        :type action_category_uuid: string
        :param action_category_name: the name of the action category
        :type action_category_name: string
        :return: a dictionnary with the action catgory added {"uuid1": "name1"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_action_category(self, extension_uuid, action_category_uuid):
        """Remove one action category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_category_uuid: the UUID of action category to remove
        :type action_category_uuid: string
        :return: a dictionary containing all action categories {"uuid1": "name1", "uuid2": "name2"}
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and Setter for subject_category_value_scope

    def get_subject_category_scope_dict(self, extension_uuid, category):
        """Get a list of all subject category scope

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param category: the category UUID where the scope values are
        :type category: string
        :return: a dictionary containing all subject category scope {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_category_scope_dict(self, extension_uuid, subject_category, scope):
        """Set the list of all scope for that subject category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_category: the UUID of the subject category where this scope will be set
        :type subject_category: string
        :return: a dictionary containing all scope {"scope_uuid1": "scope_name1, "scope_uuid2": "scope_name2}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_subject_category_scope_dict(self, extension_uuid, subject_category, scope_uuid, scope_name):
        """Add a subject category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_category: the subject category UUID where the scope will be added
        :type subject_category: string
        :param scope_uuid: the UUID of the subject category
        :type scope_uuid: string
        :param scope_name: the name of the subject category
        :type scope_name: string
        :return: a dictionary containing the subject category scope added {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_subject_category_scope_dict(self, extension_uuid, subject_category, scope_uuid):
        """Remove one scope belonging to a subject category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_category: the UUID of subject categorywhere we can find the scope to remove
        :type subject_category: string
        :param scope_uuid: the UUID of the scope to remove
        :type scope_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and Setter for object_category_scope

    def get_object_category_scope_dict(self, extension_uuid, category):
        """Get a list of all object category scope

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param category: the category UUID where the scope values are
        :type category: string
        :return: a dictionary containing all object category scope {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_category_scope_dict(self, extension_uuid, object_category, scope):
        """Set the list of all scope for that object category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_category: the UUID of the object category where this scope will be set
        :type object_category: string
        :return: a dictionary containing all scope {"scope_uuid1": "scope_name1, "scope_uuid2": "scope_name2}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_object_category_scope_dict(self, extension_uuid, object_category, scope_uuid, scope_name):
        """Add a object category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_category: the object category UUID where the scope will be added
        :type object_category: string
        :param scope_uuid: the UUID of the object category
        :type scope_uuid: string
        :param scope_name: the name of the object category
        :type scope_name: string
        :return: a dictionary containing the object category scope added {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_object_category_scope_dict(self, extension_uuid, object_category, scope_uuid):
        """Remove one scope belonging to a object category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_category: the UUID of object categorywhere we can find the scope to remove
        :type object_category: string
        :param scope_uuid: the UUID of the scope to remove
        :type scope_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and Setter for action_category_scope

    def get_action_category_scope_dict(self, extension_uuid, category):
        """Get a list of all action category scope

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param category: the category UUID where the scope values are
        :type category: string
        :return: a dictionary containing all action category scope {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_category_scope_dict(self, extension_uuid, action_category, scope):
        """Set the list of all scope for that action category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_category: the UUID of the action category where this scope will be set
        :type action_category: string
        :return: a dictionary containing all scope {"scope_uuid1": "scope_name1, "scope_uuid2": "scope_name2}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_action_category_scope_dict(self, extension_uuid, action_category, scope_uuid, scope_name):
        """Add a action category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_category: the action category UUID where the scope will be added
        :type action_category: string
        :param scope_uuid: the UUID of the action category
        :type scope_uuid: string
        :param scope_name: the name of the action category
        :type scope_name: string
        :return: a dictionary containing the action category scope added {"category1": {"scope_uuid1": "scope_name1}}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_action_category_scope_dict(self, extension_uuid, action_category, scope_uuid):
        """Remove one scope belonging to a action category

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_category: the UUID of action categorywhere we can find the scope to remove
        :type action_category: string
        :param scope_uuid: the UUID of the scope to remove
        :type scope_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and Setter for subject_category_assignment

    def get_subject_category_assignment_dict(self, extension_uuid, subject_uuid):
        """Get the assignment for a given subject_uuid

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_uuid: subject UUID
        :type subject_uuid: string
        :return: a dictionary of assignment for the given subject {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_subject_category_assignment_dict(self, extension_uuid, subject_uuid, assignment_dict):
        """Set the assignment for a given subject_uuid

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_uuid: subject UUID
        :type subject_uuid: string
        :param assignment_dict: the assignment dictionary {"cat1": ["scope_uuid1", "scope_uuid2"]}
        :type assignment_dict: dict
        :return: a dictionary of assignment for the given subject {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_subject_category_assignment_dict(self, extension_uuid, subject_uuid, category_uuid, scope_uuid):
        """Add a scope to a category and to a subject

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_uuid: the subject UUID
        :type subject_uuid: string
        :param category_uuid: the category UUID
        :type category_uuid: string
        :param scope_uuid: the scope UUID
        :type scope_uuid: string
        :return: a dictionary of assignment for the given subject {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_subject_category_assignment(self, extension_uuid, subject_uuid, category_uuid, scope_uuid):
        """Remove a scope from a category and from a subject

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param subject_uuid: the subject UUID
        :type subject_uuid: string
        :param category_uuid: the category UUID
        :type category_uuid: string
        :param scope_uuid: the scope UUID
        :type scope_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and Setter for object_category_assignment

    def get_object_category_assignment_dict(self, extension_uuid, object_uuid):
        """Get the assignment for a given object_uuid

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_uuid: object UUID
        :type object_uuid: string
        :return: a dictionary of assignment for the given object {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_object_category_assignment_dict(self, extension_uuid, object_uuid, assignment_dict):
        """Set the assignment for a given object_uuid

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_uuid: object UUID
        :type object_uuid: string
        :param assignment_dict: the assignment dictionary {"cat1": ["scope_uuid1", "scope_uuid2"]}
        :type assignment_dict: dict
        :return: a dictionary of assignment for the given object {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_object_category_assignment_dict(self, extension_uuid, object_uuid, category_uuid, scope_uuid):
        """Add a scope to a category and to a object

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_uuid: the object UUID
        :type object_uuid: string
        :param category_uuid: the category UUID
        :type category_uuid: string
        :param scope_uuid: the scope UUID
        :type scope_uuid: string
        :return: a dictionary of assignment for the given object {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_object_category_assignment(self, extension_uuid, object_uuid, category_uuid, scope_uuid):
        """Remove a scope from a category and from a object

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param object_uuid: the object UUID
        :type object_uuid: string
        :param category_uuid: the category UUID
        :type category_uuid: string
        :param scope_uuid: the scope UUID
        :type scope_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and Setter for action_category_assignment

    def get_action_category_assignment_dict(self, extension_uuid, action_uuid):
        """Get the assignment for a given action_uuid

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_uuid: action UUID
        :type action_uuid: string
        :return: a dictionary of assignment for the given action {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_action_category_assignment_dict(self, extension_uuid, action_uuid, assignment_dict):
        """Set the assignment for a given action_uuid

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_uuid: action UUID
        :type action_uuid: string
        :param assignment_dict: the assignment dictionary {"cat1": ["scope_uuid1", "scope_uuid2"]}
        :type assignment_dict: dict
        :return: a dictionary of assignment for the given action {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def add_action_category_assignment_dict(self, extension_uuid, action_uuid, category_uuid, scope_uuid):
        """Add a scope to a category and to a action

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_uuid: the action UUID
        :type action_uuid: string
        :param category_uuid: the category UUID
        :type category_uuid: string
        :param scope_uuid: the scope UUID
        :type scope_uuid: string
        :return: a dictionary of assignment for the given action {"cat1": ["scope_uuid1", "scope_uuid2"]}
        """
        raise exception.NotImplemented()  # pragma: no cover

    def remove_action_category_assignment(self, extension_uuid, action_uuid, category_uuid, scope_uuid):
        """Remove a scope from a category and from a action

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param action_uuid: the action UUID
        :type action_uuid: string
        :param category_uuid: the category UUID
        :type category_uuid: string
        :param scope_uuid: the scope UUID
        :type scope_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    # Getter and Setter for meta_rule

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

    # Getter and Setter for rules

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

    # Getter and Setter for intra_extension

    def get_intra_extension_list(self):
        """Get a list of IntraExtension UUIDs

        :return: a list of IntraExtension UUIDs ["uuid1", "uuid2"]
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_intra_extension_dict(self, extension_uuid):
        """Get a description of an IntraExtension

        :param extension_uuid: the UUID of the IntraExtension
        :type extension_uuid: string
        :return:
        """
        raise exception.NotImplemented()  # pragma: no cover

    def set_intra_extension(self, extension_uuid, extension_dict):
        """Set a new IntraExtension

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :param extension_dict: a dictionary withe the description of the IntraExtension (see below)
        :type extension_dict: dict
        :return: the IntraExtension dictionary, example:
        {
            "id": "uuid1",
            "name": "Name of the intra_extension",
            "model": "Model of te intra_extension (admin or authz)"
            "description": "a description of the intra_extension"
        }
        """
        raise exception.NotImplemented()  # pragma: no cover

    def delete_intra_extension(self, extension_uuid):
        """Delete an IntraExtension

        :param extension_uuid: IntraExtension UUID
        :type extension_uuid: string
        :return: None
        """
        raise exception.NotImplemented()  # pragma: no cover

    def get_sub_meta_rule_relations(self, username, uuid):
        # TODO: check which relations are really usable
        return {"sub_meta_rule_relations": ["relation_super", "relation_test"]}


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

