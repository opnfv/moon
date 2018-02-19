from .conf_all import *

RULES = {
    "rules":{
        "policy_id": "2",
        "rules": [{
            "meta_rule_id": "1",
            "id": "1",
            "rule": ["1", "1", "1"]
        }]
    }
}

POST_RULES = {
        "rules":{
            "1":{
                "policy_id": "2",
                "meta_rule_id": "1",
                "rule": ["1", "1", "1"]
            }
        }
}

DELETE_RULES = {
    "rules":{
        "policy_id": "2",
        "rules": []
    }
}


def conf_rule_assignments(m):
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/rules',
        [{'headers': {'X-Subject-Token': "111111111"}, 'json': RULES},
         {'headers': {'X-Subject-Token': "111111111"}, 'json': DELETE_RULES}]
    )
    m.register_uri(
        'POST', 'http://manager:30001/policies/2/rules',
        [{'headers': {'X-Subject-Token': "111111111"}, 'json': POST_RULES}]
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/policies/2/rules/1',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )