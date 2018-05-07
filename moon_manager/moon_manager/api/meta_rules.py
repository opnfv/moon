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
        try:
            data = ModelManager.get_meta_rules(
                user_id=user_id, meta_rule_id=meta_rule_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"meta_rules": data}

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
        try:
            data = ModelManager.add_meta_rule(
                user_id=user_id, meta_rule_id=None, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"meta_rules": data}

    @check_auth
    def patch(self, meta_rule_id, user_id=None):
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
        try:
            data = ModelManager.set_meta_rule(
                user_id=user_id, meta_rule_id=meta_rule_id, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"meta_rules": data}

    @check_auth
    def delete(self, meta_rule_id, user_id=None):
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
        try:
            data = ModelManager.delete_meta_rule(
                user_id=user_id, meta_rule_id=meta_rule_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"result": True}

