import logging
import requests
import utils.config

URL = None
HEADERS = None
FILE = open("/tmp/test.log", "w")

policy_template = {
    "name": "test_policy",
    "model_id": "",
    "genre": "authz",
    "description": "test",
}

subject_template = {
    "name": "test_subject",
    "description": "test",
    "email": "mail",
    "password": "my_pass",
}

object_template = {
    "name": "test_subject",
    "description": "test"
}

action_template = {
    "name": "test_subject",
    "description": "test"
}

subject_data_template = {
    "name": "subject_data1",
    "description": "description of the data subject"
}

object_data_template = {
    "name": "object_data1",
    "description": "description of the data subject"
}

action_data_template = {
    "name": "action_data1",
    "description": "description of the data subject"
}

subject_assignment_template = {
    "id": "",
    "category_id": "",
    "scope_id": ""
}


def init(consul_host, consul_port):
    conf_data = utils.config.get_conf_data(consul_host, consul_port)
    global URL, HEADERS
    URL = "http://{}:{}".format(
        conf_data['manager_hostname'],
        conf_data['manager_port'])
    URL = URL + "{}"
    HEADERS = {"content-type": "application/json"}


def check_policy(policy_id=None):
    req = requests.get(URL.format("/policies"))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "policies" in result
    if policy_id:
        assert result["policies"]
        assert policy_id in result['policies']
        assert "name" in result['policies'][policy_id]
        assert policy_template["name"] == result['policies'][policy_id]["name"]
    return result


def add_policy(name="test_policy", genre="authz"):
    policy_template["name"] = name
    policy_template["genre"] = genre
    req = requests.post(URL.format("/policies"), json=policy_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    policy_id = list(result['policies'].keys())[0]
    if "result" in result:
        assert result["result"]
    assert "name" in result['policies'][policy_id]
    assert policy_template["name"] == result['policies'][policy_id]["name"]
    return policy_id


def update_policy(policy_id, model_id):
    req = requests.patch(URL.format("/policies/{}".format(policy_id)),
                         json={"model_id": model_id}, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    policy_id = list(result['policies'].keys())[0]
    if "result" in result:
        assert result["result"]
    assert "model_id" in result['policies'][policy_id]
    assert model_id == result['policies'][policy_id]["model_id"]


def delete_policy(policy_id):
    req = requests.delete(URL.format("/policies/{}".format(policy_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "result" in result
    assert result["result"]


def add_subject(policy_id=None, name="test_subject"):
    subject_template['name'] = name
    if policy_id:
        logger.debug(URL.format("/policies/{}/subjects".format(policy_id)))
        req = requests.post(URL.format("/policies/{}/subjects".format(policy_id)),
                            json=subject_template, headers=HEADERS)
    else:
        logger.debug(URL.format("/subjects"))
        req = requests.post(URL.format("/subjects"), json=subject_template, headers=HEADERS)
    logger.debug(req.text)
    assert req.status_code == 200
    result = req.json()
    assert "subjects" in result
    subject_id = list(result['subjects'].keys())[0]
    return subject_id


def update_subject(subject_id, policy_id=None, description=None):
    if policy_id and not description:
        req = requests.patch(URL.format("/policies/{}/subjects/{}".format(policy_id, subject_id)),
                             json={})
    elif policy_id and description:
        req = requests.patch(URL.format("/policies/{}/subjects/{}".format(policy_id, subject_id)),
                             json={"description": description})
    else:
        req = requests.patch(URL.format("/subjects/{}".format(subject_id)),
                             json={"description": description})
    assert req.status_code == 200
    result = req.json()
    assert "subjects" in result
    assert "name" in result["subjects"][subject_id]
    assert subject_template["name"] == result["subjects"][subject_id]["name"]
    assert "policy_list" in result["subjects"][subject_id]
    if policy_id:
        assert policy_id in result["subjects"][subject_id]["policy_list"]
    if description:
        assert description in result["subjects"][subject_id]["description"]


def check_subject(subject_id=None, policy_id=None):
    if policy_id:
        req = requests.get(URL.format("/policies/{}/subjects".format(policy_id)))
    else:
        req = requests.get(URL.format("/subjects"))
    assert req.status_code == 200
    result = req.json()
    assert "subjects" in result
    assert "name" in result["subjects"][subject_id]
    assert subject_template["name"] == result["subjects"][subject_id]["name"]
    if policy_id:
        assert "policy_list" in result["subjects"][subject_id]
        assert policy_id in result["subjects"][subject_id]["policy_list"]


def delete_subject(subject_id, policy_id=None):
    if policy_id:
        req = requests.delete(URL.format("/policies/{}/subjects/{}".format(policy_id, subject_id)))
    else:
        req = requests.delete(URL.format("/subjects/{}".format(subject_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "result" in result
    assert result["result"]

    if policy_id:
        req = requests.get(URL.format("/policies/{}/subjects".format(policy_id)))
    else:
        req = requests.get(URL.format("/subjects"))
    assert req.status_code == 200
    result = req.json()
    assert "subjects" in result
    if subject_id in result["subjects"]:
        assert "name" in result["subjects"][subject_id]
        assert subject_template["name"] == result["subjects"][subject_id]["name"]
        if policy_id:
            assert "policy_list" in result["subjects"][subject_id]
            assert policy_id not in result["subjects"][subject_id]["policy_list"]


def add_object(policy_id=None, name="test_object"):
    object_template['name'] = name
    if policy_id:
        req = requests.post(URL.format("/policies/{}/objects".format(policy_id)),
                            json=object_template, headers=HEADERS)
    else:
        req = requests.post(URL.format("/objects"), json=object_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert "objects" in result
    object_id = list(result['objects'].keys())[0]
    return object_id


def update_object(object_id, policy_id):
    req = requests.patch(URL.format("/policies/{}/objects/{}".format(policy_id, object_id)), json={})
    assert req.status_code == 200
    result = req.json()
    assert "objects" in result
    assert "name" in result["objects"][object_id]
    assert object_template["name"] == result["objects"][object_id]["name"]
    assert "policy_list" in result["objects"][object_id]
    assert policy_id in result["objects"][object_id]["policy_list"]


def check_object(object_id=None, policy_id=None):
    if policy_id:
        req = requests.get(URL.format("/policies/{}/objects".format(policy_id)))
    else:
        req = requests.get(URL.format("/objects"))
    assert req.status_code == 200
    result = req.json()
    assert "objects" in result
    assert "name" in result["objects"][object_id]
    assert object_template["name"] == result["objects"][object_id]["name"]
    if policy_id:
        assert "policy_list" in result["objects"][object_id]
        assert policy_id in result["objects"][object_id]["policy_list"]


def delete_object(object_id, policy_id=None):
    if policy_id:
        req = requests.delete(URL.format("/policies/{}/objects/{}".format(policy_id, object_id)))
    else:
        req = requests.delete(URL.format("/objects/{}".format(object_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "result" in result
    assert result["result"]

    if policy_id:
        req = requests.get(URL.format("/policies/{}/objects".format(policy_id)))
    else:
        req = requests.get(URL.format("/objects"))
    assert req.status_code == 200
    result = req.json()
    assert "objects" in result
    if object_id in result["objects"]:
        assert "name" in result["objects"][object_id]
        assert object_template["name"] == result["objects"][object_id]["name"]
        if policy_id:
            assert "policy_list" in result["objects"][object_id]
            assert policy_id not in result["objects"][object_id]["policy_list"]


def add_action(policy_id=None, name="test_action"):
    action_template['name'] = name
    if policy_id:
        req = requests.post(URL.format("/policies/{}/actions".format(policy_id)),
                            json=action_template, headers=HEADERS)
    else:
        req = requests.post(URL.format("/actions"), json=action_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert "actions" in result
    action_id = list(result['actions'].keys())[0]
    return action_id


def update_action(action_id, policy_id):
    req = requests.patch(URL.format("/policies/{}/actions/{}".format(policy_id, action_id)), json={})
    assert req.status_code == 200
    result = req.json()
    assert "actions" in result
    assert "name" in result["actions"][action_id]
    assert action_template["name"] == result["actions"][action_id]["name"]
    assert "policy_list" in result["actions"][action_id]
    assert policy_id in result["actions"][action_id]["policy_list"]


def check_action(action_id=None, policy_id=None):
    if policy_id:
        req = requests.get(URL.format("/policies/{}/actions".format(policy_id)))
    else:
        req = requests.get(URL.format("/actions"))
    assert req.status_code == 200
    result = req.json()
    assert "actions" in result
    assert "name" in result["actions"][action_id]
    assert action_template["name"] == result["actions"][action_id]["name"]
    if policy_id:
        assert "policy_list" in result["actions"][action_id]
        assert policy_id in result["actions"][action_id]["policy_list"]


def delete_action(action_id, policy_id=None):
    if policy_id:
        req = requests.delete(URL.format("/policies/{}/actions/{}".format(policy_id, action_id)))
    else:
        req = requests.delete(URL.format("/actions/{}".format(action_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "result" in result
    assert result["result"]

    if policy_id:
        req = requests.get(URL.format("/policies/{}/actions".format(policy_id)))
    else:
        req = requests.get(URL.format("/actions"))
    assert req.status_code == 200
    result = req.json()
    assert "actions" in result
    if action_id in result["actions"]:
        assert "name" in result["actions"][action_id]
        assert action_template["name"] == result["actions"][action_id]["name"]
        if policy_id:
            assert "policy_list" in result["actions"][action_id]
            assert policy_id not in result["actions"][action_id]["policy_list"]


def add_subject_data(policy_id, category_id, name="subject_data1"):
    subject_data_template['name'] = name
    req = requests.post(URL.format("/policies/{}/subject_data/{}".format(policy_id, category_id)),
                        json=subject_data_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert "subject_data" in result
    subject_id = list(result['subject_data']['data'].keys())[0]
    return subject_id


def check_subject_data(policy_id, data_id, category_id):
    req = requests.get(URL.format("/policies/{}/subject_data/{}".format(policy_id, category_id)))
    assert req.status_code == 200
    result = req.json()
    assert "subject_data" in result
    for _data in result['subject_data']:
        assert data_id in list(_data['data'].keys())
        assert category_id == _data["category_id"]


def delete_subject_data(policy_id, category_id, data_id):
    req = requests.delete(URL.format("/policies/{}/subject_data/{}/{}".format(policy_id, category_id, data_id)),
                          headers=HEADERS)
    assert req.status_code == 200
    req = requests.get(URL.format("/policies/{}/subject_data/{}".format(policy_id, category_id)))
    assert req.status_code == 200
    result = req.json()
    assert "subject_data" in result
    for _data in result['subject_data']:
        assert data_id not in list(_data['data'].keys())
        assert category_id == _data["category_id"]


def add_object_data(policy_id, category_id, name="object_data1"):
    object_data_template['name'] = name
    req = requests.post(URL.format("/policies/{}/object_data/{}".format(policy_id, category_id)),
                        json=object_data_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert "object_data" in result
    object_id = list(result['object_data']['data'].keys())[0]
    return object_id


def check_object_data(policy_id, data_id, category_id):
    req = requests.get(URL.format("/policies/{}/object_data/{}".format(policy_id, category_id)))
    assert req.status_code == 200
    result = req.json()
    assert "object_data" in result
    for _data in result['object_data']:
        assert data_id in list(_data['data'].keys())
        assert category_id == _data["category_id"]


def delete_object_data(policy_id, category_id, data_id):
    req = requests.delete(URL.format("/policies/{}/object_data/{}/{}".format(policy_id, category_id, data_id)),
                          headers=HEADERS)
    assert req.status_code == 200
    req = requests.get(URL.format("/policies/{}/object_data/{}".format(policy_id, category_id)))
    assert req.status_code == 200
    result = req.json()
    assert "object_data" in result
    for _data in result['object_data']:
        assert data_id not in list(_data['data'].keys())
        assert category_id == _data["category_id"]


def add_action_data(policy_id, category_id, name="action_data1"):
    action_data_template['name'] = name
    req = requests.post(URL.format("/policies/{}/action_data/{}".format(policy_id, category_id)),
                        json=action_data_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert "action_data" in result
    action_id = list(result['action_data']['data'].keys())[0]
    return action_id


def check_action_data(policy_id, data_id, category_id):
    req = requests.get(URL.format("/policies/{}/action_data/{}".format(policy_id, category_id)))
    assert req.status_code == 200
    result = req.json()
    assert "action_data" in result
    for _data in result['action_data']:
        assert data_id in list(_data['data'].keys())
        assert category_id == _data["category_id"]


def delete_action_data(policy_id, category_id, data_id):
    req = requests.delete(URL.format("/policies/{}/action_data/{}/{}".format(policy_id, category_id, data_id)),
                          headers=HEADERS)
    assert req.status_code == 200
    req = requests.get(URL.format("/policies/{}/action_data/{}".format(policy_id, category_id)))
    assert req.status_code == 200
    result = req.json()
    assert "action_data" in result
    for _data in result['action_data']:
        assert data_id not in list(_data['data'].keys())
        assert category_id == _data["category_id"]


def add_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id):
    req = requests.post(URL.format("/policies/{}/subject_assignments".format(policy_id)),
                        json={
                                "id": subject_id,
                                "category_id": subject_cat_id,
                                "data_id": subject_data_id
                            }, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert "subject_assignments" in result
    assert result["subject_assignments"]


def check_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id):
    req = requests.get(URL.format("/policies/{}/subject_assignments/{}/{}/{}".format(
        policy_id, subject_id, subject_cat_id, subject_data_id)))
    assert req.status_code == 200
    result = req.json()
    assert "subject_assignments" in result
    assert result["subject_assignments"]
    for key in result["subject_assignments"]:
        assert "subject_id" in result["subject_assignments"][key]
        assert "category_id" in result["subject_assignments"][key]
        assert "assignments" in result["subject_assignments"][key]
        if result["subject_assignments"][key]['subject_id'] == subject_id and \
                result["subject_assignments"][key]["category_id"] == subject_cat_id:
            assert subject_data_id in result["subject_assignments"][key]["assignments"]


def check_object_assignments(policy_id, object_id, object_cat_id, object_data_id):
    req = requests.get(URL.format("/policies/{}/object_assignments/{}/{}/{}".format(
        policy_id, object_id, object_cat_id, object_data_id)))
    assert req.status_code == 200
    result = req.json()
    assert "object_assignments" in result
    assert result["object_assignments"]
    for key in result["object_assignments"]:
        assert "object_id" in result["object_assignments"][key]
        assert "category_id" in result["object_assignments"][key]
        assert "assignments" in result["object_assignments"][key]
        if result["object_assignments"][key]['object_id'] == object_id and \
                result["object_assignments"][key]["category_id"] == object_cat_id:
            assert object_data_id in result["object_assignments"][key]["assignments"]


def check_action_assignments(policy_id, action_id, action_cat_id, action_data_id):
    req = requests.get(URL.format("/policies/{}/action_assignments/{}/{}/{}".format(
        policy_id, action_id, action_cat_id, action_data_id)))
    assert req.status_code == 200
    result = req.json()
    assert "action_assignments" in result
    assert result["action_assignments"]
    for key in result["action_assignments"]:
        assert "action_id" in result["action_assignments"][key]
        assert "category_id" in result["action_assignments"][key]
        assert "assignments" in result["action_assignments"][key]
        if result["action_assignments"][key]['action_id'] == action_id and \
                result["action_assignments"][key]["category_id"] == action_cat_id:
            assert action_data_id in result["action_assignments"][key]["assignments"]


def add_object_assignments(policy_id, object_id, object_cat_id, object_data_id):
    req = requests.post(URL.format("/policies/{}/object_assignments".format(policy_id)),
                        json={
                                "id": object_id,
                                "category_id": object_cat_id,
                                "data_id": object_data_id
                            }, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert "object_assignments" in result
    assert result["object_assignments"]


def add_action_assignments(policy_id, action_id, action_cat_id, action_data_id):
    req = requests.post(URL.format("/policies/{}/action_assignments".format(policy_id)),
                        json={
                                "id": action_id,
                                "category_id": action_cat_id,
                                "data_id": action_data_id
                            }, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert "action_assignments" in result
    assert result["action_assignments"]


def delete_subject_assignment(policy_id, subject_id, subject_cat_id, subject_data_id):
    req = requests.delete(URL.format("/policies/{}/subject_assignments/{}/{}/{}".format(
        policy_id, subject_id, subject_cat_id, subject_data_id)))
    assert req.status_code == 200
    result = req.json()
    assert "result" in result
    assert result["result"]

    req = requests.get(URL.format("/policies/{}/subject_assignments/{}/{}/{}".format(
        policy_id, subject_id, subject_cat_id, subject_data_id)))
    assert req.status_code == 200
    result = req.json()
    assert "subject_assignments" in result
    assert result["subject_assignments"]
    for key in result["subject_assignments"]:
        assert "subject_id" in result["subject_assignments"][key]
        assert "category_id" in result["subject_assignments"][key]
        assert "assignments" in result["subject_assignments"][key]
        if result["subject_assignments"][key]['subject_id'] == subject_id and \
                result["subject_assignments"][key]["category_id"] == subject_cat_id:
            assert subject_data_id not in result["subject_assignments"][key]["assignments"]


def delete_object_assignment(policy_id, object_id, object_cat_id, object_data_id):
    req = requests.delete(URL.format("/policies/{}/object_assignments/{}/{}/{}".format(
        policy_id, object_id, object_cat_id, object_data_id)))
    assert req.status_code == 200
    result = req.json()
    assert "result" in result
    assert result["result"]

    req = requests.get(URL.format("/policies/{}/object_assignments/{}/{}/{}".format(
        policy_id, object_id, object_cat_id, object_data_id)))
    assert req.status_code == 200
    result = req.json()
    assert "object_assignments" in result
    assert result["object_assignments"]
    for key in result["object_assignments"]:
        assert "object_id" in result["object_assignments"][key]
        assert "category_id" in result["object_assignments"][key]
        assert "assignments" in result["object_assignments"][key]
        if result["object_assignments"][key]['object_id'] == object_id and \
                result["object_assignments"][key]["category_id"] == object_cat_id:
            assert object_data_id not in result["object_assignments"][key]["assignments"]


def delete_action_assignment(policy_id, action_id, action_cat_id, action_data_id):
    req = requests.delete(URL.format("/policies/{}/action_assignments/{}/{}/{}".format(
        policy_id, action_id, action_cat_id, action_data_id)))
    assert req.status_code == 200
    result = req.json()
    assert "result" in result
    assert result["result"]

    req = requests.get(URL.format("/policies/{}/action_assignments/{}/{}/{}".format(
        policy_id, action_id, action_cat_id, action_data_id)))
    assert req.status_code == 200
    result = req.json()
    assert "action_assignments" in result
    assert result["action_assignments"]
    for key in result["action_assignments"]:
        assert "action_id" in result["action_assignments"][key]
        assert "category_id" in result["action_assignments"][key]
        assert "assignments" in result["action_assignments"][key]
        if result["action_assignments"][key]['action_id'] == action_id and \
                result["action_assignments"][key]["category_id"] == action_cat_id:
            assert action_data_id not in result["action_assignments"][key]["assignments"]


def add_rule(policy_id, meta_rule_id, rule, instructions={"chain": [{"security_pipeline": "rbac"}]}):
    req = requests.post(URL.format("/policies/{}/rules".format(policy_id)),
                        json={
                            "meta_rule_id": meta_rule_id,
                            "rule": rule,
                            "instructions": instructions,
                            "enabled": True
                        },
                        headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert "rules" in result
    try:
        rule_id = list(result["rules"].keys())[0]
    except Exception as e:
        return False
    assert "policy_id" in result["rules"][rule_id]
    assert policy_id == result["rules"][rule_id]["policy_id"]
    assert "meta_rule_id" in result["rules"][rule_id]
    assert meta_rule_id == result["rules"][rule_id]["meta_rule_id"]
    assert rule == result["rules"][rule_id]["rule"]
    return rule_id


def check_rule(policy_id, meta_rule_id, rule_id, rule):
    req = requests.get(URL.format("/policies/{}/rules".format(policy_id)))
    assert req.status_code == 200
    result = req.json()
    assert "rules" in result
    assert "policy_id" in result["rules"]
    assert policy_id == result["rules"]["policy_id"]
    for item in result["rules"]["rules"]:
        assert "meta_rule_id" in item
        if meta_rule_id == item["meta_rule_id"]:
            if rule_id == item["id"]:
                assert rule == item["rule"]


def delete_rule(policy_id, rule_id):
    req = requests.delete(URL.format("/policies/{}/rules/{}".format(policy_id, rule_id)))
    assert req.status_code == 200
    result = req.json()
    assert "result" in result
    assert result["result"]

    req = requests.get(URL.format("/policies/{}/rules".format(policy_id)))
    assert req.status_code == 200
    result = req.json()
    assert "rules" in result
    assert "policy_id" in result["rules"]
    assert policy_id == result["rules"]["policy_id"]
    found_rule = False
    for item in result["rules"]["rules"]:
        if rule_id == item["id"]:
            found_rule = True
    assert not found_rule
