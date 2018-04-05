import json
import api.utilities as utilities


def get_meta_rules(client):
    req = client.get("/meta_rules")
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def add_meta_rules(client, name):
    data = {
        "name": name,
        "subject_categories": ["subject_category_id1",
                               "subject_category_id2"],
        "object_categories": ["object_category_id1"],
        "action_categories": ["action_category_id1"]
    }
    req = client.post("/meta_rules", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def add_meta_rules_without_subject_category_ids(client, name):
    data = {
        "name": name,
        "subject_categories": [],
        "object_categories": ["object_category_id1"],
        "action_categories": ["action_category_id1"]
    }
    req = client.post("/meta_rules", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def update_meta_rules(client, name, metaRuleId):
    data = {
        "name": name,
        "subject_categories": ["subject_category_id1_update",
                               "subject_category_id2_update"],
        "object_categories": ["object_category_id1_update"],
        "action_categories": ["action_category_id1_update"]
    }
    req = client.patch("/meta_rules/{}".format(metaRuleId), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def update_meta_rules_without_subject_category_ids(client, name):
    data = {
        "name": name,
        "subject_categories": [],
        "object_categories": ["object_category_id1"],
        "action_categories": ["action_category_id1"]
    }
    req = client.post("/meta_rules", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def delete_meta_rules(client, name):
    request, meta_rules = get_meta_rules(client)
    for key, value in meta_rules['meta_rules'].items():
        if value['name'] == name:
            req = client.delete("/meta_rules/{}".format(key))
            break
    return req


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
    req, meta_rules = add_meta_rules(client, "testuser")
    assert req.status_code == 200
    assert isinstance(meta_rules, dict)
    value = list(meta_rules["meta_rules"].values())[0]
    assert "meta_rules" in meta_rules
    assert value['name'] == "testuser"
    assert value["subject_categories"][0] == "subject_category_id1"
    assert value["object_categories"][0] == "object_category_id1"
    assert value["action_categories"][0] == "action_category_id1"


def test_add_meta_rules_with_empty_user():
    client = utilities.register_client()
    req, meta_rules = add_meta_rules(client, "")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "Empty String"


def test_add_meta_rules_with_user_contain_space():
    client = utilities.register_client()
    req, meta_rules = add_meta_rules(client, "test user")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "String contains space"


def test_add_meta_rules_without_subject_categories():
    client = utilities.register_client()
    req, meta_rules = add_meta_rules_without_subject_category_ids(client, "testuser")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == 'Empty Container'


def test_delete_meta_rules():
    client = utilities.register_client()
    req = delete_meta_rules(client, "testuser")
    assert req.status_code == 200


def test_delete_meta_rules_without_id():
    client = utilities.register_client()
    req = delete_meta_rules_without_id(client)
    assert req.status_code == 500


def test_update_meta_rules():
    client = utilities.register_client()
    req = add_meta_rules(client, "testuser")
    meta_rule_id = list(req[1]['meta_rules'])[0]
    req_update = update_meta_rules(client, "testuser", meta_rule_id)
    assert req_update[0].status_code == 200
    value = list(req_update[1]["meta_rules"].values())[0]
    assert value["subject_categories"][0] == "subject_category_id1_update"
    delete_meta_rules(client, "testuser")
    get_meta_rules(client)


def test_update_meta_rules_without_id():
    client = utilities.register_client()
    req_update = update_meta_rules(client, "testuser", "")
    assert req_update[0].status_code == 500


def test_update_meta_rules_without_user():
    client = utilities.register_client()
    req_update = update_meta_rules(client, "", "")
    assert req_update[0].status_code == 500
    assert json.loads(req_update[0].data)["message"] == "Empty String"


def test_update_meta_rules_without_subject_categories():
    client = utilities.register_client()
    req_update = update_meta_rules_without_subject_category_ids(client, "testuser")
    assert req_update[0].status_code == 500
    assert json.loads(req_update[0].data)["message"] == "Empty Container"
