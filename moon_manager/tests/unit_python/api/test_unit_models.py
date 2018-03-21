# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import json
import api.utilities as utilities


def get_models(client):
    req = client.get("/models")
    models = utilities.get_json(req.data)
    return req, models


def add_models(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": ["meta_rule_id1", "meta_rule_id2"]
    }
    req = client.post("/models", data=json.dumps(data),
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


def clean_models():
    client = utilities.register_client()
    req, models= get_models(client)
    for key, value in models['models'].items():
        print(key)
        print(value)
        client.delete("/models/{}".format(key))

def test_get_models():
    client = utilities.register_client()
    req, models= get_models(client)
    assert req.status_code == 200
    assert isinstance(models, dict)
    assert "models" in models


def test_add_models():
    clean_models()
    client = utilities.register_client()
    req, models = add_models(client, "testuser")
    assert req.status_code == 200
    assert isinstance(models, dict)
    value = list(models["models"].values())[0]
    assert "models" in models
    assert value['name'] == "testuser"
    assert value["description"] == "description of {}".format("testuser")
    assert value["meta_rules"][0] == "meta_rule_id1"


def test_delete_models():
    client = utilities.register_client()
    req = delete_models(client, "testuser")
    assert req.status_code == 200


def test_delete_models_without_id():
    client = utilities.register_client()
    req = delete_models_without_id(client)
    assert req.status_code == 500

