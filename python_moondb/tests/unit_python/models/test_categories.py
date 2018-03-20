# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from .test_meta_rules import *
import policies.mock_data as mock_data
import policies.test_data as test_data

logger = logging.getLogger("moon.db.tests.models.test_categories")


def add_subject_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_subject_category(user_id=None, category_id=cat_id, value=value)
    return category


def test_add_subject_category_twice():
    category = add_subject_category(value={"name": "category name", "description": "description 1"})
    category_id = list(category.keys())[0]
    assert category is not None
    with pytest.raises(SubjectCategoryExisting):
        add_subject_category(category_id, value={"name": "category name", "description": "description 2"})


def test_add_subject_category_twice_with_same_name():
    category = add_subject_category(value={"name": "category name", "description": "description 1"})
    assert category is not None
    with pytest.raises(SubjectCategoryExisting):
        add_subject_category(value={"name": "category name", "description": "description 2"})


def get_subject_category(cat_id=None):
    from python_moondb.core import ModelManager
    category = ModelManager.get_subject_categories(user_id=None, category_id=cat_id)
    return category


def test_get_subject_categories():
    added_category = add_subject_category(value={"name": "category name", "description": "description 1"})
    category_id = list(added_category.keys())[0]
    subject_category = get_subject_category(category_id)
    assert subject_category == added_category


def test_get_subject_categories_with_invalid_id():
    category_id = "invalid_id"
    subject_category = get_subject_category(category_id)
    assert len(subject_category) == 0
    category = add_subject_category(value={"name": "category name", "description": "description 1"})
    assert category is not None
    with pytest.raises(SubjectCategoryExisting):
        add_subject_category(value={"name": "category name", "description": "description 2"})


def delete_subject_category(cat_id=None):
    from python_moondb.core import ModelManager
    ModelManager.delete_subject_category(user_id=None, category_id=cat_id)


def test_delete_subject_category(db):
    category = add_subject_category(value={"name": "category name", "description": "description 1"})
    delete_subject_category(list(category.keys())[0])


def test_delete_subject_category_with_invalid_id(db):
    with pytest.raises(SubjectCategoryUnknown) as exception_info:
        delete_subject_category(-1)


def test_delete_subject_category_with_meta_rule(db):
    category = add_subject_category(value={"name": "category name", "description": "description 1"})
    subject_category_id = list(category.keys())[0]
    value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": [subject_category_id],
        "object_categories": ["vm_security_level_id_1"],
        "action_categories": ["action_type_id_1"]
    }
    add_meta_rule(value=value)
    with pytest.raises(DeleteCategoryWithMetaRule):
        delete_subject_category(subject_category_id)


def test_delete_subject_category_with_data(db):
    category = add_subject_category(value={"name": "category name", "description": "description 1"})
    subject_category_id = list(category.keys())[0]
    policy_id = mock_data.get_policy_id()
    data_id = "data_id_1"
    category_id = subject_category_id
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    test_data.add_subject_data(policy_id, data_id, category_id, value)
    with pytest.raises(DeleteCategoryWithData):
        delete_subject_category(subject_category_id)


def add_object_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_object_category(user_id=None, category_id=cat_id, value=value)
    return category


def test_add_object_category_twice():
    category = add_object_category(value={"name": "category name", "description": "description 1"})
    category_id = list(category.keys())[0]
    assert category is not None
    with pytest.raises(ObjectCategoryExisting):
        add_object_category(category_id, value={"name": "category name", "description": "description 2"})


def test_add_object_category_twice_with_same_name():
    category = add_object_category(value={"name": "category name", "description": "description 1"})
    assert category is not None
    with pytest.raises(ObjectCategoryExisting):
        add_object_category(value={"name": "category name", "description": "description 2"})


def get_object_category(cat_id=None):
    from python_moondb.core import ModelManager
    category = ModelManager.get_object_categories(user_id=None, category_id=cat_id)
    return category


def test_get_object_categories():
    added_category = add_object_category(value={"name": "category name", "description": "description 1"})
    category_id = list(added_category.keys())[0]
    object_category = get_object_category(category_id)
    assert object_category == added_category


def test_get_object_categories_with_invalid_id():
    category_id = "invalid_id"
    object_category = get_object_category(category_id)
    assert len(object_category) == 0
    category = add_object_category(value={"name": "category name", "description": "description 1"})
    assert category is not None
    with pytest.raises(ObjectCategoryExisting):
        add_object_category(value={"name": "category name", "description": "description 2"})


