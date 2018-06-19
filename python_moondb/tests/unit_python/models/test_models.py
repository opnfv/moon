# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import pytest
from python_moonutilities.exceptions import *
import logging
import helpers.mock_data as mock_data
import helpers.model_helper as model_helper
import helpers.category_helper as category_helper
import helpers.policy_helper as policy_helper

logger = logging.getLogger("moon.db.tests.test_model")


def test_get_models_empty(db):
    # act
    models = model_helper.get_models()
    # assert
    assert isinstance(models, dict)
    assert not models


def test_get_model(db):
    # prepare
    model_helper.add_model(model_id="mls_model_id")
    # act
    models = model_helper.get_models()
    # assert
    assert isinstance(models, dict)
    assert models  # assert model is not empty
    assert len(models) is 1
    model_helper.delete_all_models()


def test_get_specific_model(db):
    # prepare
    model_helper.add_model(model_id="mls_model_id")
    # act
    models = model_helper.get_models(model_id="mls_model_id")
    # assert
    assert isinstance(models, dict)
    assert models  # assert model is not empty
    assert len(models) is 1
    model_helper.delete_all_models()


def test_add_model(db):
    # act
    model = model_helper.add_model()
    # assert
    assert isinstance(model, dict)
    assert model  # assert model is not empty
    assert len(model) is 1
    model_helper.delete_all_models()


