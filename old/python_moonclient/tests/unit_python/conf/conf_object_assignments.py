from .conf_all import *

POST_OBJECT_ASSIGNMENT = {
    "object_assignments":{
        "1":{
            "policy_id": "1",
            "object_id": "2",
            "category_id": "1",
            "assignments": ["1"]
        }
    }
}

POST_OTHER_OBJECT_ASSIGNMENT = {
    "object_assignments":{
        "2":{
            "policy_id": "1",
            "object_id": "2",
            "category_id": "1",
            "assignments": ["2"]
        }
    }
}

DELETE_OBJECT_ASSIGNMENT = {
    "object_assignments":{

    }
}


def conf_object_assignments(m):
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/object_assignments/2/1/1',
        [{'headers': {'X-Subject-Token': "111111111"}, 'json': POST_OBJECT_ASSIGNMENT},
         {'headers': {'X-Subject-Token': "111111111"}, 'json': DELETE_OBJECT_ASSIGNMENT}]
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/object_assignments/2/1/2',
        headers={'X-Subject-Token': "111111111"},
        json=POST_OTHER_OBJECT_ASSIGNMENT
    )
    m.register_uri(
        'POST', 'http://manager:30001/policies/2/object_assignments',
        headers={'X-Subject-Token': "111111111"},
        json=POST_OBJECT_ASSIGNMENT
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/policies/2/object_assignments/2/1/1',
        json=RESULT_OK
    )