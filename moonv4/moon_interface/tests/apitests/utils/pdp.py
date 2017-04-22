import requests

URL = "http://172.18.0.11:38001{}"
HEADERS = {"content-type": "application/json"}
KEYSTONE_USER = "admin"
KEYSTONE_PASSWORD = "p4ssw0rd"
KEYSTONE_PROJECT = "admin"

pdp_template = {
    "name": "test_pdp",
    "security_pipeline": [],
    "keystone_project_id": "",
    "description": "test",
}


def get_keystone_projects():
    server = "keystone"

    HEADERS = {
        "Content-Type": "application/json"
    }

    data_auth = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "id": "Default"
                        },
                        "name": KEYSTONE_USER,
                        "password": KEYSTONE_PASSWORD
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "id": "Default"
                    },
                    "name": KEYSTONE_PROJECT
                }
            }
        }
    }

    req = requests.post("http://{}:5000/v3/auth/tokens".format(server), json=data_auth, headers=HEADERS)

    assert req.status_code in (200, 201)
    TOKEN = req.headers['X-Subject-Token']
    HEADERS['X-Auth-Token'] = TOKEN
    req = requests.get("http://{}:5000/v3/projects".format(server), headers=HEADERS)
    assert req.status_code in (200, 201)
    return req.json()


def check_pdp(pdp_id=None, keystone_project_id=None):
    req = requests.get(URL.format("/pdp"))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "pdps" in result
    if pdp_id:
        assert result["pdps"]
        assert pdp_id in result['pdps']
        assert "name" in result['pdps'][pdp_id]
        assert pdp_template["name"] == result['pdps'][pdp_id]["name"]
    if keystone_project_id:
        assert result["pdps"]
        assert pdp_id in result['pdps']
        assert "keystone_project_id" in result['pdps'][pdp_id]
        assert keystone_project_id == result['pdps'][pdp_id]["keystone_project_id"]
    return result


def add_pdp(name="test_pdp", policy_id=None):
    pdp_template['name'] = name
    if policy_id:
        pdp_template['security_pipeline'].append(policy_id)
    req = requests.post(URL.format("/pdp"), json=pdp_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    pdp_id = list(result['pdps'].keys())[0]
    if "result" in result:
        assert result["result"]
    assert "name" in result['pdps'][pdp_id]
    assert pdp_template["name"] == result['pdps'][pdp_id]["name"]
    return pdp_id


def update_pdp(pdp_id, policy_id=None):
    req = requests.get(URL.format("/pdp/{}".format(pdp_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "pdps" in result
    assert pdp_id in result['pdps']
    pipeline = result['pdps'][pdp_id]["security_pipeline"]
    if policy_id not in pipeline:
        pipeline.append(policy_id)
        req = requests.patch(URL.format("/pdp/{}".format(pdp_id)),
                             json={"security_pipeline": pipeline})
        assert req.status_code == 200
        result = req.json()
        assert type(result) is dict
        assert "pdps" in result
        assert pdp_id in result['pdps']

    req = requests.get(URL.format("/pdp/{}".format(pdp_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "pdps" in result
    assert pdp_id in result['pdps']
    assert policy_id in pipeline


def map_to_keystone(pdp_id, keystone_project_id):
    req = requests.patch(URL.format("/pdp/{}".format(pdp_id)), json={"keystone_project_id": keystone_project_id},
                         headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    if "result" in result:
        assert result["result"]
    assert pdp_id in result['pdps']
    assert "name" in result['pdps'][pdp_id]
    assert pdp_template["name"] == result['pdps'][pdp_id]["name"]
    return pdp_id


def delete_pdp(pdp_id):
    req = requests.delete(URL.format("/pdp/{}".format(pdp_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "result" in result
    assert result["result"]


