# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

def get_action_assignments(policy_id, action_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_action_assignments("", policy_id, action_id, category_id)


def add_action_assignment(policy_id, action_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_action_assignment("", policy_id, action_id, category_id, data_id)


def delete_action_assignment(policy_id, action_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_action_assignment("", policy_id, action_id, category_id, data_id)


def get_object_assignments(policy_id, object_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_object_assignments("", policy_id, object_id, category_id)


def add_object_assignment(policy_id, object_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_object_assignment("", policy_id, object_id, category_id, data_id)


def delete_object_assignment(policy_id, object_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_object_assignment("", policy_id, object_id, category_id, data_id)


def get_subject_assignments(policy_id, subject_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_subject_assignments("", policy_id, subject_id, category_id)


def add_subject_assignment(policy_id, subject_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_subject_assignment("", policy_id, subject_id, category_id, data_id)


def delete_subject_assignment(policy_id, subject_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_subject_assignment("", policy_id, subject_id, category_id, data_id)

