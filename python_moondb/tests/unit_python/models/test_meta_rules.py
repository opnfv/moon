# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from .test_models import *


def set_meta_rule(meta_rule_id, value=None):
    from python_moondb.core import ModelManager
    if not value:
        value = {
            "name": "MLS_meta_rule",
            "description": "test",
            "subject_categories": ["user_security_level_id_1"],
            "object_categories": ["vm_security_level_id_1"],
            "action_categories": ["action_type_id_1"]
        }
    return ModelManager.set_meta_rule(user_id=None, meta_rule_id=meta_rule_id, value=value)


def add_meta_rule(meta_rule_id=None, value=None):
    from python_moondb.core import ModelManager
    if not value:
        value = {
            "name": "MLS_meta_rule",
            "description": "test",
            "subject_categories": ["user_security_level_id_1"],
            "object_categories": ["vm_security_level_id_1"],
            "action_categories": ["action_type_id_1"]
        }
    return ModelManager.add_meta_rule(user_id=None, meta_rule_id=meta_rule_id, value=value)


def get_meta_rules(meta_rule_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.get_meta_rules(user_id=None, meta_rule_id=meta_rule_id)


def delete_meta_rules(meta_rule_id=None):
    from python_moondb.core import ModelManager
    ModelManager.delete_meta_rule(user_id=None, meta_rule_id=meta_rule_id)

def test_set_not_exist_meta_rule_error(db):
    # set not existing meta rule and expect to raise and error
    with pytest.raises(Exception) as exception_info:
        set_meta_rule(meta_rule_id=None)
    assert str(exception_info.value) == '400: Sub Meta Rule Unknown'


def test_add_new_meta_rule_success(db):
    value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": ["user_security_level_id_1"],
        "object_categories": ["vm_security_level_id_1"],
        "action_categories": ["action_type_id_1"]
    }
    metaRules = add_meta_rule()
    assert isinstance(metaRules, dict)
    assert metaRules
    assert len(metaRules) is 1
    meta_rule_id = list(metaRules.keys())[0]
    for key in ("name", "description", "subject_categories", "object_categories", "action_categories"):
        assert key in metaRules[meta_rule_id]
        assert metaRules[meta_rule_id][key] == value[key]


def test_set_meta_rule_succes(db):
    # arrange
    meta_rules = add_meta_rule()
    meta_rule_id = list(meta_rules.keys())[0]
    updated_value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": ["user_role_id_1"],
        "object_categories": ["vm_security_level_id_1"],
        "action_categories": ["action_type_id_1"]
    }
    # action
    updated_meta_rule = set_meta_rule(meta_rule_id, updated_value)
    # assert
    updated_meta_rule_id = list(updated_meta_rule.keys())[0]
    assert updated_meta_rule_id == meta_rule_id
    assert updated_meta_rule[updated_meta_rule_id]["subject_categories"] == \
           updated_value["subject_categories"]


def test_add_existing_meta_rule_error(db):
    meta_rules = add_meta_rule()
    meta_rule_id = list(meta_rules.keys())[0]
    with pytest.raises(Exception) as exception_info:
        add_meta_rule(meta_rule_id=meta_rule_id)
    assert str(exception_info.value) == '400: Sub Meta Rule Existing'


def test_get_meta_rule_success(db):
    # arrange
    values = {}
    value1 = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": ["user_security_level_id_1"],
        "object_categories": ["vm_security_level_id_1"],
        "action_categories": ["action_type_id_1"]
    }
    meta_rules1 = add_meta_rule(value=value1)
    meta_rule_id1 = list(meta_rules1.keys())[0]
    values[meta_rule_id1] = value1
    value2 = {
        "name": "rbac_meta_rule",
        "description": "test",
        "subject_categories": ["user_role_id_1"],
        "object_categories": ["vm_id_1"],
        "action_categories": ["action_type_id_1"]
    }
    meta_rules2 = add_meta_rule(value=value2)
    meta_rule_id2 = list(meta_rules2.keys())[0]
    values[meta_rule_id2] = value2

    # action
    meta_rules = get_meta_rules()
    # assert
    assert isinstance(meta_rules , dict)
    assert meta_rules
    assert len(meta_rules) is 2
    for meta_rule_id in meta_rules:
        for key in ("name", "description", "subject_categories", "object_categories", "action_categories"):
            assert key in meta_rules[meta_rule_id]
            assert meta_rules[meta_rule_id][key] == values[meta_rule_id][key]


def test_get_specific_meta_rule_success(db):
    # arrange
    added_meta_rules  = add_meta_rule()
    added_meta_rule_id = list(added_meta_rules.keys())[0]
    # action
    meta_rules = get_meta_rules(meta_rule_id=added_meta_rule_id)
    meta_rule_id = list(meta_rules.keys())[0]
    # assert
    assert meta_rule_id == added_meta_rule_id
    for key in ("name", "description", "subject_categories", "object_categories", "action_categories"):
        assert key in meta_rules[meta_rule_id]
        assert meta_rules[meta_rule_id][key] == added_meta_rules[added_meta_rule_id][key]


def test_delete_meta_rules_success(db):
    # arrange
    value1 = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": ["user_security_level_id_1"],
        "object_categories": ["vm_security_level_id_1"],
        "action_categories": ["action_type_id_1"]
    }
    meta_rules1 = add_meta_rule(value=value1)
    meta_rule_id1 = list(meta_rules1.keys())[0]

    value2 = {
        "name": "rbac_meta_rule",
        "description": "test",
        "subject_categories": ["user_role_id_1"],
        "object_categories": ["vm_id_1"],
        "action_categories": ["action_type_id_1"]
    }
    meta_rules2 = add_meta_rule(value=value2)
    meta_rule_id2 = list(meta_rules2.keys())[0]

    # action
    delete_meta_rules(meta_rule_id1)
    # assert
    meta_rules = get_meta_rules()
    assert meta_rule_id1 not in meta_rules


def test_delete_invalid_meta_rules_error(db):
    with pytest.raises(Exception) as exception_info:
        delete_meta_rules("INVALID_META_RULE_ID")
    assert str(exception_info.value) == '400: Sub Meta Rule Unknown'


def test_delete_meta_rule_with_assigned_model(db):
    value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": ["user_security_level_id_1"],
        "object_categories": ["vm_security_level_id_1"],
        "action_categories": ["action_type_id_1"]
    }
    metaRules = add_meta_rule()
    assert isinstance(metaRules, dict)
    assert metaRules
    assert len(metaRules) is 1
    meta_rule_id = list(metaRules.keys())[0]
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": meta_rule_id
    }
    add_model(value=model_value1)
    with pytest.raises(DeleteMetaRuleWithModel) as exception_info:
        delete_meta_rules(meta_rule_id)
