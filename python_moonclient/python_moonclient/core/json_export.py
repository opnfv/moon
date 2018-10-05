import logging
import copy
import requests
from python_moonclient.core import config

LOGGER = logging.getLogger("moonclient.core.export_json")

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


def export_to_json():
    req = requests.get(URL.format("/export"))
    req.raise_for_status()
    result = req.json()
    return result
