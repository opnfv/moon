import pytest
from python_moonutilities.exceptions import *
import logging
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


def add_subject_category(user_id, category_id=None, value=None):
    from python_moondb.core import ModelManager
    return ModelManager.add_subject_category("", category_id=category_id, value=value)


def get_subject_category(user_id, category_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.get_subject_categories("", category_id=category_id)


def delete_subject_category(user_id, category_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.delete_subject_category("", category_id=category_id)


def add_object_category(user_id, category_id=None, value=None):
    from python_moondb.core import ModelManager
    return ModelManager.add_object_category("", category_id=category_id, value=value)


def get_object_category(user_id, category_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.get_object_categories("", category_id=category_id)


def delete_object_category(user_id, category_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.delete_object_category("", category_id=category_id)


def add_action_category(user_id, category_id=None, value=None):
    from python_moondb.core import ModelManager
    return ModelManager.add_action_category("", category_id=category_id, value=value)


def get_action_category(user_id, category_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.get_action_categories("", category_id=category_id)


def delete_action_category(user_id, category_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.delete_action_category("", category_id=category_id)


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
    #assert str(exception_info.value) == '409: Model Error'


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


def test_add_subject_category(db):
    category_id = "category_id1"
    value = {
        "name": "subject_category",
        "description": "description subject_category"
    }
    subject_category = add_subject_category("", category_id, value)
    assert subject_category
    assert len(subject_category) == 1


def test_add_subject_category_with_empty_name(db):
    category_id = "category_id1"
    value = {
        "name": "",
        "description": "description subject_category"
    }
    with pytest.raises(Exception) as exception_info:
        add_subject_category("", category_id, value)
    assert str(exception_info.value) == '409: Category Name Invalid'



def test_add_subject_category_with_same_category_id(db):
    category_id = "category_id1"
    value = {
        "name": "subject_category",
        "description": "description subject_category"
    }
    add_subject_category("", category_id, value)
    with pytest.raises(Exception) as exception_info:
        add_subject_category("", category_id, value)
    assert str(exception_info.value) == '409: Subject Category Existing'


def test_get_subject_category(db):
    category_id = "category_id1"
    value = {
        "name": "subject_category",
        "description": "description subject_category"
    }
    add_subject_category("", category_id, value)
    subject_category = get_subject_category("", category_id)
    assert subject_category
    assert len(subject_category) == 1


def test_delete_subject_category(db):
    category_id = "category_id1"
    value = {
        "name": "subject_category",
        "description": "description subject_category"
    }
    add_subject_category("", category_id, value)
    subject_category = delete_subject_category("", category_id)
    assert not subject_category


def test_delete_subject_category_with_unkown_category_id(db):
    category_id = "invalid_category_id"

    with pytest.raises(Exception) as exception_info:
        delete_subject_category("", category_id)
    assert str(exception_info.value) == '400: Subject Category Unknown'


def test_add_object_category(db):
    category_id = "category_id1"
    value = {
        "name": "object_category",
        "description": "description object_category"
    }
    object_category = add_object_category("", category_id, value)
    assert object_category
    assert len(object_category) == 1


def test_add_object_category_with_same_category_id(db):
    category_id = "category_id1"
    value = {
        "name": "object_category",
        "description": "description object_category"
    }
    add_object_category("", category_id, value)
    with pytest.raises(Exception) as exception_info:
        add_object_category("", category_id, value)
    assert str(exception_info.value) == '409: Object Category Existing'


def test_add_object_category_with_empty_name(db):
    category_id = "category_id1"
    value = {
        "name": "",
        "description": "description object_category"
    }
    with pytest.raises(Exception) as exception_info:
        add_object_category("", category_id, value)
    assert str(exception_info.value) == '409: Category Name Invalid'


def test_get_object_category(db):
    category_id = "category_id1"
    value = {
        "name": "object_category",
        "description": "description object_category"
    }
    add_object_category("", category_id, value)
    object_category = get_object_category("", category_id)
    assert object_category
    assert len(object_category) == 1


def test_delete_object_category(db):
    category_id = "category_id1"
    value = {
        "name": "object_category",
        "description": "description object_category"
    }
    add_object_category("", category_id, value)
    object_category = delete_object_category("", category_id)
    assert not object_category


def test_delete_object_category_with_unkown_category_id(db):
    category_id = "invalid_category_id"

    with pytest.raises(Exception) as exception_info:
        delete_object_category("", category_id)
    assert str(exception_info.value) == '400: Object Category Unknown'

def test_add_action_category(db):
    category_id = "category_id1"
    value = {
        "name": "action_category",
        "description": "description action_category"
    }
    action_category = add_action_category("", category_id, value)
    assert action_category
    assert len(action_category) == 1


def test_add_action_category_with_same_category_id(db):
    category_id = "category_id1"
    value = {
        "name": "action_category",
        "description": "description action_category"
    }
    add_action_category("", category_id, value)
    with pytest.raises(Exception) as exception_info:
        add_action_category("", category_id, value)
    assert str(exception_info.value) == '409: Action Category Existing'


def test_add_action_category_with_empty_name(db):
    category_id = "category_id1"
    value = {
        "name": "",
        "description": "description action_category"
    }
    with pytest.raises(Exception) as exception_info:
        add_action_category("", category_id, value)
    assert str(exception_info.value) == '409: Category Name Invalid'


def test_get_action_category(db):
    category_id = "category_id1"
    value = {
        "name": "action_category",
        "description": "description action_category"
    }
    add_action_category("", category_id, value)
    action_category = get_action_category("", category_id)
    assert action_category
    assert len(action_category) == 1


def test_delete_action_category(db):
    category_id = "category_id1"
    value = {
        "name": "action_category",
        "description": "description action_category"
    }
    add_action_category("", category_id, value)
    action_category = delete_action_category("", category_id)
    assert not action_category


def test_delete_action_category_with_unkown_category_id(db):
    category_id = "invalid_category_id"

    with pytest.raises(Exception) as exception_info:
        delete_action_category("", category_id)
    assert str(exception_info.value) == '400: Action Category Unknown'
