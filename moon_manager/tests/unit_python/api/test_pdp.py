import json
import api.utilities as utilities
from helpers import data_builder as builder
from uuid import uuid4


def get_pdp(client):
    req = client.get("/pdp")
    pdp = utilities.get_json(req.data)
    return req, pdp


def add_pdp(client, data):
    req = client.post("/pdp", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    pdp = utilities.get_json(req.data)
    return req, pdp


def update_pdp(client, data, pdp_id):
    req = client.patch("/pdp/{}".format(pdp_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    pdp = utilities.get_json(req.data)
    return req, pdp


def delete_pdp(client, key):
    req = client.delete("/pdp/{}".format(key))
    return req


def delete_pdp_without_id(client):
    req = client.delete("/pdp/{}".format(""))
    return req


def test_get_pdp():
    client = utilities.register_client()
    req, pdp = get_pdp(client)
    assert req.status_code == 200
    assert isinstance(pdp, dict)
    assert "pdps" in pdp


def test_add_pdp():
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data = {
        "name": "testuser",
        "security_pipeline": [policy_id],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req, pdp = add_pdp(client, data)
    assert req.status_code == 200
    assert isinstance(pdp, dict)
    value = list(pdp["pdps"].values())[0]
    assert "pdps" in pdp
    assert value['name'] == "testuser"
    assert value["description"] == "description of {}".format("testuser")
    assert value["keystone_project_id"] == "keystone_project_id"


def test_delete_pdp():
    client = utilities.register_client()
    request, pdp = get_pdp(client)
    success_req = None
    for key, value in pdp['pdps'].items():
        if value['name'] == "testuser":
            success_req = delete_pdp(client, key)
            break
    assert success_req
    assert success_req.status_code == 200


def test_add_pdp_with_forbidden_char_in_user():
    data = {
        "name": "<a>",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req, models = add_pdp(client, data)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Forbidden characters in string]"


def test_add_pdp_with_forbidden_char_in_keystone():
    data = {
        "name": "testuser",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "<a>",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req, meta_rules = add_pdp(client, data)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'keystone_project_id', [Forbidden characters in string]"


def test_update_pdp():
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
        subject_category_name="subject_category1"+uuid4().hex,
        object_category_name="object_category1"+uuid4().hex,
        action_category_name="action_category1"+uuid4().hex,
        meta_rule_name="meta_rule_1"+uuid4().hex,
        model_name="model1"+uuid4().hex)
    data_add = {
        "name": "testuser",
        "security_pipeline": [policy_id],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id_update = builder.create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex,
        model_name="model1" + uuid4().hex)
    data_update = {
        "name": "testuser",
        "security_pipeline": [policy_id_update],
        "keystone_project_id": "keystone_project_id_update",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req = add_pdp(client, data_add)
    pdp_id = list(req[1]['pdps'])[0]
    req_update = update_pdp(client, data_update, pdp_id)
    assert req_update[0].status_code == 200
    value = list(req_update[1]["pdps"].values())[0]
    assert value["keystone_project_id"] == "keystone_project_id_update"
    request, pdp = get_pdp(client)
    for key, value in pdp['pdps'].items():
        if value['name'] == "testuser":
            delete_pdp(client, key)
            break


def test_update_pdp_without_id():
    client = utilities.register_client()
    req_update = update_pdp(client, "testuser", "")
    assert req_update[0].status_code == 400
    assert json.loads(req_update[0].data)["message"] == 'Invalid Key :name not found'


def test_update_pdp_without_user():
    data = {
        "name": "",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req_update = update_pdp(client, data, "<a>")
    assert req_update[0].status_code == 400
    assert json.loads(req_update[0].data)["message"] == "Forbidden characters in string"
