# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import copy
import itertools
from oslo_log import log as logging
from oslo_config import cfg
from moon_utilities.security_functions import call, Context
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


class PDP:

    def __init__(self, context):
        self.__context = context


class Authorization(object):
    """
    Retrieve the current status of all components.
    """

    __version__ = "0.1.0"
    pdp_id = None
    meta_rule_id = None
    keystone_project_id = None

    def __init__(self, component_id):
        self.component_id = component_id
        LOG.info("ext={}".format(component_id))
        for _id_value in component_id.split("_"):
            LOG.info("_id_value={}".format(_id_value.split(":")))
            _type, _id = _id_value.split(":")
            if _type == "pdp":
                self.pdp_id = _id
            elif _type == "metarule":
                self.meta_rule_id = _id
            elif _type == "project":
                self.keystone_project_id = _id
        # self.manager = IntraExtensionAdminManager
        # self.context = {"id": self.component_id, "user_id": "admin"}
        # self.aggregation_algorithm_dict = ConfigurationManager.driver.get_aggregation_algorithms_dict()
        # self.__subjects = None
        # self.__objects = None
        # self.__actions = None
        # self.__subject_scopes = None
        # self.__object_scopes = None
        # self.__action_scopes = None
        # self.__subject_categories = None
        # self.__object_categories = None
        # self.__action_categories = None
        # self.__subject_assignments = None
        # self.__object_assignments = None
        # self.__action_assignments = None
        # self.__sub_meta_rules = None
        # self.__rules = None
        # self.aggregation_algorithm_id = None

    # @property
    # def subjects(self):
    #     if not self.__subjects:
    #         self.__subjects = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=self.context,
    #                                method="get_subjects", args={})
    #         if "subjects" in self.__subjects:
    #             return self.__subjects
    #         else:
    #             LOG.error("An error occurred {}".format(self.__subjects))
    #     return self.__subjects
    #
    # @property
    # def objects(self):
    #     if not self.__objects:
    #         self.__objects = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=self.context,
    #                               method="get_objects", args={})
    #         if "objects" in self.__objects:
    #             return self.__objects
    #         else:
    #             LOG.error("An error occurred {}".format(self.__objects))
    #     return self.__objects
    #
    # @property
    # def actions(self):
    #     if not self.__actions:
    #         self.__actions = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=self.context,
    #                               method="get_actions", args={})
    #         if "actions" in self.__actions:
    #             return self.__actions
    #         else:
    #             LOG.error("An error occurred {}".format(self.__actions))
    #     return self.__actions
    #
    # @property
    # def subject_scopes(self):
    #     if not self.__subject_scopes:
    #         self.__subject_scopes = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=self.context,
    #                                      method="get_subject_scopes", args={})
    #         if "subject_scopes" in self.__subject_scopes:
    #             return self.__subject_scopes
    #         else:
    #             LOG.error("An error occurred {}".format(self.__subject_scopes))
    #     return self.__subject_scopes
    #
    # @property
    # def object_scopes(self):
    #     if not self.__object_scopes:
    #         self.__object_scopes = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=self.context,
    #                                     method="get_object_scopes", args={})
    #         if "object_scopes" in self.__object_scopes:
    #             return self.__object_scopes
    #         else:
    #             LOG.error("An error occurred {}".format(self.__object_scopes))
    #     return self.__object_scopes
    #
    # @property
    # def action_scopes(self):
    #     if not self.__action_scopes:
    #         self.__action_scopes = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=self.context,
    #                                     method="get_action_scopes", args={})
    #         if "action_scopes" in self.__action_scopes:
    #             return self.__action_scopes
    #         else:
    #             LOG.error("An error occurred {}".format(self.__action_scopes))
    #     return self.__action_scopes
    #
    # @property
    # def subject_categories(self):
    #     if not self.__subject_categories:
    #         self.__subject_categories = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=self.context,
    #                                          method="get_subject_categories", args={})
    #         if "subject_categories" in self.__subject_categories:
    #             return self.__subject_categories
    #         else:
    #             LOG.error("An error occurred {}".format(self.__subject_categories))
    #     return self.__subject_categories
    #
    # @property
    # def object_categories(self):
    #     if not self.__object_categories:
    #         self.__object_categories = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=self.context,
    #                                          method="get_object_categories", args={})
    #         if "object_categories" in self.__object_categories:
    #             return self.__object_categories
    #         else:
    #             LOG.error("An error occurred {}".format(self.__object_categories))
    #     return self.__object_categories
    #
    # @property
    # def action_categories(self):
    #     if not self.__action_categories:
    #         self.__action_categories = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=self.context,
    #                                          method="get_action_categories", args={})
    #         if "action_categories" in self.__action_categories:
    #             return self.__action_categories
    #         else:
    #             LOG.error("An error occurred {}".format(self.__action_categories))
    #     return self.__action_categories
    #
    # @property
    # def subject_assignments(self):
    #     if not self.__subject_assignments:
    #         context = copy.deepcopy(self.context)
    #         context['sid'] = None
    #         context['scid'] = None
    #         args = {'ssid': None}
    #         self.__subject_assignments = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=context,
    #                                           method="get_subject_assignments", args=args)
    #         if "subject_assignments" in self.__subject_assignments:
    #             return self.__subject_assignments
    #         else:
    #             LOG.error("An error occurred {}".format(self.__subject_assignments))
    #     return self.__subject_assignments
    #
    # @property
    # def object_assignments(self):
    #     if not self.__object_assignments:
    #         context = copy.deepcopy(self.context)
    #         context['sid'] = None
    #         context['scid'] = None
    #         args = {'ssid': None}
    #         self.__object_assignments = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=context,
    #                                           method="get_object_assignments", args=args)
    #         if "object_assignments" in self.__object_assignments:
    #             return self.__object_assignments
    #         else:
    #             LOG.error("An error occurred {}".format(self.__object_assignments))
    #     return self.__object_assignments
    #
    # @property
    # def action_assignments(self):
    #     if not self.__action_assignments:
    #         context = copy.deepcopy(self.context)
    #         context['sid'] = None
    #         context['scid'] = None
    #         args = {'ssid': None}
    #         self.__action_assignments = call("moon_secpolicy_{}".format(self.intra_extension_id), ctx=context,
    #                                           method="get_action_assignments", args=args)
    #         if "action_assignments" in self.__action_assignments:
    #             return self.__action_assignments
    #         else:
    #             LOG.error("An error occurred {}".format(self.__action_assignments))
    #     return self.__action_assignments
    #
    # @property
    # def sub_meta_rules(self):
    #     if not self.__sub_meta_rules:
    #         self.__sub_meta_rules = call("moon_secfunction_{}".format(self.intra_extension_id), ctx=self.context,
    #                                      method="get_sub_meta_rules", args={})
    #         if "sub_meta_rules" in self.__sub_meta_rules:
    #             return self.__sub_meta_rules
    #         else:
    #             LOG.error("An error occurred {}".format(self.__sub_meta_rules))
    #     return self.__sub_meta_rules
    #
    # @property
    # def rules(self):
    #     if not self.__rules:
    #         self.__rules = dict()
    #         for _id, _value in self.sub_meta_rules["sub_meta_rules"].items():
    #             context = copy.deepcopy(self.context)
    #             context["sub_meta_rule_id"] = _id
    #             __elements = call("moon_secfunction_{}".format(self.intra_extension_id), ctx=context,
    #                               method="get_rules", args={})
    #             if "rules" in __elements:
    #                 self.__rules[_id] = __elements
    #             else:
    #                 LOG.error("An error occurred {}".format(__elements))
    #     return self.__rules

    # def __get_authz_buffer(self, subject_id, object_id, action_id):
    #     """
    #     :param intra_extension_id:
    #     :param subject_id:
    #     :param object_id:
    #     :param action_id:
    #     :return: authz_buffer = {
    #         'subject_id': xxx,
    #         'object_id': yyy,
    #         'action_id': zzz,
    #         'subject_assignments': {
    #             'subject_category1': [],
    #             'subject_category2': [],
    #             ...
    #         },
    #         'object_assignments': {},
    #         'action_assignments': {},
    #     }
    #     """
    #     authz_buffer = dict()
    #     # Sometimes it is not the subject ID but the User Keystone ID, so, we have to check
    #     subjects_dict = copy.deepcopy(self.subjects)
    #     if subject_id not in subjects_dict["subjects"].keys():
    #         for _subject_id in subjects_dict["subjects"]:
    #             if subjects_dict["subjects"][_subject_id]['keystone_id']:
    #                 subject_id = _subject_id
    #                 break
    #     authz_buffer['subject_id'] = subject_id
    #     authz_buffer['object_id'] = object_id
    #     authz_buffer['action_id'] = action_id
    #     meta_data_dict = dict()
    #     meta_data_dict["subject_categories"] = copy.deepcopy(self.subject_categories["subject_categories"])
    #     meta_data_dict["object_categories"] = copy.deepcopy(self.object_categories["object_categories"])
    #     meta_data_dict["action_categories"] = copy.deepcopy(self.action_categories["action_categories"])
    #     subject_assignment_dict = copy.deepcopy(self.subject_assignments['subject_assignments'][subject_id])
    #     LOG.info("__get_authz_buffer self.object_assignments['object_assignments']={}".format(self.object_assignments['object_assignments']))
    #     LOG.info("__get_authz_buffer object_id={}".format(object_id))
    #     object_assignment_dict = copy.deepcopy(self.object_assignments['object_assignments'][object_id])
    #     action_assignment_dict = copy.deepcopy(self.action_assignments['action_assignments'][action_id])
    #
    #     authz_buffer['subject_assignments'] = dict()
    #     authz_buffer['object_assignments'] = dict()
    #     authz_buffer['action_assignments'] = dict()
    #
    #     for _subject_category in meta_data_dict['subject_categories']:
    #         authz_buffer['subject_assignments'][_subject_category] = list(subject_assignment_dict[_subject_category])
    #     for _object_category in meta_data_dict['object_categories']:
    #         authz_buffer['object_assignments'][_object_category] = list(object_assignment_dict[_object_category])
    #     for _action_category in meta_data_dict['action_categories']:
    #         authz_buffer['action_assignments'][_action_category] = list(action_assignment_dict[_action_category])
    #     return authz_buffer
    #
    # def __get_decision_dict(self, subject_id, object_id, action_id):
    #     """Check authorization for a particular action.
    #
    #     :param intra_extension_id: UUID of an IntraExtension
    #     :param subject_id: subject UUID of the request
    #     :param object_id: object UUID of the request
    #     :param action_id: action UUID of the request
    #     :return: True or False or raise an exception
    #     :raises:
    #     """
    #     authz_buffer = self.__get_authz_buffer(subject_id, object_id, action_id)
    #     decision_buffer = dict()
    #
    #     meta_rule_dict = copy.deepcopy(self.sub_meta_rules['sub_meta_rules'])
    #     rules_dict = copy.deepcopy(self.rules)
    #     for sub_meta_rule_id in meta_rule_dict:
    #         if meta_rule_dict[sub_meta_rule_id]['algorithm'] == 'inclusion':
    #             decision_buffer[sub_meta_rule_id] = algorithms.inclusion(
    #                 authz_buffer,
    #                 meta_rule_dict[sub_meta_rule_id],
    #                 rules_dict[sub_meta_rule_id]['rules'].values())
    #         elif meta_rule_dict[sub_meta_rule_id]['algorithm'] == 'comparison':
    #             decision_buffer[sub_meta_rule_id] = algorithms.comparison(
    #                 authz_buffer,
    #                 meta_rule_dict[sub_meta_rule_id],
    #                 rules_dict[sub_meta_rule_id]['rules'].values())
    #
    #     return decision_buffer
    #
    # def __authz(self, subject_id, object_id, action_id):
    #     decision = False
    #     decision_dict = dict()
    #     try:
    #         decision_dict = self.__get_decision_dict(subject_id, object_id, action_id)
    #     except (exceptions.SubjectUnknown, exceptions.ObjectUnknown, exceptions.ActionUnknown) as e:
    #         # maybe we need to synchronize with the master
    #         pass
    #         # if CONF.slave.slave_name and CONF.slave.master_url:
    #         #     self.get_data_from_master()
    #         #     decision_dict = self.__get_decision_dict(subject_id, object_id, action_id)
    #
    #     try:
    #         # aggregation_algorithm_id = IntraExtensionAdminManager.get_aggregation_algorithm_id(
    #         #     "admin",
    #         #     self.intra_extension_id)['aggregation_algorithm']
    #         if not self.aggregation_algorithm_id:
    #             self.aggregation_algorithm_id = self.intra_extension['aggregation_algorithm']
    #     except Exception as e:
    #         LOG.error(e, exc_info=True)
    #         LOG.error(self.intra_extension)
    #         return {
    #             'authz': False,
    #             'comment': "Aggregation algorithm not set"
    #         }
    #     if self.aggregation_algorithm_dict[self.aggregation_algorithm_id]['name'] == 'all_true':
    #         decision = algorithms.all_true(decision_dict)
    #     elif self.aggregation_algorithm_dict[self.aggregation_algorithm_id]['name'] == 'one_true':
    #         decision = algorithms.one_true(decision_dict)
    #     if not decision_dict or not decision:
    #         raise exceptions.AuthzException("{} {}-{}-{}".format(self.intra_extension['id'], subject_id, action_id, object_id))
    #     return {
    #         'authz': decision,
    #         'comment': "{} {}-{}-{}".format(self.intra_extension['id'], subject_id, action_id, object_id)
    #     }
    #
    # def authz_bak(self, ctx, args):
    #     """Return the authorization for a specific request
    #
    #     :param ctx: {
    #         "subject_name" : "string name",
    #         "action_name" : "string name",
    #         "object_name" : "string name"
    #     }
    #     :param args: {}
    #     :return: {
    #         "authz": "True or False",
    #         "message": "optional message"
    #     }
    #     """
    #     intra_extension_id = ctx["id"]
    #     try:
    #         subject_id = get_uuid_from_name(ctx["subject_name"], self.subjects['subjects'])
    #         object_id = get_uuid_from_name(ctx["object_name"], self.objects['objects'])
    #         action_id = get_uuid_from_name(ctx["action_name"], self.actions['actions'])
    #         authz_result = self.__authz(subject_id, object_id, action_id)
    #         return authz_result
    #     except Exception as e:
    #         LOG.error(e, exc_info=True)
    #         return {"authz": False,
    #                 "error": str(e),
    #                 "intra_extension_id": intra_extension_id,
    #                 "ctx": ctx, "args": args}
    #
    #     return {"authz": False}

    def __check_rules(self, context):
        scopes_list = list()
        current_header_id = context.headers[context.index]['id']
        current_pdp = context.pdp_set[current_header_id]
        category_list = list()
        category_list.extend(current_pdp["meta_rules"]["subject_categories"])
        category_list.extend(current_pdp["meta_rules"]["action_categories"])
        category_list.extend(current_pdp["meta_rules"]["object_categories"])
        for category in category_list:
            if not current_pdp['target'][category]:
                LOG.warning("Empty assignment detected: {} target={}".format(category, current_pdp['target']))
                return False, "Empty assignment detected..."
            scopes_list.append(current_pdp['target'][category])
        scopes_list.append([True, ])
        rules = PolicyManager.get_rules_dict(user_id="admin",
                                             policy_id=self.policy_id,
                                             meta_rule_id=current_header_id).values()
        for item in itertools.product(*scopes_list):
            if list(item) in rules:
                return True, ""
        LOG.warning("No rule match the request...")
        return False, "No rule match the request..."

    def authz(self, ctx, args):
        LOG.info("authz {}".format(ctx))
        keystone_project_id = ctx["id"]
        try:
            if "authz_context" not in ctx:
                ctx["authz_context"] = Context(keystone_project_id,
                                               ctx["subject_name"],
                                               ctx["object_name"],
                                               ctx["action_name"],
                                               ctx["request_id"]).to_dict()
                LOG.info("Context={}".format(ctx["authz_context"]))
            else:
                ctx["authz_context"].index += 1
            result, message = self.__check_rules(ctx["authz_context"])
            # if ctx["authz_context"].index < len(ctx["authz_context"].headers):
            del ctx["authz_context"]
            return {"authz": result,
                    "error": message,
                    "pdp_id": self.pdp_id,
                    "ctx": ctx, "args": args}
        except Exception as e:
            try:
                LOG.error(ctx["authz_context"])
                # del ctx["authz_context"]
            except KeyError:
                LOG.error("Cannot find \"authz_context\" in context")
            LOG.error(e, exc_info=True)
            return {"authz": False,
                    "error": str(e),
                    "pdp_id": self.pdp_id,
                    "ctx": ctx, "args": args}

