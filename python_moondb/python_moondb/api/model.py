# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
import logging
from python_moonutilities import exceptions
from python_moonutilities.security_functions import filter_input, enforce
from python_moondb.api.managers import Managers

logger = logging.getLogger("moon.db.api.model")


class ModelManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.ModelManager = self

    @enforce(("read", "write"), "models")
    def update_model(self, user_id, model_id, value):
        if model_id not in self.driver.get_models(model_id=model_id):
            raise exceptions.ModelUnknown
        if value and 'meta_rules' in value:
            for meta_rule_id in value['meta_rules']:
                if not self.driver.get_meta_rules(meta_rule_id=meta_rule_id):
                    raise exceptions.MetaRuleUnknown
        return self.driver.update_model(model_id=model_id, value=value)

    @enforce(("read", "write"), "models")
    def delete_model(self, user_id, model_id):
        if model_id not in self.driver.get_models(model_id=model_id):
            raise exceptions.ModelUnknown
        # TODO (asteroide): check that no policy is connected to this model
        policies = Managers.PolicyManager.get_policies(user_id=user_id)
        for policy in policies:
            if policies[policy]['model_id'] == model_id:
                raise exceptions.DeleteModelWithPolicy
        return self.driver.delete_model(model_id=model_id)

    @enforce(("read", "write"), "models")
    def add_model(self, user_id, model_id=None, value=None):
        if model_id in self.driver.get_models(model_id=model_id):
            raise exceptions.ModelExisting
        if not model_id:
            model_id = uuid4().hex
        if value and 'meta_rules' in value:
            for meta_rule_id in value['meta_rules']:
                if not self.driver.get_meta_rules(meta_rule_id=meta_rule_id):
                    raise exceptions.MetaRuleUnknown
        return self.driver.add_model(model_id=model_id, value=value)

    @enforce("read", "models")
    def get_models(self, user_id, model_id=None):
        return self.driver.get_models(model_id=model_id)

    @enforce(("read", "write"), "meta_rules")
    def set_meta_rule(self, user_id, meta_rule_id, value):
        if meta_rule_id not in self.driver.get_meta_rules(meta_rule_id=meta_rule_id):
            raise exceptions.MetaRuleUnknown
        if value:
            if 'subject_categories' in value:
                for subject_category_id in value['subject_categories']:
                    if not self.driver.get_subject_categories(category_id=subject_category_id):
                        raise exceptions.SubjectCategoryUnknown
            if 'object_categories' in value:
                for object_category_id in value['object_categories']:
                    if not self.driver.get_object_categories(category_id=object_category_id):
                        raise exceptions.ObjectCategoryUnknown
            if 'action_categories' in value:
                for action_category_id in value['action_categories']:
                    if not self.driver.get_action_categories(category_id=action_category_id):
                        raise exceptions.ActionCategoryUnknown
        return self.driver.set_meta_rule(meta_rule_id=meta_rule_id, value=value)

    @enforce("read", "meta_rules")
    def get_meta_rules(self, user_id, meta_rule_id=None):
        return self.driver.get_meta_rules(meta_rule_id=meta_rule_id)

    @enforce(("read", "write"), "meta_rules")
    def add_meta_rule(self, user_id, meta_rule_id=None, value=None):
        if meta_rule_id in self.driver.get_meta_rules(meta_rule_id=meta_rule_id):
            raise exceptions.MetaRuleExisting
        if value:
            if 'subject_categories' in value:
                for subject_category_id in value['subject_categories']:
                    if not self.driver.get_subject_categories(category_id=subject_category_id):
                        raise exceptions.SubjectCategoryUnknown
            if 'object_categories' in value:
                for object_category_id in value['object_categories']:
                    if not self.driver.get_object_categories(category_id=object_category_id):
                        raise exceptions.ObjectCategoryUnknown
            if 'action_categories' in value:
                for action_category_id in value['action_categories']:
                    if not self.driver.get_action_categories(category_id=action_category_id):
                        raise exceptions.ActionCategoryUnknown
        return self.driver.set_meta_rule(meta_rule_id=meta_rule_id, value=value)

    @enforce(("read", "write"), "meta_rules")
    def delete_meta_rule(self, user_id, meta_rule_id=None):
        if meta_rule_id not in self.driver.get_meta_rules(meta_rule_id=meta_rule_id):
            raise exceptions.MetaRuleUnknown
        # TODO (asteroide): check and/or delete data and assignments and rules linked to that meta_rule
        models = self.get_models(user_id=user_id)
        for model_id in models:
            if models[model_id]['meta_rules'] == meta_rule_id:
                raise exceptions.DeleteMetaRuleWithModel
        return self.driver.delete_meta_rule(meta_rule_id=meta_rule_id)

    @enforce("read", "meta_data")
    def get_subject_categories(self, user_id, category_id=None):
        return self.driver.get_subject_categories(category_id=category_id)

    @enforce(("read", "write"), "meta_data")
    def add_subject_category(self, user_id, category_id=None, value=None):
        if category_id in self.driver.get_subject_categories(category_id=category_id):
            raise exceptions.SubjectCategoryExisting
        return self.driver.add_subject_category(name=value["name"], description=value["description"], uuid=category_id)

    @enforce(("read", "write"), "meta_data")
    def delete_subject_category(self, user_id, category_id):
        # TODO (asteroide): delete all data linked to that category
        # TODO (asteroide): delete all meta_rules linked to that category
        if category_id not in self.driver.get_subject_categories(category_id=category_id):
            raise exceptions.SubjectCategoryUnknown
        meta_rules = self.get_meta_rules(user_id=user_id)
        for meta_rule_id in meta_rules:
            for subject_category_id in meta_rules[meta_rule_id]['subject_categories']:
                if subject_category_id == category_id:
                    raise exceptions.DeleteCategoryWithMetaRule
        if self.driver.is_subject_data_exist(category_id=category_id):
            raise exceptions.DeleteCategoryWithData
        return self.driver.delete_subject_category(category_id=category_id)

    @enforce("read", "meta_data")
    def get_object_categories(self, user_id, category_id=None):
        return self.driver.get_object_categories(category_id)

    @enforce(("read", "write"), "meta_data")
    def add_object_category(self, user_id, category_id=None, value=None):
        if category_id in self.driver.get_object_categories(category_id=category_id):
            raise exceptions.ObjectCategoryExisting
        return self.driver.add_object_category(name=value["name"], description=value["description"], uuid=category_id)

    @enforce(("read", "write"), "meta_data")
    def delete_object_category(self, user_id, category_id):
        # TODO (asteroide): delete all data linked to that category
        # TODO (asteroide): delete all meta_rules linked to that category
        if category_id not in self.driver.get_object_categories(category_id=category_id):
            raise exceptions.ObjectCategoryUnknown
        meta_rules = self.get_meta_rules(user_id=user_id)
        for meta_rule_id in meta_rules:
            for object_category_id in meta_rules[meta_rule_id]['object_categories']:
                if object_category_id == category_id:
                    raise exceptions.DeleteCategoryWithMetaRule
        if self.driver.is_object_data_exist(category_id=category_id):
            raise exceptions.DeleteCategoryWithData
        return self.driver.delete_object_category(category_id=category_id)

    @enforce("read", "meta_data")
    def get_action_categories(self, user_id, category_id=None):
        return self.driver.get_action_categories(category_id=category_id)

    @enforce(("read", "write"), "meta_data")
    def add_action_category(self, user_id, category_id=None, value=None):
        if category_id in self.driver.get_action_categories(category_id=category_id):
            raise exceptions.ActionCategoryExisting
        return self.driver.add_action_category(name=value["name"], description=value["description"], uuid=category_id)

    @enforce(("read", "write"), "meta_data")
    def delete_action_category(self, user_id, category_id):
        # TODO (asteroide): delete all data linked to that category
        # TODO (asteroide): delete all meta_rules linked to that category
        if category_id not in self.driver.get_action_categories(category_id=category_id):
            raise exceptions.ActionCategoryUnknown
        meta_rules = self.get_meta_rules(user_id=user_id)
        for meta_rule_id in meta_rules:
            for action_category_id in meta_rules[meta_rule_id]['action_categories']:
                if action_category_id == category_id:
                    raise exceptions.DeleteCategoryWithMetaRule
        if self.driver.is_action_data_exist(category_id=category_id):
            raise exceptions.DeleteCategoryWithData
        return self.driver.delete_action_category(category_id=category_id)
