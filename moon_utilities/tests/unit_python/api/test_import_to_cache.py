# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import helpers.import_export_cache_helper as import_export_helper
import pytest
from moon_utilities import exceptions


MODEL_WITHOUT_META_RULES = [
    {"models": [{"name": "test model", "description": "", "meta_rules": []}]},
    {"models": [{"name": "test model", "description": "new description", "meta_rules": [],
                 "override": True}]},
    {"models": [{"name": "test model", "description": "description not taken into account",
                 "meta_rules": [], "override": False}]}
]

POLICIES = [
    {"policies": [
        {"name": "test policy", "genre": "authz", "description": "description", "model": {},
         "mandatory": False}]},
    {"policies": [{"name": "test policy", "genre": "authz",
                   "description": "new description not taken into account",
                   "model": {"name": "test model"}, "mandatory": True}]},
    {"policies": [
        {"name": "test policy", "genre": "not authz ?", "description": "generates an exception",
         "model": {"name": "test model"}, "override": True}]},
    {"models": [{"name": "test model", "description": "", "meta_rules": []}], "policies": [
        {"name": "test policy", "genre": "not authz ?", "description": "changes taken into account",
         "model": {"name": "test model"}, "override": True}]},
]

SUBJECTS = [
    {"subjects": [
    {"name": "testuser", "description": "description of the subject", "extra": {},
     "policies": []}]},
    {"policies": [
        {"name": "test policy", "genre": "authz", "description": "description", "model": {},
         "mandatory": False}], "subjects": [
        {"name": "testuser", "description": "description of the subject", "extra": {},
         "policies": []}]},
    {"policies": [
        {"name": "test other policy", "genre": "authz", "description": "description",
         "model": {}, "mandatory": True}], "subjects": [
        {"name": "testuser", "description": "description of the subject", "extra": {},
         "policies": []}]},
    {"subjects": [{"name": "testuser", "description": "new description of the subject",
                   "extra": {"email": "new-email@test.com"},
                   "policies": [{"name": "test other policy"}]}]},
    {"policies": [
        {"name": "test policy", "genre": "authz", "description": "description", "model": {},
         "mandatory": False}], "subjects": [
        {"name": "testuser", "description": "description of the subject", "extra": {},
         "policies": [{"name": "test policy"}]}]}]

OBJECTS = [
    {"objects": [{"name": "test object", "description": "description of the object", "extra": {},
                  "policies": []}]},
    {"policies": [
        {"name": "test policy", "genre": "authz", "description": "description", "model": {},
         "mandatory": False}],
        "objects": [{"name": "test object", "description": "description of the object", "extra": {},
                     "policies": []}]},
    {"policies": [
        {"name": "test other policy", "genre": "authz", "description": "description", "model": {},
         "mandatory": True}],
        "objects": [{"name": "test object", "description": "description of the object", "extra": {},
                     "policies": []}]},
    {"objects": [{"name": "test object", "description": "new description of the object",
                  "extra": {"test": "test extra"},
                  "policies": [{"name": "test other policy"}]}]},
    {"policies": [
        {"name": "test policy", "genre": "authz", "description": "description", "model": {},
         "mandatory": False}],
        "objects": [{"name": "test object", "description": "description of the object", "extra": {},
                     "policies": [{"name": "test policy"}]}]},
]

ACTIONS = [
    {"actions": [
    {"name": "test action", "description": "description of the action", "extra": {},
     "policies": []}]},
    {"policies": [
        {"name": "test policy", "genre": "authz", "description": "description", "model": {},
         "mandatory": False}], "actions": [
        {"name": "test action", "description": "description of the action", "extra": {},
         "policies": []}]},
    {"policies": [
        {"name": "test other policy", "genre": "authz", "description": "description",
         "model": {}, "mandatory": True}], "actions": [
        {"name": "test action", "description": "description of the action", "extra": {},
         "policies": []}]},
    {"actions": [{"name": "test action", "description": "new description of the action",
                  "extra": {"test": "test extra"},
                  "policies": [{"name": "test other policy"}]}]},
    {"policies": [
        {"name": "test policy", "genre": "authz", "description": "description", "model": {},
         "mandatory": False}], "actions": [
        {"name": "test action", "description": "description of the action", "extra": {},
         "policies": [{"name": "test policy"}]}]}]

