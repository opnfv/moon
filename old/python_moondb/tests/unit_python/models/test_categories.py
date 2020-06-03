# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import pytest
import logging
from python_moonutilities.exceptions import *
from helpers import category_helper

logger = logging.getLogger("moon.db.tests.models.test_categories")


def test_add_subject_category_twice():
    category = category_helper.add_subject_category(
        value={"name": "category name", "description": "description 1"})
    category_id = list(category.keys())[0]
    assert category is not None
    with pytest.raises(SubjectCategoryExisting):
        category_helper.add_subject_category(category_id,
                                             value={"name": "category name",
                                                    "description": "description 2"})


def test_add_subject_category_name_space():
    with pytest.raises(CategoryNameInvalid) as exp:
        category = category_helper.add_subject_category(value={"name": " ", "description":
            "description 1"})
    assert exp.value.code == 400
    assert exp.value.description == 'The given category name is invalid.'


def test_get_subject_categories():
    added_category = category_helper.add_subject_category(
        value={"name": "category name", "description": "description 1"})
    category_id = list(added_category.keys())[0]
    subject_category = category_helper.get_subject_category(category_id)
    assert subject_category == added_category


def test_get_subject_categories_with_invalid_id():
    category_id = "invalid_id"
    subject_category = category_helper.get_subject_category(category_id)
    assert len(subject_category) == 0


def test_add_object_category_twice():
    category = category_helper.add_object_category(
        value={"name": "category name", "description": "description 1"})
    category_id = list(category.keys())[0]
    assert category is not None
    with pytest.raises(ObjectCategoryExisting):
        category_helper.add_object_category(category_id,
                                            value={"name": "category name",
                                                   "description": "description 2"})


def test_add_object_category_name_space():
    with pytest.raises(CategoryNameInvalid) as exp:
        category = category_helper.add_object_category(value={"name": " ", "description":
            "description 1"})
    assert exp.value.code == 400
    assert exp.value.description == 'The given category name is invalid.'


def test_get_object_categories():
    added_category = category_helper.add_object_category(
        value={"name": "category name", "description": "description 1"})
    category_id = list(added_category.keys())[0]
    object_category = category_helper.get_object_category(category_id)
    assert object_category == added_category


def test_get_object_categories_with_invalid_id():
    category_id = "invalid_id"
    object_category = category_helper.get_object_category(category_id)
    assert len(object_category) == 0


def test_add_action_category_twice():
    category = category_helper.add_action_category(
        value={"name": "category name", "description": "description 1"})
    category_id = list(category.keys())[0]
    assert category is not None
    with pytest.raises(ActionCategoryExisting) as exp_info:
        category_helper.add_action_category(category_id,
                                            value={"name": "category name",
                                                   "description": "description 2"})
    assert str(exp_info.value)=='409: Action Category Existing'


def test_add_action_category_name_space():
    with pytest.raises(CategoryNameInvalid) as exp:
        category = category_helper.add_action_category(value={"name": " ", "description":
            "description 1"})
    assert exp.value.code == 400
    assert exp.value.description == 'The given category name is invalid.'


def test_get_action_categories():
    added_category = category_helper.add_action_category(
        value={"name": "category name", "description": "description 1"})
    category_id = list(added_category.keys())[0]
    action_category = category_helper.get_action_category(category_id)
    assert action_category == added_category


def test_get_action_categories_with_invalid_id():
    category_id = "invalid_id"
    action_category = category_helper.get_action_category(category_id)
    assert len(action_category) == 0
