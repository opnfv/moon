import sys
import logging
import requests
from python_moonclient.core import config
from python_moonclient.core.check_tools import *


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
    req.raise_for_status()
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
        req.raise_for_status()
        TOKEN = req.headers['X-Subject-Token']
        HEADERS['X-Auth-Token'] = TOKEN
        req = requests.get("{}/projects".format(KEYSTONE_SERVER), headers=HEADERS)
    req.raise_for_status()
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
    req.raise_for_status()
    result = req.json()
    check_pdp_in_result(result)
    if pdp_id:
        check_pdp_name(pdp_template["name"], pdp_id, result)
    if keystone_project_id:
        check_pdp_project_id(keystone_project_id, pdp_id, result)
    return result


def add_pdp(name="test_pdp", policy_id=None):
    pdp_template['name'] = name
    if policy_id:
        pdp_template['security_pipeline'].append(policy_id)
    req = requests.post(URL + "/pdp", json=pdp_template, headers=HEADERS)
    logger.debug(req.status_code)
    logger.debug(req)
    req.raise_for_status()
    result = req.json()
    check_pdp_in_result(result)
    pdp_id = list(result['pdps'].keys())[0]
    check_pdp_name(pdp_template["name"], pdp_id, result)
    return pdp_id


def update_pdp(pdp_id, policy_id=None):
    req = requests.get(URL + "/pdp/{}".format(pdp_id))
    req.raise_for_status()
    result = req.json()
    check_pdp_id(pdp_id, result)
    pipeline = result['pdps'][pdp_id]["security_pipeline"]
    if policy_id not in pipeline:
        pipeline.append(policy_id)
        req = requests.patch(URL + "/pdp/{}".format(pdp_id),
                             json={"security_pipeline": pipeline})
        req.raise_for_status()
        result = req.json()
        check_pdp_id(pdp_id, result)

    req = requests.get(URL + "/pdp/{}".format(pdp_id))
    req.raise_for_status()
    result = req.json()
    check_pdp_id(pdp_id, result)
    check_policy_id_in_pipeline(pdp_id, pipeline)


def map_to_keystone(pdp_id, keystone_project_id):
    req = requests.patch(URL + "/pdp/{}".format(pdp_id),
                         json={"keystone_project_id": keystone_project_id},
                         headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_pdp_id(pdp_id, result)
    # assert "name" in result['pdps'][pdp_id]
    # assert pdp_template["name"] == result['pdps'][pdp_id]["name"]
    return pdp_id


def delete_pdp(pdp_id):
    req = requests.delete(URL + "/pdp/{}".format(pdp_id))
    req.raise_for_status()
    result = req.json()
    check_result(result)


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
