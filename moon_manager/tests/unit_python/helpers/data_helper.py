# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



def get_action_data(policy_id, data_id=None, category_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_action_data(moon_user_id="admin", policy_id=policy_id, data_id=data_id, category_id=category_id)


def add_action_data(policy_id, data_id=None, category_id=None, value=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.add_action_data(moon_user_id="admin", policy_id=policy_id, data_id=data_id, category_id=category_id, value=value)


def delete_action_data(policy_id, data_id):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_action_data(moon_user_id="admin", policy_id=policy_id, data_id=data_id)


def get_object_data(policy_id, data_id=None, category_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_object_data(moon_user_id="admin", policy_id=policy_id, data_id=data_id, category_id=category_id)


def add_object_data(policy_id, data_id=None, category_id=None, value=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.add_object_data(moon_user_id="admin", policy_id=policy_id, data_id=data_id, category_id=category_id, value=value)


def delete_object_data(policy_id, data_id):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_object_data(moon_user_id="admin", policy_id=policy_id, data_id=data_id)


def get_subject_data(policy_id, data_id=None, category_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_subject_data(moon_user_id="admin", policy_id=policy_id, data_id=data_id, category_id=category_id)


def add_subject_data(policy_id, data_id=None, category_id=None, value=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.set_subject_data(moon_user_id="admin", policy_id=policy_id, data_id=data_id, category_id=category_id, value=value)


def delete_subject_data(policy_id, data_id):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_subject_data(moon_user_id="admin", policy_id=policy_id, data_id=data_id)


def get_actions(policy_id, perimeter_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_actions(moon_user_id="admin", policy_id=policy_id, perimeter_id=perimeter_id)


def add_action(policy_id, perimeter_id=None, value=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.add_action(moon_user_id="admin", policy_id=policy_id, perimeter_id=perimeter_id, value=value)


def delete_action(policy_id, perimeter_id):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_action(moon_user_id="admin", policy_id=policy_id, perimeter_id=perimeter_id)


def get_objects(policy_id, perimeter_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_objects(moon_user_id="admin", policy_id=policy_id, perimeter_id=perimeter_id)


def add_object(policy_id, perimeter_id=None, value=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.add_object(moon_user_id="admin", policy_id=policy_id, perimeter_id=perimeter_id, value=value)


def delete_object(policy_id, perimeter_id):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_object(moon_user_id="admin", policy_id=policy_id, perimeter_id=perimeter_id)


def get_subjects(policy_id, perimeter_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_subjects(moon_user_id="admin", policy_id=policy_id, perimeter_id=perimeter_id)


def add_subject(policy_id, perimeter_id=None, value=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.add_subject(moon_user_id="admin", policy_id=policy_id, perimeter_id=perimeter_id, value=value)


def delete_subject(policy_id, perimeter_id):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_subject(moon_user_id="admin", policy_id=policy_id, perimeter_id=perimeter_id)


def get_available_metadata(policy_id):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_available_metadata(moon_user_id="admin", policy_id=policy_id)
