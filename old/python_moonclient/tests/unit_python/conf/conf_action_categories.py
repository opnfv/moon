

ACTION_CATEGORIES = {
    "action_categories": {
        "1": {
            "name": "action_cat_1",
                "description": "description of the category"
        }
    }
}

POST_ACTION_CATEGORIES = {
    "action_categories": {
        "1": {
            "name": "action_cat_1",
            "description": "description of the category"
        }
    }
}


def conf_action_categories(m):
    m.register_uri(
        'GET', 'http://manager:30001/action_categories',
        headers={'X-Subject-Token': "111111111"},
        json=ACTION_CATEGORIES
    )
    m.register_uri(
        'POST', 'http://manager:30001/action_categories',
        headers={'X-Subject-Token': "111111111"},
        json=POST_ACTION_CATEGORIES
    )