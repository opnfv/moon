# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
import json
from helpers import data_builder
from uuid import uuid4
import pytest
from moon_utilities import exceptions

# subject_categories_test


def get_subject_categories():
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(meta_data, "/subject_categories", headers=auth_headers )
    subject_categories = req.data
    return req, subject_categories


def add_subject_categories(name):
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user

    data = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = hug.test.post(meta_data, "/subject_categories", body=json.dumps(data),
                        headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")})

    subject_categories = req.data
    return req, subject_categories


def delete_subject_categories(name):
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    request, subject_categories = get_subject_categories()
    for key, value in subject_categories['subject_categories'].items():
        if value['name'] == name:
            return hug.test.delete(meta_data, "/subject_categories/{}".format(key), headers=auth_headers )
    return hug.test.delete(meta_data, "/subject_categories/{}".format(name), headers=auth_headers )


def test_get_subject_categories():
    req, subject_categories = get_subject_categories()
    assert req.status == hug.HTTP_200
    assert isinstance(subject_categories, dict)
    assert "subject_categories" in subject_categories


def test_add_subject_categories():
    name = "testuser" + uuid4().hex
    req, subject_categories = add_subject_categories(name)
    assert req.status == hug.HTTP_200
    assert isinstance(subject_categories, dict)
    value = list(subject_categories["subject_categories"].values())[0]
    assert "subject_categories" in subject_categories
    assert value['name'] == name
    assert value['description'] == "description of {}".format(name)


def test_add_subject_categories_with_existed_name():
    name = uuid4().hex
    req, subject_categories = add_subject_categories(name)
    assert req.status == hug.HTTP_200
    with pytest.raises(exceptions.SubjectCategoryExisting) as exception_info:
        req, subject_categories = add_subject_categories(name)
    assert '409: Subject Category Existing' == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data['message'] == '409: Subject Category Existing'


def test_add_subject_categories_name_contain_space():
    with pytest.raises(exceptions.CategoryNameInvalid) as exception_info:
        req, subject_categories = add_subject_categories("  ")
    assert '400: Category Name Invalid' == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == '400: Category Name Invalid'


def test_add_subject_categories_with_empty_name():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, subject_categories = add_subject_categories("<a>")
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == "Key: 'name', [Forbidden characters in string]"
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)


def test_add_subject_categories_with_name_contain_space():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, subject_categories = add_subject_categories("test<z>user")
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == "Key: 'name', [Forbidden characters in string]"


def test_delete_subject_categories():
    name = "testuser" + uuid4().hex
    add_subject_categories(name)
    req = delete_subject_categories(name)
    assert req.status == hug.HTTP_200


def test_delete_subject_categories_without_id():
    with pytest.raises(exceptions.SubjectCategoryUnknown) as exception_info:
        req = delete_subject_categories(uuid4().hex)
    assert "400: Subject Category Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == "400: Subject Category Unknown"


# ---------------------------------------------------------------------------
# object_categories_test

def get_object_categories():
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(meta_data, "/object_categories", headers=auth_headers )
    object_categories = req.data
    return req, object_categories


