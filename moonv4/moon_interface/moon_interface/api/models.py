# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Models aggregate multiple meta rules
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


class Models(Resource):
    """
    Endpoint for model requests
    """

    __urls__ = (
        "/models",
        "/models/",
        "/models/<string:uuid>",
        "/models/<string:uuid>/",
    )

    @check_auth
    def get(self, uuid=None, user_id=None):
        """Retrieve all models

        :param uuid: uuid of the model
        :param user_id: user ID who do the request
        :return: {
            "model_id1": {
                "name": "...",
                "description": "...",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: get_models
        """
        return call(ctx={"id": uuid, "method": "get_models", "user_id": user_id}, args={})

    @check_auth
    def post(self, uuid=None, user_id=None):
        """Create model.

        :param uuid: uuid of the model (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "name": "...",
            "description": "...",
            "meta_rules": ["meta_rule_id1", ]
        }
        :return: {
            "model_id1": {
                "name": "...",
                "description": "...",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: add_model
        """
        return call(ctx={"id": uuid, "method": "add_model", "user_id": user_id}, args=request.json)

    @check_auth
    def delete(self, uuid=None, user_id=None):
        """Delete a model

        :param uuid: uuid of the model to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_model
        """
        return call(ctx={"id": uuid, "method": "delete_model", "user_id": user_id}, args={})

    @check_auth
    def patch(self, uuid=None, user_id=None):
        """Update a model

        :param uuid: uuid of the model to update
        :param user_id: user ID who do the request
        :return: {
            "model_id1": {
                "name": "...",
                "description": "...",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: update_model
        """
        return call(ctx={"id": uuid, "method": "update_model", "user_id": user_id}, args=request.json)

