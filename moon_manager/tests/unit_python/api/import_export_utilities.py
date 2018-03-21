# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import api.utilities as utilities
import api.test_unit_models as test_models
import api.test_policies as test_policies
import api.test_perimeter as test_perimeter
import api.meta_data_test as test_categories
import api.test_data as test_data
import api.meta_rules_test as test_meta_rules
import api.test_assignemnt as test_assignments
import api.test_rules as test_rules
import logging

logger = logging.getLogger("moon.manager.test.api." + __name__)


def clean_models(client):
    req, models = test_models.get_models(client)
    for key in models["models"]:
        client.delete("/models/{}".format(key))
        print("deleted model with id {}".format(key))


def clean_policies(client):
    req, policies = test_policies.get_policies(client)
    for key in policies["policies"]:
        req = client.delete("/policies/{}".format(key))
        assert req.status_code == 200
        print("deleted policy with id {}".format(key))


def clean_subjects(client):
    subjects = test_perimeter.get_subjects(client)
    logger.info("subjects {}".format(subjects))
    for key in subjects["subjects"]:
        subject = subjects["subjects"][key]
        policy_keys = subject["policy_list"]
        logger.info("subjects policy_keys {}".format(policy_keys))
        for policy_key in policy_keys:
            client.delete("/policies/{}/subjects/{}".format(policy_key,key))
        client.delete("/subjects/{}".format(key))
        print("deleted subject with id {}".format(key))


def clean_objects(client):
    objects = test_perimeter.get_objects(client)
    logger.info("objects {}".format(objects))
    for key in objects["objects"]:
        object_ = objects["objects"][key]
        policy_keys = object_["policy_list"]
        logger.info("objects policy_keys {}".format(policy_keys))
        for policy_key in policy_keys:
            print("/policies/{}/objects/{}".format(policy_key, key))
            req = client.delete("/policies/{}/objects/{}".format(policy_key, key))
        client.delete("/objects/{}".format(key))
        print("deleted object with id {}".format(key))


def clean_actions(client):
    actions = test_perimeter.get_actions(client)
    logger.info("objects {}".format(actions))
    for key in actions["actions"]:
        action = actions["actions"][key]
        policy_keys = action["policy_list"]
        logger.info("action policy_keys {}".format(policy_keys))
        for policy_key in policy_keys:
            client.delete("/policies/{}/actions/{}".format(policy_key, key))
        client.delete("/actions/{}".format(key))
        print("deleted action with id {}".format(key))


def clean_subject_categories(client):
    req, categories = test_categories.get_subject_categories(client)
    logger.info(categories)
    for key in categories["subject_categories"]:
        client.delete("/subject_categories/{}".format(key))


def clean_object_categories(client):
    req, categories = test_categories.get_object_categories(client)
    logger.info(categories)
    for key in categories["object_categories"]:
        client.delete("/object_categories/{}".format(key))


def clean_action_categories(client):
    req, categories = test_categories.get_action_categories(client)
    logger.info(categories)
    for key in categories["action_categories"]:
        client.delete("/action_categories/{}".format(key))


def clean_subject_data(client):
    req, policies = test_policies.get_policies(client)
    for policy_key in policies["policies"]:
        req, data = test_data.get_subject_data(client, policy_id=policy_key)
        print(data)
        for key in data["subject_data"]:
            client.delete("/policies/{}/subject_data/{}".format(policy_key, key))


def clean_object_data(client):
    req, policies = test_policies.get_policies(client)
    for policy_key in policies["policies"]:
        req, data = test_data.get_object_data(client, policy_id=policy_key)
        print(data)
        for key in data["object_data"]:
            client.delete("/policies/{}/object_data/{}".format(policy_key, key))


def clean_action_data(client):
    req, policies = test_policies.get_policies(client)
    for policy_key in policies["policies"]:
        req, data = test_data.get_action_data(client, policy_id=policy_key)
        for key in data["action_data"]:
            client.delete("/policies/{}/action_data/{}".format(policy_key, key))


def clean_meta_rule(client):
    req, meta_rules = test_meta_rules.get_meta_rules(client)
    meta_rules = meta_rules["meta_rules"]
    for meta_rule_key in meta_rules:
        print(meta_rule_key)
        client.delete("/meta_rules/{}".format(meta_rule_key))


def clean_subject_assignments(client):
    req, policies = test_policies.get_policies(client)
    for policy_key in policies["policies"]:
        req, assignments = test_assignments.get_subject_assignment(client, policy_key)
        for key in assignments["subject_assignments"]:
            subject_key = assignments["subject_assignments"][key]["subject_id"]
            cat_key = assignments["subject_assignments"][key]["category_id"]
            data_keys = assignments["subject_assignments"][key]["assignments"]
            for data_key in data_keys:
                req = client.delete("/policies/{}/subject_assignments/{}/{}/{}".format(policy_key, subject_key, cat_key, data_key))


def clean_object_assignments(client):
    req, policies = test_policies.get_policies(client)
    for policy_key in policies["policies"]:
        req, assignments = test_assignments.get_object_assignment(client, policy_key)
        for key in assignments["object_assignments"]:
            object_key = assignments["object_assignments"][key]["object_id"]
            cat_key = assignments["object_assignments"][key]["category_id"]
            data_keys = assignments["object_assignments"][key]["assignments"]
            for data_key in data_keys:
                req = client.delete("/policies/{}/object_assignments/{}/{}/{}".format(policy_key, object_key, cat_key, data_key))


def clean_action_assignments(client):
    req, policies = test_policies.get_policies(client)
    for policy_key in policies["policies"]:
        req, assignments = test_assignments.get_action_assignment(client, policy_key)
        for key in assignments["action_assignments"]:
            action_key = assignments["action_assignments"][key]["action_id"]
            cat_key = assignments["action_assignments"][key]["category_id"]
            data_keys = assignments["action_assignments"][key]["assignments"]
            for data_key in data_keys:
                req = client.delete("/policies/{}/action_assignments/{}/{}/{}".format(policy_key, action_key, cat_key, data_key))


def clean_rules(client):
    req, policies = test_policies.get_policies(client)
    for policy_key in policies["policies"]:
        req, rules = test_rules.get_rules(client, policy_key)
        print(rules)
        rules = rules["rules"]
        rules = rules["rules"]
        for rule_key in rules:
            client.delete("/policies/{}/rules/{}".format(policy_key, rule_key))


def clean_all(client):
    clean_rules(client)

    clean_subject_assignments(client)
    clean_object_assignments(client)
    clean_action_assignments(client)

    clean_meta_rule(client)

    clean_subject_categories(client)
    clean_object_categories(client)
    clean_action_categories(client)

    clean_subject_data(client)
    clean_object_data(client)
    clean_action_data(client)

    clean_actions(client)
    clean_objects(client)
    clean_subjects(client)

    clean_policies(client)
    clean_models(client)