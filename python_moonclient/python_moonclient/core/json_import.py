import logging
import requests
import copy
from python_moonclient.core import config

LOGGER = logging.getLogger("moonclient.core.import_json")

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


def import_json(file_name):
    files = {'file': open(file_name, 'rb')}
    req = requests.post(URL.format("/import"), files=files)
    result = req.json()
    if isinstance(result, dict) and "message" in result:
        req.reason = result["message"]
    req.raise_for_status()
    return result
