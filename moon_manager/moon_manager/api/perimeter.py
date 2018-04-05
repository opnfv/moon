# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
* Subjects are the source of an action on an object
  (examples : users, virtual machines)
* Objects are the destination of an action
  (examples virtual machines, virtual Routers)
* Actions are what subject wants to do on an object
"""

from flask import request
from flask_restful import Resource
import logging
from python_moonutilities.security_functions import check_auth
from python_moondb.core import PolicyManager
from python_moonutilities.security_functions import validate_input


__version__ = "4.3.2"

logger = logging.getLogger("moon.manager.api." + __name__)


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

    @validate_input("get", kwargs_state=[False, False, False])
    @check_auth
    def get(self, uuid=None, perimeter_id=None, user_id=None):
        """Retrieve all subjects or a specific one if perimeter_id is
        given for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the subject
        :param user_id: user ID who do the request
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "a description (optional)"
            }
        }
        :internal_api: get_subjects
        """
        try:
            data = PolicyManager.get_subjects(
                user_id=user_id,
                policy_id=uuid,
                perimeter_id=perimeter_id
            )
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"subjects": data}

    @validate_input("post", body_state=[True, False, False, False])
    @check_auth
    def post(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a subject.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the subject",
            "description": "description of the subject (optional)",
            "password": "password for the subject (optional)",
            "email": "email address of the subject (optional)"
        }
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "description of the subject (optional)",
                    "password": "password for the subject (optional)",
                    "email": "email address of the subject (optional)"
            }
        }
        :internal_api: set_subject
        """
        try:
            if not perimeter_id:
                data = PolicyManager.get_subjects(user_id=user_id,
                                                  policy_id=None)
                if 'name' in request.json:
                    for data_id, data_value in data.items():
                        if data_value['name'] == request.json['name']:
                            perimeter_id = data_id
                            break
            data = PolicyManager.add_subject(
                user_id=user_id, policy_id=uuid,
                perimeter_id=perimeter_id, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"subjects": data}

    @validate_input("patch", kwargs_state=[False, True, False], body_state=[True, False, False, False])
    @check_auth
    def patch(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a subject.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the subject",
            "description": "description of the subject (optional)",
            "password": "password for the subject (optional)",
            "email": "email address of the subject (optional)"
        }
        :return: {
                "subject_id": {
                    "name": "name of the subject",
                    "keystone_id": "keystone id of the subject",
                    "description": "description of the subject (optional)",
                    "password": "password for the subject (optional)",
                    "email": "email address of the subject (optional)"
            }
        }
        :internal_api: set_subject
        """
        try:
            if not perimeter_id:
                data = PolicyManager.get_subjects(user_id=user_id,
                                                  policy_id=None)
                if 'name' in request.json:
                    for data_id, data_value in data.items():
                        if data_value['name'] == request.json['name']:
                            perimeter_id = data_id
                            break
            data = PolicyManager.add_subject(
                user_id=user_id, policy_id=uuid,
                perimeter_id=perimeter_id, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"subjects": data}

    @validate_input("delete", kwargs_state=[False, True, False])
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
                    "description": "description of the subject (optional)",
                    "password": "password for the subject (optional)",
                    "email": "email address of the subject (optional)"
            }
        }
        :internal_api: delete_subject
        """
        try:
            data = PolicyManager.delete_subject(
                user_id=user_id, policy_id=uuid, perimeter_id=perimeter_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"result": True}


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

    @validate_input("get", kwargs_state=[False, False, False])
    @check_auth
    def get(self, uuid=None, perimeter_id=None, user_id=None):
        """Retrieve all objects or a specific one if perimeter_id is
        given for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object
        :param user_id: user ID who do the request
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object (optional)"
            }
        }
        :internal_api: get_objects
        """
        try:
            data = PolicyManager.get_objects(
                user_id=user_id,
                policy_id=uuid,
                perimeter_id=perimeter_id
            )
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"objects": data}

    @validate_input("post", body_state=[True, False, False, False])
    @check_auth
    def post(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a object.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "object_name": "name of the object",
            "object_description": "description of the object (optional)"
        }
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object (optional)"
            }
        }
        :internal_api: set_object
        """
        try:
            data = PolicyManager.get_objects(user_id=user_id, policy_id=None)
            if 'name' in request.json:
                for data_id, data_value in data.items():
                    if data_value['name'] == request.json['name']:
                        perimeter_id = data_id
                        break
            data = PolicyManager.add_object(
                user_id=user_id, policy_id=uuid,
                perimeter_id=perimeter_id, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"objects": data}

    @validate_input("patch", kwargs_state=[False, True, False], body_state=[True, False, False, False])
    @check_auth
    def patch(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a object.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "object_name": "name of the object",
            "object_description": "description of the object (optional)"
        }
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object (optional)"
            }
        }
        :internal_api: set_object
        """
        try:
            data = PolicyManager.get_objects(user_id=user_id, policy_id=None)
            if 'name' in request.json:
                for data_id, data_value in data.items():
                    if data_value['name'] == request.json['name']:
                        perimeter_id = data_id
                        break
            data = PolicyManager.add_object(
                user_id=user_id, policy_id=uuid,
                perimeter_id=perimeter_id, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"objects": data}

    @validate_input("delete", kwargs_state=[False, True, False])
    @check_auth
    def delete(self, uuid=None, perimeter_id=None, user_id=None):
        """Delete a object for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object
        :param user_id: user ID who do the request
        :return: {
                "object_id": {
                    "name": "name of the object",
                    "description": "description of the object (optional)"
            }
        }
        :internal_api: delete_object
        """
        try:
            data = PolicyManager.delete_object(
                user_id=user_id, policy_id=uuid, perimeter_id=perimeter_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"result": True}


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

    @validate_input("get", kwargs_state=[False, False, False])
    @check_auth
    def get(self, uuid=None, perimeter_id=None, user_id=None):
        """Retrieve all actions or a specific one if perimeter_id
        is given for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action
        :param user_id: user ID who do the request
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action (optional)"
            }
        }
        :internal_api: get_actions
        """
        try:
            data = PolicyManager.get_actions(
                user_id=user_id, policy_id=uuid, perimeter_id=perimeter_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"actions": data}

    @validate_input("post", body_state=[True, False, False, False])
    @check_auth
    def post(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a action.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the action",
            "description": "description of the action (optional)"
        }
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action (optional)"
            }
        }
        :internal_api: set_action
        """
        try:
            data = PolicyManager.get_actions(user_id=user_id, policy_id=None)
            if 'name' in request.json:
                for data_id, data_value in data.items():
                    if data_value['name'] == request.json['name']:
                        perimeter_id = data_id
                        break
            data = PolicyManager.add_action(
                user_id=user_id, policy_id=uuid,
                perimeter_id=perimeter_id, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"actions": data}

    @validate_input("patch", kwargs_state=[False, True, False], body_state=[True, False, False, False])
    @check_auth
    def patch(self, uuid=None, perimeter_id=None, user_id=None):
        """Create or update a action.

        :param uuid: uuid of the policy
        :param perimeter_id: must not be used here
        :param user_id: user ID who do the request
        :request body: {
            "name": "name of the action",
            "description": "description of the action (optional)"
        }
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action (optional)"
            }
        }
        :internal_api: set_action
        """
        try:
            data = PolicyManager.get_actions(user_id=user_id, policy_id=None)
            if 'name' in request.json:
                for data_id, data_value in data.items():
                    if data_value['name'] == request.json['name']:
                        perimeter_id = data_id
                        break
            data = PolicyManager.add_action(
                user_id=user_id, policy_id=uuid,
                perimeter_id=perimeter_id, value=request.json)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"actions": data}

    @validate_input("delete", kwargs_state=[False, True, False])
    @check_auth
    def delete(self, uuid=None, perimeter_id=None, user_id=None):
        """Delete a action for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action
        :param user_id: user ID who do the request
        :return: {
                "action_id": {
                    "name": "name of the action",
                    "description": "description of the action (optional)"
            }
        }
        :internal_api: delete_action
        """
        try:
            data = PolicyManager.delete_action(
                user_id=user_id, policy_id=uuid, perimeter_id=perimeter_id)
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"result": True}
