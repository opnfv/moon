# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import json
import api.utilities as utilities
import helpers.import_export_helper as import_export_helper
import hug

MODEL_WITHOUT_META_RULES = {"models": [{"name": "test model", "description": "model description", "meta_rules": []}]}

DATA = {"subject_data": [{"name": "test subject data", "description": "subject data description", "policies": [{"name": "test policy"}], "category": {"name": "test subject categories"}}],
        "object_data": [{"name": "test object data", "description": "object data description", "policies": [{"name": "test policy"}], "category": {"name": "test object categories"}}],
        "action_data": [{"name": "test action data", "description": "action data description", "policies": [{"name": "test policy"}], "category": {"name": "test action categories"}}]
                                      }

META_RULES = {"subject_categories": [{"name": "test subject categories", "description": "subject category description"}],
              "object_categories": [{"name": "test object categories", "description": "object category description"}],
              "action_categories": [{"name": "test action categories", "description": "action action description"}],
              "meta_rules": [{"name": "meta rule", "description": "valid meta rule", "subject_categories": [{"name": "test subject categories"}], "object_categories": [{"name": "test object categories"}], "action_categories": [{"name": "test action categories"}]}]}


SUBJECTS_OBJECTS_ACTIONS = {"models": [{"name": "test model", "description": "", "meta_rules": [{"name":"meta rule"}]}],
                            "policies": [{"name": "test policy", "genre": "authz", "description": "policy description", "model": {"name" : "test model"}}],
                            "subjects": [{"name": "testuser", "description": "description of the subject", "extra": {"field_extra_subject": "value extra subject"}, "policies": [{"name": "test policy"}]}],
                            "objects": [{"name": "test object", "description": "description of the object", "extra": {"field_extra_object": "value extra object"}, "policies": [{"name": "test policy"}]}],
                            "actions": [{"name": "test action", "description": "description of the action", "extra": {"field_extra_action": "value extra action"}, "policies": [{"name": "test policy"}]}],
                            **META_RULES
                    }

SUBJECT_OBJECT_ACTION_CATEGORIES = {"subject_categories": [{"name": "test subject categories", "description": "subject category description"}],
                                    "object_categories": [{"name": "test object categories", "description": "object category description"}],
                                    "action_categories": [{"name": "test action categories", "description": "action category description"}]}

SUBJECT_OBJECT_ACTION_DATA = {**SUBJECTS_OBJECTS_ACTIONS,
                              **DATA
                              }
POLICIES = {"models": [{"name": "test model", "description": "", "meta_rules": [{"name": "meta rule"}]}],
            "policies": [{"name": "test policy", "genre": "authz", "description": "policy description", "model": {"name" : "test model"}}],
            **META_RULES,
        }

ASSIGNMENTS = {**POLICIES,
               **DATA,
               "subjects": [{"name": "testuser", "description": "description of the subject", "extra": {"field_extra_subject": "value extra subject"}, "policies": [{"name": "test policy"}]}],
               "objects": [{"name": "test object e0", "description": "description of the object", "extra": {"field_extra_object": "value extra object"}, "policies": [{"name": "test policy"}]}],
               "actions": [{"name": "test action e0", "description": "description of the action", "extra": {"field_extra_action": "value extra action"}, "policies": [{"name": "test policy"}]}],
               "subject_assignments": [{"subject": {"name": "testuser"}, "category": {"name": "test subject categories"}, "assignments": [{"name": "test subject data"}]}],
               "object_assignments": [{"object": {"name": "test object e0"}, "category": {"name": "test object categories"}, "assignments": [{"name": "test object data"}]}],
               "action_assignments": [{"action": {"name": "test action e0"}, "category": {"name": "test action categories"}, "assignments": [{"name": "test action data"}]}]}

RULES = {**POLICIES,
         **DATA,
         "subjects": [{"name": "testuser", "description": "description of the subject", "extra": {"field_extra_subject": "value extra subject"}, "policies": [{"name": "test policy"}]}],
         "objects": [{"name": "test object e1", "description": "description of the object", "extra": {"field_extra_object": "value extra object"}, "policies": [{"name": "test policy"}]}],
         "actions": [{"name": "test action e1", "description": "description of the action", "extra": {"field_extra_action": "value extra action"}, "policies": [{"name": "test policy"}]}],
         "subject_assignments": [{"subject": {"name": "testuser"}, "category": {"name": "test subject categories"}, "assignments": [{"name": "test subject data"}]}],
         "object_assignments": [{"object": {"name": "test object e1"}, "category": {"name": "test object categories"}, "assignments": [{"name": "test object data"}]}],
         "action_assignments": [{"action": {"name": "test action e1"}, "category": {"name": "test action categories"}, "assignments": [{"name": "test action data"}]}],
         "rules": [{"meta_rule": {"name": "meta rule"}, "rule": {"subject_data": [{"name": "test "
                                                                                           "subject data"}],
                                                                 "object_data": [{"name": "test object data"}],
                                                                 "action_data": [{"name": "test action data"}]}, "policy": {"name":"test policy"}, "instructions": [{"decision": "grant"}], "enabled": True}]
        }


def test_export_models():
    from moon_manager.api import json_import
    from moon_manager.api import json_export
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    # import_export_helper.clean_all()

    req = hug.test.post(json_import, "/import", body=json.dumps(
        MODEL_WITHOUT_META_RULES), headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")} )
    data = utilities.get_json(req.data)
    assert all(e in data for e in MODEL_WITHOUT_META_RULES.keys())

    req = hug.test.get(json_export, "/export", headers=auth_headers)
    assert req.status == hug.HTTP_200
    data = utilities.get_json(req.data)

    assert "content" in data
    assert "models" in data["content"]
    assert isinstance(data["content"]["models"], list)
    assert len(data["content"]["models"]) == 1
    model = data["content"]["models"][0]
    assert model["name"] == "test model"
    assert model["description"] == "model description"
    assert isinstance(model["meta_rules"], list)
    assert len(model["meta_rules"]) == 0


def test_export_policies():
    from moon_manager.api import json_import
    from moon_manager.api import json_export
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    import_export_helper.clean_all()
    req = hug.test.post(json_import, "/import", body=json.dumps(
        POLICIES), headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")})
    data = utilities.get_json(req.data)
    assert all(e in data for e in POLICIES.keys())

    req = hug.test.get(json_export, "/export", headers=auth_headers)
    assert req.status == hug.HTTP_200
    data = utilities.get_json(req.data)

    assert "content" in data
    assert "policies" in data["content"]
    assert isinstance(data["content"]["policies"], list)
    assert len(data["content"]["policies"]) == 1
    policy = data["content"]["policies"][0]
    assert policy["name"] == "test policy"
    assert policy["genre"] == "authz"
    assert policy["description"] == "policy description"
    assert "model" in policy
    assert "name" in policy["model"]
    model = policy["model"]
    assert model["name"] == "test model"


def test_export_subject_object_action():
    from moon_manager.api import json_import
    from moon_manager.api import json_export
    from moon_utilities.auth_functions import get_api_key_for_user

    import_export_helper.clean_all()
    req = hug.test.post(json_import, "/import", body=json.dumps(
        SUBJECTS_OBJECTS_ACTIONS) ,headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")})
    data = utilities.get_json(req.data)
    assert all(e in data for e in SUBJECTS_OBJECTS_ACTIONS.keys())

    req = hug.test.get(json_export, "/export", headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")})
    assert req.status == hug.HTTP_200
    data = utilities.get_json(req.data)

    assert "content" in data
    type_elements = ["subject", "object", "action"]
    for type_element in type_elements:
        key = type_element + "s"
        assert key in data["content"]
        assert isinstance(data["content"][key], list)
        assert len(data["content"][key]) == 1
        element = data["content"][key][0]
        if type_element == "subject":
            assert element["name"] == "testuser"
        else:
            assert element["name"] == "test "+ type_element
        assert element["description"] == "description of the " + type_element
        assert "policies" in element
        assert isinstance(element["policies"], list)
        assert len(element["policies"]) == 1
        assert isinstance(element["policies"][0], dict)
        assert element["policies"][0]["name"] == "test policy"
        assert isinstance(element["extra"], dict)
        key_dict = "field_extra_" + type_element
        value_dict = "value extra " + type_element
        assert key_dict in element["extra"]
        assert element["extra"][key_dict] == value_dict


def test_export_subject_object_action_categories():
    from moon_manager.api import json_import
    from moon_manager.api import json_export
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    import_export_helper.clean_all()
    req = hug.test.post(json_import, "/import", body=json.dumps(
        SUBJECT_OBJECT_ACTION_CATEGORIES), headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")})
    data = utilities.get_json(req.data)
    assert all(e in data for e in SUBJECT_OBJECT_ACTION_CATEGORIES.keys())

    req = hug.test.get(json_export, "/export", headers=auth_headers)
    assert req.status == hug.HTTP_200
    data = utilities.get_json(req.data)
    assert "content" in data
    type_elements = ["subject", "object", "action"]
    for type_element in type_elements:
        key = type_element + "_categories"
        assert key in data["content"]
        assert isinstance(data["content"][key], list)
        assert len(data["content"][key]) == 1
        category = data["content"][key][0]
        assert category["name"] == "test " + type_element + " categories"
        assert category["description"] == type_element + " category description"


def test_export_subject_object_action_data():
    from moon_manager.api import json_import
    from moon_manager.api import json_export
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    import_export_helper.clean_all()
    req = hug.test.post(json_import, "/import", body=json.dumps(
        SUBJECT_OBJECT_ACTION_DATA), headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")})
    data = utilities.get_json(req.data)
    assert all(e in data for e in SUBJECT_OBJECT_ACTION_DATA.keys())

    req = hug.test.get(json_export, "/export", headers=auth_headers)
    assert req.status == hug.HTTP_200
    data = utilities.get_json(req.data)
    assert "content" in data
    type_elements = ["subject", "object", "action"]
    for type_element in type_elements:
        key = type_element + "_data"
        assert key in data["content"]
        assert isinstance(data["content"][key], list)
        assert len(data["content"][key]) == 1
        data_elt = data["content"][key][0]
        assert data_elt["name"] == "test " + type_element + " data"
        assert data_elt["description"] == type_element + " data description"
        assert isinstance(data_elt["policy"], dict)
        assert data_elt["policy"]["name"] == "test policy"
        assert isinstance(data_elt["category"], dict)
        assert data_elt["category"]["name"] == "test " + type_element + " categories"


def test_export_assignments():
    from moon_manager.api import json_import
    from moon_manager.api import json_export
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    import_export_helper.clean_all()
    req = hug.test.post(json_import, "/import", body=json.dumps(
        ASSIGNMENTS), headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")})
    data = utilities.get_json(req.data)
    assert all(e in data for e in ASSIGNMENTS.keys())

    req = hug.test.get(json_export, "/export", headers=auth_headers)
    assert req.status == hug.HTTP_200
    data = utilities.get_json(req.data)
    assert "content" in data
    type_elements = ["subject", "object", "action"]
    for type_element in type_elements:
        key = type_element + "_assignments"
        assert key in data["content"]
        assert isinstance(data["content"][key], list)
        assert len(data["content"][key]) == 1
        assignment_elt = data["content"][key][0]
        assert type_element in assignment_elt
        assert isinstance(assignment_elt[type_element], dict)
        if type_element == "subject":
            assert assignment_elt[type_element]["name"] == "testuser"
        else:
            assert assignment_elt[type_element]["name"] == "test " + type_element + " e0"
        assert "category" in assignment_elt
        assert isinstance(assignment_elt["category"], dict)
        assert assignment_elt["category"]["name"] == "test " + type_element + " categories"
        assert "assignments" in assignment_elt
        assert isinstance(assignment_elt["assignments"], list)
        assert len(assignment_elt["assignments"]) == 1
        assert assignment_elt["assignments"][0]["name"] == "test " + type_element + " data"

    import_export_helper.clean_all()


def test_export_rules():
    from moon_manager.api import json_import
    from moon_manager.api import json_export
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    import_export_helper.clean_all()
    req = hug.test.post(json_import, "/import", body=json.dumps(
        RULES), headers={'Content-Type': 'application/json', "X-Api-Key":
                get_api_key_for_user("admin")})
    data = utilities.get_json(req.data)
    assert all(e in data for e in RULES.keys())

    req = hug.test.get(json_export, "/export", headers=auth_headers)
    assert req.status == hug.HTTP_200
    data = utilities.get_json(req.data)
    assert "content" in data
    assert "rules" in data["content"]
    assert isinstance(data["content"]["rules"], list)
    assert len(data["content"]["rules"]) == 1
    rule = data["content"]["rules"][0]
    assert "instructions" in rule
    assert "decision" in rule["instructions"][0]
    assert rule["instructions"][0]["decision"] == "grant"
    assert "enabled" in rule
    assert rule["enabled"]
    assert "meta_rule" in rule
    assert rule["meta_rule"]["name"] == "meta rule"
    assert "policy" in rule
    assert rule["policy"]["name"] == "test policy"
    assert "rule" in rule
    rule = rule["rule"]
    assert "subject_data" in rule
    assert isinstance(rule["subject_data"], list)
    assert len(rule["subject_data"]) == 1
    assert rule["subject_data"][0]["name"] == "test subject data"
    assert "object_data" in rule
    assert isinstance(rule["object_data"], list)
    assert len(rule["object_data"]) == 1
    assert rule["object_data"][0]["name"] == "test object data"
    assert "action_data" in rule
    assert isinstance(rule["action_data"], list)
    assert len(rule["action_data"]) == 1
    assert rule["action_data"][0]["name"] == "test action data"
