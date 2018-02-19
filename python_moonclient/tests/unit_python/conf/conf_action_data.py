from .conf_all import *

ACTION_DATA = {
    "action_data":[{
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

POST_ACTION_DATA = {
    "action_data":{
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

POST_OTHER_ACTION_DATA = {
    "action_data":{
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

DELETE_ACTION_DATA= {
    "action_data":[{
            "policy_id": "1",
            "category_id": "1",
            "data":{}
    }]
}


def conf_action_data(m):
    m.register_uri(
        'POST', 'http://manager:30001/policies/2/action_data/1',
        [{'headers': {'X-Subject-Token': "111111111"}, 'json': POST_ACTION_DATA},
         {'headers': {'X-Subject-Token': "111111111"}, 'json': POST_OTHER_ACTION_DATA}]
    )
    m.register_uri(
        'GET', 'http://manager:30001/policies/2/action_data/1',
        [{'headers': {'X-Subject-Token': "111111111"}, 'json': ACTION_DATA},
         {'headers': {'X-Subject-Token': "111111111"}, 'json': DELETE_ACTION_DATA}]
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/policies/2/action_data/1/1',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )