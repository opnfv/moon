# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import pytest
from python_moonutilities.exceptions import *
import logging
import policies.test_policies as test_policies

logger = logging.getLogger("moon.db.tests.test_model")


def get_models(model_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.get_models(user_id=None, model_id=model_id)


def add_model(model_id=None, value=None):
    from python_moondb.core import ModelManager
    if not value:
        name = "MLS" if model_id is None else "MLS " + model_id
        value = {
            "name": name,
            "description": "test",
            "meta_rules": "meta_rule_mls_1"
        }
    return ModelManager.add_model(user_id=None, model_id=model_id, value=value)


def delete_models(uuid=None, name=None):
    from python_moondb.core import ModelManager
    if not uuid:
        for model_id, model_value in get_models():
            if name == model_value['name']:
                uuid = model_id
                break
    ModelManager.delete_model(user_id=None, model_id=uuid)


def delete_all_models():
    from python_moondb.core import ModelManager
    models_values = get_models()
    print(models_values)
    for model_id, model_value in models_values.items():
        ModelManager.delete_model(user_id=None, model_id=model_id)


def update_model(model_id=None, value=None):
    from python_moondb.core import ModelManager
    return ModelManager.update_model(user_id=None, model_id=model_id, value=value)


def test_get_models_empty(db):
    # act
    models = get_models()
    # assert
    assert isinstance(models, dict)
    assert not models


def test_get_model(db):
    # prepare
    add_model(model_id="mls_model_id")
    # act
    models = get_models()
    # assert
    assert isinstance(models, dict)
    assert models  # assert model is not empty
    assert len(models) is 1
    delete_all_models()


def test_get_specific_model(db):
    # prepare
    add_model(model_id="mls_model_id")
    add_model(model_id="rbac_model_id")
    # act
    models = get_models(model_id="mls_model_id")
    # assert
    assert isinstance(models, dict)
    assert models  # assert model is not empty
    assert len(models) is 1
    delete_all_models()


def test_add_model(db):
    # act
    model = add_model()
    # assert
    assert isinstance(model, dict)
    assert model  # assert model is not empty
    assert len(model) is 1
    delete_all_models()


def test_add_same_model_twice(db):
    # prepare
    add_model(model_id="model_1")  # add model twice
    # act
    with pytest.raises(ModelExisting) as exception_info:
        add_model(model_id="model_1")
    delete_all_models()
    # assert str(exception_info.value) == '409: Model Error'


def test_add_model_generate_new_uuid(db):
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": "meta_rule_mls_1"
    }
    model1 = add_model(value=model_value1)

    model_value2 = {
        "name": "rbac",
        "description": "test",
        "meta_rules": "meta_rule_mls_2"
    }
    model2 = add_model(value=model_value2)

    assert list(model1)[0] != list(model2)[0]
    delete_all_models()


def test_add_models(db):
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": "meta_rule_mls_1"
    }
    models = add_model(value=model_value1)
    assert isinstance(models, dict)
    assert models
    assert len(models.keys()) == 1
    model_id = list(models.keys())[0]
    for key in ("name", "meta_rules", "description"):
        assert key in models[model_id]
        assert models[model_id][key] == model_value1[key]
    delete_all_models()


def test_delete_models(db):
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": "meta_rule_mls_1"
    }
    model1 = add_model(value=model_value1)

    model_value2 = {
        "name": "rbac",
        "description": "test",
        "meta_rules": "meta_rule_mls_2"
    }
    model2 = add_model(value=model_value2)

    id = list(model1)[0]
    delete_models(id)
    # assert
    models = get_models()
    assert id not in models
    delete_all_models()


def test_update_model(db):
    # prepare
    model_value = {
        "name": "MLS",
        "description": "test",
        "meta_rules": "meta_rule_mls_1"
    }
    model = add_model(value=model_value)
    model_id = list(model)[0]
    new_model_value = {
        "name": "MLS2",
        "description": "test",
        "meta_rules": "meta_rule_mls_2"
    }
    # act
    update_model(model_id=model_id, value=new_model_value)
    # assert
    model = get_models(model_id)

    for key in ("name", "meta_rules", "description"):
        assert key in model[model_id]
        assert model[model_id][key] == new_model_value[key]
    delete_all_models()


def test_delete_model_assigned_to_policy(db):
    model_value1 = {
        "name": "MLS",
        "description": "test",
        "meta_rules": "meta_rule_mls_1"
    }
    models = add_model(value=model_value1)
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
    test_policies.add_policies(value=value)
    with pytest.raises(DeleteModelWithPolicy) as exception_info:
        delete_models(uuid=model_id)
