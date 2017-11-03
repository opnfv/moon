# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from flask import request
from flask_restful import Resource
from moon_utilities.security_functions import check_auth
import logging

LOG = logging.getLogger("moon.orchestrator.api.pods")


class Pods(Resource):
    """
    Endpoint for pdp requests
    """

    __urls__ = (
        "/pods",
        "/pods/",
        "/pods/<string:uuid>",
        "/pods/<string:uuid>/",
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
        :internal_api: get_pdp
        """
        pods = {}
        # LOG.info("pods={}".format(self.driver.get_pods()))
        if uuid:
            return {"pods": self.driver.get_pods(uuid)}
        for _pod_key, _pod_values in self.driver.get_pods().items():
            pods[_pod_key] = []
            for _pod_value in _pod_values:
                if _pod_value['namespace'] != "moon":
                    continue
                pods[_pod_key].append(_pod_value)
        return {"pods": pods}

    @check_auth
    def post(self, uuid=None, user_id=None):
        """Create a new pod.

        :param uuid: uuid of the pod (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "name": "...",
            "description": "...",
            "type": "plugin_name"
        }
        :return: {
            "pdp_id1": {
                "name": "...",
                "replicas": "...",
                "description": "...",
            }
        }
        """
        return {"pods": None}

    @check_auth
    def delete(self, uuid=None, user_id=None):
        """Delete a pod

        :param uuid: uuid of the pod to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        """
        return {"result": True}

    @check_auth
    def patch(self, uuid=None, user_id=None):
        """Update a pod

        :param uuid: uuid of the pdp to update
        :param user_id: user ID who do the request
        :request body: {
            "name": "...",
            "replicas": "...",
            "description": "...",
        }
        :return: {
            "pod_id1": {
                "name": "...",
                "replicas": "...",
                "description": "...",
            }
        }
        :internal_api: update_pdp
        """
        return {"pods": None}

