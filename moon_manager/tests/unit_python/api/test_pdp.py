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
