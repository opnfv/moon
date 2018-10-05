import logging
from moon_manager.api.base_exception import BaseException

logger = logging.getLogger("moon.manager.api." + __name__)


class UnknownName(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(UnknownName, self).__init__(message)


class UnknownId(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(UnknownId, self).__init__(message)


class MissingIdOrName(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(MissingIdOrName, self).__init__(message)


class UnknownField(BaseException):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(UnknownField, self).__init__(message)


class JsonUtils:
    @staticmethod
    def get_override(json_content):
        if "override" in json_content:
            return json_content["override"]
        return False

    @staticmethod
    def get_mandatory(json_content):
        if "mandatory" in json_content:
            return json_content["mandatory"]
        return False

    @staticmethod
    def copy_field_if_exists(json_in, json_out, field_name, type_field, default_value=None):
        if field_name in json_in:
            json_out[field_name] = json_in[field_name]
        else:
            if type_field is bool:
                if default_value is None:
                    default_value = False
                json_out[field_name] = default_value
            if type_field is str:
                if default_value is None:
                    default_value = ""
                json_out[field_name] = default_value
            if type_field is dict:
                json_out[field_name] = dict()
            if type_field is list:
                json_out[field_name] = []

    @staticmethod
    def _get_element_in_db_from_id(element_type, element_id, user_id, policy_id, category_id,
                                   meta_rule_id, manager):
        # the item is supposed to be in the db, we check it exists!
        if element_type == "model":
            data_db = manager.get_models(user_id, model_id=element_id)
        elif element_type == "policy":
            data_db = manager.get_policies(user_id, policy_id=element_id)
        elif element_type == "subject":
            data_db = manager.get_subjects(user_id, policy_id, perimeter_id=element_id)
        elif element_type == "object":
            data_db = manager.get_objects(user_id, policy_id, perimeter_id=element_id)
        elif element_type == "action":
            data_db = manager.get_actions(user_id, policy_id, perimeter_id=element_id)
        elif element_type == "subject_category":
            data_db = manager.get_subject_categories(user_id, category_id=element_id)
        elif element_type == "object_category":
            data_db = manager.get_object_categories(user_id, category_id=element_id)
        elif element_type == "action_category":
            data_db = manager.get_action_categories(user_id, category_id=element_id)
        elif element_type == "meta_rule":
            data_db = manager.get_meta_rules(user_id, meta_rule_id=element_id)
        elif element_type == "subject_data":
            data_db = manager.get_subject_data(user_id, policy_id, data_id=element_id,
                                               category_id=category_id)
        elif element_type == "object_data":
            data_db = manager.get_object_data(user_id, policy_id, data_id=element_id,
                                              category_id=category_id)
        elif element_type == "action_data":
            data_db = manager.get_action_data(user_id, policy_id, data_id=element_id,
                                              category_id=category_id)
        elif element_type == "meta_rule":
            data_db = manager.get_meta_rules(user_id, meta_rule_id=meta_rule_id)
        else:
            raise Exception("Conversion of {} not implemented yet!".format(element_type))

        # logger.info(data_db)

        # do some post processing ... the result should be {key : { .... .... } }
        if element_type == "subject_data" or element_type == "object_data" or element_type == "action_data":
            if data_db is not None and isinstance(data_db, list):
                # TODO remove comments after fixing the bug on moondb when adding metarule : we can have several identical entries !
                # if len(data_db) > 1:
                #    raise Exception("Several {} with the same id : {}".format(element_type, data_db))
                data_db = data_db[0]

            if data_db is not None and data_db["data"] is not None and isinstance(data_db["data"],
                                                                                  dict):
                # TODO remove comments after fixing the bug on moondb when adding metarule : we can have several identical entries !
                # if len(data_db["data"].values()) != 1:
                #    raise Exception("Several {} with the same id : {}".format(element_type, data_db))
                # data_db = data_db["data"]
                # TODO remove these two lines after fixing the bug on moondb when adding metarule : we can have several identical entries !
                list_values = list(data_db["data"].values())
                data_db = list_values[0]
            # logger.info("subject data after postprocessing {}".format(data_db))
        return data_db

    @staticmethod
    def _get_element_id_in_db_from_name(element_type, element_name, user_id, policy_id, category_id,
                                        meta_rule_id, manager):
        if element_type == "model":
            data_db = manager.get_models(user_id)
        elif element_type == "policy":
            data_db = manager.get_policies(user_id)
        elif element_type == "subject":
            data_db = manager.get_subjects(user_id, policy_id)
        elif element_type == "object":
            data_db = manager.get_objects(user_id, policy_id)
        elif element_type == "action":
            data_db = manager.get_actions(user_id, policy_id)
        elif element_type == "subject_category":
            data_db = manager.get_subject_categories(user_id)
        elif element_type == "object_category":
            data_db = manager.get_object_categories(user_id)
        elif element_type == "action_category":
            data_db = manager.get_action_categories(user_id)
        elif element_type == "meta_rule":
            data_db = manager.get_meta_rules(user_id)
        elif element_type == "subject_data":
            data_db = manager.get_subject_data(user_id, policy_id, category_id=category_id)
        elif element_type == "object_data":
            data_db = manager.get_object_data(user_id, policy_id, category_id=category_id)
        elif element_type == "action_data":
            data_db = manager.get_action_data(user_id, policy_id, category_id=category_id)
        elif element_type == "meta_rule":
            data_db = manager.get_meta_rules(user_id)
        elif element_type == "rule":
            data_db = manager.get_rules(user_id, policy_id)
        else:
            raise BaseException("Conversion of {} not implemented yet!".format(element_type))

        if isinstance(data_db, dict):
            for key_id in data_db:
                if isinstance(data_db[key_id], dict) and "name" in data_db[key_id]:
                    if data_db[key_id]["name"] == element_name:
                        return key_id
        else:
            for elt in data_db:
                if isinstance(elt,
                              dict) and "data" in elt:  # we handle here subject_data, object_data and action_data...
                    for data_key in elt["data"]:
                        # logger.info("data from the db {} ".format(elt["data"][data_key]))
                        data = elt["data"][data_key]
                        if "name" in data and data["name"] == element_name:
                            return data_key
                        if "value" in data and data["value"]["name"] == element_name:
                            return data_key
        return None

    @staticmethod
    def convert_name_to_id(json_in, json_out, field_name_in, field_name_out, element_type, manager,
                           user_id, policy_id=None, category_id=None, meta_rule_id=None,
                           field_mandatory=True):
        if field_name_in not in json_in:
            raise UnknownField("The field {} is not in the input json".format(field_name_in))

        if "id" in json_in[field_name_in]:
            data_db = JsonUtils._get_element_in_db_from_id(element_type,
                                                           json_in[field_name_in]["id"], user_id,
                                                           policy_id, category_id, meta_rule_id,
                                                           manager)
            if data_db is None:
                raise UnknownId("No {} with id {} found in database".format(element_type,
                                                                    json_in[field_name_in]["id"]))
            json_out[field_name_out] = json_in[field_name_in]["id"]

        elif "name" in json_in[field_name_in]:
            id_in_db = JsonUtils._get_element_id_in_db_from_name(element_type,
                                                                 json_in[field_name_in]["name"],
                                                                 user_id, policy_id, category_id,
                                                                 meta_rule_id, manager)
            if id_in_db is None:
                raise UnknownName(
                    "No {} with name {} found in database".format(element_type,
                                                                  json_in[field_name_in]["name"]))
            json_out[field_name_out] = id_in_db
        elif field_mandatory is True:
            raise MissingIdOrName("No id or name found in the input json {}".format(json_in))

    @staticmethod
    def convert_id_to_name(id_, json_out, field_name_out, element_type, manager, user_id,
                           policy_id=None, category_id=None, meta_rule_id=None):
        json_out[field_name_out] = {
            "name": JsonUtils.convert_id_to_name_string(id_, element_type, manager, user_id,
                                                        policy_id, category_id, meta_rule_id)}

    @staticmethod
    def __convert_results_to_element(element):
        if isinstance(element, dict) and "name" not in element and "value" not in element:
            list_values = [v for v in element.values()]
        elif isinstance(element, list):
            list_values = element
        else:
            list_values = []
            list_values.append(element)
        return list_values[0]

    @staticmethod
    def convert_id_to_name_string(id_, element_type, manager, user_id,
                                  policy_id=None, category_id=None, meta_rule_id=None):

        element = JsonUtils._get_element_in_db_from_id(element_type, id_, user_id, policy_id,
                                                       category_id, meta_rule_id, manager)
        # logger.info(element)
        if element is None:
            raise UnknownId("No {} with id {} found in database".format(element_type, id_))
        res = JsonUtils.__convert_results_to_element(element)
        # logger.info(res)
        if "name" in res:
            return res["name"]
        if "value" in res and "name" in res["value"]:
            return res["value"]["name"]
        return None

    @staticmethod
    def convert_names_to_ids(json_in, json_out, field_name_in, field_name_out, element_type,
                             manager, user_id, policy_id=None, category_id=None, meta_rule_id=None,
                             field_mandatory=True):
        ids = []
        if field_name_in not in json_in:
            raise UnknownField("The field {} is not in the input json".format(field_name_in))

        for elt in json_in[field_name_in]:
            if "id" in elt:
                data_db = JsonUtils._get_element_in_db_from_id(element_type, elt["id"], user_id,
                                                               policy_id, category_id,
                                                               meta_rule_id, manager)
                if data_db is None:
                    raise UnknownId(
                        "No {} with id {} found in database".format(element_type, elt["id"]))
                ids.append(elt["id"])
            elif "name" in elt:
                id_in_db = JsonUtils._get_element_id_in_db_from_name(element_type, elt["name"],
                                                                     user_id, policy_id,
                                                                     category_id, meta_rule_id,
                                                                     manager)
                if id_in_db is None:
                    raise UnknownName(
                        "No {} with name {} found in database".format(element_type, elt["name"]))
                ids.append(id_in_db)
            elif field_mandatory is True:
                raise MissingIdOrName("No id or name found in the input json {}".format(elt))
        json_out[field_name_out] = ids

    @staticmethod
    def convert_ids_to_names(ids, json_out, field_name_out, element_type, manager, user_id,
                             policy_id=None, category_id=None, meta_rule_id=None):
        res_array = []
        for id_ in ids:
            element = JsonUtils._get_element_in_db_from_id(element_type, id_, user_id, policy_id,
                                                           category_id, meta_rule_id, manager)
            if element is None:
                raise UnknownId("No {} with id {} found in database".format(element_type, id_))
            res = JsonUtils.__convert_results_to_element(element)
            # logger.info(res)
            if "name" in res:
                res_array.append({"name": res["name"]})
            if "value" in res and "name" in res["value"]:
                res_array.append({"name": res["value"]["name"]})
        json_out[field_name_out] = res_array