def delete_object_category(cat_id=None):
    from python_moondb.core import ModelManager
    ModelManager.delete_object_category(user_id=None, category_id=cat_id)


def test_delete_object_category(db):
    category = add_object_category(value={"name": "category name", "description": "description 1"})
    delete_object_category(list(category.keys())[0])


def test_delete_object_category_with_invalid_id(db):
    with pytest.raises(ObjectCategoryUnknown) as exception_info:
        delete_object_category(-1)


def test_delete_object_category_with_meta_rule(db):
    category = add_object_category(value={"name": "category name", "description": "description 1"})
    object_category_id = list(category.keys())[0]
    value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": ["subject_id_1"],
        "object_categories": [object_category_id],
        "action_categories": ["action_type_id_1"]
    }
    add_meta_rule(value=value)
    with pytest.raises(DeleteCategoryWithMetaRule):
        delete_object_category(object_category_id)


def test_delete_object_category_with_data(db):
    policy_id = mock_data.get_policy_id()
    category = add_object_category(value={"name": "category name", "description": "description 1"})
    object_category_id = list(category.keys())[0]
    data_id = "data_id_1"
    category_id = object_category_id
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    test_data.add_object_data(policy_id, data_id, category_id, value)
    with pytest.raises(DeleteCategoryWithData):
        delete_object_category(object_category_id)


def add_action_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_action_category(user_id=None, category_id=cat_id, value=value)
    return category


def test_add_action_category_twice():
    category = add_action_category(value={"name": "category name", "description": "description 1"})
    category_id = list(category.keys())[0]
    assert category is not None
    with pytest.raises(ActionCategoryExisting):
        add_action_category(category_id, value={"name": "category name", "description": "description 2"})


def test_add_action_category_twice_with_same_name():
    category = add_action_category(value={"name": "category name", "description": "description 1"})
    assert category is not None
    with pytest.raises(ActionCategoryExisting):
        add_action_category(value={"name": "category name", "description": "description 2"})


def get_action_category(cat_id=None):
    from python_moondb.core import ModelManager
    category = ModelManager.get_action_categories(user_id=None, category_id=cat_id)
    return category


def test_get_action_categories():
    added_category = add_action_category(value={"name": "category name", "description": "description 1"})
    category_id = list(added_category.keys())[0]
    action_category = get_action_category(category_id)
    assert action_category == added_category


def test_get_action_categories_with_invalid_id():
    category_id = "invalid_id"
    action_category = get_action_category(category_id)
    assert len(action_category) == 0
    category = add_action_category(value={"name": "category name", "description": "description 1"})
    assert category is not None
    with pytest.raises(ActionCategoryExisting):
        add_action_category(value={"name": "category name", "description": "description 2"})


def delete_action_category(cat_id=None):
    from python_moondb.core import ModelManager
    ModelManager.delete_action_category(user_id=None, category_id=cat_id)


def test_delete_action_category(db):
    category = add_action_category(value={"name": "category name", "description": "description 1"})
    delete_action_category(list(category.keys())[0])


def test_delete_action_category_with_invalid_id(db):
    with pytest.raises(ActionCategoryUnknown) as exception_info:
        delete_action_category(-1)


def test_delete_action_category_with_meta_rule(db):
    category = add_action_category(value={"name": "category name", "description": "description 1"})
    action_category_id = list(category.keys())[0]
    value = {
        "name": "MLS_meta_rule",
        "description": "test",
        "subject_categories": ["subject_id_1"],
        "object_categories": ["vm_security_level_id_1"],
        "action_categories": [action_category_id]
    }
    add_meta_rule(value=value)
    with pytest.raises(DeleteCategoryWithMetaRule):
        delete_action_category(action_category_id)


def test_delete_action_category_with_data(db):
    category = add_action_category(value={"name": "category name", "description": "description 1"})
    action_category_id = list(category.keys())[0]
    policy_id = mock_data.get_policy_id()
    data_id = "data_id_1"
    category_id = action_category_id
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    test_data.add_action_data(policy_id, data_id, category_id, value)
    with pytest.raises(DeleteCategoryWithData):
        delete_action_category(action_category_id)