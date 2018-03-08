import logging
import requests
from python_moonclient.core import models, config
from python_moonclient.core.check_tools import *

logger = logging.getLogger("moonclient.core.policies")

URL = None
HEADERS = None

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
    conf_data = config.get_config_data(consul_host, consul_port)
    global URL, HEADERS
    URL = "http://{}:{}".format(
        conf_data['manager_host'],
        conf_data['manager_port'])
    URL = URL + "{}"
    HEADERS = {"content-type": "application/json"}


def check_policy(policy_id=None):
    req = requests.get(URL.format("/policies"))
    req.raise_for_status()
    result = req.json()
    check_policy_in_result(result)
    if policy_id:
        check_policy_name(policy_template["name"], policy_id, result)
    return result


def add_policy(name="test_policy", genre="authz"):
    policy_template["name"] = name
    policy_template["genre"] = genre
    req = requests.post(URL.format("/policies"), json=policy_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_policy_in_result(result)
    policy_id = list(result['policies'].keys())[0]
    check_optionnal_result(result)
    check_policy_name(policy_template["name"], policy_id, result)
    return policy_id


def update_policy(policy_id, model_id):
    req = requests.patch(URL.format("/policies/{}".format(policy_id)),
                         json={"model_id": model_id}, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_policy_in_result(result)
    policy_id = list(result['policies'].keys())[0]
    check_optionnal_result(result)
    check_policy_model_id(model_id, policy_id, result)


def delete_policy(policy_id):
    req = requests.delete(URL.format("/policies/{}".format(policy_id)))
    req.raise_for_status()
    result = req.json()
    check_result(result)


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
    req.raise_for_status()
    result = req.json()
    check_subject_in_result(result)
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
    req.raise_for_status()
    result = req.json()
    check_subject_name(subject_template["name"], subject_id, result)
    check_subject_policy(policy_id, result["subjects"][subject_id])
    check_subject_description(description, result["subjects"][subject_id])


def check_subject(subject_id=None, policy_id=None):
    if policy_id:
        req = requests.get(URL.format("/policies/{}/subjects".format(policy_id)))
    else:
        req = requests.get(URL.format("/subjects"))
    req.raise_for_status()
    result = req.json()
    check_subject_name(subject_template["name"], subject_id, result)
    check_subject_policy(policy_id, result["subjects"][subject_id])


def delete_subject(subject_id, policy_id=None):
    if policy_id:
        req = requests.delete(URL.format("/policies/{}/subjects/{}".format(policy_id, subject_id)))
    else:
        req = requests.delete(URL.format("/subjects/{}".format(subject_id)))
    req.raise_for_status()
    result = req.json()
    check_result(result)

    if policy_id:
        req = requests.get(URL.format("/policies/{}/subjects".format(policy_id)))
    else:
        req = requests.get(URL.format("/subjects"))
    req.raise_for_status()
    result = req.json()
    check_subject_in_result(result)
    if subject_id in result["subjects"]:
        check_subject_name(subject_template["name"], subject_id, result)
        check_subject_policy(policy_id, result["subjects"][subject_id])


def add_object(policy_id=None, name="test_object"):
    object_template['name'] = name
    if policy_id:
        req = requests.post(URL.format("/policies/{}/objects".format(policy_id)),
                            json=object_template, headers=HEADERS)
    else:
        req = requests.post(URL.format("/objects"), json=object_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_object_in_result(result)
    object_id = list(result['objects'].keys())[0]
    return object_id


def update_object(object_id, policy_id):
    req = requests.patch(URL.format("/policies/{}/objects/{}".format(policy_id, object_id)), json={})
    req.raise_for_status()
    result = req.json()
    check_object_in_result(result)
    check_object_name(object_template["name"] , object_id, result)
    check_object_policy(policy_id, result["objects"][object_id])


def check_object(object_id=None, policy_id=None):
    if policy_id:
        req = requests.get(URL.format("/policies/{}/objects".format(policy_id)))
    else:
        req = requests.get(URL.format("/objects"))
    req.raise_for_status()
    result = req.json()
    check_object_in_result(result)
    check_object_name(object_template["name"], object_id, result)
    if policy_id:
        check_object_policy(policy_id, result["objects"][object_id])


def delete_object(object_id, policy_id=None):
    if policy_id:
        req = requests.delete(URL.format("/policies/{}/objects/{}".format(policy_id, object_id)))
    else:
        req = requests.delete(URL.format("/objects/{}".format(object_id)))
    req.raise_for_status()
    result = req.json()
    check_result(result)

    if policy_id:
        req = requests.get(URL.format("/policies/{}/objects".format(policy_id)))
    else:
        req = requests.get(URL.format("/objects"))
    req.raise_for_status()
    result = req.json()
    check_object_in_result(result)
    if object_id in result["objects"]:
        check_object_name(object_template["name"], object_id, result)
        if policy_id:
            check_object_policy(policy_id, result["objects"][object_id])


def add_action(policy_id=None, name="test_action"):
    action_template['name'] = name
    if policy_id:
        req = requests.post(URL.format("/policies/{}/actions".format(policy_id)),
                            json=action_template, headers=HEADERS)
    else:
        req = requests.post(URL.format("/actions"), json=action_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_action_in_result(result)
    action_id = list(result['actions'].keys())[0]
    return action_id


def update_action(action_id, policy_id):
    req = requests.patch(URL.format("/policies/{}/actions/{}".format(policy_id, action_id)), json={})
    req.raise_for_status()
    result = req.json()
    check_action_in_result(result)
    check_action_name(action_template["name"], action_id, result)
    check_action_policy(policy_id, result["actions"][action_id])


def check_action(action_id=None, policy_id=None):
    if policy_id:
        req = requests.get(URL.format("/policies/{}/actions".format(policy_id)))
    else:
        req = requests.get(URL.format("/actions"))
    req.raise_for_status()
    result = req.json()
    check_action_in_result(result)
    check_action_name(action_template["name"], action_id, result)
    if policy_id:
        check_action_policy(policy_id, result["actions"][action_id])


def delete_action(action_id, policy_id=None):
    if policy_id:
        req = requests.delete(URL.format("/policies/{}/actions/{}".format(policy_id, action_id)))
    else:
        req = requests.delete(URL.format("/actions/{}".format(action_id)))
    req.raise_for_status()
    result = req.json()
    check_result(result)

    if policy_id:
        req = requests.get(URL.format("/policies/{}/actions".format(policy_id)))
    else:
        req = requests.get(URL.format("/actions"))
    req.raise_for_status()
    result = req.json()
    check_action_in_result(result)
    if action_id in result["actions"]:
        check_action_name(action_template["name"], action_id, result)
        if policy_id:
            check_action_policy(policy_id, result["actions"][action_id])


def add_subject_data(policy_id, category_id, name="subject_data1"):
    subject_data_template['name'] = name
    req = requests.post(URL.format("/policies/{}/subject_data/{}".format(policy_id, category_id)),
                        json=subject_data_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_subject_data_data(result)
    subject_id = list(result['subject_data']['data'].keys())[0]
    return subject_id


def check_subject_data(policy_id, data_id, category_id):
    req = requests.get(URL.format("/policies/{}/subject_data/{}".format(policy_id, category_id)))
    req.raise_for_status()
    result = req.json()
    print(result)
    if data_id is not None:
        check_id_in_subject_data_data(data_id, result)
    check_category_id_in_subject_data_data(category_id, result)
    return result


def delete_subject_data(policy_id, category_id, data_id):
    req = requests.delete(URL.format("/policies/{}/subject_data/{}/{}".format(policy_id, category_id, data_id)),
                          headers=HEADERS)
    req.raise_for_status()
    req = requests.get(URL.format("/policies/{}/subject_data/{}".format(policy_id, category_id)))
    req.raise_for_status()
    result = req.json()
    check_id_not_in_subject_data_data(data_id, result)
    check_category_id_in_subject_data_data(category_id, result)


def add_object_data(policy_id, category_id, name="object_data1"):
    object_data_template['name'] = name
    req = requests.post(URL.format("/policies/{}/object_data/{}".format(policy_id, category_id)),
                        json=object_data_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_object_data_data(result)
    object_id = list(result['object_data']['data'].keys())[0]
    return object_id


def check_object_data(policy_id, data_id, category_id):
    req = requests.get(URL.format("/policies/{}/object_data/{}".format(policy_id, category_id)))
    req.raise_for_status()
    result = req.json()
    if data_id is not None:
        check_id_in_object_data_data(data_id, result)
    check_category_id_in_object_data_data(category_id, result)
    return result

def delete_object_data(policy_id, category_id, data_id):
    req = requests.delete(URL.format("/policies/{}/object_data/{}/{}".format(policy_id, category_id, data_id)),
                          headers=HEADERS)
    req.raise_for_status()
    req = requests.get(URL.format("/policies/{}/object_data/{}".format(policy_id, category_id)))
    req.raise_for_status()
    result = req.json()
    check_id_not_in_object_data_data(data_id, result)
    check_category_id_in_object_data_data(category_id, result)


def add_action_data(policy_id, category_id, name="action_data1"):
    action_data_template['name'] = name
    req = requests.post(URL.format("/policies/{}/action_data/{}".format(policy_id, category_id)),
                        json=action_data_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_action_data_data(result)
    action_id = list(result['action_data']['data'].keys())[0]
    return action_id


def check_action_data(policy_id, data_id, category_id):
    req = requests.get(URL.format("/policies/{}/action_data/{}".format(policy_id, category_id)))
    req.raise_for_status()
    result = req.json()
    print(result)
    if data_id is not None:
        check_id_in_action_data_data(data_id, result)
    check_category_id_in_action_data_data(category_id, result)
    return result

def delete_action_data(policy_id, category_id, data_id):
    req = requests.delete(URL.format("/policies/{}/action_data/{}/{}".format(policy_id, category_id, data_id)),
                          headers=HEADERS)
    req.raise_for_status()
    req = requests.get(URL.format("/policies/{}/action_data/{}".format(policy_id, category_id)))
    req.raise_for_status()
    result = req.json()
    check_id_not_in_action_data_data(data_id, result)
    check_category_id_in_action_data_data(category_id, result)


def add_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id):
    req = requests.post(URL.format("/policies/{}/subject_assignments".format(policy_id)),
                        json={
                                "id": subject_id,
                                "category_id": subject_cat_id,
                                "data_id": subject_data_id
                            }, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_subject_assignment_in_result(result)


def check_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id):
    req = requests.get(URL.format("/policies/{}/subject_assignments/{}/{}/{}".format(
        policy_id, subject_id, subject_cat_id, subject_data_id)))
    req.raise_for_status()
    result = req.json()
    check_subject_assignment_in_result(result)
    check_subject_assignements(subject_id, subject_cat_id, subject_data_id, result)


def check_object_assignments(policy_id, object_id, object_cat_id, object_data_id):
    req = requests.get(URL.format("/policies/{}/object_assignments/{}/{}/{}".format(
        policy_id, object_id, object_cat_id, object_data_id)))
    req.raise_for_status()
    result = req.json()
    check_object_assignment_in_result(result)
    check_object_assignements(object_id, object_cat_id, object_data_id, result)


def check_action_assignments(policy_id, action_id, action_cat_id, action_data_id):
    req = requests.get(URL.format("/policies/{}/action_assignments/{}/{}/{}".format(
        policy_id, action_id, action_cat_id, action_data_id)))
    req.raise_for_status()
    result = req.json()
    check_action_assignment_in_result(result)
    check_action_assignements(action_id, action_cat_id, action_data_id, result)


def add_object_assignments(policy_id, object_id, object_cat_id, object_data_id):
    req = requests.post(URL.format("/policies/{}/object_assignments".format(policy_id)),
                        json={
                                "id": object_id,
                                "category_id": object_cat_id,
                                "data_id": object_data_id
                            }, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_object_assignment_in_result(result)


def add_action_assignments(policy_id, action_id, action_cat_id, action_data_id):
    req = requests.post(URL.format("/policies/{}/action_assignments".format(policy_id)),
                        json={
                                "id": action_id,
                                "category_id": action_cat_id,
                                "data_id": action_data_id
                            }, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_action_assignment_in_result(result)


def delete_subject_assignment(policy_id, subject_id, subject_cat_id, subject_data_id):
    req = requests.delete(URL.format("/policies/{}/subject_assignments/{}/{}/{}".format(
        policy_id, subject_id, subject_cat_id, subject_data_id)))
    req.raise_for_status()
    result = req.json()
    check_result(result)

    req = requests.get(URL.format("/policies/{}/subject_assignments/{}/{}/{}".format(
        policy_id, subject_id, subject_cat_id, subject_data_id)))
    req.raise_for_status()
    result = req.json()
    check_subject_assignment_in_result(result)
    check_not_subject_assignements(subject_id, subject_cat_id, subject_data_id, result)


def delete_object_assignment(policy_id, object_id, object_cat_id, object_data_id):
    req = requests.delete(URL.format("/policies/{}/object_assignments/{}/{}/{}".format(
        policy_id, object_id, object_cat_id, object_data_id)))
    req.raise_for_status()
    result = req.json()
    check_result(result)

    req = requests.get(URL.format("/policies/{}/object_assignments/{}/{}/{}".format(
        policy_id, object_id, object_cat_id, object_data_id)))
    req.raise_for_status()
    result = req.json()
    check_object_assignment_in_result(result)
    check_not_object_assignements(object_id, object_cat_id, object_data_id, result)


def delete_action_assignment(policy_id, action_id, action_cat_id, action_data_id):
    req = requests.delete(URL.format("/policies/{}/action_assignments/{}/{}/{}".format(
        policy_id, action_id, action_cat_id, action_data_id)))
    req.raise_for_status()
    result = req.json()
    check_result(result)

    req = requests.get(URL.format("/policies/{}/action_assignments/{}/{}/{}".format(
        policy_id, action_id, action_cat_id, action_data_id)))
    req.raise_for_status()
    result = req.json()
    check_action_assignment_in_result(result)
    check_not_action_assignements(action_id, action_cat_id, action_data_id, result)


def add_rule(policy_id, meta_rule_id, rule, instructions={"chain": [{"security_pipeline": "rbac"}]}):
    req = requests.post(URL.format("/policies/{}/rules".format(policy_id)),
                        json={
                            "meta_rule_id": meta_rule_id,
                            "rule": rule,
                            "instructions": instructions,
                            "enabled": True
                        },
                        headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_rule_in_result(result)
    rule_id = list(result["rules"].keys())[0]
    check_policy_id_in_dict(policy_id, result["rules"][rule_id])
    check_meta_rule_id_in_dict(meta_rule_id, result["rules"][rule_id])
    check_rule_in_dict(rule, result["rules"][rule_id])
    return rule_id


def check_rule(policy_id, meta_rule_id, rule_id, rule):
    req = requests.get(URL.format("/policies/{}/rules".format(policy_id)))
    req.raise_for_status()
    result = req.json()
    check_rule_in_result(result)
    check_policy_id_in_dict(policy_id, result["rules"])
    check_rule_id_in_list(meta_rule_id, rule_id, rule, result["rules"]["rules"])


def delete_rule(policy_id, rule_id):
    req = requests.delete(URL.format("/policies/{}/rules/{}".format(policy_id, rule_id)))
    req.raise_for_status()
    result = req.json()
    check_result(result)
    req = requests.get(URL.format("/policies/{}/rules".format(policy_id)))
    req.raise_for_status()
    result = req.json()
    check_rule_in_result(result)
    check_policy_id_in_dict(policy_id, result["rules"])
    check_rule_id_not_in_list(rule_id, result["rules"]["rules"])


def check_meta_rule():
    req = requests.get(URL.format("/meta_rules/"))
    req.raise_for_status()
    result = req.json()
    print(result)
    return result

def create_policy(scenario, model_id, meta_rule_list):
    logger.info("Creating policy {}".format(scenario.policy_name))
    _policies = check_policy()
    for _policy_id, _policy_value in _policies["policies"].items():
        if _policy_value['name'] == scenario.policy_name:
            policy_id = _policy_id
            break
    else:
        policy_id = add_policy(name=scenario.policy_name, genre=scenario.policy_genre)

    update_policy(policy_id, model_id)

    for meta_rule_id in meta_rule_list:
        logger.debug("add_meta_rule_to_model {} {}".format(model_id, meta_rule_id))
        models.add_meta_rule_to_model(model_id, meta_rule_id)

    logger.info("Add subject data")
    for subject_cat_name in scenario.subject_data:
        for subject_data_name in scenario.subject_data[subject_cat_name]:
            data_id = scenario.subject_data[subject_cat_name][subject_data_name] = add_subject_data(
                policy_id=policy_id,
                category_id=scenario.subject_categories[subject_cat_name], name=subject_data_name)
            scenario.subject_data[subject_cat_name][subject_data_name] = data_id
    logger.info("Add object data")
    for object_cat_name in scenario.object_data:
        for object_data_name in scenario.object_data[object_cat_name]:
            data_id = scenario.object_data[object_cat_name][object_data_name] = add_object_data(
                policy_id=policy_id,
                category_id=scenario.object_categories[object_cat_name], name=object_data_name)
            scenario.object_data[object_cat_name][object_data_name] = data_id
    logger.info("Add action data")
    for action_cat_name in scenario.action_data:
        for action_data_name in scenario.action_data[action_cat_name]:
            data_id = scenario.action_data[action_cat_name][action_data_name] = add_action_data(
                policy_id=policy_id,
                category_id=scenario.action_categories[action_cat_name], name=action_data_name)
            scenario.action_data[action_cat_name][action_data_name] = data_id

    logger.info("Add subjects")
    for name in scenario.subjects:
        scenario.subjects[name] = add_subject(policy_id, name=name)
    logger.info("Add objects")
    for name in scenario.objects:
        scenario.objects[name] = add_object(policy_id, name=name)
    logger.info("Add actions")
    for name in scenario.actions:
        scenario.actions[name] = add_action(policy_id, name=name)

    logger.info("Add subject assignments")
    for subject_name in scenario.subject_assignments:
        if type(scenario.subject_assignments[subject_name]) in (list, tuple):
            for items in scenario.subject_assignments[subject_name]:
                for subject_category_name in items:
                    subject_id = scenario.subjects[subject_name]
                    subject_cat_id = scenario.subject_categories[subject_category_name]
                    for data in scenario.subject_assignments[subject_name]:
                        subject_data_id = scenario.subject_data[subject_category_name][data[subject_category_name]]
                        add_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id)
        else:
            for subject_category_name in scenario.subject_assignments[subject_name]:
                subject_id = scenario.subjects[subject_name]
                subject_cat_id = scenario.subject_categories[subject_category_name]
                subject_data_id = scenario.subject_data[subject_category_name][scenario.subject_assignments[subject_name][subject_category_name]]
                add_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id)

    logger.info("Add object assignments")
    for object_name in scenario.object_assignments:
        if type(scenario.object_assignments[object_name]) in (list, tuple):
            for items in scenario.object_assignments[object_name]:
                for object_category_name in items:
                    object_id = scenario.objects[object_name]
                    object_cat_id = scenario.object_categories[object_category_name]
                    for data in scenario.object_assignments[object_name]:
                        object_data_id = scenario.object_data[object_category_name][data[object_category_name]]
                        add_object_assignments(policy_id, object_id, object_cat_id, object_data_id)
        else:
            for object_category_name in scenario.object_assignments[object_name]:
                object_id = scenario.objects[object_name]
                object_cat_id = scenario.object_categories[object_category_name]
                object_data_id = scenario.object_data[object_category_name][scenario.object_assignments[object_name][object_category_name]]
                add_object_assignments(policy_id, object_id, object_cat_id, object_data_id)

    logger.info("Add action assignments")
    for action_name in scenario.action_assignments:
        if type(scenario.action_assignments[action_name]) in (list, tuple):
            for items in scenario.action_assignments[action_name]:
                for action_category_name in items:
                    action_id = scenario.actions[action_name]
                    action_cat_id = scenario.action_categories[action_category_name]
                    for data in scenario.action_assignments[action_name]:
                        action_data_id = scenario.action_data[action_category_name][data[action_category_name]]
                        add_action_assignments(policy_id, action_id, action_cat_id, action_data_id)
        else:
            for action_category_name in scenario.action_assignments[action_name]:
                action_id = scenario.actions[action_name]
                action_cat_id = scenario.action_categories[action_category_name]
                action_data_id = scenario.action_data[action_category_name][scenario.action_assignments[action_name][action_category_name]]
                add_action_assignments(policy_id, action_id, action_cat_id, action_data_id)

    logger.info("Add rules")
    for meta_rule_name in scenario.rules:
        meta_rule_value = scenario.meta_rule[meta_rule_name]
        for rule in scenario.rules[meta_rule_name]:
            data_list = []
            _meta_rule = list(meta_rule_value["value"])
            for data_name in rule["rule"]:
                category_name = _meta_rule.pop(0)
                if category_name in scenario.subject_categories:
                    data_list.append(scenario.subject_data[category_name][data_name])
                elif category_name in scenario.object_categories:
                    data_list.append(scenario.object_data[category_name][data_name])
                elif category_name in scenario.action_categories:
                    data_list.append(scenario.action_data[category_name][data_name])
            instructions = rule["instructions"]
            add_rule(policy_id, meta_rule_value["id"], data_list, instructions)
    return policy_id