def add_object_categories(name):
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user

    data = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = hug.test.post(meta_data, "/object_categories", body=json.dumps(data),
                        headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")} )
    object_categories = req.data
    return req, object_categories


def delete_object_categories(name):
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    request, object_categories = get_object_categories()
    for key, value in object_categories['object_categories'].items():
        if value['name'] == name:
            return hug.test.delete(meta_data, "/object_categories/{}".format(key),
                                   headers=auth_headers )
    return hug.test.delete(meta_data, "/object_categories/{}".format(name), headers=auth_headers )


def test_get_object_categories():
    req, object_categories = get_object_categories()
    assert req.status == hug.HTTP_200
    assert isinstance(object_categories, dict)
    assert "object_categories" in object_categories


def test_add_object_categories():
    name="testuser"+uuid4().hex
    req, object_categories = add_object_categories(name)
    assert req.status == hug.HTTP_200
    assert isinstance(object_categories, dict)
    value = list(object_categories["object_categories"].values())[0]
    assert "object_categories" in object_categories
    assert value['name'] == name
    assert value['description'] == "description of {}".format(name)


def test_add_object_categories_with_existed_name():
    name = uuid4().hex
    req, object_categories = add_object_categories(name)
    assert req.status == hug.HTTP_200
    with pytest.raises(exceptions.ObjectCategoryExisting) as exception_info:
        req, object_categories = add_object_categories(name)
    assert "409: Object Category Existing" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data['message'] == '409: Object Category Existing'


def test_add_object_categories_name_contain_space():
    with pytest.raises(exceptions.CategoryNameInvalid) as exception_info:
        req, subject_categories = add_object_categories(" ")
    assert "400: Category Name Invalid" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == '400: Category Name Invalid'


def test_add_object_categories_with_empty_name():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, object_categories = add_object_categories("<a>")
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == "Key: 'name', [Forbidden characters in string]"


def test_add_object_categories_with_name_contain_space():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, object_categories = add_object_categories("test<a>user")
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == "Key: 'name', [Forbidden characters in string]"


def test_delete_object_categories():
    name = uuid4().hex
    add_object_categories(name)
    req = delete_object_categories(name)
    assert req.status == hug.HTTP_200


def test_delete_object_categories_without_id():
    with pytest.raises(exceptions.ObjectCategoryUnknown) as exception_info:
        req = delete_object_categories(uuid4().hex)
    assert "400: Object Category Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == "400: Object Category Unknown"


# ---------------------------------------------------------------------------
# action_categories_test

def get_action_categories():
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(meta_data, "/action_categories", headers=auth_headers )
    action_categories = req.data
    return req, action_categories


def add_action_categories(name):
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user

    data = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = hug.test.post(meta_data, "/action_categories", body=json.dumps(data),
                        headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")} )
    action_categories = req.data
    return req, action_categories


def delete_action_categories(name):
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    request, action_categories = get_action_categories()
    for key, value in action_categories['action_categories'].items():
        if value['name'] == name:
            return hug.test.delete(meta_data, "/action_categories/{}".format(key), headers=auth_headers )
    return hug.test.delete(meta_data, "/action_categories/{}".format(name), headers=auth_headers )


def test_get_action_categories():
    req, action_categories = get_action_categories()
    assert req.status == hug.HTTP_200
    assert isinstance(action_categories, dict)
    assert "action_categories" in action_categories


def test_add_action_categories():
    name = "testuser" + uuid4().hex
    req, action_categories = add_action_categories(name)
    assert req.status == hug.HTTP_200
    assert isinstance(action_categories, dict)
    value = list(action_categories["action_categories"].values())[0]
    assert "action_categories" in action_categories
    assert value['name'] == name
    assert value['description'] == "description of {}".format(name)


def test_add_action_categories_with_existed_name():
    name = uuid4().hex
    req, action_categories = add_action_categories(name)
    assert req.status == hug.HTTP_200
    with pytest.raises(exceptions.ActionCategoryExisting) as exception_info:
        req, action_categories = add_action_categories(name)
    assert "409: Action Category Existing" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data['message'] == '409: Action Category Existing'


def test_add_action_categories_name_contain_space():
    with pytest.raises(exceptions.CategoryNameInvalid) as exception_info:
        req, subject_categories = add_action_categories("  ")
    assert "400: Category Name Invalid" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == '400: Category Name Invalid'


def test_add_action_categories_with_empty_name():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, action_categories = add_action_categories("<a>")
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == "Key: 'name', [Forbidden characters in string]"


def test_add_action_categories_with_name_contain_space():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, action_categories = add_action_categories("test<a>user")
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == "Key: 'name', [Forbidden characters in string]"


def test_delete_action_categories():
    name = "testuser" + uuid4().hex
    add_action_categories(name)
    req = delete_action_categories(name)
    assert req.status == hug.HTTP_200


def test_delete_action_categories_without_id():
    with pytest.raises(exceptions.ActionCategoryUnknown) as exception_info:
        req = delete_action_categories(uuid4().hex)
    assert "400: Action Category Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == "400: Action Category Unknown"


def test_delete_data_categories_connected_to_meta_rule():
    from moon_manager.api import meta_data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()

    with pytest.raises(exceptions.DeleteSubjectCategoryWithMetaRule) as exception_info:
        req = hug.test.delete(meta_data, "/subject_categories/{}".format(subject_category_id),
                              headers=auth_headers )
    assert "400: Subject Category With Meta Rule Error" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == '400: Subject Category With Meta Rule Error'

    with pytest.raises(exceptions.DeleteObjectCategoryWithMetaRule) as exception_info:
        req = hug.test.delete(meta_data, "/object_categories/{}".format(object_category_id), headers=auth_headers)
    assert "400: Object Category With Meta Rule Error" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == '400: Object Category With Meta Rule Error'

    with pytest.raises(exceptions.DeleteActionCategoryWithMetaRule) as exception_info:
        req = hug.test.delete(meta_data, "/action_categories/{}".format(action_category_id), headers=auth_headers)
    assert "400: Action Category With Meta Rule Error" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data['message'] == '400: Action Category With Meta Rule Error'
