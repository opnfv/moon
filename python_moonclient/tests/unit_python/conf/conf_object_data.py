
from .conf_all import *

OBJECT_DATA = {
    "object_data":[{
            "policy_id": "1",
            "category_id": "1",
            "data": {
                "1": {
                    "name": "name of the data",
                    "description": "description of the data"
                }
            }
    }]
}

POST_OBJECT_DATA = {
    "object_data":{
            "policy_id": "1",
            "category_id": "1",
            "data": {
                "1": {
                    "name": "name of the data",
                    "description": "description of the data"
                }
            }
    }
}

POST_OTHER_OBJECT_DATA = {
    "object_data":{
            "policy_id": "1",
            "category_id": "1",
            "data": {
                "2": {
                    "name": "name of the data",
                    "description": "description of the data"
                }
            }
    }
}

DELETE_OBJECT_DATA= {
    "object_data":[{
            "policy_id": "1",
            "category_id": "1",
            "data":{}
    }]
}


def conf_object_data(m):
    m.register_uri(
        'POST', 'http://manager:30001/policies/2/object_data/1',
        [{'headers': {'X-Subject-Token': "111111111"}, 'json': POST_OBJECT_DATA},
         {'headers': {'X-Subject-Token': "111111111"}, 'json': POST_OTHER_OBJECT_DATA}]
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/object_data/1',
        [{'headers': {'X-Subject-Token': "111111111"}, 'json': OBJECT_DATA},
         {'headers': {'X-Subject-Token': "111111111"}, 'json': DELETE_OBJECT_DATA}]
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/policies/2/object_data/1/1',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )
