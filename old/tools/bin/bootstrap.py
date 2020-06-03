import os
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

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("moon.bootstrap")
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


def start_consul(data_config):
    cmd = ["docker", "run", "-d", "--net=moon", "--name=consul", "--hostname=consul", "-p", "8500:8500", "consul"]
    output = subprocess.run(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if output.returncode != 0:
        log.info(" ".join(cmd))
        log.info(output.returncode)
        log.error(output.stderr)
        log.error(output.stdout)
        raise Exception("Error starting Consul container!")
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


def start_database():
    cmd = ["docker", "run", "-dti", "--net=moon", "--hostname=db", "--name=db",
           "-e", "MYSQL_ROOT_PASSWORD=p4sswOrd1", "-e", "MYSQL_DATABASE=moon", "-e", "MYSQL_USER=moon",
           "-e", "MYSQL_PASSWORD=p4sswOrd1", "-p", "3306:3306", "mysql:latest"]
    output = subprocess.run(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if output.returncode != 0:
        log.info(cmd)
        log.error(output.stderr)
        log.error(output.stdout)
        raise Exception("Error starting DB container!")
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
                log.info("Database is up, populating it...")
                output = subprocess.run(["moon_db_manager", "upgrade"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                if output.returncode != 0:
                    raise Exception("Error populating the database!")
                break


def start_keystone():
    output = subprocess.run(["docker", "run", "-dti", "--net=moon", "--hostname=keystone", "--name=keystone",
                             "-e", "DB_HOST=db", "-e", "DB_PASSWORD_ROOT=p4sswOrd1", "-p", "35357:35357",
                             "-p", "5000:5000", "keystone:mitaka"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if output.returncode != 0:
        raise Exception("Error starting Keystone container!")
    # TODO: Keystone answers request too quickly
    #       even if it is not fully loaded
    #       we must test if a token retrieval is possible or not
    #       to see if Keystone is truly up and running
    for config in get("openstack/keystone"):
        while True:
            try:
                time.sleep(1)
                req = requests.get(config["url"])
            except requests.exceptions.ConnectionError:
                log.info("Waiting for Keystone ({})".format(config["url"]))
                time.sleep(1)
                continue
            else:
                log.info("Keystone is up")
                break


def start_moon(data_config):
    cmds = [
        # ["docker", "run", "-dti", "--net=moon", "--name=wrapper", "--hostname=wrapper", "-p",
        #  "{0}:{0}".format(data_config['components']['wrapper']['port']),
        #  data_config['components']['wrapper']['container']],
        ["docker", "run", "-dti", "--net=moon", "--name=manager",
         "--hostname=manager", "-p",
         "{0}:{0}".format(data_config['components']['manager']['port']),
         data_config['components']['manager']['container']],
        ["docker", "run", "-dti", "--net=moon", "--name=interface",
         "--hostname=interface", "-p",
         "{0}:{0}".format(data_config['components']['interface']['port']),
         data_config['components']['interface']['container']],
    ]
    for cmd in cmds:
        log.warning("Start {}".format(cmd[-1]))
        # answer = input()
        # if answer.lower() in ("y", "yes", "o", "oui"):
        output = subprocess.run(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        time.sleep(3)
        if output.returncode != 0:
            log.info(" ".join(cmd))
            log.info(output.returncode)
            log.error(output.stderr)
            log.error(output.stdout)
            raise Exception("Error starting {} container!".format(cmd[-1]))
    subprocess.run(["docker", "ps"])


def main():
    data_config = search_config_file()
    subprocess.run(["docker", "rm", "-f", "consul", "db", "manager", "wrapper", "interface", "authz*", "keystone"])
    start_consul(data_config)
    start_database()
    start_keystone()
    start_moon(data_config)

main()

