# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Meta rules are skeleton for security policies

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


class MetaRules(Resource):
    """
    Endpoint for meta rules requests
    """

    __urls__ = ("/meta_rules",
                "/meta_rules/",
                "/meta_rules/<string:meta_rule_id>",
                "/meta_rules/<string:meta_rule_id>/")

    @check_auth
    def get(self, meta_rule_id=None, user_id=None):
        """Retrieve all sub meta rules

        :param meta_rule_id: Meta rule algorithm ID
        :param user_id: user ID who do the request
        :return: {
            "meta_rules": {
                "meta_rule_id1": {
                    "name": "name of the meta rule",
                    "algorithm": "name of the meta rule algorithm",
                    "subject_categories": ["subject_category_id1", "subject_category_id2"],
                    "object_categories": ["object_category_id1"],
                    "action_categories": ["action_category_id1"]
                },
            }
        }
        :internal_api: get_meta_rules
        """
        return call("security_router", ctx={"method": "get_meta_rules",
                         "user_id": user_id,
                         "meta_rule_id": meta_rule_id}, args={})

    @check_auth
    def post(self, meta_rule_id=None, user_id=None):
        """Add a meta rule

        :param meta_rule_id: Meta rule ID
        :param user_id: user ID who do the request
        :request body: post = {
            "name": "name of the meta rule",
            "subject_categories": ["subject_category_id1", "subject_category_id2"],
            "object_categories": ["object_category_id1"],
            "action_categories": ["action_category_id1"]
        }
        :return: {
            "meta_rules": {
                "meta_rule_id1": {
                    "name": "name of the meta rule",
                    "subject_categories": ["subject_category_id1", "subject_category_id2"],
                    "object_categories": ["object_category_id1"],
                    "action_categories": ["action_category_id1"]
                },
            }
        }
        :internal_api: add_meta_rules
        """
        return call("security_router", ctx={"method": "add_meta_rules",
                         "user_id": user_id,
                         "meta_rule_id": meta_rule_id}, args=request.json)

    @check_auth
    def patch(self, meta_rule_id=None, user_id=None):
        """Update a meta rule

        :param meta_rule_id: Meta rule ID
        :param user_id: user ID who do the request
        :request body: patch = {
            "name": "name of the meta rule",
            "subject_categories": ["subject_category_id1", "subject_category_id2"],
            "object_categories": ["object_category_id1"],
            "action_categories": ["action_category_id1"]
        }
        :return: {
            "meta_rules": {
                "meta_rule_id1": {
                    "name": "name of the meta rule",
                    "subject_categories": ["subject_category_id1", "subject_category_id2"],
                    "object_categories": ["object_category_id1"],
                    "action_categories": ["action_category_id1"]
                },
            }
        }
        :internal_api: set_meta_rules
        """
        return call("security_router", ctx={"method": "set_meta_rules",
                         "user_id": user_id,
                         "meta_rule_id": meta_rule_id}, args=request.json)

    @check_auth
    def delete(self, meta_rule_id=None, user_id=None):
        """Delete a meta rule

        :param meta_rule_id: Meta rule ID
        :param user_id: user ID who do the request
        :request body: delete = {
            "name": "name of the meta rule",
            "subject_categories": ["subject_category_id1", "subject_category_id2"],
            "object_categories": ["object_category_id1"],
            "action_categories": ["action_category_id1"]
        }
        :return: {
            "meta_rules": {
                "meta_rule_id1": {
                    "name": "name of the meta rule",
                    "subject_categories": ["subject_category_id1", "subject_category_id2"],
                    "object_categories": ["object_category_id1"],
                    "action_categories": ["action_category_id1"]
                },
            }
        }
        :internal_api: delete_meta_rules
        """
        return call("security_router", ctx={"method": "delete_meta_rules",
                         "user_id": user_id,
                         "meta_rule_id": meta_rule_id}, args=request.json)


