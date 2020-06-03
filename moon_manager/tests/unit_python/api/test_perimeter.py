# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
import api.utilities as utilities
from helpers import data_builder as builder
import helpers.policy_helper as policy_helper
from uuid import uuid4
import pytest
from moon_utilities import exceptions


def get_subjects(subject_id=None):
    from moon_manager.api import perimeter
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    if not subject_id:
        req = hug.test.get(perimeter, 'subjects/', headers=auth_headers)
    else:
        req = hug.test.get(perimeter, 'subjects/{}'.format(subject_id), headers=auth_headers)
    subjects = utilities.get_json(req.data)
    return req, subjects


def add_subjects(policy_id, name, perimeter_id=None, data=None, auth_headers=None):
    from moon_manager.api import perimeter
    if not data:
        name = name + uuid4().hex
        data = {
            "name": name,
            "description": "description of {}".format(name),
            "password": "password for {}".format(name),
            "email": "{}@moon".format(name)
        }
    if not perimeter_id:
        req = hug.test.post(perimeter, "/policies/{}/subjects".format(policy_id),
                            body=data, headers=auth_headers)
    else:
        req = hug.test.post(perimeter, "/policies/{}/subjects/{}".format(policy_id, perimeter_id),
                            body=data, headers=auth_headers)
    subjects = utilities.get_json(req.data)
    return req, subjects


def delete_subjects_without_perimeter_id(auth_headers=None):
    from moon_manager.api import perimeter
    req = hug.test.delete(perimeter, "/subjects/{}".format(""), headers=auth_headers)
    return req


def test_perimeter_get_subject():
    req, subjects = get_subjects()
    assert req.status == hug.HTTP_200
    assert isinstance(subjects, dict)
    assert "subjects" in subjects


def test_perimeter_add_subject():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    req, subjects = add_subjects(policy_id, "testuser", auth_headers=auth_headers)
    value = list(subjects["subjects"].values())[0]
    assert req.status == hug.HTTP_200
    assert value["name"]
    assert value["email"]


