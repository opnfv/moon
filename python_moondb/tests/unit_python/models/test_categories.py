import pytest
import logging
from python_moonutilities.exceptions import *

logger = logging.getLogger("moon.db.tests.models.test_categories")


def add_subject_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_subject_category(user_id=None, category_id=cat_id, value=value)
    return category


def test_add_subject_category_twice():
    category = add_subject_category(value={"name":"category name", "description":"description 1"})
    category_id = list(category.keys())[0]
    assert category is not None
    with pytest.raises(SubjectCategoryExisting):
        add_subject_category(category_id, value={"name":"category name", "description":"description 2"})


def get_subject_category(cat_id=None):
    from python_moondb.core import ModelManager
    category = ModelManager.get_subject_categories(user_id=None, category_id=cat_id)
    return category


def test_get_subject_categories():
    added_category = add_subject_category(value={"name":"category name", "description":"description 1"})
    category_id = list(added_category.keys())[0]
    subject_category = get_subject_category(category_id)
    assert subject_category == added_category


def test_get_subject_categories_with_invalid_id():
    category_id = "invalid_id"
    subject_category = get_subject_category(category_id)
    assert len(subject_category) == 0


def add_object_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_object_category(user_id=None, category_id=cat_id, value=value)
    return category


def test_add_object_category_twice():
    category = add_object_category(value={"name":"category name", "description":"description 1"})
    category_id = list(category.keys())[0]
    assert category is not None
    with pytest.raises(ObjectCategoryExisting):
        add_object_category(category_id, value={"name":"category name", "description":"description 2"})


def get_object_category(cat_id=None):
    from python_moondb.core import ModelManager
    category = ModelManager.get_object_categories(user_id=None, category_id=cat_id)
    return category


def test_get_object_categories():
    added_category = add_object_category(value={"name":"category name", "description":"description 1"})
    category_id = list(added_category.keys())[0]
    object_category = get_object_category(category_id)
    assert object_category == added_category


def test_get_object_categories_with_invalid_id():
    category_id = "invalid_id"
    object_category = get_object_category(category_id)
    assert len(object_category) == 0


def add_action_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_action_category(user_id=None, category_id=cat_id, value=value)
    return category


def test_add_action_category_twice():
    category = add_action_category(value={"name":"category name", "description":"description 1"})
    category_id = list(category.keys())[0]
    assert category is not None
    with pytest.raises(ActionCategoryExisting):
        add_action_category(category_id, value={"name":"category name", "description":"description 2"})


def get_action_category(cat_id=None):
    from python_moondb.core import ModelManager
    category = ModelManager.get_action_categories(user_id=None, category_id=cat_id)
    return category


def test_get_action_categories():
    added_category = add_action_category(value={"name":"category name", "description":"description 1"})
    category_id = list(added_category.keys())[0]
    action_category = get_action_category(category_id)
    assert action_category == added_category


def test_get_action_categories_with_invalid_id():
    category_id = "invalid_id"
    action_category = get_action_category(category_id)
    assert len(action_category) == 0