# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
from  helpers import mock_data as mock_data
from helpers import meta_rule_helper

def get_policies():
    from python_moondb.core import PolicyManager
    return PolicyManager.get_policies("admin")


def add_policies(policy_id=None, value=None):
    from python_moondb.core import PolicyManager
    if not value:
        value = {
            "name": "test_policy",
            "model_id": "",
            "genre": "authz",
            "description": "test",
        }
    return PolicyManager.add_policy("admin", policy_id=policy_id, value=value)


def delete_policies(uuid=None, name=None):
    from python_moondb.core import PolicyManager
    if not uuid:
        for policy_id, policy_value in get_policies():
            if name == policy_value['name']:
                uuid = policy_id
                break
    PolicyManager.delete_policy("admin", uuid)


def update_policy(policy_id, value):
    from python_moondb.core import PolicyManager
    return PolicyManager.update_policy("admin", policy_id, value)


def get_policy_from_meta_rules(meta_rule_id):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_policy_from_meta_rules("admin", meta_rule_id)


def get_rules(policy_id=None, meta_rule_id=None, rule_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_rules("", policy_id, meta_rule_id, rule_id)


def add_rule(policy_id, meta_rule_id, value=None):
    from python_moondb.core import PolicyManager
    if not value:
        meta_rule = meta_rule_helper.get_meta_rules(meta_rule_id)
        sub_cat_id = meta_rule[meta_rule_id]['subject_categories'][0]
        ob_cat_id = meta_rule[meta_rule_id]['object_categories'][0]
        act_cat_id = meta_rule[meta_rule_id]['action_categories'][0]

        subject_data_id = mock_data.create_subject_data(policy_id=policy_id, category_id=sub_cat_id)
        object_data_id = mock_data.create_object_data(policy_id=policy_id, category_id=ob_cat_id)
        action_data_id = mock_data.create_action_data(policy_id=policy_id, category_id=act_cat_id)

        value = {
            "rule": (subject_data_id, object_data_id, action_data_id),
            "instructions": ({"decision": "grant"}),
            "enabled": "",
        }
    return PolicyManager.add_rule("", policy_id, meta_rule_id, value)


def delete_rule(policy_id=None, rule_id=None):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_rule("", policy_id, rule_id)
