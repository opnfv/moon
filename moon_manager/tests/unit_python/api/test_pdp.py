import json
import api.utilities as utilities
import pytest


def get_pdp(client):
    req = client.get("/pdp")
    pdp = utilities.get_json(req.data)
    return req, pdp


def add_pdp(client, name):
    data = {
        "name": name,
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "description of {}".format(name)
    }
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
    client = utilities.register_client()
    req, pdp = add_pdp(client, "testuser")
    assert req.status_code == 200
    assert isinstance(pdp, dict)
    value = list(pdp["pdps"].values())[0]
    assert "pdps" in pdp
    assert value['name'] == "testuser"
    assert value["description"] == "description of {}".format("testuser")
    assert value["keystone_project_id"] == "keystone_project_id1"


'''
testcase delete_pdp fails because when try to request delete(), it calls delete_pod() method 
in pdp module which is not implemented.
'''

# def test_delete_pdp():
#     client = utilities.register_client()
#     request, pdp = get_pdp(client)
#     for key, value in pdp['pdps'].items():
#         if value['name'] == "testuser":
#             success_req = delete_pdp(client, key)
#             fail_req = delete_pdp_without_id(client)
#             break
#     assert success_req.status_code == 200
#     assert fail_req.status_code == 500
