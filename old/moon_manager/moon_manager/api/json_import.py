# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from flask import request
from flask_restful import Resource
import flask_restful
from flask import abort

from python_moonutilities.security_functions import check_auth
from python_moonutilities import exceptions
import logging
import json

from moon_manager.api.base_exception import BaseException
from moon_manager.api.json_utils import JsonUtils, UnknownName
from python_moondb.core import PDPManager
from python_moondb.core import PolicyManager
from python_moondb.core import ModelManager

__version__ = "4.5.0"

logger = logging.getLogger("moon.manager.api." + __name__)

INST_CALLBACK = 0
DATA_CALLBACK = 1
ASSIGNMENT_CALLBACK = 2
CATEGORIES_CALLBACK = 3


class ForbiddenOverride(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(ForbiddenOverride, self).__init__(message)


class UnknownPolicy(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(UnknownPolicy, self).__init__(message)


class UnknownModel(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(UnknownModel, self).__init__(message)


class UnknownData(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(UnknownData, self).__init__(message)


class MissingPolicy(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(MissingPolicy, self).__init__(message)


class InvalidJson(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(InvalidJson, self).__init__(message)


class JsonImport(Resource):
    __urls__ = (
        "/import",
        "/import/",
    )

    def _reorder_rules_ids(self, rule, ordered_perimeter_categories_ids, json_data_ids, policy_id,
                           get_function):
        ordered_json_ids = [None] * len(ordered_perimeter_categories_ids)
        for json_id in json_data_ids:
            data = get_function(self._user_id, policy_id, data_id=json_id)
            data = data[0]
            if data["category_id"] not in ordered_perimeter_categories_ids:
                raise InvalidJson(
                    "The category id {} of the rule {} does not match the meta rule".format(
                        data["category_id"], rule))
            if ordered_json_ids[
                ordered_perimeter_categories_ids.index(data["category_id"])] is not None:
                raise InvalidJson(
                    "The category id {} of the rule {} shall not be used twice in the same rule".format(
                        data["category_id"], rule))
            ordered_json_ids[ordered_perimeter_categories_ids.index(data["category_id"])] = json_id
            logger.info(ordered_json_ids)
        return ordered_json_ids

    def _import_rules(self, json_rules):
        if not isinstance(json_rules, list):
            raise InvalidJson("rules shall be a list!")

        for json_rule in json_rules:
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_rule, json_to_use, "instructions", str)
            JsonUtils.copy_field_if_exists(json_rule, json_to_use, "enabled", bool,
                                           default_value=True)

            json_ids = dict()
            JsonUtils.convert_name_to_id(json_rule, json_ids, "policy", "policy_id", "policy",
                                         PolicyManager, self._user_id)
            JsonUtils.convert_name_to_id(json_rule, json_to_use, "meta_rule", "meta_rule_id",
                                         "meta_rule", ModelManager, self._user_id)
            json_subject_ids = dict()
            json_object_ids = dict()
            json_action_ids = dict()
            JsonUtils.convert_names_to_ids(json_rule["rule"], json_subject_ids, "subject_data",
                                           "subject", "subject_data", PolicyManager, self._user_id,
                                           json_ids["policy_id"])
            JsonUtils.convert_names_to_ids(json_rule["rule"], json_object_ids, "object_data",
                                           "object", "object_data", PolicyManager, self._user_id,
                                           json_ids["policy_id"])
            JsonUtils.convert_names_to_ids(json_rule["rule"], json_action_ids, "action_data",
                                           "action", "action_data", PolicyManager, self._user_id,
                                           json_ids["policy_id"])

            meta_rule = ModelManager.get_meta_rules(self._user_id, json_to_use["meta_rule_id"])
            meta_rule = [v for v in meta_rule.values()]
            meta_rule = meta_rule[0]

            json_to_use_rule = self._reorder_rules_ids(json_rule, meta_rule["subject_categories"],
                                                       json_subject_ids["subject"],
                                                       json_ids["policy_id"],
                                                       PolicyManager.get_subject_data)
            json_to_use_rule = json_to_use_rule + self._reorder_rules_ids(json_rule, meta_rule[
                "object_categories"], json_object_ids["object"], json_ids["policy_id"],
                                                                          PolicyManager.get_object_data)
            json_to_use_rule = json_to_use_rule + self._reorder_rules_ids(json_rule, meta_rule[
                "action_categories"], json_action_ids["action"], json_ids["policy_id"],
                                                                          PolicyManager.get_action_data)
            json_to_use["rule"] = json_to_use_rule
            try:
                logger.debug("Adding / updating a rule from json {}".format(json_to_use))
                PolicyManager.add_rule(self._user_id, json_ids["policy_id"],
                                       json_to_use["meta_rule_id"], json_to_use)
            except exceptions.RuleExisting:
                pass
            except exceptions.PolicyUnknown:
                raise UnknownPolicy("Unknown policy with id {}".format(json_ids["policy_id"]))

    def _import_meta_rules(self, json_meta_rules):
        logger.info("Input meta rules : {}".format(json_meta_rules))
        for json_meta_rule in json_meta_rules:
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_meta_rule, json_to_use, "name", str)
            JsonUtils.copy_field_if_exists(json_meta_rule, json_to_use, "description", str)
            JsonUtils.convert_names_to_ids(json_meta_rule, json_to_use, "subject_categories",
                                           "subject_categories", "subject_category", ModelManager,
                                           self._user_id)
            JsonUtils.convert_names_to_ids(json_meta_rule, json_to_use, "object_categories",
                                           "object_categories", "object_category", ModelManager,
                                           self._user_id)
            JsonUtils.convert_names_to_ids(json_meta_rule, json_to_use, "action_categories",
                                           "action_categories", "action_category", ModelManager,
                                           self._user_id)
            logger.debug("Adding / updating a metarule from json {}".format(json_meta_rule))
            meta_rule = ModelManager.add_meta_rule(self._user_id, meta_rule_id=None,
                                                   value=json_to_use)
            logger.debug("Added / updated meta rule : {}".format(meta_rule))

    def _import_subject_object_action_assignments(self, json_item_assignments, type_element):
        import_method = getattr(PolicyManager, 'add_' + type_element + '_assignment')
        get_method = getattr(PolicyManager, 'get_' + type_element + '_data')

        if not isinstance(json_item_assignments, list):
            raise InvalidJson(type_element + " assignments shall be a list!")

        # get the policy id related to the user
        policies = PolicyManager.get_policies(self._user_id)

        for json_item_assignment in json_item_assignments:
            item_override = JsonUtils.get_override(json_item_assignment)
            if item_override is True:
                raise ForbiddenOverride(
                    "{} assignments do not support override flag !".format(type_element))

            json_assignment = dict()
            JsonUtils.convert_name_to_id(json_item_assignment, json_assignment, "category",
                                         "category_id", type_element + "_category", ModelManager,
                                         self._user_id)

            has_found_data = False
            # loop over policies
            for policy_id in policies:
                json_data = dict()
                try:
                    JsonUtils.convert_name_to_id(json_item_assignment, json_assignment,
                                                 type_element, "id", type_element, PolicyManager,
                                                 self._user_id, policy_id)
                    JsonUtils.convert_names_to_ids(json_item_assignment, json_data, "assignments",
                                                   "data_id", type_element + "_data", PolicyManager,
                                                   self._user_id, policy_id,
                                                   json_assignment["category_id"])
                    has_found_data = True
                except UnknownName:
                    # the category or data has not been found in this policy : we look into the next one
                    continue
                for data_id in json_data["data_id"]:
                    # find the policy related to the current data
                    data = get_method(self._user_id, policy_id, data_id,
                                      json_assignment["category_id"])
                    if data is not None and len(data) == 1:
                        logger.debug(
                            "Adding / updating a {} assignment from json {}".format(type_element,
                                                                                    json_assignment))
                        import_method(self._user_id, policy_id, json_assignment["id"],
                                      json_assignment["category_id"],
                                      data_id)
                    else:
                        raise UnknownData("Unknown data with id {}".format(data_id))

            # case the data has not been found in any policies
            if has_found_data is False:
                raise InvalidJson("The json contains unknown {} data or category : {}".format(
                    type_element,
                    json_item_assignment))

    def _import_subject_object_action_datas(self, json_items_data, mandatory_policy_ids,
                                            type_element):
        if type_element == "subject":
            import_method = getattr(PolicyManager, 'set_' + type_element + '_data')
        else:
            import_method = getattr(PolicyManager, 'add_' + type_element + '_data')
        # get_method = getattr(PolicyManager, 'get_' + type_element + '_data')

        if not isinstance(json_items_data, list):
            raise InvalidJson(type_element + " data shall be a list!")

        for json_item_data in json_items_data:
            item_override = JsonUtils.get_override(json_items_data)
            if item_override is True:
                raise ForbiddenOverride(
                    "{} datas do not support override flag !".format(type_element))
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_item_data, json_to_use, "name", str)
            JsonUtils.copy_field_if_exists(json_item_data, json_to_use, "description", str)
            json_policy = dict()
            # field_mandatory : not mandatory if there is some mandatory policies
            JsonUtils.convert_names_to_ids(json_item_data, json_policy, "policies", "policy_id",
                                           "policy",
                                           PolicyManager, self._user_id,
                                           field_mandatory=len(mandatory_policy_ids) == 0)
            json_category = dict()
            JsonUtils.convert_name_to_id(json_item_data, json_category, "category", "category_id",
                                         type_element + "_category",
                                         ModelManager, self._user_id)
            policy_ids = []
            if "policy_id" in json_policy:
                policy_ids = json_policy["policy_id"]

            for policy_id in policy_ids:
                if policy_id is not None and policy_id not in mandatory_policy_ids:
                    mandatory_policy_ids.append(policy_id)

            if len(mandatory_policy_ids) == 0:
                raise InvalidJson("Invalid data, the policy shall be set when importing {}".format(
                    json_item_data))
            category_id = None
            if "category_id" in json_category:
                category_id = json_category["category_id"]
            if category_id is None:
                raise InvalidJson(
                    "Invalid data, the category shall be set when importing {}".format(
                        json_item_data))

            for policy_id in mandatory_policy_ids:
                try:
                    data = import_method(self._user_id, policy_id, category_id=category_id,
                                         value=json_to_use)
                except exceptions.PolicyUnknown:
                    raise UnknownPolicy("Unknown policy with id {}".format(policy_id))
                except Exception as e:
                    logger.exception(str(e))
                    raise e

    def _import_subject_object_action_categories(self, json_item_categories, type_element):
        import_method = getattr(ModelManager, 'add_' + type_element + '_category')
        get_method = getattr(ModelManager, 'get_' + type_element + '_categories')

        categories = get_method(self._user_id)

        if not isinstance(json_item_categories, list):
            raise InvalidJson(type_element + " categories shall be a list!")

        for json_item_category in json_item_categories:
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_item_category, json_to_use, "name", str)

            # check if category with the same name exists : do this in moondb ?
            existing_id = None
            for category_key in categories:
                if categories[category_key]["name"] == json_to_use["name"]:
                    existing_id = category_key

            JsonUtils.copy_field_if_exists(json_item_category, json_to_use, "description", str)
            item_override = JsonUtils.get_override(json_item_category)
            if item_override is True:
                raise ForbiddenOverride(
                    "{} categories do not support override flag !".format(type_element))

            try:
                category = import_method(self._user_id, existing_id, json_to_use)
            except (exceptions.SubjectCategoryExisting, exceptions.ObjectCategoryExisting,
                    exceptions.ActionCategoryExisting):
                # it already exists: do nothing
                logger.warning("Ignored {} category with name {} is already in the database".format(
                    type_element, json_to_use["name"]))
            except Exception as e:
                logger.warning("Error while importing the category : {}".format(str(e)))
                logger.exception(str(e))
                raise e

    def _import_subject_object_action(self, json_items, mandatory_policy_ids, type_element):
        import_method = getattr(PolicyManager, 'add_' + type_element)
        get_method = getattr(PolicyManager, 'get_' + type_element + 's')

        if not isinstance(json_items, list):
            raise InvalidJson(type_element + " items shall be a list!")

        for json_item in json_items:
            json_without_policy_name = dict()
            JsonUtils.copy_field_if_exists(json_item, json_without_policy_name, "name", str)
            JsonUtils.copy_field_if_exists(json_item, json_without_policy_name, "description", str)
            JsonUtils.copy_field_if_exists(json_item, json_without_policy_name, "extra", dict)
            JsonUtils.convert_names_to_ids(json_item, json_without_policy_name, "policies",
                                           "policy_list", "policy", PolicyManager, self._user_id,
                                           field_mandatory=False)
            policy_ids = json_without_policy_name["policy_list"]
            for mandatory_policy_id in mandatory_policy_ids:
                if mandatory_policy_id not in policy_ids:
                    policy_ids.append(mandatory_policy_id)
                    # policy_ids and json_without_policy_name are references to the same array...
                    # json_without_policy_name["policy_list"].append(mandatory_policy_id)

            item_override = JsonUtils.get_override(json_item)
            if item_override is True:
                raise ForbiddenOverride("{} does not support override flag !".format(type_element))

            if len(policy_ids) == 0:
                raise MissingPolicy(
                    "a {} needs at least one policy to be created or updated : {}".format(
                        type_element, json.dumps(json_item)))

            for policy_id in policy_ids:
                try:
                    items_in_db = get_method(self._user_id, policy_id)
                    key = None
                    for key_in_db in items_in_db:
                        if items_in_db[key_in_db]["name"] == json_without_policy_name["name"]:
                            key = key_in_db
                            break
                    element = import_method(self._user_id, policy_id, perimeter_id=key,
                                            value=json_without_policy_name)
                    logger.debug("Added / updated {} : {}".format(type_element, element))

                except exceptions.PolicyUnknown:
                    raise UnknownPolicy("Unknown policy when adding a {}!".format(type_element))
                except Exception as e:
                    logger.exception(str(e))
                    raise BaseException(str(e))

    def _import_policies(self, json_policies):
        policy_mandatory_ids = []

        if not isinstance(json_policies, list):
            raise InvalidJson("policies shall be a list!")

        for json_policy in json_policies:
            # TODO put this in moondb
            # policy_in_db = PolicyManager.get_policies_by_name(json_without_model_name["name"])
            policies = PolicyManager.get_policies(self._user_id)
            policy_in_db = None
            policy_id = None
            for policy_key in policies:
                if policies[policy_key]["name"] == json_policy["name"]:
                    policy_in_db = policies[policy_key]
                    policy_id = policy_key
            # end TODO
            if policy_in_db is None:
                policy_does_exist = False
            else:
                policy_does_exist = True

            policy_override = JsonUtils.get_override(json_policy)
            policy_mandatory = JsonUtils.get_mandatory(json_policy)

            if policy_override is False and policy_does_exist:
                if policy_id:
                    policy_mandatory_ids.append(policy_id)
                    logger.warning(
                        "Existing policy not updated because of the override option is not set !")
                    continue

            json_without_model_name = dict()
            JsonUtils.copy_field_if_exists(json_policy, json_without_model_name, "name", str)
            JsonUtils.copy_field_if_exists(json_policy, json_without_model_name, "description", str)
            JsonUtils.copy_field_if_exists(json_policy, json_without_model_name, "genre", str)
            JsonUtils.convert_name_to_id(json_policy, json_without_model_name, "model", "model_id",
                                         "model", ModelManager, self._user_id,
                                         field_mandatory=False)

            if not policy_does_exist:
                logger.debug("Creating policy {} ".format(json_without_model_name))
                added_policy = PolicyManager.add_policy(self._user_id, None,
                                                        json_without_model_name)
                if policy_mandatory is True:
                    keys = list(added_policy.keys())
                    policy_mandatory_ids.append(keys[0])
            elif policy_override is True:
                logger.debug("Updating policy {} ".format(json_without_model_name))
                updated_policy = PolicyManager.update_policy(self._user_id, policy_id,
                                                             json_without_model_name)
                if policy_mandatory is True:
                    policy_mandatory_ids.append(policy_id)
        return policy_mandatory_ids

    def _import_models_with_new_meta_rules(self, json_models):
        if not isinstance(json_models, list):
            raise InvalidJson("models shall be a list!")

        for json_model in json_models:
            logger.debug("json_model {}".format(json_model))
            models = ModelManager.get_models(self._user_id)
            model_in_db = None
            model_id = None
            for model_key in models:
                if ("id" in json_model and model_key == json_model["id"]) or (
                        "name" in json_model and models[model_key]["name"] == json_model["name"]):
                    model_in_db = models[model_key]
                    model_id = model_key

            # this should not occur as the model has been put in db previously in _import_models_without_new_meta_rules
            if model_in_db is None:
                raise UnknownModel("Unknown model ")

            json_key = dict()
            JsonUtils.convert_names_to_ids(json_model, json_key, "meta_rules", "meta_rule_id",
                                           "meta_rule", ModelManager, self._user_id)
            for meta_rule_id in json_key["meta_rule_id"]:
                if meta_rule_id not in model_in_db["meta_rules"]:
                    model_in_db["meta_rules"].append(meta_rule_id)

            ModelManager.update_model(self._user_id, model_id, model_in_db)

    def _import_models_without_new_meta_rules(self, json_models):
        if not isinstance(json_models, list):
            raise InvalidJson("models shall be a list!")

        for json_model in json_models:
            json_without_new_metarules = dict()
            JsonUtils.copy_field_if_exists(json_model, json_without_new_metarules, "name", str)

            # TODO put this in moondb
            # model_in_db = ModelManager.get_models_by_name(json_without_new_metarules["name"])
            models = ModelManager.get_models(self._user_id)
            model_in_db = None
            for model_key in models:
                if models[model_key]["name"] == json_without_new_metarules["name"]:
                    model_in_db = models[model_key]
                    model_id = model_key
            # end TODO

            JsonUtils.copy_field_if_exists(json_model, json_without_new_metarules, "description",
                                           str)
            if model_in_db is None:
                model_does_exist = False
            else:
                json_without_new_metarules["meta_rules"] = model_in_db["meta_rules"]
                model_does_exist = True
            model_override = JsonUtils.get_override(json_model)
            if not model_does_exist:
                logger.debug("Creating model {} ".format(json_without_new_metarules))
                ModelManager.add_model(self._user_id, None, json_without_new_metarules)
            elif model_override is True:
                logger.debug(
                    "Updating model with id {} : {} ".format(model_id, json_without_new_metarules))
                ModelManager.update_model(self._user_id, model_id, json_without_new_metarules)

    def _import_pdps(self, json_pdps):
        if not isinstance(json_pdps, list):
            raise InvalidJson("pdps shall be a list!")

        for json_pdp in json_pdps:
            json_to_use = dict()
            JsonUtils.copy_field_if_exists(json_pdp, json_to_use, "name", str)
            JsonUtils.copy_field_if_exists(json_pdp, json_to_use, "keystone_project_id", str)
            JsonUtils.copy_field_if_exists(json_pdp, json_to_use, "security_pipeline", list)
            JsonUtils.copy_field_if_exists(json_pdp, json_to_use, "description", str)

            pdps = PDPManager.get_pdp(self._user_id)
            exists = False
            for pdp_key in pdps:
                if pdps[pdp_key]["name"] == json_to_use["name"]:
                    PDPManager.update_pdp(self._user_id, pdp_id=pdp_key, value=json_to_use)
                    exists = True
            if exists is False:
                PDPManager.add_pdp(self._user_id, value=json_to_use)

    def _import_json(self, user_id):
        self._user_id = user_id
        if 'file' in request.files:
            file = request.files['file']
            logger.debug("Importing {} file...".format(file))
            json_content = json.load(file)
        else:
            json_content = request.json
        logger.debug("Importing content:  {} ...".format(json_content))

        # first import the models without the meta rules as they are not yet defined
        if "models" in json_content:
            logger.info("Importing models...")
            self._import_models_without_new_meta_rules(json_content["models"])

        # import the policies that depends on the models
        mandatory_policy_ids = []
        if "policies" in json_content:
            logger.info("Importing policies...")
            mandatory_policy_ids = self._import_policies(json_content["policies"])

        # import subjects, subject_data, subject_categories, idem for object and action
        list_element = [{"key": "subject"}, {"key": "object"}, {"key": "action"}]
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "s"
            if key in json_content:
                logger.info("Importing {}...".format(key))
                self._import_subject_object_action(json_content[key], mandatory_policy_ids, in_key)
            key = in_key + "_categories"
            if key in json_content:
                logger.info("Importing {}...".format(key))
                self._import_subject_object_action_categories(json_content[key], in_key)

        # import meta rules
        if "meta_rules" in json_content:
            logger.info("Importing meta rules...")
            self._import_meta_rules(json_content["meta_rules"])

        # add the metarule to model
        if "models" in json_content:
            logger.info("Updating models with meta rules...")
            self._import_models_with_new_meta_rules(json_content["models"])

        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "_data"
            if key in json_content:
                logger.info("Importing {}...".format(key))
                self._import_subject_object_action_datas(json_content[key], mandatory_policy_ids,
                                                         in_key)

        # import subjects assignments, idem for object and action
        for elt in list_element:
            in_key = elt["key"]
            key = in_key + "_assignments"
            if key in json_content:
                logger.info("Importing {}...".format(key))
                self._import_subject_object_action_assignments(json_content[key], in_key)

        # import rules
        if "rules" in json_content:
            logger.info("Importing rules...")
            self._import_rules(json_content["rules"])

        # import pdps
        if "pdps" in json_content:
            logger.info("Importing pdps...")
            self._import_pdps(json_content["pdps"])

    @check_auth
    def post(self, user_id=None):
        """Import file.

        :param user_id: user ID who do the request
        :return: {

        }
        :internal_api:
        """
        self._import_json(user_id)
        return "Import ok !"
