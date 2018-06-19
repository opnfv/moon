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
from python_moonutilities.security_functions import validate_input


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

    @validate_input("get", kwargs_state=[False, False])
    @check_auth
    def get(self, uuid=None, user_id=None):
        """Retrieve all policies

        :param uuid: uuid of the policy
        :param user_id: user ID who do the request
        :return: {
            "policy_id1": {
                "name": "name of the policy (mandatory)",
                "model_id": "ID of the model linked to this policy",
                "genre": "authz of admin (optional, default to authz)",
                "description": "description of the policy (optional)",
            }
        }
        :internal_api: get_policies
        """

        data = PolicyManager.get_policies(user_id=user_id, policy_id=uuid)

        return {"policies": data}

    @validate_input("post", body_state={"name": True, "model_id":True})
    @check_auth
    def post(self, uuid=None, user_id=None):
        """Create policy.

        :param uuid: uuid of the policy (not used here if a new policy is created)
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the policy (mandatory)",
            "model_id": "ID of the model linked to this policy",
            "genre": "authz of admin (optional, default to authz)",
            "description": "description of the policy (optional)",
        }
        :return: {
            "policy_id1": {
                "name": "name of the policy (mandatory)",
                "model_id": "ID of the model linked to this policy",
                "genre": "authz of admin (optional, default to authz)",
                "description": "description of the policy (optional)",
            }
        }
        :internal_api: add_policy
        """

        data = PolicyManager.add_policy(
            user_id=user_id, policy_id=uuid, value=request.json)

        return {"policies": data}

    @validate_input("delete", kwargs_state=[ True, False])
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

        data = PolicyManager.delete_policy(user_id=user_id, policy_id=uuid)

        return {"result": True}

    @validate_input("patch", kwargs_state=[True, False], body_state={"name": True, "model_id":True})
    @check_auth
    def patch(self, uuid=None, user_id=None):
        """Update a policy

        :param uuid: uuid of the policy to update
        :param user_id: user ID who do the request
        :return: {
            "policy_id1": {
                "name": "name of the policy (mandatory)",
                "model_id": "ID of the model linked to this policy",
                "genre": "authz of admin (optional, default to authz)",
                "description": "description of the policy (optional)",
            }
        }
        :internal_api: update_policy
        """

        data = PolicyManager.update_policy(
            user_id=user_id, policy_id=uuid, value=request.json)

        return {"policies": data}

