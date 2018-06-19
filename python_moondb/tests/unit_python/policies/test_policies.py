# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import pytest
import helpers.mock_data as mock_data
import helpers.policy_helper as policy_helper
from python_moonutilities.exceptions import *
import helpers.pdp_helper as pdp_helper


def test_get_policies(db):
    policies = policy_helper.get_policies()
    assert isinstance(policies, dict)
    assert not policies


def test_add_policies(db):
    value = {
        "name": "test_policy",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = policy_helper.add_policies(value=value)
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
    policy_helper.add_policies(policy_id, value)
    with pytest.raises(PolicyExisting) as exception_info:
        policy_helper.add_policies(policy_id, value)
    # assert str(exception_info.value) == '409: Policy Error'


def test_add_policies_twice_with_same_name(db):
    value = {
        "name": "test_policy",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policy_helper.add_policies(value=value)
    with pytest.raises(Exception) as exception_info:
        policy_helper.add_policies(value=value)
    # assert str(exception_info.value) == '409: Policy Error'


def test_delete_policies(db):
    value = {
        "name": "test_policy1",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = policy_helper.add_policies(value=value)
    policy_id1 = list(policies.keys())[0]
    value = {
        "name": "test_policy2",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = policy_helper.add_policies(value=value)
    policy_id2 = list(policies.keys())[0]
    assert policy_id1 != policy_id2
    policy_helper.delete_policies(policy_id1)
    policies = policy_helper.get_policies()
    assert policy_id1 not in policies


def test_delete_policies_with_invalid_id(db):
    policy_id = 'policy_id_1'
    with pytest.raises(PolicyUnknown) as exception_info:
        policy_helper.delete_policies(policy_id)
    # assert str(exception_info.value) == '400: Policy Unknown'


def test_update_policy(db):
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    value = {
        "name": "test_policy4",
        "model_id": "",
        "genre": "authz",
        "description": "test-3",
    }
    updated_policy = policy_helper.update_policy(policy_id, value)
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
        policy_helper.update_policy(policy_id, value)
    # assert str(exception_info.value) == '400: Policy Unknown'


def test_get_policy_from_meta_rules(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    security_pipeline = [policy_id]
    pdp_obj = mock_data.create_pdp(security_pipeline)
    pdp_helper.add_pdp(value=pdp_obj)
    matched_policy_id = policy_helper.get_policy_from_meta_rules(meta_rule_id)
    assert matched_policy_id
    assert policy_id == matched_policy_id


def test_get_policy_from_meta_rules_with_no_policy_ids(db):
    meta_rule_id = 'meta_rule_id'
    value = {
        "name": "test_pdp",
        "security_pipeline": [],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    pdp_helper.add_pdp(value=value)
    matched_policy_id = policy_helper.get_policy_from_meta_rules(meta_rule_id)
    assert not matched_policy_id


def test_get_rules(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category12",
        object_category_name="object_category12",
        action_category_name="action_category12",
        meta_rule_name="meta_rule_12",
        model_name="model12")
    value = {
        "rule": ("low", "medium", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
    policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    value = {
        "rule": ("low", "low", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
    policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    rules = policy_helper.get_rules(policy_id=policy_id, meta_rule_id=meta_rule_id)
    assert isinstance(rules, dict)
    assert rules
    obj = rules.get('rules')
    assert len(obj) == 2


def test_get_rules_with_invalid_policy_id_failure(db):
    rules = policy_helper.get_rules("invalid_policy_id", "meta_rule_id")
    assert not rules.get('meta_rule-id')
    assert len(rules.get('rules')) == 0


def test_add_rule(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "rule": ("high", "medium", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }

    rules = policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert rules
    assert len(rules) == 1
    assert isinstance(rules, dict)
    rule_id = list(rules.keys())[0]
    for key in ("rule", "instructions", "enabled"):
        assert key in rules[rule_id]
        assert rules[rule_id][key] == value[key]

    with pytest.raises(RuleExisting):
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)


def test_delete_rule(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category14",
        object_category_name="object_category14",
        action_category_name="action_category14",
        meta_rule_name="meta_rule_14",
        model_name="model14")
    value = {
        "rule": ("low", "low", "vm-action"),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }
    rules = policy_helper.add_rule(policy_id, meta_rule_id, value)
    rule_id = list(rules.keys())[0]
    policy_helper.delete_rule(policy_id, rule_id)
    rules = policy_helper.get_rules(policy_id, meta_rule_id)
    assert not rules.get('rules')


def test_delete_policies_with_pdp(db):
    value = {
        "name": "test_policy1",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = policy_helper.add_policies(value=value)
    policy_id1 = list(policies.keys())[0]
    pdp_id = "pdp_id1"
    value = {
        "name": "test_pdp",
        "security_pipeline": [policy_id1],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    pdp_helper.add_pdp(pdp_id=pdp_id, value=value)
    with pytest.raises(DeletePolicyWithPdp) as exception_info:
        policy_helper.delete_policies(policy_id1)
