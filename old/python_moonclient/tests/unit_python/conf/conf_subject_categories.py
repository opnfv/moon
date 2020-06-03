
SUBJECT_CATEGORIES = {
    "subject_categories": {
        "1": {
            "name": "subject_cat_1",
            "description": "description of the category"
        }
    }
}

POST_SUBJECT_CATEGORIES = {
    "subject_categories": {
        "1": {
            "name": "subject_cat_1",
            "description": "description of the category"
        }
    }
}

def conf_subject_categories(m):
    m.register_uri(
        'GET', 'http://manager:30001/subject_categories',
        headers={'X-Subject-Token': "111111111"},
        json=SUBJECT_CATEGORIES
    )
    m.register_uri(
        'POST', 'http://manager:30001/subject_categories',
        headers={'X-Subject-Token': "111111111"},
        json=POST_SUBJECT_CATEGORIES
    )
