# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import base64
import json
import requests
import logging
import logging.config
from python_moonutilities import exceptions

LOG = logging.getLogger("moon.utilities")

CONSUL_HOST = "consul"
CONSUL_PORT = "8500"

DATABASE = "database"
KEYSTONE = "keystone"
DOCKER = "docker"
COMPONENTS = "components"


def init_logging():
    config = get_configuration("logging")
    logging.config.dictConfig(config['logging'])

'''
    [Note 1] components_port_start as a key not following the same url pattern, 
    i suggest it should be components/port_start, also according to the mock data that 
    you build for mock component [components_utilities.py] will work with that pattern [components/port_start]
    
    [General Note]
    i think any request calling should be between try and catch in order to avoid any failure cause system to behave 
    in unexpected way 
'''
def increment_port():
    components_port_start = int(get_configuration("components_port_start")['components_port_start'])
    components_port_start += 1
    url = "http://{}:{}/v1/kv/components_port_start".format(CONSUL_HOST, CONSUL_PORT)
    req = requests.put(url, json=str(components_port_start))
    if req.status_code != 200:
        LOG.info("url={}".format(url))
        raise exceptions.ConsulError
    return components_port_start

'''
    [Note] Access data/item object with "Key" and "Value" keys without validating if there are already exist or not 
'''
def get_configuration(key):
    url = "http://{}:{}/v1/kv/{}".format(CONSUL_HOST, CONSUL_PORT, key)
    req = requests.get(url)
    if req.status_code != 200:
        LOG.error("url={}".format(url))
        raise exceptions.ConsulComponentNotFound("error={}: {}".format(req.status_code, req.text))
    data = req.json()
    if len(data) == 1:
        data = data[0]
        return {data["Key"]: json.loads(base64.b64decode(data["Value"]).decode("utf-8"))}
    else:
        return [
            {item["Key"]: json.loads(base64.b64decode(item["Value"]).decode("utf-8"))}
            for item in data
        ]

'''
    [Note] add_component function return get_configuration
    and get_configuration funcation may raise exception , so add component may throw an exception 
'''
def add_component(name, uuid, port=None, bind="127.0.0.1", keystone_id="", extra=None, container=None):
    data = {
        "hostname": name,
        "keystone_id": keystone_id,
        "bind": bind,
        "port": port,
        "extra": extra,
        "container": container
    }
    req = requests.put(
        "http://{}:{}/v1/kv/components/{}".format(CONSUL_HOST, CONSUL_PORT, uuid),
        headers={"content-type": "application/json"},
        json=data
    )
    if req.status_code != 200:
        LOG.debug("url={}".format("http://{}:{}/v1/kv/components/{}".format(CONSUL_HOST, CONSUL_PORT, uuid)))
        LOG.debug("data={}".format(data))
        raise exceptions.ConsulError
    LOG.info("Add component {}".format(req.text))
    return get_configuration("components/"+uuid)

'''
[Note] the same as increment_port comments
'''
def get_plugins():
    url = "http://{}:{}/v1/kv/plugins?recurse=true".format(CONSUL_HOST, CONSUL_PORT)
    req = requests.get(url)
    if req.status_code != 200:
        LOG.info("url={}".format(url))
        raise exceptions.ConsulError
    data = req.json()
    if len(data) == 1:
        data = data[0]
        return {data["Key"].replace("plugins/", ""): json.loads(base64.b64decode(data["Value"]).decode("utf-8"))}
    else:
        return {
            item["Key"].replace("plugins/", ""): json.loads(base64.b64decode(item["Value"]).decode("utf-8"))
            for item in data
        }

'''
[Note] the same as increment_port comments
'''
def get_components():
    url = "http://{}:{}/v1/kv/components?recurse=true".format(CONSUL_HOST, CONSUL_PORT)
    req = requests.get(url)
    if req.status_code != 200:
        LOG.info("url={}".format(url))
        raise exceptions.ConsulError
    data = req.json()
    if len(data) == 1:
        data = data[0]
        return {data["Key"].replace("components/", ""): json.loads(base64.b64decode(data["Value"]).decode("utf-8"))}
    else:
        return {
            item["Key"].replace("components/", ""): json.loads(base64.b64decode(item["Value"]).decode("utf-8"))
            for item in data
        }


init_logging()
