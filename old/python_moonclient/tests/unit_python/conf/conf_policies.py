from .conf_all import *

POLICIES = {
    "policies":{
        "1": {
                "name": "test_policy",
                "model_id": "1",
                "genre": "authz",
                "description": "Description of the policy",
            }
    }
}

POLICIES_AFTER_POST= {
    "policies":{
        "1": {
                "name": "test_policy",
                "model_id": "1",
                "genre": "authz",
                "description": "Description of the policy",
            },
        "2": {
                "name": "test_policy",
                "model_id": "",
                "genre": "",
                "description": "Description of the policy",
            }
    }
}


POST_POLICIES ={
    "policies":{
        "2": {
                "name": "test_policy",
                "model_id": "",
                "genre": "",
                "description": "Description of the policy",
        }
    }
}


PATCH_POLICIES ={
    "policies":{
        "2": {
                "name": "test_policy",
                "model_id": "3",
                "genre": "authz",
                "description": "Description of the policy",
        }
    }
}


def conf_policies(m):
    m.register_uri(
        'GET', 'http://manager:30001/policies',
        [{'json': POLICIES, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': POLICIES_AFTER_POST, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': POLICIES, 'headers': {'X-Subject-Token': "111111111"}}]

    )
    m.register_uri(
        'POST', 'http://manager:30001/policies',
        headers={'X-Subject-Token': "111111111"},
        json=POST_POLICIES
    )
    m.register_uri(
        'PATCH', 'http://manager:30001/policies/2',
        headers={'X-Subject-Token': "111111111"},
        json=PATCH_POLICIES
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/policies/2',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )