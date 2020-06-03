# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from falcon import HTTP_200, HTTP_400, HTTP_405
import hug
import pytest
from moon_utilities import exceptions
from uuid import uuid4
from helpers import data_builder as builder


def test_get_pdp():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    req = hug.test.get(pdp, 'pdp/', headers=auth_headers)
    assert req.status == HTTP_200
    assert isinstance(req.data, dict)
    assert "pdps" in req.data

def test_add_pdp_invalid_security_pipeline(mocker):
    from moon_manager.api import pdp
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data_no_pipeline = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [],
        "vim_project_id": "vim_project_id",
        "description": "description of testuser"
    }
    data_no_project_no_pipeline = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [],
        "vim_project_id": None,
        "description": "description of testuser"
    }
    data_no_project = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [policy_id],
        "vim_project_id": None,
        "description": "description of testuser"
    }
    
    req = hug.test.post(pdp, "pdp/", data_no_project_no_pipeline, headers=auth_headers)
    assert req.status == HTTP_200

    with pytest.raises(exceptions.PdpContentError) as exception_info:
        req = hug.test.post(pdp, "pdp/", data_no_pipeline, headers=auth_headers)
    assert "400: Pdp Error" == str(exception_info.value)

    with pytest.raises(exceptions.PdpContentError) as exception_info:    
        req = hug.test.post(pdp, "pdp/", data_no_project, headers=auth_headers)
    assert "400: Pdp Error" == str(exception_info.value)

def test_update_pdp_invalid_security_pipeline(mocker):
    from moon_manager.api import pdp
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data_no_pipeline = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [],
        "vim_project_id": "vim_project_id",
        "description": "description of testuser"
    }
    data_no_project_no_pipeline = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [],
        "vim_project_id": None,
        "description": "description of testuser"
    }
    data_no_project = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [policy_id],
        "vim_project_id": None,
        "description": "description of testuser"
    }

    data_valid = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [policy_id],
        "vim_project_id": "vim_project_id",
        "description": "description of testuser"
    }
    req = hug.test.post(pdp, "pdp/", data_valid, headers=auth_headers)
    assert req.status == HTTP_200
    pip_id = list(req.data['pdps'])[0]

    req = hug.test.patch(pdp, "pdp/{}".format(pip_id), data_no_project_no_pipeline, headers=auth_headers)
    assert req.status == HTTP_200

    with pytest.raises(exceptions.PdpContentError) as exception_info:
        req = hug.test.patch(pdp, "pdp/{}".format(pip_id), data_no_pipeline, headers=auth_headers)
    assert "400: Pdp Error" == str(exception_info.value)

    with pytest.raises(exceptions.PdpContentError) as exception_info:
        req = hug.test.patch(pdp, "pdp/{}".format(pip_id), data_no_project, headers=auth_headers)
    assert "400: Pdp Error" == str(exception_info.value)

def test_add_pdp(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [policy_id],
        "vim_project_id": "vim_project_id",
        "description": "description of testuser"
    }
    req = hug.test.post(pdp, "pdp/", data, headers=auth_headers)
    assert req.status == HTTP_200
    assert isinstance(req.data, dict)
    found = False
    assert "pdps" in req.data
    for value in req.data["pdps"].values():
        if value['name'] == data['name']:
            found = True
            assert value["description"] == "description of {}".format("testuser")
            assert value["vim_project_id"] == "vim_project_id"
            break
    assert found


def test_add_pdp_name_existed(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id1 = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)

    name = "testuser" + uuid4().hex
    data = {
        "name": name,
        "security_pipeline": [policy_id1],
        "vim_project_id": "vim_project_id",
        "description": "description of testuser"
    }
    req = hug.test.post(pdp, "pdp/", data, headers=auth_headers)
    assert req.status == HTTP_200

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id2 = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)

    data = {
        "name": name,
        "security_pipeline": [policy_id2],
        "vim_project_id": "vim_project_id" + uuid4().hex,
        "description": "description of testuser" + uuid4().hex
    }
    with pytest.raises(exceptions.PdpExisting) as exception_info:
        req = hug.test.post(pdp, "pdp/", data, headers=auth_headers)
    assert "409: Pdp Error" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data['message'] == '409: Pdp Error'


def test_add_pdp_policy_used(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id1 = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)

    data = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [policy_id1],
        "vim_project_id": "vim_project_id",
        "description": "description of testuser"
    }
    req = hug.test.post(pdp, "pdp/", data, headers=auth_headers)
    assert req.status == HTTP_200

    name_uuid = "testuser" + uuid4().hex
    data = {
        "name": name_uuid,
        "security_pipeline": [policy_id1],
        "vim_project_id": "vim_project_id " + name_uuid,
        "description": "description of testuser " + name_uuid
    }

    with pytest.raises(exceptions.PdpInUse) as exception_info:
        req = hug.test.post(pdp, "pdp/", data, headers=auth_headers)
    assert "400: Pdp Inuse" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data['message'] == '409: Pdp Conflict'


