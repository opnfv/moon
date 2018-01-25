import json
import requests


def get_json(data):
    return json.loads(data.decode("utf-8"))


def get_pdp(context):
    req = requests.get("http://{}:{}/pdp".format(
        context.get("hostname"),
        context.get("port")),
        timeout=3)
    pdp = req.json()
    return req, pdp


def add_pdp(context, data):
    req = requests.post("http://{}:{}/pdp".format(
        context.get("hostname"),
        context.get("port")),
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'},
        timeout=3)
    pdp = req.json()
    return req, pdp


def delete_pdp(context, key):
    req = requests.delete("http://{}:{}/pdp/{}".format(
        context.get("hostname"),
        context.get("port"), key),
        timeout=3)
    return req


def delete_pdp_without_id(context):
    req = requests.delete("http://{}:{}/pdp/{}".format(
        context.get("hostname"),
        context.get("port"), ""),
        timeout=3)
    return req


def test_get_pdp(context):
    req, pdp = get_pdp(context)
    assert req.status_code == 200
    assert isinstance(pdp, dict)
    assert "pdps" in pdp


def test_add_pdp(context):
    data = {
        "name": "testuser",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id",
        "description": "description of testuser"
    }
    req, pdp = add_pdp(context, data)
    assert req.status_code == 200
    assert isinstance(pdp, dict)
    value = list(pdp["pdps"].values())[0]
    assert "pdps" in pdp
    assert value['name'] == "testuser"
    assert value["description"] == "description of {}".format("testuser")
    assert value["keystone_project_id"] == "keystone_project_id"


def test_delete_pdp(context):
    request, pdp = get_pdp(context)
    success_req = None
    for key, value in pdp['pdps'].items():
        if value['name'] == "testuser":
            success_req = delete_pdp(context, key)
            break
    assert success_req
    assert success_req.status_code == 200
