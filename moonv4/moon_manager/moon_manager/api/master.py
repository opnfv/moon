# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from oslo_log import log as logging
from moon_utilities.security_functions import call, notify
from moon_db.core import PDPManager, PolicyManager, ModelManager

LOG = logging.getLogger(__name__)


class Master(object):
    """
    Retrieve the current status of all components.
    """

    __version__ = "0.1.0"
    __policies = None
    __policy_ids = []
    __models = None
    __model_ids = []
    __meta_rules = None
    __meta_rule_ids = []

    @property
    def policies(self):
        if not self.__policies:
            self.__policies = {}
            if self.__policy_ids:
                for policy_id in self.__policy_ids:
                    self.__policies.update(call("moon_manager",
                                                method="get_policies",
                                                ctx={
                                                    "id": policy_id,
                                                    "call_master": True,
                                                    "user_id": "admin"
                                                },
                                                args={})["policies"])
            else:
                self.__policies = call("moon_manager",
                                       method="get_policies",
                                       ctx={
                                           "id": None,
                                           "call_master": True,
                                           "user_id": "admin"
                                       },
                                       args={})["policies"]
        LOG.info("__get_policies={}".format(self.__policies))
        return self.__policies

    @property
    def models(self):
        if not self.__models:
            self.__models = {}
            if self.__model_ids:
                for model_id in self.__model_ids:
                    self.__models.update(call("moon_manager",
                                              method="get_models",
                                              ctx={
                                                  "id": model_id,
                                                  "call_master": True,
                                                  "user_id": "admin"
                                              },
                                              args={})["models"])
            else:
                self.__models = call("moon_manager",
                                     method="get_models",
                                     ctx={
                                         "id": None,
                                         "call_master": True,
                                         "user_id": "admin"
                                     },
                                     args={})["models"]
        LOG.info("__get_models={}".format(self.__models))
        return self.__models

    @property
    def meta_rules(self):
        if not self.__meta_rules:
            self.__meta_rules = {}
            if self.__meta_rule_ids:
                for meta_rule_id in self.__meta_rule_ids:
                    self.__meta_rules.update(call("moon_manager",
                                                  method="get_meta_rules",
                                                  ctx={
                                                      "meta_rule_id": meta_rule_id,
                                                      "call_master": True,
                                                      "user_id": "admin"
                                                  },
                                                  args={})["meta_rules"])
            else:
                self.__meta_rules = call("moon_manager",
                                         method="get_meta_rules",
                                         ctx={
                                             "meta_rule_id": None,
                                             "call_master": True,
                                             "user_id": "admin"
                                         },
                                         args={})["meta_rules"]
        LOG.info("__get_meta_rules={}".format(self.__meta_rules))
        return self.__meta_rules

    def __add_meta_data(self):
        subject_categories = ModelManager.get_subject_categories("admin")
        object_categories = ModelManager.get_object_categories("admin")
        action_categories = ModelManager.get_action_categories("admin")
        for meta_rule_id, meta_rule_value in self.meta_rules.items():
            for _scat in meta_rule_value['subject_categories']:
                if _scat not in subject_categories:
                    master_category = call("moon_manager", method="get_subject_categories",
                                           ctx={
                                               "user_id": "admin",
                                               "call_master": True,
                                               "id": None,
                                           },
                                           args={"category_id": _scat})["subject_categories"]
                    ModelManager.add_subject_category("admin", _scat, master_category[_scat])
            for _ocat in meta_rule_value['object_categories']:
                if _ocat not in object_categories:
                    master_category = call("moon_manager", method="get_object_categories",
                                           ctx={
                                               "user_id": "admin",
                                               "call_master": True,
                                               "id": None,
                                           },
                                           args={"category_id": _ocat})["object_categories"]
                    LOG.info("Add scat {} {}".format(_ocat, master_category[_ocat]))
                    ModelManager.add_object_category("admin", _ocat, master_category[_ocat])
            for _acat in meta_rule_value['action_categories']:
                if _acat not in action_categories:
                    master_category = call("moon_manager", method="get_action_categories",
                                           ctx={
                                               "user_id": "admin",
                                               "call_master": True,
                                               "id": None,
                                           },
                                           args={"category_id": _acat})["action_categories"]
                    LOG.info("Add scat {} {}".format(_acat, master_category[_acat]))
                    ModelManager.add_action_category("admin", _acat, master_category[_acat])

    def __add_meta_rule(self):
        meta_rules = ModelManager.get_meta_rules("admin")
        for uuid, value in self.meta_rules.items():
            if uuid not in meta_rules:
                ModelManager.add_meta_rule("admin", uuid, value=value)

    def __add_perimeter(self, subject_name=None, object_name=None):
        for policy_id in self.policies:
            subjects = call("moon_manager", method="get_subjects",
                            ctx={
                                "user_id": "admin",
                                "call_master": True,
                                "id": policy_id,
                            },
                            args={"perimeter_id": None, "perimeter_name": subject_name})["subjects"]
            for subject_id, subject_value in subjects.items():
                # FIXME (asteroide): if a subject with the same name had been already created before
                #                    it will not have the same ID as the subject in master
                PolicyManager.add_subject("admin", policy_id=policy_id, perimeter_id=subject_id, value=subject_value)
        for policy_id in self.policies:
            objects = call("moon_manager", method="get_objects",
                           ctx={
                               "user_id": "admin",
                               "call_master": True,
                               "id": policy_id,
                           },
                           args={"perimeter_id": None, "perimeter_name": object_name})["objects"]
            for object_id, object_value in objects.items():
                # FIXME (asteroide): if a object with the same name had been already created before
                #                    it will not have the same ID as the object in master
                PolicyManager.add_object("admin", policy_id=policy_id, perimeter_id=object_id, value=object_value)
        for policy_id in self.policies:
            actions = call("moon_manager", method="get_actions",
                           ctx={
                               "user_id": "admin",
                               "call_master": True,
                               "id": policy_id,
                           },
                           args={"perimeter_id": None})["actions"]
            for action_id, action_value in actions.items():
                # FIXME (asteroide): if a action with the same name had been already created before
                #                    it will not have the same ID as the action in master
                PolicyManager.add_action("admin", policy_id=policy_id, perimeter_id=action_id, value=action_value)

    def __add_data(self):
        subject_categories = ModelManager.get_subject_categories("admin")
        object_categories = ModelManager.get_object_categories("admin")
        action_categories = ModelManager.get_action_categories("admin")
        for policy_id in self.policies:
            for category in subject_categories.keys():
                subject_data = call("moon_manager", method="get_subject_data",
                                    ctx={
                                        "user_id": "admin",
                                        "call_master": True,
                                        "id": policy_id,
                                        "category_id": category
                                    },
                                    args={"data_id": None})["subject_data"]
                if not subject_data:
                    continue
                for data in subject_data:
                    PolicyManager.set_subject_data("admin", policy_id=policy_id,
                                                   category_id=data['category_id'], value=data)
            for category in object_categories:
                object_data = call("moon_manager", method="get_object_data",
                                   ctx={
                                       "user_id": "admin",
                                       "call_master": True,
                                       "id": policy_id,
                                       "category_id": category
                                   },
                                   args={"data_id": None})["object_data"]
                if not object_data:
                    continue
                for data in object_data:
                    PolicyManager.add_object_data("admin", policy_id=policy_id,
                                                  category_id=data['category_id'], value=data)
            for category in action_categories:
                action_data = call("moon_manager", method="get_action_data",
                                   ctx={
                                       "user_id": "admin",
                                       "call_master": True,
                                       "id": policy_id,
                                       "category_id": category
                                   },
                                   args={"data_id": None})["action_data"]
                if not action_data:
                    continue
                for data in action_data:
                    PolicyManager.add_action_data("admin", policy_id=policy_id,
                                                  category_id=data['category_id'], value=data)

    def __add_assignments(self, subject_name=None, object_name=None):
        for policy_id in self.policies:
            assignments = call("moon_manager", method="get_subject_assignments",
                               ctx={
                                   "user_id": "admin",
                                   "call_master": True,
                                   "id": policy_id,
                                   "perimeter_id": None,
                                   "perimeter_name": subject_name,
                                   "category_id": None,
                               },
                               args={})["subject_assignments"]
            for assignment_id, assignment_value in assignments.items():
                _subject_id = assignment_value['subject_id']
                _category_id = assignment_value['category_id']
                for _data_id in assignment_value['assignments']:
                    PolicyManager.add_subject_assignment("admin", policy_id=policy_id,
                                                         subject_id=_subject_id, category_id=_category_id,
                                                         data_id=_data_id)
            assignments = call("moon_manager", method="get_object_assignments",
                               ctx={
                                   "user_id": "admin",
                                   "call_master": True,
                                   "id": policy_id,
                                   "perimeter_id": None,
                                   "perimeter_name": object_name,
                                   "category_id": None,
                               },
                               args={})["object_assignments"]
            for assignment_id, assignment_value in assignments.items():
                _object_id = assignment_value['object_id']
                _category_id = assignment_value['category_id']
                for _data_id in assignment_value['assignments']:
                    PolicyManager.add_object_assignment("admin", policy_id=policy_id,
                                                        object_id=_object_id, category_id=_category_id,
                                                        data_id=_data_id)
            assignments = call("moon_manager", method="get_action_assignments",
                               ctx={
                                   "user_id": "admin",
                                   "call_master": True,
                                   "id": policy_id,
                                   "perimeter_id": None,
                                   "category_id": None,
                               },
                               args={})["action_assignments"]
            for assignment_id, assignment_value in assignments.items():
                _action_id = assignment_value['action_id']
                _category_id = assignment_value['category_id']
                for _data_id in assignment_value['assignments']:
                    PolicyManager.add_action_assignment("admin", policy_id=policy_id,
                                                        action_id=_action_id, category_id=_category_id,
                                                        data_id=_data_id)

    def __add_rules(self):
        for policy_id in self.policies:
            _rules = call("moon_manager", method="get_rules",
                          ctx={
                              "user_id": "admin",
                              "call_master": True,
                              "id": policy_id,
                              "rule_id": None
                          },
                          args={})["rules"]
            for rule in _rules["rules"]:
                LOG.info("__add_rules {}".format(rule))
                if rule["meta_rule_id"] in self.__meta_rule_ids:
                    PolicyManager.add_rule("admin",
                                           policy_id=policy_id,
                                           meta_rule_id=rule["meta_rule_id"],
                                           value=rule)

    def update_from_master(self, ctx, args):
        LOG.info("update_from_master {}".format(ctx))
        if "security_pipeline" in ctx:
            self.__policy_ids = ctx["security_pipeline"]

            for policy_id, policy_value in self.policies.items():
                self.__model_ids.append(policy_value["model_id"])

            for model_id, model_value in self.models.items():
                self.__meta_rule_ids.extend(model_value['meta_rules'])

            self.__add_meta_data()

            self.__add_meta_rule()

            for policy_id in ctx["security_pipeline"]:
                if policy_id in self.policies:
                    res = PolicyManager.add_policy("admin", policy_id, self.__policies[policy_id])

        self.__add_perimeter(subject_name=ctx.get("subject_name"), object_name=ctx.get("object_name"))

        self.__add_data()

        self.__add_assignments(subject_name=ctx.get("subject_name"), object_name=ctx.get("object_name"))

        self.__add_rules()

        models = ModelManager.get_models("admin")
        for model_id, model_value in self.models.items():
            if model_id not in models:
                ModelManager.add_model("admin", model_id, model_value)

        if args:
            pdp = PDPManager.add_pdp(user_id="admin", pdp_id=ctx["pdp_id"], value=args)
            if "error" in pdp:
                LOG.error("Error when adding PDP from master {}".format(pdp))
                return False
            call("orchestrator", method="add_container",
                 ctx={"id": ctx.get("id"), "pipeline": ctx['security_pipeline']})
        return True

