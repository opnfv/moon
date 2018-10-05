import json
import api.utilities as utilities
from helpers import category_helper
from helpers import data_builder
from uuid import uuid4


def get_meta_rules(client):
    req = client.get("/meta_rules")
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def add_meta_rules(client, name, data=None):
    if not data:
        subject_category = category_helper.add_subject_category(
            value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
        subject_category_id = list(subject_category.keys())[0]
        object_category = category_helper.add_object_category(
            value={"name": "object category name" + uuid4().hex, "description": "description 1"})
        object_category_id = list(object_category.keys())[0]
        action_category = category_helper.add_action_category(
            value={"name": "action category name" + uuid4().hex, "description": "description 1"})
        action_category_id = list(action_category.keys())[0]

        data = {
            "name": name,
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }
    req = client.post("/meta_rules", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def add_meta_rules_without_category_ids(client, name):
    data = {
        "name": name + uuid4().hex,
        "subject_categories": [],
        "object_categories": [],
        "action_categories": []
    }
    req = client.post("/meta_rules", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def update_meta_rules(client, name, metaRuleId, data=None):
    if not data:
        subject_category = category_helper.add_subject_category(
            value={"name": "subject category name update" + uuid4().hex,
                   "description": "description 1"})
        subject_category_id = list(subject_category.keys())[0]
        object_category = category_helper.add_object_category(
            value={"name": "object category name update" + uuid4().hex,
                   "description": "description 1"})
        object_category_id = list(object_category.keys())[0]
        action_category = category_helper.add_action_category(
            value={"name": "action category name update" + uuid4().hex,
                   "description": "description 1"})
        action_category_id = list(action_category.keys())[0]
        data = {
            "name": name,
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }

    req = client.patch("/meta_rules/{}".format(metaRuleId), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def update_meta_rules_with_categories(client, name, data=None, meta_rule_id=None):
    if not meta_rule_id:
        subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
        data = {
            "name": name,
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }

    req = client.patch("/meta_rules/{}".format(meta_rule_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def delete_meta_rules(client, name):
    request, meta_rules = get_meta_rules(client)
    for key, value in meta_rules['meta_rules'].items():
        if value['name'] == name:
            return client.delete("/meta_rules/{}".format(key))


def delete_meta_rules_without_id(client):
    req = client.delete("/meta_rules/{}".format(""))
    return req


def test_get_meta_rules():
    client = utilities.register_client()
    req, meta_rules = get_meta_rules(client)
    assert req.status_code == 200
    assert isinstance(meta_rules, dict)
    assert "meta_rules" in meta_rules


def test_add_meta_rules():
    client = utilities.register_client()
    meta_rule_name = uuid4().hex
    req, meta_rules = add_meta_rules(client, meta_rule_name)
    assert req.status_code == 200
    assert isinstance(meta_rules, dict)
    value = list(meta_rules["meta_rules"].values())[0]
    assert "meta_rules" in meta_rules
    assert value['name'] == meta_rule_name


def test_add_two_meta_rules_with_same_categories_combination():
    client = utilities.register_client()
    meta_rule_name = uuid4().hex
    req, meta_rules = add_meta_rules(client, meta_rule_name)
    assert req.status_code == 200
    for meta_rule_id in meta_rules['meta_rules']:
        if meta_rules['meta_rules'][meta_rule_id]['name'] == meta_rule_name:
            data = meta_rules['meta_rules'][meta_rule_id]

    data['name'] = uuid4().hex
    req, meta_rules = add_meta_rules(client, name=data['name'], data=data)
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Meta Rule Existing'


def test_add_three_meta_rules_with_different_combination_but_similar_items():
    client = utilities.register_client()
    meta_rule_name1 = uuid4().hex
    req, meta_rules = add_meta_rules(client, meta_rule_name1)
    assert req.status_code == 200
    for meta_rule_id in meta_rules['meta_rules']:
        if meta_rules['meta_rules'][meta_rule_id]['name'] == meta_rule_name1:
            data = meta_rules['meta_rules'][meta_rule_id]
            break

    meta_rule_name2 = uuid4().hex

    req, meta_rules = add_meta_rules(client, meta_rule_name2)

    for meta_rule_id in meta_rules['meta_rules']:
        if meta_rules['meta_rules'][meta_rule_id]['name'] == meta_rule_name2:
            data['subject_categories'] += meta_rules['meta_rules'][meta_rule_id][
                'subject_categories']
            data['object_categories'] += meta_rules['meta_rules'][meta_rule_id]['object_categories']
            data['action_categories'] += meta_rules['meta_rules'][meta_rule_id]['action_categories']
            break

    data['name'] = uuid4().hex

    req, meta_rules = add_meta_rules(client, name=data['name'], data=data)
    assert req.status_code == 200


def test_add_two_meta_rules_with_different_combination_but_similar_items():
    client = utilities.register_client()
    meta_rule_name1 = uuid4().hex
    meta_rule_name2 = uuid4().hex

    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id1 = list(subject_category.keys())[0]

    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id1 = list(object_category.keys())[0]

    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id1 = list(action_category.keys())[0]

    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id2 = list(subject_category.keys())[0]

    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id2 = list(object_category.keys())[0]

    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id2 = list(action_category.keys())[0]

    data = {
        "name": meta_rule_name1,
        "subject_categories": [subject_category_id1, subject_category_id2],
        "object_categories": [object_category_id1, object_category_id2],
        "action_categories": [action_category_id1, action_category_id2]
    }
    req, meta_rules = add_meta_rules(client, meta_rule_name1, data=data)
    assert req.status_code == 200
    data = {
        "name": meta_rule_name2,
        "subject_categories": [subject_category_id2],
        "object_categories": [object_category_id1],
        "action_categories": [action_category_id2]
    }

    req, meta_rules = add_meta_rules(client, meta_rule_name1, data=data)
    assert req.status_code == 200


def test_add_meta_rule_with_existing_name_error():
    client = utilities.register_client()
    name = uuid4().hex
    req, meta_rules = add_meta_rules(client, name)
    assert req.status_code == 200
    req, meta_rules = add_meta_rules(client, name)
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Meta Rule Existing'


def test_add_meta_rules_with_forbidden_char_in_name():
    client = utilities.register_client()
    req, meta_rules = add_meta_rules(client, "<a>")
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Forbidden characters in string]"


def test_add_meta_rules_with_blank_name():
    client = utilities.register_client()
    req, meta_rules = add_meta_rules(client, "")
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Meta Rule Error'


def test_add_meta_rules_without_subject_categories():
    client = utilities.register_client()
    name_meta_rule = uuid4().hex
    req, meta_rules = add_meta_rules_without_category_ids(client, name_meta_rule)
    assert req.status_code == 200


def test_delete_meta_rules():
    client = utilities.register_client()
    name_meta_rule = uuid4().hex
    req, meta_rules = add_meta_rules_without_category_ids(client, name_meta_rule)
    meta_rule_id = next(iter(meta_rules['meta_rules']))
    req = delete_meta_rules(client, meta_rules['meta_rules'][meta_rule_id]['name'])
    assert req.status_code == 200


def test_delete_meta_rules_without_id():
    client = utilities.register_client()
    req = delete_meta_rules_without_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Meta Rule Unknown"


def test_update_meta_rules():
    client = utilities.register_client()
    req = add_meta_rules(client, "testuser")
    meta_rule_id = list(req[1]['meta_rules'])[0]
    req_update = update_meta_rules(client, "testuser", meta_rule_id)
    assert req_update[0].status_code == 200
    delete_meta_rules(client, "testuser")
    get_meta_rules(client)


def test_update_meta_rule_with_combination_existed():
    client = utilities.register_client()
    meta_rule_name1 = uuid4().hex
    req, meta_rules = add_meta_rules(client, meta_rule_name1)
    meta_rule_id1 = next(iter(meta_rules['meta_rules']))
    data1 = meta_rules['meta_rules'][meta_rule_id1]

    meta_rule_name2 = uuid4().hex
    req, meta_rules = add_meta_rules(client, meta_rule_name2)
    meta_rule_id2 = next(iter(meta_rules['meta_rules']))
    data2 = meta_rules['meta_rules'][meta_rule_id2]
    data1['name'] = data2['name']
    req_update = update_meta_rules(client, name=meta_rule_name2, metaRuleId=meta_rule_id2,
                                   data=data1)
    assert req_update[0].status_code == 409
    assert req_update[1]['message']== '409: Meta Rule Existing'


def test_update_meta_rule_with_different_combination_but_same_data():
    client = utilities.register_client()
    meta_rule_name1 = uuid4().hex
    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id1 = list(subject_category.keys())[0]
    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id1 = list(object_category.keys())[0]
    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id1 = list(action_category.keys())[0]
    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id2 = list(subject_category.keys())[0]
    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id2 = list(object_category.keys())[0]
    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id2 = list(action_category.keys())[0]

    data = {
        "name": meta_rule_name1,
        "subject_categories": [subject_category_id1, subject_category_id2],
        "object_categories": [object_category_id1, object_category_id2],
        "action_categories": [action_category_id1, action_category_id2]
    }
    req, meta_rules = add_meta_rules(client, meta_rule_name1, data=data)
    assert req.status_code == 200

    meta_rule_name2 = uuid4().hex
    req, meta_rules = add_meta_rules(client, meta_rule_name2)
    meta_rule_id2 = next(iter(meta_rules['meta_rules']))
    data2 = {
        "name": meta_rule_name2,
        "subject_categories": [subject_category_id1, subject_category_id2],
        "object_categories": [object_category_id1],
        "action_categories": [action_category_id1,action_category_id2]
    }

    req_update = update_meta_rules(client, name=meta_rule_name2, metaRuleId=meta_rule_id2,
                                   data=data2)
    assert req_update[0].status_code == 200


def test_update_meta_rules_without_id():
    client = utilities.register_client()
    req_update = update_meta_rules(client, "testuser", "")
    assert req_update[0].status_code == 400
    assert json.loads(req_update[0].data)["message"] == "400: Meta Rule Unknown"


def test_update_meta_rules_without_name():
    client = utilities.register_client()
    req_update = update_meta_rules(client, "<br/>", "1234567")
    assert req_update[0].status_code == 400
    assert json.loads(req_update[0].data)[
               "message"] == "Key: 'name', [Forbidden characters in string]"


def test_update_meta_rules_without_categories():
    client = utilities.register_client()
    req_update = update_meta_rules_with_categories(client, "testuser")
    assert req_update[0].status_code == 200


def test_update_meta_rules_with_empty_categories():
    client = utilities.register_client()
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser",
        "subject_categories": [""],
        "object_categories": [""],
        "action_categories": [""]
    }
    req_update = update_meta_rules_with_categories(client, "testuser", data=data,
                                                   meta_rule_id=meta_rule_id)
    assert req_update[0].status_code == 400
    assert req_update[1]['message'] == '400: Subject Category Unknown'


def test_update_meta_rules_with_empty_action_category():
    client = utilities.register_client()
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [""]
    }
    req_update = update_meta_rules_with_categories(client, "testuser", data=data,
                                                   meta_rule_id=meta_rule_id)
    assert req_update[0].status_code == 400
    assert req_update[1]['message'] == '400: Action Category Unknown'


def test_update_meta_rules_with_empty_object_category():
    client = utilities.register_client()
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser",
        "subject_categories": [subject_category_id],
        "object_categories": [""],
        "action_categories": [action_category_id]
    }
    req_update = update_meta_rules_with_categories(client, "testuser", data=data,
                                                   meta_rule_id=meta_rule_id)
    assert req_update[0].status_code == 400
    assert req_update[1]['message'] == '400: Object Category Unknown'


def test_update_meta_rules_with_categories_and_one_empty():
    client = utilities.register_client()
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser",
        "subject_categories": [subject_category_id, ""],
        "object_categories": [object_category_id, ""],
        "action_categories": [action_category_id, ""]
    }
    req_update = update_meta_rules_with_categories(client, "testuser", data=data,
                                                   meta_rule_id=meta_rule_id)
    assert req_update[0].status_code == 400
    assert req_update[1]['message'] == '400: Subject Category Unknown'