SUBJECT_CATEGORIES = [{"subject_categories": [
    {"name": "test subject categories", "description": "subject category description"}]},
    {"subject_categories": [{"name": "test subject categories",
                             "description": "new subject category description"}]}]

OBJECT_CATEGORIES = [{"object_categories": [
    {"name": "test object categories", "description": "object category description"}]},
    {"object_categories": [{"name": "test object categories",
                            "description": "new object category description"}]}]

ACTION_CATEGORIES = [{"action_categories": [
    {"name": "test action categories", "description": "action category description"}]},
    {"action_categories": [{"name": "test action categories",
                            "description": "new action category description"}]}]

# meta_rules import is needed otherwise the search for data do not work !!!
PRE_DATA = {"models": [
                {
                    "name": "test model", "description": "",
                    "meta_rules": [{"name": "good meta rule"},
                                   {"name": "other good meta rule"}]}],
            "policies": [
                {"name": "test other policy", "genre": "authz", "description": "description",
                 "model": {"name": "test model"}, "mandatory": True}],
            "subject_categories": [
                {"name": "test subject categories", "description": "subject category description"},
                {"name": "other test subject categories",
                 "description": "subject category description"}],
            "object_categories": [
                {"name": "test object categories", "description": "object category description"},
                {"name": "other test object categories",
                 "description": "object category description"}],
            "action_categories": [
                {"name": "test action categories", "description": "action category description"},
                {"name": "other test action categories",
                 "description": "action category description"}],
            "meta_rules": [
                {
                    "name": "good meta rule", "description": "valid meta rule",
                    "subject_categories": [{"name": "test subject categories"}],
                    "object_categories": [{"name": "test object categories"}],
                    "action_categories": [{"name": "test action categories"}]
                },
                {
                    "name": "other good meta rule", "description": "valid meta rule",
                    "subject_categories": [{"name": "other test subject categories"}],
                    "object_categories": [{"name": "other test object categories"}],
                    "action_categories": [{"name": "other test action categories"}]
                }]}

SUBJECT_DATA = [{"subject_data": [
    {"name": "not valid subject data", "description": "", "policies": [{}], "category": {}}]},
    {"subject_data": [
        {"name": "not valid subject data", "description": "", "policies": [{}],
         "category": {"name": "test subject categories"}}]},
    {"policies": [
        {"name": "test policy", "genre": "authz", "description": "description",
         "model": {"name": "test model"}, "mandatory": True}], "subject_data": [
        {"name": "one valid subject data", "description": "description",
         "policies": [{}], "category": {"name": "test subject categories"}}]},
    {"subject_data": [{"name": "valid subject data", "description": "description",
                       "policies": [{"name": "test policy"}],
                       "category": {"name": "test subject categories"}}]},
    {"subject_data": [{"name": "valid subject data", "description": "new description",
                       "policies": [{"name": "test other policy"}],
                       "category": {"name": "test subject categories"}}]}]

OBJECT_DATA = [{"object_data": [
    {"name": "not valid object data", "description": "", "policies": [{}], "category": {}}]},
    {"object_data": [
        {"name": "not valid object data", "description": "", "policies": [{}],
         "category": {"name": "test object categories"}}]},
    {"policies": [{"name": "test policy", "genre": "authz", "description": "description",
                   "model": {"name": "test model"}, "mandatory": True}], "object_data": [
        {"name": "one valid object data", "description": "description", "policies": [{}],
         "category": {"name": "test object categories"}}]},
    {"object_data": [{"name": "valid object data", "description": "description",
                      "policies": [{"name": "test policy"}],
                      "category": {"name": "test object categories"}}]},
    {"object_data": [{"name": "valid object data", "description": "new description",
                      "policies": [{"name": "test other policy"}],
                      "category": {"name": "test object categories"}}]}]

