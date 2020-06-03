# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



def get_action_assignments(policy_id, action_id=None, category_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_action_assignments("", policy_id, action_id, category_id)


def add_action_assignment(policy_id, action_id, category_id, data_id):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.add_action_assignment("", policy_id, action_id, category_id, data_id)


def delete_action_assignment(policy_id, action_id, category_id, data_id):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_action_assignment("", policy_id, action_id, category_id, data_id)


def get_object_assignments(policy_id, object_id=None, category_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_object_assignments("", policy_id, object_id, category_id)


def add_object_assignment(policy_id, object_id, category_id, data_id):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.add_object_assignment("", policy_id, object_id, category_id, data_id)


def delete_object_assignment(policy_id, object_id, category_id, data_id):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_object_assignment("", policy_id, object_id, category_id, data_id)


def get_subject_assignments(policy_id, subject_id=None, category_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_subject_assignments("", policy_id, subject_id, category_id)


def add_subject_assignment(policy_id, subject_id, category_id, data_id):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.add_subject_assignment("", policy_id, subject_id, category_id, data_id)


def delete_subject_assignment(policy_id, subject_id, category_id, data_id):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_subject_assignment("", policy_id, subject_id, category_id, data_id)

