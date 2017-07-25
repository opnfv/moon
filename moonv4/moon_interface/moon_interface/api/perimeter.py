# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
* Subjects are the source of an action on an object (examples : users, virtual machines)
* Objects are the destination of an action (examples virtual machines, virtual Routers)
* Actions are what subject wants to do on an object
"""

from flask import request
from flask_restful import Resource
from oslo_log import log as logging
from moon_utilities.security_functions import call
from moon_utilities.security_functions import check_auth

__version__ = "0.2.0"

LOG = logging.getLogger("moon.interface.api." + __name__)


class Subjects(Resource):
    """
    Endpoint for subjects requests
    """

    __urls__ = (
        "/subjects",
        "/subjects/",
        "/subjects/<string:perimeter_id>",
        "/policies/<string:uuid>/subjects",
        "/policies/<string:uuid>/subjects/",
        "/policies/<string:uuid>/subjects/<string:perimeter_id>",
    )

    @check_auth
    def get(self, uuid=None, perimeter_id=None, user_id=None):
        """Retrieve all subjects or a specific one if perimeter_id is given for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the subject
        :param user_id: user ID who do the request
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "a description"
            }
        }
        :internal_api: get_subjects
        """
        return call("security_router", ctx={"id": uuid, "method": "get_subjects", "user_id": user_id}, args={"perimeter_id": perimeter_id})

    @check_auth
    def post(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a subject.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the subject",
            "description": "description of the subject",
            "password": "password for the subject",
            "email": "email address of the subject"
        }
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "description of the subject",
                    "password": "password for the subject",
                    "email": "email address of the subject"
            }
        }
        :internal_api: set_subject
        """
        return call("security_router", ctx={"id": uuid, "method": "set_subject", "user_id": user_id, "perimeter_id": None},
                    args=request.json)

    @check_auth
    def patch(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a subject.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the subject",
            "description": "description of the subject",
            "password": "password for the subject",
            "email": "email address of the subject"
        }
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "description of the subject",
                    "password": "password for the subject",
                    "email": "email address of the subject"
            }
        }
        :internal_api: set_subject
        """
        return call("security_router", ctx={"id": uuid, "method": "set_subject", "user_id": user_id, "perimeter_id": perimeter_id},
                    args=request.json)

    @check_auth
    def delete(self, uuid=None, perimeter_id=None, user_id=None):
        """Delete a subject for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the subject
        :param user_id: user ID who do the request
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "description of the subject",
                    "password": "password for the subject",
                    "email": "email address of the subject"
            }
        }
        :internal_api: delete_subject
        """
        return call("security_router", ctx={"id": uuid, "method": "delete_subject", "user_id": user_id}, args={"perimeter_id": perimeter_id})


class Objects(Resource):
    """
    Endpoint for objects requests
    """

    __urls__ = (
        "/objects",
        "/objects/",
        "/objects/<string:perimeter_id>",
        "/policies/<string:uuid>/objects",
        "/policies/<string:uuid>/objects/",
        "/policies/<string:uuid>/objects/<string:perimeter_id>",
    )

    @check_auth
    def get(self, uuid=None, perimeter_id=None, user_id=None):
        """Retrieve all objects or a specific one if perimeter_id is given for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object
        :param user_id: user ID who do the request
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object"
            }
        }
        :internal_api: get_objects
        """
        return call("security_router", ctx={"id": uuid, "method": "get_objects", "user_id": user_id}, args={"perimeter_id": perimeter_id})

    @check_auth
    def post(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a object.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "object_name": "name of the object",
            "object_description": "description of the object"
        }
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object"
            }
        }
        :internal_api: set_object
        """
        return call("security_router", ctx={"id": uuid, "method": "set_object", "user_id": user_id, "perimeter_id": None},
                    args=request.json)

    @check_auth
    def patch(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a object.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "object_name": "name of the object",
            "object_description": "description of the object"
        }
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object"
            }
        }
        :internal_api: set_object
        """
        return call("security_router", ctx={"id": uuid, "method": "set_object", "user_id": user_id, "perimeter_id": perimeter_id},
                    args=request.json)

    @check_auth
    def delete(self, uuid=None, perimeter_id=None, user_id=None):
        """Delete a object for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object
        :param user_id: user ID who do the request
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object"
            }
        }
        :internal_api: delete_object
        """
        return call("security_router", ctx={"id": uuid, "method": "delete_object", "user_id": user_id}, args={"perimeter_id": perimeter_id})


class Actions(Resource):
    """
    Endpoint for actions requests
    """

    __urls__ = (
        "/actions",
        "/actions/",
        "/actions/<string:perimeter_id>",
        "/policies/<string:uuid>/actions",
        "/policies/<string:uuid>/actions/",
        "/policies/<string:uuid>/actions/<string:perimeter_id>",
    )

    @check_auth
    def get(self, uuid=None, perimeter_id=None, user_id=None):
        """Retrieve all actions or a specific one if perimeter_id is given for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action
        :param user_id: user ID who do the request
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action"
            }
        }
        :internal_api: get_actions
        """
        return call("security_router", ctx={"id": uuid, "method": "get_actions", "user_id": user_id}, args={"perimeter_id": perimeter_id})

    @check_auth
    def post(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a action.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the action",
            "description": "description of the action"
        }
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action"
            }
        }
        :internal_api: set_action
        """
        return call("security_router", ctx={"id": uuid, "method": "set_action", "user_id": user_id, "perimeter_id": None},
                    args=request.json)

    @check_auth
    def patch(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a action.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the action",
            "description": "description of the action"
        }
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action"
            }
        }
        :internal_api: set_action
        """
        return call("security_router", ctx={"id": uuid, "method": "set_action", "user_id": user_id, "perimeter_id": perimeter_id},
                    args=request.json)

    @check_auth
    def delete(self, uuid=None, perimeter_id=None, user_id=None):
        """Delete a action for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action
        :param user_id: user ID who do the request
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action"
            }
        }
        :internal_api: delete_action
        """
        return call("security_router", ctx={"id": uuid, "method": "delete_action", "user_id": user_id}, args={"perimeter_id": perimeter_id})
