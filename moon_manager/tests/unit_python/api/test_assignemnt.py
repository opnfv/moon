import api.utilities as utilities
import json
from helpers import data_builder as builder
from uuid import uuid4


# subject_categories_test


def get_subject_assignment(client, policy_id):
    req = client.get("/policies/{}/subject_assignments".format(policy_id))
    subject_assignment = utilities.get_json(req.data)
    return req, subject_assignment


def add_subject_assignment(client):
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
    req = client.post("/policies/{}/subject_assignments".format(policy_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    subject_assignment = utilities.get_json(req.data)
    return req, subject_assignment


def add_subject_assignment_without_cat_id(client):

    data = {
        "id": "subject_id",
        "category_id": "",
        "data_id": "data_id"
    }
    req = client.post("/policies/{}/subject_assignments".format("1111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    subject_assignment = utilities.get_json(req.data)
    return req, subject_assignment


def delete_subject_assignment(client, policy_id, sub_id, cat_id,data_id):
    req = client.delete("/policies/{}/subject_assignments/{}/{}/{}".format(policy_id, sub_id, cat_id,data_id))
    return req


def test_add_subject_assignment():
    client = utilities.register_client()
    req, subject_assignment = add_subject_assignment(client)
    assert req.status_code == 200
    assert isinstance(subject_assignment, dict)
    assert "subject_assignments" in subject_assignment


def test_add_subject_assignment_without_cat_id():
    client = utilities.register_client()
    req, subject_assignment = add_subject_assignment_without_cat_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'category_id', [Empty String]"


def test_get_subject_assignment():
    client = utilities.register_client()
    policy_id = builder.get_policy_id_with_subject_assignment()
    req, subject_assignment = get_subject_assignment(client, policy_id)
    assert req.status_code == 200
    assert isinstance(subject_assignment, dict)
    assert "subject_assignments" in subject_assignment


def test_delete_subject_assignment():
    client = utilities.register_client()
    policy_id = builder.get_policy_id_with_subject_assignment()
    req, subject_assignment = get_subject_assignment(client, policy_id)
    value = subject_assignment["subject_assignments"]
    id = list(value.keys())[0]
    success_req = delete_subject_assignment(client, policy_id, value[id]['subject_id'], value[id]['category_id'],value[id]['assignments'][0])
    assert success_req.status_code == 200


def test_delete_subject_assignment_without_policy_id():
    client = utilities.register_client()
    success_req = delete_subject_assignment(client, "", "id1", "111" ,"data_id1")
    assert success_req.status_code == 404


# ---------------------------------------------------------------------------

# object_categories_test


def get_object_assignment(client, policy_id):
    req = client.get("/policies/{}/object_assignments".format(policy_id))
    object_assignment = utilities.get_json(req.data)
    return req, object_assignment


def add_object_assignment(client):
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

    req = client.post("/policies/{}/object_assignments".format(policy_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    object_assignment = utilities.get_json(req.data)
    return req, object_assignment


def add_object_assignment_without_cat_id(client):

    data = {
        "id": "object_id",
        "category_id": "",
        "data_id": "data_id"
    }
    req = client.post("/policies/{}/object_assignments".format("1111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    object_assignment = utilities.get_json(req.data)
    return req, object_assignment


def delete_object_assignment(client, policy_id, obj_id, cat_id, data_id):
    req = client.delete("/policies/{}/object_assignments/{}/{}/{}".format(policy_id, obj_id, cat_id, data_id))
    return req


def test_get_object_assignment():
    policy_id = builder.get_policy_id_with_object_assignment()
    client = utilities.register_client()
    req, object_assignment = get_object_assignment(client, policy_id)
    assert req.status_code == 200
    assert isinstance(object_assignment, dict)
    assert "object_assignments" in object_assignment


def test_add_object_assignment():
    client = utilities.register_client()
    req, object_assignment = add_object_assignment(client)
    assert req.status_code == 200
    assert "object_assignments" in object_assignment


def test_add_object_assignment_without_cat_id():
    client = utilities.register_client()
    req, object_assignment = add_object_assignment_without_cat_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'category_id', [Empty String]"


def test_delete_object_assignment():
    client = utilities.register_client()
    policy_id = builder.get_policy_id_with_object_assignment()
    req, object_assignment = get_object_assignment(client, policy_id)
    value = object_assignment["object_assignments"]
    id = list(value.keys())[0]
    success_req = delete_object_assignment(client, policy_id, value[id]['object_id'], value[id]['category_id'],value[id]['assignments'][0])
    assert success_req.status_code == 200


def test_delete_object_assignment_without_policy_id():
    client = utilities.register_client()
    success_req = delete_object_assignment(client, "", "id1", "111","data_id1")
    assert success_req.status_code == 404


# ---------------------------------------------------------------------------

# action_categories_test


def get_action_assignment(client, policy_id):
    req = client.get("/policies/{}/action_assignments".format(policy_id))
    action_assignment = utilities.get_json(req.data)
    return req, action_assignment


def add_action_assignment(client):
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
    req = client.post("/policies/{}/action_assignments".format(policy_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    action_assignment = utilities.get_json(req.data)
    return req, action_assignment


def add_action_assignment_without_cat_id(client):

    data = {
        "id": "action_id",
        "category_id": "",
        "data_id": "data_id"
    }
    req = client.post("/policies/{}/action_assignments".format("1111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    action_assignment = utilities.get_json(req.data)
    return req, action_assignment


def delete_action_assignment(client, policy_id, action_id, cat_id, data_id):
    req = client.delete("/policies/{}/action_assignments/{}/{}/{}".format(policy_id, action_id, cat_id, data_id))
    return req


def test_get_action_assignment():
    policy_id = builder.get_policy_id_with_action_assignment()
    client = utilities.register_client()
    req, action_assignment = get_action_assignment(client, policy_id)
    assert req.status_code == 200
    assert isinstance(action_assignment, dict)
    assert "action_assignments" in action_assignment


def test_add_action_assignment():
    client = utilities.register_client()
    req, action_assignment = add_action_assignment(client)
    assert req.status_code == 200
    assert "action_assignments" in action_assignment


def test_add_action_assignment_without_cat_id():
    client = utilities.register_client()
    req, action_assignment = add_action_assignment_without_cat_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'category_id', [Empty String]"


def test_delete_action_assignment():
    client = utilities.register_client()
    policy_id = builder.get_policy_id_with_action_assignment()
    req, action_assignment = get_action_assignment(client, policy_id)
    value = action_assignment["action_assignments"]
    id = list(value.keys())[0]
    success_req = delete_action_assignment(client, policy_id, value[id]['action_id'], value[id]['category_id'],value[id]['assignments'][0])
    assert success_req.status_code == 200


def test_delete_action_assignment_without_policy_id():
    client = utilities.register_client()
    success_req = delete_action_assignment(client, "", "id1", "111" ,"data_id1")
    assert success_req.status_code == 404

# ---------------------------------------------------------------------------