def test_add_same_model_twice(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id = mock_data.create_new_meta_rule(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "model1",
        "description": "test",
        "meta_rules": [meta_rule_id]
    }
    # prepare
    model_helper.add_model(model_id="model_1", value=value)  # add model twice
    # act
    subject_category_id, object_category_id, action_category_id, meta_rule_id = mock_data.create_new_meta_rule(
        subject_category_name="subject_category2",
        object_category_name="object_category2",
        action_category_name="action_category2",
        meta_rule_name="meta_rule_2")
    value = {
        "name": "model2",
        "description": "test",
        "meta_rules": [meta_rule_id]
    }
    with pytest.raises(ModelExisting) as exception_info:
        model_helper.add_model(model_id="model_1", value=value)
    model_helper.delete_all_models()
    # assert str(exception_info.value) == '409: Model Error'


def test_add_model_generate_new_uuid(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id1 = mock_data.create_new_meta_rule(
        subject_category_name="subject_category3",
        object_category_name="object_category3",
        action_category_name="action_category3",
        meta_rule_name="meta_rule_3")
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": [meta_rule_id1]
    }
    model1 = model_helper.add_model(value=model_value1)
    subject_category_id, object_category_id, action_category_id, meta_rule_id2 = mock_data.create_new_meta_rule(
        subject_category_name="subject_category4",
        object_category_name="object_category4",
        action_category_name="action_category4",
        meta_rule_name="meta_rule_4")
    model_value2 = {
        "name": "rbac",
        "description": "test",
        "meta_rules": [meta_rule_id2]
    }
    model2 = model_helper.add_model(value=model_value2)

    assert list(model1)[0] != list(model2)[0]
    model_helper.delete_all_models()


def test_add_models(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id = mock_data.create_new_meta_rule(
        subject_category_name="subject_category5",
        object_category_name="object_category5",
        action_category_name="action_category5")
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": [meta_rule_id]
    }
    models = model_helper.add_model(value=model_value1)
    assert isinstance(models, dict)
    assert models
    assert len(models.keys()) == 1
    model_id = list(models.keys())[0]
    for key in ("name", "meta_rules", "description"):
        assert key in models[model_id]
        assert models[model_id][key] == model_value1[key]
    model_helper.delete_all_models()


def test_add_models_with_same_name_twice(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id = mock_data.create_new_meta_rule(
        subject_category_name="subject_category5",
        object_category_name="object_category5",
        action_category_name="action_category5")
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": [meta_rule_id]
    }
    models = model_helper.add_model(value=model_value1)
    assert isinstance(models, dict)
    assert models
    with pytest.raises(Exception) as exc_info:
        model_helper.add_model(value=model_value1)
    model_helper.delete_all_models()


def test_delete_models(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id1 = mock_data.create_new_meta_rule(
        subject_category_name="subject_category6",
        object_category_name="object_category6",
        action_category_name="action_category6",
        meta_rule_name="meta_rule_6")
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": [meta_rule_id1]
    }
    model1 = model_helper.add_model(value=model_value1)
    subject_category_id, object_category_id, action_category_id, meta_rule_id2 = mock_data.create_new_meta_rule(
        subject_category_name="subject_category7",
        object_category_name="object_category7",
        action_category_name="action_category7",
        meta_rule_name="meta_rule_7")
    model_value2 = {
        "name": "rbac",
        "description": "test",
        "meta_rules": [meta_rule_id2]
    }
    model_helper.add_model(value=model_value2)

    id = list(model1)[0]
    model_helper.delete_models(id)
    # assert
    models = model_helper.get_models()
    assert id not in models
    model_helper.delete_all_models()


def test_update_model(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id1 = mock_data.create_new_meta_rule(
        subject_category_name="subject_category8",
        object_category_name="object_category8",
        action_category_name="action_category8",
        meta_rule_name="meta_rule_8")
    # prepare
    model_value = {
        "name": "MLS",
        "description": "test",
        "meta_rules": [meta_rule_id1]
    }
    model = model_helper.add_model(value=model_value)
    model_id = list(model)[0]
    subject_category_id, object_category_id, action_category_id, meta_rule_id2 = mock_data.create_new_meta_rule(
        subject_category_name="subject_category9",
        object_category_name="object_category9",
        action_category_name="action_category9",
        meta_rule_name="meta_rule_9")
    new_model_value = {
        "name": "MLS2",
        "description": "test",
        "meta_rules": [meta_rule_id2]
    }
    # act
    model_helper.update_model(model_id=model_id, value=new_model_value)
    # assert
    model = model_helper.get_models(model_id)

    for key in ("name", "meta_rules", "description"):
        assert key in model[model_id]
        assert model[model_id][key] == new_model_value[key]
    model_helper.delete_all_models()


def test_delete_model_assigned_to_policy(db):
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": []
    }
    models = model_helper.add_model(value=model_value1)
    assert isinstance(models, dict)
    assert models
    assert len(models.keys()) == 1
    model_id = list(models.keys())[0]
    value = {
        "name": "test_policy",
        "model_id": model_id,
        "genre": "authz",
        "description": "test",
    }
    policy_helper.add_policies(value=value)
    with pytest.raises(DeleteModelWithPolicy) as exception_info:
        model_helper.delete_models(uuid=model_id)


def test_add_subject_category(db):
    category_id = "category_id1"
    value = {
        "name": "subject_category",
        "description": "description subject_category"
    }
    subject_category = category_helper.add_subject_category(category_id, value)
    assert subject_category
    assert len(subject_category) == 1


def test_add_subject_category_with_empty_name(db):
    category_id = "category_id1"
    value = {
        "name": "",
        "description": "description subject_category"
    }
    with pytest.raises(Exception) as exception_info:
        category_helper.add_subject_category(category_id, value)
    assert str(exception_info.value) == '400: Category Name Invalid'


def test_add_subject_category_with_same_category_id(db):
    category_id = "category_id1"
    value = {
        "name": "subject_category",
        "description": "description subject_category"
    }
    category_helper.add_subject_category(category_id, value)
    with pytest.raises(Exception) as exception_info:
        category_helper.add_subject_category(category_id, value)
    assert str(exception_info.value) == '409: Subject Category Existing'


def test_get_subject_category(db):
    category_id = "category_id1"
    value = {
        "name": "subject_category",
        "description": "description subject_category"
    }
    category_helper.add_subject_category(category_id, value)
    subject_category = category_helper.get_subject_category(category_id)
    assert subject_category
    assert len(subject_category) == 1


def test_delete_subject_category(db):
    category_id = "category_id1"
    value = {
        "name": "subject_category",
        "description": "description subject_category"
    }
    category_helper.add_subject_category(category_id, value)
    subject_category = category_helper.delete_subject_category(category_id)
    assert not subject_category


def test_delete_subject_category_with_unkown_category_id(db):
    category_id = "invalid_category_id"

    with pytest.raises(Exception) as exception_info:
        category_helper.delete_subject_category(category_id)
    assert str(exception_info.value) == '400: Subject Category Unknown'


def test_add_object_category(db):
    category_id = "category_id1"
    value = {
        "name": "object_category",
        "description": "description object_category"
    }
    object_category = category_helper.add_object_category(category_id, value)
    assert object_category
    assert len(object_category) == 1


def test_add_object_category_with_same_category_id(db):
    category_id = "category_id1"
    value = {
        "name": "object_category",
        "description": "description object_category"
    }
    category_helper.add_object_category(category_id, value)
    with pytest.raises(Exception) as exception_info:
        category_helper.add_object_category(category_id, value)
    assert str(exception_info.value) == '409: Object Category Existing'


def test_add_object_category_with_empty_name(db):
    category_id = "category_id1"
    value = {
        "name": "",
        "description": "description object_category"
    }
    with pytest.raises(Exception) as exception_info:
        category_helper.add_object_category(category_id, value)
    assert str(exception_info.value) == '400: Category Name Invalid'


def test_get_object_category(db):
    category_id = "category_id1"
    value = {
        "name": "object_category",
        "description": "description object_category"
    }
    category_helper.add_object_category(category_id, value)
    object_category = category_helper.get_object_category(category_id)
    assert object_category
    assert len(object_category) == 1


def test_delete_object_category(db):
    category_id = "category_id1"
    value = {
        "name": "object_category",
        "description": "description object_category"
    }
    category_helper.add_object_category(category_id, value)
    object_category = category_helper.delete_object_category(category_id)
    assert not object_category


def test_delete_object_category_with_unkown_category_id(db):
    category_id = "invalid_category_id"

    with pytest.raises(Exception) as exception_info:
        category_helper.delete_object_category(category_id)
    assert str(exception_info.value) == '400: Object Category Unknown'


def test_add_action_category(db):
    category_id = "category_id1"
    value = {
        "name": "action_category",
        "description": "description action_category"
    }
    action_category = category_helper.add_action_category(category_id, value)
    assert action_category
    assert len(action_category) == 1


def test_add_action_category_with_same_category_id(db):
    category_id = "category_id1"
    value = {
        "name": "action_category",
        "description": "description action_category"
    }
    category_helper.add_action_category(category_id, value)
    with pytest.raises(Exception) as exception_info:
        category_helper.add_action_category(category_id, value)
    assert str(exception_info.value) == '409: Action Category Existing'


def test_add_action_category_with_empty_name(db):
    category_id = "category_id1"
    value = {
        "name": "",
        "description": "description action_category"
    }
    with pytest.raises(Exception) as exception_info:
        category_helper.add_action_category(category_id, value)
    assert str(exception_info.value) == '400: Category Name Invalid'


def test_get_action_category(db):
    category_id = "category_id1"
    value = {
        "name": "action_category",
        "description": "description action_category"
    }
    category_helper.add_action_category(category_id, value)
    action_category = category_helper.get_action_category(category_id)
    assert action_category
    assert len(action_category) == 1


def test_delete_action_category(db):
    category_id = "category_id1"
    value = {
        "name": "action_category",
        "description": "description action_category"
    }
    category_helper.add_action_category(category_id, value)
    action_category = category_helper.delete_action_category(category_id)
    assert not action_category


def test_delete_action_category_with_unkown_category_id(db):
    category_id = "invalid_category_id"

    with pytest.raises(Exception) as exception_info:
        category_helper.delete_action_category(category_id)
    assert str(exception_info.value) == '400: Action Category Unknown'
