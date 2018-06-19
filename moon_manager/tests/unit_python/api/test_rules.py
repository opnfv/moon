import api.utilities as utilities
import json
from helpers import data_builder as builder
from uuid import uuid4
from helpers import policy_helper


def get_rules(client, policy_id):
    req = client.get("/policies/{}/rules".format(policy_id))
    rules = utilities.get_json(req.data)
    return req, rules


def add_rules(client):
    sub_id, obj_id, act_id, meta_rule_id, policy_id = builder.create_new_policy("sub_cat" + uuid4().hex,
                                                                                  "obj_cat" + uuid4().hex,
                                                                                  "act_cat" + uuid4().hex)
    sub_data_id = builder.create_subject_data(policy_id, sub_id)
    obj_data_id = builder.create_object_data(policy_id, obj_id)
    act_data_id = builder.create_action_data(policy_id, act_id)
    data = {
        "meta_rule_id": meta_rule_id,
        "rule": [sub_data_id, obj_data_id, act_data_id],
        "instructions": (
            {"decision": "grant"},
        ),
        "enabled": True
    }
    req = client.post("/policies/{}/rules".format(policy_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    rules = utilities.get_json(req.data)
    return req, rules


def add_rules_without_policy_id(client):
    data = {
        "meta_rule_id": "meta_rule_id",
        "rule": ["sub_data_id", "obj_data_id", "act_data_id"],
        "instructions": (
            {"decision": "grant"},
        ),
        "enabled": True
    }
    req = client.post("/policies/{}/rules".format(None), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    rules = utilities.get_json(req.data)
    return req, rules


def add_rules_without_meta_rule_id(client, policy_id):
    data = {
        "meta_rule_id": "",
        "rule": ["subject_data_id2", "object_data_id2", "action_data_id2"],
        "instructions": (
            {"decision": "grant"},
        ),
        "enabled": True
    }
    req = client.post("/policies/{}/rules".format(policy_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    rules = utilities.get_json(req.data)
    return req, rules


def add_rules_without_rule(client, policy_id):
    data = {
        "meta_rule_id": "meta_rule_id1",
        "instructions": (
            {"decision": "grant"},
        ),
        "enabled": True
    }
    req = client.post("/policies/{}/rules".format(policy_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    rules = utilities.get_json(req.data)
    return req, rules


def delete_rules(client, policy_id, meta_rule_id):
    req = client.delete("/policies/{}/rules/{}".format(policy_id, meta_rule_id))
    return req


def test_get_rules():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, rules = get_rules(client, policy_id)
    assert req.status_code == 200
    assert isinstance(rules, dict)
    assert "rules" in rules
    return req, rules


def test_add_rules():
    client = utilities.register_client()
    req, rules = add_rules(client, )
    assert req.status_code == 200


def test_add_rules_without_policy_id():
    client = utilities.register_client()
    req, rules = add_rules_without_policy_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Policy Unknown"


def test_add_rules_without_meta_rule_id():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, rules = add_rules_without_meta_rule_id(client, policy_id)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'meta_rule_id', [Empty String]"


def test_add_rules_without_rule():
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, rules = add_rules_without_rule(client, policy_id)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == 'Invalid Key :rule not found'


def test_delete_rules_with_invalid_parameters():
    client = utilities.register_client()
    rules = delete_rules(client, "", "")
    assert rules.status_code == 404


def test_delete_rules_without_policy_id():
    client = utilities.register_client()
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy()
    sub_data_id = builder.create_subject_data(policy_id, subject_category_id)
    obj_data_id = builder.create_object_data(policy_id, object_category_id)
    act_data_id = builder.create_action_data(policy_id, action_category_id)
    data = {
        "meta_rule_id": meta_rule_id,
        "rule": [sub_data_id, obj_data_id, act_data_id],
        "instructions": (
            {"decision": "grant"},
        ),
        "enabled": True
    }
    client.post("/policies/{}/rules".format(policy_id), data=json.dumps(data),
                headers={'Content-Type': 'application/json'})
    req, added_rules = get_rules(client, policy_id)
    id = list(added_rules["rules"]["rules"])[0]["id"]
    rules = delete_rules(client, None, id)
    assert rules.status_code == 200
