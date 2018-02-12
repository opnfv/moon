
OBJECT_CATEGORIES = {
    "object_categories": {
        "1": {
            "name": "object_cat_1",
            "description": "description of the category"
        }
    }
}

POST_OBJECT_CATEGORIES = {
    "object_categories": {
        "1": {
            "name": "object_cat_1",
            "description": "description of the category"
        }
    }
}


def conf_object_categories(m):
    m.register_uri(
        'GET', 'http://manager:30001/object_categories',
        headers={'X-Subject-Token': "111111111"},
        json=OBJECT_CATEGORIES
    )
    m.register_uri(
        'POST', 'http://manager:30001/object_categories',
        headers={'X-Subject-Token': "111111111"},
        json=POST_OBJECT_CATEGORIES
    )
