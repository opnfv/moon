# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import json
from uuid import uuid4

import hug
import pytest
from helpers import data_builder as builder
from helpers import policy_helper
from moon_utilities import exceptions


# subject_categories_test


def get_subject_data(policy_id, category_id=None):
    from moon_manager.api import data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    if category_id is None:
        req = hug.test.get(data, "/policies/{}/subject_data".format(policy_id), headers=auth_headers)
    else:
        req = hug.test.get(data, "/policies/{}/subject_data/{}".format(policy_id, category_id), headers=auth_headers)
    subject_data = req.data
    return req, subject_data


def add_subject_data(name):
    from moon_manager.api import data
    from moon_utilities.auth_functions import get_api_key_for_user

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex)
    body = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = hug.test.post(data, "/policies/{}/subject_data/{}".format(policy_id, subject_category_id),
                        body=json.dumps(body),
                        headers={'Content-Type': 'application/json', "X-Api-Key": get_api_key_for_user("admin")})
    subject_data = req.data
    return req, subject_data


def delete_subject_data(policy_id, category_id, data_id):
    from moon_manager.api import data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.delete(data, "/policies/{}/subject_data/{}/{}".format(policy_id, category_id,
                                                                         data_id), headers=auth_headers)
    return req


def test_get_subject_data():
    policy = policy_helper.add_policies()
    policy_id = next(iter(policy))
    req, subject_data = get_subject_data(policy_id)
    assert req.status == hug.HTTP_200
    assert isinstance(subject_data, dict)
    assert "subject_data" in subject_data


def test_add_subject_data():
    req, subject_data = add_subject_data("testuser")
    assert req.status == hug.HTTP_200
    assert isinstance(subject_data, dict)
    value = subject_data["subject_data"]['data']
    assert "subject_data" in subject_data
    id = list(value.keys())[0]
    assert value[id]['name'] == "testuser"
    assert value[id]['description'] == "description of {}".format("testuser")


def test_add_subject_data_invalid_name():
    with pytest.raises(exceptions.DataContentError) as exception_info:
        req, subject_data = add_subject_data("  ")
        # assert req.status == hug.HTTP_400
    assert '400: Data Content Error' == str(exception_info.value)
    with pytest.raises(exceptions.DataContentError) as exception_info:
        req, subject_data = add_subject_data("")
        # assert req.status == hug.HTTP_400
    assert '400: Data Content Error' == str(exception_info.value)


def test_delete_subject_data():
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy()
    data_id = builder.create_subject_data(policy_id, subject_category_id)
    success_req = delete_subject_data(policy_id, subject_category_id, data_id)
    assert success_req.status == hug.HTTP_200


def test_add_subject_data_with_forbidden_char_in_user():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, subject_data = add_subject_data("<a>")
    # assert '400: Invalid Content' == str(exception_info.value)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
    # assert req.status == hug.HTTP_400
    # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_delete_subject_data_without_policy_id():
    success_req = delete_subject_data("", "", "")
    assert success_req.status == hug.HTTP_405


# ---------------------------------------------------------------------------
# object_categories_test


def get_object_data(policy_id, category_id=None):
    from moon_manager.api import data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    if category_id is None:
        req = hug.test.get(data, "/policies/{}/object_data".format(policy_id), headers=auth_headers)
    else:
        req = hug.test.get(data, "/policies/{}/object_data/{}".format(policy_id, category_id), headers=auth_headers)
    object_data = req.data
    return req, object_data


def add_object_data(name):
    from moon_manager.api import data
    from moon_utilities.auth_functions import get_api_key_for_user

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex)
    body = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = hug.test.post(data, "/policies/{}/object_data/{}".format(policy_id, object_category_id),
                        body=json.dumps(body), headers={'Content-Type': 'application/json',
                                                        "X-Api-Key": get_api_key_for_user("admin")})
    object_data = req.data
    return req, object_data


def delete_object_data(policy_id, category_id, data_id):
    from moon_manager.api import data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.delete(data, "/policies/{}/object_data/{}/{}".format(policy_id, category_id,
                                                                        data_id), headers=auth_headers)
    return req


def test_get_object_data():
    policy = policy_helper.add_policies()
    policy_id = next(iter(policy))
    req, object_data = get_object_data(policy_id)
    assert req.status == hug.HTTP_200
    assert isinstance(object_data, dict)
    assert "object_data" in object_data


def test_add_object_data():
    req, object_data = add_object_data("testuser")
    assert req.status == hug.HTTP_200
    assert isinstance(object_data, dict)
    value = object_data["object_data"]['data']
    assert "object_data" in object_data
    _id = list(value.keys())[0]
    assert value[_id]['name'] == "testuser"
    assert value[_id]['description'] == "description of {}".format("testuser")


def test_add_object_data_invalid_name():
    with pytest.raises(exceptions.DataContentError) as exception_info:
        req, object_data = add_object_data(" ")
        # assert req.status == hug.HTTP_400
    assert '400: Data Content Error' == str(exception_info.value)
    with pytest.raises(exceptions.DataContentError):
        req, object_data = add_object_data("")
        # assert req.status == hug.HTTP_400
    assert '400: Data Content Error' == str(exception_info.value)


def test_delete_object_data():
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy()
    data_id = builder.create_object_data(policy_id, object_category_id)
    success_req = delete_object_data(policy_id, data_id, object_category_id)
    assert success_req.status == hug.HTTP_200


def test_add_object_data_with_forbidden_char_in_user():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, subject_data = add_object_data("<a>")
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"
    # assert '400: Invalid Content' == str(exception_info.value)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)


def test_delete_object_data_without_policy_id():
    success_req = delete_object_data("", "", "")
    assert success_req.status == hug.HTTP_405


# ---------------------------------------------------------------------------
# action_categories_test


def get_action_data(policy_id, category_id=None):
    from moon_manager.api import data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    if category_id is None:
        req = hug.test.get(data, "/policies/{}/action_data".format(policy_id),
                           headers=auth_headers)
    else:
        req = hug.test.get(data, "/policies/{}/action_data/{}".format(policy_id, category_id),
                           headers=auth_headers)
    action_data = req.data
    return req, action_data


def add_action_data(name):
    from moon_manager.api import data
    from moon_utilities.auth_functions import get_api_key_for_user

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex)
    body = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = hug.test.post(data, "/policies/{}/action_data/{}".format(policy_id, action_category_id),
                        body=json.dumps(body),
                        headers={'Content-Type': 'application/json',
                                 "X-Api-Key": get_api_key_for_user("admin")})
    action_data = req.data
    return req, action_data


def delete_action_data(policy_id, categorgy_id, data_id):
    from moon_manager.api import data
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.delete(data, "/policies/{}/action_data/{}/{}".format(policy_id, categorgy_id,
                                                                        data_id), headers=auth_headers)
    return req


def test_get_action_data():
    policy = policy_helper.add_policies()
    policy_id = next(iter(policy))
    req, action_data = get_action_data(policy_id)
    assert req.status == hug.HTTP_200
    assert isinstance(action_data, dict)
    assert "action_data" in action_data


def test_add_action_data():
    req, action_data = add_action_data("testuser")
    assert req.status == hug.HTTP_200
    assert isinstance(action_data, dict)
    value = action_data["action_data"]['data']
    assert "action_data" in action_data
    id = list(value.keys())[0]
    assert value[id]['name'] == "testuser"
    assert value[id]['description'] == "description of {}".format("testuser")


def test_add_action_data_invalid_name():

    with pytest.raises(exceptions.DataContentError)as exception_info:
        req, action_data = add_action_data(" ")
        # assert req.status == hug.HTTP_400
    assert '400: Data Content Error' == str(exception_info.value)
    with pytest.raises(exceptions.DataContentError) as exception_info:
        req, action_data = add_action_data("")
        # assert req.status == hug.HTTP_400
    assert '400: Data Content Error' == str(exception_info.value)


def test_delete_action_data():
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy()
    data_id = builder.create_action_data(policy_id, action_category_id)
    success_req = delete_action_data(policy_id, data_id, action_category_id)
    assert success_req.status == hug.HTTP_200


def test_add_action_data_with_forbidden_char_in_user():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, action_data = add_action_data("<a>")
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"
    # assert '400: Invalid Content' == str(exception_info.value)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)


def test_delete_action_data_without_policy_id():
    success_req = delete_action_data("", "", "")
    assert success_req.status == hug.HTTP_405
# ---------------------------------------------------------------------------
