# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import api.utilities as utilities
import json


# subject_categories_test


def get_subject_data(client, policy_id, category_id=None):
    if category_id is None:
        req = client.get("/policies/{}/subject_data".format(policy_id))
    else:
        req = client.get("/policies/{}/subject_data/{}".format(policy_id, category_id))
    subject_data = utilities.get_json(req.data)
    return req, subject_data


def add_subject_data(client, name, policy_id, category_id):
    data = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = client.post("/policies/{}/subject_data/{}".format(policy_id, category_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    subject_data = utilities.get_json(req.data)
    return req, subject_data


def delete_subject_data(client, policy_id):
    req = client.delete("/policies/{}/subject_data".format(policy_id))
    return req


def test_get_subject_data():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, subject_data = get_subject_data(client, policy_id)
    assert req.status_code == 200
    assert isinstance(subject_data, dict)
    assert "subject_data" in subject_data


def test_add_subject_data():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, subject_data = add_subject_data(client, "testuser", policy_id, "111")
    assert req.status_code == 200
    assert isinstance(subject_data, dict)
    value = subject_data["subject_data"]['data']
    assert "subject_data" in subject_data
    id = list(value.keys())[0]
    assert value[id]['name'] == "testuser"
    assert value[id]['description'] == "description of {}".format("testuser")


def test_delete_subject_data():
    client = utilities.register_client()
    policy_id = utilities.get_policy_id()
    success_req = delete_subject_data(client, policy_id)
    assert success_req.status_code == 200


def test_add_subject_data_with_empty_user():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, subject_data = add_subject_data(client, "", policy_id, "111")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "Empty String"


def test_add_subject_data_with_user_contain_space():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, subject_data = add_subject_data(client, "test user", policy_id, "111")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "String contains space"


def test_delete_subject_data_without_policy_id():
    client = utilities.register_client()
    success_req = delete_subject_data(client, "")
    assert success_req.status_code == 500

# ---------------------------------------------------------------------------

# object_categories_test


def get_object_data(client, policy_id, category_id=None):
    if category_id is None:
        req = client.get("/policies/{}/object_data".format(policy_id))
    else:
        req = client.get("/policies/{}/object_data/{}".format(policy_id, category_id))
    object_data = utilities.get_json(req.data)
    return req, object_data


def add_object_data(client, name, policy_id, category_id):
    data = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = client.post("/policies/{}/object_data/{}".format(policy_id, category_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    object_data = utilities.get_json(req.data)
    return req, object_data


def delete_object_data(client, policy_id):
    req = client.delete("/policies/{}/object_data".format(policy_id))
    return req


def test_get_object_data():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, object_data = get_object_data(client, policy_id)
    assert req.status_code == 200
    assert isinstance(object_data, dict)
    assert "object_data" in object_data


def test_add_object_data():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, object_data = add_object_data(client, "testuser", policy_id, "111")
    assert req.status_code == 200
    assert isinstance(object_data, dict)
    value = object_data["object_data"]['data']
    assert "object_data" in object_data
    id = list(value.keys())[0]
    print("-----------------------")
    print(id)
    print(value[id])
    print("-----------------------")
    assert value[id]['name'] == "testuser"
    assert value[id]['description'] == "description of {}".format("testuser")


def test_delete_object_data():
    client = utilities.register_client()
    policy_id = utilities.get_policy_id()
    success_req = delete_object_data(client, policy_id)
    assert success_req.status_code == 200


def test_add_object_data_with_empty_user():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, subject_data = add_subject_data(client, "", policy_id, "111")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "Empty String"


def test_add_object_data_with_user_contain_space():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, object_data = add_object_data(client, "test user", policy_id, "111")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "String contains space"


def test_delete_object_data_without_policy_id():
    client = utilities.register_client()
    success_req = delete_object_data(client, "")
    assert success_req.status_code == 500
# ---------------------------------------------------------------------------

# action_categories_test


def get_action_data(client, policy_id, category_id=None):
    if category_id is None:
        req = client.get("/policies/{}/action_data".format(policy_id))
    else:
        req = client.get("/policies/{}/action_data/{}".format(policy_id, category_id))
    action_data = utilities.get_json(req.data)
    return req, action_data


def add_action_data(client, name, policy_id, category_id):
    data = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = client.post("/policies/{}/action_data/{}".format(policy_id, category_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    action_data = utilities.get_json(req.data)
    return req, action_data


def delete_action_data(client, policy_id):
    req = client.delete("/policies/{}/action_data".format(policy_id))
    return req


def test_get_action_data():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, action_data = get_action_data(client, policy_id)
    assert req.status_code == 200
    assert isinstance(action_data, dict)
    assert "action_data" in action_data


def test_add_action_data():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, action_data = add_action_data(client, "testuser", policy_id, "111")
    assert req.status_code == 200
    assert isinstance(action_data, dict)
    value = action_data["action_data"]['data']
    assert "action_data" in action_data
    id = list(value.keys())[0]
    assert value[id]['name'] == "testuser"
    assert value[id]['description'] == "description of {}".format("testuser")


def test_delete_action_data():
    client = utilities.register_client()
    policy_id = utilities.get_policy_id()
    success_req = delete_action_data(client, policy_id)
    assert success_req.status_code == 200


def test_add_action_data_with_empty_user():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, action_data = add_action_data(client, "", policy_id, "111")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "Empty String"


def test_add_action_data_with_user_contain_space():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, action_data = add_action_data(client, "test user", policy_id, "111")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "String contains space"


def test_delete_action_data_without_policy_id():
    client = utilities.register_client()
    success_req = delete_action_data(client, "")
    assert success_req.status_code == 500
# ---------------------------------------------------------------------------
