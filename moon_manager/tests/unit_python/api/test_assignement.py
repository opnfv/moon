# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
from uuid import uuid4
import pytest
import api.utilities as utilities
from helpers import data_builder as builder
from moon_utilities import exceptions


def delete_assignment_based_on_parameters(type, policy_id, pre_id=None, cat_id=None, data_id=None):
    if type in ["subject_assignments", "object_assignments", "action_assignments"] and policy_id:
        url = "/policies/" + policy_id + "/" + type
        if pre_id:
            url += "/" + pre_id
        if cat_id:
            url += "/" + cat_id
        if data_id:
            url += "/" + data_id
    else:
        return ""
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.delete(assignments, url, headers=auth_headers)
    return req


# subject_categories_test


def get_subject_assignment(policy_id):
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(assignments, "/policies/{}/subject_assignments".format(policy_id), headers=auth_headers)
    subject_assignment = utilities.get_json(req.data)
    return req, subject_assignment


def add_subject_assignment():
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex)
    subject_id = builder.create_subject(policy_id)
    data_id = builder.create_subject_data(policy_id=policy_id, category_id=subject_category_id)

    data = {
        "id": subject_id,
        "category_id": subject_category_id,
        "data_id": data_id
    }
    req = hug.test.post(assignments, "/policies/{}/subject_assignments/".format(policy_id),
                        body=data, headers=auth_headers)
    subject_assignment = utilities.get_json(req.data)
    return req, subject_assignment


def add_subject_assignment_without_cat_id():
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    data = {
        "id": "subject_id",
        "category_id": "",
        "data_id": "data_id"
    }
    req = hug.test.post(assignments, "/policies/{}/subject_assignments".format("1111"), body=data,
                        headers=auth_headers)
    subject_assignment = utilities.get_json(req.data)
    return req, subject_assignment


def delete_subject_assignment(policy_id, sub_id, cat_id, data_id):
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.delete(assignments, "/policies/{}/subject_assignments/{}/{}/{}".format(
        policy_id, sub_id, cat_id, data_id), headers=auth_headers)
    return req


def test_add_subject_assignment():
    req, subject_assignment = add_subject_assignment()
    assert req.status == hug.HTTP_200
    assert isinstance(subject_assignment, dict)
    assert "subject_assignments" in subject_assignment


# def test_add_subject_assignment_without_cat_id():
#     client = utilities.register_client()
#     req, subject_assignment = add_subject_assignment_without_cat_id(client)
#     assert req.status == hug.HTTP_400
#     assert json.loads(req.data)["message"] == "Key: 'category_id', [Empty String]"


def test_get_subject_assignment():
    policy_id = builder.get_policy_id_with_subject_assignment()
    req, subject_assignment = get_subject_assignment(policy_id)
    assert req.status == hug.HTTP_200
    assert isinstance(subject_assignment, dict)
    assert "subject_assignments" in subject_assignment


def test_delete_subject_assignment():
    policy_id = builder.get_policy_id_with_subject_assignment()
    req, subject_assignment = get_subject_assignment(policy_id)
    value = subject_assignment["subject_assignments"]
    _id = list(value.keys())[0]
    success_req = delete_subject_assignment(
        policy_id,
        value[_id]['subject_id'],
        value[_id]['category_id'],
        value[_id]['assignments'][0])
    assert success_req.status == hug.HTTP_200


def test_delete_subject_assignment_using_policy():
    policy_id = builder.get_policy_id_with_subject_assignment()
    req, subject_assignment = get_subject_assignment(policy_id)
    value = subject_assignment["subject_assignments"]
    _id = list(value.keys())[0]
    success_req = delete_assignment_based_on_parameters(
        "subject_assignments",
        policy_id)
    assert success_req.status == hug.HTTP_200


def test_delete_subject_assignment_using_policy_perimeter_id():
    policy_id = builder.get_policy_id_with_subject_assignment()
    req, subject_assignment = get_subject_assignment(policy_id)
    value = subject_assignment["subject_assignments"]
    _id = list(value.keys())[0]
    success_req = delete_assignment_based_on_parameters(
        "subject_assignments",
        policy_id,
        value[_id]['subject_id'])
    assert success_req.status == hug.HTTP_200


