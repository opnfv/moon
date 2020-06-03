# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
import api.utilities as utilities
from helpers import category_helper
from helpers import data_builder
from helpers import policy_helper
from helpers import model_helper
from helpers import meta_rule_helper
from uuid import uuid4
import pytest
from moon_utilities import exceptions


def get_meta_rules():
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(meta_rules, "/meta_rules", headers=auth_headers)
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def add_meta_rules(name, data=None):
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    if not data:
        subject_category = category_helper.add_subject_category(
            value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
        subject_category_id = list(subject_category.keys())[0]
        object_category = category_helper.add_object_category(
            value={"name": "object category name" + uuid4().hex, "description": "description 1"})
        object_category_id = list(object_category.keys())[0]
        action_category = category_helper.add_action_category(
            value={"name": "action category name" + uuid4().hex, "description": "description 1"})
        action_category_id = list(action_category.keys())[0]

        data = {
            "name": name,
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }
    req = hug.test.post(meta_rules, "/meta_rules", body=data,
                        headers=auth_headers)
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def add_meta_rules_without_category_ids(name):
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    data = {
        "name": name + uuid4().hex,
        "subject_categories": [],
        "object_categories": [],
        "action_categories": []
    }
    req = hug.test.post(meta_rules, "/meta_rules", body=data,
                        headers=auth_headers)
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def update_meta_rules(name, metaRuleId, data=None):
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    if not data:
        subject_category = category_helper.add_subject_category(
            value={"name": "subject category name update" + uuid4().hex,
                   "description": "description 1"})
        subject_category_id = list(subject_category.keys())[0]
        object_category = category_helper.add_object_category(
            value={"name": "object category name update" + uuid4().hex,
                   "description": "description 1"})
        object_category_id = list(object_category.keys())[0]
        action_category = category_helper.add_action_category(
            value={"name": "action category name update" + uuid4().hex,
                   "description": "description 1"})
        action_category_id = list(action_category.keys())[0]
        data = {
            "name": name,
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }

    req = hug.test.patch(meta_rules, "/meta_rules/{}".format(metaRuleId), body=data,
                         headers=auth_headers)
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def update_meta_rules_with_categories(name, data=None, meta_rule_id=None):
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    if not meta_rule_id:
        subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
        data = {
            "name": name,
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }

    req = hug.test.patch(meta_rules, "/meta_rules/{}".format(meta_rule_id), body=data,
                         headers=auth_headers)
    meta_rules = utilities.get_json(req.data)
    return req, meta_rules


def delete_meta_rules(name):
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    request, meta_rules_data = get_meta_rules()
    for key, value in meta_rules_data['meta_rules'].items():
        if value['name'] == name:
            return hug.test.delete(meta_rules, "/meta_rules/{}".format(key), headers=auth_headers)


def delete_meta_rules_without_id():
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.delete(meta_rules, "/meta_rules/{}".format(""), headers=auth_headers)
    return req


def test_get_meta_rules():
    req, meta_rules = get_meta_rules()
    assert req.status == hug.HTTP_200
    assert isinstance(meta_rules, dict)
    assert "meta_rules" in meta_rules


def test_add_meta_rules():
    meta_rule_name = uuid4().hex
    req, meta_rules = add_meta_rules(meta_rule_name)
    assert req.status == hug.HTTP_200
    assert isinstance(meta_rules, dict)
    value = list(meta_rules["meta_rules"].values())[0]
    assert "meta_rules" in meta_rules
    assert value['name'] == meta_rule_name


def test_add_meta_rules_space_name():
    with pytest.raises(exceptions.MetaRuleContentError) as exception_info:
        req, meta_rules = add_meta_rules("  ")
    assert "400: Meta Rule Error" == str(exception_info.value)
    # assert req.status == hug.HTTP_400
    # assert req.data["message"] == '400: Meta Rule Error'


def test_add_meta_rules_empty_name():
    with pytest.raises(exceptions.MetaRuleContentError) as exception_info:
        req, meta_rules = add_meta_rules("")
    assert "400: Meta Rule Error" == str(exception_info.value)
    # assert req.status == hug.HTTP_400
    # assert req.data["message"] == '400: Meta Rule Error'


def test_add_two_meta_rules_with_same_categories_combination():
    meta_rule_name = uuid4().hex
    req, meta_rules = add_meta_rules(meta_rule_name)
    data = None
    assert req.status == hug.HTTP_200
    for meta_rule_id in meta_rules['meta_rules']:
        if meta_rules['meta_rules'][meta_rule_id]['name'] == meta_rule_name:
            data = meta_rules['meta_rules'][meta_rule_id]

    assert data
    data['name'] = uuid4().hex
    with pytest.raises(exceptions.MetaRuleExisting) as exception_info:
        req, meta_rules = add_meta_rules(name=data['name'], data=data)
    assert "409: Meta Rule Existing" == str(exception_info.value)
    # assert req.status == hug.HTTP_409
    # assert req.data["message"] == '409: Meta Rule Existing'


def test_add_three_meta_rules_with_different_combination_but_similar_items():
    meta_rule_name1 = uuid4().hex
    req, meta_rules = add_meta_rules(meta_rule_name1)
    assert req.status == hug.HTTP_200
    for meta_rule_id in meta_rules['meta_rules']:
        if meta_rules['meta_rules'][meta_rule_id]['name'] == meta_rule_name1:
            data = meta_rules['meta_rules'][meta_rule_id]
            break

    meta_rule_name2 = uuid4().hex

    req, meta_rules = add_meta_rules(meta_rule_name2)

    for meta_rule_id in meta_rules['meta_rules']:
        if meta_rules['meta_rules'][meta_rule_id]['name'] == meta_rule_name2:
            data['subject_categories'] += meta_rules['meta_rules'][meta_rule_id][
                'subject_categories']
            data['object_categories'] += meta_rules['meta_rules'][meta_rule_id]['object_categories']
            data['action_categories'] += meta_rules['meta_rules'][meta_rule_id]['action_categories']
            break

    data['name'] = uuid4().hex

    req, meta_rules = add_meta_rules(name=data['name'], data=data)
    assert req.status == hug.HTTP_200


def test_add_two_meta_rules_with_different_combination_but_similar_items():
    meta_rule_name1 = uuid4().hex
    meta_rule_name2 = uuid4().hex

    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id1 = list(subject_category.keys())[0]

    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id1 = list(object_category.keys())[0]

    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id1 = list(action_category.keys())[0]

    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id2 = list(subject_category.keys())[0]

    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id2 = list(object_category.keys())[0]

    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id2 = list(action_category.keys())[0]

    data = {
        "name": meta_rule_name1,
        "subject_categories": [subject_category_id1, subject_category_id2],
        "object_categories": [object_category_id1, object_category_id2],
        "action_categories": [action_category_id1, action_category_id2]
    }
    req, meta_rules = add_meta_rules(meta_rule_name1, data=data)
    assert req.status == hug.HTTP_200
    data = {
        "name": meta_rule_name2,
        "subject_categories": [subject_category_id2],
        "object_categories": [object_category_id1],
        "action_categories": [action_category_id2]
    }

    req, meta_rules = add_meta_rules(meta_rule_name1, data=data)
    assert req.status == hug.HTTP_200


# This test Succeed as it's okay to have empty id in adding meta rule, as it is not attached to model yet
def test_add_meta_rules_with_empty_subject_in_mid():
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    value = meta_rule_helper.get_body_meta_rule_with_empty_category_in_mid('subject')
    with pytest.raises(exceptions.SubjectCategoryUnknown) as exception_info:
        req = hug.test.post(meta_rules, "/meta_rules", body=value,
                            headers=auth_headers)
    # assert req.status == hug.HTTP_200
    assert str(exception_info.value) == "400: Subject Category Unknown"


def test_add_meta_rules_with_empty_object_in_mid():
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    value = meta_rule_helper.get_body_meta_rule_with_empty_category_in_mid('object')
    with pytest.raises(exceptions.ObjectCategoryUnknown) as exception_info:
        req = hug.test.post(meta_rules, "/meta_rules", body=value,
                            headers=auth_headers)
    assert str(exception_info.value) == "400: Object Category Unknown"


def test_add_meta_rules_with_empty_action_in_mid():
    from moon_manager.api import meta_rules
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    value = meta_rule_helper.get_body_meta_rule_with_empty_category_in_mid('action')
    with pytest.raises(exceptions.ActionCategoryUnknown) as exception_info:
        req = hug.test.post(meta_rules, "/meta_rules", body=value,
                            headers=auth_headers)
    assert str(exception_info.value) == "400: Action Category Unknown"


def test_add_meta_rule_with_existing_name_error():
    name = uuid4().hex
    req, meta_rules = add_meta_rules(name)
    assert req.status == hug.HTTP_200
    with pytest.raises(exceptions.MetaRuleExisting) as exception_info:
        req, meta_rules = add_meta_rules(name)
    assert "409: Meta Rule Existing" == str(exception_info.value)
    # assert req.status == hug.HTTP_409
    # assert req.data["message"] == '409: Meta Rule Existing'


def test_add_meta_rules_with_forbidden_char_in_name():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, meta_rules = add_meta_rules("<a>")
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
    # assert req.status == hug.HTTP_400
    # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_add_meta_rules_with_blank_name():
    with pytest.raises(exceptions.MetaRuleContentError) as exception_info:
        req, meta_rules = add_meta_rules("")
    assert "400: Meta Rule Error" == str(exception_info.value)
    # assert req.status == hug.HTTP_400
    # assert req.data["message"] == '400: Meta Rule Error'


def test_add_meta_rules_without_subject_categories():
    name_meta_rule = uuid4().hex
    req, meta_rules = add_meta_rules_without_category_ids(name_meta_rule)
    assert req.status == hug.HTTP_200


def test_delete_meta_rules():
    name_meta_rule = uuid4().hex
    req, meta_rules = add_meta_rules_without_category_ids(name_meta_rule)
    meta_rule_id = next(iter(meta_rules['meta_rules']))
    req = delete_meta_rules(meta_rules['meta_rules'][meta_rule_id]['name'])
    assert req.status == hug.HTTP_200


def test_delete_meta_rules_without_id():
    with pytest.raises(exceptions.MetaRuleUnknown) as exception_info:
        req = delete_meta_rules_without_id()
    assert "400: Meta Rule Unknown" == str(exception_info.value)
    # assert req.status == hug.HTTP_400
    # assert req.data["message"] == "400: Meta Rule Unknown"


def test_update_meta_rules():
    name = "testuser" + uuid4().hex
    req = add_meta_rules(name)
    meta_rule_id = list(req[1]['meta_rules'])[0]
    req_update = update_meta_rules(name, meta_rule_id)
    assert req_update[0].status == hug.HTTP_200
    delete_meta_rules("testuser")
    get_meta_rules()


def test_update_meta_rules_empty_name():
    req = add_meta_rules("testuser" + uuid4().hex)
    meta_rule_id = list(req[1]['meta_rules'])[0]
    with pytest.raises(exceptions.MetaRuleContentError) as exception_info:
        req_update = update_meta_rules("", meta_rule_id)
    assert "400: Meta Rule Error" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_400
    # assert req_update[1]['message'] == '400: Meta Rule Error'


def test_update_meta_rules_space_name():
    req = add_meta_rules("testuser" + uuid4().hex)
    meta_rule_id = list(req[1]['meta_rules'])[0]
    with pytest.raises(exceptions.MetaRuleContentError) as exception_info:
        req_update = update_meta_rules("  ", meta_rule_id)
    assert "400: Meta Rule Error" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_400
    # assert req_update[1]['message'] == '400: Meta Rule Error'


def test_update_meta_rule_with_combination_existed():
    meta_rule_name1 = uuid4().hex
    req, meta_rules = add_meta_rules(meta_rule_name1)
    meta_rule_id1 = next(iter(meta_rules['meta_rules']))
    data1 = meta_rules['meta_rules'][meta_rule_id1]

    meta_rule_name2 = uuid4().hex
    req, meta_rules = add_meta_rules(meta_rule_name2)
    meta_rule_id2 = next(iter(meta_rules['meta_rules']))
    data2 = meta_rules['meta_rules'][meta_rule_id2]
    data1['name'] = data2['name']
    with pytest.raises(exceptions.MetaRuleExisting) as exception_info:
        req_update = update_meta_rules(name=meta_rule_name2, metaRuleId=meta_rule_id2,
                                       data=data1)
    assert "409: Meta Rule Existing" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_409
    # assert req_update[1]['message'] == '409: Meta Rule Existing'


def test_update_meta_rule_with_different_combination_but_same_data():
    meta_rule_name1 = uuid4().hex
    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id1 = list(subject_category.keys())[0]
    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id1 = list(object_category.keys())[0]
    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id1 = list(action_category.keys())[0]
    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id2 = list(subject_category.keys())[0]
    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id2 = list(object_category.keys())[0]
    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id2 = list(action_category.keys())[0]

    data = {
        "name": meta_rule_name1,
        "subject_categories": [subject_category_id1, subject_category_id2],
        "object_categories": [object_category_id1, object_category_id2],
        "action_categories": [action_category_id1, action_category_id2]
    }
    req, meta_rules = add_meta_rules(meta_rule_name1, data=data)
    assert req.status == hug.HTTP_200

    meta_rule_name2 = uuid4().hex
    req, meta_rules = add_meta_rules(meta_rule_name2)
    meta_rule_id2 = next(iter(meta_rules['meta_rules']))
    data2 = {
        "name": meta_rule_name2,
        "subject_categories": [subject_category_id1, subject_category_id2],
        "object_categories": [object_category_id1],
        "action_categories": [action_category_id1, action_category_id2]
    }

    req_update = update_meta_rules(name=meta_rule_name2, metaRuleId=meta_rule_id2,
                                   data=data2)
    assert req_update[0].status == hug.HTTP_200


def test_update_meta_rules_without_id():
    with pytest.raises(exceptions.MetaRuleUnknown) as exception_info:
        req_update = update_meta_rules("testuser", "")
    assert "400: Meta Rule Unknown" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_400
    # assert req_update[0].data["message"] == "400: Meta Rule Unknown"


def test_update_meta_rules_without_name():
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req_update = update_meta_rules("<br/>", "1234567")
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_400
    # assert req_update[0].data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_update_meta_rules_without_categories():
    req_update = update_meta_rules_with_categories("testuser" + uuid4().hex)
    assert req_update[0].status == hug.HTTP_200


def test_update_meta_rules_with_empty_categories():
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser",
        "subject_categories": [""],
        "object_categories": [""],
        "action_categories": [""]
    }
    req_update = update_meta_rules_with_categories("testuser", data=data,
                                                   meta_rule_id=meta_rule_id)
    assert req_update[0].status == hug.HTTP_200
    # assert "400: Subject Category Unknown" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_400
    # assert req_update[1]['message'] == '400: Subject Category Unknown'


