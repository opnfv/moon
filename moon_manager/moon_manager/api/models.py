# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Models aggregate multiple meta rules
"""

from flask import request
from flask_restful import Resource
import logging
from python_moonutilities.security_functions import check_auth
from python_moondb.core import ModelManager

__version__ = "4.3.2"

logger = logging.getLogger("moon.manager.api." + __name__)


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
                "description": "... (optional)",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: get_models
        """
        try:
            data = ModelManager.get_models(user_id=user_id, model_id=uuid)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"models": data}

    @check_auth
    def post(self, uuid=None, user_id=None):
        """Create model.

        :param uuid: uuid of the model (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the model (mandatory)",
            "description": "description of the model (optional)",
            "meta_rules": ["meta_rule_id1", ]
        }
        :return: {
            "model_id1": {
                "name": "name of the model",
                "description": "description of the model (optional)",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: add_model
        """
        try:
            data = ModelManager.add_model(
                user_id=user_id, model_id=uuid, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"models": data}

    @check_auth
    def delete(self, uuid, user_id=None):
        """Delete a model

        :param uuid: uuid of the model to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_model
        """
        try:
            data = ModelManager.delete_model(user_id=user_id, model_id=uuid)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"result": True}

    @check_auth
    def patch(self, uuid, user_id=None):
        """Update a model

        :param uuid: uuid of the model to update
        :param user_id: user ID who do the request
        :return: {
            "model_id1": {
                "name": "name of the model",
                "description": "... (optional)",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: update_model
        """
        try:
            data = ModelManager.update_model(
                user_id=user_id, model_id=uuid, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"models": data}

