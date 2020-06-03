

PROJECTS = {
    "projects": [
        {
            "is_domain": False,
            "description": None,
            "domain_id": "admin",
            "enabled": True,
            "id": "0c4e939acacf4376bdcd1129f1a054ad",
            "links": {
                "self": "http://example.com/identity/v3/projects/0c4e939acacf4376bdcd1129f1a054ad"
            },
            "name": "admin",
            "parent_id": None,
            "tags": []
        },
        {
            "is_domain": False,
            "description": None,
            "domain_id": "default",
            "enabled": True,
            "id": "0cbd49cbf76d405d9c86562e1d579bd3",
            "links": {
                "self": "http://example.com/identity/v3/projects/0cbd49cbf76d405d9c86562e1d579bd3"
            },
            "name": "demo",
            "parent_id": None,
            "tags": []
        }
    ]
}


def conf_projects(m):
    m.register_uri(
        'GET', 'http://keystone:5000/v3/projects',
        headers={'X-Subject-Token': "111111111"},
        json=PROJECTS
    )
    m.register_uri(
        'POST', 'http://keystone:5000/v3/auth/tokens',
        headers={'X-Subject-Token': "111111111"}
    )
