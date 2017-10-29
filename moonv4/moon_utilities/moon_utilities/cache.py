import logging
import time
import requests
from uuid import uuid4
from moon_utilities import configuration, exceptions

LOG = logging.getLogger("moon.utilities.cache")


class Cache(object):
    # TODO (asteroide): set cache integer in CONF file
    __UPDATE_INTERVAL = 10

    __CONTAINERS = {}
    __CONTAINERS_UPDATE = 0

    __CONTAINER_CHAINING_UPDATE = 0
    __CONTAINER_CHAINING = {}

    __PDP = {}
    __PDP_UPDATE = 0

    __POLICIES = {}
    __POLICIES_UPDATE = 0

    __MODELS = {}
    __MODELS_UPDATE = 0

    __SUBJECTS = {}
    __OBJECTS = {}
    __ACTIONS = {}

    __SUBJECT_ASSIGNMENTS = {}
    __OBJECT_ASSIGNMENTS = {}
    __ACTION_ASSIGNMENTS = {}

    __SUBJECT_CATEGORIES = {}
    __SUBJECT_CATEGORIES_UPDATE = 0
    __OBJECT_CATEGORIES = {}
    __OBJECT_CATEGORIES_UPDATE = 0
    __ACTION_CATEGORIES = {}
    __ACTION_CATEGORIES_UPDATE = 0

    __META_RULES = {}
    __META_RULES_UPDATE = 0

    __RULES = {}
    __RULES_UPDATE = 0

    __AUTHZ_REQUESTS = {}

    def __init__(self):
        self.manager_url = "{}://{}:{}".format(
            configuration.get_components()['manager'].get('protocol', 'http'),
            configuration.get_components()['manager']['hostname'],
            configuration.get_components()['manager']['port']
        )
        self.orchestrator_url = "{}://{}:{}".format(
            configuration.get_components()['orchestrator'].get('protocol', 'http'),
            configuration.get_components()['orchestrator']['hostname'],
            configuration.get_components()['orchestrator']['port']
        )

    def update(self):
        self.__update_container()
        self.__update_pdp()
        self.__update_policies()
        self.__update_models()
        for key, value in self.__PDP.items():
            # LOG.info("Updating container_chaining with {}".format(value["keystone_project_id"]))
            self.__update_container_chaining(value["keystone_project_id"])

    @property
    def authz_requests(self):
        return self.__AUTHZ_REQUESTS

    # perimeter functions

    @property
    def subjects(self):
        return self.__SUBJECTS

    def update_subjects(self, policy_id=None):
        req = requests.get("{}/policies/{}/subjects".format(
            self.manager_url, policy_id))
        self.__SUBJECTS[policy_id] = req.json()['subjects']

    def get_subject(self, policy_id, name):
        try:
            for _subject_id, _subject_dict in self.__SUBJECTS[policy_id].items():
                if _subject_dict["name"] == name:
                    return _subject_id
        except KeyError:
            pass
        self.update_subjects(policy_id)
        for _subject_id, _subject_dict in self.__SUBJECTS[policy_id].items():
            if _subject_dict["name"] == name:
                return _subject_id
        raise exceptions.SubjectUnknown("Cannot find subject {}".format(name))

    @property
    def objects(self):
        return self.__OBJECTS

    def update_objects(self, policy_id=None):
        req = requests.get("{}/policies/{}/objects".format(
            self.manager_url, policy_id))
        self.__OBJECTS[policy_id] = req.json()['objects']

    def get_object(self, policy_id, name):
        try:
            for _object_id, _object_dict in self.__OBJECTS[policy_id].items():
                if _object_dict["name"] == name:
                    return _object_id
        except KeyError:
            pass
        self.update_objects(policy_id)
        for _object_id, _object_dict in self.__OBJECTS[policy_id].items():
            if _object_dict["name"] == name:
                return _object_id
        raise exceptions.SubjectUnknown("Cannot find object {}".format(name))

    @property
    def actions(self):
        return self.__ACTIONS

    def update_actions(self, policy_id=None):
        req = requests.get("{}/policies/{}/actions".format(
            self.manager_url, policy_id))
        self.__ACTIONS[policy_id] = req.json()['actions']

    def get_action(self, policy_id, name):
        try:
            for _action_id, _action_dict in self.__ACTIONS[policy_id].items():
                if _action_dict["name"] == name:
                    return _action_id
        except KeyError:
            pass
        self.update_actions(policy_id)
        for _action_id, _action_dict in self.__ACTIONS[policy_id].items():
            if _action_dict["name"] == name:
                return _action_id
        raise exceptions.SubjectUnknown("Cannot find action {}".format(name))

    # meta_rule functions

    @property
    def meta_rules(self):
        current_time = time.time()
        if self.__META_RULES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_meta_rules()
        self.__META_RULES_UPDATE = current_time
        return self.__META_RULES

    def __update_meta_rules(self):
        req = requests.get("{}/meta_rules".format(self.manager_url))
        self.__META_RULES = req.json()['meta_rules']

    # rule functions

    @property
    def rules(self):
        current_time = time.time()
        if self.__RULES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_rules()
        self.__RULES_UPDATE = current_time
        return self.__RULES

    def __update_rules(self):
        for policy_id in self.__POLICIES:
            LOG.info("Get {}".format("{}/policies/{}/rules".format(
                self.manager_url, policy_id)))
            req = requests.get("{}/policies/{}/rules".format(
                self.manager_url, policy_id))
            self.__RULES[policy_id] = req.json()['rules']
        LOG.info("UPDATE RULES {}".format(self.__RULES))

    # assignment functions

    @property
    def subject_assignments(self):
        return self.__SUBJECT_ASSIGNMENTS

    def update_subject_assignments(self, policy_id=None, perimeter_id=None):
        if perimeter_id:
            req = requests.get("{}/policies/{}/subject_assignments/{}".format(
                self.manager_url, policy_id, perimeter_id))
        else:
            req = requests.get("{}/policies/{}/subject_assignments".format(
                self.manager_url, policy_id))
        if policy_id not in self.__SUBJECT_ASSIGNMENTS:
            self.__SUBJECT_ASSIGNMENTS[policy_id] = {}
        self.__SUBJECT_ASSIGNMENTS[policy_id].update(
            req.json()['subject_assignments'])

    def get_subject_assignments(self, policy_id, perimeter_id, category_id):
        if policy_id not in self.subject_assignments:
            self.update_subject_assignments(policy_id, perimeter_id)
        if policy_id not in self.subject_assignments:
            raise Exception("Cannot found the policy {}".format(policy_id))
        for key, value in self.subject_assignments[policy_id].items():
            if perimeter_id == value['subject_id'] and category_id == value['category_id']:
                return value['assignments']
        return []

    @property
    def object_assignments(self):
        return self.__OBJECT_ASSIGNMENTS

    def update_object_assignments(self, policy_id=None, perimeter_id=None):
        if perimeter_id:
            req = requests.get("{}/policies/{}/object_assignments/{}".format(
                self.manager_url, policy_id, perimeter_id))
        else:
            req = requests.get("{}/policies/{}/object_assignments".format(
                self.manager_url, policy_id))
        if policy_id not in self.__OBJECT_ASSIGNMENTS:
            self.__OBJECT_ASSIGNMENTS[policy_id] = {}
        self.__OBJECT_ASSIGNMENTS[policy_id].update(
            req.json()['object_assignments'])

    def get_object_assignments(self, policy_id, perimeter_id, category_id):
        if policy_id not in self.object_assignments:
            self.update_object_assignments(policy_id, perimeter_id)
        if policy_id not in self.object_assignments:
            raise Exception("Cannot found the policy {}".format(policy_id))
        for key, value in self.object_assignments[policy_id].items():
            if perimeter_id == value['object_id'] and category_id == value['category_id']:
                return value['assignments']
        return []

    @property
    def action_assignments(self):
        return self.__ACTION_ASSIGNMENTS

    def update_action_assignments(self, policy_id=None, perimeter_id=None):
        if perimeter_id:
            req = requests.get("{}/policies/{}/action_assignments/{}".format(
                self.manager_url, policy_id, perimeter_id))
        else:
            req = requests.get("{}/policies/{}/action_assignments".format(
                self.manager_url, policy_id))
        if policy_id not in self.__ACTION_ASSIGNMENTS:
            self.__ACTION_ASSIGNMENTS[policy_id] = {}
        self.__ACTION_ASSIGNMENTS[policy_id].update(
            req.json()['action_assignments'])

    def get_action_assignments(self, policy_id, perimeter_id, category_id):
        if policy_id not in self.action_assignments:
            self.update_action_assignments(policy_id, perimeter_id)
        if policy_id not in self.action_assignments:
            raise Exception("Cannot found the policy {}".format(policy_id))
        for key, value in self.action_assignments[policy_id].items():
            if perimeter_id == value['action_id'] and category_id == value['category_id']:
                return value['assignments']
        return []

    # category functions

    @property
    def subject_categories(self):
        current_time = time.time()
        if self.__SUBJECT_CATEGORIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_subject_categories()
        self.__SUBJECT_CATEGORIES_UPDATE = current_time
        return self.__SUBJECT_CATEGORIES

    def __update_subject_categories(self):
        req = requests.get("{}/policies/subject_categories".format(
            self.manager_url))
        self.__SUBJECT_CATEGORIES.update(req.json()['subject_categories'])

    @property
    def object_categories(self):
        current_time = time.time()
        if self.__OBJECT_CATEGORIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_object_categories()
        self.__OBJECT_CATEGORIES_UPDATE = current_time
        return self.__OBJECT_CATEGORIES

    def __update_object_categories(self):
        req = requests.get("{}/policies/object_categories".format(
            self.manager_url))
        self.__OBJECT_CATEGORIES.update(req.json()['object_categories'])

    @property
    def action_categories(self):
        current_time = time.time()
        if self.__ACTION_CATEGORIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_action_categories()
        self.__ACTION_CATEGORIES_UPDATE = current_time
        return self.__ACTION_CATEGORIES

    def __update_action_categories(self):
        req = requests.get("{}/policies/action_categories".format(
            self.manager_url))
        self.__ACTION_CATEGORIES.update(req.json()['action_categories'])

    # PDP functions

    def __update_pdp(self):
        req = requests.get("{}/pdp".format(self.manager_url))
        pdp = req.json()
        for _pdp in pdp["pdps"].values():
            if _pdp['keystone_project_id'] not in self.__CONTAINER_CHAINING:
                self.__CONTAINER_CHAINING[_pdp['keystone_project_id']] = {}
                # Note (asteroide): force update of chaining
                self.__update_container_chaining(_pdp['keystone_project_id'])
        for key, value in pdp["pdps"].items():
            self.__PDP[key] = value

    @property
    def pdp(self):
        """Policy Decision Point
        Example of content:
        {
            "pdp_id": {
                "keystone_project_id": "keystone_project_id",
                "name": "pdp1",
                "description": "test",
                "security_pipeline": [
                    "policy_id"
                ]
            }
        }

        :return:
        """
        current_time = time.time()
        if self.__PDP_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_pdp()
        self.__PDP_UPDATE = current_time
        return self.__PDP

    # policy functions
    def __update_policies(self):
        req = requests.get("{}/policies".format(self.manager_url))
        policies = req.json()
        for key, value in policies["policies"].items():
            self.__POLICIES[key] = value

    @property
    def policies(self):
        current_time = time.time()
        if self.__POLICIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_policies()
        self.__POLICIES_UPDATE = current_time
        return self.__POLICIES

    # model functions

    def __update_models(self):
        req = requests.get("{}/models".format(self.manager_url))
        models = req.json()
        for key, value in models["models"].items():
            self.__MODELS[key] = value

    @property
    def models(self):
        current_time = time.time()
        if self.__MODELS_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_models()
        self.__MODELS_UPDATE = current_time
        return self.__MODELS

    # helper functions

    def get_policy_from_meta_rules(self, meta_rule_id):
        for pdp_key, pdp_value in self.pdp.items():
            for policy_id in pdp_value["security_pipeline"]:
                model_id = self.policies[policy_id]["model_id"]
                if meta_rule_id in self.models[model_id]["meta_rules"]:
                    return policy_id

    def get_pdp_from_keystone_project(self, keystone_project_id):
        for pdp_key, pdp_value in self.pdp.items():
            if keystone_project_id == pdp_value["keystone_project_id"]:
                return pdp_key

    def get_keystone_project_id_from_policy_id(self, policy_id):
        for pdp_key, pdp_value in self.pdp.items():
            if policy_id in pdp_value["security_pipeline"]:
                return pdp_value["keystone_project_id"]
            # for policy_id in pdp_value["security_pipeline"]:
            #     model_id = self.policies[policy_id]["model_id"]
            #     if meta_rule_id in self.models[model_id]["meta_rules"]:
            #         return pdp_value["keystone_project_id"]

    def get_containers_from_keystone_project_id(self, keystone_project_id,
                                                meta_rule_id=None):
        for container_id, container_value in self.containers.items():
            LOG.info("container={}".format(container_value))
            if 'keystone_project_id' not in container_value:
                continue
            if container_value['keystone_project_id'] == keystone_project_id:
                if not meta_rule_id:
                    yield container_id, container_value
                elif container_value.get('meta_rule_id') == meta_rule_id:
                    yield container_id, container_value
                    break

    # containers functions

    def __update_container(self):
        LOG.info("orchestrator={}".format("{}/pods".format(self.orchestrator_url)))
        req = requests.get("{}/pods".format(self.orchestrator_url))
        LOG.info("pods={}".format(req.text))
        pods = req.json()
        for key, value in pods["pods"].items():
            if key not in self.__CONTAINERS:
                self.__CONTAINERS[key] = value
            else:
                self.__CONTAINERS[key].update(value)

    def add_container(self, container_data):
        """Add a new container in the cache

        :param container_data: dictionary with information for the container
        Example:
        {
            "name": name,
            "hostname": name,
            "port": {
                "PrivatePort": tcp_port,
                "Type": "tcp",
                "IP": "0.0.0.0",
                "PublicPort": tcp_port
            },
            "keystone_project_id": uuid,
            "pdp_id": self.CACHE.get_pdp_from_keystone_project(uuid),
            "meta_rule_id": meta_rule_id,
            "container_name": container_name,
            "plugin_name": plugin_name
            "container_id": "container_id"
        }

        :return:
        """
        self.__CONTAINERS[uuid4().hex] = {
            "keystone_project_id": container_data['keystone_project_id'],
            "name": container_data['name'],
            "container_id": container_data['container_id'],
            "hostname": container_data['name'],
            "policy_id": container_data['policy_id'],
            "meta_rule_id": container_data['meta_rule_id'],
            "port": [
                {
                    "PublicPort": container_data['port']["PublicPort"],
                    "Type": container_data['port']["Type"],
                    "IP": container_data['port']["IP"],
                    "PrivatePort": container_data['port']["PrivatePort"]
                }
            ],
            "genre": container_data['plugin_name']
        }
        self.__update_container_chaining(self.get_keystone_project_id_from_policy_id(container_data['policy_id']))

    @property
    def containers(self):
        """Containers cache
        example of content :
        {
            "policy_uuid1": "component_hostname1",
            "policy_uuid2": "component_hostname2",
        }
        :return:
        """
        current_time = time.time()
        if self.__CONTAINERS_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__update_container()
        self.__CONTAINERS_UPDATE = current_time
        return self.__CONTAINERS

    @property
    def container_chaining(self):
        """Cache for mapping Keystone Project ID with meta_rule ID and container ID
        Example of content:
        {
            "keystone_project_id": [
                {
                    "container_id": "container_id",
                    "genre": "genre",
                    "policy_id": "policy_id",
                    "meta_rule_id": "meta_rule_id",
                }
            ]
        }

        :return:
        """
        current_time = time.time()
        if self.__CONTAINER_CHAINING_UPDATE + self.__UPDATE_INTERVAL < current_time:
            for key, value in self.pdp.items():
                self.__update_container_chaining(value["keystone_project_id"])
        self.__CONTAINER_CHAINING_UPDATE = current_time
        LOG.info(self.__CONTAINER_CHAINING_UPDATE)
        return self.__CONTAINER_CHAINING

    def __update_container_chaining(self, keystone_project_id):
        container_ids = []
        for pdp_id, pdp_value, in self.__PDP.items():
            if pdp_value:
                if pdp_value["keystone_project_id"] == keystone_project_id:
                    for policy_id in pdp_value["security_pipeline"]:
                        model_id = self.__POLICIES[policy_id]['model_id']
                        for meta_rule_id in self.__MODELS[model_id]["meta_rules"]:
                            for container_id, container_value in self.get_containers_from_keystone_project_id(
                                keystone_project_id,
                                meta_rule_id
                            ):
                                container_ids.append(
                                    {
                                        "container_id": self.__CONTAINERS[container_id]["name"],
                                        "genre": self.__CONTAINERS[container_id]["genre"],
                                        "policy_id": policy_id,
                                        "meta_rule_id": meta_rule_id,
                                        "hostname": self.__CONTAINERS[container_id]["name"],
                                        "port": self.__CONTAINERS[container_id]["port"],
                                    }
                                )
        self.__CONTAINER_CHAINING[keystone_project_id] = container_ids

