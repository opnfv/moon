# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Meta Data are elements used to create Meta data (skeleton of security policies)

"""

from flask import request
from flask_restful import Resource
from oslo_config import cfg
from oslo_log import log as logging
from moon_interface.tools import call
from moon_interface.tools import check_auth

__version__ = "0.2.0"

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class SubjectCategories(Resource):
    """
    Endpoint for subject categories requests
    """

    __urls__ = (
        "/subject_categories",
        "/subject_categories/",
        "/subject_categories/<string:category_id>",
    )

    @check_auth
    def get(self, category_id=None, user_id=None):
        """Retrieve all subject categories or a specific one

        :param category_id: uuid of the subject category
        :param user_id: user ID who do the request
        :return: {
            "subject_category_id": {
                "name": "name of the category",
                "description": "description of the category"
            }
        }
        :internal_api: get_subject_categories
        """
        return call(ctx={"method": "get_subject_categories", "user_id": user_id}, args={"category_id": category_id})

    @check_auth
    def post(self, category_id=None, user_id=None):
        """Create or update a subject category.

        :param category_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the category",
            "description": "description of the category"
        }
        :return: {
            "subject_category_id": {
                "name": "name of the category",
                "description": "description of the category"
            }
        }
        :internal_api: add_subject_category
        """
        return call(ctx={"method": "set_subject_category", "user_id": user_id}, args=request.json)

    @check_auth
    def delete(self, category_id=None, user_id=None):
        """Delete a subject category

        :param category_id: uuid of the subject category to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_subject_category
        """
        return call(ctx={"method": "delete_subject_category", "user_id": user_id}, args={"category_id": category_id})


class ObjectCategories(Resource):
    """
    Endpoint for object categories requests
    """

    __urls__ = (
        "/object_categories",
        "/object_categories/",
        "/object_categories/<string:category_id>",
    )

    @check_auth
    def get(self, category_id=None, user_id=None):
        """Retrieve all object categories or a specific one

        :param category_id: uuid of the object category
        :param user_id: user ID who do the request
        :return: {
            "object_category_id": {
                "name": "name of the category",
                "description": "description of the category"
            }
        }
        :internal_api: get_object_categories
        """
        return call(ctx={"method": "get_object_categories", "user_id": user_id}, args={"category_id": category_id})

    @check_auth
    def post(self, category_id=None, user_id=None):
        """Create or update a object category.

        :param category_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the category",
            "description": "description of the category"
        }
        :return: {
            "object_category_id": {
                "name": "name of the category",
                "description": "description of the category"
            }
        }
        :internal_api: add_object_category
        """
        return call(ctx={"method": "set_object_category", "user_id": user_id}, args=request.json)

    @check_auth
    def delete(self, category_id=None, user_id=None):
        """Delete an object category

        :param category_id: uuid of the object category to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_object_category
        """
        return call(ctx={"method": "delete_object_category", "user_id": user_id}, args={"category_id": category_id})


class ActionCategories(Resource):
    """
    Endpoint for action categories requests
    """

    __urls__ = (
        "/action_categories",
        "/action_categories/",
        "/action_categories/<string:category_id>",
    )

    @check_auth
    def get(self, category_id=None, user_id=None):
        """Retrieve all action categories or a specific one

        :param category_id: uuid of the action category
        :param user_id: user ID who do the request
        :return: {
            "action_category_id": {
                "name": "name of the category",
                "description": "description of the category"
            }
        }
        :internal_api: get_action_categories
        """
        return call(ctx={"method": "get_action_categories", "user_id": user_id}, args={"category_id": category_id})

    @check_auth
    def post(self, category_id=None, user_id=None):
        """Create or update an action category.

        :param category_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the category",
            "description": "description of the category"
        }
        :return: {
            "action_category_id": {
                "name": "name of the category",
                "description": "description of the category"
            }
        }
        :internal_api: add_action_category
        """
        return call(ctx={"method": "set_action_category", "user_id": user_id}, args=request.json)

    @check_auth
    def delete(self, category_id=None, user_id=None):
        """Delete an action

        :param category_id: uuid of the action category to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_action_category
        """
        return call(ctx={"method": "delete_action_category", "user_id": user_id}, args={"category_id": category_id})
