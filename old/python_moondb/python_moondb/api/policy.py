# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
import logging
from python_moonutilities.security_functions import enforce
from python_moondb.api.managers import Managers
from python_moonutilities import exceptions

# from python_moondb.core import PDPManager

logger = logging.getLogger("moon.db.api.policy")


class PolicyManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.PolicyManager = self

    def get_policy_from_meta_rules(self, user_id, meta_rule_id):
        policies = self.PolicyManager.get_policies("admin")
        models = self.ModelManager.get_models("admin")
        for pdp_key, pdp_value in self.PDPManager.get_pdp(user_id).items():
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
    def update_policy(self, user_id, policy_id, value):

        if not value or not value['name']:
            raise exceptions.PolicyContentError

        policyList = self.driver.get_policies(policy_id=policy_id)
        if not policy_id or policy_id not in policyList:
            raise exceptions.PolicyUnknown

        policies = self.driver.get_policies(policy_name=value['name'])
        if len(policies) and not (policy_id in policies):
            raise exceptions.PolicyExisting("Policy name Existed")

        if 'model_id' in value and value['model_id']:
            if not Managers.ModelManager.get_models(user_id, model_id=value['model_id']):
                raise exceptions.ModelUnknown

        policy_obj = policyList[policy_id]
        if (policy_obj["model_id"] and value["model_id"] != policy_obj["model_id"]):

            subjects = self.driver.get_subjects(policy_id=policy_id)
            if subjects:
                raise exceptions.PolicyUpdateError("Policy is used in subject")
            objects = self.driver.get_objects(policy_id=policy_id)
            if objects:
                raise exceptions.PolicyUpdateError("Policy is used in object")
            actions = self.driver.get_actions(policy_id=policy_id)
            if actions:
                raise exceptions.PolicyUpdateError("Policy is used in action")

            rules = self.driver.get_rules(policy_id=policy_id)["rules"]
            if rules:
                raise exceptions.PolicyUpdateError("Policy is used in rule")

            subject_data = self.get_subject_data(user_id, policy_id=policy_id)
            if subject_data and subject_data[0]["data"]:
                raise exceptions.PolicyUpdateError("Policy is used in subject_data")
            object_data = self.get_object_data(user_id, policy_id=policy_id)
            if object_data and object_data[0]["data"]:
                raise exceptions.PolicyUpdateError("Policy is used in object_data")
            action_data = self.get_action_data(user_id, policy_id=policy_id)
            if action_data and action_data[0]["data"]:
                raise exceptions.PolicyUpdateError("Policy is used in action_data")

        return self.driver.update_policy(policy_id=policy_id, value=value)

    @enforce(("read", "write"), "policies")
    def delete_policy(self, user_id, policy_id):
        # TODO (asteroide): unmap PDP linked to that policy
        if policy_id not in self.driver.get_policies(policy_id=policy_id):
            raise exceptions.PolicyUnknown
        pdps = self.PDPManager.get_pdp(user_id=user_id)
        for pdp in pdps:
            for policy_id in pdps[pdp]['security_pipeline']:
                if policy_id == policy_id:
                    raise exceptions.DeletePolicyWithPdp
        subjects = self.driver.get_subjects(policy_id=policy_id)
        if subjects:
            raise exceptions.DeletePolicyWithPerimeter
        objects = self.driver.get_objects(policy_id=policy_id)
        if objects:
            raise exceptions.DeletePolicyWithPerimeter
        actions = self.driver.get_actions(policy_id=policy_id)
        if actions:
            raise exceptions.DeletePolicyWithPerimeter

        rules = self.driver.get_rules(policy_id=policy_id)["rules"]
        if rules:
            raise exceptions.DeletePolicyWithRules

        subject_data = self.get_subject_data(user_id, policy_id=policy_id)
        if subject_data and subject_data[0]["data"]:
            raise exceptions.DeletePolicyWithData
        object_data = self.get_object_data(user_id, policy_id=policy_id)
        if object_data and object_data[0]["data"]:
            raise exceptions.DeletePolicyWithData
        action_data = self.get_action_data(user_id, policy_id=policy_id)
        if action_data and action_data[0]["data"]:
            raise exceptions.DeletePolicyWithData

        return self.driver.delete_policy(policy_id=policy_id)

    @enforce(("read", "write"), "policies")
    def add_policy(self, user_id, policy_id=None, value=None):

        if not value or not value['name']:
            raise exceptions.PolicyContentError
        if policy_id in self.driver.get_policies(policy_id=policy_id):
            raise exceptions.PolicyExisting

        if len(self.driver.get_policies(policy_name=value['name'])):
            raise exceptions.PolicyExisting("Policy name Existed")

        if not policy_id:
            policy_id = uuid4().hex
        if 'model_id' in value and value['model_id'] != "":
            if not Managers.ModelManager.get_models(user_id, model_id=value['model_id']):
                raise exceptions.ModelUnknown
        return self.driver.add_policy(policy_id=policy_id, value=value)

    @enforce("read", "policies")
    def get_policies(self, user_id, policy_id=None):
        return self.driver.get_policies(policy_id=policy_id)

    @enforce("read", "perimeter")
    def get_subjects(self, user_id, policy_id, perimeter_id=None):
        # if not policy_id:
        #    raise exceptions.PolicyUnknown
        if policy_id and (not self.get_policies(user_id=user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown
        return self.driver.get_subjects(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce(("read", "write"), "perimeter")
    def add_subject(self, user_id, policy_id, perimeter_id=None, value=None):

        if not value or "name" not in value or not value["name"].strip():
            raise exceptions.PerimeterContentError('invalid name')

        if not policy_id or (not self.get_policies(user_id=user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown

        if perimeter_id:
            subjects = self.driver.get_subjects(policy_id=None, perimeter_id=perimeter_id)
            if subjects and subjects[perimeter_id]['name'] != value['name']:
                raise exceptions.PerimeterContentError

        if not perimeter_id:
            subject_per = self.driver.get_subject_by_name(value['name'])
            if len(subject_per):
                perimeter_id = next(iter(subject_per))

        k_user = Managers.KeystoneManager.get_user_by_name(value.get('name'))
        if not k_user['users']:
            k_user = Managers.KeystoneManager.create_user(value)
        if not perimeter_id:
            try:
                logger.info("k_user={}".format(k_user))
                perimeter_id = k_user['users'][0].get('id', uuid4().hex)
            except IndexError:
                k_user = Managers.KeystoneManager.get_user_by_name(
                    value.get('name'))
                perimeter_id = uuid4().hex
            except KeyError:
                k_user = Managers.KeystoneManager.get_user_by_name(
                    value.get('name'))
                perimeter_id = uuid4().hex

        value.update(k_user['users'][0])

        return self.driver.set_subject(policy_id=policy_id, perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def update_subject(self, user_id, perimeter_id, value):
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
    def delete_subject(self, user_id, policy_id, perimeter_id):

        if not perimeter_id:
            raise exceptions.SubjectUnknown

        if not policy_id:
            raise exceptions.PolicyUnknown

        if not self.get_subjects(user_id=user_id, policy_id=policy_id, perimeter_id=perimeter_id):
            raise exceptions.SubjectUnknown

        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown

        subj_assig = self.driver.get_subject_assignments(policy_id=policy_id,
                                                         subject_id=perimeter_id)
        if subj_assig:
            raise exceptions.DeletePerimeterWithAssignment

        return self.driver.delete_subject(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce("read", "perimeter")
    def get_objects(self, user_id, policy_id, perimeter_id=None):
        # if not policy_id:
        #     pass
        if policy_id and (not self.get_policies(user_id=user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown
        return self.driver.get_objects(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce(("read", "write"), "perimeter")
    def add_object(self, user_id, policy_id, perimeter_id=None, value=None):
        if not value or "name" not in value or not value["name"].strip():
            raise exceptions.PerimeterContentError('invalid name')

        if not policy_id or (not self.get_policies(user_id=user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown

        if perimeter_id:
            object_perimeter = self.driver.get_objects(policy_id=None, perimeter_id=perimeter_id)
            if not object_perimeter:
                raise exceptions.PerimeterContentError

        if not perimeter_id:
            object_perimeter = self.driver.get_object_by_name(value['name'])
            if len(object_perimeter):
                perimeter_id = next(iter(object_perimeter))

        if perimeter_id and object_perimeter[perimeter_id]['name'] != value['name']:
            raise exceptions.PerimeterContentError

        if not perimeter_id:
            perimeter_id = uuid4().hex
        return self.driver.set_object(policy_id=policy_id, perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def update_object(self, user_id, perimeter_id, value):
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
    def delete_object(self, user_id, policy_id, perimeter_id):

        if not perimeter_id:
            raise exceptions.ObjectUnknown

        if not policy_id:
            raise exceptions.PolicyUnknown

        if not self.get_objects(user_id=user_id, policy_id=policy_id, perimeter_id=perimeter_id):
            raise exceptions.ObjectUnknown

        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown

        obj_assig = self.driver.get_object_assignments(policy_id=policy_id, object_id=perimeter_id)
        if obj_assig:
            raise exceptions.DeletePerimeterWithAssignment

        return self.driver.delete_object(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce("read", "perimeter")
    def get_actions(self, user_id, policy_id, perimeter_id=None):
        # if not policy_id:
        #     pass
        if policy_id and (not self.get_policies(user_id=user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown
        return self.driver.get_actions(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce(("read", "write"), "perimeter")
    def add_action(self, user_id, policy_id, perimeter_id=None, value=None):
        logger.debug("add_action {}".format(policy_id))

        if not value or "name" not in value or not value["name"].strip():
            raise exceptions.PerimeterContentError('invalid name')

        if not policy_id or (not self.get_policies(user_id=user_id, policy_id=policy_id)):
            raise exceptions.PolicyUnknown

        if perimeter_id:
            action_perimeter = self.driver.get_actions(policy_id=None, perimeter_id=perimeter_id)
            if not action_perimeter:
                raise exceptions.PerimeterContentError

        if not perimeter_id:
            action_perimeter = self.driver.get_action_by_name(value['name'])
            if len(action_perimeter):
                perimeter_id = next(iter(action_perimeter))

        if perimeter_id and action_perimeter[perimeter_id]['name'] != value['name']:
            raise exceptions.PerimeterContentError

        if not perimeter_id:
            perimeter_id = uuid4().hex

        return self.driver.set_action(policy_id=policy_id, perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def update_action(self, user_id, perimeter_id, value):
        logger.debug("update_action perimeter_id = {}".format(perimeter_id))

        if not perimeter_id:
            raise exceptions.ActionUnknown

        actions = self.driver.get_actions(policy_id=None, perimeter_id=perimeter_id)
        if not actions or not (perimeter_id in actions):
            raise exceptions.PerimeterContentError

        if 'policy_list' in value or ('name' in value and not value['name']):
            raise exceptions.PerimeterContentError

        return self.driver.update_action(perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def delete_action(self, user_id, policy_id, perimeter_id):

        if not perimeter_id:
            raise exceptions.ActionUnknown

        if not policy_id:
            raise exceptions.PolicyUnknown

        if not self.get_actions(user_id=user_id, policy_id=policy_id, perimeter_id=perimeter_id):
            raise exceptions.ActionUnknown

        logger.debug("delete_action {} {} {}".format(policy_id, perimeter_id,
                                                     self.get_policies(user_id=user_id,
                                                                       policy_id=policy_id)))
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown

        act_assig = self.driver.get_action_assignments(policy_id=policy_id, action_id=perimeter_id)
        if act_assig:
            raise exceptions.DeletePerimeterWithAssignment
        return self.driver.delete_action(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce("read", "data")
    def get_subject_data(self, user_id, policy_id, data_id=None, category_id=None):
        available_metadata = self.get_available_metadata(user_id, policy_id)
        results = []
        if not category_id:
            for cat in available_metadata["subject"]:
                results.append(self.driver.get_subject_data(policy_id=policy_id, data_id=data_id,
                                                            category_id=cat))
        if category_id and category_id in available_metadata["subject"]:
            results.append(self.driver.get_subject_data(policy_id=policy_id, data_id=data_id,
                                                        category_id=category_id))
        return results

    @enforce(("read", "write"), "data")
    def set_subject_data(self, user_id, policy_id, data_id=None, category_id=None, value=None):
        if not category_id or (
                not Managers.ModelManager.get_subject_categories(user_id=user_id,
                                                                 category_id=category_id)):
            raise exceptions.SubjectCategoryUnknown

        self.__category_dependency_validation(user_id, policy_id, category_id, 'subject_categories')

        if not data_id:
            data_id = uuid4().hex
        return self.driver.set_subject_data(policy_id=policy_id, data_id=data_id,
                                            category_id=category_id, value=value)

    @enforce(("read", "write"), "data")
    def delete_subject_data(self, user_id, policy_id, data_id, category_id=None):
        # TODO (asteroide): check and/or delete assignments linked to that data
        subject_assignments = self.get_subject_assignments(user_id=user_id, policy_id=policy_id,
                                                           category_id=category_id)
        if subject_assignments:
            raise exceptions.DeleteData
        return self.driver.delete_subject_data(policy_id=policy_id, category_id=category_id,
                                               data_id=data_id)

    @enforce("read", "data")
    def get_object_data(self, user_id, policy_id, data_id=None, category_id=None):
        available_metadata = self.get_available_metadata(user_id, policy_id)
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
    def add_object_data(self, user_id, policy_id, data_id=None, category_id=None, value=None):

        if not category_id or (
                not Managers.ModelManager.get_object_categories(user_id=user_id,
                                                                category_id=category_id)):
            raise exceptions.ObjectCategoryUnknown

        self.__category_dependency_validation(user_id, policy_id, category_id, 'object_categories')

        if not data_id:
            data_id = uuid4().hex
        return self.driver.set_object_data(policy_id=policy_id, data_id=data_id,
                                           category_id=category_id, value=value)

    @enforce(("read", "write"), "data")
    def delete_object_data(self, user_id, policy_id, data_id, category_id=None):
        # TODO (asteroide): check and/or delete assignments linked to that data
        object_assignments = self.get_object_assignments(user_id=user_id, policy_id=policy_id,
                                                         category_id=category_id)
        if object_assignments:
            raise exceptions.DeleteData
        return self.driver.delete_object_data(policy_id=policy_id, category_id=category_id,
                                              data_id=data_id)

    @enforce("read", "data")
    def get_action_data(self, user_id, policy_id, data_id=None, category_id=None):
        available_metadata = self.get_available_metadata(user_id, policy_id)
        results = []
        if not category_id:
            for cat in available_metadata["action"]:
                results.append(self.driver.get_action_data(policy_id=policy_id, data_id=data_id,
                                                           category_id=cat))
        if category_id and category_id in available_metadata["action"]:
            results.append(self.driver.get_action_data(policy_id=policy_id, data_id=data_id,
                                                       category_id=category_id))
        return results

    @enforce(("read", "write"), "data")
    def add_action_data(self, user_id, policy_id, data_id=None, category_id=None, value=None):
        if not category_id or (
                not Managers.ModelManager.get_action_categories(user_id=user_id,
                                                                category_id=category_id)):
            raise exceptions.ActionCategoryUnknown

        self.__category_dependency_validation(user_id, policy_id, category_id, 'action_categories')

        if not data_id:
            data_id = uuid4().hex
        return self.driver.set_action_data(policy_id=policy_id, data_id=data_id,
                                           category_id=category_id, value=value)

    @enforce(("read", "write"), "data")
    def delete_action_data(self, user_id, policy_id, data_id, category_id=None):
        # TODO (asteroide): check and/or delete assignments linked to that data
        action_assignments = self.get_action_assignments(user_id=user_id, policy_id=policy_id,
                                                         category_id=category_id)
        if action_assignments:
            raise exceptions.DeleteData
        return self.driver.delete_action_data(policy_id=policy_id, category_id=category_id,
                                              data_id=data_id)

    @enforce("read", "assignments")
    def get_subject_assignments(self, user_id, policy_id, subject_id=None, category_id=None):
        return self.driver.get_subject_assignments(policy_id=policy_id, subject_id=subject_id,
                                                   category_id=category_id)

    @enforce(("read", "write"), "assignments")
    def add_subject_assignment(self, user_id, policy_id, subject_id, category_id, data_id):

        if not category_id or (
                not Managers.ModelManager.get_subject_categories(user_id=user_id,
                                                                 category_id=category_id)):
            raise exceptions.SubjectCategoryUnknown

        self.__category_dependency_validation(user_id, policy_id, category_id, 'subject_categories')

        if not subject_id or (
                not self.get_subjects(user_id=user_id, policy_id=policy_id,
                                      perimeter_id=subject_id)):
            raise exceptions.SubjectUnknown

        if not data_id or (
                not self.get_subject_data(user_id=user_id, policy_id=policy_id, data_id=data_id,
                                          category_id=category_id)):
            raise exceptions.DataUnknown

        return self.driver.add_subject_assignment(policy_id=policy_id, subject_id=subject_id,
                                                  category_id=category_id, data_id=data_id)

    @enforce(("read", "write"), "assignments")
    def delete_subject_assignment(self, user_id, policy_id, subject_id, category_id, data_id):
        return self.driver.delete_subject_assignment(policy_id=policy_id, subject_id=subject_id,
                                                     category_id=category_id, data_id=data_id)

    @enforce("read", "assignments")
    def get_object_assignments(self, user_id, policy_id, object_id=None, category_id=None):
        return self.driver.get_object_assignments(policy_id=policy_id, object_id=object_id,
                                                  category_id=category_id)

    @enforce(("read", "write"), "assignments")
    def add_object_assignment(self, user_id, policy_id, object_id, category_id, data_id):

        if not category_id or (
                not Managers.ModelManager.get_object_categories(user_id=user_id,
                                                                category_id=category_id)):
            raise exceptions.ObjectCategoryUnknown

        self.__category_dependency_validation(user_id, policy_id, category_id, 'object_categories')

        if not object_id or (
                not self.get_objects(user_id=user_id, policy_id=policy_id, perimeter_id=object_id)):
            raise exceptions.ObjectUnknown

        if not data_id or (
                not self.get_object_data(user_id=user_id, policy_id=policy_id, data_id=data_id,
                                         category_id=category_id)):
            raise exceptions.DataUnknown

        return self.driver.add_object_assignment(policy_id=policy_id, object_id=object_id,
                                                 category_id=category_id, data_id=data_id)

    @enforce(("read", "write"), "assignments")
    def delete_object_assignment(self, user_id, policy_id, object_id, category_id, data_id):
        return self.driver.delete_object_assignment(policy_id=policy_id, object_id=object_id,
                                                    category_id=category_id, data_id=data_id)

    @enforce("read", "assignments")
    def get_action_assignments(self, user_id, policy_id, action_id=None, category_id=None):
        return self.driver.get_action_assignments(policy_id=policy_id, action_id=action_id,
                                                  category_id=category_id)

    @enforce(("read", "write"), "assignments")
    def add_action_assignment(self, user_id, policy_id, action_id, category_id, data_id):

        if not category_id or (
                not Managers.ModelManager.get_action_categories(user_id=user_id,
                                                                category_id=category_id)):
            raise exceptions.ActionCategoryUnknown

        self.__category_dependency_validation(user_id, policy_id, category_id, 'action_categories')

        if not action_id or (
                not self.get_actions(user_id=user_id, policy_id=policy_id, perimeter_id=action_id)):
            raise exceptions.ActionUnknown

        if not data_id or (
                not self.get_action_data(user_id=user_id, policy_id=policy_id, data_id=data_id,
                                         category_id=category_id)):
            raise exceptions.DataUnknown

        return self.driver.add_action_assignment(policy_id=policy_id, action_id=action_id,
                                                 category_id=category_id, data_id=data_id)

    @enforce(("read", "write"), "assignments")
    def delete_action_assignment(self, user_id, policy_id, action_id, category_id, data_id):
        return self.driver.delete_action_assignment(policy_id=policy_id, action_id=action_id,
                                                    category_id=category_id, data_id=data_id)

    @enforce("read", "rules")
    def get_rules(self, user_id, policy_id, meta_rule_id=None, rule_id=None):
        return self.driver.get_rules(policy_id=policy_id, meta_rule_id=meta_rule_id,
                                     rule_id=rule_id)

    @enforce(("read", "write"), "rules")
    def add_rule(self, user_id, policy_id, meta_rule_id, value):
        if not meta_rule_id or (
                not self.ModelManager.get_meta_rules(user_id=user_id, meta_rule_id=meta_rule_id)):
            raise exceptions.MetaRuleUnknown

        self.__check_existing_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, user_id=user_id,
                                   rule_value=value)
        self.__dependencies_validation(user_id, policy_id, meta_rule_id)

        return self.driver.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)

    def __check_existing_rule(self, user_id, policy_id, meta_rule_id, rule_value):

        if not meta_rule_id:
            raise exceptions.MetaRuleUnknown

        meta_rule = self.ModelManager.get_meta_rules(user_id=user_id, meta_rule_id=meta_rule_id)
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
            subjects_data = self.get_subject_data(user_id=user_id,
                                                  category_id=sub_cat_id, policy_id=policy_id)
            found_data_counter = self.__validate_data_id(sub_cat_id, subjects_data[0]['data'],
                                                         temp_rule_data,
                                                         "Missing Subject_category "
                                                         , found_data_counter)

        if found_data_counter != len(meta_rule[meta_rule_id]['subject_categories']):
            raise exceptions.RuleContentError(message="Missing Data")

        temp_rule_data = list(
            rule_value['rule'][
            start_sub:start_sub + len(meta_rule[meta_rule_id]['object_categories'])])
        found_data_counter = 0
        start_sub = start_sub + len(meta_rule[meta_rule_id]['object_categories'])

        for ob_cat_id in meta_rule[meta_rule_id]['object_categories']:
            object_data = self.get_object_data(user_id=user_id,
                                               category_id=ob_cat_id, policy_id=policy_id)

            found_data_counter = self.__validate_data_id(ob_cat_id, object_data[0]['data'],
                                                         temp_rule_data,
                                                         "Missing Object_category ",
                                                         found_data_counter)

        if found_data_counter != len(meta_rule[meta_rule_id]['object_categories']):
            raise exceptions.RuleContentError(message="Missing Data")

        temp_rule_data = list(
            rule_value['rule'][
            start_sub:start_sub + len(meta_rule[meta_rule_id]['action_categories'])])
        found_data_counter = 0

        for act_cat_id in meta_rule[meta_rule_id]['action_categories']:
            action_data = self.get_action_data(user_id=user_id, category_id=act_cat_id,
                                               policy_id=policy_id)
            found_data_counter = self.__validate_data_id(act_cat_id, action_data[0]['data'],
                                                         temp_rule_data,
                                                         "Missing Action_category ",
                                                         found_data_counter)

        if found_data_counter != len(meta_rule[meta_rule_id]['action_categories']):
            raise exceptions.RuleContentError(message="Missing Data")

    def __validate_data_id(self, cat_id, data_ids, temp_rule_data, error_msg, found_data_counter):
        for ID in data_ids:
            if ID in temp_rule_data:
                temp_rule_data.remove(ID)
                found_data_counter += 1
        # if no data id found in the rule, so rule not valid
        if found_data_counter < 1:
            raise exceptions.RuleContentError(message=error_msg + cat_id)
        return found_data_counter

    @enforce(("read", "write"), "rules")
    def delete_rule(self, user_id, policy_id, rule_id):
        return self.driver.delete_rule(policy_id=policy_id, rule_id=rule_id)

    @enforce("read", "meta_data")
    def get_available_metadata(self, user_id, policy_id):
        categories = {
            "subject": [],
            "object": [],
            "action": []
        }
        policy = self.driver.get_policies(policy_id=policy_id)
        if not policy:
            raise exceptions.PolicyUnknown
        model_id = policy[policy_id]["model_id"]
        model = Managers.ModelManager.get_models(user_id=user_id, model_id=model_id)
        try:
            meta_rule_list = model[model_id]["meta_rules"]
            for meta_rule_id in meta_rule_list:
                meta_rule = Managers.ModelManager.get_meta_rules(user_id=user_id,
                                                                 meta_rule_id=meta_rule_id)
                categories["subject"].extend(meta_rule[meta_rule_id]["subject_categories"])
                categories["object"].extend(meta_rule[meta_rule_id]["object_categories"])
                categories["action"].extend(meta_rule[meta_rule_id]["action_categories"])
        finally:
            return categories

    def __dependencies_validation(self, user_id, policy_id, meta_rule_id=None):

        policies = self.get_policies(user_id=user_id, policy_id=policy_id)
        if not policy_id or (not policies):
            raise exceptions.PolicyUnknown

        policy_content = policies[next(iter(policies))]
        model_id = policy_content['model_id']
        models = Managers.ModelManager.get_models(user_id=user_id, model_id=model_id)
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

            meta_rule = self.ModelManager.get_meta_rules(user_id=user_id, meta_rule_id=meta_rule_id)
            meta_rule_content = meta_rule[next(iter(meta_rule))]
            if (not meta_rule_content['subject_categories']) or (
                    not meta_rule_content['object_categories']) or (
                    not meta_rule_content['action_categories']):
                raise exceptions.MetaRuleContentError
        return model_content

    def __category_dependency_validation(self, user_id, policy_id, category_id, category_key):
        model = self.__dependencies_validation(user_id=user_id, policy_id=policy_id)
        category_found = False
        for model_meta_rule_id in model['meta_rules']:
            meta_rule = self.ModelManager.get_meta_rules(user_id=user_id,
                                                         meta_rule_id=model_meta_rule_id)
            meta_rule_content = meta_rule[next(iter(meta_rule))]
            if meta_rule_content[category_key] and category_id in meta_rule_content[category_key]:
                category_found = True
                break

        if not category_found:
            raise exceptions.CategoryNotAssignedMetaRule
