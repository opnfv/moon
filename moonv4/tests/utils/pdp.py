import logging
import requests
import utils.config

config = utils.config.get_config_data()
logger = logging.getLogger("moonforming.utils.policies")

URL = "http://{}:{}".format(
    config['components']['manager']['hostname'],
    config['components']['manager']['port'])
HEADERS = {"content-type": "application/json"}
KEYSTONE_USER = config['openstack']['keystone']['user']
KEYSTONE_PASSWORD = config['openstack']['keystone']['password']
KEYSTONE_PROJECT = config['openstack']['keystone']['project']
KEYSTONE_SERVER = config['openstack']['keystone']['url']

pdp_template = {
    "name": "test_pdp",
    "security_pipeline": [],
    "keystone_project_id": None,
    "description": "test",
}


def get_keystone_projects():

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
                        "name": KEYSTONE_USER,
                        "domain": {
                            "name": "Default"
                        },
                        "password": KEYSTONE_PASSWORD
                    }
                }
            }
        }
    }

    req = requests.post("{}/auth/tokens".format(KEYSTONE_SERVER), json=data_auth, headers=HEADERS)
    logger.debug("{}/auth/tokens".format(KEYSTONE_SERVER))
    logger.debug(req.text)
    assert req.status_code in (200, 201)
    TOKEN = req.headers['X-Subject-Token']
    HEADERS['X-Auth-Token'] = TOKEN
    req = requests.get("{}/projects".format(KEYSTONE_SERVER), headers=HEADERS)
    if req.status_code not in (200, 201):
        data_auth["auth"]["scope"] = {
            "project": {
                "name": KEYSTONE_PROJECT,
                "domain": {
                    "id": "default"
                }
            }
        }
        req = requests.post("{}/auth/tokens".format(KEYSTONE_SERVER), json=data_auth, headers=HEADERS)
        assert req.status_code in (200, 201)
        TOKEN = req.headers['X-Subject-Token']
        HEADERS['X-Auth-Token'] = TOKEN
        req = requests.get("{}/projects".format(KEYSTONE_SERVER), headers=HEADERS)
    assert req.status_code in (200, 201)
    return req.json()


def check_pdp(pdp_id=None, keystone_project_id=None, moon_url=None):
    _URL = URL
    if moon_url:
        _URL = moon_url
    req = requests.get(_URL + "/pdp")
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
    req = requests.post(URL + "/pdp", json=pdp_template, headers=HEADERS)
    logger.debug(req.status_code)
    logger.debug(req)
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
    req = requests.get(URL + "/pdp/{}".format(pdp_id))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "pdps" in result
    assert pdp_id in result['pdps']
    pipeline = result['pdps'][pdp_id]["security_pipeline"]
    if policy_id not in pipeline:
        pipeline.append(policy_id)
        req = requests.patch(URL + "/pdp/{}".format(pdp_id),
                             json={"security_pipeline": pipeline})
        assert req.status_code == 200
        result = req.json()
        assert type(result) is dict
        assert "pdps" in result
        assert pdp_id in result['pdps']

    req = requests.get(URL + "/pdp/{}".format(pdp_id))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "pdps" in result
    assert pdp_id in result['pdps']
    assert policy_id in pipeline


def map_to_keystone(pdp_id, keystone_project_id):
    req = requests.patch(URL + "/pdp/{}".format(pdp_id), json={"keystone_project_id": keystone_project_id},
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
    req = requests.delete(URL + "/pdp/{}".format(pdp_id))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "result" in result
    assert result["result"]

