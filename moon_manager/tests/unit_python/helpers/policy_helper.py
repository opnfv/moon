# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from uuid import uuid4
from helpers import model_helper

def get_policies():
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_policies("admin")


def add_policies(policy_id=None, value=None):
    from moon_manager.db_driver import PolicyManager
    if not value:
        value = {
            "name": "test_policy"+ uuid4().hex,
            "model_id": "",
            "genre": "authz",
            "description": "test",
        }
    return PolicyManager.add_policy(moon_user_id="admin", policy_id=policy_id, value=value)


def add_policies_with_model(policy_id=None, value=None):
    from moon_manager.db_driver import PolicyManager
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": "test_policy"+ uuid4().hex,
        "description": "test",
        "model_id": model_id,
        "genre": "genre"
    }
    return PolicyManager.add_policy(moon_user_id="admin", policy_id=policy_id, value=data)


def delete_policies(uuid=None, name=None):
    from moon_manager.db_driver import PolicyManager
    if not uuid:
        for policy_id, policy_value in get_policies():
            if name == policy_value['name']:
                uuid = policy_id
                break
    PolicyManager.delete_policy("admin", uuid)


def update_policy(policy_id, value):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.update_policy("admin", policy_id, value)


def get_policy_from_meta_rules(meta_rule_id):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_policy_from_meta_rules("admin", meta_rule_id)


def get_rules(policy_id=None, meta_rule_id=None, rule_id=None):
    from moon_manager.db_driver import PolicyManager
    return PolicyManager.get_rules("", policy_id, meta_rule_id, rule_id)


def add_rule(policy_id=None, meta_rule_id=None, value=None):
    from moon_manager.db_driver import PolicyManager
    if not value:
        value = {
            "rule": ("high", "medium", "vm-action"),
            "instructions": [{"decision": "grant"}],
            "enabled": "",
        }
    return PolicyManager.add_rule("", policy_id, meta_rule_id, value)


def delete_rule(policy_id=None, rule_id=None):
    from moon_manager.db_driver import PolicyManager
    PolicyManager.delete_rule("", policy_id, rule_id)
