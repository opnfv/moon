# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
import logging
from python_moonutilities.security_functions import enforce
from python_moondb.api.managers import Managers
from python_moonutilities import exceptions

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
        if policy_id not in self.driver.get_policies(policy_id=policy_id):
            raise exceptions.PolicyUnknown
        return self.driver.update_policy(policy_id=policy_id, value=value)

    @enforce(("read", "write"), "policies")
    def delete_policy(self, user_id, policy_id):
        # TODO (asteroide): unmap PDP linked to that policy
        if policy_id not in self.driver.get_policies(policy_id=policy_id):
            raise exceptions.PolicyUnknown
        return self.driver.delete_policy(policy_id=policy_id)

    @enforce(("read", "write"), "policies")
    def add_policy(self, user_id, policy_id=None, value=None):
        if policy_id in self.driver.get_policies(policy_id=policy_id):
            raise exceptions.PolicyExisting
        if not policy_id:
            policy_id = uuid4().hex
        return self.driver.add_policy(policy_id=policy_id, value=value)

    @enforce("read", "policies")
    def get_policies(self, user_id, policy_id=None):
        return self.driver.get_policies(policy_id=policy_id)

    @enforce("read", "perimeter")
    def get_subjects(self, user_id, policy_id, perimeter_id=None):
        return self.driver.get_subjects(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce(("read", "write"), "perimeter")
    def add_subject(self, user_id, policy_id, perimeter_id=None, value=None):
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
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        return self.driver.set_subject(policy_id=policy_id, perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def delete_subject(self, user_id, policy_id, perimeter_id):
        return self.driver.delete_subject(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce("read", "perimeter")
    def get_objects(self, user_id, policy_id, perimeter_id=None):
        return self.driver.get_objects(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce(("read", "write"), "perimeter")
    def add_object(self, user_id, policy_id, perimeter_id=None, value=None):
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        if not perimeter_id:
            perimeter_id = uuid4().hex
        return self.driver.set_object(policy_id=policy_id, perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def delete_object(self, user_id, policy_id, perimeter_id):
        return self.driver.delete_object(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce("read", "perimeter")
    def get_actions(self, user_id, policy_id, perimeter_id=None):
        return self.driver.get_actions(policy_id=policy_id, perimeter_id=perimeter_id)

    @enforce(("read", "write"), "perimeter")
    def add_action(self, user_id, policy_id, perimeter_id=None, value=None):
        logger.info("add_action {}".format(policy_id))
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        return self.driver.set_action(policy_id=policy_id, perimeter_id=perimeter_id, value=value)

    @enforce(("read", "write"), "perimeter")
    def delete_action(self, user_id, policy_id, perimeter_id):
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
        if not category_id:
            raise Exception('Invalid category id')
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        if not data_id:
            data_id = uuid4().hex
        return self.driver.set_subject_data(policy_id=policy_id, data_id=data_id, category_id=category_id, value=value)

    @enforce(("read", "write"), "data")
    def delete_subject_data(self, user_id, policy_id, data_id):
        # TODO (asteroide): check and/or delete assignments linked to that data
        return self.driver.delete_subject_data(policy_id=policy_id, data_id=data_id)

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
        if not category_id:
            raise Exception('Invalid category id')
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        if not data_id:
            data_id = uuid4().hex
        return self.driver.set_object_data(policy_id=policy_id, data_id=data_id, category_id=category_id, value=value)

    @enforce(("read", "write"), "data")
    def delete_object_data(self, user_id, policy_id, data_id):
        # TODO (asteroide): check and/or delete assignments linked to that data
        return self.driver.delete_object_data(policy_id=policy_id, data_id=data_id)

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
        if not category_id:
            raise Exception('Invalid category id')
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        if not data_id:
            data_id = uuid4().hex
        return self.driver.set_action_data(policy_id=policy_id, data_id=data_id, category_id=category_id, value=value)

    @enforce(("read", "write"), "data")
    def delete_action_data(self, user_id, policy_id, data_id):
        # TODO (asteroide): check and/or delete assignments linked to that data
        return self.driver.delete_action_data(policy_id=policy_id, data_id=data_id)

    @enforce("read", "assignments")
    def get_subject_assignments(self, user_id, policy_id, subject_id=None, category_id=None):
        return self.driver.get_subject_assignments(policy_id=policy_id, subject_id=subject_id, category_id=category_id)

    @enforce(("read", "write"), "assignments")
    def add_subject_assignment(self, user_id, policy_id, subject_id, category_id, data_id):
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        return self.driver.add_subject_assignment(policy_id=policy_id, subject_id=subject_id,
                                                  category_id=category_id, data_id=data_id)

    @enforce(("read", "write"), "assignments")
    def delete_subject_assignment(self, user_id, policy_id, subject_id, category_id, data_id):
        return self.driver.delete_subject_assignment(policy_id=policy_id, subject_id=subject_id,
                                                     category_id=category_id, data_id=data_id)

    @enforce("read", "assignments")
    def get_object_assignments(self, user_id, policy_id, object_id=None, category_id=None):
        return self.driver.get_object_assignments(policy_id=policy_id, object_id=object_id, category_id=category_id)

    @enforce(("read", "write"), "assignments")
    def add_object_assignment(self, user_id, policy_id, object_id, category_id, data_id):
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        return self.driver.add_object_assignment(policy_id=policy_id, object_id=object_id,
                                                 category_id=category_id, data_id=data_id)

    @enforce(("read", "write"), "assignments")
    def delete_object_assignment(self, user_id, policy_id, object_id, category_id, data_id):
        return self.driver.delete_object_assignment(policy_id=policy_id, object_id=object_id,
                                                    category_id=category_id, data_id=data_id)

    @enforce("read", "assignments")
    def get_action_assignments(self, user_id, policy_id, action_id=None, category_id=None):
        return self.driver.get_action_assignments(policy_id=policy_id, action_id=action_id, category_id=category_id)

    @enforce(("read", "write"), "assignments")
    def add_action_assignment(self, user_id, policy_id, action_id, category_id, data_id):
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        return self.driver.add_action_assignment(policy_id=policy_id, action_id=action_id,
                                                 category_id=category_id, data_id=data_id)

    @enforce(("read", "write"), "assignments")
    def delete_action_assignment(self, user_id, policy_id, action_id, category_id, data_id):
        return self.driver.delete_action_assignment(policy_id=policy_id, action_id=action_id,
                                                    category_id=category_id, data_id=data_id)

    @enforce("read", "rules")
    def get_rules(self, user_id, policy_id, meta_rule_id=None, rule_id=None):
        return self.driver.get_rules(policy_id=policy_id, meta_rule_id=meta_rule_id, rule_id=rule_id)

    @enforce(("read", "write"), "rules")
    def add_rule(self, user_id, policy_id, meta_rule_id, value):
        if not self.get_policies(user_id=user_id, policy_id=policy_id):
            raise exceptions.PolicyUnknown
        return self.driver.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)

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
                meta_rule = Managers.ModelManager.get_meta_rules(user_id=user_id, meta_rule_id=meta_rule_id)
                categories["subject"].extend(meta_rule[meta_rule_id]["subject_categories"])
                categories["object"].extend(meta_rule[meta_rule_id]["object_categories"])
                categories["action"].extend(meta_rule[meta_rule_id]["action_categories"])
        finally:
            return categories