ACTION_DATA = [{"action_data": [
    {"name": "not valid action data", "description": "", "policies": [{}], "category": {}}]},
    {"action_data": [
        {"name": "not valid action data", "description": "", "policies": [{}],
         "category": {"name": "test action categories"}}]},
    {"policies": [{"name": "test policy", "genre": "authz", "description": "description",
                   "model": {"name": "test model"}, "mandatory": True}], "action_data": [
        {"name": "one valid action data", "description": "description", "policies": [{}],
         "category": {"name": "test action categories"}}]},
    {"action_data": [{"name": "valid action data", "description": "description",
                      "policies": [{"name": "test policy"}],
                      "category": {"name": "test action categories"}}]},
    {"action_data": [{"name": "valid action data", "description": "new description",
                      "policies": [{"name": "test other policy"}],
                      "category": {"name": "test action categories"}}]}]

PRE_META_RULES = {"subject_categories": [
    {"name": "test subject categories", "description": "subject category description"}],
    "object_categories": [{"name": "test object categories",
                           "description": "object category description"}],
    "action_categories": [{"name": "test action categories",
                           "description": "object action description"}]}

META_RULES = [{"meta_rules": [{"name": "bad meta rule", "description": "not valid meta rule",
                               "subject_categories": [{"name": "not valid category"}],
                               "object_categories": [{"name": "test object categories"}],
                               "action_categories": [{"name": "test action categories"}]}]},
              {"meta_rules": [{"name": "bad meta rule", "description": "not valid meta rule",
                               "subject_categories": [{"name": "test subject categories"}],
                               "object_categories": [{"name": "not valid category"}],
                               "action_categories": [{"name": "test action categories"}]}]},
              {"meta_rules": [{"name": "bad meta rule", "description": "not valid meta rule",
                               "subject_categories": [{"name": "test subject categories"}],
                               "object_categories": [{"name": "test object categories"}],
                               "action_categories": [{"name": "not valid category"}]}]},
              {"meta_rules": [{"name": "good meta rule", "description": "valid meta rule",
                               "subject_categories": [{"name": "test subject categories"}],
                               "object_categories": [{"name": "test object categories"}],
                               "action_categories": [{"name": "test action categories"}]}]}]

PRE_ASSIGNMENTS = {"models": [
    {"name": "test model", "description": "", "meta_rules": [{"name": "good meta rule"}]}],
    "policies": [
        {"name": "test policy", "genre": "authz", "description": "description",
         "model": {"name": "test model"}, "mandatory": True}],
    "subject_categories": [{"name": "test subject categories",
                            "description": "subject category description"}],
    "object_categories": [{"name": "test object categories",
                           "description": "object category description"}],
    "action_categories": [{"name": "test action categories",
                           "description": "object action description"}],
    "subjects": [{"name": "testuser", "description": "description of the subject",
                  "extra": {}, "policies": [{"name": "test policy"}]}],
    "objects": [{"name": "test object", "description": "description of the object",
                 "extra": {}, "policies": [{"name": "test policy"}]}],
    "actions": [{"name": "test action", "description": "description of the action",
                 "extra": {}, "policies": [{"name": "test policy"}]}],
    "meta_rules": [{"name": "good meta rule", "description": "valid meta rule",
                    "subject_categories": [{"name": "test subject categories"}],
                    "object_categories": [{"name": "test object categories"}],
                    "action_categories": [{"name": "test action categories"}]}],
    "subject_data": [{"name": "subject data", "description": "test subject data",
                      "policies": [{"name": "test policy"}],
                      "category": {"name": "test subject categories"}}],
    "object_data": [{"name": "object data", "description": "test object data",
                     "policies": [{"name": "test policy"}],
                     "category": {"name": "test object categories"}}],
    "action_data": [{"name": "action data", "description": "test action data",
                     "policies": [{"name": "test policy"}],
                     "category": {"name": "test action categories"}}]}

SUBJECT_ASSIGNMENTS = [
    {"subject_assignments": [
        {"subject": {"name": "unknown"},
         "category": {"name": "test subject categories"},
         "assignments": [{"name": "subject data"}]}],
        "exception": exceptions.InvalidJson
    },
    {"subject_assignments": [
        {"subject": {"name": "testuser"},
         "category": {"name": "unknown"},
         "assignments": [{"name": "subject data"}]}],
        "exception": exceptions.UnknownName
    },
    {"subject_assignments": [
        {"subject": {"name": "testuser"},
         "category": {"name": "test subject categories"},
         "assignments": [{"name": "unknown"}]}],
        "exception": exceptions.InvalidJson
    },
    {"subject_assignments": [
        {"subject": {"name": "testuser"},
         "category": {"name": "test subject categories"},
         "assignments": [{"name": "subject data"}]}],
        "exception": None
    }]

