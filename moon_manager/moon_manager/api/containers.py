# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
PDP are Policy Decision Point.

"""

import copy
from docker import Client
from flask import request
from flask_restful import Resource
from oslo_log import log as logging
from python_moonutilities.security_functions import check_auth
from python_moonutilities import configuration

docker_conf = configuration.get_configuration("docker")['docker']
docker = Client(base_url=docker_conf['url'])

__version__ = "0.1.0"

LOG = logging.getLogger("moon.manager.api." + __name__)


class Container(Resource):
    """
    Endpoint for container requests
    """

    __urls__ = (
        "/containers",
        "/containers/",
        "/containers/<string:uuid>",
        "/containers/<string:uuid>/",
    )

    def __init__(self):
        self.containers = {}
        self.update()

    def update(self):
        for _container in docker.containers():
            if _container['Id'] not in self.containers:
                self.containers[_container['Id']] = {
                    "name": _container["Names"],
                    "port": _container["Ports"],
                }

    @check_auth
    def get(self, uuid=None, user_id=None):
        """Retrieve all containers

        :param uuid: uuid of the container
        :param user_id: user ID who do the request
        :return: {
            "containers": {
                "da0fd80fc1dc146e1b...a2e07d240cde09f0a": {
                    "name": [
                        "/wrapper"
                    ],
                    "port": [
                        {
                            "PrivatePort": 8080,
                            "Type": "tcp",
                            "IP": "0.0.0.0",
                            "PublicPort": 8080
                        }
                    ]
                },
            }
        }
        :internal_api: get_containers
        """
        # try:
        #     data = [{"name": item["Names"], "port": item["Ports"], } for item in docker.containers()]
        # except Exception as e:
        #     LOG.error(e, exc_info=True)
        #     return {"result": False,
        #             "error": str(e)}
        return {"containers": self.containers}

    @check_auth
    def post(self, uuid=None, user_id=None):
        """Add a new container.

        :param uuid: uuid of the pdp (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "id": "id of the new container",
            "name": "name of the new container",
            "hostname": "hostname of the new container",
            "port": {
                "PrivatePort": 8080,
                "Type": "tcp",
                "IP": "0.0.0.0",
                "PublicPort": 8080
            },
            "keystone_project_id": "keystone_project_id1",
            "pdp_id": "PDP UUID",
            "container_name": "wukongsun/moon_authz:v4.1"
        }
        :return: {
            "containers": {
                "da0fd80fc1dc146e1b...a2e07d240cde09f0a": {
                    "name": [
                        "/wrapper"
                    ],
                    "port": [
                        {
                            "PrivatePort": 8080,
                            "Type": "tcp",
                            "IP": "0.0.0.0",
                            "PublicPort": 8080
                        }
                    ]
                },
            }
        }
        :internal_api: add_container
        """
        try:
            self.update()
            self.containers[request.json.get('id')] = copy.deepcopy(request.json)
            LOG.info("Added a new container {}".format(request.json.get('name')))
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"containers": self.containers}

    @check_auth
    def delete(self, uuid=None, user_id=None):
        """Delete a pdp

        :param uuid: uuid of the pdp to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_pdp
        """
        # try:
        #     data = PDPManager.delete_pdp(user_id=user_id, pdp_id=uuid)
        # except Exception as e:
        #     LOG.error(e, exc_info=True)
        #     return {"result": False,
        #             "error": str(e)}
        # return {"result": True}
        raise NotImplementedError

    @check_auth
    def patch(self, uuid=None, user_id=None):
        """Update a pdp

        :param uuid: uuid of the pdp to update
        :param user_id: user ID who do the request
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "keystone_project_id": "keystone_project_id1",
                "description": "...",
            }
        }
        :internal_api: update_pdp
        """
        # try:
        #     data = PDPManager.update_pdp(user_id=user_id, pdp_id=uuid, value=request.json)
        #     add_container(uuid=uuid, pipeline=data[uuid]['security_pipeline'])
        # except Exception as e:
        #     LOG.error(e, exc_info=True)
        #     return {"result": False,
        #             "error": str(e)}
        # return {"pdps": data}
        raise NotImplementedError

