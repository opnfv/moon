import utilities


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
    m.register_uri(
        'GET', 'http://{}:{}/v1/kv/components/manager'.format(utilities.CONSUL_HOST, utilities.CONSUL_PORT),
        json=[{'Key': 'components/manager', 'Value': utilities.get_b64_conf(components_manager_mock)}]
    )

    m.register_uri(
        'GET', 'http://{}:{}/v1/kv/openstack/keystone'.format(utilities.CONSUL_HOST, utilities.CONSUL_PORT),
        json=[{'Key': 'openstack/keystone', 'Value': utilities.get_b64_conf(openstack_keystone_mock)}]
    )
