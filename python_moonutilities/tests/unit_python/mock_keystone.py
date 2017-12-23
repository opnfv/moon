def register_keystone(m):
    m.register_uri(
        'POST', 'http://keystone:5000/v3/auth/tokens',
        headers={'X-Subject-Token': "111111111"}
    )
    m.register_uri(
        'DELETE', 'http://keystone:5000/v3/auth/tokens',
        headers={'X-Subject-Token': "111111111"}
    )
    m.register_uri(
        'POST', 'http://keystone:5000/v3/users?name=testuser&domain_id=default',
        json={"users": {}}
    )
    m.register_uri(
        'GET', 'http://keystone:5000/v3/users?name=testuser&domain_id=default',
        json={"users": {}}
    )
    m.register_uri(
        'POST', 'http://keystone:5000/v3/users/',
        json={"users": [{
            "id": "1111111111111"
        }]}
    )