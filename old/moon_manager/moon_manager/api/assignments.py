# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Assignments allow to connect data with elements of perimeter

"""
import flask
from flask import request
from flask_restful import Resource
import logging
import requests
from python_moonutilities.security_functions import check_auth
from python_moondb.core import PolicyManager
from python_moonutilities.security_functions import validate_input

__version__ = "4.3.2"

logger = logging.getLogger("moon.manager.api." + __name__)


def invalidate_data_in_slaves(
        policy_id,
        perimeter_id,
        category_id,
        data_id):
    slaves = requests.get("http://{}/slaves".format(request.host)).json().get("slaves")
    for slave in slaves:
        if not slave.get("configured", False):
            continue
        try:
            update = requests.put("http://{}:{}/update".format(
                slave.get("wrapper_name"), slave.get("internal_port")),
                data={
                    "policy_id": policy_id,
                    "perimeter_id": perimeter_id,
                    "category_id": category_id,
                    "data_id": data_id
                },
                timeout=1
            )
            logger.info("result {} {}:{} = {}".format(
                update.status_code,
                slave.get("wrapper_name"),
                slave.get("internal_port"),
                update.text))
        except requests.exceptions.ConnectionError:
            logger.warning("Cannot reach {}:{}".format(slave.get("wrapper_name"), slave.get("port")))


class SubjectAssignments(Resource):
    """
    Endpoint for subject assignment requests
    """

    __urls__ = (
        "/policies/<string:uuid>/subject_assignments",
        "/policies/<string:uuid>/subject_assignments/",
        "/policies/<string:uuid>/subject_assignments/<string:perimeter_id>",
        "/policies/<string:uuid>/subject_assignments/<string:perimeter_id>/<string:category_id>",
        "/policies/<string:uuid>/subject_assignments/<string:perimeter_id>/<string:category_id>/<string:data_id>",
    )

    @validate_input("get", kwargs_state=[True, False, False, False, False])
    @check_auth
    def get(self, uuid=None, perimeter_id=None, category_id=None,
            data_id=None, user_id=None):
        """Retrieve all subject assignments or a specific one for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the subject
        :param category_id: uuid of the subject category
        :param data_id: uuid of the subject scope (not used here)
        :param user_id: user ID who do the request
        :return: {
            "subject_data_id": {
                "policy_id": "ID of the policy",
                "subject_id": "ID of the subject",
                "category_id": "ID of the category",
                "assignments": "Assignments list (list of data_id)",
            }
        }
        :internal_api: get_subject_assignments
        """

        data = PolicyManager.get_subject_assignments(
            user_id=user_id, policy_id=uuid,
            subject_id=perimeter_id, category_id=category_id)

        return {"subject_assignments": data}

    @validate_input("post", kwargs_state=[True, False, False, False, False],
                    body_state={"id": True, "category_id": True, "data_id": True})
    @check_auth
    def post(self, uuid=None, perimeter_id=None, category_id=None,
             data_id=None, user_id=None):
        """Create a subject assignment.

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the subject (not used here)
        :param category_id: uuid of the subject category (not used here)
        :param data_id: uuid of the subject scope (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "id": "UUID of the subject (mandatory)",
            "category_id": "UUID of the category (mandatory)"
            "data_id": "UUID of the scope (mandatory)"
        }
        :return: {
            "subject_data_id": {
                "policy_id": "ID of the policy",
                "subject_id": "ID of the subject (mandatory)",
                "category_id": "ID of the category (mandatory)",
                "assignments": "Assignments list (list of data_id)",
            }
        }
        :internal_api: update_subject_assignment
        """
        data_id = request.json.get("data_id")
        category_id = request.json.get("category_id")
        perimeter_id = request.json.get("id")
        data = PolicyManager.add_subject_assignment(
            user_id=user_id, policy_id=uuid,
            subject_id=perimeter_id, category_id=category_id,
            data_id=data_id)
        invalidate_data_in_slaves(
            policy_id=uuid,
            perimeter_id=perimeter_id,
            category_id=category_id,
            data_id=data_id)

        return {"subject_assignments": data}

    @validate_input("delete", kwargs_state=[True, True, True, True, False])
    @check_auth
    def delete(self, uuid=None, perimeter_id=None, category_id=None,
               data_id=None, user_id=None):
        """Delete a subject assignment for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the subject
        :param category_id: uuid of the subject category
        :param data_id: uuid of the subject scope
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_subject_assignment
        """

        data = PolicyManager.delete_subject_assignment(
            user_id=user_id, policy_id=uuid,
            subject_id=perimeter_id, category_id=category_id,
            data_id=data_id)
        invalidate_data_in_slaves(
            policy_id=uuid,
            perimeter_id=perimeter_id,
            category_id=category_id,
            data_id=data_id)

        return {"result": True}


class ObjectAssignments(Resource):
    """
    Endpoint for object assignment requests
    """

    __urls__ = (
        "/policies/<string:uuid>/object_assignments",
        "/policies/<string:uuid>/object_assignments/",
        "/policies/<string:uuid>/object_assignments/<string:perimeter_id>",
        "/policies/<string:uuid>/object_assignments/<string:perimeter_id>/<string:category_id>",
        "/policies/<string:uuid>/object_assignments/<string:perimeter_id>/<string:category_id>/<string:data_id>",
    )

    @validate_input("get", kwargs_state=[True, False, False, False, False])
    @check_auth
    def get(self, uuid=None, perimeter_id=None, category_id=None,
            data_id=None, user_id=None):
        """Retrieve all object assignment or a specific one for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object
        :param category_id: uuid of the object category
        :param data_id: uuid of the object scope (not used here)
        :param user_id: user ID who do the request
        :return: {
            "object_data_id": {
                "policy_id": "ID of the policy",
                "object_id": "ID of the object",
                "category_id": "ID of the category",
                "assignments": "Assignments list (list of data_id)",
            }
        }
        :internal_api: get_object_assignments
        """

        data = PolicyManager.get_object_assignments(
            user_id=user_id, policy_id=uuid,
            object_id=perimeter_id, category_id=category_id)

        return {"object_assignments": data}

    @validate_input("post", kwargs_state=[True, False, False, False, False],
                    body_state={"id": True, "category_id": True, "data_id": True})
    @check_auth
    def post(self, uuid=None, perimeter_id=None, category_id=None,
             data_id=None, user_id=None):
        """Create an object assignment.

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object (not used here)
        :param category_id: uuid of the object category (not used here)
        :param data_id: uuid of the object scope (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "id": "UUID of the action (mandatory)",
            "category_id": "UUID of the category (mandatory)",
            "data_id": "UUID of the scope (mandatory)"
        }
        :return: {
            "object_data_id": {
                "policy_id": "ID of the policy",
                "object_id": "ID of the object",
                "category_id": "ID of the category",
                "assignments": "Assignments list (list of data_id)",
            }
        }
        :internal_api: update_object_assignment
        """

        data_id = request.json.get("data_id")
        category_id = request.json.get("category_id")
        perimeter_id = request.json.get("id")
        data = PolicyManager.add_object_assignment(
            user_id=user_id, policy_id=uuid,
            object_id=perimeter_id, category_id=category_id,
            data_id=data_id)
        invalidate_data_in_slaves(
            policy_id=uuid,
            perimeter_id=perimeter_id,
            category_id=category_id,
            data_id=data_id)

        return {"object_assignments": data}

    @validate_input("delete", kwargs_state=[True, True, True, True, False])
    @check_auth
    def delete(self, uuid=None, perimeter_id=None, category_id=None,
               data_id=None, user_id=None):
        """Delete a object assignment for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object
        :param category_id: uuid of the object category
        :param data_id: uuid of the object scope
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_object_assignment
        """
        data = PolicyManager.delete_object_assignment(
            user_id=user_id, policy_id=uuid,
            object_id=perimeter_id, category_id=category_id,
            data_id=data_id)
        invalidate_data_in_slaves(
            policy_id=uuid,
            perimeter_id=perimeter_id,
            category_id=category_id,
            data_id=data_id)

        return {"result": True}


class ActionAssignments(Resource):
    """
    Endpoint for action assignment requests
    """

    __urls__ = (
        "/policies/<string:uuid>/action_assignments",
        "/policies/<string:uuid>/action_assignments/",
        "/policies/<string:uuid>/action_assignments/<string:perimeter_id>",
        "/policies/<string:uuid>/action_assignments/<string:perimeter_id>/<string:category_id>",
        "/policies/<string:uuid>/action_assignments/<string:perimeter_id>/<string:category_id>/<string:data_id>",
    )

    @validate_input("get", kwargs_state=[True, False, False, False, False])
    @check_auth
    def get(self, uuid=None, perimeter_id=None, category_id=None,
            data_id=None, user_id=None):
        """Retrieve all action assignment or a specific one for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action
        :param category_id: uuid of the action category
        :param data_id: uuid of the action scope
        :param user_id: user ID who do the request
        :return: {
            "action_data_id": {
                "policy_id": "ID of the policy",
                "object_id": "ID of the action",
                "category_id": "ID of the category",
                "assignments": "Assignments list (list of data_id)",
            }
        }
        :internal_api: get_action_assignments
        """
        data = PolicyManager.get_action_assignments(
            user_id=user_id, policy_id=uuid,
            action_id=perimeter_id, category_id=category_id)

        return {"action_assignments": data}

    @validate_input("post", kwargs_state=[True, False, False, False, False],
                    body_state={"id": True, "category_id": True, "data_id": True})
    @check_auth
    def post(self, uuid=None, perimeter_id=None, category_id=None,
             data_id=None, user_id=None):
        """Create an action assignment.

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action (not used here)
        :param category_id: uuid of the action category (not used here)
        :param data_id: uuid of the action scope (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "id": "UUID of the action (mandatory)",
            "category_id": "UUID of the category (mandatory)",
            "data_id": "UUID of the scope (mandatory)"
        }
        :return: {
            "action_data_id": {
                "policy_id": "ID of the policy",
                "object_id": "ID of the action",
                "category_id": "ID of the category",
                "assignments": "Assignments list (list of data_id)",
            }
        }
        :internal_api: update_action_assignment
        """

        data_id = request.json.get("data_id")
        category_id = request.json.get("category_id")
        perimeter_id = request.json.get("id")
        data = PolicyManager.add_action_assignment(
            user_id=user_id, policy_id=uuid,
            action_id=perimeter_id, category_id=category_id,
            data_id=data_id)
        invalidate_data_in_slaves(
            policy_id=uuid,
            perimeter_id=perimeter_id,
            category_id=category_id,
            data_id=data_id)

        return {"action_assignments": data}

    @validate_input("delete", kwargs_state=[True, True, True, True, False])
    @check_auth
    def delete(self, uuid=None, perimeter_id=None, category_id=None,
               data_id=None, user_id=None):
        """Delete a action assignment for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action
        :param category_id: uuid of the action category
        :param data_id: uuid of the action scope
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_action_assignment
        """

        data = PolicyManager.delete_action_assignment(
            user_id=user_id, policy_id=uuid,
            action_id=perimeter_id, category_id=category_id,
            data_id=data_id)
        invalidate_data_in_slaves(
            policy_id=uuid,
            perimeter_id=perimeter_id,
            category_id=category_id,
            data_id=data_id)

        return {"result": True}
