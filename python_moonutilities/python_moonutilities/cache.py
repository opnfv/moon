import logging
import time
import python_moonutilities.request_wrapper as requests
from uuid import uuid4
from python_moonutilities import configuration, exceptions

logger = logging.getLogger("moon.utilities.cache")


class Cache(object):
    # TODO (asteroide): set cache integer in CONF file
    '''
        [NOTE] Propose to define the following variables inside the init method
        as defining them out side the init, will be treated as private static variables
        and keep tracks with any changes done anywhere
        for more info : you can check https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables
    '''
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
            if "keystone_project_id" in value:
                self.__update_container_chaining(value["keystone_project_id"])
            else:
                logger.warning("no 'keystone_project_id' found while Updating container_chaining")

    @property
    def authz_requests(self):
        return self.__AUTHZ_REQUESTS

    # perimeter functions

    @property
    def subjects(self):
        return self.__SUBJECTS

    def __update_subjects(self, policy_id):
        response = requests.get("{}/policies/{}/subjects".format(self.manager_url, policy_id))
        if 'subjects' in response.json():
            self.__SUBJECTS[policy_id] = response.json()['subjects']
        else:
            raise exceptions.SubjectUnknown("Cannot find subject within policy_id {}".format(policy_id))

    def get_subject(self, policy_id, name):
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(policy_id))

        if policy_id in self.subjects:
            for _subject_id, _subject_dict in self.subjects[policy_id].items():
                if "name" in _subject_dict and _subject_dict["name"] == name:
                    return _subject_id

        self.__update_subjects(policy_id)

        if policy_id in self.subjects:
            for _subject_id, _subject_dict in self.subjects[policy_id].items():
                if "name" in _subject_dict and _subject_dict["name"] == name:
                    return _subject_id

        raise exceptions.SubjectUnknown("Cannot find subject {}".format(name))

    @property
    def objects(self):
        return self.__OBJECTS

    def __update_objects(self, policy_id):
        response = requests.get("{}/policies/{}/objects".format(self.manager_url, policy_id))
        if 'objects' in response.json():
            self.__OBJECTS[policy_id] = response.json()['objects']
        else:
            raise exceptions.ObjectUnknown("Cannot find object within policy_id {}".format(policy_id))

    def get_object(self, policy_id, name):
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(policy_id))

        if policy_id in self.objects:
            for _object_id, _object_dict in self.__OBJECTS[policy_id].items():
                if "name" in _object_dict and _object_dict["name"] == name:
                    return _object_id

        self.__update_objects(policy_id)

        if policy_id in self.objects:
            for _object_id, _object_dict in self.__OBJECTS[policy_id].items():
                if "name" in _object_dict and _object_dict["name"] == name:
                    return _object_id

        raise exceptions.ObjectUnknown("Cannot find object {}".format(name))

    @property
    def actions(self):
        return self.__ACTIONS

    def __update_actions(self, policy_id):
        response = requests.get("{}/policies/{}/actions".format(self.manager_url, policy_id))

        if 'actions' in response.json():
            self.__ACTIONS[policy_id] = response.json()['actions']
        else:
            raise exceptions.ActionUnknown("Cannot find action within policy_id {}".format(policy_id))

    def get_action(self, policy_id, name):
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(policy_id))

        if policy_id in self.actions:
            for _action_id, _action_dict in self.__ACTIONS[policy_id].items():
                if "name" in _action_dict and _action_dict["name"] == name:
                    return _action_id

        self.__update_actions(policy_id)

        for _action_id, _action_dict in self.__ACTIONS[policy_id].items():
            if "name" in _action_dict and _action_dict["name"] == name:
                return _action_id

        raise exceptions.ActionUnknown("Cannot find action {}".format(name))

    # meta_rule functions

    @property
    def meta_rules(self):
        current_time = time.time()
        if self.__META_RULES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__META_RULES_UPDATE = current_time
            self.__update_meta_rules()
        self.__META_RULES_UPDATE = current_time
        return self.__META_RULES

    def __update_meta_rules(self):
        response = requests.get("{}/meta_rules".format(self.manager_url))

        if 'meta_rules' in response.json():
            self.__META_RULES = response.json()['meta_rules']
        else:
            raise exceptions.MetaRuleUnknown("Cannot find meta rules")

    # rule functions

    @property
    def rules(self):
        current_time = time.time()
        if self.__RULES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__RULES_UPDATE = current_time
            self.__update_rules()
        self.__RULES_UPDATE = current_time
        return self.__RULES

    def __update_rules(self):
        for policy_id in self.policies:
            logger.debug("Get {}".format("{}/policies/{}/rules".format(
                self.manager_url, policy_id)))

            response = requests.get("{}/policies/{}/rules".format(
                self.manager_url, policy_id))
            if 'rules' in response.json():
                self.__RULES[policy_id] = response.json()['rules']
            else:
                logger.warning(" no 'rules' found within policy_id: {}".format(policy_id))

        logger.debug("UPDATE RULES {}".format(self.__RULES))

    # assignment functions

    @property
    def subject_assignments(self):
        return self.__SUBJECT_ASSIGNMENTS

    def __update_subject_assignments(self, policy_id, perimeter_id=None):
        if perimeter_id:
            response = requests.get("{}/policies/{}/subject_assignments/{}".format(
                self.manager_url, policy_id, perimeter_id))
        else:
            response = requests.get("{}/policies/{}/subject_assignments".format(
                self.manager_url, policy_id))

        if 'subject_assignments' in response.json():
            if policy_id not in self.subject_assignments:
                self.__SUBJECT_ASSIGNMENTS[policy_id] = {}

            self.__SUBJECT_ASSIGNMENTS[policy_id].update(response.json()['subject_assignments'])
        else:
            raise exceptions.SubjectAssignmentUnknown(
                "Cannot find subject assignment within policy_id {}".format(policy_id))

    def get_subject_assignments(self, policy_id, perimeter_id, category_id):
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(policy_id))

        if policy_id not in self.subject_assignments:
            self.__update_subject_assignments(policy_id, perimeter_id)

        for key, value in self.subject_assignments[policy_id].items():
            if all(k in value for k in ("subject_id", "category_id", "assignments")):
                if perimeter_id == value['subject_id'] and category_id == value['category_id']:
                    return value['assignments']
            else:
                logger.warning("'subject_id' or 'category_id' or'assignments'"
                               " keys are not found in subject_assignments")
        return []

    @property
    def object_assignments(self):
        return self.__OBJECT_ASSIGNMENTS

    def __update_object_assignments(self, policy_id, perimeter_id=None):
        if perimeter_id:
            response = requests.get("{}/policies/{}/object_assignments/{}".format(
                self.manager_url, policy_id, perimeter_id))
        else:
            response = requests.get("{}/policies/{}/object_assignments".format(
                self.manager_url, policy_id))

        if 'object_assignments' in response.json():
            if policy_id not in self.object_assignments:
                self.__OBJECT_ASSIGNMENTS[policy_id] = {}

            self.__OBJECT_ASSIGNMENTS[policy_id].update(response.json()['object_assignments'])
        else:
            raise exceptions.ObjectAssignmentUnknown(
                "Cannot find object assignment within policy_id {}".format(policy_id))

    def get_object_assignments(self, policy_id, perimeter_id, category_id):
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(policy_id))

        if policy_id not in self.object_assignments:
            self.__update_object_assignments(policy_id, perimeter_id)

        for key, value in self.object_assignments[policy_id].items():
            if all(k in value for k in ("object_id", "category_id", "assignments")):
                if perimeter_id == value['object_id'] and category_id == value['category_id']:
                    return value['assignments']
            else:
                logger.warning("'object_id' or 'category_id' or'assignments'"
                               " keys are not found in object_assignments")
        return []

    @property
    def action_assignments(self):
        return self.__ACTION_ASSIGNMENTS

    def __update_action_assignments(self, policy_id, perimeter_id=None):
        if perimeter_id:
            response = requests.get("{}/policies/{}/action_assignments/{}".format(
                self.manager_url, policy_id, perimeter_id))
        else:
            response = requests.get("{}/policies/{}/action_assignments".format(
                self.manager_url, policy_id))

        if 'action_assignments' in response.json():
            if policy_id not in self.__ACTION_ASSIGNMENTS:
                self.__ACTION_ASSIGNMENTS[policy_id] = {}

            self.__ACTION_ASSIGNMENTS[policy_id].update(response.json()['action_assignments'])
        else:
            raise exceptions.ActionAssignmentUnknown(
                "Cannot find action assignment within policy_id {}".format(policy_id))

    def get_action_assignments(self, policy_id, perimeter_id, category_id):
        if not policy_id:
            raise exceptions.PolicyUnknown("Cannot find policy within policy_id {}".format(policy_id))

        if policy_id not in self.action_assignments:
            self.__update_action_assignments(policy_id, perimeter_id)

        for key, value in self.action_assignments[policy_id].items():
            if all(k in value for k in ("action_id", "category_id", "assignments")):
                if perimeter_id == value['action_id'] and category_id == value['category_id']:
                    return value['assignments']
            else:
                logger.warning("'action_id' or 'category_id' or'assignments'"
                               " keys are not found in action_assignments")
        return []

    # category functions

    @property
    def subject_categories(self):
        current_time = time.time()
        if self.__SUBJECT_CATEGORIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__SUBJECT_CATEGORIES_UPDATE = current_time
            self.__update_subject_categories()
        self.__SUBJECT_CATEGORIES_UPDATE = current_time
        return self.__SUBJECT_CATEGORIES

    def __update_subject_categories(self):
        response = requests.get("{}/policies/subject_categories".format(
            self.manager_url))

        if 'subject_categories' in response.json():
            self.__SUBJECT_CATEGORIES.update(response.json()['subject_categories'])
        else:
            raise exceptions.SubjectCategoryUnknown("Cannot find subject category")

    @property
    def object_categories(self):
        current_time = time.time()
        if self.__OBJECT_CATEGORIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__OBJECT_CATEGORIES_UPDATE = current_time
            self.__update_object_categories()
        self.__OBJECT_CATEGORIES_UPDATE = current_time
        return self.__OBJECT_CATEGORIES

    def __update_object_categories(self):
        response = requests.get("{}/policies/object_categories".format(self.manager_url))

        if 'object_categories' in response.json():
            self.__OBJECT_CATEGORIES.update(response.json()['object_categories'])
        else:
            raise exceptions.ObjectCategoryUnknown("Cannot find object category")

    @property
    def action_categories(self):
        current_time = time.time()
        if self.__ACTION_CATEGORIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__ACTION_CATEGORIES_UPDATE = current_time
            self.__update_action_categories()
        self.__ACTION_CATEGORIES_UPDATE = current_time
        return self.__ACTION_CATEGORIES

    def __update_action_categories(self):
        response = requests.get("{}/policies/action_categories".format(self.manager_url))

        if 'action_categories' in response.json():
            self.__ACTION_CATEGORIES.update(response.json()['action_categories'])
        else:
            raise exceptions.ActionCategoryUnknown("Cannot find action category")

    # PDP functions

    def __update_pdp(self):
        response = requests.get("{}/pdp".format(self.manager_url))
        pdp = response.json()
        if 'pdps' in pdp:
            for _pdp in pdp["pdps"].values():
                if "keystone_project_id" in _pdp and _pdp['keystone_project_id'] not in self.container_chaining:
                    self.__CONTAINER_CHAINING[_pdp['keystone_project_id']] = {}
                    # Note (asteroide): force update of chaining
                    self.__update_container_chaining(_pdp['keystone_project_id'])
            for key, value in pdp["pdps"].items():
                self.__PDP[key] = value

        else:
            raise exceptions.PdpError("Cannot find 'pdps' key")

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
            self.__PDP_UPDATE = current_time
            self.__update_pdp()
        self.__PDP_UPDATE = current_time
        return self.__PDP

    # policy functions
    def __update_policies(self):
        response = requests.get("{}/policies".format(self.manager_url))
        policies = response.json()

        if 'policies' in policies:
            for key, value in policies["policies"].items():
                self.__POLICIES[key] = value
        else:
            raise exceptions.PolicytNotFound("Cannot find 'policies' key")

    @property
    def policies(self):
        current_time = time.time()
        if self.__POLICIES_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__POLICIES_UPDATE = current_time
            self.__update_policies()
        self.__POLICIES_UPDATE = current_time
        return self.__POLICIES

    # model functions

    def __update_models(self):
        response = requests.get("{}/models".format(self.manager_url))
        models = response.json()
        if 'models' in models:
            for key, value in models["models"].items():
                self.__MODELS[key] = value
        else:
            raise exceptions.ModelNotFound("Cannot find 'models' key")

    @property
    def models(self):
        current_time = time.time()
        if self.__MODELS_UPDATE + self.__UPDATE_INTERVAL < current_time:
            self.__MODELS_UPDATE = current_time
            self.__update_models()
        self.__MODELS_UPDATE = current_time
        return self.__MODELS

    # helper functions

    def get_policy_from_meta_rules(self, meta_rule_id):
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
        meta_rules = []
        if "security_pipeline" in pdp_value:
            for policy_id in pdp_value["security_pipeline"]:
                if policy_id not in self.policies or "model_id" not in self.policies[policy_id]:
                    raise exceptions.PolicyUnknown("Cannot find 'models' key")
                model_id = self.policies[policy_id]["model_id"]
                if model_id not in self.models or 'meta_rules' not in self.models[model_id]:
                    raise exceptions.ModelNotFound("Cannot find 'models' key")
                for meta_rule in self.models[model_id]["meta_rules"]:
                    meta_rules.append(meta_rule)
            return meta_rules
        raise exceptions.PdpContentError

    def get_pdp_from_keystone_project(self, keystone_project_id):
        for pdp_key, pdp_value in self.pdp.items():
            if "keystone_project_id" in pdp_value and \
                    keystone_project_id == pdp_value["keystone_project_id"]:
                return pdp_key

    def get_keystone_project_id_from_policy_id(self, policy_id):
        for pdp_key, pdp_value in self.pdp.items():
            if "security_pipeline" in pdp_value and \
                    "keystone_project_id" in pdp_value:
                if policy_id in pdp_value["security_pipeline"]:
                    return pdp_value["keystone_project_id"]
            else:
                logger.warning(" 'security_pipeline','keystone_project_id' "
                               "key not in pdp {}".format(pdp_value))

    def get_keystone_project_id_from_pdp_id(self, pdp_id):
        if pdp_id in self.pdp:
            pdp_value = self.pdp.get(pdp_id)
            if "security_pipeline" in pdp_value and \
                    "keystone_project_id" in pdp_value:
                return pdp_value["keystone_project_id"]
        logger.warning("Unknown PDP ID".format(pdp_id))

    def get_containers_from_keystone_project_id(self, keystone_project_id,
                                                meta_rule_id=None):
        for container_id, container_values in self.containers.items():
            for container_value in container_values:
                if 'keystone_project_id' not in container_value:
                    continue
                if container_value['keystone_project_id'] == keystone_project_id:
                    if not meta_rule_id:
                        yield container_id, container_value
                    elif "meta_rule_id" in container_value and \
                            container_value.get('meta_rule_id') == meta_rule_id:
                        yield container_id, container_value
                        break

    # containers functions

    def __update_container(self):
        response = requests.get("{}/pods".format(self.orchestrator_url))
        pods = response.json()
        if "pods" in pods:
            for key, value in pods["pods"].items():
                # if key not in self.__CONTAINERS:
                self.__CONTAINERS[key] = value
                # else:
                #     for container in value:
                #         self.__CONTAINERS[key].update(value)
        else:
            raise exceptions.PodError("Cannot find 'pods' key")

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
        if all(k in container_data for k in ("keystone_project_id", "name", "container_id", "policy_id",
                                             "meta_rule_id", "port")) \
                and all(k in container_data['port'] for k in ("PublicPort", "Type", "IP", "PrivatePort")):

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
        else:
            raise exceptions.ContainerError("Cannot find 'container' parameters key")

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
            self.__CONTAINERS_UPDATE = current_time
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
            self.__CONTAINER_CHAINING_UPDATE = current_time
            for key, value in self.pdp.items():
                if "keystone_project_id" in value:
                    if not value["keystone_project_id"]:
                        continue
                    self.__update_container_chaining(value["keystone_project_id"])
                else:
                    logger.warning("no 'keystone_project_id' found")
        self.__CONTAINER_CHAINING_UPDATE = current_time
        return self.__CONTAINER_CHAINING

    def __update_container_chaining(self, keystone_project_id):
        container_ids = []
        for pdp_id, pdp_value, in self.__PDP.items():
            if pdp_value:
                if all(k in pdp_value for k in ("keystone_project_id", "security_pipeline")) \
                        and pdp_value["keystone_project_id"] == keystone_project_id:
                    for policy_id in pdp_value["security_pipeline"]:
                        if policy_id in self.policies and "model_id" in self.policies[policy_id]:
                            model_id = self.policies[policy_id]['model_id']
                            if model_id in self.models and "meta_rules" in self.models[model_id]:
                                for meta_rule_id in self.models[model_id]["meta_rules"]:
                                    for container_id, container_value in self.get_containers_from_keystone_project_id(
                                            keystone_project_id,
                                            meta_rule_id
                                    ):
                                        if "name" in container_value:
                                            if all(k in container_value for k in ("genre", "port")):
                                                container_ids.append(
                                                    {
                                                        "container_id": container_value["name"],
                                                        "genre": container_value["genre"],
                                                        "policy_id": policy_id,
                                                        "meta_rule_id": meta_rule_id,
                                                        "hostname": container_value["name"],
                                                        "hostip": "127.0.0.1",
                                                        "port": container_value["port"],
                                                    }
                                                )
                                            else:
                                                logger.warning("Container content keys not found {}", container_value)
                                        else:
                                            logger.warning("Container content keys not found {}", container_value)
                            else:
                                raise exceptions.ModelUnknown("Cannot find model_id: {} in models and "
                                                              "may not contains 'meta_rules' key".format(model_id))
                        else:
                            raise exceptions.PolicyUnknown("Cannot find policy within policy_id: {}, "
                                                           "and may not contains 'model_id' key".format(policy_id))

        self.__CONTAINER_CHAINING[keystone_project_id] = container_ids
