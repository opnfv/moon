# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import base64
import json
import python_moonutilities.request_wrapper as requests
import logging.config
from python_moonutilities import exceptions

logger = logging.getLogger("moon.utilities.configuration")

CONSUL_HOST = "consul"
CONSUL_PORT = "8500"

DATABASE = "database"
KEYSTONE = "keystone"
DOCKER = "docker"
COMPONENTS = "components"


def init_logging():
    config = get_configuration("logging")
    logging.config.dictConfig(config['logging'])


def increment_port():
    components_object = get_configuration("components/port_start")
    if 'components/port_start' in components_object:
        components_port_start = int(components_object['components/port_start'])
        components_port_start += 1
    else:
        raise exceptions.ConsulComponentContentError("error={}".format(components_object))
    url = "http://{}:{}/v1/kv/components/port_start".format(CONSUL_HOST, CONSUL_PORT)
    req = requests.put(url, json=str(components_port_start))
    if req.status_code != 200:
        logger.info("url={}".format(url))
        raise exceptions.ConsulError
    return components_port_start


def get_configuration(key):
    url = "http://{}:{}/v1/kv/{}".format(CONSUL_HOST, CONSUL_PORT, key)
    req = requests.get(url)
    if req.status_code != 200:
        logger.error("url={}".format(url))
        raise exceptions.ConsulComponentNotFound("error={}: {}".format(req.status_code, req.text))
    data = req.json()
    if len(data) == 1:
        data = data[0]
        if all( k in data for k in ("Key", "Value")) :
            return {data["Key"]: json.loads(base64.b64decode(data["Value"]).decode("utf-8"))}
        raise exceptions.ConsulComponentContentError("error={}".format(data))
    else:
        for item in data:
            if not all(k in item for k in ("Key", "Value")):
                logger.warning("invalidate content {}".format(item))
                raise exceptions.ConsulComponentContentError("error={}".format(data))
        return [
            {
                item["Key"]: json.loads(base64.b64decode(item["Value"]).decode("utf-8"))
            } for item in data
        ]


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
        logger.debug("url={}".format("http://{}:{}/v1/kv/components/{}".format(CONSUL_HOST, CONSUL_PORT, uuid)))
        logger.debug("data={}".format(data))
        raise exceptions.ConsulError
    logger.info("Add component {}".format(req.text))
    return get_configuration("components/"+uuid)


def get_plugins():
    pipeline = get_configuration("components/pipeline")
    logger.debug("pipeline={}".format(pipeline))
    components = pipeline.get("components/pipeline")
    if 'interface' in components:
        components.pop('interface')
    else:
        raise exceptions.ConsulComponentContentError("error= Components pipeline has no interface")
    return components


def get_components():
    url = "http://{}:{}/v1/kv/components?recurse=true".format(CONSUL_HOST, CONSUL_PORT)
    req = requests.get(url)
    if req.status_code != 200:
        logger.info("url={}".format(url))
        raise exceptions.ConsulError
    data = req.json()
    if len(data) == 1:
        data = data[0]
        if all(k in data for k in ("Key", "Value")):
            return {data["Key"].replace("components/", ""): json.loads(base64.b64decode(data["Value"]).decode("utf-8"))}
        raise exceptions.ConsulComponentContentError("error={}".format(data))
    else:
        for item in data:
            if not all(k in item for k in ("Key", "Value")):
                logger.warning("invalidate content {}".format(item))
                raise exceptions.ConsulComponentContentError("error={}".format(data))
        return {
            item["Key"].replace("components/", ""): json.loads(base64.b64decode(item["Value"]).decode("utf-8"))
            for item in data
        }


init_logging()
