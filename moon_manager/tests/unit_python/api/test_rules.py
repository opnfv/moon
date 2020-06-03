# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import pytest
from moon_utilities import exceptions
import json
from helpers import data_builder as builder
from helpers import policy_helper
from helpers import rules_helper
import hug


def get_rules(policy_id):
    from moon_manager.api import rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(rules, "/policies/{}/rules".format(policy_id), headers=auth_headers)
    rules = req.data
    return req, rules


def add_rules_without_policy_id(headers):
    from moon_manager.api import rules
    subject_category_id, object_category_id, action_category_id, meta_rule_id = builder.create_new_meta_rule()
    data = {
        "meta_rule_id": meta_rule_id,
        "rule": [subject_category_id, object_category_id, action_category_id],
        "instructions": [
            {"decision": "grant"},
        ],
        "enabled": True
    }
    headers['Content-Type'] = 'application/json'
    req = hug.test.post(rules, "/policies/{}/rules".format(None), body=json.dumps(data),
                        headers=headers)
    rules = req.data
    return req, rules


def add_rules_without_meta_rule_id(policy_id, headers):
    from moon_manager.api import rules
    data = {
        "meta_rule_id": "",
        "rule": ["subject_data_id2", "object_data_id2", "action_data_id2"],
        "instructions": [
            {"decision": "grant"},
        ],
        "enabled": True
    }
    headers['Content-Type'] = 'application/json'
    req = hug.test.post(rules, "/policies/{}/rules".format(policy_id), body=json.dumps(data),
                        headers=headers)
    rules = req.data
    return req, rules


def add_rules_without_rule(policy_id, headers):
    from moon_manager.api import rules
    data = {
        "meta_rule_id": "meta_rule_id1",
        "instructions": [
            {"decision": "grant"},
        ],
        "enabled": True
    }
    headers['Content-Type'] = 'application/json'
    req = hug.test.post(rules, "/policies/{}/rules".format(policy_id), body=json.dumps(data),
                        headers=headers)
    rules = req.data
    return req, rules


def delete_rules(policy_id, meta_rule_id, headers):
    from moon_manager.api import rules
    req = hug.test.delete(rules, "/policies/{}/rules/{}".format(policy_id, meta_rule_id),
                          headers=headers)
    return req


def update_rule(policy_id, rule_id, instructions, headers):
    from moon_manager.api import rules
    req = hug.test.patch(rules, "/policies/{}/rules/{}".format(policy_id, rule_id),
                         headers=headers,
                         body=instructions)
    return req


def test_add_rules_with_invalid_decision_instructions():
    from moon_manager.api import rules

    auth_headers = rules_helper.get_headers()
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy()

    data = {
        "meta_rule_id": meta_rule_id,
        "rule": [subject_category_id, object_category_id, action_category_id],
        "instructions": [
            {"decision": "invalid"},
        ],
        "enabled": True
    }

    with pytest.raises(exceptions.RuleContentError) as exception_info:
        hug.test.post(rules, "/policies/{}/rules".format(policy_id), body=json.dumps(data),
                      headers=auth_headers)
    assert "400: Rule Error" == str(exception_info.value)


def test_add_rules_with_meta_rule_not_linked_with_policy_model():
    from moon_manager.api import rules

    auth_headers = rules_helper.get_headers()
    policy_id = builder.create_new_policy()[-1]
    meta_rule_id = builder.create_new_meta_rule()[-1]

    data = {
        "meta_rule_id": meta_rule_id,
        "rule": ["subject_data_id2", "object_data_id2", "action_data_id2"],
        "instructions": [
            {"decision": "grant"},
        ],
        "enabled": True
    }

    with pytest.raises(exceptions.MetaRuleNotLinkedWithPolicyModel) as exception_info:
        hug.test.post(rules, "/policies/{}/rules".format(policy_id), body=json.dumps(data),
                      headers=auth_headers)
    assert "400: MetaRule Not Linked With Model - Policy" == str(exception_info.value)


def test_add_rules_with_invalid_rule():
    from moon_manager.api import rules

    auth_headers = rules_helper.get_headers()

    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy()
    sub_data_id = builder.create_subject_data(policy_id, subject_category_id)
    obj_data_id = builder.create_object_data(policy_id, object_category_id)
    act_data_id = builder.create_action_data(policy_id, action_category_id)

    data = {
        "meta_rule_id": meta_rule_id,
        "rule": [obj_data_id, sub_data_id, act_data_id],
        "instructions": [
            {"decision": "grant"},
        ],
        "enabled": True
    }

    with pytest.raises(exceptions.RuleContentError) as exception_info:
        hug.test.post(rules, "/policies/{}/rules".format(policy_id), body=json.dumps(data),
                      headers=auth_headers)
    assert "400: Rule Error" == str(exception_info.value)


def test_add_rules_with_no_given_decision_instructions(policy_id=None):
    from moon_manager.api import rules

    auth_headers = rules_helper.get_headers()
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy()
    sub_data_id = builder.create_subject_data(policy_id, subject_category_id)
    obj_data_id = builder.create_object_data(policy_id, object_category_id)
    act_data_id = builder.create_action_data(policy_id, action_category_id)

    data = {
        "meta_rule_id": meta_rule_id,
        "rule": [sub_data_id, obj_data_id, act_data_id],
        "instructions": [],
        "enabled": True
    }

    req = hug.test.post(rules, "/policies/{}/rules".format(policy_id), body=json.dumps(data),
                        headers=auth_headers)

    assert req.status == hug.HTTP_200

    default_instruction = {"decision": "grant"}
    rules = req.data['rules']
    rule_id = next(iter(req.data['rules']))
    assert rules[rule_id]["instructions"][0] == default_instruction


def test_get_rules(policy_id=None):
    if policy_id == None:
        policy = policy_helper.add_policies()
        policy_id = next(iter(policy))

    req, rules = get_rules(policy_id)
    assert req.status == hug.HTTP_200
    assert isinstance(rules, dict)
    assert "rules" in rules
    return req, rules


def test_add_rules():
    req, rules, policy = builder.add_rules()
    assert req.status == hug.HTTP_200


def test_add_rules_without_policy_id():
    from moon_manager.api import rules

    subject_category_id, object_category_id, action_category_id, meta_rule_id = builder.create_new_meta_rule()
    data = {
        "meta_rule_id": meta_rule_id,
        "rule": [subject_category_id, object_category_id, action_category_id],
        "instructions": [
            {"decision": "grant"},
        ],
        "enabled": True
    }

    headers = rules_helper.get_headers()
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        req = hug.test.post(rules, "/policies/{}/rules".format(None), body=json.dumps(data),
                            headers=headers)
    assert "400: Policy Unknown" == str(exception_info.value)
    # assert req.status == hug.HTTP_400
    # assert req.data["message"] == "400: Policy Unknown"


#
# def test_add_rules_without_meta_rule_id():
#     policy_id = utilities.get_policy_id()
#     client = utilities.register_client()
#     req, rules = add_rules_without_meta_rule_id(client, policy_id)
#     assert req.status == 400
#     assert json.loads(req.data)["message"] == "Key: 'meta_rule_id', [Empty String]"


def test_add_rules_without_rule():
    from moon_utilities.auth_functions import get_api_key_for_user
    policy = policy_helper.add_policies()
    policy_id = next(iter(policy))
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    with pytest.raises(exceptions.ValidationKeyError) as exception_info:
        req, rules = add_rules_without_rule(policy_id, headers=auth_headers)
    assert "Invalid Key :rule not found" == str(exception_info.value)
    # assert req.status == hug.HTTP_400
    # assert req.data["message"] == 'Invalid Key :rule not found'


def test_update_rule_without_body():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req, rules, policy_id = builder.add_rules()
    rule_id = list(rules['rules'].keys())[0]

    req = update_rule(policy_id, rule_id, instructions=None, headers=auth_headers)

    assert req.status == hug.HTTP_400


def test_update_rule_without_instructions_in_body():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    data = {"instruction": [   # faute de frappe
        {"decision": "deny"},
    ]}

    req, rules, policy_id = builder.add_rules()
    rule_id = list(rules['rules'].keys())[0]

    req = update_rule(policy_id, rule_id, instructions=None, headers=auth_headers)

    assert req.status == hug.HTTP_400


def test_update_rule():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req, rules, policy_id = builder.add_rules()
    rule_id = list(rules['rules'].keys())[0]

    data = {"instructions": [
        {"decision": "deny"},
    ]}
    req = update_rule(policy_id, rule_id, data, headers=auth_headers)

    rules = get_rules(policy_id)[1]['rules']['rules']

    rule = None
    for rule_ in rules:
        if rule_['id'] == rule_id:
            rule = rule_
            break

    assert req.status == hug.HTTP_200 and rule['instructions'][0]['decision'] == "deny"


def test_delete_rules_with_invalid_parameters():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = delete_rules("", "", headers=auth_headers)
    assert req.status == hug.HTTP_405


def test_delete_rules_without_policy_id():
    from moon_manager.api import rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy()
    sub_data_id = builder.create_subject_data(policy_id, subject_category_id)
    obj_data_id = builder.create_object_data(policy_id, object_category_id)
    act_data_id = builder.create_action_data(policy_id, action_category_id)
    data = {
        "meta_rule_id": meta_rule_id,
        "rule": [sub_data_id, obj_data_id, act_data_id],
        "instructions": [
            {"decision": "grant"},
        ],
        "enabled": True
    }
    hug.test.post(rules, "/policies/{}/rules".format(policy_id), body=json.dumps(data),
                  headers={'Content-Type': 'application/json',
                           "X-Api-Key": get_api_key_for_user("admin")})
    req, added_rules = get_rules(policy_id)
    id = list(added_rules["rules"]["rules"])[0]["id"]
    rules = delete_rules(None, id, headers=auth_headers)
    assert rules.status == hug.HTTP_200
