# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Assignments allow to connect data with elements of perimeter

"""

from flask import request
from flask_restful import Resource
# from oslo_config import cfg
from oslo_log import log as logging
# from moon_interface.tools import check_auth

__version__ = "0.1.0"

LOG = logging.getLogger(__name__)
# CONF = cfg.CONF


class Docker(Resource):
    """
    Endpoint for system requests
    """

    __urls__ = (
        "/configuration/docker",
    )

    def __init__(self, *args, **kwargs):
        self.conf = kwargs.get('conf', {})

    # @check_auth
    def get(self):
        """Retrieve docker configuration

        :return: {
            "docker": {
                "url": "hostname for the docker server (eg. /var/run/docker.sock)",
                "port": "port of the server",
                "user": "user of the server",
                "password": "password of the server",
                "protocol": "protocol to use (eg. unix)"
            }
        }
        """
        url = self.conf.DOCKER_URL
        # LOG.info(url)
        # hostname = url.split("@")[-1].split(":")[0].split("/")[0]
        # try:
        #     port = int(url.split("@")[-1].split(":")[1].split("/")[0])
        # except ValueError:
        #     port = None
        # user = url.split("//")[1].split(":")[0]
        # # TODO: password must be encrypted
        # try:
        #     password = url.split(":")[2].split("@")[0]
        # except IndexError:
        #     password = ""
        # protocol = url.split(":")[0]
        return {
            "docker": {
                "url": self.conf.DOCKER_URL,
                # "port": port,
                # "user": user,
                # "password": password,
                # "protocol": protocol,
            }
        }


class Components(Resource):
    """
    Endpoint for requests on components
    """

    __urls__ = (
        "/configuration/components",
        "/configuration/components/",
        "/configuration/components/<string:id_or_name>",
    )

    def __init__(self, *args, **kwargs):
        self.conf = kwargs.get('conf', {})

    # @check_auth
    def get(self, id_or_name=None):
        """Retrieve component list
        
        :param id_or_name: ID or name of the component

        :return: {
            "components": [ 
                {
                    "hostname": "hostname of the component",
                    "port": "port of the server in this component",
                    "id": "id of the component",
                    "keystone_id": "Keystone project ID served by this component if needed"
                },
            ]
        }
        """
        if id_or_name:
            for _component in self.conf.COMPONENTS:
                if id_or_name in (_component["hostname"], _component["id"]):
                    return {
                        "components": [_component, ]
                    }
            return {"components": []}
        return {"components": self.conf.COMPONENTS}

    # @check_auth
    def put(self, id_or_name=None):
        """Ask for adding a new component
        The response gives the TCP port to be used
        
        :param id_or_name: ID or name of the component
        :request body: {
            "hostname": "hostname of the new component",
            "keystone_id": "Keystone ID mapped to that component (if needed)"
        }
        :return: {
            "components": [ 
                {
                    "hostname": "hostname of the component",
                    "port": "port of the server in this component",
                    "id": "id of the component",
                    "keystone_id": "Keystone project ID served by this component"
                }
            ]
        }
        """
        if not id_or_name:
            return "Need a name for that component", 400
        for _component in self.conf.COMPONENTS:
            if id_or_name in (_component["hostname"], _component["id"]):
                return "ID already used", 409
        self.conf.COMPONENTS_PORT_START += 1
        port = self.conf.COMPONENTS_PORT_START
        data = request.json
        new_component = {
            "hostname": data.get("hostname", id_or_name),
            "port": port,
            "id": id_or_name,
            "keystone_id": data.get("keystone_id", "")
        }
        self.conf.COMPONENTS.append(new_component)
        return {
            "components": [new_component, ]
        }

    # @check_auth
    def delete(self, id_or_name=None):
        """Delete a component
        
        :param id_or_name: ID or name of the component
        :return: {
            "result": true
        }
        """
        if not id_or_name:
            return "Need a name for that component", 400
        for index, _component in enumerate(self.conf.COMPONENTS):
            if id_or_name in (_component["hostname"], _component["id"]):
                self.conf.COMPONENTS.pop(index)
                return {"result": True}
        return "Cannot find component named {}".format(id_or_name), 403

