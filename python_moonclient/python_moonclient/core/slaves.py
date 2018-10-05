import logging
import requests
from python_moonclient.core import config
from python_moonclient.core.check_tools import *

LOGGER = logging.getLogger("moonclient.core.slaves")

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
    req.raise_for_status()
    result = req.json()
    check_slaves_in_result(result)
    return result


def set_slave(name):
    slaves = get_slaves().get("slaves", [])
    check_name_in_slaves(name, slaves)
    req = requests.patch(URL.format("/slaves/{}".format(name)),
                         headers=HEADERS,
                         json={
                             "op": "replace",
                             "variable": "configured",
                             "value": True
                         })
    req.raise_for_status()
    result = req.json()
    check_slaves_in_result(result)
    return get_slaves()


def delete_slave(name):
    slaves = get_slaves().get("slaves", [])
    check_name_in_slaves(name, slaves)
    req = requests.patch(URL.format("/slaves/{}".format(name)),
                         headers=HEADERS,
                         json={
                             "op": "replace",
                             "variable": "configured",
                             "value": False
                         })
    req.raise_for_status()
    result = req.json()
    check_slaves_in_result(result)
    return get_slaves()
