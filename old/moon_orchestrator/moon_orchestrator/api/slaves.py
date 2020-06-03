# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from flask import request
from flask_restful import Resource
from python_moonutilities.security_functions import check_auth
import logging

logger = logging.getLogger("moon.orchestrator.api.slaves")


class Slaves(Resource):
    """
    Endpoint for slaves requests
    """

    __version__ = "4.3.1"

    __urls__ = (
        "/slaves",
        "/slaves/",
        "/slaves/<string:uuid>",
        "/slaves/<string:uuid>/",
    )

    def __init__(self, **kwargs):
        self.driver = kwargs.get("driver")

    @check_auth
    def get(self, uuid=None, user_id=None):
        """Retrieve all pods

        :param uuid: uuid of the pod
        :param user_id: user ID who do the request
        :return: {
            "pod_id1": {
                "name": "...",
                "replicas": "...",
                "description": "...",
            }
        }
        """
        slaves = self.driver.get_slaves()
        return {"slaves": slaves}
