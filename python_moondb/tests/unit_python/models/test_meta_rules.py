# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import pytest
from helpers import meta_rule_helper
import helpers.mock_data as mock_data


def test_set_not_exist_meta_rule_error(db):
    # set not existing meta rule and expect to raise and error
    with pytest.raises(Exception) as exception_info:
        meta_rule_helper.set_meta_rule(meta_rule_id=None)
    assert str(exception_info.value) == '400: Meta Rule Unknown'


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
    for key in ("name", "description", "subject_categories", "object_categories", "action_categories"):
        assert key in meta_rules[meta_rule_id]
        assert meta_rules[meta_rule_id][key] == value[key]


def test_set_meta_rule_success(db):
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
    updated_meta_rule = meta_rule_helper.set_meta_rule(meta_rule_id, updated_value)
    # assert
    updated_meta_rule_id = list(updated_meta_rule.keys())[0]
    assert updated_meta_rule_id == meta_rule_id
    assert updated_meta_rule[updated_meta_rule_id]["subject_categories"] == updated_value["subject_categories"]


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
    with pytest.raises(Exception) as exception_info:
        meta_rule_helper.add_meta_rule(meta_rule_id=meta_rule_id)
    assert str(exception_info.value) == '400: Sub Meta Rule Existing'


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
        for key in ("name", "description", "subject_categories", "object_categories", "action_categories"):
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
    for key in ("name", "description", "subject_categories", "object_categories", "action_categories"):
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


def test_delete_invalid_meta_rules_error(db):
    with pytest.raises(Exception) as exception_info:
        meta_rule_helper.delete_meta_rules("INVALID_META_RULE_ID")
    assert str(exception_info.value) == '400: Meta Rule Unknown'
