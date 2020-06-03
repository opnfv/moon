# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import pytest
from helpers import meta_rule_helper
from helpers import policy_helper
import helpers.mock_data as mock_data
import helpers.model_helper as model_helper
from python_moonutilities.exceptions import *
from uuid import uuid4


def test_update_not_exist_meta_rule_error(db):
    # set not existing meta rule and expect to raise and error
    with pytest.raises(MetaRuleUnknown) as exception_info:
        meta_rule_helper.update_meta_rule(meta_rule_id=None)
    assert str(exception_info.value) == '400: Meta Rule Unknown'


def test_update_meta_rule_connected_with_policy_and_rule():
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

    action_category_id = mock_data.create_action_category("action_category_id2")
    subject_category_id = mock_data.create_subject_category("subject_category_id2")
    object_category_id = mock_data.create_object_category("object_category_id2")

    updated_value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    with pytest.raises(MetaRuleUpdateError) as exception_info:
        updated_meta_rule = meta_rule_helper.update_meta_rule(meta_rule_id, updated_value)
    assert str(exception_info.value) == '400: Meta_Rule Update Error'


def test_update_meta_rule_connected_with_policy(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    action_category_id = mock_data.create_action_category("action_category_id2")
    subject_category_id = mock_data.create_subject_category("subject_category_id2")
    object_category_id = mock_data.create_object_category("object_category_id2")
    value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    meta_rules = meta_rule_helper.add_meta_rule(value=value)
    assert isinstance(meta_rules, dict)
    assert meta_rules
    assert len(meta_rules) is 1
    meta_rule_id = list(meta_rules.keys())[0]
    for key in (
    "name", "description", "subject_categories", "object_categories", "action_categories"):
        assert key in meta_rules[meta_rule_id]
        assert meta_rules[meta_rule_id][key] == value[key]


def test_add_new_meta_rule_success(db):
    action_category_id = mock_data.create_action_category("action_category_id1")
    subject_category_id = mock_data.create_subject_category("subject_category_id1")
    object_category_id = mock_data.create_object_category("object_category_id1")
    value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    meta_rules = meta_rule_helper.add_meta_rule(value=value)
    assert isinstance(meta_rules, dict)
    assert meta_rules
    assert len(meta_rules) is 1
    meta_rule_id = list(meta_rules.keys())[0]
    for key in (
    "name", "description", "subject_categories", "object_categories", "action_categories"):
        assert key in meta_rules[meta_rule_id]
        assert meta_rules[meta_rule_id][key] == value[key]


def test_meta_rule_with_blank_name(db):
    action_category_id = mock_data.create_action_category(uuid4().hex)
    subject_category_id = mock_data.create_subject_category(uuid4().hex)
    object_category_id = mock_data.create_object_category(uuid4().hex)
    value = {
        "name": "",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    with pytest.raises(MetaRuleContentError) as exception_info:
        meta_rule_helper.add_meta_rule(value=value)
    assert str(exception_info.value) == '400: Meta Rule Error'


def test_update_meta_rule_success(db):
    # arrange
    meta_rules = meta_rule_helper.add_meta_rule()
    meta_rule_id = list(meta_rules.keys())[0]
    action_category_id = mock_data.create_action_category("action_category_id2")
    subject_category_id = mock_data.create_subject_category("subject_category_id2")
    object_category_id = mock_data.create_object_category("object_category_id2")
    updated_value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    # action
    updated_meta_rule = meta_rule_helper.update_meta_rule(meta_rule_id, updated_value)
    # assert
    updated_meta_rule_id = list(updated_meta_rule.keys())[0]
    assert updated_meta_rule_id == meta_rule_id
    assert updated_meta_rule[updated_meta_rule_id]["subject_categories"] == updated_value[
        "subject_categories"]


def test_update_meta_rule_with_existed_categories_combination(db):
    action_category_id1 = mock_data.create_action_category(uuid4().hex)
    subject_category_id1 = mock_data.create_subject_category(uuid4().hex)
    object_category_id1 = mock_data.create_object_category(uuid4().hex)
    meta_rule_name1=uuid4().hex
    value1 = {
        "name": meta_rule_name1,
        "description": "test",
        "subject_categories": [subject_category_id1],
        "object_categories": [object_category_id1],
        "action_categories": [action_category_id1]
    }
    meta_rules = meta_rule_helper.add_meta_rule(value=value1)

    action_category_id2 = mock_data.create_action_category(uuid4().hex)
    subject_category_id2 = mock_data.create_subject_category(uuid4().hex)
    object_category_id2 = mock_data.create_object_category(uuid4().hex)
    meta_rule_name2 = uuid4().hex
    value2 = {
        "name": meta_rule_name2,
        "description": "test",
        "subject_categories": [subject_category_id2],
        "object_categories": [object_category_id2],
        "action_categories": [action_category_id2]
    }
    meta_rules = meta_rule_helper.add_meta_rule(value=value2)
    meta_rule_id2 = list(meta_rules.keys())[0]
    value1['name']=value2['name']
    with pytest.raises(MetaRuleExisting) as exception_info:
         updated_meta_rule = meta_rule_helper.update_meta_rule(meta_rule_id2, value1)
    assert str(exception_info.value) == '409: Meta Rule Existing'
    assert exception_info.value.description=="Same categories combination existed"


def test_update_meta_rule_with_different_categories_combination_but_same_data(db):
    action_category_id1 = mock_data.create_action_category(uuid4().hex)
    subject_category_id1 = mock_data.create_subject_category(uuid4().hex)
    object_category_id1 = mock_data.create_object_category(uuid4().hex)
    meta_rule_name1=uuid4().hex
    value1 = {
        "name": meta_rule_name1,
        "description": "test",
        "subject_categories": [subject_category_id1],
        "object_categories": [object_category_id1],
        "action_categories": [action_category_id1]
    }
    meta_rules = meta_rule_helper.add_meta_rule(value=value1)

    action_category_id2 = mock_data.create_action_category(uuid4().hex)
    subject_category_id2 = mock_data.create_subject_category(uuid4().hex)
    object_category_id2 = mock_data.create_object_category(uuid4().hex)
    meta_rule_name2 = uuid4().hex
    value2 = {
        "name": meta_rule_name2,
        "description": "test",
        "subject_categories": [subject_category_id2],
        "object_categories": [object_category_id2],
        "action_categories": [action_category_id2]
    }
    meta_rules = meta_rule_helper.add_meta_rule(value=value2)
    meta_rule_id2 = list(meta_rules.keys())[0]
    value1['name']=value2['name']
    value1['object_categories']+=[object_category_id1]
    updated_meta_rule = meta_rule_helper.update_meta_rule(meta_rule_id2, value1)
    assert meta_rule_id2 in updated_meta_rule


def test_add_existing_meta_rule_error(db):
    action_category_id = mock_data.create_action_category("action_category_id3")
    subject_category_id = mock_data.create_subject_category("subject_category_id3")
    object_category_id = mock_data.create_object_category("object_category_id3")
    value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    meta_rules = meta_rule_helper.add_meta_rule(value=value)
    meta_rule_id = list(meta_rules.keys())[0]
    with pytest.raises(MetaRuleExisting) as exception_info:
        meta_rule_helper.add_meta_rule(meta_rule_id=meta_rule_id)
    assert str(exception_info.value) == '409: Meta Rule Existing'


def test_add_meta_rule_with_existing_name_error(db):
    action_category_id = mock_data.create_action_category(uuid4().hex)
    subject_category_id = mock_data.create_subject_category(uuid4().hex)
    object_category_id = mock_data.create_object_category(uuid4().hex)
    name = uuid4().hex
    value = {
        "name": name,
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    meta_rule_helper.add_meta_rule(value=value)
    action_category_id = mock_data.create_action_category(uuid4().hex)
    subject_category_id = mock_data.create_subject_category(uuid4().hex)
    object_category_id = mock_data.create_object_category(uuid4().hex)
    value = {
        "name": name,
        "description": 'test',
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    with pytest.raises(MetaRuleExisting) as exception_info:
        meta_rule_helper.add_meta_rule(value=value)
    assert str(exception_info.value) == '409: Meta Rule Existing'
    assert exception_info.value.description == 'The meta rule already exists.'


def test_add_meta_rule_with_existing_categories_combination(db):
    action_category_id = mock_data.create_action_category(uuid4().hex)
    subject_category_id = mock_data.create_subject_category(uuid4().hex)
    object_category_id = mock_data.create_object_category(uuid4().hex)
    name = uuid4().hex
    value = {
        "name": name,
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    meta_rule_helper.add_meta_rule(value=value)
    value['name'] = uuid4().hex
    with pytest.raises(MetaRuleExisting) as exception_info:
        meta_rule_helper.add_meta_rule(value=value)
    assert str(exception_info.value) == '409: Meta Rule Existing'
    assert exception_info.value.description == "Same categories combination existed"


def test_add_meta_rule_with_different_categories_combination_but_same_data(db):
    action_category_id = mock_data.create_action_category(uuid4().hex)
    subject_category_id = mock_data.create_subject_category(uuid4().hex)
    object_category_id1 = mock_data.create_object_category(uuid4().hex)
    object_category_id2 = mock_data.create_object_category(uuid4().hex)

    name1 = uuid4().hex
    value = {
        "name": name1,
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id1],
        "action_categories": [action_category_id]
    }
    meta_rule_helper.add_meta_rule(value=value)
    name2 = uuid4().hex
    value['name'] = name2
    value['object_categories'] += [object_category_id2]
    meta_rules = meta_rule_helper.add_meta_rule(value=value)
    bool_found_meta_rule = 0
    for meta_rule_id in meta_rules:
        if meta_rules[meta_rule_id]['name'] == name2:
            bool_found_meta_rule = 1
            break
    assert bool_found_meta_rule


def test_get_meta_rule_success(db):
    # arrange
    action_category_id = mock_data.create_action_category("action_type")
    subject_category_id = mock_data.create_subject_category("user_security_level")
    object_category_id = mock_data.create_object_category("vm_security_level")
    values = {}
    value1 = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    meta_rules1 = meta_rule_helper.add_meta_rule(value=value1)
    meta_rule_id1 = list(meta_rules1.keys())[0]
    values[meta_rule_id1] = value1
    action_category_id = mock_data.create_action_category("action_type2")
    subject_category_id = mock_data.create_subject_category("user_security_level2")
    object_category_id = mock_data.create_object_category("vm_security_level2")
    value2 = {
        "name": "rbac_meta_rule",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    meta_rules2 = meta_rule_helper.add_meta_rule(value=value2)
    meta_rule_id2 = list(meta_rules2.keys())[0]
    values[meta_rule_id2] = value2

    # action
    meta_rules = meta_rule_helper.get_meta_rules()
    # assert
    assert isinstance(meta_rules, dict)
    assert meta_rules
    assert len(meta_rules) is 2
    for meta_rule_id in meta_rules:
        for key in (
        "name", "description", "subject_categories", "object_categories", "action_categories"):
            assert key in meta_rules[meta_rule_id]
            assert meta_rules[meta_rule_id][key] == values[meta_rule_id][key]


def test_get_specific_meta_rule_success(db):
    # arrange
    added_meta_rules = meta_rule_helper.add_meta_rule()
    added_meta_rule_id = list(added_meta_rules.keys())[0]
    # action
    meta_rules = meta_rule_helper.get_meta_rules(meta_rule_id=added_meta_rule_id)
    meta_rule_id = list(meta_rules.keys())[0]
    # assert
    assert meta_rule_id == added_meta_rule_id
    for key in (
    "name", "description", "subject_categories", "object_categories", "action_categories"):
        assert key in meta_rules[meta_rule_id]
        assert meta_rules[meta_rule_id][key] == added_meta_rules[added_meta_rule_id][key]


def test_delete_meta_rules_success(db):
    action_category_id = mock_data.create_action_category("action_type")
    subject_category_id = mock_data.create_subject_category("user_security_level")
    object_category_id = mock_data.create_object_category("vm_security_level")
    # arrange
    value1 = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    meta_rules1 = meta_rule_helper.add_meta_rule(value=value1)
    meta_rule_id1 = list(meta_rules1.keys())[0]

    # action
    meta_rule_helper.delete_meta_rules(meta_rule_id1)
    # assert
    meta_rules = meta_rule_helper.get_meta_rules()
    assert meta_rule_id1 not in meta_rules


def test_delete_meta_rules_with_model(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy()

    with pytest.raises(DeleteMetaRuleWithModel) as exception_info:
        meta_rule_helper.delete_meta_rules(meta_rule_id)
    assert str(exception_info.value) == '400: Meta rule With Model Error'


def test_delete_invalid_meta_rules_error(db):
    with pytest.raises(MetaRuleUnknown) as exception_info:
        meta_rule_helper.delete_meta_rules("INVALID_META_RULE_ID")
    assert str(exception_info.value) == '400: Meta Rule Unknown'
