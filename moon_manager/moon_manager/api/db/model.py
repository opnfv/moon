# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from uuid import uuid4
import logging
from moon_utilities import exceptions
from moon_utilities.security_functions import enforce
from moon_manager.api.db.managers import Managers
import copy
from moon_manager import pip_driver

logger = logging.getLogger("moon.db.api.model")


class ModelManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.ModelManager = self

    @enforce(("read", "write"), "models")
    def update_model(self, moon_user_id, model_id, value):
        if model_id not in self.driver.get_models(model_id=model_id):
            raise exceptions.ModelUnknown

        if not value['name'].strip():
            raise exceptions.ModelContentError('Model name invalid')

        if 'meta_rules' not in value:
            raise exceptions.MetaRuleUnknown

        model = self.get_models(moon_user_id=moon_user_id, model_id=model_id)
        model = model[next(iter(model))]
        if ((model['meta_rules'] and value['meta_rules'] and model['meta_rules'] != value[
            'meta_rules']) \
                or (model['meta_rules'] and not value['meta_rules'])):
            policies = Managers.PolicyManager.get_policies(moon_user_id=moon_user_id)
            for policy_id in policies:
                if policies[policy_id]["model_id"] == model_id:
                    raise exceptions.DeleteModelWithPolicy

        if value and 'meta_rules' in value:
            for meta_rule_id in value['meta_rules']:
                if meta_rule_id:
                    meta_rule_tmp = self.driver.get_meta_rules(meta_rule_id=meta_rule_id)
                if (not meta_rule_id) or (not meta_rule_tmp) :
                    raise exceptions.MetaRuleUnknown

        return self.driver.update_model(model_id=model_id, value=value)

    @enforce(("read", "write"), "models")
    def delete_model(self, moon_user_id, model_id):
        if model_id not in self.driver.get_models(model_id=model_id):
            raise exceptions.ModelUnknown
        # TODO (asteroide): check that no policy is connected to this model
        policies = Managers.PolicyManager.get_policies(moon_user_id=moon_user_id)
        for policy in policies:
            if policies[policy]['model_id'] == model_id:
                raise exceptions.DeleteModelWithPolicy
        return self.driver.delete_model(model_id=model_id)

    @enforce(("read", "write"), "models")
    def add_model(self, moon_user_id, model_id=None, value=None):

        if not value['name'].strip():
            raise exceptions.ModelContentError('Model name invalid')

        models = self.driver.get_models()
        if model_id in models:
            raise exceptions.ModelExisting

        if value.get('meta_rules', []):
            for model in models:
                if models[model]['name'] == value['name']:
                    raise exceptions.ModelExisting("Model Name Existed")
                if sorted(models[model].get('meta_rules', [])) == sorted(value.get('meta_rules', [])):
                    raise exceptions.ModelExisting("Meta Rules List Existed in another Model")

        if not model_id:
            model_id = uuid4().hex
        if value and 'meta_rules' in value:
            for meta_rule_id in value['meta_rules']:
                if not meta_rule_id:
                    raise exceptions.MetaRuleUnknown
                meta_rule = self.driver.get_meta_rules(meta_rule_id=meta_rule_id)
                if not meta_rule:
                    raise exceptions.MetaRuleUnknown

        return self.driver.add_model(model_id=model_id, value=value)

    @enforce("read", "models")
    def get_models(self, moon_user_id, model_id=None):
        return self.driver.get_models(model_id=model_id)

    @enforce("read", "policies")
    def get_policies(self, moon_user_id, policy_id=None):
        return self.driver.get_policies(policy_id=policy_id)

    @enforce(("read", "write"), "meta_rules")
    def update_meta_rule(self, moon_user_id, meta_rule_id, value):
        meta_rules = self.driver.get_meta_rules()
        if not meta_rule_id or meta_rule_id not in meta_rules:
            raise exceptions.MetaRuleUnknown
        self.__check_meta_rule_dependencies(moon_user_id=moon_user_id, meta_rule_id=meta_rule_id)
        if value:
            if not value['name'].strip():
                raise exceptions.MetaRuleContentError('Meta_rule name invalid')

            if 'subject_categories' in value:
                if (len(value['subject_categories']) == 1 and (value['subject_categories'][0] is None or value[
                'subject_categories'][0].strip() == "")):
                    value['subject_categories'] = [];
                else:
                    for subject_category_id in value['subject_categories']:
                        if (not subject_category_id) or (not self.driver.get_subject_categories(
                                category_id=subject_category_id)):
                            raise exceptions.SubjectCategoryUnknown
            if 'object_categories' in value:
                if (len(value['object_categories']) == 1 and (value['object_categories'][0] is None or value[
                'object_categories'][0].strip() == "")):
                    value['object_categories'] = [];
                else:
                    for object_category_id in value['object_categories']:
                        if (not object_category_id) or (not self.driver.get_object_categories(
                                category_id=object_category_id)):
                            raise exceptions.ObjectCategoryUnknown
            if 'action_categories' in value:
                if (len(value['action_categories']) == 1 and (value['action_categories'][0] is None or value[
                'action_categories'][0].strip() == "")):
                    value['action_categories'] = [];
                else:
                    for action_category_id in value['action_categories']:
                        if (not action_category_id) or (not self.driver.get_action_categories(
                                category_id=action_category_id)):
                            raise exceptions.ActionCategoryUnknown

        for meta_rule_obj_id in meta_rules:
            counter_matched_list = 0
            counter_matched_list += self.check_combination(
                meta_rules[meta_rule_obj_id]['subject_categories'],
                value['subject_categories'])
            counter_matched_list += self.check_combination(
                meta_rules[meta_rule_obj_id]['object_categories'],
                value['object_categories'])
            counter_matched_list += self.check_combination(
                meta_rules[meta_rule_obj_id]['action_categories'],
                value['action_categories'])
            if counter_matched_list == 3 and meta_rule_obj_id != meta_rule_id:
                raise exceptions.MetaRuleExisting("Same categories combination existed")

        return self.driver.set_meta_rule(meta_rule_id=meta_rule_id, value=value)

    def __check_meta_rule_dependencies(self, moon_user_id, meta_rule_id):
        policies = self.get_policies(moon_user_id=moon_user_id)
        for policy in policies:
            model_id = policies[policy]["model_id"]
            model = self.get_models(moon_user_id=moon_user_id, model_id=model_id)[model_id]
            if meta_rule_id in model["meta_rules"]:
                raise exceptions.MetaRuleUpdateError("This meta_rule is already in use in a policy")

        policies = Managers.PolicyManager.get_policies(moon_user_id=moon_user_id)
        for policy_id in policies:
            rules = Managers.PolicyManager.get_rules(moon_user_id=moon_user_id, policy_id=policy_id,
                                                     meta_rule_id=meta_rule_id)
            if rules['rules']:
                raise exceptions.MetaRuleUpdateError

    @enforce("read", "meta_rules")
    def get_meta_rules(self, moon_user_id, meta_rule_id=None):
        return self.driver.get_meta_rules(meta_rule_id=meta_rule_id)

    @enforce(("read", "write"), "meta_rules")
    def add_meta_rule(self, moon_user_id, meta_rule_id=None, value=None):

        if not value['name'].strip():
            raise exceptions.MetaRuleContentError('Meta_rule name invalid')

        meta_rules = self.driver.get_meta_rules()

        if meta_rule_id in meta_rules:
            raise exceptions.MetaRuleExisting

        if value:
            if 'subject_categories' in value:
                if (len(value['subject_categories']) == 1 and (value['subject_categories'][0] is None or value[
                'subject_categories'][0].strip() == "")):
                    value['subject_categories'] = [];
                else:
                    for subject_category_id in value['subject_categories']:
                        if ((not subject_category_id) or (not self.driver.get_subject_categories(
                                category_id=subject_category_id))):
                            if subject_category_id.startswith("attributes:"):
                                _attributes = pip_driver.AttrsManager.get_objects(
                                    moon_user_id="admin",
                                    object_type=subject_category_id.replace("attributes:", "")
                                )
                                action_category_id = subject_category_id.replace("attributes:", "")
                                if action_category_id != _attributes['id']:
                                    raise exceptions.SubjectCategoryUnknown
                            else:
                                raise exceptions.SubjectCategoryUnknown
            if 'object_categories' in value:
                if(len(value['object_categories']) == 1 and (value['object_categories'][0] is None or value[
                'object_categories'][0].strip() == "")):
                    value['object_categories'] = [];
                else:
                    for object_category_id in value['object_categories']:
                        if ((not object_category_id) or (not self.driver.get_object_categories(
                                category_id=object_category_id))):
                            if object_category_id.startswith("attributes:"):
                                _attributes = pip_driver.AttrsManager.get_objects(
                                    moon_user_id="admin",
                                    object_type=object_category_id.replace("attributes:", "")
                                )
                                action_category_id = object_category_id.replace("attributes:", "")
                                if action_category_id != _attributes['id']:
                                    raise exceptions.ObjectCategoryUnknown
                            else:
                                raise exceptions.ObjectCategoryUnknown
            if 'action_categories' in value:
                if (len(value['action_categories']) == 1 and (value['action_categories'][0] is None or value[
                'action_categories'][0].strip() == "")):
                    value['action_categories'] = [];
                else:
                    for action_category_id in value['action_categories']:
                        if ((not action_category_id) or (not self.driver.get_action_categories(
                                category_id=action_category_id))):
                            if action_category_id.startswith("attributes:"):
                                _attributes = pip_driver.AttrsManager.get_objects(
                                    moon_user_id="admin",
                                    object_type=action_category_id.replace("attributes:", "")
                                )
                                action_category_id = action_category_id.replace("attributes:", "")
                                if action_category_id not in _attributes.keys():
                                    raise exceptions.ActionCategoryUnknown
                            else:
                                raise exceptions.ActionCategoryUnknown

        for meta_rule_obj_id in meta_rules:
            counter_matched_list = 0

            counter_matched_list += self.check_combination(
                meta_rules[meta_rule_obj_id]['subject_categories'], value['subject_categories'])

            counter_matched_list += self.check_combination(
                meta_rules[meta_rule_obj_id]['object_categories'], value['object_categories'])

            counter_matched_list += self.check_combination(
                meta_rules[meta_rule_obj_id]['action_categories'], value['action_categories'])

            if counter_matched_list == 3:
                raise exceptions.MetaRuleExisting("Same categories combination existed")

        return self.driver.set_meta_rule(meta_rule_id=meta_rule_id, value=value)

    # @enforce(("read", "write"), "meta_rules")
    def check_combination(self, list_one, list_two):
        counter_removed_items = 0
        temp_list_two = copy.deepcopy(list_two)
        for item in list_one:
            if item in temp_list_two:
                temp_list_two.remove(item)
                counter_removed_items += 1

        if list_two and counter_removed_items == len(list_two) and len(list_two) == len(list_one):
            return 1
        return 0

    @enforce(("read", "write"), "meta_rules")
    def delete_meta_rule(self, moon_user_id, meta_rule_id=None):
        if meta_rule_id not in self.driver.get_meta_rules(meta_rule_id=meta_rule_id):
            raise exceptions.MetaRuleUnknown
        # TODO (asteroide): check and/or delete data and assignments and rules linked to that meta_rule
        models = self.get_models(moon_user_id=moon_user_id)
        for model_id in models:
            for id in models[model_id]['meta_rules']:
                if id == meta_rule_id:
                    raise exceptions.DeleteMetaRuleWithModel
        return self.driver.delete_meta_rule(meta_rule_id=meta_rule_id)

    @enforce("read", "meta_data")
    def get_subject_categories(self, moon_user_id, category_id=None):
        return self.driver.get_subject_categories(category_id=category_id)

    @enforce(("read", "write"), "meta_data")
    def add_subject_category(self, moon_user_id, category_id=None, value=None):

        if not value['name'].strip():
            raise exceptions.CategoryNameInvalid

        subject_categories = []
        if category_id is not None:
            subject_categories = self.driver.get_subject_categories(category_id=category_id)
            
        subject_categories_names = self.driver.get_subject_categories(category_name=value['name'].strip())

        if subject_categories_names or subject_categories:
            raise exceptions.SubjectCategoryExisting
        

        if not ('description' in value):
            value['description'] = ""
        return self.driver.add_subject_category(name=value["name"],
                                                description=value["description"], uuid=category_id)

    @enforce(("read", "write"), "meta_data")
    def delete_subject_category(self, moon_user_id, category_id):
        # TODO (asteroide): delete all data linked to that category
        # TODO (asteroide): delete all meta_rules linked to that category
        if category_id not in self.driver.get_subject_categories(category_id=category_id):
            raise exceptions.SubjectCategoryUnknown
        meta_rules = self.get_meta_rules(moon_user_id=moon_user_id)
        for meta_rule_id in meta_rules:
            for subject_category_id in meta_rules[meta_rule_id]['subject_categories']:
                logger.info(
                    "delete_subject_category {} {}".format(subject_category_id, meta_rule_id))
                logger.info("delete_subject_category {}".format(meta_rules[meta_rule_id]))
                if subject_category_id == category_id:
                    # has_rules = self.driver.is_meta_rule_has_rules(meta_rule_id)
                    # if has_rules:
                    raise exceptions.DeleteSubjectCategoryWithMetaRule

        if self.driver.is_subject_category_has_assignment(category_id):
            raise exceptions.DeleteCategoryWithAssignment

        if self.driver.is_subject_data_exist(category_id=category_id):
            raise exceptions.DeleteCategoryWithData

        return self.driver.delete_subject_category(category_id=category_id)

    @enforce("read", "meta_data")
    def get_object_categories(self, moon_user_id, category_id=None):
        return self.driver.get_object_categories(category_id)

    @enforce(("read", "write"), "meta_data")
    def add_object_category(self, moon_user_id, category_id=None, value=None):
        if not value['name'].strip():
            raise exceptions.CategoryNameInvalid

        object_categories = []
        if category_id is not None:
            object_categories = self.driver.get_object_categories(category_id=category_id)
        
        object_categories_names = self.driver.get_object_categories(category_name=value['name'].strip())
        if object_categories_names or object_categories:
            raise exceptions.ObjectCategoryExisting

        if not ('description' in value):
            value['description'] = ""

        return self.driver.add_object_category(name=value["name"], description=value["description"],
                                               uuid=category_id)

    @enforce(("read", "write"), "meta_data")
    def delete_object_category(self, moon_user_id, category_id):
        # TODO (asteroide): delete all data linked to that category
        # TODO (asteroide): delete all meta_rules linked to that category
        if category_id not in self.driver.get_object_categories(category_id=category_id):
            raise exceptions.ObjectCategoryUnknown
        meta_rules = self.get_meta_rules(moon_user_id=moon_user_id)
        for meta_rule_id in meta_rules:
            for object_category_id in meta_rules[meta_rule_id]['object_categories']:
                if object_category_id == category_id:
                    # has_rules = self.driver.is_meta_rule_has_rules(meta_rule_id)
                    # if has_rules:
                    raise exceptions.DeleteObjectCategoryWithMetaRule

        if self.driver.is_object_category_has_assignment(category_id):
            raise exceptions.DeleteCategoryWithAssignment

        if self.driver.is_object_data_exist(category_id=category_id):
            raise exceptions.DeleteCategoryWithData

        return self.driver.delete_object_category(category_id=category_id)

    @enforce("read", "meta_data")
    def get_action_categories(self, moon_user_id, category_id=None):
        return self.driver.get_action_categories(category_id=category_id)

    @enforce(("read", "write"), "meta_data")
    def add_action_category(self, moon_user_id, category_id=None, value=None):

        if not value['name'].strip():
            raise exceptions.CategoryNameInvalid

        action_categories = []
        if category_id is not None:
            action_categories = self.driver.get_action_categories(category_id=category_id)
        
        action_categories_names = self.driver.get_action_categories(category_name=value['name'].strip())
        if action_categories_names or action_categories:
            raise exceptions.ActionCategoryExisting

        if not ('description' in value):
            value['description'] = ""

        return self.driver.add_action_category(name=value["name"], description=value["description"],
                                               uuid=category_id)

    @enforce(("read", "write"), "meta_data")
    def delete_action_category(self, moon_user_id, category_id):
        # TODO (asteroide): delete all data linked to that category
        # TODO (asteroide): delete all meta_rules linked to that category
        if category_id not in self.driver.get_action_categories(category_id=category_id):
            raise exceptions.ActionCategoryUnknown
        meta_rules = self.get_meta_rules(moon_user_id=moon_user_id)
        for meta_rule_id in meta_rules:
            for action_category_id in meta_rules[meta_rule_id]['action_categories']:
                if action_category_id == category_id:
                    # has_rules = self.driver.is_meta_rule_has_rules(meta_rule_id)
                    # if has_rules:
                    raise exceptions.DeleteActionCategoryWithMetaRule

        if self.driver.is_action_category_has_assignment(category_id):
            raise exceptions.DeleteCategoryWithAssignment

        if self.driver.is_action_data_exist(category_id=category_id):
            raise exceptions.DeleteCategoryWithData

        return self.driver.delete_action_category(category_id=category_id)
