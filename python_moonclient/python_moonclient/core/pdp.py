import sys
import logging
import requests
from python_moonclient.core import config

logger = logging.getLogger("python_moonclient.core.pdp")

URL = None
HEADERS = None
KEYSTONE_USER = None
KEYSTONE_PASSWORD = None
KEYSTONE_PROJECT = None
KEYSTONE_SERVER = None


pdp_template = {
    "name": "test_pdp",
    "security_pipeline": [],
    "keystone_project_id": None,
    "description": "test",
}


def init(consul_host, consul_port):
    conf_data = config.get_config_data(consul_host, consul_port)
    global URL, HEADERS, KEYSTONE_USER, KEYSTONE_PASSWORD, KEYSTONE_PROJECT, KEYSTONE_SERVER
    URL = "http://{}:{}".format(
        conf_data['manager_host'],
        conf_data['manager_port'])
    # URL = URL + "{}"
    HEADERS = {"content-type": "application/json"}
    KEYSTONE_USER = conf_data['keystone_user']
    KEYSTONE_PASSWORD = conf_data['keystone_password']
    KEYSTONE_PROJECT = conf_data['keystone_project']
    KEYSTONE_SERVER = conf_data['keystone_host']


def get_keystone_projects():
    global HEADERS
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


def get_keystone_id(pdp_name):
    keystone_project_id = None
    for pdp_key, pdp_value in check_pdp()["pdps"].items():
        if pdp_name:
            if pdp_name != pdp_value["name"]:
                continue
        if pdp_value['security_pipeline'] and pdp_value["keystone_project_id"]:
            logger.debug("Found pdp with keystone_project_id={}".format(pdp_value["keystone_project_id"]))
            keystone_project_id = pdp_value["keystone_project_id"]

    if not keystone_project_id:
        logger.error("Cannot find PDP with keystone project ID")
        sys.exit(1)
    return keystone_project_id


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
    req = requests.patch(URL + "/pdp/{}".format(pdp_id),
                         json={"keystone_project_id": keystone_project_id},
                         headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    if "result" in result:
        assert result["result"]
    assert pdp_id in result['pdps']
    # assert "name" in result['pdps'][pdp_id]
    # assert pdp_template["name"] == result['pdps'][pdp_id]["name"]
    return pdp_id


def delete_pdp(pdp_id):
    req = requests.delete(URL + "/pdp/{}".format(pdp_id))
    print(req)
    assert req.status_code == 200
    print('test')
    result = req.json()
    print(result)
    assert type(result) is dict
    assert "result" in result
    assert result["result"]


def create_pdp(scenario, policy_id=None, project_id=None):
    logger.info("Creating PDP {}".format(scenario.pdp_name))
    projects = get_keystone_projects()
    # if not project_id:
    #     for _project in projects['projects']:
    #         if _project['name'] == "admin":
    #             project_id = _project['id']
    # assert project_id
    pdps = check_pdp()["pdps"]
    for pdp_id, pdp_value in pdps.items():
        if scenario.pdp_name == pdp_value["name"]:
            update_pdp(pdp_id, policy_id=policy_id)
            logger.debug("Found existing PDP named {} (will add policy {})".format(scenario.pdp_name, policy_id))
            return pdp_id
    _pdp_id = add_pdp(name=scenario.pdp_name, policy_id=policy_id)
    # map_to_keystone(pdp_id=_pdp_id, keystone_project_id=project_id)
    return _pdp_id
