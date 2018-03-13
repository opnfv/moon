# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Rules (TODO)
"""

from flask import request
from flask_restful import Resource
import logging
from python_moonutilities.security_functions import check_auth
from python_moondb.core import PolicyManager

__version__ = "4.3.2"

logger = logging.getLogger("moon.manager.api." + __name__)


class Rules(Resource):
    """
    Endpoint for rules requests
    """

    __urls__ = ("/policies/<string:uuid>/rules",
                "/policies/<string:uuid>/rules/",
                "/policies/<string:uuid>/rules/<string:rule_id>",
                "/policies/<string:uuid>/rules/<string:rule_id>/",
                )

    @check_auth
    def get(self, uuid=None, rule_id=None, user_id=None):
        """Retrieve all rules or a specific one

        :param uuid: policy ID
        :param rule_id: rule ID
        :param user_id: user ID who do the request
        :return: {
            "rules": [
                "policy_id": "policy_id1",
                "meta_rule_id": "meta_rule_id1",
                "rule_id1":
                    ["subject_data_id1", "subject_data_id2", "object_data_id1", "action_data_id1"],
                "rule_id2":
                    ["subject_data_id3", "subject_data_id4", "object_data_id2", "action_data_id2"],
            ]
        }
        :internal_api: get_rules
        """
        try:
            data = PolicyManager.get_rules(user_id=user_id,
                                           policy_id=uuid,
                                           rule_id=rule_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"rules": data}

    @check_auth
    def post(self, uuid=None, rule_id=None, user_id=None):
        """Add a rule to a meta rule

        :param uuid: policy ID
        :param rule_id: rule ID
        :param user_id: user ID who do the request
        :request body: post = {
            "meta_rule_id": "meta_rule_id1",
            "rule": ["subject_data_id2", "object_data_id2", "action_data_id2"],
            "instructions": (
                {"decision": "grant"},
            )
            "enabled": True
        }
        :return: {
            "rules": [
                "meta_rule_id": "meta_rule_id1",
                "rule_id1": {
                    "rule": ["subject_data_id1",
                             "object_data_id1",
                             "action_data_id1"],
                    "instructions": (
                        {"decision": "grant"},
                        # "grant" to immediately exit,
                        # "continue" to wait for the result of next policy
                        # "deny" to deny the request
                    )
                }
                "rule_id2": {
                    "rule": ["subject_data_id2",
                             "object_data_id2",
                             "action_data_id2"],
                    "instructions": (
                        {
                            "update": {
                                "operation": "add",
                                    # operations may be "add" or "delete"
                                "target": "rbac:role:admin"
                                    # add the role admin to the current user
                            }
                        },
                        {"chain": {"name": "rbac"}}
                            # chain with the policy named rbac
                    )
                }
            ]
        }
        :internal_api: add_rule
        """
        args = request.json
        try:
            data = PolicyManager.add_rule(user_id=user_id,
                                          policy_id=uuid,
                                          meta_rule_id=args['meta_rule_id'],
                                          value=args)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"rules": data}

    @check_auth
    def delete(self, uuid=None, rule_id=None, user_id=None):
        """Delete one rule linked to a specific sub meta rule

        :param uuid: policy ID
        :param rule_id: rule ID
        :param user_id: user ID who do the request
        :return: { "result": true }
        :internal_api: delete_rule
        """
        try:
            data = PolicyManager.delete_rule(
                user_id=user_id, policy_id=uuid, rule_id=rule_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"result": True}

