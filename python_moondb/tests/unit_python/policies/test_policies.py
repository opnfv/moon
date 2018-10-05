# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import pytest
import helpers.mock_data as mock_data
import helpers.policy_helper as policy_helper
import helpers.model_helper as model_helper
import helpers.model_helper as model_helper
from python_moonutilities.exceptions import *
import helpers.pdp_helper as pdp_helper
import helpers.data_helper as data_helper
import helpers.assignment_helper as assignment_helper
from uuid import uuid4


def test_get_policies(db):
    policies = policy_helper.get_policies()
    assert isinstance(policies, dict)
    assert not policies


def test_add_policies(db):
    model = model_helper.add_model(model_id=uuid4().hex)
    model_id = next(iter(model))
    value = {
        "name": "test_policy",
        "model_id": model_id,
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
    model = model_helper.add_model(model_id=uuid4().hex)
    model_id = next(iter(model))
    value = {
        "name": "test_policy",
        "model_id": model_id,
        "genre": "authz",
        "description": "test",
    }
    policy_helper.add_policies(policy_id, value)
    with pytest.raises(PolicyExisting) as exception_info:
        policy_helper.add_policies(policy_id, value)
    assert str(exception_info.value) == '409: Policy Already Exists'


def test_add_policies_twice_with_same_name(db):
    model = model_helper.add_model(model_id=uuid4().hex)
    model_id = next(iter(model))
    policy_name=uuid4().hex
    value = {
        "name": policy_name,
        "model_id": model_id,
        "genre": "authz",
        "description": "test",
    }
    policy_helper.add_policies(value=value)
    with pytest.raises(Exception) as exception_info:
        policy_helper.add_policies(value=value)
    assert str(exception_info.value) == '409: Policy Already Exists'
    assert str(exception_info.value.description)== 'Policy name Existed'


def test_delete_policies(db):
    model = model_helper.add_model(model_id=uuid4().hex)
    model_id = next(iter(model))
    policy_name1 = uuid4().hex
    value = {
        "name": policy_name1,
        "model_id": model_id,
        "genre": "authz",
        "description": "test",
    }
    policies = policy_helper.add_policies(value=value)
    policy_id1 = list(policies.keys())[0]
    policy_name2 = uuid4().hex
    value = {
        "name": policy_name2,
        "model_id": model_id,
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
        "model_id": policies[policy_id]['model_id'],
        "genre": "authz",
        "description": "test-3",
    }
    updated_policy = policy_helper.update_policy(policy_id, value)
    assert updated_policy
    for key in ("genre", "name", "model_id", "description"):
        assert key in updated_policy[policy_id]
        assert updated_policy[policy_id][key] == value[key]


def test_update_policy_name_with_existed_one(db):
    policies = policy_helper.add_policies()
    policy_id1 = list(policies.keys())[0]
    policy_name = uuid4().hex
    value = {
        "name": policy_name,
        "model_id": policies[policy_id1]['model_id'],
        "genre": "authz",
        "description": "test-3",
    }
    policy_helper.add_policies(value=value)
    with pytest.raises(PolicyExisting) as exception_info:
        policy_helper.update_policy(policy_id=policy_id1,value=value)

    assert str(exception_info.value) == '409: Policy Already Exists'
    assert str(exception_info.value.description)== 'Policy name Existed'


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
    assert str(exception_info.value) == '400: Policy Unknown'


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

    policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id)

    policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id)
    rules = policy_helper.get_rules(policy_id=policy_id, meta_rule_id=meta_rule_id)
    assert isinstance(rules, dict)
    assert rules
    obj = rules.get('rules')
    assert len(obj) == 2


def test_get_rules_with_invalid_policy_id_failure(db):
    rules = policy_helper.get_rules("invalid_policy_id", "meta_rule_id")
    assert not rules.get('meta_rule-id')
    assert len(rules.get('rules')) == 0


