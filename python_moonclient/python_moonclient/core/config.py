import base64
import json
import requests


def get_configuration(consul_host, consul_port, key):
    url = "http://{}:{}/v1/kv/{}".format(consul_host, consul_port, key)
    req = requests.get(url)
    if req.status_code != 200:
        raise Exception("Exception when retrieving configuration from Consul: {} {}".format(
            req.status_code, req.text
        ))
    data = req.json()
    if len(data) == 1:
        data = data[0]
        return {data["Key"]: json.loads(base64.b64decode(data["Value"]).decode("utf-8"))}
    else:
        return [
            {item["Key"]: json.loads(base64.b64decode(item["Value"]).decode("utf-8"))}
            for item in data
        ]


def get_config_data(consul_host, consul_port):
    conf_data = dict()
    conf_data['manager_host'] = get_configuration(
        consul_host, consul_port,
        'components/manager')['components/manager']['external']['hostname']
    conf_data['manager_port'] = get_configuration(
        consul_host, consul_port,
        'components/manager')['components/manager']['external']['port']
    try:
        requests.get("http://{}:{}/".format(
                conf_data['manager_host'],
                conf_data['manager_port']
            ),
            timeout=2)
    except requests.exceptions.ConnectionError:
        conf_data['manager_host'] = get_configuration(consul_host, consul_port,
                                                      'components/manager')[
            'components/manager']['hostname']
        conf_data['manager_port'] = get_configuration(consul_host, consul_port,
                                                      'components/manager')[
            'components/manager']['port']

    conf_data['keystone_host'] = get_configuration(
        consul_host, consul_port,
        'openstack/keystone')['openstack/keystone']['external']['url']
    try:
        requests.get(conf_data['keystone_host'], timeout=2)
    except requests.exceptions.ConnectionError:
        conf_data['keystone_host'] = get_configuration(
            consul_host, consul_port,
            'openstack/keystone')['openstack/keystone']['url']

    conf_data['keystone_user'] = get_configuration(consul_host, consul_port,
                                                   'openstack/keystone')['openstack/keystone']['user']
    conf_data['keystone_password'] = get_configuration(consul_host, consul_port,
                                                       'openstack/keystone')['openstack/keystone']['password']
    conf_data['keystone_project'] = get_configuration(consul_host, consul_port,
                                                      'openstack/keystone')['openstack/keystone']['project']
    return conf_data