OBJECT_ASSIGNMENTS = [
    {"object_assignments": [
        {"object": {"name": "unknown"},
         "category": {"name": "test object categories"},
         "assignments": [{"name": "object data"}]}],
        "exception": exceptions.InvalidJson
    },
    {"object_assignments": [
        {"object": {"name": "test object"},
         "category": {"name": "unknown"},
         "assignments": [{"name": "object data"}]}],
        "exception": exceptions.UnknownName
    },
    {"object_assignments": [
        {"object": {"name": "test object"},
         "category": {"name": "test object categories"},
         "assignments": [{"name": "unknown"}]}],
        "exception": exceptions.InvalidJson
    },
    {"object_assignments": [
        {"object": {"name": "test object"},
         "category": {"name": "test object categories"},
         "assignments": [{"name": "object data"}]}],
        "exception": None
    }]

ACTION_ASSIGNMENTS = [
    {"action_assignments": [
        {"action": {"name": "unknown"},
         "category": {"name": "test action categories"},
         "assignments": [{"name": "action data"}]}],
        "exception": exceptions.InvalidJson
    },
    {"action_assignments": [
        {"action": {"name": "test action"},
         "category": {"name": "unknown"},
         "assignments": [{"name": "action data"}]}],
        "exception": exceptions.UnknownName
    },
    {"action_assignments": [
        {"action": {"name": "test action"},
         "category": {"name": "test action categories"},
         "assignments": [{"name": "unknown"}]}],
        "exception": exceptions.InvalidJson
    },
    {"action_assignments": [
        {"action": {"name": "test action"},
         "category": {"name": "test action categories"},
         "assignments": [{"name": "action data"}]}],
        "exception": None
    }]

RULES = [{"rules": [{"meta_rule": {"name": "unknown meta rule"}, "policy": {"name": "test "
                                                                                    "policy"},
                     "instructions": ({"decision": "grant"},), "enabled": True, "rule": {
        "subject_data": [{"name": "subject data"}], "object_data": [{"name": "object data"}],
        "action_data": [{"name": "action data"}]}}]},
         {"rules": [{"meta_rule": {"name": "good meta rule"}, "policy": {"name": "unknown "
                                                                                 "policy"},
                     "instructions": ({"decision": "grant"},), "enabled": True, "rule": {
                 "subject_data": [{"name": "subject data"}],
                 "object_data": [{"name": "object data"}],
                 "action_data": [{"name": "action data"}]}}]},
         {"rules": [{"meta_rule": {"name": "good meta rule"}, "policy": {"name": "test policy"},
                     "instructions": ({"decision": "grant"},), "enabled": True, "rule": {
                 "subject_data": [{"name": "unknown subject data"}],
                 "object_data": [{"name": "object data"}],
                 "action_data": [{"name": "action data"}]}}]},
         {"rules": [{"meta_rule": {"name": "good meta rule"}, "policy": {"name": "test policy"},
                     "instructions": ({"decision": "grant"},), "enabled": True, "rule": {
                 "subject_data": [{"name": "subject data"}],
                 "object_data": [{"name": "unknown object data"}],
                 "action_data": [{"name": "action data"}]}}]},
         {"rules": [{"meta_rule": {"name": "good meta rule"}, "policy": {"name": "test policy"},
                     "instructions": ({"decision": "grant"},), "enabled": True, "rule": {
                 "subject_data": [{"name": "subject data"}],
                 "object_data": [{"name": "object data"}],
                 "action_data": [{"name": "unknown action data"}]}}]},
         {"rules": [{"meta_rule": {"name": "good meta rule"}, "policy": {"name": "test policy"},
                     "instructions": ({"decision": "grant"},), "enabled": True, "rule": {
                 "subject_data": [{"name": "subject data"}],
                 "object_data": [{"name": "object data"}],
                 "action_data": [{"name": "action data"}]}}]}]


