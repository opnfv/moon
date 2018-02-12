from .conf_all import *


META_RULES = {
    "meta_rules": {
        "1": {
            "name": "test_meta_rule",
            "algorithm": "name of the meta rule algorithm",
            "subject_categories": ["1"],
            "object_categories": ["1"],
            "action_categories": ["1"]
        }
    }
}

POST_META_RULES = {
    "meta_rules": {
        "1": {
            "name": "test_meta_rule",
            "algorithm": "name of the meta rule algorithm",
            "subject_categories": ["1"],
            "object_categories": ["1"],
            "action_categories": ["1"]
        }
    }
}


def conf_meta_rules(m):
    m.register_uri(
            'GET', 'http://manager:30001/meta_rules',
            headers={'X-Subject-Token': "111111111"},
            json=META_RULES
        )
    m.register_uri(
        'POST', 'http://manager:30001/meta_rules',
        headers={'X-Subject-Token': "111111111"},
        json=POST_META_RULES
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/meta_rules/1',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )
