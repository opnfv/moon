# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from api import test_models as test_models
from api import test_policies as test_policies
from api import test_perimeter as test_perimeter
from api import test_meta_data as test_categories
from api import test_data as test_data
from api import test_meta_rules as test_meta_rules
from api import test_assignement as test_assignments
from api import test_rules as test_rules
import logging
import hug

logger = logging.getLogger("moon.manager.test.api." + __name__)


def clean_models():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req, models = test_models.get_models()
    for key in models["models"]:
        from moon_manager.api import models
        hug.test.delete(models, "/models/{}".format(key), headers=auth_headers)


def clean_policies():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = test_policies.get_policies(auth_headers=auth_headers)

    policies = req.data
    for key in policies["policies"]:
        from moon_manager.api import policy
        req = hug.test.delete(policy, "/policies/{}".format(key), headers=auth_headers)
        assert req.status == hug.HTTP_200


def clean_subjects():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    subjects = test_perimeter.get_subjects()
    logger.info("subjects {}".format(subjects))
    for key in subjects[1]["subjects"]:
        subject = subjects[1]["subjects"][key]
        policy_keys = subject["policy_list"]
        logger.info("subjects policy_keys {}".format(policy_keys))
        for policy_key in policy_keys:
            from moon_manager.api import perimeter
            hug.test.delete(perimeter, "/policies/{}/subjects/{}".format(policy_key, key), headers=auth_headers )
        hug.test.delete(perimeter, "/subjects/{}".format(key), headers=auth_headers)


def clean_objects():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    objects = test_perimeter.get_objects()
    logger.info("objects {}".format(objects))
    for key in objects[1]["objects"]:
        object_ = objects[1]["objects"][key]
        policy_keys = object_["policy_list"]
        logger.info("objects policy_keys {}".format(policy_keys))
        for policy_key in policy_keys:
            from moon_manager.api import perimeter
            hug.test.delete(perimeter, "/policies/{}/objects/{}".format(policy_key, key), headers=auth_headers )
        hug.test.delete(perimeter, "/objects/{}".format(key), headers=auth_headers)

def clean_actions():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    actions = test_perimeter.get_actions()
    logger.info("actions {}".format(actions))
    for key in actions[1]["actions"]:
        action = actions[1]["actions"][key]
        policy_keys = action["policy_list"]
        logger.info("action policy_keys {}".format(policy_keys))
        from moon_manager.api import perimeter
        for policy_key in policy_keys:
            hug.test.delete(perimeter, "/policies/{}/actions/{}".format(policy_key, key), headers=auth_headers)
        hug.test.delete(perimeter, "/actions/{}".format(key), headers=auth_headers)



def clean_subject_categories():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req, categories = test_categories.get_subject_categories()
    logger.info(categories)
    for key in categories["subject_categories"]:
        from moon_manager.api import meta_data
        hug.test.delete(meta_data, "/subject_categories/{}".format(key), headers=auth_headers)


def clean_object_categories():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req, categories = test_categories.get_object_categories()
    logger.info(categories)
    for key in categories["object_categories"]:
        from moon_manager.api import meta_data
        hug.test.delete(meta_data, "/object_categories/{}".format(key), headers=auth_headers)


def clean_action_categories():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req, categories = test_categories.get_action_categories()
    logger.info(categories)
    for key in categories["action_categories"]:
        from moon_manager.api import meta_data
        hug.test.delete(meta_data, "/action_categories/{}".format(key), headers=auth_headers)


def clean_subject_data():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = test_policies.get_policies(auth_headers=auth_headers)

    policies = req.data
    logger.info("clean_subject_data on {}".format(policies))
    for policy_key in policies["policies"]:
        req, data = test_data.get_subject_data(policy_id=policy_key)
        logger.info("============= data {}".format(data))
        for data_item in data["subject_data"]:
            if data_item["data"]:
                for data_id in data_item["data"]:
                    logger.info("============= Deleting {}/{}".format(policy_key, data_id))
                    from moon_manager.api import data
                    hug.test.delete(data, "/policies/{}/subject_data/{}/{}".format(policy_key,
                                            data_item['category_id'], data_id), headers=auth_headers)