def test_add_rule_existing(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id = mock_data.create_subject_data(policy_id=policy_id,
                                                    category_id=subject_category_id)
    object_data_id = mock_data.create_object_data(policy_id=policy_id,
                                                  category_id=object_category_id)
    action_data_id = mock_data.create_action_data(policy_id=policy_id,
                                                  category_id=action_category_id)

    value = {
        "rule": (subject_data_id, object_data_id, action_data_id),
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

    with pytest.raises(RuleExisting) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '409: Rule Existing'


def test_check_existing_rule_valid_request(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id = mock_data.create_subject_data(policy_id=policy_id,
                                                    category_id=subject_category_id)
    object_data_id = mock_data.create_object_data(policy_id=policy_id,
                                                  category_id=object_category_id)
    action_data_id = mock_data.create_action_data(policy_id=policy_id,
                                                  category_id=action_category_id)
    value = {
        "rule": (subject_data_id, object_data_id, action_data_id),
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

    with pytest.raises(RuleExisting) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '409: Rule Existing'


def test_check_existing_rule_valid_multiple__data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id1 = mock_data.create_subject_data(policy_id=policy_id,
                                                     category_id=subject_category_id)
    subject_data_id2 = mock_data.create_subject_data(policy_id=policy_id,
                                                     category_id=subject_category_id)
    object_data_id1 = mock_data.create_object_data(policy_id=policy_id,
                                                   category_id=object_category_id)
    object_data_id2 = mock_data.create_object_data(policy_id=policy_id,
                                                   category_id=object_category_id)
    action_data_id1 = mock_data.create_action_data(policy_id=policy_id,
                                                   category_id=action_category_id)
    action_data_id2 = mock_data.create_action_data(policy_id=policy_id,
                                                   category_id=action_category_id)
    value = {
        "rule": (
            subject_data_id1, object_data_id2, action_data_id1),
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

    with pytest.raises(RuleExisting) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '409: Rule Existing'


def test_check_existing_rule_missing_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id = mock_data.create_subject_data(policy_id=policy_id,
                                                    category_id=subject_category_id)
    object_data_id = mock_data.create_object_data(policy_id=policy_id,
                                                  category_id=object_category_id)
    action_data_id = mock_data.create_action_data(policy_id=policy_id,
                                                  category_id=action_category_id)
    value = {
        "rule": (object_data_id, action_data_id),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }

    with pytest.raises(RuleContentError) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '400: Rule Error'
    assert exception_info.value.description== "Missing Data"


def test_check_existing_rule_meta_rule_missing_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id = mock_data.create_subject_data(policy_id=policy_id,
                                                    category_id=subject_category_id)
    object_data_id = mock_data.create_object_data(policy_id=policy_id,
                                                  category_id=object_category_id)
    action_data_id = mock_data.create_action_data(policy_id=policy_id,
                                                  category_id=action_category_id)
    value = {
        "rule": (subject_data_id, object_data_id, action_data_id, action_data_id),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }

    with pytest.raises(MetaRuleContentError) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '400: Meta Rule Error'
    assert exception_info.value.description == "Missing Data"


def test_check_existing_rule_invalid_data_id_order(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id = mock_data.create_subject_data(policy_id=policy_id,
                                                    category_id=subject_category_id)
    object_data_id = mock_data.create_object_data(policy_id=policy_id,
                                                  category_id=object_category_id)
    action_data_id = mock_data.create_action_data(policy_id=policy_id,
                                                  category_id=action_category_id)
    value = {
        "rule": (object_data_id, action_data_id, subject_data_id),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }

    with pytest.raises(RuleContentError) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '400: Rule Error'
    assert "Missing Subject_category" in exception_info.value.description


def test_check_existing_rule_invalid_data_id_order_scenrio_2(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id = mock_data.create_subject_data(policy_id=policy_id,
                                                    category_id=subject_category_id)
    object_data_id = mock_data.create_object_data(policy_id=policy_id,
                                                  category_id=object_category_id)
    action_data_id = mock_data.create_action_data(policy_id=policy_id,
                                                  category_id=action_category_id)
    value = {
        "rule": (subject_data_id, action_data_id, object_data_id),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }

    with pytest.raises(RuleContentError) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '400: Rule Error'
    assert "Missing Object_category" in exception_info.value.description


def test_check_existing_rule_wrong_subject_data_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id = mock_data.create_subject_data(policy_id=policy_id,
                                                    category_id=subject_category_id)
    object_data_id = mock_data.create_object_data(policy_id=policy_id,
                                                  category_id=object_category_id)
    action_data_id = mock_data.create_action_data(policy_id=policy_id,
                                                  category_id=action_category_id)
    value = {
        "rule": (uuid4().hex, object_data_id, action_data_id),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }

    with pytest.raises(RuleContentError) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '400: Rule Error'
    assert "Missing Subject_category" in exception_info.value.description


def test_check_existing_rule_wrong_object_data_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id = mock_data.create_subject_data(policy_id=policy_id,
                                                    category_id=subject_category_id)
    object_data_id = mock_data.create_object_data(policy_id=policy_id,
                                                  category_id=object_category_id)
    action_data_id = mock_data.create_action_data(policy_id=policy_id,
                                                  category_id=action_category_id)
    value = {
        "rule": (subject_data_id, uuid4().hex, action_data_id),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }

    with pytest.raises(RuleContentError) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '400: Rule Error'
    assert "Missing Object_category" in exception_info.value.description


def test_check_existing_rule_wrong_action_data_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    subject_data_id = mock_data.create_subject_data(policy_id=policy_id,
                                                    category_id=subject_category_id)
    object_data_id = mock_data.create_object_data(policy_id=policy_id,
                                                  category_id=object_category_id)
    action_data_id = mock_data.create_action_data(policy_id=policy_id,
                                                  category_id=action_category_id)
    value = {
        "rule": (subject_data_id, object_data_id, uuid4().hex),
        "instructions": ({"decision": "grant"}),
        "enabled": "",
    }

    with pytest.raises(RuleContentError) as exception_info:
        policy_helper.add_rule(policy_id=policy_id, meta_rule_id=meta_rule_id, value=value)
    assert str(exception_info.value) == '400: Rule Error'
    assert "Missing Action_category" in exception_info.value.description


def test_delete_rule(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy()

    rules = policy_helper.add_rule(policy_id, meta_rule_id)
    rule_id = list(rules.keys())[0]
    policy_helper.delete_rule(policy_id, rule_id)
    rules = policy_helper.get_rules(policy_id, meta_rule_id)
    assert not rules.get('rules')


def test_delete_policies_with_pdp(db):
    policies = policy_helper.add_policies()
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
    assert str(exception_info.value) == '400: Policy With PDP Error'
    assert 'Cannot delete policy with pdp' == exception_info.value.description


def test_delete_policies_with_subject_perimeter(db):
    policies = policy_helper.add_policies()
    policy_id1 = list(policies.keys())[0]

    value = {
        "name": "testuser",
        "security_pipeline": [policy_id1],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    data_helper.add_subject(policy_id=policy_id1, value=value)
    with pytest.raises(DeletePolicyWithPerimeter) as exception_info:
        policy_helper.delete_policies(policy_id1)
    assert str(exception_info.value) == '400: Policy With Perimeter Error'
    assert 'Cannot delete policy with perimeter'== exception_info.value.description


def test_delete_policies_with_object_perimeter(db):
    policies = policy_helper.add_policies()
    policy_id1 = list(policies.keys())[0]

    value = {
        "name": "test_obj",
        "security_pipeline": [policy_id1],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    data_helper.add_object(policy_id=policy_id1, value=value)
    with pytest.raises(DeletePolicyWithPerimeter) as exception_info:
        policy_helper.delete_policies(policy_id1)
    assert str(exception_info.value) == '400: Policy With Perimeter Error'
    assert 'Cannot delete policy with perimeter'== exception_info.value.description


def test_delete_policies_with_action_perimeter(db):
    policies = policy_helper.add_policies()
    policy_id1 = list(policies.keys())[0]

    value = {
        "name": "test_act",
        "security_pipeline": [policy_id1],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    data_helper.add_action(policy_id=policy_id1, value=value)
    with pytest.raises(DeletePolicyWithPerimeter) as exception_info:
        policy_helper.delete_policies(policy_id1)
    assert '400: Policy With Perimeter Error' == str(exception_info.value)


def test_delete_policies_with_subject_assignment(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy()

    subject_id = mock_data.create_subject(policy_id)
    data_id = mock_data.create_subject_data(policy_id=policy_id, category_id=subject_category_id)
    assignment_helper.add_subject_assignment(policy_id, subject_id, subject_category_id, data_id)

    with pytest.raises(DeletePolicyWithPerimeter) as exception_info:
        policy_helper.delete_policies(policy_id)

    assert '400: Policy With Perimeter Error' == str(exception_info.value)


def test_delete_policies_with_object_assignment(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy()

    object_id = mock_data.create_object(policy_id)
    data_id = mock_data.create_object_data(policy_id=policy_id, category_id=object_category_id)
    assignment_helper.add_object_assignment(policy_id, object_id, object_category_id, data_id)

    with pytest.raises(DeletePolicyWithPerimeter) as exception_info:
        policy_helper.delete_policies(policy_id)
    assert '400: Policy With Perimeter Error' == str(exception_info.value)


def test_delete_policies_with_action_assignment(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy()

    action_id = mock_data.create_action(policy_id)
    data_id = mock_data.create_action_data(policy_id=policy_id, category_id=action_category_id)
    assignment_helper.add_action_assignment(policy_id, action_id, action_category_id, data_id)

    with pytest.raises(DeletePolicyWithPerimeter) as exception_info:
        policy_helper.delete_policies(policy_id)
    assert '400: Policy With Perimeter Error' == str(exception_info.value)


def test_delete_policies_with_subject_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy()

    data_id = mock_data.create_subject_data(policy_id=policy_id, category_id=subject_category_id)

    with pytest.raises(DeletePolicyWithData) as exception_info:
        policy_helper.delete_policies(policy_id)

    assert '400: Policy With Data Error' == str(exception_info.value)


def test_delete_policies_with_object_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy()

    data_id = mock_data.create_object_data(policy_id=policy_id, category_id=object_category_id)

    with pytest.raises(DeletePolicyWithData) as exception_info:
        policy_helper.delete_policies(policy_id)
    assert '400: Policy With Data Error' == str(exception_info.value)


def test_delete_policies_with_action_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy()

    data_id = mock_data.create_action_data(policy_id=policy_id, category_id=action_category_id)

    with pytest.raises(DeletePolicyWithData) as exception_info:
        policy_helper.delete_policies(policy_id)
    assert '400: Policy With Data Error' == str(exception_info.value)


def test_delete_policies_with_rule(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy()

    rules = policy_helper.add_rule(policy_id, meta_rule_id)

    with pytest.raises(DeletePolicyWithRules) as exception_info:
        policy_helper.delete_policies(policy_id)
    assert '400: Policy With Rule Error' == str(exception_info.value)
