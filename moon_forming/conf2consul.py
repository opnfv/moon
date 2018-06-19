import os
import sys
import requests
import yaml
import logging
import json
import base64

__version__ = "1.4.1"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("moon.conf2consul")
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARNING)
requests_log.propagate = True

if len(sys.argv) == 2:
    if os.path.isfile(sys.argv[1]):
        CONF_FILENAME = sys.argv[1]
        CONSUL_HOST = "consul"
    else:
        CONF_FILENAME = "moon.conf"
        CONSUL_HOST = sys.argv[1]
    CONSUL_PORT = 8500
else:
    CONSUL_HOST = sys.argv[1] if len(sys.argv) > 1 else "consul"
    CONSUL_PORT = sys.argv[2] if len(sys.argv) > 2 else 8500
    CONF_FILENAME = sys.argv[3] if len(sys.argv) > 3 else "moon.conf"
HEADERS = {"content-type": "application/json"}


def search_config_file():
    data_config = None
    for _file in (
            CONF_FILENAME,
            "conf/moon.conf",
            "../moon.conf",
            "../conf/moon.conf",
            "/etc/moon/moon.conf",
    ):
        try:
            data_config = yaml.safe_load(open(_file))
        except FileNotFoundError:
            data_config = None
            continue
        else:
            break
    if not data_config:
        raise Exception("Configuration file not found...")
    return data_config


def put(key, value):
    url = "http://{host}:{port}/v1/kv/{key}".format(host=CONSUL_HOST, port=CONSUL_PORT, key=key)
    log.info(url)
    req = requests.put(
        url,
        headers=HEADERS,
        json=value
    )
    if req.status_code != 200:
        raise Exception("Error connecting to Consul ({}, {})".format(req.status_code, req.text))


def get(key):
    url = "http://{host}:{port}/v1/kv/{key}".format(host=CONSUL_HOST, port=CONSUL_PORT, key=key)
    req = requests.get(url)
    data = req.json()
    for item in data:
        log.info("{} {} -> {}".format(
            req.status_code,
            item["Key"],
            json.loads(base64.b64decode(item["Value"]).decode("utf-8"))
        ))
        yield json.loads(base64.b64decode(item["Value"]).decode("utf-8"))


def main():
    data_config = search_config_file()
    req = requests.head("http://{}:{}/ui/".format(CONSUL_HOST, CONSUL_PORT))
    if req.status_code != 200:
        log.critical("Consul is down...")
        log.critical("request info: {}/{}".format(req, req.text))
        sys.exit(1)

    put("database", data_config["database"])
    # put("messenger", data_config["messenger"])
    # put("slave", data_config["slave"])
    # put("docker", data_config["docker"])
    put("logging", data_config["logging"])
    # put("components_port_start", data_config["components"]["port_start"])

    for _key, _value in data_config["components"].items():
        put("components/{}".format(_key), data_config["components"][_key])

    # for _key, _value in data_config["plugins"].items():
    #     put("plugins/{}".format(_key), data_config["plugins"][_key])

    for _key, _value in data_config["openstack"].items():
        put("openstack/{}".format(_key), data_config["openstack"][_key])


main()

