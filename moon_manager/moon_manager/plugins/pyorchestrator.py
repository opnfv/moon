# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
PyOrchestrator plugin
"""
import logging
import os
import time
import subprocess  # nosec
from uuid import uuid4
import requests
import yaml
from moon_manager.orchestration_driver import SlaveDriver
from moon_manager.orchestration_driver import PipelineDriver
from moon_manager import db_driver
from moon_manager.api.configuration import get_configuration
from moon_utilities.auth_functions import get_api_key_for_user, xor_decode
from moon_utilities import exceptions
from datetime import datetime

LOGGER = logging.getLogger("moon.manager.orchestrator.driver.pyorchestrator")

PLUGIN_TYPE = "orchestration"
WRAPPERS = {}
PORTS = []


def init():
    """
    Initialize the plugin by initializing wrappers
    :return: nothing
    """

    slaves = db_driver.SlaveManager.get_slaves(moon_user_id="admin")
    # TODO: check if server with UUID is not already up and running
    for _slave in slaves:
        LOGGER.info("testing PDP {}".format(_slave))
        if _slave not in WRAPPERS:
            start_new_server(_slave, slaves[_slave])


def create_gunicorn_config(host, port, uuid):
    """
    Create a Gunicorn config file in a temporary directory
    :return: filename
    """
    config_dir = get_configuration("orchestration").get("config_dir", "/tmp")  # nosec
    # (/tmp is a fallback solution)
    filename = os.path.join(config_dir, "gunicorn_{}.cfg".format(uuid))
    file_descriptor = open(filename, "w")
    file_descriptor.write("""bind = "{host}:{port}"
workers = {workers}
moon = "{moon_filename}"
    """.format(
        host=host,
        port=port,
        workers=1,
        moon_filename=os.path.join(config_dir, "moon_{}.yaml".format(uuid)),
    ))
    file_descriptor.close()
    return filename


def create_moon_config(uuid, data):
    """
    Create a Gunicorn config file in a temporary directory
    :return: filename
    """
    _log_config = get_configuration("logging")
    config_dir = get_configuration("orchestration").get("config_dir", "/tmp")  # nosec
    # (/tmp is a fallback solution)
    _log_config["handlers"]["file"]["filename"] = os.path.join(config_dir,
                                                               "moon_{}.log".format(uuid))
    __manager_url = get_configuration("management")["url"]
    api_token = get_api_key_for_user(get_configuration("management")["user"])
    filename = os.path.join(config_dir, "moon_{}.yaml".format(uuid))
    pwd_file = os.path.join(get_configuration("orchestration")["config_dir"],
                            "db_{}.json".format(uuid))
    config_dict = {
        "type": "wrapper",
        "uuid": str(uuid),
        "management": {
            "url": __manager_url,
            "user": get_configuration("management")["user"],
            "password": get_configuration("management")["password"],
            "token_file": pwd_file
        },
        "incremental_updates": False,
        "api_token": api_token,
        "data": "",
        "logging": _log_config,
        "orchestration": {
            "driver": "moon_engine.plugins.pyorchestrator",
            "connection": "local",
            "port": "20000...20100",
            "config_dir": config_dir
        },
        "authorization": {"driver": "moon_engine.plugins.authz"},
        "plugins": {"directory": get_configuration("plugins")["directory"]},
        "debug": get_configuration(key='debug', default=False),
        "grant_if_unknown_project": data.get("grant_if_unknown_project")
    }
    LOGGER.info("Writing config file to {}".format(filename))
    yaml.dump(config_dict, open(filename, "w"), default_flow_style=False)
    return filename


def kill_server(uuid):
    """
    Kill the server given its UUID
    :param uuid: UUID of the server
    :return: nothing
    """
    if uuid in WRAPPERS:
        LOGGER.info("Killing server {} after {} of uptime".format(
            uuid, str(datetime.now() - datetime.fromtimestamp(WRAPPERS[uuid]["starttime"]))
        ))
        with open(WRAPPERS[uuid]["process"], 'r') as pid_file:
            try:
                pid = int(pid_file.read())
            except ValueError:
                LOGGER.error("The pid found in {} is not valid".format(WRAPPERS[uuid]["process"]))
                return

        os.kill(pid, 15)
        del_server_port(WRAPPERS[uuid]["port"])
        WRAPPERS.pop(uuid)
    else:
        LOGGER.warning("Cannot find UUID {} in wrappers or interfaces".format(uuid))


def get_ports_range():
    """
    Get the range inside we can create new server
    :return: (port_min, port_max)
    """
    ports_range = get_configuration("orchestration")["port"]
    return int(ports_range.split(".")[0]), int(ports_range.split(".")[-1])


def get_next_port(server_host="127.0.0.1"):
    """
    Check the next free TCP port for this host
    :param server_host: the server host
    :return: a TCP port (int)
    """
    port_min, port_max = get_ports_range()
    _port = port_min
    _ports = []
    for _wrapper in WRAPPERS:
        _ports.append(WRAPPERS[_wrapper]["port"])
    _ports.sort()
    if not _ports:
        _port = port_min
    elif _ports[-1] + 1 > port_max:
        raise Exception(
            "Cannot add a new slave because "
            "the port range is bounded to {}".format(port_max))
    while True:
        if _port in _ports:
            _port += 1
            continue
        try:
            requests.get("http://{}:{}/status".format(server_host, _port), timeout=1)
        except requests.exceptions.ConnectionError:
            break
        if _port > port_max:
            raise Exception(
                "Cannot add a new slave because "
                "the port range is bounded to {}".format(port_max))
        _port += 1
    return _port


def add_server_port(port):
    """
    Append the server port in cache
    :param port: TCP port
    :return: None
    """
    PORTS.append(port)


def del_server_port(port):
    """
    Delete the server port in cache
    :param port: TCP port
    :return: None
    """
    try:
        PORTS.remove(port)
    except ValueError:
        LOGGER.warning("port {} is not in the known port".format(port))


def get_server_url(uuid=None):
    """
    Retrieve the server URL for this Slave ID
    If no server can be found, return None
    :param uuid: slave ID
    :return: a URL or None
    """
    if not uuid:
        return
    url = ""
    try:
        if uuid in WRAPPERS:
            url = "http://{}:{}".format(WRAPPERS[uuid]["server_ip"],
                                        WRAPPERS[uuid]["port"])
        LOGGER.debug(f"url in get_server_url '{url}'")
        if url:
            response = requests.get(url + "/status")
            if response.status_code == 200:
                return url
    except TimeoutError as _exception:
        LOGGER.warning("A timeout occurred when connecting to {}".format(url))
    # if port has not be found in local data, try to get information from remote servers
    port_min, port_max = get_ports_range()
    # FIXME: all servers may be not on localhost
    host = "127.0.0.1"
    LOGGER.debug(f"Go search through slaves")
    for _port in range(port_min, port_max):
        try:
            req = requests.get("http://{}:{}/status".format(host, _port), timeout=1)
            data = req.json()
            if "status" in data and data["status"]["uuid"] == uuid:
                return "http://{}:{}".format(host, _port)
        except Exception as _exception:
            LOGGER.warning("Error getting information from {}:{} ({})".format(host, _port, str(_exception)))
            return


def start_new_server(uuid, data):
    """Start a new server in a new process

    :param uuid: UUID of the server
    :param data: data of the server
    :return: nothing
    """
    _url = get_server_url(uuid)
    config_dir = get_configuration("orchestration").get("config_dir", "/tmp")  # nosec
    # (/tmp is a fallback solution)
    config_filename = os.path.join(config_dir, "moon_{}.yaml".format(uuid))
    # FIXME: maybe the server is not on the 127.0.0.1
    server_ip = "127.0.0.1"
    LOGGER.info("Starting server {} {}".format(_url, uuid))
    # debug = get_configuration("debug", False)
    if _url:
        _port = int(_url.split(":")[-1])
        add_server_port(_port)
        WRAPPERS[uuid] = {
            "starttime": data["extra"].get("starttime"),
            "port": _port,
            "server_ip": server_ip,
            "name": data.get("name"),
            "status": "up",
            "process": data.get("process"),
            "api_key": data.get("api_key"),
            "log": data.get("log")
        }
    else:
        _port = get_next_port()
        pid_file = os.path.join(config_dir, uuid + ".pid")
        # NOTE: we have actually no solution to get the actual IP address
        # so we need to put 0.0.0.0 in the host address
        gunicorn_config = create_gunicorn_config(host="0.0.0.0",  # nosec
                                                 port=_port,
                                                 uuid=uuid)
        create_moon_config(uuid=uuid, data=data)
        _command = ["gunicorn", "moon_engine.server:__hug_wsgi__", "--threads", "10",
                    "--log-level", "debug", "--log-file", gunicorn_config.replace("cfg", "log"),
                    "-p", pid_file, "-c", gunicorn_config]
        LOGGER.info("command: {}".format(" ".join(_command)))
        WRAPPERS[uuid] = {
            "starttime": time.time(),
            "port": _port,
            "server_ip": server_ip,
            "name": data.get("name"),
            "status": "down",
            "process": pid_file,
        }
        subprocess.Popen(_command, stdout=subprocess.PIPE, close_fds=True)  # nosec
        # Note: wait the process creation
        time.sleep(1)
        config = yaml.safe_load(open(config_filename))
        log_file = config["logging"]["handlers"]["file"]["filename"]
        WRAPPERS[uuid]["log"] = log_file
        for cpt in range(10):
            try:
                f_sock = open(log_file)
            except FileNotFoundError:
                time.sleep(1)
            else:
                break
        else:
            LOGGER.error("Cannot find log file ({})".format(log_file))
            return
        p_sock = 0
        LOGGER.info("Process running")
        WRAPPERS[uuid]["status"] = "up"
        while True:
            f_sock.seek(p_sock)
            latest_data = f_sock.read()
            p_sock = f_sock.tell()
            if latest_data and "APIKEY" in latest_data:
                _index_start = latest_data.index("APIKEY=") + len("APIKEY=")
                _index_stop = latest_data.index("\n", _index_start)
                key = latest_data[_index_start:_index_stop].strip()
                api_key = get_api_key_for_user("admin")
                try:
                    engine_api_key = xor_decode(key, api_key)
                    LOGGER.info(f"key={key}")
                    LOGGER.info(f"engine_api_key={engine_api_key}")
                except exceptions.DecryptError:
                    engine_api_key = False
                WRAPPERS[uuid]["api_key"] = engine_api_key
                break
            time.sleep(1)


class SlaveConnector(SlaveDriver):
    """
    Connector to Slave API
    """

    def __init__(self, driver_name, engine_name):
        self.driver_name = driver_name
        self.engine_name = engine_name

    def update_slave(self, slave_id, value):
        LOGGER.info("Updating the slave {} with {}".format(slave_id, value))
        slave_url = WRAPPERS[slave_id]['server_ip']
        slave_port = WRAPPERS[slave_id]['port']

        config_dir = get_configuration("orchestration").get("config_dir", "/tmp")  # nosec
        config_filename = os.path.join(config_dir, "moon_{}.yaml".format(slave_id))

        conf = yaml.safe_load(open(config_filename, 'r'))
        for key in value:
            if key in conf:
                conf[key] = value[key]

        os.remove(config_filename)
        yaml.dump(conf, open(config_filename, "w"), default_flow_style=False)

        req = requests.put("http://{}:{}/update".format(slave_url, slave_port),
                           headers={"x-api-key": WRAPPERS[slave_id]["api_key"]})
        return req

    def delete_slave(self, slave_id):
        LOGGER.info("Deleting slave {}".format(slave_id))
        kill_server(slave_id)

    def add_slave(self, slave_id=None, data=None):
        LOGGER.info("Adding slave {} {}".format(slave_id, data))
        if not slave_id:
            slave_id = uuid4().hex
        start_new_server(slave_id, data)
        return WRAPPERS[slave_id]

    def get_slaves(self, slave_id=None):
        LOGGER.info("Get slaves {}".format(WRAPPERS))
        results = {}
        for wrapper in WRAPPERS:
            results[wrapper] = {
                "starttime": WRAPPERS[wrapper]["starttime"],
                "port": WRAPPERS[wrapper]["port"],
                "server_ip": WRAPPERS[wrapper]["server_ip"],
                "name": WRAPPERS[wrapper]["name"],
                "status": "down",
                "log": WRAPPERS[wrapper]["log"]
            }
            try:
                req = requests.get("http://{}:{}/status".format(
                    WRAPPERS[wrapper]["server_ip"],
                    WRAPPERS[wrapper]["port"]
                ))
                if req.status_code == 200:
                    results[wrapper]["status"] = "up"
                else:
                    results[wrapper]["status"] = "down"
                LOGGER.info("get_slaves: {} {} {}".format(
                    slave_id, req.status_code, results[wrapper]["status"]))
            except TimeoutError:
                LOGGER.warning("Timeout connecting {} on port {}".format(
                    WRAPPERS[wrapper]["server_ip"],
                    WRAPPERS[wrapper]["port"]
                ))
            except requests.exceptions.ConnectionError:
                results[wrapper]["status"] = "down"
        return results


class PipelineConnector(PipelineDriver):
    """
    Connector to Pipeline API
    """

    def __init__(self, driver_name, engine_name):
        self.driver_name = driver_name
        self.engine_name = engine_name

    def update_pipeline(self, pipeline_id, data):
        for _wrapper in WRAPPERS:
            _url = get_server_url(_wrapper)
            req = requests.put("{}/update/pdp/{}".format(_url, pipeline_id),
                               headers={"x-api-key": WRAPPERS[_wrapper]["api_key"]},
                               json=data)
            if req.status_code == 206:
                LOGGER.warning("No pipeline available...")
            elif req.status_code != 202:
                LOGGER.warning("Error sending upgrade command to pipeline ({})".format(req.text))

    def delete_pipeline(self, pipeline_id):
        LOGGER.info("Deleting pipeline {}".format(pipeline_id))
        for _wrapper in WRAPPERS:
            if WRAPPERS[_wrapper]['status'] == "down":
                continue
            # FIXME: we should manage https here
            _url = "http://{}:{}".format(WRAPPERS[_wrapper]['server_ip'],
                                         WRAPPERS[_wrapper]['port'])
            req = requests.delete("{}/pipeline/{}".format(_url, pipeline_id),
                                  headers={"x-api-key": WRAPPERS[_wrapper]["api_key"]})
            LOGGER.info("{}/pipeline/{}".format(_url, pipeline_id))
            if req.status_code != 200:
                LOGGER.error("Cannot delete the pipeline in slave {} ({}, {})".format(
                    _wrapper, req.status_code, req.content))
        # FIXME: make a request to the correct wrapper

    def add_pipeline(self, pipeline_id=None, data=None):
        LOGGER.info("Adding POD in manager {} {}".format(pipeline_id, data))
        if not pipeline_id:
            pipeline_id = uuid4().hex
        slaves = data.get("slaves", [])
        pipelines = []
        for _wrapper in WRAPPERS:
            if slaves and (WRAPPERS[_wrapper]['name'] not in slaves):
                continue
            # FIXME: we should manage https here
            _url = "http://{}:{}".format(WRAPPERS[_wrapper]['server_ip'],
                                         WRAPPERS[_wrapper]['port'])
            req = requests.put("{}/pipeline/{}".format(_url, pipeline_id), json=data,
                               headers={"x-api-key": WRAPPERS[_wrapper]['api_key']})
            if req.status_code != 200:
                LOGGER.error("Cannot create a new pipeline ({}, {})".format(req.status_code,
                                                                            req.content))
            elif "pipelines" not in req.json():
                LOGGER.error("Cannot create a new pipeline ({}, {})".format(req.status_code,
                                                                            req.content))
            else:
                pipelines.append(req.json())
        LOGGER.info("Pipeline created {}".format(pipelines))
        return pipelines
        # FIXME: make a request to the correct wrapper

    def get_pipelines(self, slave_id=None, pipeline_id=None):
        results = {}
        for _wrapper in WRAPPERS:
            if slave_id and _wrapper != slave_id:
                continue
            if WRAPPERS[_wrapper]['status'] == "down":
                continue
            results[_wrapper] = {}
            # FIXME: we should manage https here
            _url = "http://{}:{}".format(WRAPPERS[_wrapper]['server_ip'],
                                         WRAPPERS[_wrapper]['port'])
            req = requests.get("{}/pipelines".format(_url),
                               headers={"x-api-key": WRAPPERS[_wrapper]['api_key']})
            if req.status_code != 200:
                LOGGER.error("Cannot get information for slave {} ({}, {})".format(
                    _wrapper, req.status_code, req.content))
            else:
                # FIXME: filter on pipeline_id
                results[_wrapper] = req.json()
        return results


class Connector(SlaveConnector, PipelineConnector):
    """
    General connector to get all APIs in one endpoint
    """

    def __init__(self, *args, **kwargs):
        init()
