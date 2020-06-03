# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
import os
import time
import requests
import subprocess  # nosec
from uuid import uuid4
import yaml
from moon_engine.orchestration_driver import PipelineDriver
from moon_engine.api import configuration
from moon_engine.api.configuration import get_configuration
from moon_engine import get_api_key
from moon_utilities.auth_functions import xor_decode
from moon_utilities import exceptions
from datetime import datetime

LOGGER = logging.getLogger("moon.engine.orchestrator.driver.pyorchestrator")

PLUGIN_TYPE = "orchestration"
pipelines = {}
ports = []


def init():
    """Initialize the plugin by initializing wrappers

    :return: nothing
    """

    # FIXME: get pipelines from Manager
    pass


def create_gunicorn_config(host, port, server_type, uuid):
    """Create a Gunicorn config file in a temporary directory

    :return: filename
    """
    config_dir = get_configuration("orchestration").get("config_dir", "/tmp")  # nosec
    # (/tmp is a fallback solution)
    _log_config = get_configuration("logging")
    _log_config["handlers"]["file"]["filename"] = os.path.join(config_dir,
                                                               "moon_{}.log".format(uuid))
    __manager_url = get_configuration("management")["url"]
    filename = os.path.join(config_dir, "gunicorn_{}.cfg".format(uuid4().hex))
    fd = open(filename, "w")
    fd.write("""bind = "{host}:{port}"
workers = {workers}
moon = "{moon_filename}"
    """.format(
        host=host,
        port=port,
        workers=1,
        moon_filename=os.path.join(config_dir, "moon_{}.yaml".format(uuid)),
    ))
    fd.close()
    return filename


def create_moon_config(uuid, manager_cnx=True, policy_file=None):
    """Create a Moon config file in a temporary directory

    :return: filename
    """
    LOGGER.info(f"create_moon_config({uuid})")
    config_dir = get_configuration("orchestration").get("config_dir", "/tmp")  # nosec
    _log_config = get_configuration("logging")
    _log_config["handlers"]["file"]["filename"] = os.path.join(config_dir,
                                                               "moon_{}.log".format(uuid))
    if manager_cnx:
        __manager_url = get_configuration("management")["url"]
        api_token = get_api_key(get_configuration("management")["url"],
                                get_configuration("management")["user"],
                                get_configuration("management")["password"])
    else:
        __manager_url = ""
        api_token = ""
    config_dir = get_configuration("orchestration").get("config_dir", "/tmp")  # nosec
    # (/tmp is a fallback solution)
    filename = os.path.join(config_dir, "moon_{}.yaml".format(uuid))
    config_dict = {
        "type": "pipeline",
        "uuid": uuid,
        "management": {
            "url": __manager_url,
            "token_file": os.path.join(config_dir, "db_{}.json".format(uuid))
        },
        "incremental_updates": True,
        "api_token": api_token,
        "data": "",
        "logging": _log_config,
        "authorization": get_configuration("authorization",
                                           {"driver": "moon_engine.plugins.authz"}),
        "plugins": get_configuration("plugins"),
        "debug": get_configuration(key='debug', default=False)
    }
    if policy_file:
        config_dict['data'] = policy_file
    if not manager_cnx:
        config_dict['uuid'] = ""
        config_dict['incremental_updates'] = False
    LOGGER.info("Writing config file to {}".format(filename))
    yaml.dump(config_dict, open(filename, "w"), default_flow_style=False)
    return filename


def kill_server(uuid):
    """Kill the server given its UUID

    :param uuid: UUID of the server
    :return: nothing
    """
    LOGGER.info("pipelines={}".format(pipelines))
    if uuid in pipelines:
        LOGGER.info("pipeline={}".format(pipelines[uuid]))
        # Fixme: if the server has been restarted, the process attribute is empty
        LOGGER.info("Killing server {} after {} of uptime".format(
            uuid,
            str(datetime.now() - datetime.fromtimestamp(pipelines[uuid]["starttime"]))
        ))
        with open(pipelines[uuid]["process"], 'r') as pid_file:
            try:
                pid = int(pid_file.read())
            except ValueError:
                LOGGER.error("The pid found in {} is not valid".format(pipelines[uuid]["process"]))
                return

        os.kill(pid, 15)
        del_server_port(pipelines[uuid]["port"])
        pipelines.pop(uuid)
    else:
        LOGGER.warning("Cannot find UUID {} in wrappers or interfaces".format(uuid))


def get_ports_range():
    ports_range = get_configuration("orchestration")["port"]
    return int(ports_range.split(".")[0]), int(ports_range.split(".")[-1])


def get_next_port(server_host="127.0.0.1"):
    port_min, port_max = get_ports_range()
    _port = port_min
    _ports = []
    for _pipeline in pipelines:
        _ports.append(pipelines[_pipeline]["port"])
    _ports.sort()
    if not _ports:
        _port = port_min
    elif _ports[-1]+1 > port_max:
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
                "Cannot add a new pipeline because "
                "the port range is bounded to {}".format(port_max))
        _port += 1
    return _port


def add_server_port(port):
    ports.append(port)


def del_server_port(port):
    try:
        ports.remove(port)
    except ValueError:
        LOGGER.warning("port {} is not in the known port".format(port))