def test_update_meta_rules_with_blank_subject_categories():
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser1",
        "subject_categories": [],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    req_update = update_meta_rules_with_categories("testuser", data=data,
                                                   meta_rule_id=meta_rule_id)

    assert req_update[0].status == hug.HTTP_200


def test_update_meta_rules_with_blank_object_categories():
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser1",
        "subject_categories": [subject_category_id],
        "object_categories": [],
        "action_categories": [action_category_id]
    }
    req_update = update_meta_rules_with_categories("testuser", data=data,
                                                   meta_rule_id=meta_rule_id)

    assert req_update[0].status == hug.HTTP_200


def test_update_meta_rules_with_blank_action_categories():
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser1",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": []
    }
    req_update = update_meta_rules_with_categories("testuser", data=data,
                                                   meta_rule_id=meta_rule_id)

    assert req_update[0].status == hug.HTTP_200


def test_update_meta_rules_with_empty_subject_category():
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser",
        "subject_categories": [""],
        "object_categories": [object_category_id],
        "action_categories": [action_category_id]
    }
    req_update = update_meta_rules_with_categories("testuser", data=data,
                                                       meta_rule_id=meta_rule_id)
    assert req_update[0].status == hug.HTTP_200
    # assert "400: Subject Category Unknown" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_400
    # assert req_update[1]['message'] == '400: Subject Category Unknown'


def test_update_meta_rules_with_empty_action_category():
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser",
        "subject_categories": [subject_category_id],
        "object_categories": [object_category_id],
        "action_categories": [""]
    }
    req_update = update_meta_rules_with_categories("testuser", data=data,
                                                       meta_rule_id=meta_rule_id)
    assert req_update[0].status == hug.HTTP_200
    # assert "400: Action Category Unknown" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_400
    # assert req_update[1]['message'] == '400: Action Category Unknown'


def test_update_meta_rules_with_empty_object_category():
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser",
        "subject_categories": [subject_category_id],
        "object_categories": [""],
        "action_categories": [action_category_id]
    }
    req_update = update_meta_rules_with_categories("testuser", data=data,
                                                       meta_rule_id=meta_rule_id)

    assert req_update[0].status == hug.HTTP_200
    # assert "400: Object Category Unknown" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_400
    # assert req_update[1]['message'] == '400: Object Category Unknown'


def test_update_meta_rules_with_categories_and_one_empty():
    subject_category_id, object_category_id, action_category_id, meta_rule_id = data_builder.create_new_meta_rule()
    data = {
        "name": "testuser",
        "subject_categories": [subject_category_id, ""],
        "object_categories": [object_category_id, ""],
        "action_categories": [action_category_id, ""]
    }
    with pytest.raises(exceptions.SubjectCategoryUnknown) as exception_info:
        req_update = update_meta_rules_with_categories("testuser", data=data,
                                                       meta_rule_id=meta_rule_id)
    assert "400: Subject Category Unknown" == str(exception_info.value)
    # assert req_update[0].status == hug.HTTP_400
    # assert req_update[1]['message'] == '400: Subject Category Unknown'


def test_add_one_meta_rules_with_different_combination_but_similar_items():
    meta_rule_name1 = uuid4().hex

    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id1 = list(subject_category.keys())[0]

    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id1 = list(object_category.keys())[0]

    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id1 = list(action_category.keys())[0]

    subject_category = category_helper.add_subject_category(
        value={"name": "subject category name" + uuid4().hex, "description": "description 1"})
    subject_category_id2 = list(subject_category.keys())[0]

    object_category = category_helper.add_object_category(
        value={"name": "object category name" + uuid4().hex, "description": "description 1"})
    object_category_id2 = list(object_category.keys())[0]

    action_category = category_helper.add_action_category(
        value={"name": "action category name" + uuid4().hex, "description": "description 1"})
    action_category_id2 = list(action_category.keys())[0]

    data = {
        "name": meta_rule_name1,
        "subject_categories": [subject_category_id1, subject_category_id2],
        "object_categories": [object_category_id1, object_category_id2],
        "action_categories": [action_category_id1, action_category_id2]
    }
    req, meta_rules = add_meta_rules(meta_rule_name1, data=data)
    assert req.status == hug.HTTP_200

    value = {
        "name": "name_model",
        "description": "test",
        "meta_rules": [next(iter(meta_rules['meta_rules']))]
    }
    mode_id = next(iter(model_helper.add_model(value=value)))

    value = {
        "name": "test_policy" + uuid4().hex,
        "model_id": mode_id,
        "genre": "authz",
        "description": "test",
    }

    policy_id = next(iter(policy_helper.add_policies(value=value)))

    data_id_1 = data_builder.create_subject_data(policy_id, subject_category_id1)
    data_id_2 = data_builder.create_subject_data(policy_id, subject_category_id2)
    data_id_3 = data_builder.create_object_data(policy_id, object_category_id2)
    data_id_4 = data_builder.create_object_data(policy_id, object_category_id1)
    data_id_5 = data_builder.create_action_data(policy_id, action_category_id1)
    data_id_5 = data_builder.create_action_data(policy_id, action_category_id2)

    from moon_utilities.auth_functions import get_api_key_for_user
    from falcon import HTTP_200, HTTP_400, HTTP_405, HTTP_409

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import policy

    req = hug.test.delete(policy, "policies/{}".format(policy_id), headers=auth_headers)
    assert req.status == HTTP_200


def test_update_meta_rules_with_blank_action_categories_assigned_to_used_model():
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_manager.api import meta_rules
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policies_list = policy_helper.add_policies_with_model()
    policy_id = list(policies_list.keys())[0]
    model_id = policies_list[policy_id]['model_id']
    models_list = model_helper.get_models(model_id=model_id)
    meta_rule_id = models_list[model_id]["meta_rules"][0]
    meta_rules_list = meta_rule_helper.get_meta_rules(meta_rule_id=meta_rule_id);
    data = meta_rules_list[meta_rule_id]

    data["action_categories"] = []

    with pytest.raises(exceptions.MetaRuleUpdateError) as exception_info:
        hug.test.patch(meta_rules, "/meta_rules/{}".format(meta_rule_id), body=data,
                       headers=auth_headers)
    assert "400: Meta_Rule Update Error" == str(exception_info.value)
