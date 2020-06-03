# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from falcon import HTTP_200, HTTP_400, HTTP_405, HTTP_409
import hug
from uuid import uuid4
import pytest
from moon_utilities import exceptions
from helpers import model_helper
from helpers import policy_helper


def get_policies(auth_headers):
    from moon_manager.api import policy
    req = hug.test.get(policy, "policies", headers=auth_headers)
    return req


def add_policies(name, auth_headers):
    from moon_manager.api import policy
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = hug.test.post(policy, "policies", data, headers=auth_headers)
    return req


def delete_policies_without_id(auth_headers):
    from moon_manager.api import policy
    req = hug.test.delete(policy, "policies/{}".format(""), headers=auth_headers)
    return req


def test_get_policies():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = get_policies(auth_headers=auth_headers)
    assert req.status == HTTP_200
    assert isinstance(req.data, dict)
    assert "policies" in req.data


def test_add_policies():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policy_name = "testuser" + uuid4().hex
    req = add_policies(policy_name, auth_headers=auth_headers)
    assert req.status == HTTP_200
    assert isinstance(req.data, dict)
    value = list(req.data["policies"].values())[0]
    assert "policies" in req.data
    assert value['name'] == policy_name
    assert value["description"] == "description of {}".format(policy_name)


def test_add_policies_without_model():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import policy
    policy_name = "testuser" + uuid4().hex
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": "",
        "genre": "genre"
    }
    req = hug.test.post(policy, "policies/", data, headers=auth_headers)

    assert req.status == HTTP_200


def test_add_policies_with_same_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    name = uuid4().hex
    policy_name = name
    req = add_policies(policy_name, auth_headers=auth_headers)
    assert req.status == HTTP_200
    assert isinstance(req.data, dict)
    value = list(req.data["policies"].values())[0]
    assert "policies" in req.data
    assert value['name'] == policy_name
    assert value["description"] == "description of {}".format(policy_name)
    with pytest.raises(exceptions.PolicyExisting) as exception_info:
        req = add_policies(policy_name, auth_headers=auth_headers)
    assert "409: Policy Already Exists" == str(exception_info.value)
        # assert req.status == HTTP_409
        # assert req.data["message"] == '409: Policy Already Exists'


def test_add_policy_with_empty_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policy_name = ""
    with pytest.raises(exceptions.PolicyContentError) as exception_info:
        req = add_policies(policy_name, auth_headers=auth_headers)
    assert "400: Policy Content Error" == str(exception_info.value)
        # assert req.status == HTTP_400
        # assert req.data["message"] == '400: Policy Content Error'


def test_add_policy_with_model_has_no_meta_rule():
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_manager.api import policy

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policy_name = "testuser" + uuid4().hex
    req = model_helper.add_model_without_meta_rule()
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    with pytest.raises(exceptions.MetaRuleUnknown) as exception_info:
        hug.test.post(policy, "policies/", data, headers=auth_headers)
    assert "400: Meta Rule Unknown" == str(exception_info.value)


def test_add_policy_with_model_has_blank_subject_meta_rule():
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_manager.api import policy

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    policy_name = "testuser" + uuid4().hex
    req = model_helper.add_model_with_blank_subject_meta_rule()
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    with pytest.raises(exceptions.MetaRuleContentError) as exception_info:
        hug.test.post(policy, "policies/", data, headers=auth_headers)
    assert "400: Meta Rule Error" == str(exception_info.value)



# FIXME: uncomment when model API is re-inserted
# def test_update_policies_with_model():
#     from moon_manager.api import policy
#     policy_name = "testuser" + uuid4().hex
#     data = {
#         "name": policy_name,
#         "description": "description of {}".format(policy_name),
#         "model_id": "",
#         "genre": "genre"
#     }
#     req = hug.test.post(policy, "policies/", data)
#     policy_id = next(iter(req.data['policies']))
#     req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
#     model_id = list(req.data.keys())[0]
#     data = {
#         "name": policy_name + "-2",
#         "description": "description of {}".format(policy_name),
#         "model_id": model_id,
#         "genre": "genre"
#     }
#     req = hug.test.patch("policies/{}".format(policy_id), data)
#     assert req.status == HTTP_200
#     assert req.data['policies'][policy_id]['name'] == policy_name + '-2'


def test_update_policies_name_success():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import policy
    policy_name = "testuser" + uuid4().hex
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = hug.test.post(policy, "policies/", data, headers=auth_headers)
    policy_id = next(iter(req.data['policies']))

    data = {
        "name": policy_name + "-2",
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = hug.test.patch(policy, "policies/{}".format(policy_id), data, headers=auth_headers)
    assert req.status == HTTP_200
    assert req.data['policies'][policy_id]['name'] == policy_name + '-2'


def test_update_blank_policies_with_model():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import policy
    policy_name = uuid4().hex
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": "",
        "genre": "genre"
    }
    req = hug.test.post(policy, "policies/", data, headers=auth_headers)
    policy_id = next(iter(req.data['policies']))
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = hug.test.patch(policy, "policies/{}".format(policy_id), data, headers=auth_headers)
    assert req.status == HTTP_200


def test_update_policies_model_unused():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import policy
    policy_name = uuid4().hex
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = hug.test.post(policy, "policies/", data, headers=auth_headers)
    policy_id = next(iter(req.data['policies']))
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }

    with pytest.raises(exceptions.PolicyUpdateError) as exception_info:
        req = hug.test.patch(policy, "policies/{}".format(policy_id), data, headers=auth_headers)
    assert "400: Policy update error" == str(exception_info.value)


# FIXME: uncomment when model API is re-inserted
# def test_update_policy_name_with_existed_one():
#     from moon_manager.api import policy
#     policy_name1 = "testuser" + uuid4().hex
#     req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
#     model_id = list(req.keys())[0]
#     data = {
#         "name": policy_name1,
#         "description": "description of {}".format(policy_name1),
#         "model_id": model_id,
#         "genre": "genre"
#     }
#     req = hug.test.post(policy, "policies/", data)
#     policy_id1 = next(iter(req.data['policies']))
#
#     policy_name2 = "testuser" + uuid4().hex
#     eq = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
#     model_id = list(req.data.keys())[0]
#     data = {
#         "name": policy_name2,
#         "description": "description of {}".format(policy_name2),
#         "model_id": model_id,
#         "genre": "genre"
#     }
#     req = hug.test.post(policy, "policies/", data)
#     policy_id2 = next(iter(req.data['policies']))
#
#     data = {
#         "name": policy_name1,
#         "description": "description of {}".format(policy_name1),
#         "model_id": model_id,
#         "genre": "genre"
#     }
#     req = hug.test.patch(policy, "policies/{}".format(policy_id2), data)
#     assert req.status == HTTP_409
#     assert req.data["message"] == '409: Policy Already Exists'


def test_update_policies_with_empty_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import policy
    policy_name = "testuser" + uuid4().hex
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = hug.test.post(policy, "policies/", data, headers=auth_headers)
    policy_id = next(iter(req.data['policies']))

    data = {
        "name": "",
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    with pytest.raises(exceptions.PolicyContentError) as exception_info:
        req = hug.test.patch(policy, "policies/{}".format(policy_id), data, headers=auth_headers)
    assert "400: Policy Content Error" == str(exception_info.value)
        # assert req.status == HTTP_400
        # assert req.data["message"] == '400: Policy Content Error'


def test_update_policies_with_blank_model():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import policy
    policy_name = "testuser" + uuid4().hex
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = hug.test.post(policy, "policies/", data, headers=auth_headers)
    policy_id = next(iter(req.data['policies']))

    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": "",
        "genre": "genre"
    }

    with pytest.raises(exceptions.PolicyUpdateError) as exception_info:
        req = hug.test.patch(policy, "policies/{}".format(policy_id), data, headers=auth_headers)
    assert "400: Policy update error" == str(exception_info.value)


# FIXME: uncomment when model API is re-inserted
# def test_update_policies_connected_to_rules_with_blank_model():
#     from moon_manager.api import policy
#     req, rules, policy_id = data_builder.add_rules()
#     req = hug.test.get(policy, "policies")
#     for policy_obj_id in req.data['policies']:
#         if policy_obj_id == policy_id:
#             policy = req.data['policies'][policy_obj_id]
#     policy['model_id'] = ''
#     req = hug.test.patch("/policies/{}".format(policy_id), req.data)
#     assert req.status == HTTP_400
#     assert req.data["message"] == '400: Policy update error'


def test_delete_policies():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import policy
    _policy = policy_helper.add_policies()
    policy_id = list(_policy.keys())[0]
    req = hug.test.delete(policy, "policies/{}".format(policy_id), headers=auth_headers)
    assert req.status == HTTP_200


# FIXME: uncomment when rule API is re-inserted
# def test_delete_policy_with_dependencies_rule():
#     from moon_manager.api import policy
#     req, rules, policy_id = data_builder.add_rules()
#     req = hug.test.delete(policy, "policies/{}".format(policy_id))
#     assert req.status == HTTP_400
#     assert req.data["message"] == '400: Policy With Rule Error'


# FIXME: uncomment when perimeter API is re-inserted
# def test_delete_policy_with_dependencies_subject_data():
#     from moon_manager.api import policy
#     req, rules, policy_id = data_builder.add_rules()
#     req = hug.test.delete(policy, "policies/{}/rules/{}".format(policy_id, next(iter(rules['rules']))))
#     assert req.status == HTTP_200
#     req = hug.test.delete(policy, "policies/{}".format(policy_id))
#     assert req.status == HTTP_400
#     assert req.data["message"] == '400: Policy With Data Error'


# FIXME: uncomment when perimeter API is re-inserted
# def test_delete_policy_with_dependencies_perimeter():
#     from moon_manager.api import policy
#     _policy = policy_helper.add_policies()
#     policy_id = next(iter(_policy))
#
#     data = {
#         "name": 'testuser'+uuid4().hex,
#         "description": "description of {}".format(uuid4().hex),
#         "password": "password for {}".format(uuid4().hex),
#         "email": "{}@moon".format(uuid4().hex)
#     }
#     req = hug.test.post(policy, "policies/{}/subjects".format(policy_id), data)
#
#     assert req.status == HTTP_200
#     req = hug.test.delete(policy, "policies/{}".format(policy_id))
#     assert req.status == HTTP_400
#     assert req.data["message"] == '400: Policy With Perimeter Error'


def test_delete_policies_without_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = delete_policies_without_id(auth_headers=auth_headers)
    assert req.status == HTTP_405
