# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""Status API"""
import hug
import logging
import requests
from moon_utilities.auth_functions import api_key_authentication, connect_from_env
from moon_manager import orchestration_driver
from moon_manager.api import configuration
from datetime import datetime

logger = logging.getLogger("moon.manager.api.status")


class Status(object):
    """
    Endpoint for status requests
    """
    @staticmethod
    @hug.local()
    @hug.get("/status/", requires=api_key_authentication)
    def list_status(authed_user: hug.directives.user=None):
        """
        List statuses
        :return: JSON status output
        """
        pipelines = orchestration_driver.PipelineManager.get_pipelines(moon_user_id=authed_user)
        slaves = orchestration_driver.SlaveManager.get_slaves(moon_user_id=authed_user)

        config = configuration.search_config_file("moon.yaml")
        log_file = config["logging"]["handlers"]["file"]["filename"]

        result = {"status": {
            "manager": {"name": "manager", "status": "up", "log": log_file},
        }}

        for slave in slaves:
            result["status"][slave] = slaves[slave]
        for slave in pipelines:
            result["status"][slave].update(pipelines[slave])

        web_port = config["dashboard"]["port"]
        url = ":".join(config["management"]["url"].split(":")[:-1])

        result["status"]["web_GUI"] = {"name": "web GUI", "status": "down"}
        try:
            req = requests.get(f"{url}:{web_port}")
        except requests.exceptions.ConnectionError:
            req = None

        if req and req.status_code == 200:
            result["status"]["web_GUI"].update({"status": "up", "port": web_port})

        return result


StatusAPI = hug.API(name='status', doc=Status.__doc__)


@hug.cli("status")
def status(quiet: bool = False, human: bool = False):
    """
    CLI Parameter to get status
    :param quiet: 
    :param human: 
    :return: JSON status output
    """
    db_conf = configuration.get_configuration(key='management')
    manager_api_key = connect_from_env()
    _status = requests.get("{}/status".format(db_conf.get("url")),
                           headers={"x-api-key": manager_api_key}
                           )

    if _status.status_code == 200:
        if human:
            result = "Status"
            statuses = _status.json()["status"].items()
            for uuid, values in statuses:
                # for humans, it's best to call the servers by their name
                # instead of their uuid
                result += f"\n{values['name']} :"
                if quiet:
                    result += " OK" if values["status"] == "up" else " KO"
                    pipelines = values.get("pipelines")
                    if pipelines is not None:
                        for pipeline_uuid in pipelines:
                            result += f"\n\t{pipeline_uuid} :"
                            result += " OK" if pipelines[pipeline_uuid]["status"] == "up" else " KO"
                else:
                    result += "\n"  # not quiet mode : newline needed
                    result += f"\tuuid : {uuid}\n"
                    for k2, v2 in values.items():
                        if k2 == "pipelines":
                            result += StatusCLI.format_pipelines_for_status(values["pipelines"])
                        elif k2 == "starttime":
                            result += f"\t{k2} : {datetime.fromtimestamp(v2).strftime('%d/%m/%Y %H:%M:%S')}\n"
                        elif k2 != "name":
                            result += f"\t{k2} : {v2}\n"
            return result
        else:
            return _status.json()


@hug.object(name='status', version='1.0.0', api=StatusAPI)
class StatusCLI(object):
    """An example of command like calls via an Object"""
    @staticmethod
    def format_pipelines_for_status(pipelines):
        result = ""
        for pipeline in pipelines:
            result += f"\n\t{pipeline} :\n"
            for k,v in pipelines[pipeline].items():
                if k == "starttime":
                    result += f"\t\t{k} : {datetime.fromtimestamp(v).strftime('%d/%m/%Y %H:%M:%S')}\n"
                else:
                    result += f"\t\t{k} : {v}\n"
        return result