def test_perimeter_add_same_subject_perimeter_id_with_new_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    name = "testuser"
    perimeter_id = uuid4().hex
    data = {
        "name": name + uuid4().hex,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    add_subjects(policy_id1, data['name'], perimeter_id=perimeter_id, data=data,
                 auth_headers=auth_headers)
    policies2 = policy_helper.add_policies()
    policy_id2 = list(policies2.keys())[0]
    req, subjects = add_subjects(policy_id2, data['name'],
                                 perimeter_id=perimeter_id, data=data,
                                 auth_headers=auth_headers)
    value = list(subjects["subjects"].values())[0]
    assert req.status == hug.HTTP_200
    assert value["name"]
    assert value["email"]
    assert len(value['policy_list']) == 2
    assert policy_id1 in value['policy_list']
    assert policy_id2 in value['policy_list']


def test_perimeter_add_same_subject_perimeter_id_with_different_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    perimeter_id = uuid4().hex
    add_subjects(policy_id1, "testuser", perimeter_id=perimeter_id, auth_headers=auth_headers)
    policies2 = policy_helper.add_policies()
    policy_id2 = list(policies2.keys())[0]
    with pytest.raises(exceptions.PerimeterContentError) as exception_info:
        req, subjects = add_subjects(policy_id2, "testuser", perimeter_id=perimeter_id,
                                     auth_headers=auth_headers)
    assert "400: Perimeter content is invalid." == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Perimeter content is invalid.'


def test_perimeter_add_same_subject_name_with_new_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    perimeter_id = uuid4().hex
    name = "testuser" + uuid4().hex
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req, subjects = add_subjects(policy_id1, None, perimeter_id=perimeter_id, data=data,
                                 auth_headers=auth_headers)
    policies2 = policy_helper.add_policies()
    policy_id2 = list(policies2.keys())[0]
    value = list(subjects["subjects"].values())[0]
    data = {
        "name": value['name'],
        "description": "description of {}".format(value['name']),
        "password": "password for {}".format(value['name']),
        "email": "{}@moon".format(value['name'])
    }
    req, subjects = add_subjects(policy_id2, None, data=data, auth_headers=auth_headers)
    value = list(subjects["subjects"].values())[0]
    assert req.status == hug.HTTP_200
    assert value["name"]
    assert value["email"]
    assert len(value['policy_list']) == 2
    assert policy_id1 in value['policy_list']
    assert policy_id2 in value['policy_list']


def test_perimeter_add_same_subject_name_with_same_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    perimeter_id = uuid4().hex
    name = "testuser" + uuid4().hex
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req, subjects = add_subjects(policy_id1, None, perimeter_id=perimeter_id,
                                 data=data, auth_headers=auth_headers)
    value = list(subjects["subjects"].values())[0]
    data = {
        "name": value['name'],
        "description": "description of {}".format(value['name']),
        "password": "password for {}".format(value['name']),
        "email": "{}@moon".format(value['name'])
    }
    with pytest.raises(exceptions.PolicyExisting) as exception_info:
        req, subjects = add_subjects(policy_id1, None, data=data, auth_headers=auth_headers)
    assert "409: Policy Already Exists" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Policy Already Exists'


def test_perimeter_add_same_subject_perimeter_id_with_existed_policy_id_in_list():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    name = "testuser" + uuid4().hex
    data = {
        "name": name + uuid4().hex,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    subj_id = "b34e5a29-5494-4cc5-9356-daa244b8c254"
    req, subjects = get_subjects(subj_id)
    if subjects['subjects']:
        for __policy_id in subjects['subjects'][subj_id]['policy_list']:
            req = hug.test.delete(perimeter,
                                  "/policies/{}/subjects/{}".format(__policy_id, subj_id),
                                  headers=auth_headers)
    req, subjects = add_subjects(policy_id, name, data=data, auth_headers=auth_headers)
    perimeter_id = list(subjects["subjects"].values())[0]['id']
    with pytest.raises(exceptions.PolicyExisting) as exception_info:
        req, subjects = add_subjects(policy_id, name, perimeter_id=perimeter_id, data=data,
                                     auth_headers=auth_headers)
    assert "409: Policy Already Exists" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Policy Already Exists'


def test_perimeter_add_subject_invalid_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    name = "testuser"
    data = {
        "name": name + uuid4().hex,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req, subjects = add_subjects( policy_id + "0", "testuser", data, auth_headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Policy Unknown'


def test_perimeter_add_subject_blank_data():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    with pytest.raises(exceptions.ValidationKeyError) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/subjects".format(policy_id), body={'test':"aa"},
                            headers=auth_headers)
    assert "Invalid Key :name not found" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == 'Invalid Key :name not found'


def test_perimeter_add_subject_with_forbidden_char_in_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "<a>",
        "description": "description of {}".format(""),
        "password": "password for {}".format(""),
        "email": "{}@moon".format("")
    }
    subj_id = "a34e5a29-5494-4cc5-9356-daa244b8c888"
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/subjects".format(subj_id), body=data,
                            headers=auth_headers)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_perimeter_update_subject_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    req, subjects = add_subjects(policy_id, "testuser", auth_headers=auth_headers)
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update"
    }
    req = hug.test.patch(perimeter, "/subjects/{}".format(perimeter_id), body=data,
                         headers=auth_headers)
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["subjects"].values())[0]
    assert req.status == hug.HTTP_200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] == value2['description']


def test_perimeter_update_subject_description():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    req, subjects = add_subjects(policy_id, "testuser", auth_headers=auth_headers)
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'description': value1['description'] + "update",
    }
    req = hug.test.patch(perimeter, "/subjects/{}".format(perimeter_id), body=data,
                         headers=auth_headers)
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["subjects"].values())[0]

    assert req.status == hug.HTTP_200
    assert value1['name'] == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_subject_description_and_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    req, subjects = add_subjects(policy_id, "testuser", auth_headers=auth_headers)
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'description': value1['description'] + "update",
        'name': value1['name'] + "update"
    }
    from moon_manager.api import perimeter
    req = hug.test.patch(perimeter, "/subjects/{}".format(perimeter_id), body=data,
                         headers=auth_headers)
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["subjects"].values())[0]

    assert req.status == hug.HTTP_200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_subject_wrong_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, subjects = add_subjects(policy_id=policy_id1, name='testuser', data=data,
                                 auth_headers=auth_headers)
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    with pytest.raises(exceptions.PerimeterContentError) as exception_info:
        req = hug.test.patch(perimeter, "/subjects/{}".format(perimeter_id + "wrong"),
                             body=data, headers=auth_headers)
    assert "400: Perimeter content is invalid." == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Perimeter content is invalid.'


def test_perimeter_update_subject_name_with_existed_one():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    name1 = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    perimeter_id1 = uuid4().hex
    req, subjects = add_subjects(policy_id=policy_id1, name=name1,
                                 perimeter_id=perimeter_id1, auth_headers=auth_headers)
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id2 = uuid4().hex
    name2 = 'testuser' + uuid4().hex
    req, subjects = add_subjects(policy_id=policy_id1, name=name2,
                                 perimeter_id=perimeter_id2, auth_headers=auth_headers)
    data = {
        'name': value1['name'],
    }
    with pytest.raises(exceptions.SubjectExisting) as exception_info:
        req = hug.test.patch(perimeter, "/subjects/{}".format(perimeter_id2), body=data,
                             headers=auth_headers)
    assert "409: Subject Existing" == str(exception_info.value)
        # assert req.status == hug.HTTP_409


def test_perimeter_delete_subject():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    req, subjects = add_subjects(policy_id, "testuser", auth_headers=auth_headers)
    subject_id = list(subjects["subjects"].values())[0]["id"]
    req = hug.test.delete(perimeter, "/policies/{}/subjects/{}".format(policy_id, subject_id),
                          headers=auth_headers)
    assert req.status == hug.HTTP_200


def test_perimeter_delete_subjects_without_perimeter_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    with pytest.raises(exceptions.SubjectUnknown) as exception_info:
        req = delete_subjects_without_perimeter_id(auth_headers)
    assert "400: Subject Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Subject Unknown"


def get_objects():
    from moon_manager.api import perimeter
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(perimeter, "/objects", headers=auth_headers)
    objects = utilities.get_json(req.data)
    return req, objects


def add_objects(name, policyId=None, data=None, perimeter_id=None, auth_headers=None):
    from moon_manager.api import perimeter
    if not policyId:
        subject_category_id, object_category_id, action_category_id, meta_rule_id, policyId = builder.create_new_policy(
            subject_category_name="subject_category1" + uuid4().hex,
            object_category_name="object_category1" + uuid4().hex,
            action_category_name="action_category1" + uuid4().hex,
            meta_rule_name="meta_rule_1" + uuid4().hex,
            model_name="model1" + uuid4().hex)
    if not data:
        data = {
            "name": name + uuid4().hex,
            "description": "description of {}".format(name),
        }
    if not perimeter_id:
        req = hug.test.post(perimeter, "/policies/{}/objects/".format(policyId), body=data,
                            headers=auth_headers)
    else:
        req = hug.test.post(perimeter, "/policies/{}/objects/{}".format(policyId, perimeter_id),
                            body=data, headers=auth_headers)

    objects = utilities.get_json(req.data)
    return req, objects


def delete_objects_without_perimeter_id(auth_headers=None):
    from moon_manager.api import perimeter
    req = hug.test.delete(perimeter, "/objects/{}".format(""), headers=auth_headers)
    return req


def test_perimeter_get_object():

    req, objects = get_objects()
    assert req.status == hug.HTTP_200
    assert isinstance(objects, dict)
    assert "objects" in objects


def test_perimeter_add_object():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req, objects = add_objects("testuser", auth_headers=auth_headers)
    value = list(objects["objects"].values())[0]
    assert req.status == hug.HTTP_200
    assert value['name']


def test_perimeter_add_object_with_wrong_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req, objects = add_objects("testuser", policyId='wrong', auth_headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Policy Unknown'


def test_perimeter_add_object_with_policy_id_none():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "testuser" + uuid4().hex,
        "description": "description of {}".format("testuser"),
    }
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/objects/".format(None), body=data,
                            headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Policy Unknown'


