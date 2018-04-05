import json
import api.utilities as utilities
import pytest


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
    data = {
        "name": "testuser",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
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
    for key, value in pdp['pdps'].items():
        if value['name'] == "testuser":
            success_req = delete_pdp(client, key)
            break
    assert success_req.status_code == 200


def test_add_pdp_with_empty_user():
    data = {
        "name": "",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req, models = add_pdp(client, data)
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "Empty String"


def test_add_pdp_with_user_contain_space():
    data = {
        "name": "test user",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req, models = add_pdp(client, data)
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "String contains space"


def test_add_pdp_without_security_pipeline():
    data = {
        "name": "testuser",
        "security_pipeline": [],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req, meta_rules = add_pdp(client, data)
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == 'Empty Container'


def test_add_pdp_without_keystone():
    data = {
        "name": "testuser",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req, meta_rules = add_pdp(client, data)
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == 'Empty String'


def test_update_pdp():
    data_add = {
        "name": "testuser",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    data_update = {
        "name": "testuser",
        "security_pipeline": ["policy_id_1_update", "policy_id_2_update"],
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
    assert req_update[0].status_code == 500


def test_update_pdp_without_user():
    data = {
        "name": "",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req_update = update_pdp(client, data, "")
    assert req_update[0].status_code == 500
    assert json.loads(req_update[0].data)["message"] == "Empty String"


def test_update_pdp_without_security_pipeline():
    data = {
        "name": "testuser",
        "security_pipeline": [],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    client = utilities.register_client()
    req_update = update_pdp(client, data, "")
    assert req_update[0].status_code == 500
    assert json.loads(req_update[0].data)["message"] == "Empty Container"