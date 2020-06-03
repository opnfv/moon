# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import json
import api.utilities as utilities
from helpers import data_builder as builder
from helpers import policy_helper
from helpers import model_helper
from uuid import uuid4


def get_models(client):
    req = client.get("/models")
    models = utilities.get_json(req.data)
    return req, models


def add_models(client, name, data=None):
    subject_category_id, object_category_id, action_category_id, meta_rule_id = builder.create_new_meta_rule()

    if not data:
        data = {
            "name": name,
            "description": "description of {}".format(name),
            "meta_rules": [meta_rule_id]
        }
    req = client.post("/models", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    models = utilities.get_json(req.data)
    return req, models


def update_model(client, name, model_id):
    subject_category_id, object_category_id, action_category_id, meta_rule_id = builder.create_new_meta_rule()

    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [meta_rule_id]
    }
    req = client.patch("/models/{}".format(model_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    models = utilities.get_json(req.data)
    return req, models


def add_model_without_meta_rules_ids(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": []
    }
    req = client.post("/models", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    models = utilities.get_json(req.data)
    return req, models


def add_model_with_empty_meta_rule_id(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [""]
    }
    req = client.post("/models", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    models = utilities.get_json(req.data)
    return req, models


def update_model_without_meta_rules_ids(client, model_id):
    name = "model_id" + uuid4().hex
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": []
    }
    req = client.patch("/models/{}".format(model_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    models = utilities.get_json(req.data)
    return req, models


def delete_models(client, name):
    request, models = get_models(client)
    for key, value in models['models'].items():
        if value['name'] == name:
            req = client.delete("/models/{}".format(key))
            break
    return req


def delete_models_without_id(client):
    req = client.delete("/models/{}".format(""))
    return req


def test_delete_model_assigned_to_policy():
    policy_name = "testuser" + uuid4().hex
    client = utilities.register_client()
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.post("/policies", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    req = client.delete("/models/{}".format(model_id))
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Model With Policy Error'


def clean_models():
    client = utilities.register_client()
    req, models = get_models(client)
    for key, value in models['models'].items():
        print(key)
        print(value)
        client.delete("/models/{}".format(key))


def test_get_models():
    client = utilities.register_client()
    req, models = get_models(client)
    assert req.status_code == 200
    assert isinstance(models, dict)
    assert "models" in models


def test_add_models():
    clean_models()
    client = utilities.register_client()
    req, models = add_models(client, "testuser")
    assert req.status_code == 200
    assert isinstance(models, dict)
    model_id = list(models["models"])[0]
    assert "models" in models
    assert models['models'][model_id]['name'] == "testuser"
    assert models['models'][model_id]["description"] == "description of {}".format("testuser")


def test_delete_models():
    client = utilities.register_client()
    req = delete_models(client, "testuser")
    assert req.status_code == 200


def test_update_models_with_assigned_policy():
    client = utilities.register_client()

    model = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(model.keys())[0]
    value = {
        "name": "test_policy" + uuid4().hex,
        "model_id": model_id,
        "description": "test",
    }
    policy = policy_helper.add_policies(value=value)
    data = {
        "name": "model_" + uuid4().hex,
        "description": "description of model_2",
        "meta_rules": []
    }
    req = client.patch("/models/{}".format(model_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})

    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Model With Policy Error"


def test_update_models_with_no_assigned_policy():
    client = utilities.register_client()

    model = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(model.keys())[0]

    data = {
        "name": "model_" + uuid4().hex,
        "description": "description of model_2",
        "meta_rules": []
    }
    req = client.patch("/models/{}".format(model_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})

    assert req.status_code == 200


def test_add_models_with_meta_rule_key():
    client = utilities.register_client()

    model = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(model.keys())[0]

    data = {
        "name": "model_" + uuid4().hex,
        "description": "description of model_2",

    }
    req = client.patch("/models/{}".format(model_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})

    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Invalid Key :meta_rules not found"


def test_delete_models_without_id():
    client = utilities.register_client()
    req = delete_models_without_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Model Unknown"


def test_add_model_with_empty_name():
    clean_models()
    client = utilities.register_client()
    req, models = add_models(client, "<br/>")
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Forbidden characters in string]"


def test_add_model_with_name_contain_space():
    clean_models()
    client = utilities.register_client()
    req, models = add_models(client, "test<br>user")
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Forbidden characters in string]"


def test_add_model_with_name_space():
    clean_models()
    client = utilities.register_client()
    req, models = add_models(client, " ")
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Model Unknown'


def test_add_model_with_empty_meta_rule_id():
    clean_models()
    client = utilities.register_client()
    req, meta_rules = add_model_with_empty_meta_rule_id(client, "testuser")
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Meta Rule Unknown'


def test_add_model_with_existed_name():
    clean_models()
    client = utilities.register_client()
    name = uuid4().hex
    req, models = add_models(client, name)
    assert req.status_code == 200
    req, models = add_models(client, name)
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Model Error'


def test_add_model_with_existed_meta_rules_list():
    clean_models()
    client = utilities.register_client()
    name = uuid4().hex

    subject_category_id, object_category_id, action_category_id, meta_rule_id = builder.create_new_meta_rule()
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [meta_rule_id]
    }
    name = uuid4().hex
    req, models = add_models(client=client, name=name, data=data)
    assert req.status_code == 200

    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": [meta_rule_id]
    }
    req, models = add_models(client=client, name=name, data=data)
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Model Error'


def test_add_model_without_meta_rules():
    clean_models()
    client = utilities.register_client()
    req, meta_rules = add_model_without_meta_rules_ids(client, "testuser")
    assert req.status_code == 200
    # assert json.loads(req.data)["message"] == "Key: 'meta_rules', [Empty Container]"


def test_update_model():
    clean_models()
    client = utilities.register_client()
    req = add_models(client, "testuser")
    model_id = list(req[1]['models'])[0]
    req_update = update_model(client, "testuser", model_id)
    assert req_update[0].status_code == 200
    model_id = list(req_update[1]["models"])[0]
    assert req_update[1]["models"][model_id]["meta_rules"][0] is not None
    delete_models(client, "testuser")


def test_update_model_name_with_space():
    clean_models()
    client = utilities.register_client()
    req = add_models(client, "testuser")
    model_id = list(req[1]['models'])[0]
    req_update = update_model(client, " ", model_id)
    assert req_update[0].status_code == 400
    assert req_update[1]["message"] == '400: Model Unknown'


def test_update_model_with_empty_name():
    clean_models()
    client = utilities.register_client()
    req = add_models(client, "testuser")
    model_id = list(req[1]['models'])[0]
    req_update = update_model(client, "", model_id)
    assert req_update[0].status_code == 400
    assert req_update[1]['message'] == '400: Model Unknown'


def test_update_meta_rules_without_id():
    clean_models()
    client = utilities.register_client()
    req_update = update_model(client, "testuser", "")
    assert req_update[0].status_code == 400
    assert json.loads(req_update[0].data)["message"] == "400: Model Unknown"


def test_update_meta_rules_without_name():
    client = utilities.register_client()
    req_update = update_model(client, "<a></a>", "1234567")
    assert req_update[0].status_code == 400
    assert json.loads(req_update[0].data)[
               "message"] == "Key: 'name', [Forbidden characters in string]"


def test_update_meta_rules_without_meta_rules():
    value = {
        "name": "mls_model_id" + uuid4().hex,
        "description": "test",
        "meta_rules": []
    }
    model = model_helper.add_model(value=value)
    model_id = list(model.keys())[0]
    client = utilities.register_client()
    req_update = update_model_without_meta_rules_ids(client, model_id)
    assert req_update[0].status_code == 200