def get_server_url(uuid=None):
    if not uuid:
        return
    url = ""
    try:
        if uuid in pipelines:
            url = "http://{}:{}".format(pipelines[uuid]["server_ip"],
                                        pipelines[uuid]["port"])
        if url:
            response = requests.get(url + "/status")
            if response.status_code == 200:
                return url
    except TimeoutError:
        LOGGER.warning("A timeout occurred when connecting to {}".format(url))
    # if port has not be found in local data, try to get information from remote servers
    port_min, port_max = get_ports_range()
    host = "127.0.0.1"
    for _port in range(port_min, port_max):
        try:
            req = requests.get("http://{}:{}/status".format(host, _port), timeout=1)
            data = req.json()
            if "status" in data and data["status"]["uuid"] == uuid:
                return "http://{}:{}".format(host, _port)
        except Exception as e:
            LOGGER.warning("Error getting information from {} ({})".format(host, str(e)))
            return


def start_new_server(uuid):
    """Start a new server in a new process

    :param uuid: UUID of the server
    :return: nothing
    """
    _url = get_server_url(uuid)
    config_dir = get_configuration("orchestration").get("config_dir", "/tmp")  # nosec
    server_ip = "127.0.0.1"
    config_filename = os.path.join(config_dir, "moon_{}.yaml".format(uuid))
    LOGGER.info("Starting server {} {}".format(_url, uuid))
    if _url:
        _port = int(_url.split(":")[-1])
        add_server_port(_port)
        config = yaml.safe_load(open(config_filename))
        log_file = config["logging"]["handlers"]["file"]["filename"]
        _out = {
            "pipeline_id": uuid,
            "starttime": time.time(),
            "port": _port,
            "host": server_ip,
            "server_ip": server_ip,
            "log_file": log_file
        }
    else:
        _port = get_next_port()
        create_moon_config(uuid=uuid)
        pid_file = os.path.join(config_dir, uuid + ".pid")
        # NOTE: we have actually no solution to get the actual IP address
        # so we need to put 0.0.0.0 in the host address
        gunicorn_config = create_gunicorn_config(
            host="0.0.0.0",  # nosec
            port=_port,
            server_type="pipeline",
            uuid=uuid)
        command = ["gunicorn", "moon_engine.server:__hug_wsgi__", "--threads", "10",
                   "-p", pid_file, "-D", "-c", gunicorn_config]
        LOGGER.info("Executing {}".format(" ".join(command)))
        subprocess.Popen(command, stdout=subprocess.PIPE, close_fds=True)  # nosec
        # (command attribute is safe)
        _out = {
            "pipeline_id": uuid,
            "starttime": time.time(),
            "port": _port,
            "host": server_ip,
            "server_ip": server_ip,
            "process": pid_file,
        }
        time.sleep(1)
        config = yaml.safe_load(open(config_filename))
        log_file = config["logging"]["handlers"]["file"]["filename"]
        _out["log"] = log_file
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
        while True:
            f_sock.seek(p_sock)
            latest_data = f_sock.read()
            p_sock = f_sock.tell()
            if latest_data and "APIKEY" in latest_data:
                _index_start = latest_data.index("APIKEY=") + len("APIKEY=")
                _index_stop = latest_data.index("\n", _index_start)
                key = latest_data[_index_start:_index_stop].strip()
                # api_key = get_api_key_for_user("admin")
                api_key = configuration.get_configuration('api_token')
                try:
                    engine_api_key = xor_decode(key, api_key)
                except exceptions.DecryptError:
                    engine_api_key = False
                _out["api_key"] = engine_api_key
                break
            time.sleep(1)

    return _out


class PipelineConnector(PipelineDriver):

    def __init__(self, driver_name, engine_name):
        self.driver_name = driver_name
        self.engine_name = engine_name

    def update_pipeline(self, pipeline_id, data):
        _url = get_server_url(pipeline_id)
        if not _url:
            self.add_pipeline(pipeline_id, data)
        if "security_pipeline" in data:
            req = requests.post("{}/update".format(_url), json={"attributes": "pdp"})
            if req.status_code == 206:
                LOGGER.warning("No pipeline available...")
            elif req.status_code != 202:
                LOGGER.warning("Error sending upgrade command to pipeline ({})".format(req))
        if "vim_project_id" in data and data['vim_project_id']:
            LOGGER.warning("Cannot update vim_project_id for the moment")
            # FIXME: manage vim_project_id

    def delete_pipeline(self, pipeline_id):
        LOGGER.info("Deleting pipeline {}".format(pipeline_id))
        kill_server(pipeline_id)

    def add_pipeline(self, pipeline_id=None, data=None):
        LOGGER.debug("Adding POD in Engine {} {}".format(pipeline_id, data))
        if not pipeline_id:
            pipeline_id = uuid4().hex
        if not data:
            content = dict()
        else:
            content = dict(data)
        content.update(start_new_server(pipeline_id))
        pipelines[pipeline_id] = content
        return pipelines[pipeline_id]

    def get_pipelines(self, pipeline_id=None):
        results = {}
        for interface in pipelines:
            results[interface] = {
                "starttime": pipelines[interface]["starttime"],
                "port": pipelines[interface]["port"],
                "server_ip": pipelines[interface]["server_ip"],
                "status": "down",
                "log": pipelines[interface]["log"]
            }
            try:
                req = requests.get("http://{}:{}/status".format(
                    pipelines[interface]["server_ip"],
                    pipelines[interface]["port"]
                ))
                if req.status_code == 200:
                    results[interface]["status"] = "up"
            except TimeoutError:
                LOGGER.warning("Timeout connecting {} on port {}".format(
                    pipelines[interface]["server_ip"],
                    pipelines[interface]["port"]
                ))
        return results

    def get_pipeline_api_key(self, pipeline_id):
        return pipelines.get(pipeline_id, {}).get('api_key', "")


class Connector(PipelineConnector):
    pass


init()
