from . import utilities


components_manager_mock = {
    "port": 8082,
    "bind": "0.0.0.0",
    "hostname": "manager",
    "container": "wukongsun/moon_manager:v4.3.1",
    "external": {
        "port": 30001,
        "hostname": "88.88.88.2"
    }
}


openstack_keystone_mock = {
    "url": "http://keystone:5000/v3",
    "user": "admin",
    "password": "p4ssw0rd",
    "domain": "default",
    "project": "admin",
    "check_token": False,
    "certificate": False,
    "external": {
        "url": "http://88.88.88.2:30006/v3"
    }
}


def register_consul(m):
    for component in utilities.COMPONENTS:
        m.register_uri(
            'GET', 'http://consul:8500/v1/kv/{}'.format(component),
            json=[{'Key': component, 'Value': utilities.get_b64_conf(component)}]
        )

    m.register_uri(
        'GET', 'http://manager:30001',
        json={}
    )
    m.register_uri(
        'GET', 'http://keystone:5000/v3',
        json={}
    )
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
        json={"users": [{"id": "1111111111111"}]}
    )
