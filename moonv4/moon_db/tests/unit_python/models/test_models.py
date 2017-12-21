import pytest
from moon_utilities import exceptions


def get_models(model_id=None):
    from moon_db.core import ModelManager
    return ModelManager.get_models(user_id= None , model_id= model_id)


def add_model(model_id=None, value=None):
    from moon_db.core import ModelManager
    if not value:
        value = {
            "name": "MLS",
            "description": "test",
            "meta_rules": "meta_rule_mls_1"
        }
    return ModelManager.add_model(user_id=None, model_id=model_id, value=value)


def delete_models(uuid=None, name=None):
    from moon_db.core import ModelManager
    if not uuid:
        for model_id, model_value in get_models():
            if name == model_value['name']:
                uuid = model_id
                break
    ModelManager.delete_model(user_id=None, model_id=uuid)


def update_model(model_id=None, value=None):
    from moon_db.core import ModelManager
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


def test_add_model(db):
    # act
    model = add_model()
    # assert
    assert isinstance(model, dict)
    assert model  # assert model is not empty
    assert len(model) is 1


def test_add_same_model_twice(db):
    # prepare
    add_model(model_id="model_1")  # add model twice
    # act
    with pytest.raises(exceptions.ModelExisting) as e_info:
        add_model(model_id="model_1")


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
        "name": "MLS",
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
