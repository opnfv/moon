# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""
Meta rules are skeleton for security policies

"""
import hug
import logging
import requests
from moon_manager import db_driver as driver
from moon_utilities.security_functions import validate_input
from moon_utilities.auth_functions import api_key_authentication, connect_from_env
from moon_utilities.invalided_functions import invalidate_meta_rule_in_slaves
from moon_manager.api import slave as slave_class
from moon_manager.api import configuration
from moon_manager.api import meta_data

# from moon_manager.server import handle_exception, handle_custom_exceptions

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class MetaRules(object):
    """
    Endpoint for meta rules requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/meta_rules/", requires=api_key_authentication)
    @hug.get("/meta_rules/{meta_rule_id}", requires=api_key_authentication)
    def get(meta_rule_id: hug.types.text = None, authed_user: hug.directives.user = None):
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

        data = driver.ModelManager.get_meta_rules(
            moon_user_id=authed_user, meta_rule_id=meta_rule_id)

        return {"meta_rules": data}

    @staticmethod
    @hug.local()
    @hug.post("/meta_rules/", requires=api_key_authentication)
    # @validate_input("post", body_state={"name": True, "subject_categories": False,
    #                                     "object_categories": False, "action_categories": False})
    def post(
            body: validate_input("name", "subject_categories", "object_categories",
                                 "action_categories"), authed_user: hug.directives.user = None):
        """Add a meta rule

        :param body: body of the request
        :param authed_user: user ID who do the request
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

        data = driver.ModelManager.add_meta_rule(
            moon_user_id=authed_user, meta_rule_id=None, value=body)

        return {"meta_rules": data}

    @staticmethod
    @hug.local()
    @hug.patch("/meta_rules/", requires=api_key_authentication)
    @hug.patch("/meta_rules/{meta_rule_id}", requires=api_key_authentication)
    def patch(body: validate_input("name", "subject_categories", "object_categories",
                                   "action_categories"), meta_rule_id: hug.types.text = None,
              authed_user: hug.directives.user = None):
        """Update a meta rule

        :param body: body of the request
        :param meta_rule_id: ID of the Meta Rule
        :param authed_user: user ID who do the request
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
        data = driver.ModelManager.update_meta_rule(
            moon_user_id=authed_user, meta_rule_id=meta_rule_id, value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_meta_rule_in_slaves(slaves=slaves, meta_rule_id=meta_rule_id,is_delete=False,
                                       data=data)

        return {"meta_rules": data}

    @staticmethod
    @hug.local()
    @hug.delete("/meta_rules/", requires=api_key_authentication)
    @hug.delete("/meta_rules/{meta_rule_id}", requires=api_key_authentication)
    def delete(meta_rule_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Delete a meta rule

        :param meta_rule_id: Meta rule ID
        :param authed_user: user ID who do the request
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

        driver.ModelManager.delete_meta_rule(
            moon_user_id=authed_user, meta_rule_id=meta_rule_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_meta_rule_in_slaves(slaves=slaves, meta_rule_id=meta_rule_id)

        return {"result": True}


MetaRulesAPI = hug.API(name='meta_rules', doc=MetaRules.__doc__)


@hug.object(name='meta_rules', version='1.0.0', api=MetaRulesAPI)
class MetaRulesCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id="", human: bool = False):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        _meta_rules_req = requests.get("{}/meta_rules".format(db_conf.get("url")),
                                       headers={"x-api-key": manager_api_key}
                                       )
        if _meta_rules_req.status_code == 200:
            if name_or_id:
                _meta_rules = None
                if name_or_id in _meta_rules_req.json().get("meta_rules"):
                    _meta_rules = _meta_rules_req.json().get("meta_rules").get(name_or_id)
                else:
                    for _key in _meta_rules_req.json().get("meta_rules"):
                        _name = _meta_rules_req.json().get("meta_rules").get(_key).get("name")
                        if _name == name_or_id:
                            _meta_rules = _meta_rules_req.json().get("meta_rules").get(_key)
                            name_or_id = _key
                            break
                if not _meta_rules:
                    raise Exception("Cannot find meta_rules with name or ID {}".format(
                        name_or_id))
                result = {"meta_rules": {name_or_id: _meta_rules}}
            else:
                result = _meta_rules_req.json()

            if human:
                return MetaRulesCLI.human_display(result)
            else:
                return result
        LOGGER.error('Cannot list meta_rules {}'.format(_meta_rules_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, subject_categories, object_categories, action_categories, human: bool = False):
        """
        Add a meta rule in database
        :return: JSON status output
        """
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        subject_categories_ids = []
        for cat in subject_categories.split(","):
            _cat_dict = meta_data.SubjectCategoriesCLI.list(cat).get("subject_categories")
            if cat in _cat_dict:
                subject_categories_ids.append(cat)
            else:
                subject_categories_ids.append(list(_cat_dict.keys())[0])
        object_categories_ids = []
        for cat in object_categories.split(","):
            _cat_dict = meta_data.ObjectCategoriesCLI.list(cat).get("object_categories")
            if cat in _cat_dict:
                object_categories_ids.append(cat)
            else:
                object_categories_ids.append(list(_cat_dict.keys())[0])
        action_categories_ids = []
        for cat in action_categories.split(","):
            _cat_dict = meta_data.ActionCategoriesCLI.list(cat).get("action_categories")
            if cat in _cat_dict:
                action_categories_ids.append(cat)
            else:
                action_categories_ids.append(list(_cat_dict.keys())[0])
        _url = "{}/meta_rules".format(db_conf.get("url"))
        req = requests.post(
            _url,
            json={
                "name": name,
                "subject_categories": subject_categories_ids,
                "object_categories": object_categories_ids,
                "action_categories": action_categories_ids,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if req.status_code == 200:
            LOGGER.warning('Create {}'.format(req.content))
            if human:
                return MetaRulesCLI.human_display(req.json())
            else:
                return req.json()
        LOGGER.error('Cannot create {}'.format(name, req.content[:40]))

    @staticmethod
    @hug.object.cli
    def delete(name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        _meta_rules = MetaRulesCLI.list()
        for _id, _value in _meta_rules.get("meta_rules").items():
            if _id == name_or_id or _value.get("name") == name_or_id:
                _url = "{}/meta_rules/{}".format(db_conf.get("url"), _id)
                req = requests.delete(
                    _url,
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find meta_rules with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot delete meta_rules with name {}".format(name_or_id))
        return False

    @staticmethod
    def human_display(meta_rules_json):
        human_result = "Meta Rules"
        for metarule in meta_rules_json.get("meta_rules"):
            human_result += "\n" + meta_rules_json.get("meta_rules").get(metarule).get("name") + "\n"
            human_result += "\tid : " + metarule + "\n"
            human_result += "\tname : " + meta_rules_json.get("meta_rules").get(metarule).get("name") + "\n"
            human_result += "\tdescription : " + meta_rules_json.get("meta_rules").get(metarule).get("description") + "\n"
            human_result += "\tsubject_categories :\n"
            for subject_category in meta_rules_json.get("meta_rules").get(metarule).get("subject_categories"):
                human_result += "\t\t" + subject_category + "\n"
            human_result += "\tobject_categories :\n"
            for object_category in meta_rules_json.get("meta_rules").get(metarule).get("object_categories"):
                human_result += "\t\t" + object_category + "\n"
            human_result += "\taction_categories :\n"
            for action_category in meta_rules_json.get("meta_rules").get(metarule).get("action_categories"):
                human_result += "\t\t" + action_category + "\n"
        return human_result
