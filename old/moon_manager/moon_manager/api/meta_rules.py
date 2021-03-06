# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Meta rules are skeleton for security policies

"""

from flask import request
from flask_restful import Resource
import logging
from python_moonutilities.security_functions import check_auth
from python_moondb.core import ModelManager
from python_moonutilities.security_functions import validate_input

__version__ = "4.3.2"

logger = logging.getLogger("moon.manager.api." + __name__)


class MetaRules(Resource):
    """
    Endpoint for meta rules requests
    """

    __urls__ = (
        "/meta_rules",
        "/meta_rules/",
        "/meta_rules/<string:meta_rule_id>",
        "/meta_rules/<string:meta_rule_id>/"
    )

    @validate_input("get", kwargs_state=[False, False])
    @check_auth
    def get(self, meta_rule_id=None, user_id=None):
        """Retrieve all sub meta rules

        :param meta_rule_id: Meta rule algorithm ID
        :param user_id: user ID who do the request
        :return: {
            "meta_rules": {
                "meta_rule_id1": {
                    "name": "name of the meta rule",
                    "subject_categories": ["subject_category_id1",
                                           "subject_category_id2"],
                    "object_categories": ["object_category_id1"],
                    "action_categories": ["action_category_id1"]
                },
            }
        }
        :internal_api: get_meta_rules
        """

        data = ModelManager.get_meta_rules(
            user_id=user_id, meta_rule_id=meta_rule_id)

        return {"meta_rules": data}

    @validate_input("post", body_state={"name": True, "subject_categories": False,
                                        "object_categories": False, "action_categories": False})
    @check_auth
    def post(self, meta_rule_id=None, user_id=None):
        """Add a meta rule

        :param meta_rule_id: Meta rule ID (not used here)
        :param user_id: user ID who do the request
        :request body: post = {
            "name": "name of the meta rule (mandatory)",
            "subject_categories": ["subject_category_id1 (mandatory)",
                                   "subject_category_id2"],
            "object_categories": ["object_category_id1 (mandatory)"],
            "action_categories": ["action_category_id1 (mandatory)"]
        }
        :return: {
            "meta_rules": {
                "meta_rule_id1": {
                    "name": "name of the meta rule",
                    "subject_categories": ["subject_category_id1",
                                           "subject_category_id2"],
                    "object_categories": ["object_category_id1"],
                    "action_categories": ["action_category_id1"]
                },
            }
        }
        :internal_api: add_meta_rules
        """

        data = ModelManager.add_meta_rule(
            user_id=user_id, meta_rule_id=None, value=request.json)

        return {"meta_rules": data}

    @validate_input("patch", kwargs_state=[True, False],
                    body_state={"name": True, "subject_categories": False,
                                "object_categories": False, "action_categories": False})
    @check_auth
    def patch(self, meta_rule_id=None, user_id=None):
        """Update a meta rule

        :param meta_rule_id: Meta rule ID
        :param user_id: user ID who do the request
        :request body: patch = {
            "name": "name of the meta rule",
            "subject_categories": ["subject_category_id1",
                                   "subject_category_id2"],
            "object_categories": ["object_category_id1"],
            "action_categories": ["action_category_id1"]
        }
        :return: {
            "meta_rules": {
                "meta_rule_id1": {
                    "name": "name of the meta rule",
                    "subject_categories": ["subject_category_id1",
                                           "subject_category_id2"],
                    "object_categories": ["object_category_id1"],
                    "action_categories": ["action_category_id1"]
                },
            }
        }
        :internal_api: set_meta_rules
        """
        data = ModelManager.update_meta_rule(
            user_id=user_id, meta_rule_id=meta_rule_id, value=request.json)

        return {"meta_rules": data}

    @validate_input("delete", kwargs_state=[True, False])
    @check_auth
    def delete(self, meta_rule_id=None, user_id=None):
        """Delete a meta rule

        :param meta_rule_id: Meta rule ID
        :param user_id: user ID who do the request
        :return: {
            "meta_rules": {
                "meta_rule_id1": {
                    "name": "name of the meta rule",
                    "subject_categories": ["subject_category_id1",
                                           "subject_category_id2"],
                    "object_categories": ["object_category_id1"],
                    "action_categories": ["action_category_id1"]
                },
            }
        }
        :internal_api: delete_meta_rules
        """

        data = ModelManager.delete_meta_rule(
            user_id=user_id, meta_rule_id=meta_rule_id)

        return {"result": True}