def test_import_models_without_new_meta_rules():
    from moon_utilities import json_utils
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    import_to_cache = json_utils.JsonImport(driver_name="cache", driver=_cache)

    import_export_helper.clean_all()
    counter = 0
    for models_description in MODEL_WITHOUT_META_RULES:
        data = import_to_cache.import_json(body=models_description)
        assert "models" in data
        models = _cache.models
        assert len(list(models.keys())) == 1
        values = list(models.values())
        assert values[0]["name"] == "test model"
        if counter == 0:
            assert len(values[0]["description"]) == 0
        if counter == 1 or counter == 2:
            assert values[0]["description"] == "new description"
        counter = counter + 1
    import_export_helper.clean_all()


def test_import_policies():
    from moon_utilities import json_utils
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    import_to_cache = json_utils.JsonImport(driver_name="cache", driver=_cache)

    counter = -1
    for policy_description in POLICIES:
        counter = counter + 1
        if counter == 2:
            with pytest.raises(exceptions.UnknownName):
                import_to_cache.import_json(body=policy_description)
            continue
        else:
            data = import_to_cache.import_json(body=policy_description)
            assert "policies" in data
            if counter == 2:
                assert "models" in data

        from moon_cache.cache import Cache
        _cache = Cache.getInstance()
        policies = _cache.policies
        assert len(list(policies.keys())) == 1
        values = list(policies.values())
        assert values[0]["name"] == "test policy"
        if counter < 3:
            assert values[0]["genre"] == "authz"
            assert values[0]["description"] == "description"
        else:
            assert values[0]["genre"] == "not authz ?"
            assert values[0]["description"] == "changes taken into account"
            assert len(values[0]["model_id"]) > 0


def test_import_subject_object_action():
    from moon_utilities import json_utils
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    import_to_cache = json_utils.JsonImport(driver_name="cache", driver=_cache)

    type_elements = ["subject", "object", "action"]

    for type_element in type_elements:
        import_export_helper.clean_all()
        counter = -1
        # set the getters and the comparison values
        if type_element == "subject":
            elements = SUBJECTS
            clean_method = import_export_helper.clean_subjects
            name = "testuser"
            key_extra = "email"
            value_extra = "new-email@test.com"
        elif type_element == "object":
            elements = OBJECTS
            clean_method = import_export_helper.clean_objects
            name = "test object"
            key_extra = "test"
            value_extra = "test extra"
        else:
            elements = ACTIONS
            clean_method = import_export_helper.clean_actions
            name = "test action"
            key_extra = "test"
            value_extra = "test extra"

        for element in elements:
            counter = counter + 1
            if counter == 2 or counter == 4:
                clean_method()
            if counter == 3:
                clean_method()
                data = import_to_cache.import_json(body=element)
            elif counter < 2:
                with pytest.raises(exceptions.PolicyUnknown) as exception_info:
                    import_to_cache.import_json(body=element)
                assert '400: Policy Unknown' == str(exception_info.value)
                continue
            else:
                data = import_to_cache.import_json(body=element)
            assert data

            if counter != 3:
                assert type_element+"s" in data
                assert "policies" in data

            get_elements = getattr(_cache, type_element + "s")

            policy_key = list(get_elements.keys())[0]
            assert len(list(get_elements[policy_key].keys())) == 1
            values = list(get_elements[policy_key].values())
            assert values[0]["name"] == name
            if counter == 2 or counter == 4:
                assert values[0]["description"] == "description of the " + type_element
            if counter == 3:
                assert values[0]["description"] == "new description of the " + type_element
                assert values[0]["extra"][key_extra] == value_extra

            assert len(values[0]["policy_list"]) == 1
    import_export_helper.clean_all()


def test_import_subject_object_action_categories():
    from moon_utilities import json_utils
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    import_to_cache = json_utils.JsonImport(driver_name="cache", driver=_cache)

    type_elements = ["subject", "object", "action"]

    for type_element in type_elements:
        import_export_helper.clean_all()
        counter = -1
        # set the getters and the comparison values
        if type_element == "subject":
            elements = SUBJECT_CATEGORIES
        elif type_element == "object":
            elements = OBJECT_CATEGORIES
        else:
            elements = ACTION_CATEGORIES

        for element in elements:
            data = import_to_cache.import_json(body=element)
            counter = counter + 1
            assert type_element + "_categories" in data
            get_elements = getattr(_cache, type_element + "_categories")
            assert len(list(get_elements.keys())) == 1
            values = list(get_elements.values())
            assert values[0]["name"] == "test " + type_element + " categories"
            assert values[0]["description"] == type_element + " category description"


