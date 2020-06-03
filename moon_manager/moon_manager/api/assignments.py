# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Assignments allow to connect data with elements of perimeter

"""
import hug
import logging
import requests
from moon_manager import db_driver as driver
from moon_utilities.security_functions import validate_input
from moon_manager.api import slave as slave_class
from moon_manager.api import configuration
from moon_manager.api import policy
from moon_manager.api import perimeter
from moon_manager.api import meta_data
from moon_manager.api import data
from moon_utilities.auth_functions import api_key_authentication, connect_from_env
from moon_utilities.invalided_functions import invalidate_assignment_in_slaves

# from moon_manager.server import handle_exception, handle_custom_exceptions

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class SubjectAssignments(object):
    """
    Endpoint for subject assignment requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/policies/{uuid}/subject_assignments", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/subject_assignments/{perimeter_id}",
             requires=api_key_authentication)
    @hug.get("/policies/{uuid}/subject_assignments/{perimeter_id}/{category_id}",
             requires=api_key_authentication)
    def get(uuid: hug.types.text, perimeter_id: hug.types.text = None,
            category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Retrieve all subject assignments or a specific one for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the subject
        :param category_id: uuid of the subject category
        :param authed_user: user ID who do the request
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

        data = driver.PolicyManager.get_subject_assignments(
            moon_user_id=authed_user, policy_id=uuid,
            subject_id=perimeter_id, category_id=category_id)

        return {"subject_assignments": data}

    @staticmethod
    @hug.local()
    @hug.post("/policies/{uuid}/subject_assignments", requires=api_key_authentication)
    def post(body: validate_input("id", "category_id", "data_id"), uuid: hug.types.text,
             authed_user: hug.directives.user = None):
        """Create a subject assignment.

        :param body: body of the request
        :param uuid: uuid of the policy
        :param authed_user: user ID who do the request
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
        data_id = body.get("data_id")
        category_id = body.get("category_id")
        perimeter_id = body.get("id")

        data = driver.PolicyManager.add_subject_assignment(
            moon_user_id=authed_user, policy_id=uuid,
            subject_id=perimeter_id, category_id=category_id, data_id=data_id)

        return {"subject_assignments": data}

    @staticmethod
    @hug.local()
    @hug.delete("/policies/{uuid}/subject_assignments", requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/subject_assignments/{perimeter_id}",
                requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/subject_assignments/{perimeter_id}/{category_id}",
                requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/subject_assignments/{perimeter_id}/{category_id}/{data_id}",
                requires=api_key_authentication)
    def delete(uuid: hug.types.text, perimeter_id: hug.types.text = None,
               category_id: hug.types.text = None, data_id: hug.types.text = None,
               authed_user: hug.directives.user = None):
        """Delete a subject assignment for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the subject
        :param category_id: uuid of the subject category
        :param data_id: uuid of the subject scope
        :param authed_user: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_subject_assignment
        """

        driver.PolicyManager.delete_subject_assignment(
            moon_user_id=authed_user, policy_id=uuid,
            subject_id=perimeter_id, category_id=category_id,
            data_id=data_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_assignment_in_slaves(slaves=slaves, policy_id=uuid, perimeter_id=perimeter_id,
                                        category_id=category_id, data_id=data_id, type="subject")
        return {"result": True}


class ObjectAssignments(object):
    """
    Endpoint for object assignment requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/policies/{uuid}/object_assignments", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/object_assignments/{perimeter_id}", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/object_assignments/{perimeter_id}/{category_id}",
             requires=api_key_authentication)
    def get(uuid: hug.types.text, perimeter_id: hug.types.text = None,
            category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Retrieve all object assignment or a specific one for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object
        :param category_id: uuid of the object category
        :param authed_user: user ID who do the request
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

        data = driver.PolicyManager.get_object_assignments(
            moon_user_id=authed_user, policy_id=uuid,
            object_id=perimeter_id, category_id=category_id)

        return {"object_assignments": data}

    @staticmethod
    @hug.local()
    @hug.post("/policies/{uuid}/object_assignments", requires=api_key_authentication)
    def post(body: validate_input("id", "category_id", "data_id"), uuid,
             authed_user: hug.directives.user = None):
        """Create an object assignment.

        :param body: body of the request
        :param uuid: uuid of the policy
        :param authed_user: user ID who do the request
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

        data_id = body.get("data_id")
        category_id = body.get("category_id")
        perimeter_id = body.get("id")
        data = driver.PolicyManager.add_object_assignment(moon_user_id=authed_user, policy_id=uuid,
                                                          object_id=perimeter_id,
                                                          category_id=category_id, data_id=data_id)

        return {"object_assignments": data}

    @staticmethod
    @hug.local()
    @hug.delete("/policies/{uuid}/object_assignments", requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/object_assignments/{perimeter_id}",
                requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/object_assignments/{perimeter_id}/{category_id}",
                requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/object_assignments/{perimeter_id}/{category_id}/{data_id}",
                requires=api_key_authentication)
    def delete(uuid: hug.types.text, perimeter_id: hug.types.text = None,
               category_id: hug.types.text = None, data_id: hug.types.text = None,
               authed_user: hug.directives.user = None):
        """Delete a object assignment for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the object
        :param category_id: uuid of the object category
        :param data_id: uuid of the object scope
        :param authed_user: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_object_assignment
        """
        driver.PolicyManager.delete_object_assignment(
            moon_user_id=authed_user, policy_id=uuid, object_id=perimeter_id,
            category_id=category_id, data_id=data_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_assignment_in_slaves(slaves=slaves, policy_id=uuid, perimeter_id=perimeter_id,
                                        category_id=category_id, data_id=data_id, type="object")

        return {"result": True}


class ActionAssignments(object):
    """
    Endpoint for action assignment requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/policies/{uuid}/action_assignments", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/action_assignments/{perimeter_id}", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/action_assignments/{perimeter_id}/{category_id}",
             requires=api_key_authentication)
    def get(uuid: hug.types.text, perimeter_id: hug.types.text = None,
            category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Retrieve all action assignment or a specific one for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action
        :param category_id: uuid of the action category
        :param authed_user: user ID who do the request
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
        data = driver.PolicyManager.get_action_assignments(
            moon_user_id=authed_user, policy_id=uuid,
            action_id=perimeter_id, category_id=category_id)

        return {"action_assignments": data}

    @staticmethod
    @hug.local()
    @hug.post("/policies/{uuid}/action_assignments", requires=api_key_authentication)
    def post(body: validate_input("id", "category_id", "data_id"), uuid,
             authed_user: hug.directives.user = None):
        """Create an action assignment.

        :param body: body of the request
        :param uuid: uuid of the policy
        :param authed_user: user ID who do the request
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

        data_id = body.get("data_id")
        category_id = body.get("category_id")
        perimeter_id = body.get("id")
        data = driver.PolicyManager.add_action_assignment(
            moon_user_id=authed_user, policy_id=uuid,
            action_id=perimeter_id, category_id=category_id, data_id=data_id)

        return {"action_assignments": data}

    @staticmethod
    @hug.local()
    @hug.delete("/policies/{uuid}/action_assignments", requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/action_assignments/{perimeter_id}",
                requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/action_assignments/{perimeter_id}/{category_id}",
                requires=api_key_authentication)
    @hug.delete("/policies/{uuid}/action_assignments/{perimeter_id}/{category_id}/{data_id}",
                requires=api_key_authentication)
    def delete(uuid: hug.types.text, perimeter_id: hug.types.text = None,
               category_id: hug.types.text = None, data_id: hug.types.text = None,
               authed_user: hug.directives.user = None):
        """Delete a action assignment for a given policy

        :param uuid: uuid of the policy
        :param perimeter_id: uuid of the action
        :param category_id: uuid of the action category
        :param data_id: uuid of the action scope
        :param authed_user: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_action_assignment
        """

        driver.PolicyManager.delete_action_assignment(
            moon_user_id=authed_user, policy_id=uuid,
            action_id=perimeter_id, category_id=category_id, data_id=data_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_assignment_in_slaves(slaves=slaves, policy_id=uuid, perimeter_id=perimeter_id,
                                        category_id=category_id, data_id=data_id, type="action")

        return {"result": True}


SubjectAssignmentsAPI = hug.API(name='subject_assignments', doc=SubjectAssignments.__doc__)
ObjectAssignmentsAPI = hug.API(name='object_assignments', doc=ObjectAssignments.__doc__)
ActionAssignmentsAPI = hug.API(name='action_assignments', doc=ActionAssignments.__doc__)


@hug.object(name='subjects', version='1.0.0', api=SubjectAssignmentsAPI)
class SubjectAssignmentsCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(policy_name_or_id, name_or_id="", human: bool = False):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _assignments_req = requests.get("{}/policies/{}/subject_assignments".format(
                                            db_conf.get("url"), policy_id),
                                        headers={"x-api-key": manager_api_key}
                                        )
        _assignment_key = None
        if _assignments_req.status_code == 200:
            _subject_assignments = _assignments_req.json().get("subject_assignments")
            if name_or_id:
                _assignments = None
                if name_or_id in _subject_assignments:
                    _assignments = _subject_assignments.get(name_or_id)
                    _assignment_key = name_or_id
                else:
                    for _key in _subject_assignments:
                        try:
                            _subject = perimeter.SubjectsCLI.list(name_or_id).get("subjects")[0]
                            _subject_key = list(_subject.keys())[0]
                        except Exception as e:
                            # FIXME: should upgrade this exception
                            LOGGER.exception(e)
                            continue
                        else:
                            if _subject_assignments.get(_key).get("subject_id") == _subject_key:
                                _assignments = _subject_assignments.get(_key)
                                _assignment_key = _key
                                break
                if not _assignments:
                    raise Exception("Cannot find Subject Assignments with ID {}".format(name_or_id))
                result = {"subject_assignments": [{_assignment_key: _assignments}]}
            else:
                result = _assignments_req.json()

            if human:
                return SubjectAssignmentsCLI.human_display(result)
            else:
                return result
        LOGGER.error('Cannot list Subject Assignments {}'.format(_assignments_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id, human: bool = False):
        """
        Add subject assignment in database
        :return: JSON status output
        """
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        perimeter_id = list(perimeter.SubjectsCLI.list(perimeter_name_or_id).get("subjects")[0].keys())[0]
        category_id = list(meta_data.SubjectCategoriesCLI.list(category_name_or_id).get("subject_categories").keys())[0]
        data_id = data.SubjectDataCLI.list(policy_id, data_name_or_id).get("subject_data").get("id")
        _url = "{}/policies/{}/subject_assignments".format(db_conf.get("url"), policy_id)

        _assignments = requests.post(
            _url,
            json={
                "id": perimeter_id,
                "category_id": category_id,
                "data_id": data_id,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _assignments.status_code == 200:
            LOGGER.warning('Create {}'.format(_assignments.content))
            if human:
                return SubjectAssignmentsCLI.human_display(_assignments.json())
            else:
                return _assignments.json()
        LOGGER.error('Cannot create assignment for {}/{}/{} ({})'.format(
            perimeter_name_or_id, category_name_or_id, data_name_or_id, _assignments.content[:40]))
        LOGGER.error("{}/{}/{}".format(perimeter_id, category_id, data_id))

    @staticmethod
    @hug.object.cli
    def delete(policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        perimeter_id = list(perimeter.SubjectsCLI.list(perimeter_name_or_id).get("subjects")[0].keys())[0]
        category_id = list(meta_data.SubjectCategoriesCLI.list(category_name_or_id).get("subject_categories").keys())[0]
        data_id = data.SubjectDataCLI.list(policy_id, data_name_or_id).get("subject_data").get("id")
        _url = "{}/policies/{}/subject_assignments/{}/{}/{}".format(
            db_conf.get("url"),
            policy_id,
            perimeter_id,
            category_id,
            data_id)
        req = requests.delete(
            _url,
            headers={"x-api-key": manager_api_key}
        )
        if req.status_code == 200:
            LOGGER.warning('Deleted {}-{}-{}-{}'.format(
                policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id))
            return True
        LOGGER.error("Cannot delete Assignment with {}-{}-{}-{}".format(
            policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id
        ))
        return False

    @staticmethod
    def human_display(subject_assigment_json):
        human_result = "Subject Assignments"
        for subject_assignment in subject_assigment_json.get("subject_assignments"):
            human_result += "\n" + subject_assigment_json.get("subject_assignments").get(subject_assignment).get("id") + "\n"
            human_result += "\tid : " + subject_assigment_json.get("subject_assignments").get(subject_assignment).get("id") + "\n"
            human_result += "\tpolicy_id : " + subject_assigment_json.get("subject_assignments").get(subject_assignment).get("policy_id") + "\n"
            human_result += "\tsubject_id : " + subject_assigment_json.get("subject_assignments").get(subject_assignment).get("subject_id") + "\n"
            human_result += "\tcategory_id : " + subject_assigment_json.get("subject_assignments").get(subject_assignment).get("category_id") + "\n"
            human_result += "\tassignments : \n"
            for assignment in subject_assigment_json.get("subject_assignments").get(subject_assignment).get("assignments"):
                human_result += "\t\t" + assignment + "\n"
        return human_result


@hug.object(name='objects', version='1.0.0', api=ObjectAssignmentsAPI)
class ObjectAssignmentsCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(policy_name_or_id, name_or_id="", human: bool = False):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _assignments_req = requests.get("{}/policies/{}/object_assignments".format(
                                            db_conf.get("url"), policy_id),
                                        headers={"x-api-key": manager_api_key}
                                        )
        _assignment_key = None
        if _assignments_req.status_code == 200:
            _object_assignments = _assignments_req.json().get("object_assignments")
            if name_or_id:
                _assignments = None
                if name_or_id in _object_assignments:
                    _assignments = _object_assignments.get(name_or_id)
                    _assignment_key = name_or_id
                else:
                    for _key in _object_assignments:
                        try:
                            _object = perimeter.ObjectsCLI.list(name_or_id).get("objects")[0]
                            _object_key = list(_object.keys())[0]
                        except Exception as e:
                            # FIXME: should upgrade this exception
                            LOGGER.exception(e)
                            continue
                        else:
                            if _object_assignments.get(_key).get("object_id") == _object_key:
                                _assignments = _object_assignments.get(_key)
                                _assignment_key = _key
                                break
                if not _assignments:
                    raise Exception("Cannot find Object Assignments with ID {}".format(name_or_id))
                result = {"object_assignments": [{_assignment_key: _assignments}]}
            else:
                result = _assignments_req.json()

            if human:
                return ObjectAssignmentsCLI.human_display(result)
            else:
                return result
        LOGGER.error('Cannot list Object Assignments {}'.format(_assignments_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id, human: bool = False):
        """
        Add object assignment in database
        :return: JSON status output
        """
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        perimeter_id = list(perimeter.ObjectsCLI.list(perimeter_name_or_id).get("objects")[0].keys())[0]
        category_id = list(meta_data.ObjectCategoriesCLI.list(category_name_or_id).get("object_categories").keys())[0]
        data_id = data.ObjectDataCLI.list(policy_id, data_name_or_id).get("object_data").get("id")
        _url = "{}/policies/{}/object_assignments".format(db_conf.get("url"), policy_id)

        _assignments = requests.post(
            _url,
            json={
                "id": perimeter_id,
                "category_id": category_id,
                "data_id": data_id,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _assignments.status_code == 200:
            LOGGER.warning('Create {}'.format(_assignments.content))
            if human:
                return ObjectAssignmentsCLI.human_display(_assignments.json())
            else:
                return _assignments.json()
        LOGGER.error('Cannot create assignment for {}/{}/{} ({})'.format(
            perimeter_name_or_id, category_name_or_id, data_name_or_id, _assignments.content[:40]))
        LOGGER.error("{}/{}/{}".format(perimeter_id, category_id, data_id))

    @staticmethod
    @hug.object.cli
    def delete(policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        perimeter_id = list(perimeter.ObjectsCLI.list(perimeter_name_or_id).get("objects")[0].keys())[0]
        category_id = list(meta_data.ObjectCategoriesCLI.list(category_name_or_id).get("object_categories").keys())[0]
        data_id = data.ObjectDataCLI.list(policy_id, data_name_or_id).get("object_data").get("id")
        _url = "{}/policies/{}/object_assignments/{}/{}/{}".format(
            db_conf.get("url"),
            policy_id,
            perimeter_id,
            category_id,
            data_id)
        req = requests.delete(
            _url,
            headers={"x-api-key": manager_api_key}
        )
        if req.status_code == 200:
            LOGGER.warning('Deleted {}-{}-{}-{}'.format(
                policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id))
            return True
        LOGGER.error("Cannot delete Assignment with {}-{}-{}-{}".format(
            policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id
        ))
        return False

    @staticmethod
    def human_display(object_assigment_json):
        human_result = "Object Assignments"
        for object_assignment in object_assigment_json.get("object_assignments"):
            human_result += "\n" + object_assigment_json.get("object_assignments").get(object_assignment).get("id") + "\n"
            human_result += "\tid : " + object_assigment_json.get("object_assignments").get(object_assignment).get("id") + "\n"
            human_result += "\tpolicy_id : " + object_assigment_json.get("object_assignments").get(object_assignment).get("policy_id") + "\n"
            human_result += "\tobject_id : " + object_assigment_json.get("object_assignments").get(object_assignment).get("object_id") + "\n"
            human_result += "\tcategory_id : " + object_assigment_json.get("object_assignments").get(object_assignment).get("category_id") + "\n"
            human_result += "\tassignments : \n"
            for assignment in object_assigment_json.get("object_assignments").get(object_assignment).get("assignments"):
                human_result += "\t\t" + assignment + "\n"
        return human_result


@hug.object(name='actions', version='1.0.0', api=ActionAssignmentsAPI)
class ActionAssignmentsCLI(object):
    """An example of command like calls via an Action"""

    @staticmethod
    @hug.object.cli
    def list(policy_name_or_id, name_or_id="", human: bool = False):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _assignments_req = requests.get("{}/policies/{}/action_assignments".format(
                                            db_conf.get("url"), policy_id),
                                        headers={"x-api-key": manager_api_key}
                                        )
        _assignment_key = None
        if _assignments_req.status_code == 200:
            _action_assignments = _assignments_req.json().get("action_assignments")
            if name_or_id:
                _assignments = None
                if name_or_id in _action_assignments:
                    _assignments = _action_assignments.get(name_or_id)
                    _assignment_key = name_or_id
                else:
                    for _key in _action_assignments:
                        try:
                            _action = perimeter.ActionsCLI.list(name_or_id).get("actions")[0]
                            _action_key = list(_action.keys())[0]
                        except Exception as e:
                            # FIXME: should upgrade this exception
                            LOGGER.exception(e)
                            continue
                        else:
                            if _action_assignments.get(_key).get("action_id") == _action_key:
                                _assignments = _action_assignments.get(_key)
                                _assignment_key = _key
                                break
                if not _assignments:
                    raise Exception("Cannot find Action Assignments with ID {}".format(name_or_id))
                result = {"action_assignments": [{_assignment_key: _assignments}]}
            else:
                result = _assignments_req.json()

            if human:
                return ActionAssignmentsCLI.human_display(result)
            else:
                return result
        LOGGER.error('Cannot list Action Assignments {}'.format(_assignments_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id, human: bool = False):
        """
        Add action assignment in database
        :return: JSON status output
        """
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        perimeter_id = list(perimeter.ActionsCLI.list(perimeter_name_or_id).get("actions")[0].keys())[0]
        category_id = list(meta_data.ActionCategoriesCLI.list(category_name_or_id).get("action_categories").keys())[0]
        data_id = data.ActionDataCLI.list(policy_id, data_name_or_id).get("action_data").get("id")
        _url = "{}/policies/{}/action_assignments".format(db_conf.get("url"), policy_id)

        _assignments = requests.post(
            _url,
            json={
                "id": perimeter_id,
                "category_id": category_id,
                "data_id": data_id,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _assignments.status_code == 200:
            LOGGER.warning('Create {}'.format(_assignments.content))
            if human:
                return ActionAssignmentsCLI.human_display(_assignments.json())
            else:
                return _assignments.json()
        LOGGER.error('Cannot create assignment for {}/{}/{} ({})'.format(
            perimeter_name_or_id, category_name_or_id, data_name_or_id, _assignments.content[:40]))
        LOGGER.error("{}/{}/{}".format(perimeter_id, category_id, data_id))

    @staticmethod
    @hug.object.cli
    def delete(policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        perimeter_id = list(perimeter.ActionsCLI.list(perimeter_name_or_id).get("actions")[0].keys())[0]
        category_id = list(meta_data.ActionCategoriesCLI.list(category_name_or_id).get("action_categories").keys())[0]
        data_id = data.ActionDataCLI.list(policy_id, data_name_or_id).get("action_data").get("id")
        _url = "{}/policies/{}/action_assignments/{}/{}/{}".format(
            db_conf.get("url"),
            policy_id,
            perimeter_id,
            category_id,
            data_id)
        req = requests.delete(
            _url,
            headers={"x-api-key": manager_api_key}
        )
        if req.status_code == 200:
            LOGGER.warning('Deleted {}-{}-{}-{}'.format(
                policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id))
            return True
        LOGGER.error("Cannot delete Assignment with {}-{}-{}-{}".format(
            policy_name_or_id, perimeter_name_or_id, category_name_or_id, data_name_or_id
        ))
        return False

    @staticmethod
    def human_display(action_assigment_json):
        human_result = "Action Assignments"
        for action_assignment in action_assigment_json.get("action_assignments"):
            human_result += "\n" + action_assigment_json.get("action_assignments").get(action_assignment).get("id") + "\n"
            human_result += "\tid : " + action_assigment_json.get("action_assignments").get(action_assignment).get("id") + "\n"
            human_result += "\tpolicy_id : " + action_assigment_json.get("action_assignments").get(action_assignment).get("policy_id") + "\n"
            human_result += "\taction_id : " + action_assigment_json.get("action_assignments").get(action_assignment).get("action_id") + "\n"
            human_result += "\tcategory_id : " + action_assigment_json.get("action_assignments").get(action_assignment).get("category_id") + "\n"
            human_result += "\tassignments : \n"
            for assignment in action_assigment_json.get("action_assignments").get(action_assignment).get("assignments"):
                human_result += "\t\t" + assignment + "\n"
        return human_result
