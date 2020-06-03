# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import html
import json
import logging

from moon_utilities import exceptions

LOGGER = logging.getLogger("moon.utilities." + __name__)


class Manager:
    __policy_manager = None
    __model_manager = None
    __pdp_manager = None

    def get_meta_rules(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def set_subject_data(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def set_object_data(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def set_action_data(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_subject_data(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_object_data(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_action_data(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_rule(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_meta_rule(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_subject_assignment(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_object_assignment(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_action_assignment(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_subject_assignments(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_object_assignments(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_action_assignments(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_policies(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_subject_category(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_object_category(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_action_category(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_subject_categories(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_object_categories(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_action_categories(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_subject(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_object(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_action(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_subjects(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_objects(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_actions(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_policy(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def update_policy(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_models(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def update_model(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_model(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_pdp(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def update_pdp(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def add_pdp(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def get_rules(self, **kwargs):
        raise NotImplementedError  # pragma: no cover


class CacheManager(Manager):
    __policy_manager = None
    __model_manager = None
    __pdp_manager = None

    def __init__(self, cache):
        self.__cache = cache

    def get_meta_rules(self, **kwargs):
        return self.__cache.meta_rules

    def set_subject_data(self, **kwargs):
        value = kwargs.get("value", {})
        value["category_id"] = kwargs.get("category_id", "")
        value["policy_id"] = kwargs.get("policy_id", "")
        return self.__cache.add_subject_data(
            policy_id=kwargs.get("policy_id", ""),
            category_id=kwargs.get("category_id", ""),
            data=value
        )

    def set_object_data(self, **kwargs):
        value = kwargs.get("value", {})
        value["category_id"] = kwargs.get("category_id", "")
        value["policy_id"] = kwargs.get("policy_id", "")
        return self.__cache.add_object_data(
            policy_id=kwargs.get("policy_id", ""),
            category_id=kwargs.get("category_id", ""),
            data=value
        )

    def set_action_data(self, **kwargs):
        value = kwargs.get("value", {})
        value["category_id"] = kwargs.get("category_id", "")
        value["policy_id"] = kwargs.get("policy_id", "")
        return self.__cache.add_action_data(
            policy_id=kwargs.get("policy_id", ""),
            category_id=kwargs.get("category_id", ""),
            data=value
        )

    def get_subject_data(self, **kwargs):
        if "policy_id" in kwargs:
            results = []
            for data in self.__cache.subject_data:
                if data.get("policy_id") == kwargs["policy_id"]:
                    if data.get("category_id") == kwargs.get("category_id"):
                        results.append(data)
                    elif not kwargs.get("category_id"):
                        results.append(data)
            if "data_id" in kwargs:
                for res in results:
                    if kwargs.get("data_id") in res.get("data"):
                        return [res, ]
            else:
                return results
        else:
            return self.__cache.subject_data

    def get_object_data(self, **kwargs):
        if "policy_id" in kwargs:
            results = []
            for data in self.__cache.object_data:
                if data.get("policy_id") == kwargs["policy_id"]:
                    if data.get("category_id") == kwargs.get("category_id"):
                        results.append(data)
                    elif not kwargs.get("category_id"):
                        results.append(data)
            return results
        else:
            return self.__cache.object_data

    def get_action_data(self, **kwargs):
        if "policy_id" in kwargs:
            results = []
            for data in self.__cache.action_data:
                if data.get("policy_id") == kwargs["policy_id"]:
                    if data.get("category_id") == kwargs.get("category_id"):
                        results.append(data)
                    elif not kwargs.get("category_id"):
                        results.append(data)
            return results
        else:
            return self.__cache.action_data

    def add_rule(self, **kwargs):
        value = {
            'policy_id': kwargs.get('policy_id'),
            'meta_rule_id': kwargs.get('meta_rule_id'),
            'value': kwargs.get('value')
        }
        return self.__cache.add_rule(value)

    def add_meta_rule(self, **kwargs):
        return self.__cache.add_meta_rule(kwargs.get("value"))

    def add_subject_assignment(self, **kwargs):
        return self.__cache.add_subject_assignment(
            policy_id=kwargs.get("policy_id"),
            perimeter_id=kwargs.get("subject_id"),
            category_id=kwargs.get("category_id"),
            data_id=kwargs.get("data_id"),
        )

    def add_object_assignment(self, **kwargs):
        return self.__cache.add_object_assignment(
            policy_id=kwargs.get("policy_id"),
            perimeter_id=kwargs.get("object_id"),
            category_id=kwargs.get("category_id"),
            data_id=kwargs.get("data_id"),
        )

    def add_action_assignment(self, **kwargs):
        return self.__cache.add_action_assignment(
            policy_id=kwargs.get("policy_id"),
            perimeter_id=kwargs.get("action_id"),
            category_id=kwargs.get("category_id"),
            data_id=kwargs.get("data_id"),
        )

    def get_subject_assignments(self, **kwargs):
        return self.__cache.subject_assignments

    def get_object_assignments(self, **kwargs):
        return self.__cache.object_assignments

    def get_action_assignments(self, **kwargs):
        return self.__cache.action_assignments

    def get_policies(self, **kwargs):
        return self.__cache.policies

    def add_subject_category(self, **kwargs):
        if kwargs.get("value", {}).get("name") != html.escape(kwargs.get("value", {}).get("name")):
            raise exceptions.ValidationContentError('Forbidden characters in string')
        if kwargs.get("category_id"):
            if kwargs.get("category_id") in self.__cache.subject_categories:
                raise exceptions.SubjectCategoryExisting
        self.__cache.add_subject_category(kwargs.get("value"))

    def add_object_category(self, **kwargs):
        if kwargs.get("value", {}).get("name") != html.escape(kwargs.get("value", {}).get("name")):
            raise exceptions.ValidationContentError('Forbidden characters in string')
        if kwargs.get("category_id"):
            if kwargs.get("category_id") in self.__cache.object_categories:
                raise exceptions.ObjectCategoryExisting
        self.__cache.add_object_category(kwargs.get("value"))

    def add_action_category(self, **kwargs):
        if kwargs.get("value", {}).get("name") != html.escape(kwargs.get("value", {}).get("name")):
            raise exceptions.ValidationContentError('Forbidden characters in string')
        if kwargs.get("category_id"):
            if kwargs.get("category_id") in self.__cache.action_categories:
                raise exceptions.ActionCategoryExisting
        self.__cache.add_action_category(kwargs.get("value"))

    def get_subject_categories(self, **kwargs):
        return self.__cache.subject_categories

    def get_object_categories(self, **kwargs):
        return self.__cache.object_categories

    def get_action_categories(self, **kwargs):
        return self.__cache.action_categories

    def add_subject(self, **kwargs):
        if kwargs.get("value", {}).get("name") != html.escape(kwargs.get("value", {}).get("name")):
            raise exceptions.ValidationContentError('Forbidden characters in string')
        value = kwargs.get("value")
        if kwargs.get("policy_id"):
            value["policy_list"] = [kwargs.get("policy_id")]
        if kwargs.get("perimeter_id"):
            return self.__cache.update_subject(kwargs.get("perimeter_id"), value)
        else:
            return self.__cache.add_subject(value)

    def add_object(self, **kwargs):
        if kwargs.get("value", {}).get("name") != html.escape(kwargs.get("value", {}).get("name")):
            raise exceptions.ValidationContentError('Forbidden characters in string')
        value = kwargs.get("value")
        if kwargs.get("policy_id"):
            value["policy_list"] = [kwargs.get("policy_id")]
        if kwargs.get("perimeter_id"):
            return self.__cache.update_object(kwargs.get("perimeter_id"), value)
        else:
            return self.__cache.add_object(value)

    def add_action(self, **kwargs):
        if kwargs.get("value", {}).get("name") != html.escape(kwargs.get("value", {}).get("name")):
            raise exceptions.ValidationContentError('Forbidden characters in string')
        value = kwargs.get("value")
        if kwargs.get("policy_id"):
            value["policy_list"] = [kwargs.get("policy_id")]
        if kwargs.get("perimeter_id"):
            return self.__cache.update_action(kwargs.get("perimeter_id"), value)
        else:
            return self.__cache.add_action(value)

    def get_subjects(self, **kwargs):
        results = {}
        subjects = self.__cache.subjects
        for policy_id in subjects:
            results.update(subjects[policy_id])
        return results

    def get_objects(self, **kwargs):
        results = {}
        objects = self.__cache.objects
        for policy_id in objects:
            results.update(objects[policy_id])
        return results

    def get_actions(self, **kwargs):
        results = {}
        actions = self.__cache.actions
        for policy_id in actions:
            results.update(actions[policy_id])
        return results

    def add_policy(self, **kwargs):
        return self.__cache.add_policy(kwargs.get("value"))

    def update_policy(self, **kwargs):
        self.__cache.update_policy(kwargs.get("policy_id"), kwargs.get("value"))

    def get_models(self, **kwargs):
        return self.__cache.models

    def update_model(self, **kwargs):
        self.__cache.update_model(kwargs.get("model_id"), kwargs.get("value"))

    def add_model(self, **kwargs):
        if kwargs.get("value", {}).get("name") != html.escape(kwargs.get("value", {}).get("name")):
            raise exceptions.ValidationContentError('Forbidden characters in string')
        self.__cache.add_model(kwargs.get("value"))

    def get_pdp(self, **kwargs):
        return self.__cache.pdp

    def update_pdp(self, **kwargs):
        self.__cache.add_pdp(pdp_id=kwargs.get("pdp_id"), data=kwargs.get("value"))

    def add_pdp(self, **kwargs):
        self.__cache.add_pdp(data=kwargs.get("value"))

    def get_rules(self, **kwargs):
        return self.__cache.rules


class DBManager(Manager):
    __policy_manager = None
    __model_manager = None
    __pdp_manager = None

    def __init__(self, driver):  # pragma: no cover
        self.__policy_manager = driver.PolicyManager
        self.__model_manager = driver.ModelManager
        self.__pdp_manager = driver.PDPManager

    @property
    def meta_rules(self):
        return self.get_meta_rules()

    def get_meta_rules(self, **kwargs):
        return self.__model_manager.get_meta_rules(
                moon_user_id=kwargs.get("moon_user_id"),
                meta_rule_id=kwargs.get("meta_rule_id")
            )

    def set_subject_data(self, **kwargs):
        value = self.__policy_manager.set_subject_data(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            category_id=kwargs.get("category_id"),
            value=kwargs.get("value")
        )
        return value

    def set_object_data(self, **kwargs):
        return self.__policy_manager.add_object_data(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            category_id=kwargs.get("category_id"),
            value=kwargs.get("value")
        )

    def set_action_data(self, **kwargs):
        return self.__policy_manager.add_action_data(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            category_id=kwargs.get("category_id"),
            value=kwargs.get("value")
        )

    @property
    def subject_data(self):
        _data = []
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            for category in self.__model_manager.get_subject_categories(moon_user_id="admin"):
                _data += self.__policy_manager.get_subject_data(moon_user_id="admin",
                                                                policy_id=policy,
                                                                category_id=category)
        return _data

    def get_subject_data(self, **kwargs):
        return self.__policy_manager.get_subject_data(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            data_id=kwargs.get("data_id"),
            category_id=kwargs.get("category_id")
        )

    @property
    def object_data(self):
        _data = []
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            _data += self.__policy_manager.get_object_data(moon_user_id="admin",
                                                           policy_id=policy)
        return _data

    def get_object_data(self, **kwargs):
        return self.__policy_manager.get_object_data(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            data_id=kwargs.get("data_id"),
            category_id=kwargs.get("category_id")
        )

    @property
    def action_data(self):
        _data = []
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            _data += self.__policy_manager.get_action_data(moon_user_id="admin",
                                                           policy_id=policy)
        return _data

    def get_action_data(self, **kwargs):
        return self.__policy_manager.get_action_data(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            data_id=kwargs.get("data_id"),
            category_id=kwargs.get("category_id")
        )

    def add_rule(self, **kwargs):
        return self.__policy_manager.add_rule(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            meta_rule_id=kwargs.get("meta_rule_id"),
            value=kwargs.get("value")
        )

    def add_meta_rule(self, **kwargs):
        return self.__model_manager.add_meta_rule(
            moon_user_id=kwargs.get("moon_user_id"),
            meta_rule_id=kwargs.get("meta_rule_id"),
            value=kwargs.get("value")
        )

    @property
    def subject_assignments(self):
        _assignments = {}
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            _assignments.update(self.__policy_manager.get_subject_assignments(
                moon_user_id="admin",
                policy_id=policy))
        return _assignments

    def add_subject_assignment(self, **kwargs):
        return self.__policy_manager.add_subject_assignment(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            subject_id=kwargs.get("subject_id"),
            category_id=kwargs.get("category_id"),
            data_id=kwargs.get("data_id")
        )

    @property
    def object_assignments(self):
        _assignments = {}
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            _assignments.update(self.__policy_manager.get_object_assignments(
                moon_user_id="admin",
                policy_id=policy))
        return _assignments

    def add_object_assignment(self, **kwargs):
        return self.__policy_manager.add_object_assignment(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            object_id=kwargs.get("object_id"),
            category_id=kwargs.get("category_id"),
            data_id=kwargs.get("data_id")
        )

    @property
    def action_assignments(self):
        _assignments = {}
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            _assignments.update(self.__policy_manager.get_action_assignments(
                moon_user_id="admin",
                policy_id=policy))
        return _assignments

    def add_action_assignment(self, **kwargs):
        return self.__policy_manager.add_action_assignment(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            action_id=kwargs.get("action_id"),
            category_id=kwargs.get("category_id"),
            data_id=kwargs.get("data_id")
        )

    def get_subject_assignments(self, **kwargs):
        return self.__policy_manager.get_subject_assignments(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            category_id=kwargs.get("category_id")
        )

    def get_object_assignments(self, **kwargs):
        return self.__policy_manager.get_object_assignments(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            category_id=kwargs.get("category_id")
        )

    def get_action_assignments(self, **kwargs):
        return self.__policy_manager.get_action_assignments(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            category_id=kwargs.get("category_id")
        )

    def get_policies(self, **kwargs):
        return self.__policy_manager.get_policies(moon_user_id=kwargs.get("moon_user_id"))

    @property
    def subject_categories(self):
        return self.__model_manager.get_subject_categories(moon_user_id="admin")

    def add_subject_category(self, **kwargs):
        return self.__model_manager.add_subject_category(
            moon_user_id=kwargs.get("moon_user_id"),
            category_id=kwargs.get("category_id"),
            value=kwargs.get("value")
        )

    @property
    def object_categories(self):
        return self.__model_manager.get_object_categories(moon_user_id="admin")

    def add_object_category(self, **kwargs):
        return self.__model_manager.add_object_category(
            moon_user_id=kwargs.get("moon_user_id"),
            category_id=kwargs.get("category_id"),
            value=kwargs.get("value")
        )

    @property
    def action_categories(self):
        return self.__model_manager.get_action_categories(moon_user_id="admin")

    def add_action_category(self, **kwargs):
        return self.__model_manager.add_action_category(
            moon_user_id=kwargs.get("moon_user_id"),
            category_id=kwargs.get("category_id"),
            value=kwargs.get("value")
        )

    def get_subject_categories(self, **kwargs):
        return self.__model_manager.get_subject_categories(
            moon_user_id=kwargs.get("moon_user_id")
        )

    def get_object_categories(self, **kwargs):
        return self.__model_manager.get_object_categories(
            moon_user_id=kwargs.get("moon_user_id")
        )

    def get_action_categories(self, **kwargs):
        return self.__model_manager.get_action_categories(
            moon_user_id=kwargs.get("moon_user_id")
        )

    @property
    def subjects(self):
        _perimeter = {}
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            _perimeter.update(self.__policy_manager.get_subjects(moon_user_id="admin",
                                                                 policy_id=policy))
        return _perimeter

    def add_subject(self, **kwargs):
        if kwargs.get("perimeter_id"):
            return self.__policy_manager.update_subject(
                moon_user_id=kwargs.get("moon_user_id"),
                perimeter_id=kwargs.get("perimeter_id"),
                value=kwargs.get("value")
            )
        else:
            return self.__policy_manager.add_subject(
                moon_user_id=kwargs.get("moon_user_id"),
                policy_id=kwargs.get("policy_id"),
                value=kwargs.get("value")
            )

    @property
    def objects(self):
        _perimeter = {}
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            _perimeter.update(self.__policy_manager.get_objects(moon_user_id="admin",
                                                                policy_id=policy))
        return _perimeter

    def add_object(self, **kwargs):
        if kwargs.get("perimeter_id"):
            return self.__policy_manager.update_object(
                moon_user_id=kwargs.get("moon_user_id"),
                perimeter_id=kwargs.get("perimeter_id"),
                value=kwargs.get("value")
            )
        else:
            return self.__policy_manager.add_object(
                moon_user_id=kwargs.get("moon_user_id"),
                policy_id=kwargs.get("policy_id"),
                value=kwargs.get("value")
            )

    @property
    def actions(self):
        _perimeter = {}
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            _perimeter.update(self.__policy_manager.get_actions(moon_user_id="admin",
                                                                policy_id=policy))
        return _perimeter

    def add_action(self, **kwargs):
        if kwargs.get("perimeter_id"):
            return self.__policy_manager.update_action(
                moon_user_id=kwargs.get("moon_user_id"),
                perimeter_id=kwargs.get("perimeter_id"),
                value=kwargs.get("value")
            )
        else:
            return self.__policy_manager.add_action(
                moon_user_id=kwargs.get("moon_user_id"),
                policy_id=kwargs.get("policy_id"),
                value=kwargs.get("value")
            )

    def get_subjects(self, **kwargs):
        return self.__policy_manager.get_subjects(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id")
        )

    def get_objects(self, **kwargs):
        return self.__policy_manager.get_objects(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id")
        )

    def get_actions(self, **kwargs):
        return self.__policy_manager.get_actions(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id")
        )

    @property
    def policies(self):
        return self.__policy_manager.get_policies(moon_user_id="admin")

    def add_policy(self, **kwargs):
        return self.__policy_manager.add_policy(
            moon_user_id=kwargs.get("moon_user_id"),
            value=kwargs.get("value")
        )

    def update_policy(self, **kwargs):
        return self.__policy_manager.update_policy(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id"),
            value=kwargs.get("value"))

    @property
    def models(self):
        return self.get_models()

    def get_models(self, **kwargs):
        return self.__model_manager.get_models(moon_user_id=kwargs.get("moon_user_id"))

    def update_model(self, **kwargs):
        return self.__model_manager.update_model(
            moon_user_id=kwargs.get("moon_user_id"),
            model_id=kwargs.get("model_id"),
            value=kwargs.get("value")
        )

    def add_model(self, **kwargs):
        return self.__model_manager.add_model(
            moon_user_id=kwargs.get("moon_user_id"),
            value=kwargs.get("value")
        )

    @property
    def pdp(self):
        return self.get_pdp()

    def get_pdp(self, **kwargs):
        return self.__pdp_manager.get_pdp(moon_user_id=kwargs.get("moon_user_id"))

    def update_pdp(self, **kwargs):
        return self.__pdp_manager.update_pdp(
            moon_user_id=kwargs.get("moon_user_id"),
            pdp_id=kwargs.get("pdp_id"),
            value=kwargs.get("value")
        )

    def add_pdp(self, **kwargs):
        return self.__pdp_manager.add_pdp(
            moon_user_id=kwargs.get("moon_user_id"),
            value=kwargs.get("value")
        )

    @property
    def rules(self):
        _rules = []
        for policy in self.__policy_manager.get_policies(moon_user_id="admin"):
            _rules.append(self.__policy_manager.get_rules(moon_user_id="admin",
                                                          policy_id=policy))
        return _rules

    def get_rules(self, **kwargs):
        return self.__policy_manager.get_rules(
            moon_user_id=kwargs.get("moon_user_id"),
            policy_id=kwargs.get("policy_id")
        )


class JsonUtils:
    @staticmethod
    def get_override(json_content):
        if "override" in json_content:
            return json_content["override"]
        return False

    @staticmethod
    def get_mandatory(json_content):
        if "mandatory" in json_content:
            return json_content["mandatory"]
        return False

    @staticmethod
    def copy_field_if_exists(json_in, json_out, field_name, type_field, default_value=None):
        if field_name in json_in:
            json_out[field_name] = json_in[field_name]
        else:
            if type_field is bool:
                if default_value is None:
                    default_value = False
                json_out[field_name] = default_value
            if type_field is str:
                if default_value is None:
                    default_value = ""
                json_out[field_name] = default_value
            if type_field is dict:
                json_out[field_name] = dict()
            if type_field is list:
                json_out[field_name] = []

    @staticmethod
    def _get_element_in_db_from_id(element_type, element_id, user_id, policy_id, category_id,
                                   meta_rule_id, manager):
        # the item is supposed to be in the db, we check it exists!
        if element_type == "model":
            data_db = manager.get_models(moon_user_id=user_id, model_id=element_id)
        elif element_type == "policy":
            data_db = manager.get_policies(moon_user_id=user_id, policy_id=element_id)
        elif element_type == "subject":
            data_db = manager.get_subjects(moon_user_id=user_id, policy_id=policy_id, perimeter_id=element_id)
        elif element_type == "object":
            data_db = manager.get_objects(moon_user_id=user_id, policy_id=policy_id, perimeter_id=element_id)
        elif element_type == "action":
            data_db = manager.get_actions(moon_user_id=user_id, policy_id=policy_id, perimeter_id=element_id)
        elif element_type == "subject_category":
            data_db = manager.get_subject_categories(moon_user_id=user_id, category_id=element_id)
        elif element_type == "object_category":
            data_db = manager.get_object_categories(moon_user_id=user_id, category_id=element_id)
        elif element_type == "action_category":
            data_db = manager.get_action_categories(moon_user_id=user_id, category_id=element_id)
        elif element_type == "meta_rule":
            data_db = manager.get_meta_rules(moon_user_id=user_id, meta_rule_id=element_id)
        elif element_type == "subject_data":
            data_db = manager.get_subject_data(moon_user_id=user_id, policy_id=policy_id, data_id=element_id,
                                               category_id=category_id)
        elif element_type == "object_data":
            data_db = manager.get_object_data(moon_user_id=user_id, policy_id=policy_id, data_id=element_id,
                                              category_id=category_id)
        elif element_type == "action_data":
            data_db = manager.get_action_data(moon_user_id=user_id, policy_id=policy_id,
                                              data_id=element_id,
                                              category_id=category_id)
        elif element_type == "meta_rule":
            data_db = manager.get_meta_rules(moon_user_id=user_id, meta_rule_id=meta_rule_id)
        else:
            raise Exception("Conversion of {} not implemented yet!".format(element_type))

        # do some post processing ... the result should be {key : { .... .... } }
        if element_type == "subject_data" or element_type == "object_data" or element_type == "action_data":
            if data_db is not None and isinstance(data_db, list):
                # TODO remove comments after fixing the bug on moondb when adding metarule:
                #  we can have several identical entries !
                # if len(data_db) > 1:
                #    raise Exception("Several {} with the same id : {}".format(element_type, data_db))
                data_db = data_db[0]

            if data_db is not None and data_db["data"] is not None and isinstance(data_db["data"],
                                                                                  dict):
                # TODO remove comments after fixing the bug on moondb when adding metarule:
                #  we can have several identical entries !
                # if len(data_db["data"].values()) != 1:
                #    raise Exception("Several {} with the same id : {}".format(element_type, data_db))
                # data_db = data_db["data"]
                # TODO remove these two lines after fixing the bug on moondb when adding metarule:
                #  we can have several identical entries !
                list_values = list(data_db["data"].values())
                data_db = list_values[0]
        return data_db

    @staticmethod
    def _get_element_id_in_db_from_name(element_type, element_name, user_id, policy_id, category_id,
                                        meta_rule_id, manager):
        if element_type == "model":
            data_db = manager.get_models(moon_user_id=user_id)
        elif element_type == "policy":
            data_db = manager.get_policies(moon_user_id=user_id)
        elif element_type == "subject":
            data_db = manager.get_subjects(moon_user_id=user_id, policy_id=policy_id)
        elif element_type == "object":
            data_db = manager.get_objects(moon_user_id=user_id, policy_id=policy_id)
        elif element_type == "action":
            data_db = manager.get_actions(moon_user_id=user_id,policy_id= policy_id)
        elif element_type == "subject_category":
            data_db = manager.get_subject_categories(moon_user_id=user_id)
        elif element_type == "object_category":
            data_db = manager.get_object_categories(moon_user_id=user_id)
        elif element_type == "action_category":
            data_db = manager.get_action_categories(moon_user_id=user_id)
        elif element_type == "meta_rule":
            data_db = manager.get_meta_rules(moon_user_id=user_id)
        elif element_type == "subject_data":
            data_db = manager.get_subject_data(moon_user_id=user_id, policy_id=policy_id,
                                               category_id=category_id)
        elif element_type == "object_data":
            data_db = manager.get_object_data(moon_user_id=user_id, policy_id=policy_id,
                                              category_id=category_id)
        elif element_type == "action_data":
            data_db = manager.get_action_data(moon_user_id=user_id, policy_id=policy_id,
                                              category_id=category_id)
        elif element_type == "meta_rule":
            data_db = manager.get_meta_rules(moon_user_id=user_id)
        elif element_type == "rule":
            data_db = manager.get_rules(moon_user_id=user_id, policy_id=policy_id)
        else:
            raise exceptions.MoonError("Conversion of {} not implemented yet!".format(element_type))

        if isinstance(data_db, dict):
            for key_id in data_db:
                if isinstance(data_db[key_id], dict) and "name" in data_db[key_id]:
                    if data_db[key_id]["name"] == element_name:
                        return key_id
        else:
            for elt in data_db:
                if isinstance(elt, dict) and "data" in elt:
                    # we handle here subject_data, object_data and action_data...
                    for data_key in elt["data"]:
                        data = elt["data"][data_key]
                        if "name" in data and data["name"] == element_name:
                            return data_key
                        if "value" in data and data["value"]["name"] == element_name:
                            return data_key
        return None

    @staticmethod
    def convert_name_to_id(json_in, json_out, field_name_in, field_name_out, element_type, manager,
                           user_id, policy_id=None, category_id=None, meta_rule_id=None,
                           field_mandatory=True):
        if field_name_in not in json_in:
            raise exceptions.UnknownField(
                "The field {} is not in the input json".format(field_name_in))

        if "id" in json_in[field_name_in]:
            data_db = JsonUtils._get_element_in_db_from_id(element_type,
                                                           json_in[field_name_in]["id"], user_id,
                                                           policy_id, category_id, meta_rule_id,
                                                           manager)
            if data_db is None:
                raise exceptions.UnknownId("No {} with id {} found in database".format(element_type,
                                                                    json_in[field_name_in]["id"]))
            json_out[field_name_out] = json_in[field_name_in]["id"]

        elif "name" in json_in[field_name_in]:
            id_in_db = JsonUtils._get_element_id_in_db_from_name(element_type,
                                                                 json_in[field_name_in]["name"],
                                                                 user_id, policy_id, category_id,
                                                                 meta_rule_id, manager)
            if id_in_db is None:
                raise exceptions.UnknownName(
                    "No {} with name {} found in database".format(element_type,
                                                                  json_in[field_name_in]["name"]))
            json_out[field_name_out] = id_in_db
        elif field_mandatory is True:
            raise exceptions.MissingIdOrName(
                "No id or name found in the input json {}".format(json_in))

    @staticmethod
    def convert_id_to_name(id_, json_out, field_name_out, element_type, manager, user_id,
                           policy_id=None, category_id=None, meta_rule_id=None):
        json_out[field_name_out] = {
            "name": JsonUtils.convert_id_to_name_string(id_, element_type, manager, user_id,
                                                        policy_id, category_id, meta_rule_id)}

    @staticmethod
    def __convert_results_to_element(element):
        if isinstance(element, dict) and "name" not in element and "value" not in element:
            list_values = [v for v in element.values()]
        elif isinstance(element, list):
            list_values = element
        else:
            list_values = []
            list_values.append(element)
        return list_values[0]

    @staticmethod
    def convert_id_to_name_string(id_, element_type, manager, user_id,
                                  policy_id=None, category_id=None, meta_rule_id=None):

        element = JsonUtils._get_element_in_db_from_id(element_type, id_, user_id, policy_id,
                                                       category_id, meta_rule_id, manager)
        if element is None:
            raise exceptions.UnknownId("No {} with id {} found in database".format(
                element_type, id_))
        res = JsonUtils.__convert_results_to_element(element)
        if "name" in res:
            return res["name"]
        if "value" in res and "name" in res["value"]:
            return res["value"]["name"]
        return None

    @staticmethod
    def convert_names_to_ids(json_in, json_out, field_name_in, field_name_out, element_type,
                             manager, user_id, policy_id=None, category_id=None, meta_rule_id=None,
                             field_mandatory=True):
        ids = []
        if field_name_in not in json_in:
            raise exceptions.UnknownField("The field {} is not in the input json".format(
                field_name_in))

        for elt in json_in[field_name_in]:
            if "id" in elt:
                data_db = JsonUtils._get_element_in_db_from_id(element_type, elt["id"], user_id,
                                                               policy_id, category_id,
                                                               meta_rule_id, manager)
                if data_db is None:
                    raise exceptions.UnknownId(
                        "No {} with id {} found in database".format(element_type, elt["id"]))
                ids.append(elt["id"])
            elif "name" in elt:
                id_in_db = JsonUtils._get_element_id_in_db_from_name(element_type, elt["name"],
                                                                     user_id, policy_id,
                                                                     category_id, meta_rule_id,
                                                                     manager)
                if id_in_db is None:
                    LOGGER.debug("No {} with name {} found in database".format(element_type, elt["name"]))
                    raise exceptions.UnknownName(
                        "No {} with name {} found in database".format(element_type, elt["name"]))
                ids.append(id_in_db)
            elif "attr" in elt:
                ids.append("attributes:" + elt['attr'])
            elif field_mandatory is True:
                raise exceptions.MissingIdOrName(
                    "No id or name found in the input json {}".format(elt))
        json_out[field_name_out] = ids

    @staticmethod
    def convert_ids_to_names(ids, json_out, field_name_out, element_type, manager, user_id,
                             policy_id=None, category_id=None, meta_rule_id=None):
        res_array = []
        for id_ in ids:
            element = JsonUtils._get_element_in_db_from_id(element_type, id_, user_id, policy_id,
                                                           category_id, meta_rule_id, manager)
            if element is None:
                raise exceptions.UnknownId("No {} with id {} found in database".format(
                    element_type, id_))
            res = JsonUtils.__convert_results_to_element(element)
            if "name" in res:
                res_array.append({"name": res["name"]})
            if "value" in res and "name" in res["value"]:
                res_array.append({"name": res["value"]["name"]})
        json_out[field_name_out] = res_array


class JsonImport(object):
    __user_id = None
    __manager = None
    __driver = None

    def __init__(self, driver_name="db", driver=None):
        self.__driver = driver_name
        if driver_name == "db":
            self.__manager = DBManager(driver)
        else:
            self.__manager = CacheManager(driver)

    @property
    def driver(self):
        return self.__manager

    def _reorder_rules_ids(self, rule, ordered_perimeter_categories_ids, json_data_ids, policy_id,
                           get_function):
        ordered_json_ids = [None] * len(ordered_perimeter_categories_ids)
        _exc = None
        data = get_function(moon_user_id=self.__user_id, policy_id=policy_id)
        for _data in data:
            for item in json_data_ids:
                if not _data['data']:
                    continue
                if _data.get('data').get(item):
                    index = ordered_perimeter_categories_ids.index(_data["category_id"])
                    if _data["category_id"] not in ordered_perimeter_categories_ids:
                        _exc = exceptions.InvalidJson(
                            "The category id {} of the rule {} does not match the meta rule".format(
                                _data["category_id"], rule))
                        continue
                    if ordered_json_ids[index] is not None:
                        _exc = exceptions.InvalidJson(
                            "The category id {} of the rule {} shall not be used "
                            "twice in the same rule".format(
                                _data["category_id"], rule))
                    ordered_json_ids[index] = item
        if None in ordered_json_ids:
            for cpt, _id in enumerate(ordered_perimeter_categories_ids):
                if _id.startswith("attributes:"):
                    if not ordered_json_ids[cpt]:
                        ordered_json_ids[cpt] = json_data_ids[cpt]

        if _exc:
            raise _exc
        return ordered_json_ids

    def _import_rules(self, json_rules):
        if not isinstance(json_rules, list):
            raise exceptions.InvalidJson("rules shall be a list!")

        for json_rule in json_rules:
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_rule, json_to_use, "instructions", str)
            JsonUtils.copy_field_if_exists(json_rule, json_to_use, "enabled", bool,
                                           default_value=True)

            json_ids = dict()
            JsonUtils.convert_name_to_id(json_rule, json_ids, "policy", "policy_id", "policy",
                                         self.__manager, self.__user_id)
            JsonUtils.convert_name_to_id(json_rule, json_to_use, "meta_rule", "meta_rule_id",
                                         "meta_rule", self.__manager, self.__user_id)
            json_subject_ids = dict()
            json_object_ids = dict()
            json_action_ids = dict()
            JsonUtils.convert_names_to_ids(json_rule["rule"], json_subject_ids, "subject_data",
                                           "subject", "subject_data", self.__manager,
                                           self.__user_id,
                                           json_ids["policy_id"])
            JsonUtils.convert_names_to_ids(json_rule["rule"], json_object_ids, "object_data",
                                           "object", "object_data", self.__manager,
                                           self.__user_id,
                                           json_ids["policy_id"])
            JsonUtils.convert_names_to_ids(json_rule["rule"], json_action_ids, "action_data",
                                           "action", "action_data", self.__manager,
                                           self.__user_id,
                                           json_ids["policy_id"])

            meta_rule = self.__manager.get_meta_rules(
                moon_user_id=self.__user_id,
                meta_rule_id=json_to_use["meta_rule_id"]
            )
            meta_rule = [v for v in meta_rule.values()]
            meta_rule = meta_rule[0]

            json_to_use_rule = self._reorder_rules_ids(json_rule, meta_rule["subject_categories"],
                                                       json_subject_ids["subject"],
                                                       json_ids["policy_id"],
                                                       self.__manager.get_subject_data)
            json_to_use_rule = json_to_use_rule + self._reorder_rules_ids(
                json_rule, meta_rule["object_categories"],
                json_object_ids["object"],
                json_ids["policy_id"],
                self.__manager.get_object_data)
            json_to_use_rule = json_to_use_rule + self._reorder_rules_ids(
                json_rule,
                meta_rule["action_categories"],
                json_action_ids["action"],
                json_ids["policy_id"],
                self.__manager.get_action_data)
            json_to_use["rule"] = json_to_use_rule
            try:
                LOGGER.debug("Adding / updating a rule from json {}".format(json_to_use))
                self.__manager.add_rule(
                    moon_user_id=self.__user_id,
                    policy_id=json_ids["policy_id"],
                    meta_rule_id=json_to_use["meta_rule_id"],
                    value=json_to_use
                )
            except exceptions.RuleExisting as e:
                LOGGER.error("rule existing {}".format(e))
            except exceptions.PolicyUnknown:
                raise exceptions.PolicyUnknown("Unknown policy with id {}".format(
                    json_ids["policy_id"]))

    def _import_meta_rules(self, json_meta_rules):
        imported_mrule = []
        for json_meta_rule in json_meta_rules:
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_meta_rule, json_to_use, "name", str)
            JsonUtils.copy_field_if_exists(json_meta_rule, json_to_use, "description", str)
            JsonUtils.convert_names_to_ids(json_meta_rule, json_to_use, "subject_categories",
                                           "subject_categories", "subject_category",
                                           self.__manager,
                                           self.__user_id)
            JsonUtils.convert_names_to_ids(json_meta_rule, json_to_use, "object_categories",
                                           "object_categories", "object_category",
                                           self.__manager,
                                           self.__user_id)
            JsonUtils.convert_names_to_ids(json_meta_rule, json_to_use, "action_categories",
                                           "action_categories", "action_category",
                                           self.__manager,
                                           self.__user_id)
            LOGGER.debug("Adding / updating a metarule from json {}".format(json_meta_rule))
            try:
                meta_rule = self.__manager.add_meta_rule(
                    moon_user_id=self.__user_id,
                    meta_rule_id=None,
                    value=json_to_use
                )
                LOGGER.debug("Added / updated meta rule : {}".format(meta_rule))
                imported_mrule.append(meta_rule)
            except exceptions.MetaRuleExisting:
                pass
        return imported_mrule

    def _import_subject_object_action_assignments(self, json_item_assignments, type_element):
        import_method = None
        get_method = None
        if type_element == "subject":
            import_method = self.__manager.add_subject_assignment
            get_method = self.__manager.get_subject_data
        elif type_element == "object":
            import_method = self.__manager.add_object_assignment
            get_method = self.__manager.get_object_data
        elif type_element == "action":
            import_method = self.__manager.add_action_assignment
            get_method = self.__manager.get_action_data

        if not isinstance(json_item_assignments, list):
            raise exceptions.InvalidJson(type_element + " assignments shall be a list!")

        # get the policy id related to the user
        policies = self.__manager.get_policies(moon_user_id=self.__user_id)

        for json_item_assignment in json_item_assignments:
            item_override = JsonUtils.get_override(json_item_assignment)
            if item_override is True:
                raise exceptions.ForbiddenOverride(
                    "{} assignments do not support override flag !".format(type_element))

            json_assignment = dict()
            JsonUtils.convert_name_to_id(json_item_assignment, json_assignment, "category",
                                         "category_id", type_element + "_category",
                                         self.__manager,
                                         self.__user_id)

            has_found_data = False
            # loop over policies
            for policy_id in policies:
                json_data = dict()
                try:
                    JsonUtils.convert_name_to_id(json_item_assignment, json_assignment,
                                                 type_element, "id", type_element,
                                                 self.__manager,
                                                 self.__user_id, policy_id)
                    JsonUtils.convert_names_to_ids(json_item_assignment, json_data, "assignments",
                                                   "data_id", type_element + "_data",
                                                   self.__manager,
                                                   self.__user_id, policy_id,
                                                   json_assignment["category_id"])
                    has_found_data = True
                except exceptions.UnknownName:
                    # the category or data has not been found in this policy:
                    # we look into the next one
                    continue
                for data_id in json_data["data_id"]:
                    # find the policy related to the current data
                    data = get_method(moon_user_id=self.__user_id, policy_id=policy_id,
                                      data_id=data_id,
                                      category_id=json_assignment["category_id"])
                    if data is not None and len(data) == 1:
                        LOGGER.debug(
                            "Adding / updating a {} assignment from json {}".format(
                                type_element,
                                json_assignment))
                        args = {"moon_user_id": self.__user_id, "policy_id": policy_id,
                                type_element + "_id": json_assignment["id"],
                                "category_id": json_assignment["category_id"], "data_id": data_id}
                        try:
                            import_method(**args)
                        except exceptions.SubjectAssignmentExisting:
                            pass
                        except exceptions.ObjectAssignmentExisting:
                            pass
                        except exceptions.ActionAssignmentExisting:
                            pass
                    else:
                        raise exceptions.DataUnknown("Unknown data with id {}".format(data_id))

            # case the data has not been found in any policies
            if has_found_data is False:
                raise exceptions.InvalidJson(
                    "The json contains unknown {} data or category : {}".format(
                        type_element,
                        json_item_assignment))

    def _import_subject_object_action_datas(self, json_items_data, mandatory_policy_ids,
                                            type_element):
        import_method = None
        if type_element == "subject":
            import_method = self.__manager.set_subject_data
        elif type_element == "object":
            import_method = self.__manager.set_object_data
        elif type_element == "action":
            import_method = self.__manager.set_action_data

        if not isinstance(json_items_data, list):
            raise exceptions.InvalidJson(type_element + " data shall be a list!")

        for json_item_data in json_items_data:
            item_override = JsonUtils.get_override(json_items_data)
            if item_override is True:
                raise exceptions.ForbiddenOverride(
                    "{} datas do not support override flag !".format(type_element))
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_item_data, json_to_use, "name", str)
            JsonUtils.copy_field_if_exists(json_item_data, json_to_use, "description", str)
            json_policy = dict()
            # field_mandatory : not mandatory if there is some mandatory policies
            JsonUtils.convert_names_to_ids(json_item_data, json_policy, "policies", "policy_id",
                                           "policy",
                                           self.__manager, self.__user_id,
                                           field_mandatory=len(mandatory_policy_ids) == 0)
            json_category = dict()
            JsonUtils.convert_name_to_id(json_item_data, json_category, "category", "category_id",
                                         type_element + "_category",
                                         self.__manager, self.__user_id)
            policy_ids = []
            if "policy_id" in json_policy:
                policy_ids = json_policy["policy_id"]

            for policy_id in policy_ids:
                if policy_id is not None and policy_id not in mandatory_policy_ids:
                    mandatory_policy_ids.append(policy_id)

            if len(mandatory_policy_ids) == 0:
                raise exceptions.InvalidJson("Invalid data, the policy shall be set when "
                                             "importing {}".format(json_item_data))
            category_id = None
            if "category_id" in json_category:
                category_id = json_category["category_id"]
            if category_id is None:
                raise exceptions.InvalidJson(
                    "Invalid data, the category shall be set when importing {}".format(
                        json_item_data))

            for policy_id in mandatory_policy_ids:
                try:
                    import_method(moon_user_id=self.__user_id, policy_id=policy_id,
                                  category_id=category_id,
                                  value=json_to_use)
                except exceptions.PolicyUnknown:
                    raise exceptions.PolicyUnknown("Unknown policy with id {}".format(policy_id))
                except exceptions.SubjectScopeExisting:
                    pass
                except exceptions.ObjectScopeExisting:
                    pass
                except exceptions.ActionScopeExisting:
                    pass
                except Exception as e:
                    LOGGER.exception(str(e))
                    raise e

    def _import_subject_object_action_categories(self, json_item_categories, type_element):
        imported_oac = []
        import_method = None
        get_method = None
        if type_element == "subject":
            import_method = self.__manager.add_subject_category
            get_method = self.__manager.get_subject_categories
        elif type_element == "object":
            import_method = self.__manager.add_object_category
            get_method = self.__manager.get_object_categories
        elif type_element == "action":
            import_method = self.__manager.add_action_category
            get_method = self.__manager.get_action_categories

        categories = get_method(moon_user_id=self.__user_id)

        if not isinstance(json_item_categories, list):
            raise exceptions.InvalidJson(type_element + " categories shall be a list!")

        for json_item_category in json_item_categories:
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_item_category, json_to_use, "name", str)

            # check if category with the same name exists : do this in moondb ?
            existing_id = None
            for category_key in categories:
                if categories[category_key]["name"] == json_to_use["name"]:
                    existing_id = category_key

            JsonUtils.copy_field_if_exists(json_item_category, json_to_use, "description", str)
            item_override = JsonUtils.get_override(json_item_category)
            if item_override is True:
                raise exceptions.ForbiddenOverride(
                    "{} categories do not support override flag !".format(type_element))

            try:
                import_method(moon_user_id=self.__user_id, category_id=existing_id,
                              value=json_to_use)
            except (exceptions.SubjectCategoryExisting, exceptions.ObjectCategoryExisting,
                    exceptions.ActionCategoryExisting):
                # it already exists: do nothing
                LOGGER.warning("Ignored {} category with name {} is already in the database".format(
                    type_element, json_to_use["name"]))
            except Exception as e:
                LOGGER.warning("Error while importing the category : {}".format(str(e)))
                LOGGER.exception(str(e))
                raise e
            imported_oac.append({
                'category': type_element,
                'name': json_to_use["name"]})
        return imported_oac

    def _import_subject_object_action(self, json_items, mandatory_policy_ids, type_element):
        import_method = None
        get_method = None
        if type_element == "subject":
            import_method = self.__manager.add_subject
            get_method = self.__manager.get_subjects
        elif type_element == "object":
            import_method = self.__manager.add_object
            get_method = self.__manager.get_objects
        elif type_element == "action":
            import_method = self.__manager.add_action
            get_method = self.__manager.get_actions

        if not isinstance(json_items, list):
            raise exceptions.InvalidJson(type_element + " items shall be a list!")

        for json_item in json_items:
            json_without_policy_name = dict()
            JsonUtils.copy_field_if_exists(json_item, json_without_policy_name, "name", str)
            JsonUtils.copy_field_if_exists(json_item, json_without_policy_name, "description", str)
            JsonUtils.copy_field_if_exists(json_item, json_without_policy_name, "extra", dict)

            policy_list_ids = {}
            JsonUtils.convert_names_to_ids(json_item, policy_list_ids, "policies",
                                           "policy_list", "policy", self.__manager,
                                           self.__user_id,
                                           field_mandatory=False)
            policy_ids = policy_list_ids["policy_list"]
            # json_without_policy_name["policies"] = []
            for mandatory_policy_id in mandatory_policy_ids:
                if mandatory_policy_id not in policy_ids:
                    policy_ids.append(mandatory_policy_id)
                    # policy_ids and json_without_policy_name are references to the same array...
                    # json_without_policy_name["policy_list"].append(mandatory_policy_id)

            item_override = JsonUtils.get_override(json_item)
            if item_override is True:
                raise exceptions.ForbiddenOverride("{} does not support override flag !".format(
                    type_element))

            if len(policy_ids) == 0:
                raise exceptions.PolicyUnknown(
                    "a {} needs at least one policy to be created or updated : {}".format(
                        type_element, json.dumps(json_item)))

            for policy_id in policy_ids:
                try:
                    items_in_db = get_method(moon_user_id=self.__user_id, policy_id=policy_id)
                    items_in_db = items_in_db.get(policy_id, {})
                    key = None
                    for key_in_db in items_in_db:
                        if items_in_db[key_in_db]["name"] == json_without_policy_name["name"]:
                            key = key_in_db
                            break
                    try:
                        element = import_method(moon_user_id=self.__user_id, policy_id=policy_id,
                                                perimeter_id=key,
                                                value=json_without_policy_name)
                        LOGGER.debug("Added / updated {} : {}".format(type_element, element))
                    except exceptions.PolicyExisting:
                        pass

                except exceptions.PolicyUnknown:
                    LOGGER.error("Unknown policy when adding a {}!".format(
                        type_element))
                    raise exceptions.PolicyUnknown("Unknown policy when adding a {}!".format(
                        type_element))
                except Exception as e:
                    LOGGER.exception(str(e))
                    raise e

    def _import_policies(self, json_policies):
        policy_mandatory_ids = []
        policy_mandatory_names = []

        if not isinstance(json_policies, list):
            raise exceptions.InvalidJson("policies shall be a list!")

        for json_policy in json_policies:
            # TODO put this in moondb
            # policy_in_db =
            #     self.driver.PolicyManager.get_policies_by_name(json_without_model_name["name"])
            policies = self.__manager.get_policies(moon_user_id=self.__user_id)
            policy_in_db = None
            policy_id = None
            for policy_key in policies:
                if policies[policy_key]["name"] == json_policy["name"]:
                    policy_in_db = policies[policy_key]
                    policy_id = policy_key
            # end TODO
            if policy_in_db is None:
                policy_does_exist = False
            else:
                policy_does_exist = True

            policy_override = JsonUtils.get_override(json_policy)
            policy_mandatory = JsonUtils.get_mandatory(json_policy)

            if policy_override is False and policy_does_exist:
                if policy_id:
                    policy_mandatory_ids.append(policy_id)
                    policy_mandatory_names.append(json_policy["name"])
                    LOGGER.warning(
                        "Existing policy not updated because of the override option is not set !")
                    continue

            json_without_model_name = dict()
            JsonUtils.copy_field_if_exists(json_policy, json_without_model_name, "name", str)
            JsonUtils.copy_field_if_exists(json_policy, json_without_model_name, "description", str)
            JsonUtils.copy_field_if_exists(json_policy, json_without_model_name, "genre", str)
            JsonUtils.convert_name_to_id(json_policy, json_without_model_name, "model", "model_id",
                                         "model", self.__manager, self.__user_id,
                                         field_mandatory=False)

            if not policy_does_exist:
                LOGGER.debug("Creating policy {} ".format(json_without_model_name))
                added_policy = self.__manager.add_policy(
                    moon_user_id=self.__user_id,
                    value=json_without_model_name)
                if policy_mandatory is True:
                    keys = list(added_policy.keys())
                    policy_mandatory_ids.append(keys[0])
                    policy_mandatory_names.append(json_policy["name"])
            elif policy_override is True:
                LOGGER.debug("Updating policy {} ".format(json_without_model_name))
                self.__manager.update_policy(moon_user_id=self.__user_id,
                                             policy_id=policy_id,
                                             value=json_without_model_name)
                if policy_mandatory is True:
                    policy_mandatory_ids.append(policy_id)
                    policy_mandatory_names.append(json_policy["name"])
        return [policy_mandatory_ids, policy_mandatory_names]

    def _import_models_with_new_meta_rules(self, json_models):
        if not isinstance(json_models, list):
            raise exceptions.InvalidJson("models shall be a list!")

        for json_model in json_models:
            models = self.__manager.get_models(moon_user_id=self.__user_id)
            model_in_db = None
            model_id = None
            for model_key in models:
                if ("id" in json_model and model_key == json_model["id"]) or (
                        "name" in json_model and models[model_key]["name"] == json_model["name"]):
                    model_in_db = models[model_key]
                    model_id = model_key

            # this should not occur as the model has been put in db previously in
            # import_models_without_new_meta_rules
            if model_in_db is None:
                raise exceptions.ModelUnknown("Unknown model")

            json_key = dict()
            JsonUtils.convert_names_to_ids(json_model, json_key, "meta_rules", "meta_rule_id",
                                           "meta_rule", self.__manager, self.__user_id)
            for meta_rule_id in json_key["meta_rule_id"]:
                if meta_rule_id not in model_in_db["meta_rules"]:
                    model_in_db["meta_rules"].append(meta_rule_id)

            self.__manager.update_model(moon_user_id=self.__user_id,
                                        model_id=model_id,
                                        value=model_in_db)

    def _import_models_without_new_meta_rules(self, json_models):
        if not isinstance(json_models, list):
            raise exceptions.InvalidJson("models shall be a list!")
        imported_model_names = []
        for json_model in json_models:
            json_without_new_metarules = dict()
            JsonUtils.copy_field_if_exists(json_model, json_without_new_metarules, "name", str)

            models = self.__manager.get_models(moon_user_id=self.__user_id)
            model_in_db = None
            model_id = None
            for model_key in models:
                if models[model_key]["name"] == json_without_new_metarules["name"]:
                    model_in_db = models[model_key]
                    model_id = model_key

            JsonUtils.copy_field_if_exists(json_model, json_without_new_metarules, "description",
                                           str)
            if model_in_db is None:
                model_does_exist = False
            else:
                json_without_new_metarules["meta_rules"] = model_in_db["meta_rules"]
                model_does_exist = True
            model_override = JsonUtils.get_override(json_model)
            if not model_does_exist:
                LOGGER.debug("Creating model {} ".format(json_without_new_metarules))
                self.__manager.add_model(moon_user_id=self.__user_id,
                                         value=json_without_new_metarules)
            elif model_override is True:
                LOGGER.debug(
                    "Updating model with id {} : {} ".format(model_id, json_without_new_metarules))
                self.__manager.update_model(moon_user_id=self.__user_id,
                                            model_id=model_id,
                                            value=json_without_new_metarules)
        if "name" in json_without_new_metarules:
            imported_model_names.append(json_without_new_metarules["name"])
        return imported_model_names

    def _import_pdps(self, json_pdps):
        if not isinstance(json_pdps, list):
            raise exceptions.InvalidJson("pdps shall be a list!")
        imported_pdp_names = []
        for json_pdp in json_pdps:
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_pdp, json_to_use, "name", str)
            JsonUtils.copy_field_if_exists(json_pdp, json_to_use, "vim_project_id", str)
            JsonUtils.copy_field_if_exists(json_pdp, json_to_use, "security_pipeline", list)
            JsonUtils.copy_field_if_exists(json_pdp, json_to_use, "description", str)

            pdps = self.__manager.get_pdp(moon_user_id=self.__user_id)
            exists = False
            for pdp_key in pdps:
                if pdps[pdp_key]["name"] == json_to_use["name"]:
                    self.__manager.update_pdp(moon_user_id=self.__user_id, pdp_id=pdp_key,
                                      value=json_to_use)
                    exists = True
            if exists is False:
                self.__manager.add_pdp(moon_user_id=self.__user_id, value=json_to_use)
            imported_pdp_names.append(json_to_use["name"])

    def import_json(self, **kwargs):
        if self.__driver == "db":
            if "body" in kwargs:
                return self.__import_json_to_db(kwargs.get("body")).keys()
            else:
                raise Exception("Bad argument given...")
        else:
            if "body" in kwargs:
                return self.__import_json_to_cache(kwargs.get("body")).keys()
            else:
                raise Exception("Bad argument given...")

    def __import_json_to_db(self, body):
        imported_data = {}

        LOGGER.debug("Importing content:  {} ...".format(body))

        # first import the models without the meta rules as they are not yet defined
        if "models" in body:
            LOGGER.info("Importing models...")
            imported_model_names = self._import_models_without_new_meta_rules(body["models"])
            imported_data['models'] = imported_model_names



        # import subjects, object, action_categories
        list_element = [{"key": "subject"}, {"key": "object"}, {"key": "action"}]
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "_categories"
            if key in body:
                LOGGER.info("Importing {}...".format(key))
                imported_oac = self._import_subject_object_action_categories(body[key], in_key)
                imported_data[key] = imported_oac

        # import meta rules
        if "meta_rules" in body:
            LOGGER.info("Importing meta rules...")
            imported_mrules = self._import_meta_rules(body["meta_rules"])
            imported_data["meta_rules"] = imported_mrules

        # add the metarule to model
        if "models" in body:
            LOGGER.info("Updating models with meta rules...")
            self._import_models_with_new_meta_rules(body["models"])

        # import the policies that depends on the models
        mandatory_policy_ids = []
        if "policies" in body:
            LOGGER.info("Importing policies...")
            mandatory_policy_ids, policy_mandatory_names = self._import_policies(body["policies"])
            imported_data["policies"] = {
                'id': mandatory_policy_ids,
                'name': policy_mandatory_names}

        # import subjects, object, action
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "s"
            if key in body:
                LOGGER.info("Importing {}...".format(key))
                imported_sub = self._import_subject_object_action(body[key], mandatory_policy_ids, in_key)
                imported_data[key] = imported_sub

        # import subjects, object, action data
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "_data"
            if key in body:
                LOGGER.info("Importing {}...".format(key))
                imported_sub =self._import_subject_object_action_datas(body[key], mandatory_policy_ids,
                                                         in_key)
                imported_data[key] = imported_sub
                
        # import subjects assignments, idem for object and action
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "_assignments"
            if key in body:
                LOGGER.info("Importing {}...".format(key))
                imported_sub = self._import_subject_object_action_assignments(body[key], in_key)
                imported_data[key] = imported_sub
                
        # import rules
        if "rules" in body:
            LOGGER.info("Importing rules...")
            imported_sub = self._import_rules(body["rules"])
            imported_data["rules"] = imported_sub

        # import pdps
        if "pdps" in body:
            LOGGER.info("Importing pdps...")
            imported_sub = self._import_pdps(body["pdps"])
            imported_data["pdps"] = imported_sub

        return imported_data

    def __import_json_to_cache(self, body):
        imported_data = {}

        LOGGER.debug("Importing content:  {} ...".format(body))

        # first import the models without the meta rules as they are not yet defined
        if "models" in body:
            LOGGER.info("Importing models...")
            imported_model_names = self._import_models_without_new_meta_rules(body["models"])
            imported_data['models'] = imported_model_names


        # import subjects, object, action_categories
        list_element = [{"key": "subject"}, {"key": "object"}, {"key": "action"}]
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "_categories"
            if key in body:
                LOGGER.info("Importing {}...".format(key))
                imported_oac = self._import_subject_object_action_categories(body[key], in_key)
                imported_data[key] = imported_oac

        # import meta rules
        if "meta_rules" in body:
            LOGGER.info("Importing meta rules...")
            imported_mrules = self._import_meta_rules(body["meta_rules"])
            imported_data["meta_rules"] = imported_mrules

        # add the metarule to model
        if "models" in body:
            LOGGER.info("Updating models with meta rules...")
            self._import_models_with_new_meta_rules(body["models"])

        # import the policies that depends on the models
        mandatory_policy_ids = []
        if "policies" in body:
            LOGGER.info("Importing policies...")
            mandatory_policy_ids, policy_mandatory_names = self._import_policies(body["policies"])
            imported_data["policies"] = {
                'id': mandatory_policy_ids,
                'name': policy_mandatory_names}

        # import subjects, object, action
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "s"
            if key in body:
                LOGGER.info("Importing {}...".format(key))
                imported_sub = self._import_subject_object_action(body[key], mandatory_policy_ids, in_key)
                imported_data[key] = imported_sub

        #import subjects, object, action data
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "_data"
            if key in body:
                LOGGER.info("Importing {}...".format(key))
                imported_sub= self._import_subject_object_action_datas(body[key], mandatory_policy_ids,
                                                         in_key)
                imported_data[key] = imported_sub

        # import subjects assignments, idem for object and action
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "_assignments"
            if key in body:
                LOGGER.info("Importing {}...".format(key))
                imported_sub = self._import_subject_object_action_assignments(body[key], in_key)
                imported_data[key] = imported_sub

        # import rules
        if "rules" in body:
            LOGGER.info("Importing rules...")
            imported_sub = self._import_rules(body["rules"])
            imported_data["rules"] = imported_sub

        # import pdps
        if "pdps" in body:
            LOGGER.info("Importing pdps...")
            imported_sub = self._import_pdps(body["pdps"])
            imported_data["pdps"] = imported_sub
        return imported_data


class JsonExport(object):
    __user_id = None
    __dirver = None
    __manager = None

    def __init__(self, driver_name="db", driver=None):
        self.__driver = driver_name
        if driver_name == "db":
            self.__manager = DBManager(driver)
        else:
            self.__manager = CacheManager(driver)

    def _export_rules(self, json_content):
        policies = self.__manager.get_policies(moon_user_id=self.__user_id)
        rules_array = []

        for policy_key in policies:
            rules = self.__manager.get_rules(moon_user_id=self.__user_id, policy_id=policy_key)
            rules = rules["rules"]
            for rule in rules:
                rule_dict = dict()
                JsonUtils.copy_field_if_exists(rule, rule_dict, "instructions", dict)
                JsonUtils.copy_field_if_exists(rule, rule_dict, "enabled", True)
                JsonUtils.convert_id_to_name(rule["meta_rule_id"], rule_dict, "meta_rule",
                                             "meta_rule", self.__manager, self.__user_id)
                JsonUtils.convert_id_to_name(policy_key, rule_dict, "policy", "policy",
                                             self.__manager, self.__user_id)
                ids = rule["rule"]
                rule_description = dict()
                meta_rule = self.__manager.get_meta_rules(moon_user_id=self.__user_id,
                                                  meta_rule_id=rule["meta_rule_id"])
                meta_rule = [v for v in meta_rule.values()]
                meta_rule = meta_rule[0]
                index_subject_data = len(meta_rule["subject_categories"]) - 1
                index_object_data = len(meta_rule["subject_categories"]) + len(
                    meta_rule["object_categories"]) - 1
                index_action_data = len(meta_rule["subject_categories"]) + len(
                    meta_rule["object_categories"]) + len(meta_rule["action_categories"]) - 1
                ids_subject_data = [ids[0]] if len(meta_rule["subject_categories"]) == 1 else ids[
                                                                                              0:index_subject_data]
                ids_object_data = [ids[index_object_data]] if len(
                    meta_rule["object_categories"]) == 1 else ids[
                                                              index_subject_data + 1:index_object_data]
                ids_action_date = [ids[index_action_data]] if len(
                    meta_rule["action_categories"]) == 1 else ids[
                                                              index_object_data + 1:index_action_data]
                JsonUtils.convert_ids_to_names(ids_subject_data, rule_description, "subject_data",
                                               "subject_data", self.__manager, self.__user_id,
                                               policy_key)
                JsonUtils.convert_ids_to_names(ids_object_data, rule_description, "object_data",
                                               "object_data", self.__manager, self.__user_id,
                                               policy_key)
                JsonUtils.convert_ids_to_names(ids_action_date, rule_description, "action_data",
                                               "action_data", self.__manager, self.__user_id,
                                               policy_key)
                rule_dict["rule"] = rule_description
                rules_array.append(rule_dict)

        if len(rules_array) > 0:
            json_content['rules'] = rules_array

    def _export_meta_rules(self, json_content):
        meta_rules = self.__manager.get_meta_rules(moon_user_id=self.__user_id)
        meta_rules_array = []
        for meta_rule_key in meta_rules:
            meta_rule_dict = dict()
            JsonUtils.copy_field_if_exists(meta_rules[meta_rule_key], meta_rule_dict, "name", str)
            JsonUtils.copy_field_if_exists(meta_rules[meta_rule_key], meta_rule_dict, "description",
                                           str)
            JsonUtils.convert_ids_to_names(meta_rules[meta_rule_key]["subject_categories"],
                                           meta_rule_dict, "subject_categories", "subject_category",
                                           self.__manager, self.__user_id)
            JsonUtils.convert_ids_to_names(meta_rules[meta_rule_key]["object_categories"],
                                           meta_rule_dict, "object_categories", "object_category",
                                           self.__manager, self.__user_id)
            JsonUtils.convert_ids_to_names(meta_rules[meta_rule_key]["action_categories"],
                                           meta_rule_dict, "action_categories", "action_category",
                                           self.__manager, self.__user_id)
            meta_rules_array.append(meta_rule_dict)
        if len(meta_rules_array) > 0:
            json_content['meta_rules'] = meta_rules_array

    def _export_subject_object_action_assignments(self, type_element, json_content):
        export_method_data = None
        if type_element == "subject":
            export_method_data = self.__manager.get_subject_assignments
        elif type_element == "object":
            export_method_data = self.__manager.get_object_assignments
        if type_element == "action":
            export_method_data = self.__manager.get_action_assignments
        policies = self.__manager.get_policies(moon_user_id=self.__user_id)
        element_assignments_array = []
        for policy_key in policies:
            assignments = export_method_data(moon_user_id=self.__user_id, policy_id=policy_key)
            for assignment_key in assignments:
                assignment_dict = dict()
                JsonUtils.convert_id_to_name(assignments[assignment_key][type_element + "_id"],
                                             assignment_dict, type_element, type_element,
                                             self.__manager, self.__user_id, policy_key)
                JsonUtils.convert_id_to_name(assignments[assignment_key]["category_id"],
                                             assignment_dict, "category",
                                             type_element + "_category", self.__manager,
                                             self.__user_id, policy_key)
                JsonUtils.convert_ids_to_names(assignments[assignment_key]["assignments"],
                                               assignment_dict, "assignments",
                                               type_element + "_data", self.__manager,
                                               self.__user_id,
                                               policy_key)
                element_assignments_array.append(assignment_dict)
                LOGGER.info("Exporting {} assignment {}".format(type_element, assignment_dict))
        if len(element_assignments_array) > 0:
            json_content[type_element + '_assignments'] = element_assignments_array

    def _export_subject_object_action_datas(self, type_element, json_content):
        export_method_data = None
        if type_element == "subject":
            export_method_data = self.__manager.get_subject_data
        elif type_element == "object":
            export_method_data = self.__manager.get_object_data
        if type_element == "action":
            export_method_data = self.__manager.get_action_data
        policies = self.__manager.get_policies(moon_user_id=self.__user_id)
        element_datas_array = []
        for policy_key in policies:
            datas = export_method_data(moon_user_id=self.__user_id, policy_id=policy_key)
            for data_group in datas:
                policy_id = data_group["policy_id"]
                category_id = data_group["category_id"]
                for data_key in data_group["data"]:
                    data_dict = dict()
                    if type_element == 'subject':
                        JsonUtils.copy_field_if_exists(data_group["data"][data_key], data_dict,
                                                       "name", str)
                        JsonUtils.copy_field_if_exists(data_group["data"][data_key], data_dict,
                                                       "description", str)
                    else:
                        JsonUtils.copy_field_if_exists(data_group["data"][data_key], data_dict,
                                                       "name", str)
                        JsonUtils.copy_field_if_exists(data_group["data"][data_key], data_dict,
                                                       "description", str)

                    JsonUtils.convert_id_to_name(policy_id, data_dict, "policy", "policy",
                                                 self.__manager, self.__user_id)
                    JsonUtils.convert_id_to_name(category_id, data_dict, "category",
                                                 type_element + "_category", self.__manager,
                                                 self.__user_id, policy_key)
                    LOGGER.info("Exporting {} data {}".format(type_element, data_dict))
                    element_datas_array.append(data_dict)

        if len(element_datas_array) > 0:
            json_content[type_element + '_data'] = element_datas_array

    def _export_subject_object_action_categories(self, type_element, json_content):
        export_method = None
        if type_element == "subject":
            export_method = self.__manager.get_subject_categories
        elif type_element == "object":
            export_method = self.__manager.get_object_categories
        if type_element == "action":
            export_method = self.__manager.get_action_categories
        element_categories = export_method(moon_user_id=self.__user_id)
        element_categories_array = []
        for element_category_key in element_categories:
            element_category = dict()
            JsonUtils.copy_field_if_exists(element_categories[element_category_key],
                                           element_category, "name", str)
            JsonUtils.copy_field_if_exists(element_categories[element_category_key],
                                           element_category, "description", str)
            element_categories_array.append(element_category)
            LOGGER.info("Exporting {} category {}".format(type_element, element_category))
        if len(element_categories_array) > 0:
            json_content[type_element + '_categories'] = element_categories_array

    def _export_subject_object_action(self, type_element, json_content):
        export_method = None
        if type_element == "subject":
            export_method = self.__manager.get_subjects
        elif type_element == "object":
            export_method = self.__manager.get_objects
        if type_element == "action":
            export_method = self.__manager.get_actions
        policies = self.__manager.get_policies(moon_user_id=self.__user_id)
        element_dict = dict()
        elements_array = []
        for policy_key in policies:
            elements = export_method(moon_user_id=self.__user_id, policy_id=policy_key)
            for element_key in elements:
                element = dict()
                JsonUtils.copy_field_if_exists(elements[element_key], element, "name", str)
                JsonUtils.copy_field_if_exists(elements[element_key], element, "description", str)
                JsonUtils.copy_field_if_exists(elements[element_key], element, "extra", dict)
                if element["name"] not in element_dict:
                    element["policies"] = []
                    element_dict[element["name"]] = element
                current_element = element_dict[element["name"]]
                current_element["policies"].append({"name": JsonUtils.convert_id_to_name_string(
                    policy_key, "policy", self.__manager, self.__user_id)})

        for key in element_dict:
            LOGGER.info("Exporting {} {}".format(type_element, element_dict[key]))
            elements_array.append(element_dict[key])

        if len(elements_array) > 0:
            json_content[type_element + 's'] = elements_array

    def _export_policies(self, json_content):
        policies = self.__manager.get_policies(moon_user_id = self.__user_id)
        policies_array = []
        for policy_key in policies:
            policy = dict()
            JsonUtils.copy_field_if_exists(policies[policy_key], policy, "name", str)
            JsonUtils.copy_field_if_exists(policies[policy_key], policy, "genre", str)
            JsonUtils.copy_field_if_exists(policies[policy_key], policy, "description", str)
            JsonUtils.convert_id_to_name(policies[policy_key]["model_id"], policy, "model", "model",
                                         self.__manager, self.__user_id)
            LOGGER.info("Exporting policy {}".format(policy))
            policies_array.append(policy)
        if len(policies_array) > 0:
            json_content["policies"] = policies_array

    def _export_models(self, json_content):
        models = self.__manager.get_models(moon_user_id=self.__user_id)
        models_array = []
        for model_key in models:
            model = dict()
            JsonUtils.copy_field_if_exists(models[model_key], model, "name", str)
            JsonUtils.copy_field_if_exists(models[model_key], model, "description", str)
            JsonUtils.convert_ids_to_names(models[model_key]["meta_rules"], model, "meta_rules",
                                           "meta_rule", self.__manager, self.__user_id)
            LOGGER.info("Exporting model {}".format(model))
            models_array.append(model)
        if len(models_array) > 0:
            json_content["models"] = models_array

    def _export_pdps(self, json_content):
        pdps = self.__manager.get_pdp(moon_user_id=self.__user_id)
        pdps_array = []
        for pdp_key in pdps:
            LOGGER.info("Exporting pdp {}".format(pdps[pdp_key]))
            pdps_array.append(pdps[pdp_key])
        if len(pdps_array) > 0:
            json_content["pdps"] = pdps_array

    def export_json(self, **kwargs):
        if self.__driver == "db":
            if "moon_user_id" in kwargs:
                return self.__export_json_from_db(kwargs.get("moon_user_id"))
            else:
                raise Exception("Bad argument given...")
        else:
            if "body" in kwargs:
                return self.__export_json_from_db(kwargs.get("body"))
            else:
                raise Exception("Bad argument given...")

    def __export_json_from_db(self, moon_user_id=None):
        self.__user_id = moon_user_id

        json_content = dict()

        LOGGER.info("Exporting pdps...")
        self._export_pdps(json_content)
        LOGGER.info("Exporting policies...")
        self._export_policies(json_content)
        LOGGER.info("Exporting models...")
        self._export_models(json_content)
        # export subjects, subject_data, subject_categories, subject_assignements
        # idem for object and action
        list_element = [{"key": "subject"}, {"key": "object"}, {"key": "action"}]
        for elt in list_element:
            LOGGER.info("Exporting {}s...".format(elt["key"]))
            self._export_subject_object_action(elt["key"], json_content)
            LOGGER.info("Exporting {} categories...".format(elt["key"]))
            self._export_subject_object_action_categories(elt["key"], json_content)
            LOGGER.info("Exporting {} data...".format(elt["key"]))
            self._export_subject_object_action_datas(elt["key"], json_content)
            LOGGER.info("Exporting {} assignments...".format(elt["key"]))
            self._export_subject_object_action_assignments(elt["key"], json_content)
        LOGGER.info("Exporting meta rules...")
        self._export_meta_rules(json_content)
        LOGGER.info("Exporting rules...")
        self._export_rules(json_content)

        return json_content
