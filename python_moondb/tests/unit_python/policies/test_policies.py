# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import pytest
import policies.mock_data as mock_data
from python_moonutilities.exceptions import *

def get_policies():
    from python_moondb.core import PolicyManager
    return PolicyManager.get_policies("admin")


def add_policies(policy_id=None, value=None):
    from python_moondb.core import PolicyManager
    if not value:
        value = {
            "name": "test_policiy",
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
    policies = add_policies(value=value)
    assert isinstance(policies, dict)
    assert policies
    assert len(policies.keys()) == 1
    policy_id = list(policies.keys())[0]
    for key in ("genre", "name", "model_id", "description"):
        assert key in policies[policy_id]
        assert policies[policy_id][key] == value[key]


def test_add_policies_twice_with_same_id(db):
    policy_id = 'policy_id_1'
    value = {
        "name": "test_policy",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    add_policies(policy_id, value)
    with pytest.raises(PolicyExisting) as exception_info:
        add_policies(policy_id, value)
    #assert str(exception_info.value) == '409: Policy Error'


def test_delete_policies(db):
    value = {
        "name": "test_policy1",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = add_policies(value=value)
    policy_id1 = list(policies.keys())[0]
    value = {
        "name": "test_policy2",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = add_policies(value=value)
    policy_id2 = list(policies.keys())[0]
    assert policy_id1 != policy_id2
    delete_policies(policy_id1)
    policies = get_policies()
    assert policy_id1 not in policies


def test_delete_policies_with_invalid_id(db):
    policy_id = 'policy_id_1'
    with pytest.raises(PolicyUnknown) as exception_info:
        delete_policies(policy_id)
    #assert str(exception_info.value) == '400: Policy Unknown'


def test_update_policy(db):
    policies = add_policies()
    policy_id = list(policies.keys())[0]
    value = {
        "name": "test_policy4",
        "model_id": "",
        "genre": "authz",
        "description": "test-3",
    }
    updated_policy = update_policy(policy_id, value)
    assert updated_policy
    for key in ("genre", "name", "model_id", "description"):
        assert key in updated_policy[policy_id]
        assert updated_policy[policy_id][key] == value[key]


def test_update_policy_with_invalid_id(db):
    policy_id = 'invalid-id'
    value = {
        "name": "test_policy4",
        "model_id": "",
        "genre": "authz",
        "description": "test-3",
    }
    with pytest.raises(PolicyUnknown) as exception_info:
        update_policy(policy_id, value)
    #assert str(exception_info.value) == '400: Policy Unknown'


def test_get_policy_from_meta_rules(db):
    import models.test_models as test_models
    import models.test_meta_rules as test_meta_rules
    import test_pdp as test_pdp
    meta_rule = test_meta_rules.add_meta_rule(value=mock_data.create_meta_rule())
    meta_rule_id = list(meta_rule.keys())[0]
    model = test_models.add_model(value=mock_data.create_model(meta_rule_id))
    model_id = list(model.keys())[0]
    value = mock_data.create_policy(model_id)
    policy = add_policies(value=value)
    assert policy
    policy_id = list(policy.keys())[0]
    pdp_ids = [policy_id,]
    pdp_obj = mock_data.create_pdp(pdp_ids)
    test_pdp.add_pdp(value=pdp_obj)
    matched_policy_id = get_policy_from_meta_rules(meta_rule_id)
    assert matched_policy_id
    assert policy_id == matched_policy_id


def test_get_policy_from_meta_rules_with_no_policy_ids(db):
    import test_pdp as test_pdp
    meta_rule_id = 'meta_rule_id'
    value = {
        "name": "test_pdp",
        "security_pipeline": [],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    test_pdp.add_pdp(value=value)
    matched_policy_id = get_policy_from_meta_rules(meta_rule_id)
    assert not matched_policy_id


def test_get_policy_from_meta_rules_with_no_policies(db):
    import test_pdp as test_pdp
    meta_rule_id = 'meta_rule_id'
    policy_id = 'invalid'
    pdp_ids = [policy_id,]
    pdp_obj = mock_data.create_pdp(pdp_ids)
    test_pdp.add_pdp(value=pdp_obj)
    with pytest.raises(Exception) as exception_info:
        get_policy_from_meta_rules(meta_rule_id)
    assert str(exception_info.value) == '400: Policy Unknown'


def test_get_policy_from_meta_rules_with_no_models(db):
    import models.test_meta_rules as test_meta_rules
    import test_pdp as test_pdp
    meta_rule = test_meta_rules.add_meta_rule(value=mock_data.create_meta_rule())
    meta_rule_id = list(meta_rule.keys())[0]
    model_id = 'invalid'
    value = mock_data.create_policy(model_id)
    policy = add_policies(value=value)
    assert policy
    policy_id = list(policy.keys())[0]
    pdp_ids = [policy_id,]
    pdp_obj = mock_data.create_pdp(pdp_ids)
    test_pdp.add_pdp(value=pdp_obj)
    with pytest.raises(Exception) as exception_info:
        get_policy_from_meta_rules(meta_rule_id)
    assert str(exception_info.value) == '400: Model Unknown'


def test_get_rules(db):
    value = {
        "rule": ("low", "medium", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
    policy_id = mock_data.get_policy_id()
    meta_rule_id = "1"
    add_rule(policy_id, meta_rule_id, value)
    value = {
        "rule": ("low", "low", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
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
    policy_id = mock_data.get_policy_id()
    meta_rule_id = "1"
    rules = add_rule(policy_id, meta_rule_id, value)
    assert rules
    assert len(rules) == 1
    assert isinstance(rules, dict)
    rule_id = list(rules.keys())[0]
    for key in ("rule", "instructions", "enabled"):
        assert key in rules[rule_id]
        assert rules[rule_id][key] == value[key]

    with pytest.raises(RuleExisting):
        add_rule(policy_id, meta_rule_id, value)


def test_delete_rule(db):
    value = {
        "rule": ("low", "low", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
    policy_id = mock_data.get_policy_id()
    meta_rule_id = "2"
    rules = add_rule(policy_id, meta_rule_id, value)
    rule_id = list(rules.keys())[0]
    delete_rule(policy_id, rule_id)
    rules = get_rules(policy_id, meta_rule_id)
    assert not rules.get('rules')
