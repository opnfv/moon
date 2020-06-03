# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging

logger = logging.getLogger("moon.manager.test.api." + __name__)


def clean_models():
    from moon_manager import db_driver as driver
    keys = driver.ModelManager.get_models(moon_user_id="admin")
    for key in keys:
        driver.ModelManager.delete_model(moon_user_id="admin", model_id=key)


def clean_policies():
    from moon_manager import db_driver as driver
    keys = driver.PolicyManager.get_policies(moon_user_id="admin")
    for key in keys:
        driver.PolicyManager.delete_policy(moon_user_id="admin", policy_id=key)


def clean_subjects():
    from moon_manager import db_driver as driver
    for policy in driver.PolicyManager.get_policies(moon_user_id="admin"):
        subjects = driver.PolicyManager.get_subjects(moon_user_id="admin", policy_id=policy)
        for key in subjects:
            driver.PolicyManager.delete_subject(moon_user_id="admin", policy_id=policy,
                                                perimeter_id=key)


def clean_objects():
    from moon_manager import db_driver as driver
    for policy in driver.PolicyManager.get_policies(moon_user_id="admin"):
        objects = driver.PolicyManager.get_objects(moon_user_id="admin", policy_id=policy)
        for key in objects:
            driver.PolicyManager.delete_object(moon_user_id="admin", policy_id=policy,
                                               perimeter_id=key)


def clean_actions():
    from moon_manager import db_driver as driver
    for policy in driver.PolicyManager.get_policies(moon_user_id="admin"):
        actions = driver.PolicyManager.get_actions(moon_user_id="admin", policy_id=policy)
        for key in actions:
            driver.PolicyManager.delete_action(moon_user_id="admin", policy_id=policy,
                                               perimeter_id=key)


def clean_subject_categories():
    from moon_manager import db_driver as driver
    categories = driver.ModelManager.get_subject_categories(moon_user_id="admin")

    for key in categories:
        driver.ModelManager.delete_subject_category(moon_user_id="admin", category_id=key)


def clean_object_categories():
    from moon_manager import db_driver as driver
    categories = driver.ModelManager.get_object_categories(moon_user_id="admin")

    for key in categories:
        driver.ModelManager.delete_object_category(moon_user_id="admin", category_id=key)


def clean_action_categories():
    from moon_manager import db_driver as driver
    categories = driver.ModelManager.get_action_categories(moon_user_id="admin")

    for key in categories:
        driver.ModelManager.delete_action_category(moon_user_id="admin", category_id=key)


def clean_subject_data():
    from moon_manager import db_driver as driver
    policies = driver.PolicyManager.get_policies(moon_user_id="admin")
    categories = driver.ModelManager.get_subject_categories(moon_user_id="admin")
    for policy in policies:
        for category in categories:
            data_object = driver.PolicyManager.get_subject_data(
                moon_user_id="admin", policy_id=policy, category_id=category)
            for data_item in data_object:
                for data in data_item.get("data", {}):
                    driver.PolicyManager.delete_subject_data(moon_user_id="admin", policy_id=policy,
                                                             category_id=category, data_id=data)


def clean_object_data():
    from moon_manager import db_driver as driver
    policies = driver.PolicyManager.get_policies(moon_user_id="admin")
    categories = driver.ModelManager.get_object_categories(moon_user_id="admin")
    for policy in policies:
        for category in categories:
            data_object = driver.PolicyManager.get_object_data(
                moon_user_id="admin", policy_id=policy, category_id=category)
            for data_item in data_object:
                for data in data_item.get("data", {}):
                    driver.PolicyManager.delete_object_data(moon_user_id="admin", policy_id=policy,
                                                            category_id=category, data_id=data)


def clean_action_data():
    from moon_manager import db_driver as driver
    policies = driver.PolicyManager.get_policies(moon_user_id="admin")
    categories = driver.ModelManager.get_action_categories(moon_user_id="admin")
    for policy in policies:
        for category in categories:
            data_object = driver.PolicyManager.get_action_data(
                moon_user_id="admin", policy_id=policy, category_id=category)
            for data_item in data_object:
                for data in data_item.get("data", {}):
                    driver.PolicyManager.delete_action_data(moon_user_id="admin", policy_id=policy,
                                                            category_id=category, data_id=data)


def clean_meta_rule():
    from moon_manager import db_driver as driver
    keys = driver.ModelManager.get_meta_rules(moon_user_id="admin")

    for key in keys:
        driver.ModelManager.delete_meta_rule(moon_user_id="admin", meta_rule_id=key)


def clean_subject_assignments():
    pass


def clean_object_assignments():
    pass


def clean_action_assignments():
    pass


def clean_rules():
    from moon_manager import db_driver as driver

    policies = driver.PolicyManager.get_policies(moon_user_id="admin")

    for policy in policies:
        rules = driver.PolicyManager.get_rules(moon_user_id="admin", policy_id=policy)

        for rule in rules:
            driver.PolicyManager.delete_rule(moon_user_id="admin", policy_id=policy, rule_id=rule)


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
