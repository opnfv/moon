from python_moonclient.core.cli_exceptions import MoonCliException


def check_optionnal_result(result):
    if type(result) is not dict:
        raise MoonCliException("Unexpected request result. It should be a dictionnary")
    if "result" in result:
        check_result(result)


def check_result(result):
    if type(result) is not dict or "result" not in result:
        raise MoonCliException(
            "Unexpected request result. It should be a dictionnary with a 'result' entry")
    if result["result"] is None:
        raise MoonCliException("Unexpected request result. The 'result' entry shall not be null")


def _check_generic_in_result(field, result, check_not_null=False):
    if type(field) is not str or type(result) is not dict or field not in result:
        raise MoonCliException(
            "Unexpected request result. It should be a dictionnary with a '{}' entry".format(field))
    if check_not_null is True and result[field] is None:
        raise MoonCliException(
            "Unexpected request result. The '{}' entry shall not be null".format(field))


def check_slaves_in_result(result):
    _check_generic_in_result("slaves", result)


def check_pdp_in_result(result):
    _check_generic_in_result("pdps", result)


def check_model_in_result(result, check_not_null=False):
    _check_generic_in_result("models", result)
    if check_not_null is True and result["models"] is None:
        raise MoonCliException("Unexpected request result. The 'models' entry shall not be null")


def check_meta_rule_in_result(result):
    _check_generic_in_result("meta_rules", result)


def check_rule_in_result(result):
    _check_generic_in_result("rules", result)


def check_subject_in_result(result):
    _check_generic_in_result("subjects", result)


def check_subject_category_in_result(result):
    _check_generic_in_result("subject_categories", result)


def check_object_category_in_result(result):
    _check_generic_in_result("object_categories", result)


def check_action_category_in_result(result):
    _check_generic_in_result("action_categories", result)


def check_policy_in_result(result):
    _check_generic_in_result("policies", result)


def check_object_in_result(result):
    _check_generic_in_result("objects", result)


def check_action_in_result(result):
    _check_generic_in_result("actions", result)


def check_subject_assignment_in_result(result):
    _check_generic_in_result("subject_assignments", result, True)


def check_object_assignment_in_result(result):
    _check_generic_in_result("object_assignments", result, True)


def check_action_assignment_in_result(result):
    _check_generic_in_result("action_assignments", result, True)


def check_pdp_id(pdp_id, result):
    check_pdp_in_result(result)
    if pdp_id not in result['pdps']:
        raise MoonCliException("Unexpected request result. Unknown pdp id")


def _check_generic_name(field, name, field_elt_id, result, do_check_name=True):
    if type(field) is str:
        if result[field] is None:
            raise MoonCliException(
                "Unexpected request result : {} shall not be empty".format(field))
        if field_elt_id not in result[field]:
            raise MoonCliException("Unexpected request result. Unknown {} id".format(field))
        if "name" not in result[field][field_elt_id]:
            raise MoonCliException(
                "Unexpected request result : {} with id {} has no name".format(field, field_elt_id))
        if do_check_name and name != result[field][field_elt_id]["name"]:
            raise MoonCliException(
                "Unexpected request result : {} with id {} has a bad name. Expected {}".format(
                    field, field_elt_id, name))


def check_model_name(name, model_id, result, do_check_name):
    _check_generic_name("models", name, model_id, result, do_check_name)


def check_pdp_name(name, pdp_id, result):
    _check_generic_name("pdps", name, pdp_id, result)


def check_subject_categories_name(name, category_id, result):
    _check_generic_name("subject_categories", name, category_id, result)


def check_object_categories_name(name, category_id, result):
    _check_generic_name("object_categories", name, category_id, result)


def check_action_categories_name(name, category_id, result):
    _check_generic_name("action_categories", name, category_id, result)


def check_meta_rules_name(name, meta_rule_id, result):
    _check_generic_name("meta_rules", name, meta_rule_id, result, False)