def test_perimeter_add_same_object_name_with_new_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req, objects = add_objects("testuser", auth_headers=auth_headers)
    value1 = list(objects["objects"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects('testuser', policyId=policy_id1, data=data, auth_headers=auth_headers)
    value2 = list(objects["objects"].values())[0]
    assert req.status == hug.HTTP_200
    assert value1['id'] == value2['id']
    assert value1['name'] == value2['name']


def test_perimeter_add_same_object_perimeter_id_with_new_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req, objects = add_objects( "testuser", auth_headers=auth_headers)
    value1 = list(objects["objects"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects('testuser', policyId=policy_id1, data=data,
                               perimeter_id=value1['id'],auth_headers=auth_headers)
    value2 = list(objects["objects"].values())[0]
    assert req.status == hug.HTTP_200
    assert value1['id'] == value2['id']
    assert value1['name'] == value2['name']


def test_perimeter_add_same_object_perimeter_id_with_different_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req, objects = add_objects( "testuser", auth_headers=auth_headers)
    value1 = list(objects["objects"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'] + 'different',
        "description": "description of {}".format('testuser'),
    }
    with pytest.raises(exceptions.PerimeterContentError) as exception_info:
        req, objects = add_objects('testuser', policyId=policy_id1, data=data,
                                   perimeter_id=value1['id'], auth_headers=auth_headers)
    assert "400: Perimeter content is invalid." == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Perimeter content is invalid.'


def test_perimeter_add_same_object_name_with_same_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects('testuser', policyId=policy_id1, data=data, auth_headers=auth_headers)
    value = list(objects["objects"].values())[0]

    assert req.status == hug.HTTP_200
    with pytest.raises(exceptions.PolicyExisting) as exception_info:
        req, objects = add_objects('testuser', policyId=policy_id1, data=data, auth_headers=auth_headers)
    assert "409: Policy Already Exists" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Policy Already Exists'


def test_perimeter_add_same_object_perimeter_id_with_existed_policy_id_in_list():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects( 'testuser', policyId=policy_id1, data=data,
                                auth_headers=auth_headers)
    value = list(objects["objects"].values())[0]
    with pytest.raises(exceptions.PolicyExisting) as exception_info:
        req, objects = add_objects('testuser', policyId=policy_id1, data=data,
                                   perimeter_id=value['id'], auth_headers=auth_headers)
    assert "409: Policy Already Exists" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Policy Already Exists'


def test_perimeter_update_object_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects('testuser', policyId=policy_id1, data=data,
                               auth_headers=auth_headers)

    value1 = list(objects["objects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update"
    }
    req = hug.test.patch(perimeter, "/objects/{}".format(perimeter_id), body=data,
                         headers=auth_headers)

    objects = utilities.get_json(req.data)
    value2 = list(objects["objects"].values())[0]

    assert req.status == hug.HTTP_200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] == value2['description']


def test_perimeter_update_object_description():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects('testuser', policyId=policy_id1, data=data,
                               auth_headers=auth_headers)

    value1 = list(objects["objects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'description': value1['description'] + "update"
    }
    req = hug.test.patch(perimeter, "/objects/{}".format(perimeter_id), body=data,
                         headers=auth_headers)

    objects = utilities.get_json(req.data)
    value2 = list(objects["objects"].values())[0]

    assert req.status == hug.HTTP_200
    assert value1['name'] == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_object_description_and_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects('testuser', policyId=policy_id1, data=data,
                               auth_headers=auth_headers)

    value1 = list(objects["objects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    req = hug.test.patch(perimeter, "/objects/{}".format(perimeter_id), body=data,
                         headers=auth_headers)

    objects = utilities.get_json(req.data)
    value2 = list(objects["objects"].values())[0]
    assert req.status == hug.HTTP_200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_object_wrong_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects('testuser', policyId=policy_id1, data=data,
                               auth_headers=auth_headers)

    value1 = list(objects["objects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    with pytest.raises(exceptions.PerimeterContentError) as exception_info:
        req = hug.test.patch(perimeter, "/objects/{}".format(perimeter_id + "wrong"), body=data,
                             headers=auth_headers)
    assert "400: Perimeter content is invalid." == str(exception_info.value)
        # assert req.status == hug.HTTP_400


def test_perimeter_update_object_name_with_existed_one():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data1 = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects('testuser', policyId=policy_id1, data=data1,
                               auth_headers=auth_headers)
    value1 = list(objects["objects"].values())[0]

    name = 'testuser' + uuid4().hex

    data2 = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects('testuser', policyId=policy_id1, data=data2,
                               auth_headers=auth_headers)

    value2 = list(objects["objects"].values())[0]
    perimeter_id2 = value2['id']

    data3 = {
        'name': value1['name']
    }
    with pytest.raises(exceptions.ObjectExisting) as exception_info:
        req = hug.test.patch(perimeter, "/objects/{}".format(perimeter_id2), body=data3,
                             headers=auth_headers)
    assert "409: Object Existing" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Object Existing'


def test_perimeter_add_object_without_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "<br/>",
        "description": "description of {}".format(""),
    }
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/objects/".format(
            "a34e5a29-5494-4cc5-9356-daa244b8c888"),
                          body=data, headers=auth_headers)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_perimeter_add_object_blank_data():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    with pytest.raises(exceptions.ValidationKeyError) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/objects/".format(
            "a34e5a29-5494-4cc5-9356-daa244b8c888"),
                          body={}, headers=auth_headers)
    assert "Invalid Key :name not found" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == 'Invalid Key :name not found'


def test_perimeter_add_object_with_name_contain_spaces():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "test<a>user",
        "description": "description of {}".format("test user"),
    }
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/objects/".format(
            "a34e5a29-5494-4cc5-9356-daa244b8c888"), body=data,
                          headers=auth_headers)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_perimeter_add_object_with_name_space():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": " ",
        "description": "description of {}".format("test user"),
    }
    with pytest.raises(exceptions.PerimeterContentError) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/objects/".format(
            "a34e5a29-5494-4cc5-9356-daa244b8c888"),
                     body =data, headers=auth_headers)
    assert "400: Perimeter content is invalid." == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Perimeter content is invalid.'


