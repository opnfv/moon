import requests
import copy

URL = "http://172.18.0.11:38001{}"
HEADERS = {"content-type": "application/json"}

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


def check_model(model_id=None, check_model_name=True):
    req = requests.get(URL.format("/models"))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "models" in result
    if model_id:
        assert result["models"]
        assert model_id in result['models']
        assert "name" in result['models'][model_id]
        if check_model_name:
            assert model_template["name"] == result['models'][model_id]["name"]
    return result


def add_model(name=None):
    if name:
        model_template['name'] = name
    req = requests.post(URL.format("/models"), json=model_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    model_id = list(result['models'].keys())[0]
    if "result" in result:
        assert result["result"]
    assert "name" in result['models'][model_id]
    assert model_template["name"] == result['models'][model_id]["name"]
    return model_id


def delete_model(model_id):
    req = requests.delete(URL.format("/models/{}".format(model_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "result" in result
    assert result["result"]


def add_subject_category(name="subject_cat_1"):
    category_template["name"] = name
    req = requests.post(URL.format("/subject_categories"), json=category_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "subject_categories" in result
    category_id = list(result['subject_categories'].keys())[0]
    if "result" in result:
        assert result["result"]
    assert "name" in result['subject_categories'][category_id]
    assert category_template["name"] == result['subject_categories'][category_id]["name"]
    return category_id


def check_subject_category(category_id):
    req = requests.get(URL.format("/subject_categories"))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "subject_categories" in result
    if "result" in result:
        assert result["result"]
    assert category_id in result['subject_categories']
    assert "name" in result['subject_categories'][category_id]
    assert category_template["name"] == result['subject_categories'][category_id]["name"]


def delete_subject_category(category_id):
    req = requests.delete(URL.format("/subject_categories/{}".format(category_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    if "result" in result:
        assert result["result"]


def add_object_category(name="object_cat_1"):
    category_template["name"] = name
    req = requests.post(URL.format("/object_categories"), json=category_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "object_categories" in result
    category_id = list(result['object_categories'].keys())[0]
    if "result" in result:
        assert result["result"]
    assert "name" in result['object_categories'][category_id]
    assert category_template["name"] == result['object_categories'][category_id]["name"]
    return category_id


def check_object_category(category_id):
    req = requests.get(URL.format("/object_categories"))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "object_categories" in result
    if "result" in result:
        assert result["result"]
    assert category_id in result['object_categories']
    assert "name" in result['object_categories'][category_id]
    assert category_template["name"] == result['object_categories'][category_id]["name"]


def delete_object_category(category_id):
    req = requests.delete(URL.format("/object_categories/{}".format(category_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    if "result" in result:
        assert result["result"]


def add_action_category(name="action_cat_1"):
    category_template["name"] = name
    req = requests.post(URL.format("/action_categories"), json=category_template, headers=HEADERS)
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "action_categories" in result
    category_id = list(result['action_categories'].keys())[0]
    if "result" in result:
        assert result["result"]
    assert "name" in result['action_categories'][category_id]
    assert category_template["name"] == result['action_categories'][category_id]["name"]
    return category_id


def check_action_category(category_id):
    req = requests.get(URL.format("/action_categories"))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "action_categories" in result
    if "result" in result:
        assert result["result"]
    assert category_id in result['action_categories']
    assert "name" in result['action_categories'][category_id]
    assert category_template["name"] == result['action_categories'][category_id]["name"]


def delete_action_category(category_id):
    req = requests.delete(URL.format("/action_categories/{}".format(category_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    if "result" in result:
        assert result["result"]


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
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "meta_rules" in result
    meta_rule_id = list(result['meta_rules'].keys())[0]
    if "result" in result:
        assert result["result"]
    assert "name" in result['meta_rules'][meta_rule_id]
    assert _meta_rule_template["name"] == result['meta_rules'][meta_rule_id]["name"]
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
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "meta_rules" in result
    meta_rule_id = list(result['meta_rules'].keys())[0]
    if "result" in result:
        assert result["result"]
    assert "name" in result['meta_rules'][meta_rule_id]
    assert _meta_rule_template["name"] == result['meta_rules'][meta_rule_id]["name"]
    return meta_rule_id


def check_meta_rule(meta_rule_id, scat_id=None, ocat_id=None, acat_id=None):
    req = requests.get(URL.format("/meta_rules"))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "meta_rules" in result
    if "result" in result:
        assert result["result"]
    if not meta_rule_id:
        return result
    assert meta_rule_id in result['meta_rules']
    assert "name" in result['meta_rules'][meta_rule_id]
    if scat_id:
        assert scat_id in result['meta_rules'][meta_rule_id]["subject_categories"]
    if ocat_id:
        assert ocat_id in result['meta_rules'][meta_rule_id]["object_categories"]
    if acat_id:
        assert acat_id in result['meta_rules'][meta_rule_id]["action_categories"]


def delete_meta_rule(meta_rule_id):
    req = requests.delete(URL.format("/meta_rules/{}".format(meta_rule_id)))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    if "result" in result:
        assert result["result"]


def add_meta_rule_to_model(model_id, meta_rule_id):
    model = check_model(model_id, check_model_name=False)['models']
    meta_rule_list = model[model_id]["meta_rules"]
    if meta_rule_id not in meta_rule_list:
        meta_rule_list.append(meta_rule_id)
        req = requests.patch(URL.format("/models/{}".format(model_id)),
                             json={"meta_rules": meta_rule_list},
                             headers=HEADERS)
        assert req.status_code == 200
        result = req.json()
        assert type(result) is dict
        model_id = list(result['models'].keys())[0]
        if "result" in result:
            assert result["result"]
        assert "meta_rules" in result['models'][model_id]
        assert meta_rule_list == result['models'][model_id]["meta_rules"]
