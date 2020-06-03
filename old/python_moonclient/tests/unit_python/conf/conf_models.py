from .conf_all import *


MODELS = {
    "models": {
        "1": {
            "name": "model 1",
            "description": "description model 1",
            "meta_rules": [{
                "meta_rule_id": "1"
            }, {
                "meta_rule_id": "2"
            }]
        },
        "2": {
            "name": "model 2",
            "description": "description model 2",
            "meta_rules": ["2"]
        },
        "3": {
            "name": "test_model",
            "description": "description model 3",
            "meta_rules": ["2"]
        }
    }
}

POST_MODEL = {
    "models": {
        "3": {
            "name": "test_model",
            "description": "description model 3",
            "meta_rules": ["2"]
        }
    }
}

PATCH_MODEL = {
    "models": {
        "3": {
            "name": "test_model",
            "description": "description model 3",
            "meta_rules": ["2", "1"]
        }
    }
}


MODELS_AFTER_POST = {
"models": {
        "1": {
            "name": "model 1",
            "description": "description model 1",
            "meta_rules": [{
                "meta_rule_id": "1"
            }, {
                "meta_rule_id": "2"
            }]
        },
        "2": {
            "name": "model 2",
            "description": "description model 2",
            "meta_rules": ["2"]
        },
        "3": {
            "name": "test_model",
            "description": "description model 3",
            "meta_rules": ["1", "2"]
        }
    }
}


def conf_models(m):
    m.register_uri(
        'GET', 'http://manager:30001/models',
        [{'json': MODELS, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': MODELS_AFTER_POST, 'headers': {'X-Subject-Token': "111111111"}}]
    )
    m.register_uri(
        'POST', 'http://manager:30001/models',
        headers={'X-Subject-Token': "111111111"},
        json=POST_MODEL
    )
    m.register_uri(
        'PATCH', 'http://manager:30001/models/3',
        headers={'X-Subject-Token': "111111111"},
        json=PATCH_MODEL
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/models/3',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )