# import moon_manager
# import moon_manager.api
import json
import api.utilities as utilities
from helpers import data_builder as builder
from uuid import uuid4


def get_subjects(client):
    req = client.get("/subjects")
    subjects = utilities.get_json(req.data)
    return req, subjects


def add_subjects(client, name):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data = {
        "name": name + uuid4().hex,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req = client.post("/policies/{}/subjects".format(policy_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    subjects = utilities.get_json(req.data)
    return req, subjects


def delete_subject(client):
    subjects = get_subjects(client)
    value = subjects[1]['subjects']
    id = list(value.keys())[0]
    policy_id = builder.get_policy_id_with_subject_assignment()
    return client.delete("/policies/{}/subjects/{}".format(policy_id, id))


def delete_subjects_without_perimeter_id(client):
    req = client.delete("/subjects/{}".format(""))
    return req


def test_perimeter_get_subject():
    client = utilities.register_client()
    req, subjects = get_subjects(client)
    assert req.status_code == 200
    assert isinstance(subjects, dict)
    assert "subjects" in subjects


def test_perimeter_add_subject():
    client = utilities.register_client()
    req, subjects = add_subjects(client, "testuser")
    value = list(subjects["subjects"].values())[0]
    assert req.status_code == 200
    assert "subjects" in subjects
    assert value["name"] is not None
    assert value["email"] is not None


def test_perimeter_add_subject_without_name():
    client = utilities.register_client()
    data = {
        "name": "",
        "description": "description of {}".format(""),
        "password": "password for {}".format(""),
        "email": "{}@moon".format("")
    }
    req = client.post("/policies/{}/subjects".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Empty String]"


def test_perimeter_add_subject_with_name_contain_spaces():
    client = utilities.register_client()
    data = {
        "name": "test user",
        "description": "description of {}".format("test user"),
        "password": "password for {}".format("test user"),
        "email": "{}@moon".format("test user")
    }
    req = client.post("/policies/{}/subjects".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [String contains space]"


def test_perimeter_delete_subject():
    client = utilities.register_client()
    req = delete_subject(client)
    assert req.status_code == 200


def test_perimeter_delete_subjects_without_perimeter_id():
    client = utilities.register_client()
    req = delete_subjects_without_perimeter_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Subject Unknown"


def get_objects(client):
    req = client.get("/objects")
    objects = utilities.get_json(req.data)
    return req, objects


def add_objects(client, name):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policyId = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data = {
        "name": name + uuid4().hex,
        "description": "description of {}".format(name),
    }
    req = client.post("/policies/{}/objects/".format(policyId), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    objects = utilities.get_json(req.data)
    return req, objects


def delete_object(client):
    objects = get_objects(client)
    value = objects[1]['objects']
    id = list(value.keys())[0]
    policy_id = builder.get_policy_id_with_object_assignment()
    return client.delete("/policies/{}/objects/{}".format(policy_id, id))


def delete_objects_without_perimeter_id(client):
    req = client.delete("/objects/{}".format(""))
    return req


def test_perimeter_get_object():
    client = utilities.register_client()
    req, objects = get_objects(client)
    assert req.status_code == 200
    assert isinstance(objects, dict)
    assert "objects" in objects


def test_perimeter_add_object():
    client = utilities.register_client()
    req, objects = add_objects(client, "testuser")
    value = list(objects["objects"].values())[0]
    assert req.status_code == 200
    assert "objects" in objects
    assert value['name'] is not None


def test_perimeter_add_object_without_name():
    client = utilities.register_client()
    data = {
        "name": "",
        "description": "description of {}".format(""),
    }
    req = client.post("/policies/{}/objects/".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Empty String]"


def test_perimeter_add_object_with_name_contain_spaces():
    client = utilities.register_client()
    data = {
        "name": "test user",
        "description": "description of {}".format("test user"),
    }
    req = client.post("/policies/{}/objects/".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [String contains space]"


def test_perimeter_delete_object():
    client = utilities.register_client()
    req = delete_object(client)
    assert req.status_code == 200


def test_perimeter_delete_objects_without_perimeter_id():
    client = utilities.register_client()
    req = delete_objects_without_perimeter_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Object Unknown"


def get_actions(client):
    req = client.get("/actions")
    actions = utilities.get_json(req.data)
    return req, actions


def add_actions(client, name):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policyId = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data = {
        "name": name + uuid4().hex,
        "description": "description of {}".format(name),
    }
    req = client.post("/policies/{}/actions".format(policyId), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    actions = utilities.get_json(req.data)
    return req, actions


def delete_actions(client):
    actions = get_actions(client)
    value = actions[1]['actions']
    id = list(value.keys())[0]
    policy_id = builder.get_policy_id_with_action_assignment()
    return client.delete("/policies/{}/actions/{}".format(policy_id, id))


def delete_actions_without_perimeter_id(client):
    req = client.delete("/actions/{}".format(""))
    return req


def test_perimeter_get_actions():
    client = utilities.register_client()
    req, actions = get_actions(client)
    assert req.status_code == 200
    assert isinstance(actions, dict)
    assert "actions" in actions


def test_perimeter_add_actions():
    client = utilities.register_client()
    req, actions = add_actions(client, "testuser")
    value = list(actions["actions"].values())[0]
    assert req.status_code == 200
    assert "actions" in actions
    assert value['name'] is not None


def test_perimeter_add_actions_without_name():
    client = utilities.register_client()
    data = {
        "name": "",
        "description": "description of {}".format(""),
    }
    req = client.post("/policies/{}/actions".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Empty String]"


def test_perimeter_add_actions_with_name_contain_spaces():
    client = utilities.register_client()
    data = {
        "name": "test user",
        "description": "description of {}".format("test user"),
    }
    req = client.post("/policies/{}/actions".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [String contains space]"


def test_perimeter_delete_actions():
    client = utilities.register_client()
    req = delete_actions(client)
    assert req.status_code == 200


def test_perimeter_delete_actions_without_perimeter_id():
    client = utilities.register_client()
    req = delete_actions_without_perimeter_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Action Unknown"