def test_import_meta_rules():
    from moon_utilities import json_utils
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    import_to_cache = json_utils.JsonImport(driver_name="cache", driver=_cache)

    import_export_helper.clean_all()
    # import some categories
    data = import_to_cache.import_json(body=PRE_META_RULES)
    for cat in ['subject_categories', 'object_categories', 'action_categories']:
        assert cat in data

    counter = -1
    for meta_rule in META_RULES:
        counter = counter + 1
        if counter != 3:
            with pytest.raises(exceptions.UnknownName) as exception_info:
                import_to_cache.import_json(body=meta_rule)
            assert '400: Unknown Name.' == str(exception_info.value)
            continue
        else:
            data = import_to_cache.import_json(body=meta_rule)
            assert "meta_rules" in data
            assert _cache.meta_rules

            meta_rules = _cache.meta_rules
            key = list(meta_rules.keys())[0]
            assert isinstance(meta_rules, dict)
            assert meta_rules[key]["name"] == "good meta rule"
            assert meta_rules[key]["description"] == "valid meta rule"
            assert len(meta_rules[key]["subject_categories"]) == 1
            assert len(meta_rules[key]["object_categories"]) == 1
            assert len(meta_rules[key]["action_categories"]) == 1

            subject_category_key = meta_rules[key]["subject_categories"][0]
            object_category_key = meta_rules[key]["object_categories"][0]
            action_category_key = meta_rules[key]["action_categories"][0]

            sub_cat = _cache.subject_categories
            assert sub_cat[subject_category_key]["name"] == "test subject categories"

            ob_cat = _cache.object_categories
            assert ob_cat[object_category_key]["name"] == "test object categories"

            ac_cat = _cache.action_categories
            assert ac_cat[action_category_key]["name"] == "test action categories"

    import_export_helper.clean_all()


def test_import_subject_object_action_assignments():
    from moon_utilities import json_utils
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    import_to_cache = json_utils.JsonImport(driver_name="cache", driver=_cache)

    import_export_helper.clean_all()

    data = import_to_cache.import_json(body=PRE_ASSIGNMENTS)
    for item in PRE_ASSIGNMENTS.keys():
        assert item in data

    type_elements = ["subject", "object", "action"]

    for type_element in type_elements:
        counter = -1
        if type_element == "subject":
            datas = SUBJECT_ASSIGNMENTS
        elif type_element == "object":
            datas = OBJECT_ASSIGNMENTS
        else:
            datas = ACTION_ASSIGNMENTS

        for assignments in datas:
            counter = counter + 1
            my_exception = assignments.pop("exception")
            if my_exception:
                with pytest.raises(my_exception) as exception_info:
                    import_to_cache.import_json(body=assignments)
                assert '400:' in str(exception_info.value)
            else:
                data = import_to_cache.import_json(body=assignments)
                assert type_element+"_assignments" in data
                assert getattr(_cache, type_element+"_assignments")

                assert len(getattr(_cache, type_element+"_assignments")) == 1


def test_import_rules():
    from moon_utilities import json_utils
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    import_to_cache = json_utils.JsonImport(driver_name="cache", driver=_cache)

    import_export_helper.clean_all()

    data = import_to_cache.import_json(body=PRE_ASSIGNMENTS)
    for item in PRE_ASSIGNMENTS.keys():
        assert item in data

    counter = -1
    for rule in RULES:
        counter = counter + 1
        if counter < 5:
            with pytest.raises(exceptions.UnknownName) as exception_info:
                import_to_cache.import_json(body=rule)

            assert '400: Unknown Name.' == str(exception_info.value)
            continue
        data = import_to_cache.import_json(body=rule)
        assert "rules" in data
        policies = _cache.policies
        policy_id = None
        for policy in policies:
            if policies[policy]['name'] == rule['rules'][0]['policy']['name']:
                policy_id = policy
                break

        assert policy_id
        rules = _cache.rules
        assert len(rules) == 1
        rule_content = list(rules.values())[0]
        assert policy_id == rule_content["policy_id"]
        assert rule_content["rules"]
        assert len(rule_content["rules"]) == 1
        assert rule_content["rules"][0]["enabled"]
        assert rule_content["rules"][0]["instructions"][0]["decision"] == "grant"

        meta_rules = _cache.meta_rules
        assert meta_rules[list(meta_rules.keys())[0]]["name"] == "good meta rule"


