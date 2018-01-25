import json
import requests


def get_models(context):
    req = requests.get("http://{}:{}/models".format(
        context.get("hostname"),
        context.get("port")),
        timeout=3)
    models = req.json()
    return req, models


def add_models(context, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "meta_rules": ["meta_rule_id1", "meta_rule_id2"]
    }
    req = requests.post("http://{}:{}/models".format(
        context.get("hostname"),
        context.get("port")),
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'},
        timeout=3)
    models = req.json()
    return req, models


def delete_models(context, name):
    _, models = get_models(context)
    request = None
    for key, value in models['models'].items():
        if value['name'] == name:
            request = requests.delete("http://{}:{}/models/{}".format(key,
                                      context.get("hostname"),
                                      context.get("port")),
                                      timeout=3)
            break
    return request


def delete_models_without_id(context):
    req = requests.delete("http://{}:{}/models/{}".format(
                          context.get("hostname"),
                          context.get("port"),
                          ""),
                          timeout=3)
    return req


def test_get_models(context):
    req, models = get_models(context)
    assert req.status_code == 200
    assert isinstance(models, dict)
    assert "models" in models


def test_add_models(context):
    req, models = add_models(context, "testuser")
    assert req.status_code == 200
    assert isinstance(models, dict)
    value = list(models["models"].values())[0]
    assert "models" in models
    assert value['name'] == "testuser"
    assert value["description"] == "description of {}".format("testuser")
    assert value["meta_rules"][0] == "meta_rule_id1"


def test_delete_models(context):
    req = delete_models(context, "testuser")
    assert req.status_code == 200


def test_delete_models_without_id(context):
    req = delete_models_without_id(context)
    assert req.status_code == 500

