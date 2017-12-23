# Copyright 2017 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import docker
import logging
import re
import requests
import time
from python_moonutilities import configuration, exceptions

__version__ = "0.1.0"

LOG = logging.getLogger("moon.interface.container")


class DockerManager:

    def __init__(self):
        docker_conf = configuration.get_configuration("docker")['docker']
        self.docker = docker.DockerClient(base_url=docker_conf['url'])

    def create_container(self, data):
        """Create the container through the docker client

        :param data: {
            "name": "authz",
            "hostname": "authz123456789",
            "port": {
                "PrivatePort": 8090,
                "Type": "tcp",
                "IP": "0.0.0.0",
                "PublicPort": 8090
            },
            "keystone_project_id": "keystone_project_id1",
            "pdp_id": "123456789",
            "container_name": "wukongsun/moon_authz:v4.1"
        }
        :return: container output
        """
        output = self.docker.containers.run(
            image=data.get("container_name"),
            hostname=data.get("hostname", data.get("name"))[:63],
            name=data.get("name"),
            network='moon',
            ports={'{}/{}'.format(
                data.get("port").get("PrivatePort"),
                data.get("port").get("Type")
            ): int(data.get("port").get("PrivatePort"))},
            environment={
                "UUID": data.get("hostname"),
                "BIND": data.get("port").get("IP"),
                "TYPE": data.get("plugin_name"),
                "PORT": data.get("port").get("PrivatePort"),
                "PDP_ID": data.get("pdp_id"),
                "META_RULE_ID": data.get("meta_rule_id"),
                "KEYSTONE_PROJECT_ID": data.get("keystone_project_id"),
            },
            detach=True
        )
        try:
            req = requests.head("http://{}:{}/".format(data.get("hostname"), data.get("port").get("PublicPort")))
        except requests.exceptions.ConnectionError:
            pass
        else:
            if req.status_code != 200:
                raise exceptions.DockerError("Container {} is not running!".format(data.get("hostname")))
            output.ip = "0.0.0.0"
            return output

        # Note: host is not reachable through hostname so trying to find th IP address
        res = output.exec_run("ip addr")
        find = re.findall("inet (\d+\.\d+\.\d+\.\d+)", res.decode("utf-8"))
        ip = "127.0.0.1"
        for ip in find:
            if ip.startswith("127"):
                continue
            break
        cpt = 0
        while True:
            try:
                req = requests.head("http://{}:{}/".format(ip, data.get("port").get("PublicPort")))
            except requests.exceptions.ConnectionError:
                pass
            else:
                if req.status_code not in (200, 201):
                    LOG.error("url={}".format("http://{}:{}/".format(ip, data.get("port").get("PublicPort"))))
                    LOG.error("req={}".format(req))
                    raise exceptions.DockerError("Container {} is not running!".format(data.get("hostname")))
                output.ip = ip
                return output
            finally:
                cpt += 1
                time.sleep(0.1)
                if cpt > 20:
                    break
        output.ip = ip
        return output

    def delete_container(self, uuid):
        raise NotImplementedError