def test_import_subject_object_action_data():
    from moon_utilities import json_utils
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    import_to_cache = json_utils.JsonImport(driver_name="cache", driver=_cache)

    type_elements = ["subject", "object", "action"]

    for type_element in type_elements:
        import_export_helper.clean_all()
        data = import_to_cache.import_json(body=PRE_DATA)
        for key in PRE_DATA.keys():
            assert key in data
        counter = -1
        if type_element == "subject":
            elements = SUBJECT_DATA
            get_method = _cache.subject_data
            get_categories = _cache.subject_categories
        elif type_element == "object":
            elements = OBJECT_DATA
            get_method = _cache.object_data
            get_categories = _cache.object_categories
        else:
            elements = ACTION_DATA
            get_method = _cache.action_data
            get_categories = _cache.action_categories

        for element in elements:
            counter = counter + 1
            if counter == 0 or counter == 1:
                with pytest.raises(exceptions.MissingIdOrName) as exception_info:
                    import_to_cache.import_json(body=element)
                assert '400: Missing ID or Name.' == str(exception_info.value)
                continue
            else:
                data = import_to_cache.import_json(body=element)
            for key in element.keys():
                assert key in data

            policies = _cache.policies
            categories = get_categories
            case_tested = False
            for policy_key in policies.keys():
                policy = policies[policy_key]
                for category_key in categories:
                    get_elements = get_method
                    _all_data = []
                    for _data in get_elements:
                        if category_key == _data["category_id"] and policy_key == _data["policy_id"]:
                            _all_data.append(_data)
                    get_elements = _all_data
                    if not get_elements:
                        continue
                    if policy["name"] == "test policy":
                        assert len(get_elements) == 1
                        el = get_elements[0]
                        assert isinstance(el["data"], dict)
                        if counter == 2:
                            assert len(el["data"].keys()) == 1
                            el = el["data"][list(el["data"].keys())[0]]
                            if "value" in el:
                                el = el["value"]
                            assert el["name"] == "one valid " + type_element + " data"
                        if counter == 3:
                            assert len(el["data"].keys()) == 2
                            el1 = el["data"][list(el["data"].keys())[0]]
                            el2 = el["data"][list(el["data"].keys())[1]]
                            if "value" in el1:
                                el1 = el1["value"]
                                el2 = el2["value"]
                            assert (el1["name"] == "one valid " + type_element + " data" and el2[
                                "name"] == "valid " + type_element + " data") or (el2[
                                                                                      "name"] == "one valid " + type_element + " data" and
                                                                                  el1[
                                                                                      "name"] == "valid " + type_element + " data")
                            assert el1["description"] == "description"
                            assert el2["description"] == "description"

                        case_tested = True

                    if policy["name"] == "test other policy":
                        if counter == 4:
                            assert len(get_elements) == 1
                            el = get_elements[0]
                            assert isinstance(el["data"], dict)
                            assert len(el["data"].keys()) == 1
                            el = el["data"][list(el["data"].keys())[0]]
                            if "value" in el:
                                el = el["value"]
                            assert el["name"] == "valid " + type_element + " data"
                            assert el["description"] == "new description"
                            case_tested = True

            assert case_tested is True


def test_clean():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    import_export_helper.clean_all()
    assert not _cache.subject_categories
    assert not _cache.object_categories
    assert not _cache.action_categories
    assert not _cache.subjects
    assert not _cache.objects
    assert not _cache.actions
    assert not _cache.subject_data
    assert not _cache.object_data
    assert not _cache.action_data
    assert not _cache.subject_assignments
    assert not _cache.object_assignments
    assert not _cache.action_assignments
    assert not _cache.models
    assert not _cache.pdp
    assert not _cache.policies
