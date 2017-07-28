import sys
import time
import requests
import yaml
import logging
import json
import base64
import mysql.connector
import re
import subprocess
import pika
import pika.credentials
import pika.exceptions

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("moon.bootstrap")
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARNING)
requests_log.propagate = True
pika_log = logging.getLogger("pika")
pika_log.setLevel(logging.ERROR)
pika_log.propagate = True

CONSUL_HOST = sys.argv[1] if len(sys.argv) > 1 else "consul"
CONSUL_PORT = sys.argv[2] if len(sys.argv) > 2 else 8500
HEADERS = {"content-type": "application/json"}


def search_config_file():
    data_config = None
    for _file in (
            "moon.conf",
            "conf/moon.conf",
            "../moon.conf",
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


def populate_consul(data_config):
    while True:
        try:
            req = requests.get("http://{}:{}/ui".format(CONSUL_HOST, CONSUL_PORT))
        except requests.exceptions.ConnectionError:
            log.info("Waiting for Consul ({}:{})".format(CONSUL_HOST, CONSUL_PORT))
            time.sleep(1)
            continue
        else:
            break
        # if req.status_code in (302, 200):
        #     break
        # log.info("Waiting for Consul ({}:{})".format(CONSUL_HOST, CONSUL_PORT))
        # time.sleep(1)
    log.info("Consul is up")

    req = requests.get("http://{}:{}/v1/kv/database".format(CONSUL_HOST, CONSUL_PORT))
    if req.status_code == 200:
        log.info("Consul is already populated")
        return

    put("database", data_config["database"])
    put("messenger", data_config["messenger"])
    put("slave", data_config["slave"])
    put("docker", data_config["docker"])
    put("logging", data_config["logging"])
    put("components_port_start", data_config["components"]["port_start"])

    for _key, _value in data_config["components"].items():
        if type(_value) is dict:
            put("components/{}".format(_key), data_config["components"][_key])

    for _key, _value in data_config["plugins"].items():
        put("plugins/{}".format(_key), data_config["plugins"][_key])

    for _key, _value in data_config["openstack"].items():
        put("openstack/{}".format(_key), data_config["openstack"][_key])


def wait_for_database():
    log.info(get("database"))
    for database in get("database"):
        database_url = database['url']
        match = re.search("(?P<proto>^[\\w+]+):\/\/(?P<user>\\w+):(?P<password>.+)@(?P<host>\\w+):*(?P<port>\\d*)",
                          database_url)
        config = match.groupdict()
        while True:
            try:
                conn = mysql.connector.connect(
                    host=config["host"],
                    user=config["user"],
                    password=config["password"],
                    database="moon"
                )
                conn.close()
            except mysql.connector.errors.InterfaceError:
                log.info("Waiting for Database ({})".format(config["host"]))
                time.sleep(1)
                continue
            else:
                log.info("Database i up, populating it...")
                output = subprocess.run(["moon_db_manager", "upgrade"])
                if output.returncode != 0:
                    raise Exception("Error populating the database!")
                break


def wait_for_message_queue():
    for messenger in get("messenger"):
        url = messenger['url']
        match = re.search("(?P<proto>^[\\w+]+):\/\/(?P<user>\\w+):(?P<password>.+)@(?P<host>\\w+):?(?P<port>\\d*)/?(?P<virtual_host>\\w+)",
                          url)
        config = match.groupdict()
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=config['host'],
                        port=int(config['port']),
                        virtual_host=config['virtual_host'],
                        credentials=pika.credentials.PlainCredentials(
                            config['user'],
                            config['password']
                        )
                    )
                )
                connection.close()
            except (
                pika.exceptions.ProbableAuthenticationError,
                pika.exceptions.ConnectionClosed,
                ConnectionResetError,
                pika.exceptions.IncompatibleProtocolError
            ):
                log.info("Waiting for MessageQueue ({})".format(config["host"]))
                time.sleep(1)
                continue
            else:
                log.info("MessageQueue is up")
                break


def wait_for_keystone():
    # TODO: Keystone answers request too quickly
    #       even if it is not fully loaded
    #       we must test if a token retrieval is possible or not
    #       to see if Keystone is truly up and running
    for config in get("openstack/keystone"):
        while True:
            try:
                req = requests.get(config["url"])
            except requests.exceptions.ConnectionError:
                log.info("Waiting for Keystone ({})".format(config["url"]))
                time.sleep(1)
                continue
            else:
                log.info("Keystone is up")
                break


def main():
    data_config = search_config_file()
    populate_consul(data_config)
    wait_for_database()
    wait_for_message_queue()
    wait_for_keystone()
    import moon_orchestrator.server
    moon_orchestrator.server.main()

main()

