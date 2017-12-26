# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


def get_policies():
    from python_moondb.core import PolicyManager
    return PolicyManager.get_policies("admin")


def add_policies(value=None):
    from python_moondb.core import PolicyManager
    if not value:
        value = {
            "name": "test_policiy",
            "model_id": "",
            "genre": "authz",
            "description": "test",
        }
    return PolicyManager.add_policy("admin", value=value)


def delete_policies(uuid=None, name=None):
    from python_moondb.core import PolicyManager
    if not uuid:
        for policy_id, policy_value in get_policies():
            if name == policy_value['name']:
                uuid = policy_id
                break
    PolicyManager.delete_policy("admin", uuid)


def get_rules(policy_id=None, meta_rule_id=None, rule_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_rules("", policy_id, meta_rule_id, rule_id)


def add_rule(policy_id=None, meta_rule_id=None, value=None):
    from python_moondb.core import PolicyManager
    if not value:
        value = {
            "rule": ("high", "medium", "vm-action"),
            "instructions": ({"decision": "grant"}),
            "enabled": "",
        }
    return PolicyManager.add_rule("", policy_id, meta_rule_id, value)


def delete_rule(policy_id=None, rule_id=None):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_rule("", policy_id, rule_id)


def test_get_policies(db):
    policies = get_policies()
    assert isinstance(policies, dict)
    assert not policies


def test_add_policies(db):
    value = {
        "name": "test_policy",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = add_policies(value)
    assert isinstance(policies, dict)
    assert policies
    assert len(policies.keys()) == 1
    policy_id = list(policies.keys())[0]
    for key in ("genre", "name", "model_id", "description"):
        assert key in policies[policy_id]
        assert policies[policy_id][key] == value[key]


def test_delete_policies(db):
    value = {
        "name": "test_policy1",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = add_policies(value)
    policy_id1 = list(policies.keys())[0]
    value = {
        "name": "test_policy2",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = add_policies(value)
    policy_id2 = list(policies.keys())[0]
    assert policy_id1 != policy_id2
    delete_policies(policy_id1)
    policies = get_policies()
    assert policy_id1 not in policies


def test_get_rules(db):
    value = {
        "rule": ("low", "medium", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
    policy_id = "1"
    meta_rule_id = "1"
    add_rule(policy_id, meta_rule_id, value)
    value = {
        "rule": ("low", "low", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
    policy_id = "1"
    meta_rule_id = "1"
    add_rule(policy_id, meta_rule_id, value)
    rules = get_rules(policy_id, meta_rule_id)
    assert isinstance(rules, dict)
    assert rules
    obj = rules.get('rules')
    assert len(obj) == 2


def test_get_rules_with_invalid_policy_id_failure(db):
    rules = get_rules("invalid_policy_id", "meta_rule_id")
    assert not rules.get('meta_rule-id')
    assert len(rules.get('rules')) == 0


def test_add_rule(db):
    value = {
        "rule": ("high", "medium", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
    policy_id = "1"
    meta_rule_id = "1"
    rules = add_rule(policy_id, meta_rule_id, value)
    assert rules
    assert len(rules) == 1
    assert isinstance(rules, dict)
    rule_id = list(rules.keys())[0]
    for key in ("rule", "instructions", "enabled"):
        assert key in rules[rule_id]
        assert rules[rule_id][key] == value[key]


def test_delete_rule(db):
    value = {
        "rule": ("low", "low", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
    policy_id = "2"
    meta_rule_id = "2"
    rules = add_rule(policy_id, meta_rule_id, value)
    rule_id = list(rules.keys())[0]
    delete_rule(policy_id, rule_id)
    rules = get_rules(policy_id, meta_rule_id)
    assert not rules.get('rules')
