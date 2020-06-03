# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
from uuid import uuid4
from moon_manager.api.db.managers import Managers
from moon_manager.pip_driver import InformationManager
from moon_utilities.security_functions import enforce
from moon_utilities import exceptions
from moon_manager import pip_driver


logger = logging.getLogger("moon.db.api.policy")


class PolicyManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.PolicyManager = self

    def get_policy_from_meta_rules(self, moon_user_id, meta_rule_id):
        policies = self.PolicyManager.get_policies("admin")
        models = self.ModelManager.get_models("admin")
        for pdp_key, pdp_value in self.PDPManager.get_pdp(moon_user_id=moon_user_id).items():
            if 'security_pipeline' not in pdp_value:
                raise exceptions.PdpContentError
            for policy_id in pdp_value["security_pipeline"]:
                if not policies or policy_id not in policies:
                    raise exceptions.PolicyUnknown
                model_id = policies[policy_id]["model_id"]
                if not models:
                    raise exceptions.ModelUnknown
                if model_id not in models:
                    raise exceptions.ModelUnknown
                if meta_rule_id in models[model_id]["meta_rules"]:
                    return policy_id

    @enforce(("read", "write"), "policies")
    def update_policy(self, moon_user_id, policy_id, value):

        if not value or not value['name'].strip():
            raise exceptions.PolicyContentError

        policy_list = self.driver.get_policies(policy_id=policy_id)
        if not policy_id or policy_id not in policy_list:
            raise exceptions.PolicyUnknown

        policies = self.driver.get_policies(policy_name=value['name'])
        if policies and not (policy_id in policies):
            raise exceptions.PolicyExisting("Policy name Existed")

        if 'model_id' in value and value['model_id']:
            if not value['model_id'].strip() or not Managers.ModelManager.get_models(
                    moon_user_id=moon_user_id, model_id=value['model_id']):
                raise exceptions.ModelUnknown

        policy_obj = policy_list[policy_id]
        if policy_obj["model_id"] and policy_obj["model_id"] != value['model_id']:
            raise exceptions.PolicyUpdateError("Model is not empty")

        return self.driver.update_policy(policy_id=policy_id, value=value)

    @enforce(("read", "write"), "policies")
    def delete_policy(self, moon_user_id, policy_id):
        # TODO (asteroide): unmap PDP linked to that policy
        if policy_id not in self.driver.get_policies(policy_id=policy_id):
            raise exceptions.PolicyUnknown
        pdps = self.PDPManager.get_pdp(moon_user_id=moon_user_id)
        for pdp in pdps:
            if policy_id in pdps[pdp]['security_pipeline']:
                self.PDPManager.delete_policy_from_pdp(moon_user_id=moon_user_id,
                                                       pdp_id=pdp,
                                                       policy_id=policy_id)

        subject_data = self.get_subject_data(moon_user_id=moon_user_id, policy_id=policy_id)
        if subject_data:
            for subject_data_obj in subject_data:
                if subject_data_obj and subject_data_obj["data"]:
                    for subject_data_id in subject_data_obj['data']:
                        self.delete_subject_data(moon_user_id=moon_user_id, policy_id=policy_id,
                                                 data_id=subject_data_id)

        object_data = self.get_object_data(moon_user_id=moon_user_id, policy_id=policy_id)
        if object_data:
            for object_data_obj in object_data:
                if object_data_obj and object_data_obj["data"]:
                    for object_data_id in object_data_obj['data']:
                        self.delete_object_data(moon_user_id=moon_user_id, policy_id=policy_id,
                                                data_id=object_data_id)
        action_data = self.get_action_data(moon_user_id=moon_user_id, policy_id=policy_id)
        if action_data:
            for action_data_obj in action_data:
                if action_data_obj and action_data_obj["data"]:
                    for action_data_id in action_data_obj['data']:
                        self.delete_action_data(moon_user_id=moon_user_id, policy_id=policy_id,
                                                data_id=action_data_id)

        subjects = self.driver.get_subjects(policy_id=policy_id)
        if subjects:
            for subject_id in subjects:
                self.delete_subject(moon_user_id=moon_user_id, policy_id=policy_id,
                                    perimeter_id=subject_id)
        objects = self.driver.get_objects(policy_id=policy_id)
        if objects:
            for object_id in objects:
                self.delete_object(moon_user_id=moon_user_id, policy_id=policy_id,
                                   perimeter_id=object_id)
        actions = self.driver.get_actions(policy_id=policy_id)
        if actions:
            for action_id in actions:
                self.delete_action(moon_user_id=moon_user_id, policy_id=policy_id,
                                   perimeter_id=action_id)

        # rules = self.driver.get_rules(policy_id=policy_id)["rules"]
        # if rules:
        #     for rule_id in rules:
        #         self.delete_rule(moon_user_id=moon_user_id, policy_id=policy_id, rules=rule_id)

        return self.driver.delete_policy(policy_id=policy_id)

    @enforce(("read", "write"), "policies")
    def add_policy(self, moon_user_id, policy_id=None, value=None):

        if not value or not value['name'].strip():
            raise exceptions.PolicyContentError
        if policy_id in self.driver.get_policies(policy_id=policy_id):
            raise exceptions.PolicyExisting

        if self.driver.get_policies(policy_name=value['name']):
            raise exceptions.PolicyExisting("Policy name Existed")

        if not policy_id:
            policy_id = uuid4().hex
        if 'model_id' in value and value['model_id'] != "":
            model_id = value['model_id']
            if model_id is None:
                raise exceptions.ModelUnknown
            else:
                model_list = Managers.ModelManager.get_models(moon_user_id=moon_user_id,
                                                     model_id=model_id)
            if not model_list:
                raise exceptions.ModelUnknown

            self.__check_blank_model(model_list[model_id])

        return self.driver.add_policy(policy_id=policy_id, value=value)

    @enforce("read", "policies")
    def get_policies(self, moon_user_id, policy_id=None):
        return self.driver.get_policies(policy_id=policy_id)

    @enforce("read", "perimeter")
    def get_subjects(self, moon_user_id, policy_id, perimeter_id=None):
        # if not policy_id:
        #    raise exceptions.PolicyUnknown
        if policy_id and (not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown
        return self.driver.get_subjects(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce(("read", "write"), "perimeter")
    def add_subject(self, moon_user_id, policy_id=None, perimeter_id=None, value=None):

        logger.debug("add_subject {}".format(policy_id))
        if not value or "name" not in value or not value["name"].strip():
            raise exceptions.PerimeterContentError('invalid name')

        if 'policy_list' in value:
            raise exceptions.PerimeterContentError("body should not contain policy_list")

        if policy_id and (not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown

        if perimeter_id:
            subjects = self.driver.get_subjects(policy_id=None, perimeter_id=perimeter_id)
            if subjects and subjects[perimeter_id]['name'] != value['name']:
                raise exceptions.PerimeterContentError

        if not perimeter_id:
            subject_per = self.driver.get_subject_by_name(value['name'])
            if subject_per:
                perimeter_id = next(iter(subject_per))

        # should get k_user = {'users':[{"id":"11111"}]} from Keystone
        # FIXME: need to check other input
        # k_user = InformationManager.get_users(username=value.get('name'))
        #
        # if not k_user.get('users', {}):
        #     k_user = InformationManager.add_user(**value)
        # if k_user:
        #     if not perimeter_id:
        #         try:
        #             logger.info("k_user={}".format(k_user))
        #             perimeter_id = k_user['users'][0].get('id', uuid4().hex)
        #         except IndexError:
        #             k_user = InformationManager.get_users(value.get('name'))
        #             perimeter_id = uuid4().hex
        #         except KeyError:
        #             k_user = InformationManager.get_users(value.get('name'))
        #             perimeter_id = uuid4().hex
        #
        #     try:
        #         value.update(k_user['users'][0])
        #     except IndexError:
        #         logger.error("Cannot update user from external server data, got {}".format(k_user))

        return self.driver.set_subject(policy_id=policy_id, perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def update_subject(self, moon_user_id, perimeter_id, value):
        logger.debug("update_subject perimeter_id = {}".format(perimeter_id))

        if not perimeter_id:
            raise exceptions.SubjectUnknown

        subjects = self.driver.get_subjects(policy_id=None, perimeter_id=perimeter_id)
        if not subjects or not (perimeter_id in subjects):
            raise exceptions.PerimeterContentError

        if 'policy_list' in value or ('name' in value and not value['name']):
            raise exceptions.PerimeterContentError

        return self.driver.update_subject(perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def delete_subject(self, moon_user_id, policy_id, perimeter_id):

        if not perimeter_id:
            raise exceptions.SubjectUnknown

        # if not policy_id:
        #     raise exceptions.PolicyUnknown

        if not self.get_subjects(moon_user_id=moon_user_id, policy_id=policy_id,
                                 perimeter_id=perimeter_id):
            raise exceptions.SubjectUnknown

        if policy_id:
            if not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id):
                raise exceptions.PolicyUnknown

            subj_assig = self.driver.get_subject_assignments(policy_id=policy_id,
                                                             subject_id=perimeter_id)
            if subj_assig:
                assign_id = next(iter(subj_assig))
                for data_id in subj_assig[assign_id]['assignments']:
                    self.delete_subject_assignment(moon_user_id=moon_user_id,
                                                   policy_id=policy_id,
                                                   subject_id=perimeter_id,
                                                   category_id=subj_assig[assign_id]['category_id'],
                                                   data_id=data_id)

        return self.driver.delete_subject(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce("read", "perimeter")
    def get_objects(self, moon_user_id, policy_id, perimeter_id=None):
        # if not policy_id:
        #     pass
        if policy_id and (not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown
        return self.driver.get_objects(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce(("read", "write"), "perimeter")
    def add_object(self, moon_user_id, policy_id, perimeter_id=None, value=None):
        logger.debug("add_object {}".format(policy_id))

        if not value or "name" not in value or not value["name"].strip():
            raise exceptions.PerimeterContentError('invalid name')

        if 'policy_list' in value:
            raise exceptions.PerimeterContentError("body should not contain policy_list")

        if policy_id and (not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown

        # object_perimeter = {}
        # if perimeter_id:
        #     object_perimeter = self.driver.get_objects(policy_id=None, perimeter_id=perimeter_id)
        #     if not object_perimeter:
        #         raise exceptions.PerimeterContentError
        # empeche l'ajout d'un objet avec un id prédéterminé

        if not perimeter_id:
            object_perimeter = self.driver.get_object_by_name(value['name'])
            if object_perimeter:
                perimeter_id = next(iter(object_perimeter))

        if perimeter_id:
            objects = self.driver.get_objects(policy_id=None, perimeter_id=perimeter_id)
            if objects and objects[perimeter_id]['name'] != value['name']:
                raise exceptions.PerimeterContentError

        if not perimeter_id:
            perimeter_id = uuid4().hex
        return self.driver.set_object(policy_id=policy_id, perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def update_object(self, moon_user_id, perimeter_id, value):
        logger.debug("update_object perimeter_id = {}".format(perimeter_id))

        if not perimeter_id:
            raise exceptions.ObjectUnknown

        objects = self.driver.get_objects(policy_id=None, perimeter_id=perimeter_id)
        if not objects or not (perimeter_id in objects):
            raise exceptions.PerimeterContentError

        if 'policy_list' in value or ('name' in value and not value['name']):
            raise exceptions.PerimeterContentError

        return self.driver.update_object(perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def delete_object(self, moon_user_id, policy_id, perimeter_id):

        if not perimeter_id:
            raise exceptions.ObjectUnknown

        # if not policy_id:
        #     raise exceptions.PolicyUnknown

        if not self.get_objects(moon_user_id=moon_user_id, policy_id=policy_id,
                                perimeter_id=perimeter_id):
            raise exceptions.ObjectUnknown

        if policy_id:

            if not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id):
                raise exceptions.PolicyUnknown

            obj_assig = self.driver.get_object_assignments(policy_id=policy_id, object_id=perimeter_id)

            if obj_assig:
                assign_id = next(iter(obj_assig))
                for data_id in obj_assig[assign_id]['assignments']:
                    self.delete_object_assignment(moon_user_id,
                                                  policy_id=policy_id,
                                                  object_id=perimeter_id,
                                                  category_id=obj_assig[assign_id]['category_id'],
                                                  data_id=data_id)

        return self.driver.delete_object(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce("read", "perimeter")
    def get_actions(self, moon_user_id, policy_id, perimeter_id=None):

        if policy_id and (not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown
        return self.driver.get_actions(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce(("read", "write"), "perimeter")
    def add_action(self, moon_user_id, policy_id, perimeter_id=None, value=None):
        logger.debug("add_action {}".format(policy_id))

        if not value or "name" not in value or not value["name"].strip():
            raise exceptions.PerimeterContentError('invalid name')

        if 'policy_list' in value:
            raise exceptions.PerimeterContentError("body should not contain policy_list")

        if policy_id and (not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown

        action_perimeter = {}
        if perimeter_id:
            action_perimeter = self.driver.get_actions(policy_id=None, perimeter_id=perimeter_id)
            if not action_perimeter:
                raise exceptions.PerimeterContentError

        if not perimeter_id:
            action_perimeter = self.driver.get_action_by_name(value['name'])
            if action_perimeter:
                perimeter_id = next(iter(action_perimeter))

        if perimeter_id and action_perimeter[perimeter_id]['name'] != value['name']:
            raise exceptions.PerimeterContentError

        if not perimeter_id:
            perimeter_id = uuid4().hex

        return self.driver.set_action(policy_id=policy_id, perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def update_action(self, moon_user_id, perimeter_id, value):
        logger.debug("update_action perimeter_id = {}".format(perimeter_id))

        if not perimeter_id:
            raise exceptions.ActionUnknown

        actions = self.driver.get_actions(policy_id=None, perimeter_id=perimeter_id)
        if not actions or not (perimeter_id in actions):
            raise exceptions.PerimeterContentError

        if 'policy_list' in value or ('name' in value and not value['name'].strip()):
            raise exceptions.PerimeterContentError

        return self.driver.update_action(perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def delete_action(self, moon_user_id, policy_id, perimeter_id):

        if not perimeter_id:
            raise exceptions.ActionUnknown

        # if not policy_id:
        #     raise exceptions.PolicyUnknown

        if not self.get_actions(moon_user_id=moon_user_id, policy_id=policy_id,
                                perimeter_id=perimeter_id):
            raise exceptions.ActionUnknown

        logger.debug("delete_action {} {} {}".format(policy_id, perimeter_id,
                                                     self.get_policies(moon_user_id=moon_user_id,
                                                                       policy_id=policy_id)))
        if policy_id:
            if not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id):
                raise exceptions.PolicyUnknown

            act_assig = self.driver.get_action_assignments(policy_id=policy_id, action_id=perimeter_id)

            if act_assig:
                assign_id = next(iter(act_assig))
                for data_id in act_assig[assign_id]['assignments']:
                    self.delete_action_assignment(moon_user_id=moon_user_id,
                                                  policy_id=policy_id,
                                                  action_id=perimeter_id,
                                                  category_id=act_assig[assign_id]['category_id'],
                                                  data_id=data_id)

        return self.driver.delete_action(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce("read", "data")
    def get_subject_data(self, moon_user_id, policy_id, data_id=None, category_id=None):
        available_metadata = self.get_available_metadata(moon_user_id=moon_user_id,
                                                         policy_id=policy_id)
        results = []
        if not category_id:
            for cat in available_metadata["subject"]:
                _value = self.driver.get_subject_data(policy_id=policy_id, data_id=data_id,
                                                      category_id=cat)
                results.append(_value)
        if category_id and category_id in available_metadata["subject"]:
            results.append(self.driver.get_subject_data(policy_id=policy_id, data_id=data_id,
                                                        category_id=category_id))
        return results

    @enforce(("read", "write"), "data")
    def set_subject_data(self, moon_user_id, policy_id, data_id=None, category_id=None, value=None):

        logger.debug("set_subject_data policyID {}".format(policy_id))

        if not value or 'name' not in value or not value['name'].strip():
            raise exceptions.DataContentError

        if not policy_id or not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown

        if not category_id or (
                not Managers.ModelManager.get_subject_categories(moon_user_id=moon_user_id,
                                                                 category_id=category_id)):
            raise exceptions.SubjectCategoryUnknown

        self.__category_dependency_validation(moon_user_id, policy_id, category_id,
                                              'subject_categories')

        if not data_id:
            data_id = uuid4().hex
        return self.driver.set_subject_data(policy_id=policy_id, data_id=data_id,
                                            category_id=category_id, value=value)

    @enforce(("read", "write"), "data")
    def delete_subject_data(self, moon_user_id, policy_id, data_id, category_id=None):
        # TODO (asteroide): check and/or delete assignments linked to that data
        subject_assignments = self.get_subject_assignments(moon_user_id=moon_user_id,
                                                           policy_id=policy_id,
                                                           category_id=category_id)
        if subject_assignments:
            for assign_id in subject_assignments:
                self.driver.delete_subject_assignment(
                    policy_id=subject_assignments[assign_id]['policy_id'],
                    subject_id=subject_assignments[assign_id]['subject_id'],
                    category_id=subject_assignments[assign_id]['category_id'],
                    data_id=subject_assignments[assign_id]['id'])

        rules = self.driver.get_rules(policy_id=policy_id)
        if rules['rules']:
            for rule in rules['rules']:
                if data_id in rule['rule']:
                    self.driver.delete_rule(policy_id, rule['id'])

        return self.driver.delete_subject_data(policy_id=policy_id, category_id=category_id,
                                               data_id=data_id)

    @enforce("read", "data")
    def get_object_data(self, moon_user_id, policy_id, data_id=None, category_id=None):
        available_metadata = self.get_available_metadata(moon_user_id=moon_user_id,
                                                         policy_id=policy_id)
        results = []
        if not category_id:
            for cat in available_metadata["object"]:
                results.append(self.driver.get_object_data(policy_id=policy_id, data_id=data_id,
                                                           category_id=cat))
        if category_id and category_id in available_metadata["object"]:
            results.append(self.driver.get_object_data(policy_id=policy_id, data_id=data_id,
                                                       category_id=category_id))
        return results

    @enforce(("read", "write"), "data")
    def add_object_data(self, moon_user_id, policy_id, data_id=None, category_id=None, value=None):
        logger.debug("add_object_data policyID {}".format(policy_id))

        if not value or 'name' not in value or not value['name'].strip():
            raise exceptions.DataContentError

        if not policy_id or not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown

        if not category_id or (
                not Managers.ModelManager.get_object_categories(moon_user_id=moon_user_id,
                                                                category_id=category_id)):
            raise exceptions.ObjectCategoryUnknown

        self.__category_dependency_validation(moon_user_id, policy_id, category_id,
                                              'object_categories')

        if not data_id:
            data_id = uuid4().hex
        return self.driver.set_object_data(policy_id=policy_id, data_id=data_id,
                                           category_id=category_id, value=value)

    @enforce(("read", "write"), "data")
    def delete_object_data(self, moon_user_id, policy_id, data_id, category_id=None):
        # TODO (asteroide): check and/or delete assignments linked to that data
        object_assignments = self.get_object_assignments(moon_user_id=moon_user_id,
                                                         policy_id=policy_id,
                                                         category_id=category_id)

        if object_assignments:
            for assign_id in object_assignments:
                self.driver.delete_object_assignment(
                    policy_id=object_assignments[assign_id]['policy_id'],
                    object_id=object_assignments[assign_id]['object_id'],
                    category_id=object_assignments[assign_id]['category_id'],
                    data_id=object_assignments[assign_id]['id'])

        rules = self.driver.get_rules(policy_id=policy_id)
        if rules['rules']:
            for rule in rules['rules']:
                if data_id in rule['rule']:
                    self.driver.delete_rule(policy_id, rule['id'])

        return self.driver.delete_object_data(policy_id=policy_id, category_id=category_id,
                                              data_id=data_id)

    @enforce("read", "data")
    def get_action_data(self, moon_user_id, policy_id, data_id=None, category_id=None):
        available_metadata = self.get_available_metadata(moon_user_id=moon_user_id,
                                                         policy_id=policy_id)
        results = []
        if not category_id:
            for cat in available_metadata["action"]:
                results.append(self.driver.get_action_data(policy_id=policy_id, data_id=data_id,
                                                           category_id=cat))
        if category_id and category_id in available_metadata["action"]:
            if category_id.startswith("attributes:"):
                data = {}
                attrs = pip_driver.AttrsManager.get_objects(
                    moon_user_id="admin",
                    object_type=category_id.replace("attributes:", ""))
                for item in attrs.keys():
                    data[item] = {"id": item, "name": item, "description": item}
                results.append(
                    {
                        "policy_id": policy_id,
                        "category_id": category_id,
                        "data": data,
                    }
                )
            else:
                results.append(self.driver.get_action_data(policy_id=policy_id,
                                                           data_id=data_id,
                                                           category_id=category_id))
        return results

    @enforce(("read", "write"), "data")
    def add_action_data(self, moon_user_id, policy_id, data_id=None, category_id=None, value=None):

        logger.debug("add_action_data policyID {}".format(policy_id))

        if not value or 'name' not in value or not value['name'].strip():
            raise exceptions.DataContentError

        if not policy_id or not self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown

        if not category_id or (
                not Managers.ModelManager.get_action_categories(moon_user_id=moon_user_id,
                                                                category_id=category_id)):
            raise exceptions.ActionCategoryUnknown

        self.__category_dependency_validation(moon_user_id, policy_id, category_id,
                                              'action_categories')

        if not data_id:
            data_id = uuid4().hex
        return self.driver.set_action_data(policy_id=policy_id, data_id=data_id,
                                           category_id=category_id, value=value)

    @enforce(("read", "write"), "data")
    def delete_action_data(self, moon_user_id, policy_id, data_id, category_id=None):
        # TODO (asteroide): check and/or delete assignments linked to that data
        action_assignments = self.get_action_assignments(moon_user_id=moon_user_id,
                                                         policy_id=policy_id,
                                                         category_id=category_id)
        if action_assignments:
            for assign_id in action_assignments:
                self.driver.delete_action_assignment(
                    policy_id=action_assignments[assign_id]['policy_id'],
                    action_id=action_assignments[assign_id]['action_id'],
                    category_id=action_assignments[assign_id]['category_id'],
                    data_id=action_assignments[assign_id]['id'])

        rules = self.driver.get_rules(policy_id=policy_id)
        if rules['rules']:
            for rule in rules['rules']:
                if data_id in rule['rule']:
                    self.driver.delete_rule(policy_id, rule['id'])

        return self.driver.delete_action_data(policy_id=policy_id, category_id=category_id,
                                              data_id=data_id)

    @enforce("read", "assignments")
    def get_subject_assignments(self, moon_user_id, policy_id, subject_id=None, category_id=None):
        return self.driver.get_subject_assignments(policy_id=policy_id, subject_id=subject_id,
                                                   category_id=category_id)

    @enforce(("read", "write"), "assignments")
    def add_subject_assignment(self, moon_user_id, policy_id, subject_id, category_id, data_id):

        logger.debug("add_subject_assignment policyID {}".format(policy_id))
        if not category_id or (
                not Managers.ModelManager.get_subject_categories(moon_user_id=moon_user_id,
                                                                 category_id=category_id)):
            raise exceptions.SubjectCategoryUnknown

        self.__category_dependency_validation(moon_user_id, policy_id, category_id,
                                              'subject_categories')

        if not subject_id or (
                not self.get_subjects(moon_user_id=moon_user_id, policy_id=policy_id,
                                      perimeter_id=subject_id)):
            raise exceptions.SubjectUnknown
        subjects_data = self.get_subject_data(moon_user_id=moon_user_id, policy_id=policy_id,
                                              data_id=data_id, category_id=category_id)
        if not data_id or not subjects_data or data_id not in subjects_data[0]['data']:
            raise exceptions.DataUnknown

        return self.driver.add_subject_assignment(policy_id=policy_id, subject_id=subject_id,
                                                  category_id=category_id, data_id=data_id)

    @enforce(("read", "write"), "assignments")
    def delete_subject_assignment(self, moon_user_id, policy_id, subject_id, category_id, data_id):
        if policy_id:
            return self.driver.delete_subject_assignment(
                policy_id=policy_id, subject_id=subject_id,
                category_id=category_id, data_id=data_id)
        raise exceptions.PolicyUnknown

    @enforce("read", "assignments")
    def get_object_assignments(self, moon_user_id, policy_id, object_id=None, category_id=None):
        return self.driver.get_object_assignments(policy_id=policy_id, object_id=object_id,
                                                  category_id=category_id)

    @enforce(("read", "write"), "assignments")
    def add_object_assignment(self, moon_user_id, policy_id, object_id, category_id, data_id):

        logger.debug("add_object_assignment policyID {}".format(policy_id))
        if not category_id or (
                not Managers.ModelManager.get_object_categories(moon_user_id=moon_user_id,
                                                                category_id=category_id)):
            raise exceptions.ObjectCategoryUnknown

        self.__category_dependency_validation(moon_user_id, policy_id, category_id,
                                              'object_categories')

        if not object_id or (
                not self.get_objects(moon_user_id=moon_user_id, policy_id=policy_id,
                                     perimeter_id=object_id)):
            raise exceptions.ObjectUnknown
        objects_data = self.get_object_data(moon_user_id=moon_user_id, policy_id=policy_id,
                                            data_id=data_id, category_id=category_id)
        if not data_id or not objects_data or data_id not in objects_data[0]['data']:
            raise exceptions.DataUnknown

        return self.driver.add_object_assignment(policy_id=policy_id, object_id=object_id,
                                                 category_id=category_id, data_id=data_id)

    @enforce(("read", "write"), "assignments")
    def delete_object_assignment(self, moon_user_id, policy_id, object_id, category_id, data_id):
        if policy_id:
            return self.driver.delete_object_assignment(policy_id=policy_id, object_id=object_id,
                                                        category_id=category_id, data_id=data_id)
        raise exceptions.PolicyUnknown

    @enforce("read", "assignments")
    def get_action_assignments(self, moon_user_id, policy_id, action_id=None, category_id=None):
        return self.driver.get_action_assignments(policy_id=policy_id, action_id=action_id,
                                                  category_id=category_id)

    @enforce(("read", "write"), "assignments")
    def add_action_assignment(self, moon_user_id, policy_id, action_id, category_id, data_id):

        logger.debug("add_action_assignment policyID {}".format(policy_id))

        if not category_id or (
                not Managers.ModelManager.get_action_categories(moon_user_id=moon_user_id,
                                                                category_id=category_id)):
            raise exceptions.ActionCategoryUnknown

        self.__category_dependency_validation(moon_user_id, policy_id, category_id,
                                              'action_categories')

        if not action_id or (
                not self.get_actions(moon_user_id=moon_user_id, policy_id=policy_id,
                                     perimeter_id=action_id)):
            raise exceptions.ActionUnknown
        actions_data = self.get_action_data(moon_user_id=moon_user_id, policy_id=policy_id,
                                            data_id=data_id, category_id=category_id)
        if not data_id or not actions_data or data_id not in actions_data[0]['data']:
            raise exceptions.DataUnknown

        return self.driver.add_action_assignment(policy_id=policy_id, action_id=action_id,
                                                 category_id=category_id, data_id=data_id)

    @enforce(("read", "write"), "assignments")
    def delete_action_assignment(self, moon_user_id, policy_id, action_id, category_id, data_id):
        if policy_id:
            return self.driver.delete_action_assignment(policy_id=policy_id, action_id=action_id,
                                                        category_id=category_id, data_id=data_id)
        raise exceptions.PolicyUnknown

    @enforce("read", "rules")
    def get_rules(self, moon_user_id, policy_id, meta_rule_id=None, rule_id=None):
        return self.driver.get_rules(policy_id=policy_id, meta_rule_id=meta_rule_id,
                                     rule_id=rule_id)

    @enforce(("read", "write"), "policies")
    def update_rule(self, moon_user_id, rule_id, value):
        if not value or 'instructions' not in value:
            raise exceptions.RuleContentError

        rule_list = self.driver.get_rules(policy_id=None, rule_id=rule_id)
        if not rule_id or rule_id not in rule_list:
            raise exceptions.RuleUnknown

        return self.driver.update_rule(rule_id=rule_id, value=value)

    @enforce(("read", "write"), "rules")
    def add_rule(self, moon_user_id, policy_id, meta_rule_id, value):

        if not meta_rule_id or (
                not self.ModelManager.get_meta_rules(moon_user_id=moon_user_id,
                                                     meta_rule_id=meta_rule_id)):
            raise exceptions.MetaRuleUnknown

        if not value or 'instructions' not in value:  # TODO or not value['instructions']:
            raise exceptions.MetaRuleContentError

        decision_exist = False
        default_instruction = {"decision": "grant"}

        for instruction in value['instructions']:
            if 'decision' in instruction:
                decision_exist = True
                if not instruction['decision']:
                    instruction['decision'] = default_instruction['decision']
                elif instruction['decision'].lower() not in ['grant', 'deny', 'continue']:
                    raise exceptions.RuleContentError("Invalid Decision")

        if not decision_exist:
            value['instructions'].append(default_instruction)

        self.__dependencies_validation(moon_user_id, policy_id, meta_rule_id)

        self.__check_existing_rule(policy_id=policy_id, meta_rule_id=meta_rule_id,
                                   moon_user_id=moon_user_id, rule_value=value)

        return self.driver.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)

    def __check_existing_rule(self, moon_user_id, policy_id, meta_rule_id, rule_value):

        if not meta_rule_id:
            raise exceptions.MetaRuleUnknown

        meta_rule = self.ModelManager.get_meta_rules(moon_user_id=moon_user_id,
                                                     meta_rule_id=meta_rule_id)
        if not meta_rule:
            raise exceptions.MetaRuleUnknown

        if len(meta_rule[meta_rule_id]['subject_categories']) + len(
                meta_rule[meta_rule_id]['object_categories']) \
                + len(meta_rule[meta_rule_id]['action_categories']) > len(rule_value['rule']):
            raise exceptions.RuleContentError(message="Missing Data")

        if len(meta_rule[meta_rule_id]['subject_categories']) + len(
                meta_rule[meta_rule_id]['object_categories']) \
                + len(meta_rule[meta_rule_id]['action_categories']) < len(rule_value['rule']):
            raise exceptions.MetaRuleContentError(message="Missing Data")

        temp_rule_data = list(
            rule_value['rule'][0:len(meta_rule[meta_rule_id]['subject_categories'])])
        found_data_counter = 0
        start_sub = len(meta_rule[meta_rule_id]['subject_categories'])

        for sub_cat_id in meta_rule[meta_rule_id]['subject_categories']:
            subjects_data = self.get_subject_data(moon_user_id=moon_user_id,
                                                  category_id=sub_cat_id, policy_id=policy_id)
            if subjects_data:
                found_data_counter = self.__validate_data_id(sub_cat_id, subjects_data[0]['data'],
                                                             temp_rule_data,
                                                             "Missing Subject_category "
                                                             , found_data_counter)

        if found_data_counter != len(meta_rule[meta_rule_id]['subject_categories']):
            raise exceptions.RuleContentError(message="Missing Data")

        _index = start_sub + len(meta_rule[meta_rule_id]['object_categories'])
        temp_rule_data = list(rule_value['rule'][start_sub:_index])
        found_data_counter = 0
        start_sub = start_sub + len(meta_rule[meta_rule_id]['object_categories'])

        for ob_cat_id in meta_rule[meta_rule_id]['object_categories']:
            object_data = self.get_object_data(moon_user_id=moon_user_id,
                                               category_id=ob_cat_id, policy_id=policy_id)
            if object_data:
                found_data_counter = self.__validate_data_id(ob_cat_id, object_data[0]['data'],
                                                             temp_rule_data,
                                                             "Missing Object_category ",
                                                             found_data_counter)

        if found_data_counter != len(meta_rule[meta_rule_id]['object_categories']):
            raise exceptions.RuleContentError(message="Missing Data")

        _index = start_sub + len(meta_rule[meta_rule_id]['action_categories'])
        temp_rule_data = list(rule_value['rule'][start_sub:_index])
        found_data_counter = 0

        for act_cat_id in meta_rule[meta_rule_id]['action_categories']:
            action_data = self.get_action_data(moon_user_id=moon_user_id, category_id=act_cat_id,
                                               policy_id=policy_id)
            if action_data:
                found_data_counter = self.__validate_data_id(act_cat_id, action_data[0]['data'],
                                                             temp_rule_data,
                                                             "Missing Action_category ",
                                                             found_data_counter)

        # Note: adding count of data linked to a global attribute
        found_data_counter += len(list(filter(lambda x: "attributes:" in x, temp_rule_data)))
        if found_data_counter != len(meta_rule[meta_rule_id]['action_categories']):
            raise exceptions.RuleContentError(message="Missing Data")

    @staticmethod
    def __validate_data_id(cat_id, data_ids, temp_rule_data, error_msg, found_data_counter):
        for ID in data_ids:
            if ID in temp_rule_data:
                temp_rule_data.remove(ID)
                found_data_counter += 1
        # if no data id found in the rule, so rule not valid
        if found_data_counter < 1:
            raise exceptions.RuleContentError(message=error_msg + cat_id)
        return found_data_counter

    @enforce(("read", "write"), "rules")
    def delete_rule(self, moon_user_id, policy_id, rule_id):
        return self.driver.delete_rule(policy_id=policy_id, rule_id=rule_id)

    @enforce("read", "meta_data")
    def get_available_metadata(self, moon_user_id, policy_id):
        categories = {
            "subject": [],
            "object": [],
            "action": []
        }
        policy = self.driver.get_policies(policy_id=policy_id)
        if not policy:
            raise exceptions.PolicyUnknown
        model_id = policy[policy_id]["model_id"]
        model = Managers.ModelManager.get_models(moon_user_id=moon_user_id, model_id=model_id)
        try:
            meta_rule_list = model[model_id]["meta_rules"]
            for meta_rule_id in meta_rule_list:
                meta_rule = Managers.ModelManager.get_meta_rules(moon_user_id=moon_user_id,
                                                                 meta_rule_id=meta_rule_id)
                categories["subject"].extend(meta_rule[meta_rule_id]["subject_categories"])
                categories["object"].extend(meta_rule[meta_rule_id]["object_categories"])
                categories["action"].extend(meta_rule[meta_rule_id]["action_categories"])
        finally:
            return categories

    def __dependencies_validation(self, moon_user_id, policy_id, meta_rule_id=None):

        policies = self.get_policies(moon_user_id=moon_user_id, policy_id=policy_id)
        if not policy_id or (not policies):
            raise exceptions.PolicyUnknown

        policy_content = policies[next(iter(policies))]
        model_id = policy_content['model_id']
        models = Managers.ModelManager.get_models(moon_user_id=moon_user_id, model_id=model_id)
        if not model_id or not models:
            raise exceptions.ModelUnknown

        model_content = models[next(iter(models))]
        if meta_rule_id:
            meta_rule_exists = False

            for model_meta_rule_id in model_content['meta_rules']:
                if model_meta_rule_id == meta_rule_id:
                    meta_rule_exists = True
                    break

            if not meta_rule_exists:
                raise exceptions.MetaRuleNotLinkedWithPolicyModel

            meta_rule = self.ModelManager.get_meta_rules(moon_user_id=moon_user_id,
                                                         meta_rule_id=meta_rule_id)
            meta_rule_content = meta_rule[next(iter(meta_rule))]
            if (not meta_rule_content['subject_categories']) or \
                    (not meta_rule_content['object_categories']) or \
                    (not meta_rule_content['action_categories']):
                raise exceptions.MetaRuleContentError
        return model_content

    def __category_dependency_validation(self, moon_user_id, policy_id, category_id, category_key):
        model = self.__dependencies_validation(moon_user_id=moon_user_id, policy_id=policy_id)
        category_found = False
        for model_meta_rule_id in model['meta_rules']:
            meta_rule = self.ModelManager.get_meta_rules(moon_user_id=moon_user_id,
                                                         meta_rule_id=model_meta_rule_id)
            meta_rule_content = meta_rule[next(iter(meta_rule))]
            if meta_rule_content[category_key] and category_id in meta_rule_content[category_key]:
                category_found = True
                break

        if not category_found:
            raise exceptions.CategoryNotAssignedMetaRule

    def __check_blank_model(self, model):
        if 'meta_rules' not in model or not model['meta_rules']:
            raise exceptions.MetaRuleUnknown
        for meta_rule_id in model['meta_rules']:
            self.__check_blank_meta_rule(meta_rule_id)

    def __check_blank_meta_rule(self, meta_rule_id):
        meta_rule = self.driver.get_meta_rules(meta_rule_id=meta_rule_id)
        if not meta_rule:
            return exceptions.MetaRuleUnknown
        meta_rule_content = meta_rule[next(iter(meta_rule))]
        if (not meta_rule_content['subject_categories']) or (
                not meta_rule_content['object_categories']) or (
                not meta_rule_content['action_categories']):
            raise exceptions.MetaRuleContentError