def check_policy_name(name, policy_id, result):
    _check_generic_name("policies", name, policy_id, result)


def check_subject_name(name, subject_id, result):
    _check_generic_name("subjects", name, subject_id, result)


def check_object_name(name, object_id, result):
    _check_generic_name("objects", name, object_id, result)


def check_action_name(name, action_id, result):
    _check_generic_name("actions", name, action_id, result)


def check_scat_id_in_dict(scat_id, in_dict):
    if scat_id not in in_dict:
        raise MoonCliException("Unexpected request result. Subject category not in result")


def check_ocat_id_in_dict(ocat_id, in_dict):
    if ocat_id not in in_dict:
        raise MoonCliException("Unexpected request result. Object category not in result")


def check_acat_id_in_dict(acat_id, in_dict):
    if acat_id not in in_dict:
        raise MoonCliException("Unexpected request result. Action category not in result")


def check_policy_id_in_pipeline(policy_id, pipeline):
    if policy_id not in pipeline:
        raise MoonCliException(
            "Unexpected request result. The policy id {} shall be in the pipeline".format(
                policy_id))


def _check_generic_policy_in_dict(field, policy_id, in_dict):
    if type(field) is str:
        if policy_id is not None:
            if "policy_list" not in in_dict:
                raise MoonCliException(
                    "Unexpected request result. The policy list of the {} shall not be empty".format(
                        field))
            if policy_id not in in_dict["policy_list"]:
                raise MoonCliException(
                    "Unexpected request result. The policy with id {} shall be in the {}".format(
                        policy_id, field))


def check_subject_policy(policy_id, in_dict):
    _check_generic_policy_in_dict("subject", policy_id, in_dict)


def check_object_policy(policy_id, in_dict):
    _check_generic_policy_in_dict("object", policy_id, in_dict)


def check_action_policy(policy_id, in_dict):
    _check_generic_policy_in_dict("action", policy_id, in_dict)


def _check_generic_elt_id(field1, field1_id, field2, field2_id, result):
    if type(field1) is str and type(field2) is str:
        if result[field1] is None:
            raise MoonCliException(
                "Unexpected request result: {} shall not be empty".format(field1))
        if field1_id not in result[field1]:
            raise MoonCliException("Unexpected request result. Unknown {} with id".format(field1))
        if field2 not in result[field1][field1_id]:
            raise MoonCliException(
                "Unexpected request result. {} element with id {} has no {} field".format(field1,
                                                                                          field1_id,
                                                                                          field2))
        if field2_id != result[field1][field1_id][field2]:
            raise MoonCliException(
                "Unexpected request result. {} element with id {} has a bad {} id. Expected {}".format(
                    field1, field1_id, field2, field2_id))


def check_policy_model_id(model_id, policy_id, result):
    _check_generic_elt_id("policies", policy_id, "model_id", model_id, result)


def check_pdp_project_id(project_id, pdp_id, result):
    _check_generic_elt_id("pdps", pdp_id, "keystone_project_id", project_id, result)


def check_subject_description(description, in_dict):
    if description is not None:
        if "description" not in in_dict:
            raise MoonCliException(
                "Unexpected request result. The description of the subject shall not be empty")
        if description not in in_dict["description"]:
            raise MoonCliException(
                "Unexpected request result. The description {} shall be in the subject".format(
                    description))


def check_meta_rules_list_in_model(meta_rule_list, model_id, result):
    if result["models"] is None:
        raise MoonCliException("Unexpected request result. results shall not be empty")
    if model_id not in result['models']:
        raise MoonCliException("Unexpected request result. Unknown Model id")
    if "meta_rules" not in result['models'][model_id]:
        raise MoonCliException(
            "Unexpected request result. Meta rules related to model with id {} are empty".format(
                model_id))
    if meta_rule_list != result['models'][model_id]["meta_rules"]:
        raise MoonCliException(
            "Unexpected request result. Meta rule of model with id {} are different from those expected".format(
                model_id))