def test_perimeter_delete_object():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    object_id = builder.create_object(policy_id)
    req = hug.test.delete(perimeter, "/policies/{}/objects/{}".format(policy_id, object_id), headers=auth_headers)

    assert req.status == hug.HTTP_200


def test_perimeter_delete_objects_without_perimeter_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    with pytest.raises(exceptions.ObjectUnknown) as exception_info:
        req = delete_objects_without_perimeter_id(auth_headers=auth_headers)
    assert "400: Object Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Object Unknown"


def get_actions():
    from moon_manager.api import perimeter
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(perimeter, "/actions", headers=auth_headers)
    actions = utilities.get_json(req.data)
    return req, actions


def add_actions(name, policy_id=None, data=None, perimeter_id=None, auth_headers=None):
    from moon_manager.api import perimeter
    if not policy_id:
        subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
            subject_category_name="subject_category1" + uuid4().hex,
            object_category_name="object_category1" + uuid4().hex,
            action_category_name="action_category1" + uuid4().hex,
            meta_rule_name="meta_rule_1" + uuid4().hex,
            model_name="model1" + uuid4().hex)

    if not data:
        data = {
            "name": name + uuid4().hex,
            "description": "description of {}".format(name),
        }
    if not perimeter_id:
        req = hug.test.post(perimeter, "/policies/{}/actions/".format(policy_id), body=data,
                            headers=auth_headers)
    else:
        req = hug.test.post(perimeter, "/policies/{}/actions/{}".format(policy_id, perimeter_id),
                            body=data, headers=auth_headers)

    actions = utilities.get_json(req.data)
    return req, actions


def delete_actions_without_perimeter_id(auth_headers=None):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    req = hug.test.delete(perimeter, "/actions/{}".format(""), headers=auth_headers)
    return req


def test_perimeter_get_actions():

    req, actions = get_actions()

    assert req.status == hug.HTTP_200
    assert isinstance(actions, dict)
    assert "actions" in actions


