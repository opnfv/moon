import json
import requests

hostname = "manager"
port = 8082


def get_json(data):
    return json.loads(data.decode("utf-8"))


def get_pdp():
    req = requests.get("http://{}:{}/pdp".format(hostname, port))
    pdp = req.json()
    return req, pdp


def add_pdp(data):
    req = requests.post("http://{}:{}/pdp".format(hostname, port),
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    pdp = req.json()
    return req, pdp


def delete_pdp(key):
    req = requests.delete("http://{}:{}/pdp/{}".format(hostname, port, key))
    return req


def delete_pdp_without_id():
    req = requests.delete("http://{}:{}/pdp/{}".format(hostname, port, ""))
    return req


def test_get_pdp():
    req, pdp = get_pdp()
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
    req, pdp = add_pdp(data)
    assert req.status_code == 200
    assert isinstance(pdp, dict)
    value = list(pdp["pdps"].values())[0]
    assert "pdps" in pdp
    assert value['name'] == "testuser"
    assert value["description"] == "description of {}".format("testuser")
    assert value["keystone_project_id"] == "keystone_project_id"


def test_delete_pdp():
    request, pdp = get_pdp()
    success_req = None
    for key, value in pdp['pdps'].items():
        if value['name'] == "testuser":
            success_req = delete_pdp(key)
            break
    assert success_req
    assert success_req.status_code == 200
