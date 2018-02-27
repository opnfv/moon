import api.utilities as utilities
import json


def get_rules(client, policy_id):
    req = client.get("/policies/{}/rules".format(policy_id))
    rules = utilities.get_json(req.data)
    return req, rules


def add_rules(client, policy_id):
    data = {
        "meta_rule_id": "meta_rule_id1",
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
    policy_id = utilities.get_policy_id()
    client = utilities.register_client()
    req, rules = add_rules(client, policy_id)
    assert req.status_code == 200
    assert isinstance(rules, dict)
    value = rules["rules"]
    assert "rules" in rules
    id = list(value.keys())[0]
    assert value[id]["meta_rule_id"] == "meta_rule_id1"


def test_delete_rules():
    client = utilities.register_client()
    policy_id = utilities.get_policy_id()
    req, added_rules = get_rules(client, policy_id)
    id = added_rules["rules"]['rules'][0]['id']
    rules = delete_rules(client, policy_id, id)
    assert rules.status_code == 200