def test_perimeter_add_actions():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req, actions = add_actions("testuser", auth_headers=auth_headers)
    value = list(actions["actions"].values())[0]
    assert req.status == hug.HTTP_200
    assert value['name']


def test_perimeter_add_action_with_wrong_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req, actions = add_actions("testuser", policy_id="wrong", auth_headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Policy Unknown'


def test_perimeter_add_action_with_policy_id_none():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "testuser" + uuid4().hex,
        "description": "description of {}".format("testuser"),
    }
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/actions/".format(None), body=data,
                            headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Policy Unknown'


def test_perimeter_add_same_action_name_with_new_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req, action = add_actions("testuser", auth_headers=auth_headers)
    value1 = list(action["actions"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, action = add_actions('testuser', policy_id=policy_id1, data=data,
                              auth_headers=auth_headers)
    value2 = list(action["actions"].values())[0]
    assert req.status == hug.HTTP_200
    assert value1['id'] == value2['id']
    assert value1['name'] == value2['name']


def test_perimeter_add_same_action_perimeter_id_with_new_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req, action = add_actions("testuser", auth_headers=auth_headers)
    value1 = list(action["actions"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, action = add_actions('testuser', policy_id=policy_id1, data=data,
                              perimeter_id=value1['id'], auth_headers=auth_headers)
    value2 = list(action["actions"].values())[0]

    assert req.status == hug.HTTP_200
    assert value1['id'] == value2['id']
    assert value1['name'] == value2['name']


def test_perimeter_add_same_action_perimeter_id_with_different_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req, action = add_actions("testuser", auth_headers=auth_headers)
    value1 = list(action["actions"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'] + 'different',
        "description": "description of {}".format('testuser'),
    }
    with pytest.raises(exceptions.PerimeterContentError) as exception_info:
        req, action = add_actions('testuser', policy_id=policy_id1, data=data,
                                  perimeter_id=value1['id'], auth_headers=auth_headers)
    assert "400: Perimeter content is invalid." == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Perimeter content is invalid.'


def test_perimeter_add_same_action_name_with_same_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    req, action = add_actions("testuser", policy_id=policy_id1, auth_headers=auth_headers)
    value1 = list(action["actions"].values())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    with pytest.raises(exceptions.PolicyExisting) as exception_info:
        req, action = add_actions('testuser', policy_id=policy_id1, data=data,
                                  auth_headers=auth_headers)
    assert "409: Policy Already Exists" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Policy Already Exists'


def test_perimeter_add_same_action_perimeter_id_with_existed_policy_id_in_list():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    req, action = add_actions("testuser", policy_id=policy_id1, auth_headers=auth_headers)
    value1 = list(action["actions"].values())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    with pytest.raises(exceptions.PolicyExisting) as exception_info:
        req, action = add_actions('testuser', policy_id=policy_id1, data=data,
                                  perimeter_id=value1['id'], auth_headers=auth_headers)
    assert "409: Policy Already Exists" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Policy Already Exists'


def test_perimeter_add_actions_without_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "<a>",
        "description": "description of {}".format(""),
    }
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/actions".format(
            "a34e5a29-5494-4cc5-9356-daa244b8c888"),
                     body=data, headers=auth_headers)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_perimeter_add_actions_with_name_contain_spaces():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "test<a>user",
        "description": "description of {}".format("test user"),
    }
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/actions".format(
            "a34e5a29-5494-4cc5-9356-daa244b8c888"),
                     body=data, headers=auth_headers)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_add_subjects_without_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "testuser",
        "description": "description of {}".format("test user"),
    }
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/subjects".format(
            "a34e5a29-5494-4cc5-9356-daa244b8c888"),
                     body=data, headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Policy Unknown"


def test_add_objects_without_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "testuser",
        "description": "description of {}".format("test user"),
    }
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/objects".format(
            "a34e5a29-5494-4cc5-9356-daa244b8c888"),
                     body=data, headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Policy Unknown"


