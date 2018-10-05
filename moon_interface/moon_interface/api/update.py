# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Authz is the endpoint to get authorization response
"""

from flask import request
from flask_restful import Resource
import requests
import logging

__version__ = "4.3.1"

logger = logging.getLogger("moon.interface.api." + __name__)


class Update(Resource):
    """
    Endpoint for update requests
    """

    __urls__ = (
        "/update",
    )

    def __init__(self, **kwargs):
        self.CACHE = kwargs.get("cache")
        self.INTERFACE_NAME = kwargs.get("interface_name", "interface")
        self.MANAGER_URL = kwargs.get("manager_url", "http://manager:8080")
        self.TIMEOUT = 5

    def put(self):
        try:
            self.CACHE.update_assignments(
                request.form.get("policy_id", None),
                request.form.get("perimeter_id", None),
            )
            for project_id in self.CACHE.container_chaining:
                hostname = self.CACHE.container_chaining[project_id][0]["hostip"]
                port = self.CACHE.container_chaining[project_id][0]["port"]
                req = requests.put("http://{}:{}/update".format(hostname, port), request.form)
                if req.status_code != 200:
                    logger.error("Cannot connect to {} on port {}".format(hostname, port))
        except Exception as e:
            logger.exception(e)
            return {"result": False, "reason": str(e)}
        return {"result": True}
