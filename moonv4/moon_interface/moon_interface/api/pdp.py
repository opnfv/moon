# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
PDP are Policy Decision Point.

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


class PDP(Resource):
    """
    Endpoint for pdp requests
    """

    __urls__ = (
        "/pdp",
        "/pdp/",
        "/pdp/<string:uuid>",
        "/pdp/<string:uuid>/",
    )

    @check_auth
    def get(self, uuid=None, user_id=None):
        """Retrieve all pdp

        :param uuid: uuid of the pdp
        :param user_id: user ID who do the request
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "keystone_project_id": "keystone_project_id1",
                "description": "...",
            }
        }
        :internal_api: get_pdp
        """
        return call(ctx={"id": uuid, "method": "get_pdp", "user_id": user_id}, args={})

    @check_auth
    def post(self, uuid=None, user_id=None):
        """Create pdp.

        :param uuid: uuid of the pdp (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "name": "...",
            "security_pipeline": [...],
            "keystone_project_id": "keystone_project_id1",
            "description": "...",
        }
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "keystone_project_id": "keystone_project_id1",
                "description": "...",
            }
        }
        :internal_api: add_pdp
        """
        return call(ctx={"id": uuid, "method": "add_pdp", "user_id": user_id}, args=request.json)

    @check_auth
    def delete(self, uuid=None, user_id=None):
        """Delete a pdp

        :param uuid: uuid of the pdp to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_pdp
        """
        return call(ctx={"id": uuid, "method": "delete_pdp", "user_id": user_id}, args={})

    @check_auth
    def patch(self, uuid=None, user_id=None):
        """Update a pdp

        :param uuid: uuid of the pdp to update
        :param user_id: user ID who do the request
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "keystone_project_id": "keystone_project_id1",
                "description": "...",
            }
        }
        :internal_api: update_pdp
        """
        return call(ctx={"id": uuid, "method": "update_pdp", "user_id": user_id}, args=request.json)

