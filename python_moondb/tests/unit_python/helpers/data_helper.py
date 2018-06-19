# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

def get_action_data(policy_id, data_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_action_data("", policy_id, data_id, category_id)


def add_action_data(policy_id, data_id=None, category_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_action_data("", policy_id, data_id, category_id, value)


def delete_action_data(policy_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_action_data("", policy_id, data_id)


def get_object_data(policy_id, data_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_object_data("", policy_id, data_id, category_id)


def add_object_data(policy_id, data_id=None, category_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_object_data("", policy_id, data_id, category_id, value)


def delete_object_data(policy_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_object_data("", policy_id, data_id)


def get_subject_data(policy_id, data_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_subject_data("", policy_id, data_id, category_id)


def add_subject_data(policy_id, data_id=None, category_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.set_subject_data("", policy_id, data_id, category_id, value)


def delete_subject_data(policy_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_subject_data("", policy_id, data_id)


def get_actions(policy_id, perimeter_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_actions("", policy_id, perimeter_id)


def add_action(policy_id, perimeter_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_action("", policy_id, perimeter_id, value)


def delete_action(policy_id, perimeter_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_action("", policy_id, perimeter_id)


def get_objects(policy_id, perimeter_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_objects("", policy_id, perimeter_id)


def add_object(policy_id, perimeter_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_object("", policy_id, perimeter_id, value)


def delete_object(policy_id, perimeter_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_object("", policy_id, perimeter_id)


def get_subjects(policy_id, perimeter_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_subjects("", policy_id, perimeter_id)


def add_subject(policy_id, perimeter_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_subject("", policy_id, perimeter_id, value)


def delete_subject(policy_id, perimeter_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_subject("", policy_id, perimeter_id)


def get_available_metadata(policy_id):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_available_metadata("", policy_id)