def test_delete_pdp(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data = {
        "name": "testuser" + uuid4().hex,
        "security_pipeline": [policy_id],
        "vim_project_id": "vim_project_id",
        "description": "description of testuser"
    }
    req = hug.test.post(pdp, "pdp/", data, headers=auth_headers)
    assert req.status == HTTP_200
    assert isinstance(req.data, dict)
    req = hug.test.get(pdp, 'pdp/', headers=auth_headers)
    success_req = None
    for key, value in req.data['pdps'].items():
        if value['name'] == data['name']:
            success_req = hug.test.delete(pdp, 'pdp/{}'.format(key), headers=auth_headers)
            break
    assert success_req
    assert success_req.status == HTTP_200


# Fixme: should re-enabled the input validation for those tests
# def test_add_pdp_with_forbidden_char_in_user():
#     data = {
#         "name": "<a>",
#         "security_pipeline": ["policy_id_1", "policy_id_2"],
#         "vim_project_id": "vim_project_id",
#         "description": "description of testuser"
#     }
#     req = hug.test.post(pdp, "pdp/", data)
#     assert req.status == HTTP_400
#     print(req.data)
#     assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"
#
#
# def test_add_pdp_with_forbidden_char_in_keystone():
#     data = {
#         "name": "testuser",
#         "security_pipeline": ["policy_id_1", "policy_id_2"],
#         "vim_project_id": "<a>",
#         "description": "description of testuser"
#     }
#     req = hug.test.post(pdp, "pdp/", data)
#     assert req.status == 400
#     assert req.data["message"] == "Key: 'vim_project_id', [Forbidden characters in string]"


def test_update_pdp(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data_add = {
        "name": "testuser",
        "security_pipeline": [policy_id],
        "vim_project_id": "vim_project_id",
        "description": "description of testuser"
    }

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id_update = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data_update = {
        "name": "testuser_updated",
        "security_pipeline": [policy_id_update],
        "vim_project_id": "vim_project_id_update",
        "description": "description of testuser_updated"
    }
    req = hug.test.post(pdp, "pdp/", data_add, headers=auth_headers)
    pdp_id = list(req.data['pdps'])[0]
    req_update = hug.test.patch(pdp, "pdp/{}".format(pdp_id), data_update, headers=auth_headers)
    assert req_update.status == HTTP_200
    value = list(req_update.data["pdps"].values())[0]
    assert value["vim_project_id"] == data_update["vim_project_id"]
    assert value["description"] == data_update["description"]
    assert value["name"] == data_update['name']
    assert value["security_pipeline"] == data_update['security_pipeline']
    req = hug.test.get(pdp, 'pdp/', headers=auth_headers)
    for key, value in req.data['pdps'].items():
        if value['name'] == "testuser":
            hug.test.delete(pdp, 'pdp/{}'.format(key), headers=auth_headers)
            break


def test_update_pdp_without_id(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    req = hug.test.patch(pdp, "pdp/", "testuser", headers=auth_headers)
    assert req.status == HTTP_405
    # assert req.data["message"] == 'Invalid Key :name not found'


def test_update_pdp_without_user(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    data = {
        "name": "",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "vim_project_id": "vim_project_id",
        "description": "description of testuser"
    }
    req = hug.test.patch(pdp, "pdp/<a>", data, headers=auth_headers)
    assert req.status == HTTP_400
    print(req.data)
    assert req.data["errors"] == {'uuid': 'Invalid UUID provided'}


def test_update_pdp_name_existed(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id1 = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    uuid1 = uuid4().hex
    data1 = {
        "name": "testuser1" + uuid1,
        "security_pipeline": [policy_id1],
        "vim_project_id": "vim_project_id" + uuid1,
        "description": "description of testuser1" + uuid1
    }
    req = hug.test.post(pdp, "pdp/", data1, headers=auth_headers)
    assert req.status == HTTP_200

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id2 = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)

    uuid2 = uuid4().hex
    data2 = {
        "name": "testuser2" + uuid2,
        "security_pipeline": [policy_id2],
        "vim_project_id": "vim_project_id" + uuid2,
        "description": "description of testuser2" + uuid2
    }
    req = hug.test.post(pdp, "pdp/", data2, headers=auth_headers)
    pdp_id = list(req.data['pdps'])[0]
    for item in list(req.data['pdps']):
        if req.data['pdps'][item]['name']==data2['name']:
            pdp_id=item
            break
    data2['name'] = data1['name']
    with pytest.raises(exceptions.PdpExisting) as exception_info:
        req_update = hug.test.patch(pdp, "pdp/{}".format(pdp_id), data2, headers=auth_headers)
        # assert req_update.data['message'] == '409: Pdp Error'
    assert "409: Pdp Error" == str(exception_info.value)



def test_update_pdp_policy_used(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import pdp
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:20000")
    mocker.patch("subprocess.Popen", return_value=True)
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id1 = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    uuid1 = uuid4().hex
    data1 = {
        "name": "testuser1" + uuid1,
        "security_pipeline": [policy_id1],
        "vim_project_id": "vim_project_id" + uuid1,
        "description": "description of testuser1" + uuid1
    }
    req = hug.test.post(pdp, "pdp/", data1, headers=auth_headers)
    assert req.status == HTTP_200

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id2 = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)

    uuid2 = uuid4().hex
    data2 = {
        "name": "testuser2" + uuid2,
        "security_pipeline": [policy_id2],
        "vim_project_id": "vim_project_id" + uuid2,
        "description": "description of testuser2" + uuid2
    }
    req = hug.test.post(pdp, "pdp/", data2, headers=auth_headers)
    pdp_id = list(req.data['pdps'])[0]
    for item in list(req.data['pdps']):
        if req.data['pdps'][item]['name']==data2['name']:
            pdp_id=item
            break
    data2['security_pipeline'] = data1['security_pipeline']

    with pytest.raises(exceptions.PdpInUse) as exception_info:
        req_update = hug.test.patch(pdp, "pdp/{}".format(pdp_id), data2, headers=auth_headers)
    assert "400: Pdp Inuse" == str(exception_info.value)
        # assert req_update.data['message'] == '409: Pdp Conflict'