def test_delete_subject_assignment_using_policy_perimeter_id_category_id():
    policy_id = builder.get_policy_id_with_subject_assignment()
    req, subject_assignment = get_subject_assignment(policy_id)
    value = subject_assignment["subject_assignments"]
    _id = list(value.keys())[0]
    success_req = delete_assignment_based_on_parameters(
        "subject_assignments",
        policy_id,
        value[_id]['subject_id'],
        value[_id]['category_id'])
    assert success_req.status == hug.HTTP_200


def test_delete_subject_assignment_without_policy_id():

    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        success_req = delete_subject_assignment("", "id1", "111", "data_id1")

    assert '400: Policy Unknown' == str(exception_info.value)

    # assert success_req.status == hug.HTTP_400
        # assert success_req.data["message"] == "400: Policy Unknown"


# ---------------------------------------------------------------------------
# object_categories_test


def get_object_assignment(policy_id):
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(assignments, "/policies/{}/object_assignments".format(policy_id), headers=auth_headers)
    object_assignment = utilities.get_json(req.data)
    return req, object_assignment


def add_object_assignment():
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex)
    object_id = builder.create_object(policy_id)
    data_id = builder.create_object_data(policy_id=policy_id, category_id=object_category_id)

    data = {
        "id": object_id,
        "category_id": object_category_id,
        "data_id": data_id
    }

    req = hug.test.post(assignments, "/policies/{}/object_assignments".format(policy_id),
                        body=data, headers=auth_headers)
    object_assignment = utilities.get_json(req.data)
    return req, object_assignment


def add_object_assignment_without_cat_id():
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    data = {
        "id": "object_id",
        "category_id": "",
        "data_id": "data_id"
    }
    req = hug.test.post(assignments, "/policies/{}/object_assignments".format("1111"),
                        body=data, headers=auth_headers)
    object_assignment = utilities.get_json(req.data)
    return req, object_assignment


def delete_object_assignment(policy_id, obj_id, cat_id, data_id):
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.delete(assignments, "/policies/{}/object_assignments/{}/{}/{}".format(
        policy_id, obj_id, cat_id, data_id), headers=auth_headers)
    return req


def test_get_object_assignment():
    policy_id = builder.get_policy_id_with_object_assignment()

    req, object_assignment = get_object_assignment(policy_id)
    assert req.status == hug.HTTP_200
    assert isinstance(object_assignment, dict)
    assert "object_assignments" in object_assignment


def test_add_object_assignment():
    req, object_assignment = add_object_assignment()
    assert req.status == hug.HTTP_200
    assert "object_assignments" in object_assignment


# def test_add_object_assignment_without_cat_id():
#     client = utilities.register_client()
#     req, object_assignment = add_object_assignment_without_cat_id(client)
#     assert req.status == hug.HTTP_400
#     assert json.loads(req.data)["message"] == "Key: 'category_id', [Empty String]"


def test_delete_object_assignment():
    policy_id = builder.get_policy_id_with_object_assignment()
    req, object_assignment = get_object_assignment(policy_id)
    value = object_assignment["object_assignments"]
    _id = list(value.keys())[0]
    success_req = delete_object_assignment(policy_id,
                                           value[_id]['object_id'],
                                           value[_id]['category_id'],
                                           value[_id]['assignments'][0])
    assert success_req.status == hug.HTTP_200


def test_delete_object_assignment_using_policy():
    policy_id = builder.get_policy_id_with_object_assignment()
    req, object_assignment = get_object_assignment(policy_id)
    value = object_assignment["object_assignments"]
    _id = list(value.keys())[0]
    success_req = delete_assignment_based_on_parameters(
        "object_assignments",
        policy_id)
    assert success_req.status == hug.HTTP_200


def test_delete_object_assignment_using_policy_perimeter_id():
    policy_id = builder.get_policy_id_with_object_assignment()
    req, object_assignment = get_object_assignment(policy_id)
    value = object_assignment["object_assignments"]
    _id = list(value.keys())[0]
    success_req = delete_assignment_based_on_parameters(
        "object_assignments",
        policy_id,
        value[_id]['object_id'])
    assert success_req.status == hug.HTTP_200


def test_delete_object_assignment_using_policy_perimeter_id_category_id():
    policy_id = builder.get_policy_id_with_object_assignment()
    req, object_assignment = get_object_assignment(policy_id)
    value = object_assignment["object_assignments"]
    _id = list(value.keys())[0]
    success_req = delete_assignment_based_on_parameters(
        "object_assignments",
        policy_id,
        value[_id]['object_id'],
        value[_id]['category_id'])
    assert success_req.status == hug.HTTP_200