def clean_object_data():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = test_policies.get_policies(auth_headers=auth_headers)

    policies = req.data
    for policy_key in policies["policies"]:
        req, data = test_data.get_object_data(policy_id=policy_key)
        for data_item in data["object_data"]:
            if data_item["data"]:
                for data_id in data_item["data"]:
                    logger.info("============= object_data {}/{}".format(policy_key, data_id))
                    from moon_manager.api import data
                    hug.test.delete(data, "/policies/{}/object_data/{}/{}".format(policy_key,
                                        data_item['category_id'], data_id), headers=auth_headers)


def clean_action_data():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = test_policies.get_policies(auth_headers=auth_headers)

    policies = req.data
    for policy_key in policies["policies"]:
        req, data = test_data.get_action_data(policy_id=policy_key)
        for data_item in data["action_data"]:
            if data_item["data"]:
                for data_id in data_item["data"]:
                    logger.info("============= action_data {}/{}".format(policy_key, data_id))
                    from moon_manager.api import data
                    hug.test.delete(data, "/policies/{}/action_data/{}/{}".format(policy_key,
                                        data_item['category_id'], data_id), headers=auth_headers)


def clean_meta_rule():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req, meta_rules_obj = test_meta_rules.get_meta_rules()
    meta_rules_obj = meta_rules_obj["meta_rules"]
    for meta_rule_key in meta_rules_obj:
        logger.info("clean_meta_rule.meta_rule_key={}".format(meta_rule_key))
        logger.info("clean_meta_rule.meta_rule={}".format(meta_rules_obj[meta_rule_key]))
        from moon_manager.api import meta_rules
        hug.test.delete(meta_rules, "/meta_rules/{}".format(meta_rule_key), headers=auth_headers)


def clean_subject_assignments():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = test_policies.get_policies(auth_headers=auth_headers)

    policies = req.data
    for policy_key in policies["policies"]:
        req, assignments = test_assignments.get_subject_assignment(policy_key)
        for key in assignments["subject_assignments"]:
            subject_key = assignments["subject_assignments"][key]["subject_id"]
            cat_key = assignments["subject_assignments"][key]["category_id"]
            data_keys = assignments["subject_assignments"][key]["assignments"]
            for data_key in data_keys:
                from moon_manager.api import assignments
                hug.test.delete(assignments,
                                "/policies/{}/subject_assignments/{}/{}/{}".format(policy_key,
                                        subject_key, cat_key, data_key), headers=auth_headers)


def clean_object_assignments():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = test_policies.get_policies(auth_headers=auth_headers)

    policies = req.data
    for policy_key in policies["policies"]:
        req, assignments = test_assignments.get_object_assignment(policy_key)
        for key in assignments["object_assignments"]:
            object_key = assignments["object_assignments"][key]["object_id"]
            cat_key = assignments["object_assignments"][key]["category_id"]
            data_keys = assignments["object_assignments"][key]["assignments"]
            for data_key in data_keys:
                from moon_manager.api import assignments
                hug.test.delete(assignments,
                                "/policies/{}/object_assignments/{}/{}/{}".format(policy_key,
                                            object_key, cat_key, data_key), headers=auth_headers)


def clean_action_assignments():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = test_policies.get_policies(auth_headers=auth_headers)

    policies = req.data
    for policy_key in policies["policies"]:
        req, assignments = test_assignments.get_action_assignment(policy_key)
        for key in assignments["action_assignments"]:
            action_key = assignments["action_assignments"][key]["action_id"]
            cat_key = assignments["action_assignments"][key]["category_id"]
            data_keys = assignments["action_assignments"][key]["assignments"]
            for data_key in data_keys:
                from moon_manager.api import assignments
                hug.test.delete(assignments,
                                "/policies/{}/action_assignments/{}/{}/{}".format(policy_key,
                                            action_key, cat_key, data_key), headers=auth_headers)


def clean_rules():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = test_policies.get_policies(auth_headers=auth_headers)

    policies = req.data
    for policy_key in policies["policies"]:
        req, rules = test_rules.get_rules(policy_key)
        rules = rules["rules"]["rules"]
        for rule_key in rules:
            from moon_manager.api import rules
            hug.test.delete(rules, "/policies/{}/rules/{}".format(policy_key, rule_key["id"]), headers=auth_headers)


def clean_all():
    clean_rules()

    clean_subject_assignments()
    clean_object_assignments()
    clean_action_assignments()

    clean_subject_data()
    clean_object_data()
    clean_action_data()

    clean_actions()
    clean_objects()
    clean_subjects()

    clean_policies()
    clean_models()
    clean_meta_rule()

    clean_subject_categories()
    clean_object_categories()
    clean_action_categories()
