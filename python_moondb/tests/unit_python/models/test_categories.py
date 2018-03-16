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
    assert category is not None
    with pytest.raises(SubjectCategoryExisting):
        add_subject_category(value={"name":"category name", "description":"description 2"})


def add_object_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_object_category(user_id=None, category_id=cat_id, value=value)
    return category


def test_add_object_category_twice():
    category = add_object_category(value={"name":"category name", "description":"description 1"})
    assert category is not None
    with pytest.raises(ObjectCategoryExisting):
        add_object_category(value={"name":"category name", "description":"description 2"})


def add_action_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_action_category(user_id=None, category_id=cat_id, value=value)
    return category


def test_add_action_category_twice():
    category = add_action_category(value={"name":"category name", "description":"description 1"})
    assert category is not None
    with pytest.raises(ActionCategoryExisting):
        add_action_category(value={"name":"category name", "description":"description 2"})
