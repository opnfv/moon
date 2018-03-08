# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Policies are instances of security models and implement security policies

"""

from flask import request
from flask_restful import Resource
import logging
from python_moonutilities.security_functions import check_auth
from python_moondb.core import PolicyManager

__version__ = "4.3.2"

logger = logging.getLogger("moon.manager.api." + __name__)


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
                "genre": "... (optional)",
                "description": "... (optional)",
            }
        }
        :internal_api: get_policies
        """
        try:
            data = PolicyManager.get_policies(user_id=user_id, policy_id=uuid)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"policies": data}

    @check_auth
    def post(self, uuid=None, user_id=None):
        """Create policy.

        :param uuid: uuid of the policy (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "name": "...",
            "model_id": "...",
            "genre": "... (optional)",
            "description": "... (optional)",
        }
        :return: {
            "policy_id1": {
                "name": "...",
                "model_id": "...",
                "genre": "... (optional)",
                "description": "... (optional)",
            }
        }
        :internal_api: add_policy
        """
        try:
            data = PolicyManager.add_policy(
                user_id=user_id, policy_id=uuid, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"policies": data}

    @check_auth
    def delete(self, uuid=None, user_id=None):
        """Delete a policy

        :param uuid: uuid of the policy to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_policy
        """
        try:
            data = PolicyManager.delete_policy(user_id=user_id, policy_id=uuid)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"result": True}

    @check_auth
    def patch(self, uuid=None, user_id=None):
        """Update a policy

        :param uuid: uuid of the policy to update
        :param user_id: user ID who do the request
        :return: {
            "policy_id1": {
                "name": "...",
                "model_id": "...",
                "genre": "... (optional)",
                "description": "... (optional)",
            }
        }
        :internal_api: update_policy
        """
        try:
            data = PolicyManager.update_policy(
                user_id=user_id, policy_id=uuid, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"policies": data}

