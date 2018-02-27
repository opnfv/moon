import api.utilities as utilities
import json


# subject_categories_test


def get_subject_assignment(client, policy_id):
    req = client.get("/policies/{}/subject_assignments".format(policy_id))
    subject_assignment = utilities.get_json(req.data)
    return req, subject_assignment


def add_subject_assignment(client, policy_id, category_id):
    data = {
        "id": "id1",
        "category_id": category_id,
        "data_id": "data_id1"
    }
    req = client.post("/policies/{}/subject_assignments/{}".format(policy_id, category_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    subject_assignment = utilities.get_json(req.data)
    return req, subject_assignment


def delete_subject_assignment(client, policy_id):
    req = client.delete("/policies/{}/subject_assignments".format(policy_id))
    return req


def test_add_subject_assignment():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, subject_assignment = add_subject_assignment(client, policy_id, "111")
    assert req.status_code == 200
    assert isinstance(subject_assignment, dict)
    value = subject_assignment["subject_assignments"]
    assert "subject_assignments" in subject_assignment
    id = list(value.keys())[0]
    assert value[id]['policy_id'] == policy_id
    assert value[id]['category_id'] == "111"
    assert value[id]['subject_id'] == "id1"


def test_get_subject_assignment():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, subject_assignment = get_subject_assignment(client, policy_id)
    assert req.status_code == 200
    assert isinstance(subject_assignment, dict)
    assert "subject_assignments" in subject_assignment


def test_delete_subject_assignment():
    client = utilities.register_client()
    policy_id = utilities.get_policy_id()
    success_req = delete_subject_assignment(client, policy_id)
    assert success_req.status_code == 200

# ---------------------------------------------------------------------------

# object_categories_test


def get_object_assignment(client, policy_id):
    req = client.get("/policies/{}/object_assignments".format(policy_id))
    object_assignment = utilities.get_json(req.data)
    return req, object_assignment


def add_object_assignment(client, policy_id, category_id):
    data = {
        "id": "id1",
        "category_id": category_id,
        "data_id": "data_id1"
    }
    req = client.post("/policies/{}/object_assignments/{}".format(policy_id, category_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    object_assignment = utilities.get_json(req.data)
    return req, object_assignment


def delete_object_assignment(client, policy_id):
    req = client.delete("/policies/{}/object_assignments".format(policy_id))
    return req


def test_get_object_assignment():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, object_assignment = get_object_assignment(client, policy_id)
    assert req.status_code == 200
    assert isinstance(object_assignment, dict)
    assert "object_assignments" in object_assignment


def test_add_object_assignment():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, object_assignment = add_object_assignment(client, policy_id, "111")
    assert req.status_code == 200
    assert isinstance(object_assignment, dict)
    value = object_assignment["object_assignments"]
    assert "object_assignments" in object_assignment
    id = list(value.keys())[0]
    assert value[id]['policy_id'] == policy_id
    assert value[id]['category_id'] == "111"
    assert value[id]['object_id'] == "id1"


def test_delete_object_assignment():
    client = utilities.register_client()
    policy_id = utilities.get_policy_id()
    success_req = delete_object_assignment(client, policy_id)
    assert success_req.status_code == 200

# ---------------------------------------------------------------------------

# action_categories_test


def get_action_assignment(client, policy_id):
    req = client.get("/policies/{}/action_assignments".format(policy_id))
    action_assignment = utilities.get_json(req.data)
    return req, action_assignment


def add_action_assignment(client, policy_id, category_id):
    data = {
        "id": "id1",
        "category_id": category_id,
        "data_id": "data_id1"
    }
    req = client.post("/policies/{}/action_assignments/{}".format(policy_id, category_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    action_assignment = utilities.get_json(req.data)
    return req, action_assignment


def delete_action_assignment(client, policy_id):
    req = client.delete("/policies/{}/action_assignments".format(policy_id))
    return req


def test_get_action_assignment():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, action_assignment = get_action_assignment(client, policy_id)
    assert req.status_code == 200
    assert isinstance(action_assignment, dict)
    assert "action_assignments" in action_assignment


def test_add_action_assignment():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, action_assignment = add_action_assignment(client, policy_id, "111")
    assert req.status_code == 200
    assert isinstance(action_assignment, dict)
    value = action_assignment["action_assignments"]
    assert "action_assignments" in action_assignment
    id = list(value.keys())[0]
    assert value[id]['policy_id'] == policy_id
    assert value[id]['category_id'] == "111"
    assert value[id]['action_id'] == "id1"


def test_delete_action_assignment():
    client = utilities.register_client()
    policy_id = utilities.get_policy_id()
    success_req = delete_action_assignment(client, policy_id)
    assert success_req.status_code == 200

# ---------------------------------------------------------------------------