# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
import time
import copy
from uuid import uuid4
import moon_cache.request_wrapper as requests
from moon_utilities import exceptions

logger = logging.getLogger("moon.cache.cache")


class Cache(object):
    """
    Cache object allowing to save all data for a specific moon component
    """

    __UPDATE_INTERVAL = 10

    __MANAGER_API_KEY = None

    __CURRENT_SERVER = None
    __CURRENT_SERVER_API_KEY = None

    __pipelines = {}
    __PIPELINES_UPDATE = 0

    __security_functions = {}
    __SECURITY_FUNCTIONS_UPDATE = 0

    __attributes = {}
    __ATTRS_UPDATE = 0

    __pdp = {}
    __PDP_UPDATE = 0

    __policies = {}
    __POLICIES_UPDATE = 0

    __models = {}
    __MODELS_UPDATE = 0

    __subjects = {}
    __objects = {}
    __actions = {}

    __subject_assignments = {}
    __object_assignments = {}
    __action_assignments = {}

    __subject_categories = {}
    __SUBJECT_CATEGORIES_UPDATE = 0
    __object_categories = {}
    __OBJECT_CATEGORIES_UPDATE = 0
    __action_categories = {}
    __ACTION_CATEGORIES_UPDATE = 0

    __meta_rules = {}
    __META_RULES_UPDATE = 0

    __rules = {}
    __RULES_UPDATE = 0

    __subject_data = []
    __object_data = []
    __action_data = []

    __authz_requests = {}

    __instance = None

    @staticmethod
    def getInstance(manager_url=None, incremental=True, manager_api_key=None, static_conf=None):
        """ Static access method. """

        if Cache.__instance == None:
            Cache(manager_url, incremental, manager_api_key, static_conf)

        return Cache.__instance

    @staticmethod
    def deleteInstance():
        Cache.__instance = None

    def __init__(self, manager_url=None, incremental=True, manager_api_key=None, static_conf=None):

        if Cache.__instance != None:
            raise exceptions.MoonError("This class is a singleton! use getInstance() instead")
        else:
            Cache.__instance = self

        self.manager_url = manager_url
        self.incremental = incremental
        self.headers = {"X-Api-Key": manager_api_key}
        self.__MANAGER_API_KEY = manager_api_key

        if self.manager_url:
            self.update()
        elif static_conf:
            self.update_from_static_conf(static_conf)
        logger.info("Update done!")

    def update(self, pdp_id=None, pipeline=None):
        """
        Force the update of one or more elements
        :param pdp_id: PDP ID
        :param pipeline: Pipeline ID
        :return: None
        """
        if not self.manager_url:
            return
        if pipeline:
            # if we are in wrapper, retrieve pipeline list from pdp
            self.__update_pipelines(pipeline)
        else:
            # else update pdp and policy list
            self.__update_pdp(pdp_id)
            self.__update_policies(pdp_id)
            if not self.incremental:
                # if it is written in config file ; retrieve all data from Manager
                self.__update_models()
                self.__update_meta_rules()
                self.__update_rules()
                self.__update_subject_categories()
                self.__update_object_categories()
                self.__update_action_categories()
                for _policy_id in self.__policies:
                    self.__update_subjects(_policy_id)
                    self.__update_objects(_policy_id)
                    self.__update_actions(_policy_id)
                    self.__update_subject_assignments(_policy_id)
                    self.__update_object_assignments(_policy_id)
                    self.__update_action_assignments(_policy_id)

    def set_current_server(self, url, api_key):
        self.__CURRENT_SERVER = url
        self.__CURRENT_SERVER_API_KEY = api_key

    @staticmethod
    def __update_list_to_dict(data):
        """
        Transform a list in a dictionary
        :param data: the list to be transformed
        :return: a dictionary
        """
        return {uuid4().hex: value for value in data}

    def update_from_static_conf(self, conf):
        """
        Get the data in the JSON file and save its content into the cache
        :param conf: the content of the JSON file
        :return:
        """
        logger.info("update_from_static_conf {}".format(conf.get("policies", [])))
        self.__pdp = self.__update_list_to_dict(conf.get("pdp", []))
        self.__policies = self.__update_list_to_dict(conf.get("policies", []))
        self.__models = self.__update_list_to_dict(conf.get("models", []))
        self.__subjects = self.__update_list_to_dict(conf.get("subjects", []))
        self.__objects = self.__update_list_to_dict(conf.get("objects", []))
        self.__actions = self.__update_list_to_dict(conf.get("actions", []))
        self.__subject_categories = self.__update_list_to_dict(conf.get("subjects_categories", []))
        self.__object_categories = self.__update_list_to_dict(conf.get("objects_categories", []))
        self.__action_categories = self.__update_list_to_dict(conf.get("actions_categories", []))
        # FIXME: should add DATA in Cache
        self.__subject_data = conf.get("subjects_data", [])
        self.__object_data = conf.get("objects_data", [])
        self.__action_data = conf.get("actions_data", [])
        self.__subject_assignments = self.__update_list_to_dict(conf.get("subjects_assignments", []))
        self.__object_assignments = self.__update_list_to_dict(conf.get("objects_assignments", []))
        self.__action_assignments = self.__update_list_to_dict(conf.get("actions_assignments", []))
        self.__rules = conf.get("rules", [])
        self.__meta_rules = self.__update_list_to_dict(conf.get("meta_rules", []))

    @property
    def manager_api_token(self):
        return self.__MANAGER_API_KEY

    @property
    def authz_requests(self):
        """
        Authorization requests
        :return: a dictionary
        """
        return self.__authz_requests

    # Attributes

    @property
    def attributes(self):
        """
        Global attributes
        :return: a dictionary containing attributes
        """
        _keys = list(self.__attributes.keys())
        self.update_attribute()
        return self.__attributes

    def set_attribute(self, name, value=None):
        """
        Set one global attribute
        :return: a dictionary containing attributes
        """
        self.__attributes[name] = value
        return self.__attributes

    def update_attribute(self, name=None):
        """
        Update one global attribute from the Manager
        :return: a dictionary containing attributes
        """
        if self.manager_url:
            if not name:
                response = requests.get("{}/attributes".format(self.manager_url),
                                        headers=self.headers)
                for key in response.json()["attributes"]:
                    self.__attributes[key] = response.json()["attributes"][key]['value']
            else:
                response = requests.get("{}/attributes/{}".format(self.manager_url, name),
                                        headers=self.headers)
                self.__attributes[name] = response.json()["attributes"]['value']

    # perimeter functions

    def __check_policies(self, policy_ids):
        for policy in policy_ids:
            if policy not in self.__policies:
                raise exceptions.PolicyUnknown

    @property
    def subjects(self):
        """
        Subjects
        :return: a dictionary
        """
        return self.__subjects

    def add_subject(self, value):
        _id = value.get("id", uuid4().hex)
        self.__check_policies(value.get("policy_list", []))
        policy_id = value.get("policy_list", [])[0]
        if policy_id not in self.__subjects:
            self.__subjects[policy_id] = {_id: dict(value)}
        else:
            self.__subjects[policy_id][_id] = dict(value)
        return {_id: dict(value)}

    def delete_subject(self, policy_id=None, perimeter_id=None):
        if not policy_id and perimeter_id:
            self.__subjects.pop(perimeter_id)
            return
        elif not perimeter_id:
            self.__subjects = {}
            return
        self.__check_policies([policy_id])
        self.__subjects[perimeter_id].get("policies").remove(policy_id)

    def update_subject(self, perimeter_id, value):
        self.__check_policies(value.get("policies", []))
        policy_id = value.get("policy_list", [])[0]
        _policies = self.__subjects[policy_id][perimeter_id].get("policies", [])
        for policy in value.get("policies", []):
            if policy not in _policies:
                _policies.append(policy)
        value.pop("policies", None)
        prev_dict = dict(self.__subjects[policy_id][perimeter_id])
        prev_dict.update(value)
        prev_dict["policies"] = _policies
        self.__subjects[policy_id][perimeter_id] = dict(prev_dict)

    def __update_subjects(self, policy_id):
        """
        Update all subjects in a specific policy
        :param policy_id: the policy ID
        :return: None
        """
        response = requests.get("{}/policies/{}/subjects".format(self.manager_url, policy_id),
                                headers=self.headers)
        if 'subjects' in response.json():
            self.__subjects[policy_id] = response.json()['subjects']
        else:
            raise exceptions.SubjectUnknown("Cannot find subject within policy_id {}".format(
                policy_id))

    def get_subject(self, policy_id, name):
        """
        Get one subject knowing its name
        :param policy_id: the policy ID
        :param name: the subject name
        :return: a dictionary
        """
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(
                policy_id))

        if policy_id in self.subjects:
            for _subject_id, _subject_dict in self.subjects[policy_id].items():
                if _subject_id == name or _subject_dict.get("name") == name:
                    return _subject_id

        if self.manager_url:
            self.__update_subjects(policy_id)

            if policy_id in self.subjects:
                for _subject_id, _subject_dict in self.subjects[policy_id].items():
                    if _subject_id == name or _subject_dict.get("name") == name:
                        return _subject_id

        raise exceptions.SubjectUnknown("Cannot find subject {}".format(name))

    @property
    def objects(self):
        """
        Objects
        :return: a dictionary
        """
        return self.__objects

    def add_object(self, value):
        _id = value.get("id", uuid4().hex)
        self.__check_policies(value.get("policy_list", []))
        policy_id = value.get("policy_list", [])[0]
        if policy_id not in self.__objects:
            self.__objects[policy_id] = {_id: dict(value)}
        else:
            self.__objects[policy_id][_id] = dict(value)
        return {_id: dict(value)}

    def delete_object(self, policy_id=None, perimeter_id=None):
        if not policy_id and perimeter_id:
            self.__objects.pop(perimeter_id)
            return
        elif not perimeter_id:
            self.__objects = {}
            return
        self.__check_policies([policy_id])
        self.__objects[perimeter_id].get("policies").remove(policy_id)

    def update_object(self, perimeter_id, value):
        self.__check_policies(value.get("policies", []))
        policy_id = value.get("policy_list", [])[0]
        _policies = self.__objects[policy_id][perimeter_id].get("policies", [])
        for policy in value.get("policies", []):
            if policy not in _policies:
                _policies.append(policy)
        value.pop("policies", None)
        prev_dict = dict(self.__objects[policy_id][perimeter_id])
        prev_dict.update(value)
        prev_dict["policies"] = _policies
        self.__objects[policy_id][perimeter_id] = dict(prev_dict)

    def __update_objects(self, policy_id):
        """
        Update all objects in a specific policy
        :param policy_id: the policy ID
        :return: None
        """
        response = requests.get("{}/policies/{}/objects".format(self.manager_url, policy_id),
                                headers=self.headers)
        if 'objects' in response.json():
            self.__objects[policy_id] = response.json()['objects']
        else:
            raise exceptions.ObjectUnknown("Cannot find object within policy_id {}".format(
                policy_id))

    def get_object(self, policy_id, name):
        """
        Get an object knowing its name
        :param policy_id: the policy ID
        :param name: the object name
        :return: a dictionary
        """
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(
                policy_id))

        if policy_id in self.objects:
            for _object_id, _object_dict in self.__objects[policy_id].items():
                if _object_id == name or _object_dict.get("name") == name:
                    return _object_id

        if self.manager_url:
            self.__update_objects(policy_id)

            if policy_id in self.objects:
                for _object_id, _object_dict in self.__objects[policy_id].items():
                    if _object_id == name or _object_dict.get("name") == name:
                        return _object_id

        raise exceptions.ObjectUnknown("Cannot find object {}".format(name))

    @property
    def actions(self):
        """
        Actions
        :return: a dictionary
        """
        return self.__actions

    def add_action(self, value):
        _id = value.get("id", uuid4().hex)
        self.__check_policies(value.get("policy_list", []))
        policy_id = value.get("policy_list", [])[0]
        if policy_id not in self.__actions:
            self.__actions[policy_id] = {_id: dict(value)}
        else:
            self.__actions[policy_id][_id] = dict(value)
        return {_id: dict(value)}

    def delete_action(self, policy_id=None, perimeter_id=None):
        if not policy_id and perimeter_id:
            self.__actions.pop(perimeter_id)
            return
        elif not perimeter_id:
            self.__actions = {}
            return
        self.__check_policies([policy_id])
        self.__actions[perimeter_id].get("policies").remove(policy_id)

    def update_action(self, perimeter_id, value):
        self.__check_policies(value.get("policies", []))
        policy_id = value.get("policy_list", [])[0]
        _policies = self.__actions[policy_id][perimeter_id].get("policies", [])
        for policy in value.get("policies", []):
            if policy not in _policies:
                _policies.append(policy)
        value.pop("policies", None)
        prev_dict = dict(self.__actions[policy_id][perimeter_id])
        prev_dict.update(value)
        prev_dict["policies"] = _policies
        self.__actions[policy_id][perimeter_id] = dict(prev_dict)

    def __update_actions(self, policy_id):
        """
        Update all actions in a specific policy
        :param policy_id: the policy ID
        :return: None
        """
        response = requests.get("{}/policies/{}/actions".format(self.manager_url, policy_id),
                                headers=self.headers)

        if 'actions' in response.json():
            self.__actions[policy_id] = response.json()['actions']
        else:
            raise exceptions.ActionUnknown("Cannot find action within policy_id {}".format(
                policy_id))

    def get_action(self, policy_id, name):
        """
        Get an action knowing its name
        :param policy_id: the policy ID
        :param name: the action name
        :return: a dictionary
        """
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(
                policy_id))

        if policy_id in self.actions:
            for _action_id, _action_dict in self.__actions[policy_id].items():
                if _action_id == name or _action_dict.get("name") == name:
                    return _action_id

        if self.manager_url:
            self.__update_actions(policy_id)

            for _action_id, _action_dict in self.__actions[policy_id].items():
                if _action_id == name or _action_dict.get("name") == name:
                    return _action_id

        raise exceptions.ActionUnknown("Cannot find action {}".format(name))

    # meta_rule functions

    @property
    def meta_rules(self):
        """
        Meta Rules
        :return: a dictionary
        """
        if self.manager_url:
            current_time = time.time()
            if self.__META_RULES_UPDATE + self.__UPDATE_INTERVAL < current_time:
                self.__META_RULES_UPDATE = current_time
                self.__update_meta_rules()
            self.__META_RULES_UPDATE = current_time
        return self.__meta_rules

    def add_meta_rule(self, value):
        _id = uuid4().hex
        self.__meta_rules[_id] = dict(value)

    def delete_meta_rule(self, meta_rule_id):
        self.__meta_rules.pop(meta_rule_id)

    def __update_meta_rules(self):
        """
        Update all meta rules
        :return: None
        """
        response = requests.get("{}/meta_rules".format(self.manager_url), headers=self.headers)

        if 'meta_rules' in response.json():
            self.__meta_rules = response.json()['meta_rules']
        else:
            raise exceptions.MetaRuleUnknown("Cannot find meta rules")

    # rule functions

    @property
    def rules(self):
        """
        Rules
        :return: a dictionary
        """
        if self.manager_url:
            current_time = time.time()
            if self.__RULES_UPDATE + self.__UPDATE_INTERVAL < current_time:
                self.__RULES_UPDATE = current_time
                self.__update_rules()
            self.__RULES_UPDATE = current_time
        return self.__rules

    def add_rule(self, value):
        value = dict(value)
        _id = value.get("policy_id")
        if "value" in value:
            for key in value["value"]:
                value[key] = value["value"][key]
            value.pop('value')
        if _id in self.__rules:
            self.__rules[_id]['rules'].append(value)
        else:
            self.__rules[_id] = {
                "policy_id": _id,
                "rules": [value]
            }

    def delete_rule(self, policy_id, rule_id=None):
        if not rule_id:
            self.__rules.pop(policy_id)
            return
        for _index, _rule in enumerate(self.__rules.get(policy_id, {}).get("rules")):
            if _rule.get('id') == rule_id:
                index = _index
                break
        else:
            return
        self.__rules.get(policy_id, {}).get("rules").pop(index)

    def __update_rules(self):
        """
        Update all rules
        :return: None
        """
        for policy_id in self.policies:

            response = requests.get("{}/policies/{}/rules".format(
                self.manager_url, policy_id), headers=self.headers)
            if 'rules' in response.json():
                self.__rules[policy_id] = response.json()['rules']
            else:
                logger.warning(" no 'rules' found within policy_id: {}".format(policy_id))

    # assignment functions

    def update_assignments(self, policy_id=None, perimeter_id=None):
        """
        Update all assignments for a specific perimeter (subject, object or action)
        :param policy_id: the policy ID
        :param perimeter_id: the perimeter ID
        :return: None
        """
        if self.manager_url:
            if policy_id:
                self.__update_subject_assignments(policy_id=policy_id, perimeter_id=perimeter_id)
                self.__update_object_assignments(policy_id=policy_id, perimeter_id=perimeter_id)
                self.__update_action_assignments(policy_id=policy_id, perimeter_id=perimeter_id)
            else:
                for policy_id in self.__policies:
                    self.__update_subject_assignments(policy_id=policy_id,
                                                      perimeter_id=perimeter_id)
                    self.__update_object_assignments(policy_id=policy_id,
                                                     perimeter_id=perimeter_id)
                    self.__update_action_assignments(policy_id=policy_id,
                                                     perimeter_id=perimeter_id)

    @property
    def subject_assignments(self):
        """
        Subject Assignments
        :return: a dictionary
        """
        return self.__subject_assignments

    def __update_subject_assignments(self, policy_id, perimeter_id=None):
        """
        Update all assignments for a specific perimeter
        :param policy_id: the policy ID
        :param perimeter_id: the perimeter ID
        :return: None
        """
        if perimeter_id:
            response = requests.get("{}/policies/{}/subject_assignments/{}".format(
                self.manager_url, policy_id, perimeter_id), headers=self.headers)
        else:
            response = requests.get("{}/policies/{}/subject_assignments".format(
                self.manager_url, policy_id), headers=self.headers)

        if 'subject_assignments' in response.json():
            if policy_id not in self.subject_assignments:
                self.__subject_assignments[policy_id] = {}
            self.__subject_assignments[policy_id] = response.json()['subject_assignments']
        else:
            raise exceptions.SubjectAssignmentUnknown(
                "Cannot find subject assignment within policy_id {}".format(policy_id))

    def get_subject_assignments(self, policy_id, perimeter_id, category_id):
        """
        Get all subject assignments for a specific perimeter ID and in a specific category ID
        :param policy_id: the policy ID
        :param perimeter_id: the perimeter ID
        :param category_id: the category ID
        :return: a dictionary
        """
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(
                policy_id))

        if self.manager_url:
            self.__update_subject_assignments(policy_id, perimeter_id)

        for key, value in self.__subject_assignments[policy_id].items():
            if all(k in value for k in ("subject_id", "category_id", "assignments")):
                if perimeter_id == value['subject_id'] and category_id == value['category_id']:
                    return value['assignments']
            else:
                logger.warning("'subject_id' or 'category_id' or 'assignments'"
                               " keys are not found in subject_assignments")
        return []

    def add_subject_assignment(self, policy_id, perimeter_id, category_id, data_id):
        self.__check_policies([policy_id])
        for key, value in self.__subject_assignments.get(policy_id, {}).items():
            if all(k in value for k in ("subject_id", "category_id", "assignments")):
                if perimeter_id == value['subject_id'] and category_id == value['category_id']:
                    if data_id not in value['assignments']:
                        value['assignments'].append(data_id)
                    return value['assignments']
            else:
                logger.warning("'subject_id' or 'category_id' or 'assignments'"
                               " keys are not found in subject_assignments")
        value = {
            "id": uuid4().hex,
            "policy_id": policy_id,
            "subject_id": perimeter_id,
            "category_id": category_id,
            "assignments": [data_id, ],
        }
        if policy_id not in self.__subject_assignments:
            self.__subject_assignments[policy_id] = {}
        self.__subject_assignments[policy_id][value["id"]] = value
        return value

    def delete_subject_assignment(self, policy_id=None, perimeter_id=None,
                                  category_id=None, data_id=None):
        if not policy_id and not perimeter_id and not category_id and not data_id:
            self.__subject_assignments = {}
            return
        self.__check_policies([policy_id])
        for key, value in self.__subject_assignments[policy_id].items():
            if all(k in value for k in ("subject_id", "category_id", "assignments")):
                if perimeter_id == value['subject_id'] and category_id == value['category_id']:
                    try:
                        value['assignments'].remove(data_id)
                    except ValueError:
                        pass
                    return value['assignments']
            else:
                logger.warning("'subject_id' or 'category_id' or 'assignments'"
                               " keys are not found in subject_assignments")
        return []

    @property
    def object_assignments(self):
        """
        Object Assignments
        :return: a dictionary
        """
        return self.__object_assignments

    def __update_object_assignments(self, policy_id, perimeter_id=None):
        """
        Update all assignments for a specific perimeter
        :param policy_id: the policy ID
        :param perimeter_id: the perimeter ID
        :return: None
        """
        if perimeter_id:
            response = requests.get("{}/policies/{}/object_assignments/{}".format(
                self.manager_url, policy_id, perimeter_id), headers=self.headers)
        else:
            response = requests.get("{}/policies/{}/object_assignments".format(
                self.manager_url, policy_id), headers=self.headers)

        if 'object_assignments' in response.json():
            if policy_id not in self.object_assignments:
                self.__object_assignments[policy_id] = {}

            self.__object_assignments[policy_id] = response.json()['object_assignments']
        else:
            raise exceptions.ObjectAssignmentUnknown(
                "Cannot find object assignment within policy_id {}".format(policy_id))

    def get_object_assignments(self, policy_id, perimeter_id, category_id):
        """
        Get all object assignments for a specific perimeter ID and in a specific category ID
        :param policy_id: the policy ID
        :param perimeter_id: the perimeter ID
        :param category_id: the category ID
        :return: a dictionary
        """
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(
                policy_id))

        if self.manager_url:
            self.__update_object_assignments(policy_id, perimeter_id)

        for key, value in self.object_assignments[policy_id].items():
            if all(k in value for k in ("object_id", "category_id", "assignments")):
                if perimeter_id == value['object_id'] and category_id == value['category_id']:
                    return value['assignments']
            else:
                logger.warning("'object_id' or 'category_id' or'assignments'"
                               " keys are not found in object_assignments")
        return []

    def add_object_assignment(self, policy_id, perimeter_id, category_id, data_id):
        self.__check_policies([policy_id])
        for key, value in self.__object_assignments.get(policy_id, {}).items():
            if all(k in value for k in ("object_id", "category_id", "assignments")):
                if perimeter_id == value['object_id'] and category_id == value['category_id']:
                    if data_id not in value['assignments']:
                        value['assignments'].append(data_id)
                    return value['assignments']
            else:
                logger.warning("'object_id' or 'category_id' or 'assignments'"
                               " keys are not found in object_assignments")
        value = {
            "id": uuid4().hex,
            "policy_id": policy_id,
            "object_id": perimeter_id,
            "category_id": category_id,
            "assignments": [data_id, ],
        }
        if policy_id not in self.__object_assignments:
            self.__object_assignments[policy_id] = {}
        self.__object_assignments[policy_id][value["id"]] = value
        return value

    def delete_object_assignment(self, policy_id=None, perimeter_id=None,
                                 category_id=None, data_id=None):
        if not policy_id and not perimeter_id and not category_id and not data_id:
            self.__object_assignments = {}
            return
        self.__check_policies([policy_id])
        for key, value in self.__object_assignments[policy_id].items():
            if all(k in value for k in ("object_id", "category_id", "assignments")):
                if perimeter_id == value['object_id'] and category_id == value['category_id']:
                    try:
                        value['assignments'].remove(data_id)
                    except ValueError:
                        pass
                    return value['assignments']
            else:
                logger.warning("'object_id' or 'category_id' or 'assignments'"
                               " keys are not found in object_assignments")
        return []

    @property
    def action_assignments(self):
        """
        Action Assignments
        :return: a dictionary
        """
        return self.__action_assignments

    def __update_action_assignments(self, policy_id, perimeter_id=None):
        """
        Update all assignments for a specific perimeter
        :param policy_id: the policy ID
        :param perimeter_id: the perimeter ID
        :return: None
        """
        if perimeter_id:
            response = requests.get("{}/policies/{}/action_assignments/{}".format(
                self.manager_url, policy_id, perimeter_id), headers=self.headers)
        else:
            response = requests.get("{}/policies/{}/action_assignments".format(
                self.manager_url, policy_id), headers=self.headers)

        if 'action_assignments' in response.json():
            if policy_id not in self.__action_assignments:
                self.__action_assignments[policy_id] = {}

            self.__action_assignments[policy_id] = response.json()['action_assignments']
        else:
            raise exceptions.ActionAssignmentUnknown(
                "Cannot find action assignment within policy_id {}".format(policy_id))

    def get_action_assignments(self, policy_id, perimeter_id, category_id):
        """
        Get all subject assignments for a specific perimeter ID and in a specific category ID
        :param policy_id: the policy ID
        :param perimeter_id: the perimeter ID
        :param category_id: the category ID
        :return: a dictionary
        """
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(
                policy_id))

        if self.manager_url:
            # FIXME: this should be not done automatically (performance consuming)
            self.__update_action_assignments(policy_id, perimeter_id)

        for key, value in self.action_assignments[policy_id].items():
            if all(k in value for k in ("action_id", "category_id", "assignments")):
                if perimeter_id == value['action_id'] and category_id == value['category_id']:
                    return value['assignments']
            else:
                logger.warning("'action_id' or 'category_id' or'assignments'"
                               " keys are not found in action_assignments")
        return []

    def add_action_assignment(self, policy_id, perimeter_id, category_id, data_id):
        self.__check_policies([policy_id])
        for key, value in self.__action_assignments.get(policy_id, {}).items():
            if all(k in value for k in ("action_id", "category_id", "assignments")):
                if perimeter_id == value['action_id'] and category_id == value['category_id']:
                    if data_id not in value['assignments']:
                        value['assignments'].append(data_id)
                    return value['assignments']
            else:
                logger.warning("'action_id' or 'category_id' or 'assignments'"
                               " keys are not found in action_assignments")
        value = {
            "id": uuid4().hex,
            "policy_id": policy_id,
            "action_id": perimeter_id,
            "category_id": category_id,
            "assignments": [data_id, ],
        }
        if policy_id not in self.__action_assignments:
            self.__action_assignments[policy_id] = {}
        self.__action_assignments[policy_id][value["id"]] = value
        return value

    def delete_action_assignment(self, policy_id=None, perimeter_id=None,
                                 category_id=None, data_id=None):
        if not policy_id and not perimeter_id and not category_id and not data_id:
            self.__action_assignments = {}
            return
        self.__check_policies([policy_id])
        for key, value in self.__action_assignments[policy_id].items():
            if all(k in value for k in ("action_id", "category_id", "assignments")):
                if perimeter_id == value['action_id'] and category_id == value['category_id']:
                    try:
                        value['assignments'].remove(data_id)
                    except ValueError:
                        pass
                    return value['assignments']
            else:
                logger.warning("'action_id' or 'category_id' or 'assignments'"
                               " keys are not found in action_assignments")
        return []

    # category functions

    @property
    def subject_categories(self):
        """
        Subject Categories
        :return: a dictionary
        """
        if self.manager_url:
            current_time = time.time()
            if self.__SUBJECT_CATEGORIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
                self.__SUBJECT_CATEGORIES_UPDATE = current_time
                self.__update_subject_categories()
            self.__SUBJECT_CATEGORIES_UPDATE = current_time
        return self.__subject_categories

    def add_subject_category(self, value):
        _id = uuid4().hex
        self.__subject_categories[_id] = dict(value)

    def delete_subject_category(self, category_id):
        self.__subject_categories.pop(category_id)

    def update_subject_category(self, category_id, value):
        self.__subject_categories[category_id] = dict(value)

    def __update_subject_categories(self):
        """
        Update all subject categories
        :return: None
        """
        response = requests.get("{}/subject_categories".format(self.manager_url),
                                headers=self.headers)

        if 'subject_categories' in response.json():
            self.__subject_categories.update(response.json()['subject_categories'])
        else:
            raise exceptions.SubjectCategoryUnknown("Cannot find subject category")

    @property
    def object_categories(self):
        """
        Object Categories
        :return: a dictionary
        """
        if self.manager_url:
            current_time = time.time()
            if self.__OBJECT_CATEGORIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
                self.__OBJECT_CATEGORIES_UPDATE = current_time
                self.__update_object_categories()
            self.__OBJECT_CATEGORIES_UPDATE = current_time
        return self.__object_categories

    def add_object_category(self, value):
        _id = uuid4().hex
        self.__object_categories[_id] = dict(value)

    def delete_object_category(self, category_id):
        self.__object_categories.pop(category_id)

    def update_object_category(self, category_id, value):
        self.__object_categories[category_id] = dict(value)

    def __update_object_categories(self):
        """
        Update all object categories
        :return: None
        """
        response = requests.get("{}/object_categories".format(self.manager_url),
                                headers=self.headers)

        if 'object_categories' in response.json():
            self.__object_categories.update(response.json()['object_categories'])
        else:
            raise exceptions.ObjectCategoryUnknown("Cannot find object category")

    @property
    def action_categories(self):
        """
        Action Categories
        :return: a dictionary
        """
        if self.manager_url:
            current_time = time.time()
            if self.__ACTION_CATEGORIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
                self.__ACTION_CATEGORIES_UPDATE = current_time
                self.__update_action_categories()
            self.__ACTION_CATEGORIES_UPDATE = current_time
        return self.__action_categories

    def add_action_category(self, value):
        _id = uuid4().hex
        self.__action_categories[_id] = dict(value)

    def delete_action_category(self, category_id):
        self.__action_categories.pop(category_id)

    def update_action_category(self, category_id, value):
        self.__action_categories[category_id] = dict(value)

    def __update_action_categories(self):
        """
        Update all action categories
        :return: None
        """
        response = requests.get("{}/action_categories".format(self.manager_url),
                                headers=self.headers)

        if 'action_categories' in response.json():
            self.__action_categories.update(response.json()['action_categories'])
        else:
            raise exceptions.ActionCategoryUnknown("Cannot find action category")

    # PDP functions

    def __update_pdp(self, uuid=None):
        """
        Update one or all PDP
        :param uuid: the PDP ID to update
        :return: None
        """
        if not uuid:
            response = requests.get("{}/pdp".format(self.manager_url), headers=self.headers)
        else:
            response = requests.get("{}/pdp/{}".format(self.manager_url, uuid),
                                    headers=self.headers)
        try:
            pdp = response.json()
        except Exception as e:
            logger.error("Got an error from the server: {}".format(response.content))
            raise e
        if 'pdps' in pdp:
            self.__pdp = copy.deepcopy(pdp["pdps"])

        else:
            logger.error("Receive bad response from manager: {}".format(pdp))
            raise exceptions.DataContentError("Cannot find 'pdps' key")

    @property
    def pdp(self):
        """Policy Decision Point
        Example of content:
        {
            "pdp_id": {
                "vim_project_id": "vim_project_id",
                "name": "pdp1",
                "description": "test",
                "security_pipeline": [
                    "policy_id"
                ]
            }
        }

        :return: a dictionary
        """
        if self.manager_url:
            current_time = time.time()
            if self.__PDP_UPDATE + self.__UPDATE_INTERVAL < current_time:
                self.__PDP_UPDATE = current_time
                self.__update_pdp()
            self.__PDP_UPDATE = current_time
        return self.__pdp

    def add_pdp(self, pdp_id=None, data=None):
        if not pdp_id:
            pdp_id = uuid4().hex
        self.__pdp[pdp_id] = data

    def delete_pdp(self, pdp_id):
        self.__pdp.pop(pdp_id)

    # policy functions
    def __update_policies(self, pdp_id=None):
        """
        Update all policies
        :param pdp_id: the PDP ID (if not given, update all policies)
        :return: None
        """
        response = requests.get("{}/policies".format(self.manager_url), headers=self.headers)
        policies = response.json()

        if 'policies' in policies:
            for key, value in policies["policies"].items():
                if not pdp_id or (pdp_id and key in self.__pdp.get("security_pipeline", [])):
                    self.__policies[key] = value
        else:
            raise exceptions.PolicyContentError("Cannot find 'policies' key")

    @property
    def policies(self):
        """
        Policies
        :return: a dictionary
        """
        if self.manager_url:
            current_time = time.time()
            if self.__POLICIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
                self.__POLICIES_UPDATE = current_time
                self.__update_policies()
            self.__POLICIES_UPDATE = current_time
        return self.__policies

    def add_policy(self, value):
        _id = value.get("id", uuid4().hex)
        self.__policies[_id] = dict(value)
        return {_id: self.__policies[_id]}

    def delete_policy(self, policy_id):
        self.__policies.pop(policy_id)

    def update_policy(self, policy_id, value):
        self.__policies[policy_id] = dict(value)

    # model functions

    def __update_models(self):
        """
        Update all models
        :return: None
        """
        response = requests.get("{}/models".format(self.manager_url), headers=self.headers)
        models = response.json()
        if 'models' in models:
            for key, value in models["models"].items():
                self.__models[key] = value
        else:
            raise exceptions.DataContentError("Cannot find 'models' key")

    @property
    def models(self):
        """
        Models
        :return: a dictionary
        """
        if self.manager_url:
            current_time = time.time()
            if self.__MODELS_UPDATE + self.__UPDATE_INTERVAL < current_time:
                self.__MODELS_UPDATE = current_time
                self.__update_models()
            self.__MODELS_UPDATE = current_time
        return self.__models

    def add_model(self, value):
        _id = value.get("id", uuid4().hex)
        if "meta_rules" not in value:
            value["meta_rules"] = []
        self.__models[_id] = dict(value)
        return {_id: self.__models[_id]}

    def delete_model(self, model_id):
        self.__models.pop(model_id)

    def update_model(self, model_id, value):
        self.__models[model_id] = dict(value)

    # helper functions

    def get_policy_from_meta_rules(self, meta_rule_id):
        """
        Get the policy ID with the given meta rule ID
        :param meta_rule_id: the meta rule ID
        :return: a policy ID
        """
        for pdp_key, pdp_value in self.pdp.items():
            if "security_pipeline" in pdp_value:
                for policy_id in pdp_value["security_pipeline"]:
                    if policy_id in self.policies and "model_id" in self.policies[policy_id]:
                        model_id = self.policies[policy_id]["model_id"]
                        if model_id in self.models and "meta_rules" in self.models[model_id]:
                            if meta_rule_id in self.models[model_id]["meta_rules"]:
                                return policy_id
                        else:
                            logger.warning(
                                "Cannot find model_id: {} within "
                                "models and 'meta_rules' key".format(model_id))
                    else:
                        logger.warning(
                            "Cannot find policy_id: {} "
                            "within policies and 'model_id' key".format(
                                policy_id))
            else:
                logger.warning("Cannot find 'security_pipeline' "
                               "key within pdp ")

    def get_meta_rule_ids_from_pdp_value(self, pdp_value):
        """
        Get the meta rule ID given the content of a PDP
        :param pdp_value: the content of the PDP
        :return: a meta rule ID
        """
        meta_rules = []
        if "security_pipeline" in pdp_value:
            for policy_id in pdp_value["security_pipeline"]:
                if policy_id not in self.policies or "model_id" not in self.policies[policy_id]:
                    raise exceptions.PolicyUnknown("Cannot find 'models' key")
                model_id = self.policies[policy_id]["model_id"]
                if model_id not in self.models or 'meta_rules' not in self.models[model_id]:
                    raise exceptions.DataContentError("Cannot find 'models' key")
                for meta_rule in self.models[model_id]["meta_rules"]:
                    meta_rules.append(meta_rule)
            return meta_rules
        raise exceptions.PdpContentError

    def get_pdp_from_vim_project(self, vim_project_id):
        """
        Get the PDP ID given the VIM project ID
        :param vim_project_id: the VIM project ID
        :return: the PDP ID
        """
        for pdp_key, pdp_value in self.pdp.items():
            if "vim_project_id" in pdp_value and \
                    vim_project_id == pdp_value["vim_project_id"]:
                return pdp_key

    def get_vim_project_id_from_policy_id(self, policy_id):
        """
        Get the VIM project ID given the policy ID
        :param policy_id: the policy ID
        :return: the VIM project ID
        """
        for pdp_key, pdp_value in self.pdp.items():
            if "security_pipeline" in pdp_value and \
                    "vim_project_id" in pdp_value:
                if policy_id in pdp_value["security_pipeline"]:
                    return pdp_value["vim_project_id"]
            else:
                logger.warning(" 'security_pipeline','vim_project_id' "
                               "key not in pdp {}".format(pdp_value))

    def get_pdp_id_from_policy_id(self, policy_id):
        """
        Get the PDP ID given the policy ID
        :param policy_id: the policy ID
        :return: the PDP ID
        """
        for _pdp_id in self.pdp:
            if policy_id in self.__pdp.get(_pdp_id).get("security_pipeline"):
                return _pdp_id

    def get_vim_project_id_from_pdp_id(self, pdp_id):
        """
        Get the VIM project ID given the PDP ID
        :param pdp_id: the PDP ID
        :return: the VIM project ID
        """
        if pdp_id in self.pdp:
            pdp_value = self.pdp.get(pdp_id)
            if "security_pipeline" in pdp_value and \
                    "vim_project_id" in pdp_value:
                return pdp_value["vim_project_id"]
        logger.warning("Unknown PDP ID".format(pdp_id))

    # pipelines functions

    @property
    def pipelines(self):
        """
        Pipelines
        :return: a dictionary
        """
        return self.__pipelines

    def add_pipeline(self, pipeline_id=None, data=None):
        if not pipeline_id:
            pipeline_id = uuid4().hex
        self.__pipelines[pipeline_id] = data

    def delete_pipeline(self, pipeline_id=None):
        self.__pipelines.pop(pipeline_id)

    def __update_pipelines(self, pdp_id=None):
        """
        Update all pipelines
        :param pdp_id: the PDP ID
        :return: None
        """
        headers = {
            'x-api-key': self.__CURRENT_SERVER_API_KEY
        }
        req = requests.get("{}/pdp".format(self.manager_url), headers=self.headers)
        pdps = req.json().get("pdps", {})
        for _pdp_id in pdps:
            if pdp_id and pdp_id != _pdp_id:
                continue
            for policy_id in pdps[_pdp_id].get("security_pipeline", []):
                _policy = requests.get("{}/policies/{}".format(self.manager_url, policy_id),
                                       headers=self.headers)
                req = requests.get("{}/pipelines".format(self.__CURRENT_SERVER),
                                   headers=headers)
                _pipelines = req.json().get('pipelines', {})
                self.__pipelines[_pdp_id] = {
                    "pdp_id": _pdp_id,
                    "vim_project_id": pdps[_pdp_id].get("vim_project_id", ""),
                    "protocol": _pipelines[_pdp_id].get("protocol", "http"),
                    "host": _pipelines[_pdp_id].get("server_ip", "127.0.0.1"),
                    "port": _pipelines[_pdp_id].get("port", "8000"),
                }

    def get_pipeline_id_from_project_id(self, project_id):
        """
        Retrieve the pipeline ID from the project ID
        :param project_id: the VIM project ID
        :return: a pipeline_id
        """
        for _pdp_id in self.pdp:
            if self.__pdp.get(_pdp_id).get("vim_project_id") == project_id:
                return _pdp_id
                # try:
                #     return self.__pdp.get(_pdp_id).get("security_pipeline")[0]
                # except IndexError:
                #     return

    def get_pipeline_url(self, project_id=None, pipeline_id=None, pdp_id=None):
        """
        Retrieve the URL of the pipeline
        :param project_id: the VIM project ID
        :param pipeline_id: the pipeline ID
        :param pdp_id: the PDP ID
        :return: the URL
        """
        self.__update_pdp()
        if pdp_id:
            return "{proto}://{host}:{port}".format(
                proto=self.__pipelines[pdp_id].get("protocol", "http"),
                host=self.__pipelines[pdp_id].get("host", "127.0.0.1"),
                port=self.__pipelines[pdp_id].get("port", "8000"),
            )
        if project_id:
            for _pdp_id in self.__pdp:
                if self.__pdp.get(_pdp_id).get("vim_project_id") == project_id:
                    return "{proto}://{host}:{port}".format(
                        proto=self.__pipelines[_pdp_id].get("protocol", "http"),
                        host=self.__pipelines[_pdp_id].get("host", "127.0.0.1"),
                        port=self.__pipelines[_pdp_id].get("port", "8000"),
                    )
        if pipeline_id and pipeline_id in self.pipelines:
            return "{proto}://{host}:{port}".format(
                proto=self.__pipelines[pipeline_id].get("protocol", "http"),
                host=self.__pipelines[pipeline_id].get("host", "127.0.0.1"),
                port=self.__pipelines[pipeline_id].get("port", "8000"),
            )

    def get_api_key(self, project_id=None, pipeline_id=None, pdp_id=None):
        """
        Retrieve the API ky of the pipeline
        :param project_id: the VIM project ID
        :param pipeline_id: the pipeline ID
        :param pdp_id: the PDP ID
        :return: the URL
        """
        self.__update_pdp()
        if pdp_id:
            return self.__pipelines[pdp_id].get("api_key", "")
        if project_id:
            for _pdp_id in self.__pdp:
                if self.__pdp.get(_pdp_id).get("vim_project_id") == project_id:
                    return self.__pipelines[_pdp_id].get("api_key", "")
        if pipeline_id and pipeline_id in self.pipelines:
            return self.__pipelines[pipeline_id].get("api_key", "")

    # security_functions functions

    @property
    def security_functions(self):
        """
        Security Functions
        :return: a dictionary
        """
        if self.manager_url:
            current_time = time.time()
            if self.__SECURITY_FUNCTIONS_UPDATE + self.__UPDATE_INTERVAL < current_time:
                self.__SECURITY_FUNCTIONS_UPDATE = current_time
                self.__update_security_functions()
            self.__SECURITY_FUNCTIONS_UPDATE = current_time
        return self.__security_functions

    def __update_security_functions(self):
        """
        Update security functions
        :return: None
        """
        req = requests.get("{}/policies".format(self.manager_url), headers=self.headers)
        for key in req.json():
            self.__security_functions[key] = req.json()[key]

    @property
    def subject_data(self):
        """Subject Data
        :return: a dictionary"""
        return self.__subject_data

    def add_subject_data(self, policy_id, category_id, data):
        for index, value in enumerate(self.__subject_data):
            if policy_id == value["policy_id"] and category_id == value["category_id"]:
                self.__subject_data[index]["data"][data.get('id', uuid4().hex)] = data
                return self.__subject_data[index]
        else:
            _id = data.get('id', uuid4().hex)
            data['id'] = _id
            value = {
                "policy_id": policy_id,
                "category_id": category_id,
                "data": {
                    _id: data
                }
            }
            self.__subject_data.append(value)
            return value

    def delete_subject_data(self, policy_id=None, category_id=None, data_id=None):
        if not policy_id and not category_id and not data_id:
            self.__subject_data = []
        for index, value in enumerate(self.__subject_data):
            if policy_id == value["policy_id"] and category_id == value["category_id"]:
                self.__subject_data[index]["data"].pop(data_id)

    @property
    def object_data(self):
        """Object Data
        :return: a dictionary"""
        return self.__object_data

    def add_object_data(self, policy_id, category_id, data):
        for index, value in enumerate(self.__object_data):
            if policy_id == value["policy_id"] and category_id == value["category_id"]:
                self.__object_data[index]["data"][data.get('id', uuid4().hex)] = data
                return self.__object_data[index]
        else:
            _id = data.get('id', uuid4().hex)
            data['id'] = _id
            value = {
                "policy_id": policy_id,
                "category_id": category_id,
                "data": {
                    _id: data
                }
            }
            self.__object_data.append(value)
            return value

    def delete_object_data(self, policy_id=None, category_id=None, data_id=None):
        if not policy_id and not category_id and not data_id:
            self.__object_data = []
        for index, value in enumerate(self.__object_data):
            if policy_id == value["policy_id"] and category_id == value["category_id"]:
                self.__object_data[index]["data"].pop(data_id)

    @property
    def action_data(self):
        """Action Data
        :return: a dictionary"""
        return self.__action_data

    def add_action_data(self, policy_id, category_id, data):
        for index, value in enumerate(self.__action_data):
            if policy_id == value["policy_id"] and category_id == value["category_id"]:
                self.__action_data[index]["data"][data.get('id', uuid4().hex)] = data
                return self.__action_data[index]
        else:
            _id = data.get('id', uuid4().hex)
            data['id'] = _id
            value = {
                "policy_id": policy_id,
                "category_id": category_id,
                "data": {
                    _id: data
                }
            }
            self.__action_data.append(value)
            return value

    def delete_action_data(self, policy_id=None, category_id=None, data_id=None):
        if not policy_id and not category_id and not data_id:
            self.__action_data = []
        for index, value in enumerate(self.__action_data):
            if policy_id == value["policy_id"] and category_id == value["category_id"]:
                self.__action_data[index]["data"].pop(data_id)