def test_delete_object_assignment_without_policy_id():
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        success_req = delete_object_assignment("", "id1", "111", "data_id1")
        # assert success_req.status == hug.HTTP_400
        # assert success_req.data["message"] == "400: Policy Unknown"
    assert '400: Policy Unknown' == str(exception_info.value)


# ---------------------------------------------------------------------------
# action_categories_test


def get_action_assignment(policy_id):
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(assignments, "/policies/{}/action_assignments".format(policy_id), headers=auth_headers)
    action_assignment = utilities.get_json(req.data)
    return req, action_assignment


def add_action_assignment():
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex)
    action_id = builder.create_action(policy_id)
    data_id = builder.create_action_data(policy_id=policy_id, category_id=action_category_id)

    data = {
        "id": action_id,
        "category_id": action_category_id,
        "data_id": data_id
    }
    req = hug.test.post(assignments, "/policies/{}/action_assignments".format(policy_id),
                        body=data,
                        headers=auth_headers)
    action_assignment = utilities.get_json(req.data)
    return req, action_assignment


def add_action_assignment_without_cat_id():
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    data = {
        "id": "action_id",
        "category_id": "",
        "data_id": "data_id"
    }
    req = hug.test.post(assignments, "/policies/{}/action_assignments".format("1111"),
                        body=data, headers=auth_headers)
    action_assignment = utilities.get_json(req.data)
    return req, action_assignment


def delete_action_assignment(policy_id, action_id, cat_id, data_id):
    from moon_manager.api import assignments
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.delete(assignments, "/policies/{}/action_assignments/{}/{}/{}".format(
        policy_id, action_id, cat_id, data_id), headers=auth_headers)
    return req


def test_get_action_assignment():
    policy_id = builder.get_policy_id_with_action_assignment()
    req, action_assignment = get_action_assignment(policy_id)
    assert req.status == hug.HTTP_200
    assert isinstance(action_assignment, dict)
    assert "action_assignments" in action_assignment


def test_add_action_assignment():
    req, action_assignment = add_action_assignment()
    assert req.status == hug.HTTP_200
    assert "action_assignments" in action_assignment


# def test_add_action_assignment_without_cat_id():
#     client = utilities.register_client()
#     req, action_assignment = add_action_assignment_without_cat_id(client)
#     assert req.status == hug.HTTP_400
#     assert json.loads(req.data)["message"] == "Key: 'category_id', [Empty String]"


def test_delete_action_assignment():
    policy_id = builder.get_policy_id_with_action_assignment()
    req, action_assignment = get_action_assignment(policy_id)
    value = action_assignment["action_assignments"]
    id = list(value.keys())[0]
    success_req = delete_action_assignment(policy_id,
                                           value[id]['action_id'],
                                           value[id]['category_id'],
                                           value[id]['assignments'][0])
    assert success_req.status == hug.HTTP_200


def test_delete_action_assignment_policy():
    policy_id = builder.get_policy_id_with_action_assignment()
    req, action_assignment = get_action_assignment(policy_id)
    value = action_assignment["action_assignments"]
    id = list(value.keys())[0]
    success_req = delete_assignment_based_on_parameters(
        "action_assignments",
        policy_id)
    assert success_req.status == hug.HTTP_200


def test_delete_action_assignment_policy_perimeter_id():
    policy_id = builder.get_policy_id_with_action_assignment()
    req, action_assignment = get_action_assignment(policy_id)
    value = action_assignment["action_assignments"]
    id = list(value.keys())[0]
    success_req = delete_assignment_based_on_parameters(
        "action_assignments",
        policy_id,
        value[id]['action_id'])
    assert success_req.status == hug.HTTP_200


def test_delete_action_assignment_policy_perimeter_id_category_id():
    policy_id = builder.get_policy_id_with_action_assignment()
    req, action_assignment = get_action_assignment(policy_id)
    value = action_assignment["action_assignments"]
    id = list(value.keys())[0]
    success_req = delete_assignment_based_on_parameters(
        "action_assignments",
        policy_id,
        value[id]['action_id'],
        value[id]['category_id'])
    assert success_req.status == hug.HTTP_200


def test_delete_action_assignment_without_policy_id():
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        success_req = delete_action_assignment("", "id1", "111", "data_id1")
        # assert success_req.status == hug.HTTP_400
        # assert success_req.data["message"] == "400: Policy Unknown"
    assert '400: Policy Unknown' == str(exception_info.value)

# ---------------------------------------------------------------------------
