import logging
import copy
import requests
from python_moonclient.core import config
from python_moonclient.core.check_tools import *

LOGGER = logging.getLogger("moonclient.core.models")

URL = None
HEADERS = None

model_template = {
    "name": "test_model",
    "description": "test",
    "meta_rules": []
}

category_template = {
    "name": "name of the category",
    "description": "description of the category"
}

meta_rule_template = {
    "name": "test_meta_rule",
    "subject_categories": [],
    "object_categories": [],
    "action_categories": []
}


def init(consul_host, consul_port):
    conf_data = config.get_config_data(consul_host, consul_port)
    global URL, HEADERS
    URL = "http://{}:{}".format(
        conf_data['manager_host'],
        conf_data['manager_port'])
    URL = URL + "{}"
    HEADERS = {"content-type": "application/json"}


def check_model(model_id=None, do_check_model_name=True):
    req = requests.get(URL.format("/models"))
    req.raise_for_status()
    result = req.json()
    check_model_in_result(result)
    if model_id:
        check_model_name(model_template["name"], model_id, result, do_check_model_name)
    return result


def add_model(name=None):
    if name:
        model_template['name'] = name
    req = requests.post(URL.format("/models"), json=model_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_model_in_result(result)
    model_id = list(result['models'].keys())[0]
    check_model_name(model_template["name"], model_id, result, True)
    return model_id


def delete_model(model_id):
    req = requests.delete(URL.format("/models/{}".format(model_id)))
    req.raise_for_status()
    result = req.json()
    check_result(result)


def add_subject_category(name="subject_cat_1"):
    category_template["name"] = name
    req = requests.post(URL.format("/subject_categories"), json=category_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()

    check_subject_category_in_result(result)
    category_id = list(result['subject_categories'].keys())[0]
    check_optionnal_result(result)
    check_subject_categories_name(category_template["name"], category_id, result)
    return category_id


def check_subject_category(category_id=None):
    req = requests.get(URL.format("/subject_categories"))
    req.raise_for_status()
    result = req.json()

    check_subject_category_in_result(result)
    check_optionnal_result(result)
    if category_id is not None:
        check_subject_categories_name(category_template["name"], category_id, result)
    return result


def delete_subject_category(category_id):
    req = requests.delete(URL.format("/subject_categories/{}".format(category_id)))
    req.raise_for_status()
    result = req.json()
    check_optionnal_result(result)


def add_object_category(name="object_cat_1"):
    category_template["name"] = name
    req = requests.post(URL.format("/object_categories"), json=category_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_object_category_in_result(result)
    category_id = list(result['object_categories'].keys())[0]
    check_optionnal_result(result)
    check_object_categories_name(category_template["name"], category_id, result)
    return category_id


def check_object_category(category_id=None):
    req = requests.get(URL.format("/object_categories"))
    req.raise_for_status()
    result = req.json()
    check_object_category_in_result(result)
    check_optionnal_result(result)
    if category_id is not None:
        check_object_categories_name(category_template["name"], category_id, result)
    return result


def delete_object_category(category_id):
    req = requests.delete(URL.format("/object_categories/{}".format(category_id)))
    req.raise_for_status()
    result = req.json()
    check_optionnal_result(result)


def add_action_category(name="action_cat_1"):
    category_template["name"] = name
    req = requests.post(URL.format("/action_categories"), json=category_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_action_category_in_result(result)
    category_id = list(result['action_categories'].keys())[0]
    check_optionnal_result(result)
    check_action_categories_name(category_template["name"], category_id, result)
    return category_id


def check_action_category(category_id=None):
    req = requests.get(URL.format("/action_categories"))
    req.raise_for_status()
    result = req.json()
    print(result)
    check_action_category_in_result(result)
    check_optionnal_result(result)
    if category_id is not None:
        check_action_categories_name(category_template["name"], category_id, result)
    return result


def delete_action_category(category_id):
    req = requests.delete(URL.format("/action_categories/{}".format(category_id)))
    req.raise_for_status()
    result = req.json()
    check_optionnal_result(result)


def add_categories_and_meta_rule(name="test_meta_rule"):
    scat_id = add_subject_category()
    ocat_id = add_object_category()
    acat_id = add_action_category()
    _meta_rule_template = copy.deepcopy(meta_rule_template)
    _meta_rule_template["name"] = name
    _meta_rule_template["subject_categories"].append(scat_id)
    _meta_rule_template["object_categories"].append(ocat_id)
    _meta_rule_template["action_categories"].append(acat_id)
    req = requests.post(URL.format("/meta_rules"), json=_meta_rule_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_meta_rule_in_result(result)
    meta_rule_id = list(result['meta_rules'].keys())[0]
    check_optionnal_result(result)
    check_meta_rules_name(_meta_rule_template["name"], meta_rule_id, result)
    return meta_rule_id, scat_id, ocat_id, acat_id


def add_meta_rule(name="test_meta_rule", scat=[], ocat=[], acat=[]):
    _meta_rule_template = copy.deepcopy(meta_rule_template)
    _meta_rule_template["name"] = name
    _meta_rule_template["subject_categories"] = []
    _meta_rule_template["subject_categories"].extend(scat)
    _meta_rule_template["object_categories"] = []
    _meta_rule_template["object_categories"].extend(ocat)
    _meta_rule_template["action_categories"] = []
    _meta_rule_template["action_categories"].extend(acat)
    req = requests.post(URL.format("/meta_rules"), json=_meta_rule_template, headers=HEADERS)
    req.raise_for_status()
    result = req.json()
    check_meta_rule_in_result(result)
    meta_rule_id = list(result['meta_rules'].keys())[0]
    check_optionnal_result(result)
    check_meta_rules_name(_meta_rule_template["name"], meta_rule_id, result)
    return meta_rule_id


def check_meta_rule(meta_rule_id, scat_id=None, ocat_id=None, acat_id=None):
    req = requests.get(URL.format("/meta_rules"))
    req.raise_for_status()
    result = req.json()
    check_meta_rule_in_result(result)
    check_optionnal_result(result)
    if not meta_rule_id:
        return result
    check_meta_rules_name(None, meta_rule_id, result)
    if scat_id:
        check_scat_id_in_dict(scat_id, result['meta_rules'][meta_rule_id]["subject_categories"])
    if ocat_id:
        check_ocat_id_in_dict(ocat_id, result['meta_rules'][meta_rule_id]["object_categories"])
    if acat_id:
        check_acat_id_in_dict(acat_id, result['meta_rules'][meta_rule_id]["action_categories"])
    return result


def delete_meta_rule(meta_rule_id):
    req = requests.delete(URL.format("/meta_rules/{}".format(meta_rule_id)))
    req.raise_for_status()
    result = req.json()
    check_optionnal_result(result)


def add_meta_rule_to_model(model_id, meta_rule_id):
    model = check_model(model_id, do_check_model_name=False)['models']
    meta_rule_list = model[model_id]["meta_rules"]
    if meta_rule_id not in meta_rule_list:
        meta_rule_list.append(meta_rule_id)
        req = requests.patch(URL.format("/models/{}".format(model_id)),
                             json={"meta_rules": meta_rule_list},
                             headers=HEADERS)
        req.raise_for_status()
        result = req.json()
        check_model_in_result(result)
        model_id = list(result['models'].keys())[0]
        check_optionnal_result(result)
        check_meta_rules_list_in_model(meta_rule_list, model_id, result)


def create_model(scenario, model_id=None):
    LOGGER.info("Creating model {}".format(scenario.model_name))
    if not model_id:
        LOGGER.info("Add model")
        model_id = add_model(name=scenario.model_name)
    LOGGER.info("Add subject categories")
    for cat in scenario.subject_categories:
        scenario.subject_categories[cat] = add_subject_category(name=cat)
    LOGGER.info("Add object categories")
    for cat in scenario.object_categories:
        scenario.object_categories[cat] = add_object_category(name=cat)
    LOGGER.info("Add action categories")
    for cat in scenario.action_categories:
        scenario.action_categories[cat] = add_action_category(name=cat)
    sub_cat = []
    ob_cat = []
    act_cat = []
    meta_rule_list = []
    for item_name, item_value in scenario.meta_rule.items():
        for item in item_value["value"]:
            if item in scenario.subject_categories:
                sub_cat.append(scenario.subject_categories[item])
            elif item in scenario.object_categories:
                ob_cat.append(scenario.object_categories[item])
            elif item in scenario.action_categories:
                act_cat.append(scenario.action_categories[item])
        meta_rules = check_meta_rule(meta_rule_id=None)
        for _meta_rule_id, _meta_rule_value in meta_rules['meta_rules'].items():
            if _meta_rule_value['name'] == item_name:
                meta_rule_id = _meta_rule_id
                break
        else:
            LOGGER.info("Add meta rule")
            meta_rule_id = add_meta_rule(item_name, sub_cat, ob_cat, act_cat)
        item_value["id"] = meta_rule_id
        if meta_rule_id not in meta_rule_list:
            meta_rule_list.append(meta_rule_id)
    return model_id, meta_rule_list
