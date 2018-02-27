import logging
from flask_restful import Resource
from python_moonutilities.security_functions import check_auth
from python_moondb.core import PDPManager
from python_moondb.core import PolicyManager
from python_moondb.core import ModelManager
from moon_manager.api.json_utils import JsonUtils, BaseException

__version__ = "4.5.0"

logger = logging.getLogger("moon.manager.api." + __name__)


class JsonExport(Resource):

    __urls__ = (
        "/export",
        "/export/",
    )

    def _export_rules(self, json_content):
        policies = PolicyManager.get_policies(self._user_id)
        rules_array = []

        for policy_key in policies:
            rules = PolicyManager.get_rules(self._user_id, policy_key)
            rules = rules["rules"]
            # logger.info(rules)
            for rule in rules:
                rule_dict = dict()
                JsonUtils.copy_field_if_exists(rule, rule_dict, "instructions", dict)
                JsonUtils.copy_field_if_exists(rule, rule_dict, "enabled", True)
                JsonUtils.convert_id_to_name(rule["meta_rule_id"], rule_dict, "meta_rule", "meta_rule", ModelManager, self._user_id)
                JsonUtils.convert_id_to_name(policy_key, rule_dict, "policy", "policy", PolicyManager, self._user_id)
                ids = rule["rule"]
                rule_description = dict()
                JsonUtils.convert_ids_to_names([ids[0]], rule_description, "subject_data", "subject_data",  PolicyManager, self._user_id, policy_key)
                JsonUtils.convert_ids_to_names([ids[1]], rule_description, "object_data", "object_data", PolicyManager, self._user_id, policy_key)
                JsonUtils.convert_ids_to_names([ids[2]], rule_description, "action_data", "action_data", PolicyManager, self._user_id, policy_key)
                rule_dict["rule"] = rule_description
                logger.info("Exporting rule {}".format(rule_dict))
                rules_array.append(rule_dict)

        if len(rules_array) > 0:
            json_content['rules'] = rules_array

    def _export_meta_rules(self, json_content):
        meta_rules = ModelManager.get_meta_rules(self._user_id)
        meta_rules_array = []
        # logger.info(meta_rules)
        for meta_rule_key in meta_rules:
            #logger.info(meta_rules[meta_rule_key])
            meta_rule_dict = dict()
            JsonUtils.copy_field_if_exists(meta_rules[meta_rule_key], meta_rule_dict, "name", str)
            JsonUtils.copy_field_if_exists(meta_rules[meta_rule_key], meta_rule_dict, "description", str)
            JsonUtils.convert_ids_to_names(meta_rules[meta_rule_key]["subject_categories"], meta_rule_dict, "subject_categories", "subject_category", ModelManager, self._user_id)
            JsonUtils.convert_ids_to_names(meta_rules[meta_rule_key]["object_categories"], meta_rule_dict, "object_categories", "object_category", ModelManager, self._user_id)
            JsonUtils.convert_ids_to_names(meta_rules[meta_rule_key]["action_categories"], meta_rule_dict, "action_categories", "action_category", ModelManager, self._user_id)
            logger.info("Exporting meta rule {}".format(meta_rule_dict))
            meta_rules_array.append(meta_rule_dict)
        if len(meta_rules_array) > 0:
            json_content['meta_rules'] = meta_rules_array

    def _export_subject_object_action_assignments(self, type_element, json_content):
        export_method_data = getattr(PolicyManager, 'get_' + type_element + '_assignments')
        policies = PolicyManager.get_policies(self._user_id)
        element_assignments_array = []
        for policy_key in policies:
            assignments = export_method_data(self._user_id, policy_key)
            #logger.info(assignments)
            for assignment_key in assignments:
                assignment_dict = dict()
                JsonUtils.convert_id_to_name(assignments[assignment_key][type_element + "_id"], assignment_dict, type_element, type_element , PolicyManager, self._user_id, policy_key)
                JsonUtils.convert_id_to_name(assignments[assignment_key]["category_id"], assignment_dict, "category", type_element + "_category", ModelManager, self._user_id, policy_key)
                JsonUtils.convert_ids_to_names(assignments[assignment_key]["assignments"], assignment_dict, "assignments", type_element + "_data", PolicyManager, self._user_id, policy_key)
                element_assignments_array.append(assignment_dict)
                logger.info("Exporting {} assignment {}".format(type_element, assignment_dict))
        if len(element_assignments_array) > 0:
            json_content[type_element + '_assignments'] = element_assignments_array

    def _export_subject_object_action_datas(self, type_element, json_content):
        export_method_data = getattr(PolicyManager, 'get_' + type_element + '_data')
        policies = PolicyManager.get_policies(self._user_id)
        element_datas_array = []
        for policy_key in policies:
            datas = export_method_data(self._user_id, policy_key)
            #logger.info("data found : {}".format(datas))
            for data_group in datas:
                policy_id = data_group["policy_id"]
                category_id = data_group["category_id"]
                # logger.info(data_group["data"])
                for data_key in data_group["data"]:
                    data_dict = dict()
                    if type_element == 'subject':
                        JsonUtils.copy_field_if_exists(data_group["data"][data_key], data_dict, "name", str)
                        JsonUtils.copy_field_if_exists(data_group["data"][data_key], data_dict, "description", str)
                    else:
                        JsonUtils.copy_field_if_exists(data_group["data"][data_key]["value"], data_dict, "name", str)
                        JsonUtils.copy_field_if_exists(data_group["data"][data_key]["value"], data_dict, "description", str)

                    JsonUtils.convert_id_to_name(policy_id, data_dict, "policy", "policy", PolicyManager, self._user_id)
                    JsonUtils.convert_id_to_name(category_id, data_dict, "category", type_element + "_category", ModelManager, self._user_id, policy_key)
                    logger.info("Exporting {} data {}".format(type_element, data_dict))
                    element_datas_array.append(data_dict)

        if len(element_datas_array) > 0:
            json_content[type_element + '_data'] = element_datas_array

    def _export_subject_object_action_categories(self, type_element, json_content):
        export_method = getattr(ModelManager, 'get_' + type_element + '_categories')
        element_categories = export_method(self._user_id)
        element_categories_array = []
        for element_category_key in element_categories:
            element_category = dict()
            JsonUtils.copy_field_if_exists(element_categories[element_category_key], element_category, "name", str)
            JsonUtils.copy_field_if_exists(element_categories[element_category_key], element_category, "description", str)
            element_categories_array.append(element_category)
            logger.info("Exporting {} category {}".format(type_element, element_category))
        if len(element_categories_array) > 0:
            json_content[type_element + '_categories'] = element_categories_array

    def _export_subject_object_action(self, type_element, json_content):
        export_method = getattr(PolicyManager, 'get_' + type_element + 's')
        policies = PolicyManager.get_policies(self._user_id)
        element_dict = dict()
        elements_array = []
        for policy_key in policies:
            elements = export_method(self._user_id, policy_key)
            for element_key in elements:
                #logger.info("Exporting {}".format(elements[element_key]))
                element = dict()
                JsonUtils.copy_field_if_exists(elements[element_key], element, "name", str)
                JsonUtils.copy_field_if_exists(elements[element_key], element, "description", str)
                JsonUtils.copy_field_if_exists(elements[element_key], element, "extra", dict)
                if element["name"] not in element_dict:
                    element["policies"] = []
                    element_dict[element["name"]] = element
                current_element = element_dict[element["name"]]
                current_element["policies"].append({"name": JsonUtils.convert_id_to_name_string(policy_key, "policy", PolicyManager, self._user_id)})

        for key in element_dict:
            logger.info("Exporting {} {}".format(type_element, element_dict[key]))
            elements_array.append(element_dict[key])

        if len(elements_array) > 0:
            json_content[type_element + 's'] = elements_array

    def _export_policies(self, json_content):
        policies = PolicyManager.get_policies(self._user_id)
        policies_array = []
        for policy_key in policies:
            policy = dict()
            JsonUtils.copy_field_if_exists(policies[policy_key], policy, "name", str)
            JsonUtils.copy_field_if_exists(policies[policy_key], policy, "genre", str)
            JsonUtils.copy_field_if_exists(policies[policy_key], policy, "description", str)
            JsonUtils.convert_id_to_name(policies[policy_key]["model_id"], policy, "model", "model", ModelManager, self._user_id)
            logger.info("Exporting policy {}".format(policy))
            policies_array.append(policy)
        if len(policies_array) > 0:
            json_content["policies"] = policies_array

    def _export_models(self, json_content):
        models = ModelManager.get_models(self._user_id)
        models_array = []
        for model_key in models:
            model = dict()
            JsonUtils.copy_field_if_exists(models[model_key], model, "name", str)
            JsonUtils.copy_field_if_exists(models[model_key], model, "description", str)
            # logger.info(models[model_key]["meta_rules"])
            JsonUtils.convert_ids_to_names(models[model_key]["meta_rules"], model, "meta_rules", "meta_rule", ModelManager, self._user_id)
            logger.info("Exporting model {}".format(model))
            models_array.append(model)
        if len(models_array) > 0:
            json_content["models"] = models_array

    def _export_pdps(self, json_content):
        pdps = PDPManager.get_pdp(self._user_id)
        pdps_array = []
        for pdp_key in pdps:
            logger.info("Exporting pdp {}".format(pdps[pdp_key]))
            pdps_array.append(pdps[pdp_key])
        if len(pdps_array) > 0:
            json_content["pdps"] = pdps_array

    def _export_json(self, user_id):
        self._user_id = user_id
        json_content = dict()

        logger.info("Exporting pdps...")
        self._export_pdps(json_content)
        logger.info("Exporting policies...")
        self._export_policies(json_content)
        logger.info("Exporting models...")
        self._export_models(json_content)
        # export subjects, subject_data, subject_categories, subject_assignements idem for object and action
        list_element = [{"key": "subject"}, {"key": "object"}, {"key": "action"}]
        for elt in list_element:
            logger.info("Exporting {}s...".format(elt["key"]))
            self._export_subject_object_action(elt["key"], json_content)
            logger.info("Exporting {} categories...".format(elt["key"]))
            self._export_subject_object_action_categories(elt["key"], json_content)
            logger.info("Exporting {} data...".format(elt["key"]))
            self._export_subject_object_action_datas(elt["key"], json_content)
            logger.info("Exporting {} assignments...".format(elt["key"]))
            self._export_subject_object_action_assignments(elt["key"], json_content)
        logger.info("Exporting meta rules...")
        self._export_meta_rules(json_content)
        logger.info("Exporting rules...")
        self._export_rules(json_content)

        return json_content

    @check_auth
    def get(self, user_id=None):
        """Import file.

        :param user_id: user ID who do the request
        :return: {

        }
        :internal_api:
        """
        json_file = self._export_json(user_id)
        logger.info(json_file)
        return {"content": json_file}