def test_add_action_without_policy_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    data = {
        "name": "testuser",
        "description": "description of {}".format("test user"),
    }
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req = hug.test.post(perimeter, "/policies/{}/actions".format(
            "a34e5a29-5494-4cc5-9356-daa244b8c888"), body=data,
                          headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Policy Unknown"


def test_perimeter_update_action_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    req, actions = add_actions("testuser", auth_headers=auth_headers)
    value1 = list(actions["actions"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update"
    }
    req = hug.test.patch(perimeter, "/actions/{}".format(perimeter_id), body=data,
                         headers=auth_headers)
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["actions"].values())[0]

    assert req.status == hug.HTTP_200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] == value2['description']


def test_perimeter_update_actions_description():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    req, actions = add_actions("testuser", auth_headers=auth_headers)
    value1 = list(actions["actions"].values())[0]
    perimeter_id = value1['id']
    data = {
        'description': value1['description'] + "update"
    }
    req = hug.test.patch(perimeter, "/actions/{}".format(perimeter_id), body=data,
                         headers=auth_headers)
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["actions"].values())[0]

    assert req.status == hug.HTTP_200
    assert value1['name'] == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_actions_description_and_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    req, actions = add_actions("testuser", auth_headers=auth_headers)
    value1 = list(actions["actions"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    req = hug.test.patch(perimeter, "/actions/{}".format(perimeter_id), body=data,
                         headers=auth_headers)
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["actions"].values())[0]

    assert req.status == hug.HTTP_200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_action_wrong_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    req, actions = add_actions("testuser", auth_headers=auth_headers)
    value1 = list(actions["actions"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    with pytest.raises(exceptions.PerimeterContentError) as exception_info:
        req = hug.test.patch(perimeter, "/actions/{}".format(perimeter_id + "wrong"), body=data,
                             headers=auth_headers)
    assert "400: Perimeter content is invalid." == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Perimeter content is invalid.'


def test_perimeter_update_action_name_with_existed_one():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    req, actions = add_actions("testuser", auth_headers=auth_headers)
    value1 = list(actions["actions"].values())[0]
    req, actions = add_actions("testuser", auth_headers=auth_headers)
    value2 = list(actions["actions"].values())[0]
    perimeter_id2 = value2['id']
    data = {
        'name': value1['name'],
    }
    with pytest.raises(exceptions.ActionExisting) as exception_info:
        req = hug.test.patch(perimeter, "/actions/{}".format(perimeter_id2), body=data,
                             headers=auth_headers)
    assert "409: Action Existing" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Action Existing'


def test_perimeter_delete_actions():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    action_id = builder.create_action(policy_id)
    req = hug.test.delete(perimeter, "/policies/{}/actions/{}".format(policy_id, action_id),
                          headers=auth_headers)


    assert req.status == hug.HTTP_200

def test_delete_subject_assigned_to_policy():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    from moon_manager.db_driver import PolicyManager

    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    subject_id = builder.create_subject(policy_id)
    PolicyManager.delete_policy(moon_user_id="admin", policy_id=policy_id)
    PolicyManager.delete_subject(moon_user_id="admin",  policy_id=None ,perimeter_id=subject_id)

    req = hug.test.get(perimeter, "subjects/{}".format(subject_id), headers=auth_headers)
    assert req.data['subjects'] == {}


def test_delete_subject_without_policy():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    subject_id = builder.create_subject(policy_id)

    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req = hug.test.delete(perimeter, "/subjects/{}".format(subject_id), headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Policy Unknown"


def test_delete_objects_without_policy():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    object_id = builder.create_object(policy_id)

    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req = hug.test.delete(perimeter, "/objects/{}".format(object_id), headers=auth_headers)

    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Policy Unknown"


def test_delete_actions_without_policy():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import perimeter
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    action_id = builder.create_action(policy_id)

    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req = hug.test.delete(perimeter, "/actions/{}".format(action_id), headers=auth_headers)
    assert "400: Policy Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Policy Unknown"


def test_perimeter_delete_actions_without_perimeter_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    with pytest.raises(exceptions.ActionUnknown) as exception_info:
        req = delete_actions_without_perimeter_id(auth_headers=auth_headers)
    assert "400: Action Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Action Unknown"
