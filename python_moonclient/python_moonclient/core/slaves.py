import logging
import requests
import copy
from . import config

logger = logging.getLogger("moonclient.core.slaves")


URL = None
HEADERS = None


def init(consul_host, consul_port):
    conf_data = config.get_config_data(consul_host, consul_port)
    global URL, HEADERS
    URL = "http://{}:{}".format(
        conf_data['manager_host'],
        conf_data['manager_port'])
    URL = URL + "{}"
    HEADERS = {"content-type": "application/json"}


def get_slaves():
    req = requests.get(URL.format("/slaves"))
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "slaves" in result
    return result


def set_slave(name):
    slaves = get_slaves().get("slaves", [])
    names = map(lambda x: x['name'], slaves)
    assert name in names
    req = requests.patch(URL.format("/slaves/{}".format(name)),
                         headers=HEADERS,
                         json={
                            "op": "replace",
                            "variable": "configured",
                            "value": True
                        })
    assert req.status_code == 200
    result = req.json()
    assert type(result) is dict
    assert "slaves" in result
    return get_slaves()


def delete_slave(name):
    slaves = get_slaves().get("slaves", [])
    names = map(lambda x: x['name'], slaves)
    assert name in names
    req = requests.patch(URL.format("/slaves/{}".format(name)),
                         headers=HEADERS,
                         json={
                            "op": "replace",
                            "variable": "configured",
                            "value": False
                        })
    return get_slaves()
