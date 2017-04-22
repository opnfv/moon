# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Rules (TODO)
"""

from flask import request
from flask_restful import Resource
from oslo_config import cfg
from oslo_log import log as logging
from moon_interface.tools import call
from moon_interface.tools import check_auth

__version__ = "0.1.0"

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


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
                "rule_id1": ["subject_data_id1", "object_data_id1", "action_data_id1"],
                "rule_id2": ["subject_data_id2", "object_data_id2", "action_data_id2"],
            ]
        }
        :internal_api: get_rules
        """
        return call(ctx={"id": uuid,
                         "method": "get_rules",
                         "user_id": user_id,
                         "rule_id": rule_id}, args={})

    @check_auth
    def post(self, uuid=None, rule_id=None, user_id=None):
        """Add a rule to a meta rule

        :param uuid: policy ID
        :param rule_id: rule ID
        :param user_id: user ID who do the request
        :request body: post = {
            "meta_rule_id": "meta_rule_id1",
            "rule": ["subject_data_id2", "object_data_id2", "action_data_id2"],
            "enabled": True
        }
        :return: {
            "rules": [
                "meta_rule_id": "meta_rule_id1",
                "rule_id1": ["subject_data_id1", "object_data_id1", "action_data_id1"],
                "rule_id2": ["subject_data_id2", "object_data_id2", "action_data_id2"],
            ]
        }
        :internal_api: add_rule
        """
        return call(ctx={"id": uuid,
                         "method": "add_rule",
                         "user_id": user_id,
                         "rule_id": rule_id}, args=request.json)

    @check_auth
    def delete(self, uuid=None, rule_id=None, user_id=None):
        """Delete one rule linked to a specific sub meta rule

        :param uuid: policy ID
        :param rule_id: rule ID
        :param user_id: user ID who do the request
        :return: { "result": true }
        :internal_api: delete_rule
        """
        return call(ctx={"id": uuid,
                         "method": "delete_rule",
                         "user_id": user_id,
                         "rule_id": rule_id}, args={})