def check_name_in_slaves(name, slaves):
    if name is None:
        raise MoonCliException("The slave name must be provided !")
    names = map(lambda x: x['name'], slaves)
    if name not in names:
        raise MoonCliException("The slave '{}' was not found !".format(name))


def _check_generic_data_data(field, result):
    if type(field) is str:
        if field not in result:
            raise MoonCliException(
                "Unexpected request result. The {} field shall be in result".format(field))
        # if "data" not in resulti[field]:
        #    raise MoonCliException("Unexpected request result. The data field shall be in result['{}']".format(field))


def _check_id_in_generic_data_data(field, data_id, result):
    if type(field) is str:
        _check_generic_data_data(field, result)
        for _data in result[field]:
            if data_id not in list(_data['data'].keys()):
                raise MoonCliException(
                    "Unexpected request result. Data id {} not in {}".format(data_id, field))


def _check_id_not_in_generic_data_data(field, data_id, result):
    if type(field) is str:
        _check_generic_data_data(field, result)
        for _data in result[field]:
            if data_id in list(_data['data'].keys()):
                raise MoonCliException(
                    "Unexpected request result. Data id {} shall not be in {}".format(data_id,
                                                                                      field))


def _check_category_in_generic_data_data(field, category_id, result):
    _check_generic_data_data(field, result)
    for _data in result[field]:
        if category_id != _data["category_id"]:
            raise MoonCliException(
                "Unexpected request result. Category id {} not in {} data".format(category_id,
                                                                                  field))


def check_subject_data_data(result):
    _check_generic_data_data("subject_data", result)


def check_id_in_subject_data_data(data_id, result):
    _check_id_in_generic_data_data("subject_data", data_id, result)


def check_id_not_in_subject_data_data(data_id, result):
    _check_id_not_in_generic_data_data("subject_data", data_id, result)


def check_category_id_in_subject_data_data(category_id, result):
    _check_category_in_generic_data_data('subject_data', category_id, result)


def check_object_data_data(result):
    _check_generic_data_data("object_data", result)


def check_id_in_object_data_data(data_id, result):
    _check_id_in_generic_data_data("object_data", data_id, result)


def check_id_not_in_object_data_data(data_id, result):
    _check_id_not_in_generic_data_data("object_data", data_id, result)


def check_category_id_in_object_data_data(category_id, result):
    _check_category_in_generic_data_data('object_data', category_id, result)


def check_action_data_data(result):
    _check_generic_data_data("action_data", result)


def check_id_in_action_data_data(data_id, result):
    _check_id_in_generic_data_data("action_data", data_id, result)


def check_id_not_in_action_data_data(data_id, result):
    _check_id_not_in_generic_data_data("action_data", data_id, result)


def check_category_id_in_action_data_data(category_id, result):
    _check_category_in_generic_data_data('action_data', category_id, result)


def _check_generic_assignments(field, field_id_name, field_id, field_cat_id, field_data_id, result):
    if type(field) is str and type(field_id_name) is str:
        for key in result[field]:
            if field_id_name not in result[field][key]:
                raise MoonCliException(
                    "Unexpected request result. subject_id not in result[{}] data".format(field))
            if "category_id" not in result[field][key]:
                raise MoonCliException(
                    "Unexpected request result. category_id not in result[{}] data".format(field))
            if "assignments" not in result[field][key]:
                raise MoonCliException(
                    "Unexpected request result. assignments not in result[{}] data".format(field))
            if result[field][key][field_id_name] == field_id and \
                    result[field][key]["category_id"] == field_cat_id:
                if field_data_id not in result[field][key]["assignments"]:
                    raise MoonCliException(
                        "Unexpected request result. {} data with id {} not in result[{}][]['assignements'] data".format(
                            field, field_data_id, field))


def check_subject_assignements(subject_id, subject_act_id, subject_data_id, result):
    _check_generic_assignments("subject_assignments", "subject_id", subject_id, subject_act_id,
                               subject_data_id, result)


def check_object_assignements(object_id, object_act_id, object_data_id, result):
    _check_generic_assignments("object_assignments", "object_id", object_id, object_act_id,
                               object_data_id, result)


def check_action_assignements(action_id, action_act_id, action_data_id, result):
    _check_generic_assignments("action_assignments", "action_id", action_id, action_act_id,
                               action_data_id, result)


def _check_not_generic_assignments(field, field_id_name, field_id, field_cat_id, field_data_id,
                                   result):
    if type(field) is str and type(field_id_name) is str:
        for key in result[field]:
            if field_id_name not in result[field][key]:
                raise MoonCliException(
                    "Unexpected request result. subject_id not in result[{}] data".format(field))
            if "category_id" not in result[field][key]:
                raise MoonCliException(
                    "Unexpected request result. category_id not in result[{}] data".format(field))
            if "assignments" not in result[field][key]:
                raise MoonCliException(
                    "Unexpected request result. assignments not in result[{}] data".format(field))
            if result[field][key]['subject_id'] == field_id and \
                    result[field][key]["category_id"] == field_cat_id:
                if field_data_id in result[field][key]["assignments"]:
                    raise MoonCliException(
                        "Unexpected request result. {} data with id {} shall not be in result[{}][]['assignements'] data".format(
                            field, field_data_id, field))


def check_not_subject_assignements(subject_id, subject_act_id, subject_data_id, result):
    _check_not_generic_assignments("subject_assignments", "subject_id", subject_id, subject_act_id,
                                   subject_data_id, result)


def check_not_object_assignements(object_id, object_act_id, object_data_id, result):
    _check_not_generic_assignments("object_assignments", "object_id", object_id, object_act_id,
                                   object_data_id, result)


def check_not_action_assignements(action_id, action_act_id, action_data_id, result):
    _check_not_generic_assignments("action_assignments", "action_id", action_id, action_act_id,
                                   action_data_id, result)


def check_policy_id_in_dict(policy_id, in_dict):
    if "policy_id" not in in_dict:
        raise MoonCliException("Unexpected request result. policy_id not in result")
    if policy_id != in_dict["policy_id"]:
        raise MoonCliException(
            "Unexpected request result. Bad policy id in result, expected {}".format(policy_id))


def check_meta_rule_id_in_dict(meta_rule_id, in_dict):
    if "meta_rule_id" not in in_dict:
        raise MoonCliException("Unexpected request result. meta_rule_id not in result")
    if meta_rule_id != in_dict["meta_rule_id"]:
        raise MoonCliException(
            "Unexpected request result. Bad meta rule id in result, expected {}".format(
                meta_rule_id))


def check_rule_in_dict(rule, in_dict):
    if "rule" not in in_dict:
        raise MoonCliException("Unexpected request result. rule not in result")
    if rule != in_dict["rule"]:
        raise MoonCliException(
            "Unexpected request result. Bad rule in result, expected {}".format(rule))


def check_rule_id_in_list(meta_rule_id, rule_id, rule, in_dict):
    for item in in_dict:
        if "meta_rule_id" not in item:
            raise MoonCliException("Unexpected request result. meta_rule_id field not in result")
        if meta_rule_id == item["meta_rule_id"]:
            if rule_id == item["id"]:
                if rule != item["rule"]:
                    raise MoonCliException(
                        "Unexpected request result. Bad rule in result, expected {}".format(rule))


def check_rule_id_not_in_list(rule_id, in_dict):
    found_rule = False
    for item in in_dict:
        if rule_id == item["id"]:
            found_rule = True
    if found_rule is True:
        raise MoonCliException(
            "Unexpected request result. Rule with id {} shall not be in result".format(rule_id))
