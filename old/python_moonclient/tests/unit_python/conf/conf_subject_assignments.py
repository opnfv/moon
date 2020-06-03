from .conf_all import *

POST_SUBJECT_ASSIGNMENT = {
    "subject_assignments":{
        "1":{
            "policy_id": "1",
            "subject_id": "2",
            "category_id": "1",
            "assignments": ["1"]
        }
    }
}

DELETE_SUBJECT_ASSIGNMENT = {
    "subject_assignments":{

    }
}

POST_OTHER_SUBJECT_ASSIGNMENT = {
    "subject_assignments":{
        "2":{
            "policy_id": "1",
            "subject_id": "2",
            "category_id": "1",
            "assignments": ["2"]
        }
    }
}


def conf_subject_assignments(m):
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/subject_assignments/2/1/1',
        [{'headers': {'X-Subject-Token': "111111111"}, 'json': POST_SUBJECT_ASSIGNMENT},
         {'headers': {'X-Subject-Token': "111111111"}, 'json': DELETE_SUBJECT_ASSIGNMENT}]
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/subject_assignments/2/1/2',
        headers={'X-Subject-Token': "111111111"},
        json=POST_OTHER_SUBJECT_ASSIGNMENT
    )
    m.register_uri(
        'POST', 'http://manager:30001/policies/2/subject_assignments',
        headers={'X-Subject-Token': "111111111"},
        json=POST_SUBJECT_ASSIGNMENT
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/policies/2/subject_assignments/2/1/1',
        json=RESULT_OK
    )