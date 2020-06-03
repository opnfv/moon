from .conf_all import *

ACTIONS = {
    "actions":{
        "1": {
            "name": "name of the action",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["1"]
            }
    }
}

ACTIONS_AFTER_POST = {
    "actions":{
        "1": {
            "name": "name of the action",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["1"]
            },
        "2": {
            "name": "test_action",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": []
            }
    }
}

ACTIONS_AFTER_PATCH = {
    "actions":{
        "1": {
            "name": "name of the action",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["1"]
            },
        "2": {
            "name": "test_action",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["2"]
            }
    }
}


POST_ACTIONS = {
    "actions":{
        "2": {
            "name": "test_action",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": []
            }
    }
}

PATCH_ACTIONS = {
    "actions":{
        "2": {
            "name": "test_action",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["2"]
            }
    }
}

def conf_actions(m):
    m.register_uri(
        'GET', 'http://manager:30001/actions',
        headers={'X-Subject-Token': "111111111"},
        json=ACTIONS
    )
    m.register_uri(
        'POST', 'http://manager:30001/actions',
        headers={'X-Subject-Token': "111111111"},
        json=POST_ACTIONS
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/actions/2',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )
    m.register_uri(
        'PATCH', 'http://manager:30001/policies/2/actions/2',
        headers={'X-Subject-Token': "111111111"},
        json=PATCH_ACTIONS
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/actions',
        headers={'X-Subject-Token': "111111111"},
        json=ACTIONS_AFTER_PATCH
    )
    m.register_uri(
        'POST', 'http://manager:30001/policies/2/actions',
        headers={'X-Subject-Token': "111111111"},
        json=POST_ACTIONS
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/actions/2',
        headers={'X-Subject-Token': "111111111"},
        json=PATCH_ACTIONS
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/policies/2/actions/2',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )