# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Policies are instances of security models and implement security policies

"""

from flask import request
from flask_restful import Resource
from oslo_config import cfg
from oslo_log import log as logging
from moon_utilities.security_functions import call
from moon_interface.tools import check_auth

__version__ = "0.1.0"

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Policies(Resource):
    """
    Endpoint for policy requests
    """

    __urls__ = (
        "/policies",
        "/policies/",
        "/policies/<string:uuid>",
        "/policies/<string:uuid>/",
    )

    @check_auth
    def get(self, uuid=None, user_id=None):
        """Retrieve all policies

        :param uuid: uuid of the policy
        :param user_id: user ID who do the request
        :return: {
            "policy_id1": {
                "name": "...",
                "model_id": "...",
                "genre": "...",
                "description": "...",
            }
        }
        :internal_api: get_policies
        """
        return call("security_router", ctx={"id": uuid, "method": "get_policies", "user_id": user_id}, args={})

    @check_auth
    def post(self, uuid=None, user_id=None):
        """Create policy.

        :param uuid: uuid of the policy (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "name": "...",
            "model_id": "...",
            "genre": "...",
            "description": "...",
        }
        :return: {
            "policy_id1": {
                "name": "...",
                "model_id": "...",
                "genre": "...",
                "description": "...",
            }
        }
        :internal_api: add_policy
        """
        return call("security_router", ctx={"id": uuid, "method": "add_policy", "user_id": user_id}, args=request.json)

    @check_auth
    def delete(self, uuid=None, user_id=None):
        """Delete a policy

        :param uuid: uuid of the policy to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_policy
        """
        return call("security_router", ctx={"id": uuid, "method": "delete_policy", "user_id": user_id}, args={})

    @check_auth
    def patch(self, uuid=None, user_id=None):
        """Update a policy

        :param uuid: uuid of the policy to update
        :param user_id: user ID who do the request
        :return: {
            "policy_id1": {
                "name": "...",
                "model_id": "...",
                "genre": "...",
                "description": "...",
            }
        }
        :internal_api: update_policy
        """
        return call("security_router", ctx={"id": uuid, "method": "update_policy", "user_id": user_id}, args=request.json)

