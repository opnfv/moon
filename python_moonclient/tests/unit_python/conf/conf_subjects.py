from .conf_all import *

SUBJECTS = {
    "subjects":{
        "1": {
            "name": "name of the subject",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["1"]
            }
    }
}

SUBJECTS_AFTER_POST= {
    "subjects":{
        "1": {
            "name": "name of the subject",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["1"]
            },
        "2": {
            "name": "test_subject",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": []
            }
    }
}

SUBJECTS_AFTER_PATCH= {
    "subjects":{
        "1": {
            "name": "name of the subject",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["1"]
            },
        "2": {
            "name": "test_subject",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["2"]
            }
    }
}

POST_SUBJECTS = {
    "subjects":{
        "2": {
            "name": "test_subject",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": []
            }
    }
}


PATCH_SUBJECTS = {
    "subjects":{
        "2": {
            "name": "test_subject",
            "keystone_id": "1",
            "description": "a description",
            "policy_list": ["2"]
            }
    }
}

def conf_subjects(m):
    m.register_uri(
        'GET', 'http://manager:30001/subjects',
        [{'json': SUBJECTS, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': SUBJECTS_AFTER_POST, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': SUBJECTS, 'headers': {'X-Subject-Token': "111111111"}}]
    )
    m.register_uri(
        'POST', 'http://manager:30001/subjects',
        headers={'X-Subject-Token': "111111111"},
        json=POST_SUBJECTS
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/subjects/2',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )
    m.register_uri(
        'PATCH', 'http://manager:30001/policies/2/subjects/2',
        headers={'X-Subject-Token': "111111111"},
        json=PATCH_SUBJECTS
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/subjects',
        headers={'X-Subject-Token': "111111111"},
        json=SUBJECTS_AFTER_PATCH
    )
    m.register_uri(
        'POST', 'http://manager:30001/policies/2/subjects',
        headers={'X-Subject-Token': "111111111"},
        json=POST_SUBJECTS
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/subjects/2',
        headers={'X-Subject-Token': "111111111"},
        json=PATCH_SUBJECTS
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/policies/2/subjects/2',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )