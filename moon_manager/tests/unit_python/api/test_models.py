# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import json
import hug
import pytest
from moon_utilities import exceptions
from helpers import data_builder as builder
from helpers import policy_helper
from helpers import model_helper
from uuid import uuid4


def get_models():
    from moon_manager.api import models
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.get(models, "/models", headers=auth_headers)
    models = req.data
    return req, models


def add_models(name, headers, data=None, ):
    from moon_manager.api import models
    subject_category_id, object_category_id, action_category_id, meta_rule_id = \
        builder.create_new_meta_rule()
    if not data:
        data = {
            "name": name,
            "description": "description of {}".format(name),
            "meta_rules": [meta_rule_id]
        }
    headers['Content-Type'] = 'application/json'
    req = hug.test.post(models, "/models", body=json.dumps(data),
                        headers=headers)
    models = req.data
    return req, models


def update_model(name, model_id, headers):
    from moon_manager.api import models
    subject_category_id, object_category_id, action_category_id, meta_rule_id = \
        builder.create_new_meta_rule()
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [meta_rule_id]
    }
    headers['Content-Type'] = 'application/json'
    req = hug.test.patch(models, "/models/{}".format(model_id), body=json.dumps(data),
                         headers=headers)
    if req.status == hug.HTTP_405:
        return req
    models = req.data
    return req, models


def add_model_without_meta_rules_ids(name, headers):
    from moon_manager.api import models
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": []
    }
    headers['Content-Type'] = 'application/json'
    req = hug.test.post(models, "/models", body=json.dumps(data),
                        headers=headers)
    models = req.data
    return req, models


def add_model_with_empty_meta_rule_id(name, headers):
    from moon_manager.api import models
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [""]
    }
    headers['Content-Type'] = 'application/json'
    req = hug.test.post(models, "/models", body=json.dumps(data),
                        headers=headers)
    models = req.data
    return req, models


def update_model_without_meta_rules_ids(model_id, headers):
    from moon_manager.api import models
    name = "model_id" + uuid4().hex
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": []
    }
    headers['Content-Type'] = 'application/json'
    req = hug.test.patch(models, "/models/{}".format(model_id), body=json.dumps(data),
                         headers=headers)
    models = req.data
    return req, models


def delete_models(name, headers):
    request, models = get_models()
    for key, value in models['models'].items():
        if value['name'] == name:
            from moon_manager.api import models
            req = hug.test.delete(models, "/models/{}".format(key), headers=headers)
            break
    return req


def delete_models_without_id(headers):
    from moon_manager.api import models
    req = hug.test.delete(models, "/models/{}".format(""), headers=headers)
    return req


def clean_models(headers):
    req, models = get_models()
    for key, value in models['models'].items():
        print(key)
        print(value)
        from moon_manager.api import models
        hug.test.delete(models, "/models/{}".format(key), headers=headers)


def test_delete_model_assigned_to_policy():
    policy_name = "testuser" + uuid4().hex
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    from moon_manager.api import policy
    from moon_manager.api import models
    from moon_utilities.auth_functions import get_api_key_for_user
    headers = {"X-Api-Key": get_api_key_for_user("admin"), 'Content-Type': 'application/json'}
    hug.test.post(policy, "/policies", body=json.dumps(data), headers=headers)
    with pytest.raises(exceptions.DeleteModelWithPolicy) as exception_info:
        req = hug.test.delete(models, "/models/{}".format(model_id), headers={"X-Api-Key":
                                                                                  get_api_key_for_user("admin")})
    assert "400: Model With Policy Error" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Model With Policy Error'


def test_get_models():
    req, models = get_models()
    assert req.status == hug.HTTP_200
    assert isinstance(models, dict)
    assert "models" in models


def test_add_models():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    req, models = add_models("testuser", auth_headers)
    assert req.status == hug.HTTP_200
    assert isinstance(models, dict)
    model_id = list(models["models"])[0]
    assert "models" in models
    assert models['models'][model_id]['name'] == "testuser"
    assert models['models'][model_id]["description"] == "description of {}".format("testuser")


def test_add_models_with_meta_rule_has_blank_subject():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    name = "testuser1"
    from moon_manager.api import models
    subject_category_id, object_category_id, action_category_id, meta_rule_id = \
        builder.create_new_meta_rule(empty="subject")
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [meta_rule_id]
    }
    auth_headers['Content-Type'] = 'application/json'
    req = hug.test.post(models, "/models", body=json.dumps(data),
                      headers=auth_headers)
    assert req.status == hug.HTTP_200


def test_add_models_with_meta_rule_has_blank_object():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    name = "testuser1"
    from moon_manager.api import models
    subject_category_id, object_category_id, action_category_id, meta_rule_id = \
        builder.create_new_meta_rule(empty="object")
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [meta_rule_id]
    }
    auth_headers['Content-Type'] = 'application/json'
    req = hug.test.post(models, "/models", body=json.dumps(data),
                            headers=auth_headers)
    assert req.status == hug.HTTP_200


def test_add_models_with_meta_rule_has_blank_action():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    name = "testuser1"
    from moon_manager.api import models
    subject_category_id, object_category_id, action_category_id, meta_rule_id = \
        builder.create_new_meta_rule(empty="action")
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [meta_rule_id]
    }
    auth_headers['Content-Type'] = 'application/json'
    req = hug.test.post(models, "/models", body=json.dumps(data),
                            headers=auth_headers)
    assert req.status == hug.HTTP_200


def test_delete_models():
    name = uuid4().hex + "testuser"
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    add_models(name, auth_headers)
    req = delete_models(name, headers=auth_headers)
    assert req.status == hug.HTTP_200


def test_update_models_with_assigned_policy():
    from moon_manager.api import models
    model = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(model.keys())[0]
    value = {
        "name": "test_policy" + uuid4().hex,
        "model_id": model_id,
        "description": "test",
    }
    policy_helper.add_policies(value=value)
    data = {
        "name": "model_" + uuid4().hex,
        "description": "description of model_2",
        "meta_rules": []
    }
    from moon_utilities.auth_functions import get_api_key_for_user
    headers = {"X-Api-Key": get_api_key_for_user("admin"), 'Content-Type': 'application/json'}
    with pytest.raises(exceptions.DeleteModelWithPolicy) as exception_info:
        req = hug.test.patch(models, "/models/{}".format(model_id), body=json.dumps(data),
                             headers=headers)
    assert "400: Model With Policy Error" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Model With Policy Error"


def test_update_models_with_no_assigned_policy():
    from moon_manager.api import models
    model = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(model.keys())[0]
    data = {
        "name": "model_" + uuid4().hex,
        "description": "description of model_2",
        "meta_rules": []
    }
    from moon_utilities.auth_functions import get_api_key_for_user
    headers = {"X-Api-Key": get_api_key_for_user("admin"), 'Content-Type': 'application/json'}
    req = hug.test.patch(models, "/models/{}".format(model_id), body=json.dumps(data),
                         headers=headers)
    assert req.status == hug.HTTP_200


def test_update_models_without_meta_rule_key():
    from moon_manager.api import models
    model = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(model.keys())[0]

    data = {
        "name": "model_" + uuid4().hex,
        "description": "description of model_2",
    }
    from moon_utilities.auth_functions import get_api_key_for_user
    headers = {"X-Api-Key": get_api_key_for_user("admin"), 'Content-Type': 'application/json'}
    with pytest.raises(exceptions.MetaRuleUnknown) as exception_info:
        req = hug.test.patch(models, "/models/{}".format(model_id), body=json.dumps(data),
                             headers=headers)
    assert "400: Meta Rule Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "400: Meta Rule Unknown"


def test_delete_models_without_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = delete_models_without_id(headers=headers)
    assert req.status == hug.HTTP_405


def test_add_model_with_empty_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, models = add_models("<br/>", headers=auth_headers)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_add_model_with_name_contain_space():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req, models = add_models("test<br>user", headers=auth_headers)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_add_model_with_name_space():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    with pytest.raises(exceptions.ModelContentError) as exception_info:
        req, models = add_models(" ", headers=auth_headers)
    assert "400: Model Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Model Unknown'


def test_add_model_with_empty_meta_rule_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    with pytest.raises(exceptions.MetaRuleUnknown) as exception_info:
        req, meta_rules = add_model_with_empty_meta_rule_id("testuser", headers=auth_headers)
    assert "400: Meta Rule Unknown" == str(exception_info.value)
        # assert req.status == hug.HTTP_400
        # assert req.data["message"] == '400: Meta Rule Unknown'


def test_add_model_with_existed_name():
    name = uuid4().hex
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    req, models = add_models(name, headers=auth_headers)
    assert req.status == hug.HTTP_200
    with pytest.raises(exceptions.ModelExisting) as exception_info:
        req, models = add_models(name, headers=auth_headers)
    assert "409: Model Error" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Model Error'


def test_add_model_with_existed_meta_rules_list():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    name = uuid4().hex
    subject_category_id, object_category_id, action_category_id, meta_rule_id = \
        builder.create_new_meta_rule()
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [meta_rule_id]
    }
    name = uuid4().hex
    req, models = add_models(name=name, headers=auth_headers, data=data)
    assert req.status == hug.HTTP_200
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [meta_rule_id]
    }
    with pytest.raises(exceptions.ModelExisting) as exception_info:
        req, models = add_models(name=name, headers=auth_headers, data=data)
    assert "409: Model Error" == str(exception_info.value)
        # assert req.status == hug.HTTP_409
        # assert req.data["message"] == '409: Model Error'


def test_add_model_without_meta_rules():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    req, meta_rules = add_model_without_meta_rules_ids("testuser", headers=auth_headers)
    assert req.status == hug.HTTP_200


def test_update_model():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    req = add_models("testuser", headers=auth_headers)
    model_id = list(req[1]['models'])[0]
    req_update = update_model("testuser", model_id, headers=auth_headers)
    assert req_update[0].status == hug.HTTP_200
    model_id = list(req_update[1]["models"])[0]
    assert req_update[1]["models"][model_id]["meta_rules"][0] is not None
    delete_models("testuser", headers=auth_headers)


def test_update_model_name_with_space():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    req = add_models("testuser", headers=auth_headers)
    model_id = list(req[1]['models'])[0]
    with pytest.raises(exceptions.ModelContentError) as exception_info:
        req_update = update_model(" ", model_id, headers=auth_headers)
    assert "400: Model Unknown" == str(exception_info.value)
        # assert req_update[0].status == hug.HTTP_400
        # assert req_update[1]["message"] == '400: Model Unknown'


def test_update_model_with_empty_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    req = add_models("testuser", headers=auth_headers)
    model_id = list(req[1]['models'])[0]
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    with pytest.raises(exceptions.ModelContentError) as exception_info:
        req_update = update_model("", model_id, headers=auth_headers)
    assert "400: Model Unknown" == str(exception_info.value)
        # assert req_update[0].status == hug.HTTP_400
        # assert req_update[1]['message'] == '400: Model Unknown'


def test_update_meta_rules_without_id():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    clean_models(headers=auth_headers)
    req_update = update_model("testuser", "", headers=auth_headers)
    assert req_update.status == hug.HTTP_405


def test_update_meta_rules_without_name():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    with pytest.raises(exceptions.ValidationContentError) as exception_info:
        req_update = update_model("<a></a>", "1234567", headers=auth_headers)
    assert "Key: 'name', [Forbidden characters in string]" == str(exception_info.value)
        # assert req_update[0].status == hug.HTTP_400
        # assert req_update[0].data["message"] == "Key: 'name', [Forbidden characters in string]"


def test_update_meta_rules_without_meta_rules():
    value = {
        "name": "mls_model_id" + uuid4().hex,
        "description": "test",
        "meta_rules": []
    }
    model = model_helper.add_model(value=value)
    model_id = list(model.keys())[0]
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req_update = update_model_without_meta_rules_ids(model_id, headers=auth_headers)
    assert req_update[0].status == hug.HTTP_200
