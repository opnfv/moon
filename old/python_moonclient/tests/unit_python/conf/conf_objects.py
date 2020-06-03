from .conf_all import *

OBJECTS = {
    "objects":{
        "1": {
            "name": "name of the object",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["1"]
            }
    }
}

OBJECTS_AFTER_POST = {
    "objects":{
        "1": {
            "name": "name of the object",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["1"]
            },
        "2": {
            "name": "test_object",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": []
            }
    }
}

OBJECTS_AFTER_PATCH = {
    "objects":{
        "1": {
            "name": "name of the object",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["1"]
            },
        "2": {
            "name": "test_object",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["2"]
            }
    }
}


POST_OBJECTS = {
    "objects":{
        "2": {
            "name": "test_object",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": []
            }
    }
}

PATCH_OBJECTS = {
    "objects":{
        "2": {
            "name": "test_object",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["2"]
            }
    }
}

def conf_objects(m):
    m.register_uri(
        'GET', 'http://manager:30001/objects',
        [{'json': OBJECTS, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': OBJECTS_AFTER_POST, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': OBJECTS, 'headers': {'X-Subject-Token': "111111111"}}]
    )
    m.register_uri(
        'POST', 'http://manager:30001/objects',
        headers={'X-Subject-Token': "111111111"},
        json=POST_OBJECTS
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/objects/2',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )
    m.register_uri(
        'PATCH', 'http://manager:30001/policies/2/objects/2',
        headers={'X-Subject-Token': "111111111"},
        json=PATCH_OBJECTS
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/objects',
        headers={'X-Subject-Token': "111111111"},
        json=OBJECTS_AFTER_PATCH
    )
    m.register_uri(
        'POST', 'http://manager:30001/policies/2/objects',
        headers={'X-Subject-Token': "111111111"},
        json=POST_OBJECTS
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/objects/2',
        headers={'X-Subject-Token': "111111111"},
        json=PATCH_OBJECTS
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/policies/2/objects/2',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )
