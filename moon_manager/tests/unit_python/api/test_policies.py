# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import json
from uuid import uuid4
import api.utilities as utilities
from helpers import model_helper
from helpers import policy_helper
from helpers import data_builder


def get_policies(client):
    req = client.get("/policies")
    policies = utilities.get_json(req.data)
    return req, policies


def add_policies(client, name):
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.post("/policies", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policies = utilities.get_json(req.data)
    return req, policies


def delete_policies_without_id(client):
    req = client.delete("/policies/{}".format(""))
    return req


def test_get_policies():
    client = utilities.register_client()
    req, policies = get_policies(client)
    assert req.status_code == 200
    assert isinstance(policies, dict)
    assert "policies" in policies


def test_add_policies():
    policy_name = "testuser" + uuid4().hex
    client = utilities.register_client()
    req, policies = add_policies(client, policy_name)
    assert req.status_code == 200
    assert isinstance(policies, dict)
    value = list(policies["policies"].values())[0]
    assert "policies" in policies
    assert value['name'] == policy_name
    assert value["description"] == "description of {}".format(policy_name)


def test_add_policies_without_model():
    policy_name = "testuser" + uuid4().hex
    client = utilities.register_client()
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": "",
        "genre": "genre"
    }
    req = client.post("/policies/", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})

    assert req.status_code == 200


def test_add_policies_with_same_name():
    name = uuid4().hex
    policy_name = name
    client = utilities.register_client()
    req, policies = add_policies(client, policy_name)
    assert req.status_code == 200
    assert isinstance(policies, dict)
    value = list(policies["policies"].values())[0]
    assert "policies" in policies
    assert value['name'] == policy_name
    assert value["description"] == "description of {}".format(policy_name)
    client = utilities.register_client()
    req, policies = add_policies(client, policy_name)
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Policy Already Exists'


def test_add_policy_with_empty_name():
    policy_name = ""
    client = utilities.register_client()
    req, policies = add_policies(client, policy_name)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Content Error'


def test_update_policies_with_model():
    policy_name = "testuser" + uuid4().hex
    client = utilities.register_client()
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": "",
        "genre": "genre"
    }
    req = client.post("/policies/", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policy_id = next(iter(utilities.get_json(req.data)['policies']))
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name + "-2",
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.patch("/policies/{}".format(policy_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 200
    assert json.loads(req.data)['policies'][policy_id]['name'] == policy_name + '-2'


def test_update_policies_name_success():
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
    req = client.post("/policies/", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policy_id = next(iter(utilities.get_json(req.data)['policies']))

    data = {
        "name": policy_name + "-2",
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.patch("/policies/{}".format(policy_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 200
    assert json.loads(req.data)['policies'][policy_id]['name'] == policy_name + '-2'


def test_update_policies_model_unused():
    policy_name = uuid4().hex
    client = utilities.register_client()
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.post("/policies/", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policy_id = next(iter(utilities.get_json(req.data)['policies']))
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.patch("/policies/{}".format(policy_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 200


def test_update_policy_name_with_existed_one():
    policy_name1 = "testuser" + uuid4().hex
    client = utilities.register_client()
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name1,
        "description": "description of {}".format(policy_name1),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.post("/policies/", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policy_id1 = next(iter(utilities.get_json(req.data)['policies']))

    policy_name2 = "testuser" + uuid4().hex
    client = utilities.register_client()
    req = model_helper.add_model(model_id="mls_model_id" + uuid4().hex)
    model_id = list(req.keys())[0]
    data = {
        "name": policy_name2,
        "description": "description of {}".format(policy_name2),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.post("/policies/", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policy_id2 = next(iter(utilities.get_json(req.data)['policies']))

    data = {
        "name": policy_name1,
        "description": "description of {}".format(policy_name1),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.patch("/policies/{}".format(policy_id2), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Policy Already Exists'


def test_update_policies_with_empty_name():
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
    req = client.post("/policies/", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policy_id = next(iter(utilities.get_json(req.data)['policies']))

    data = {
        "name": "",
        "description": "description of {}".format(policy_name),
        "model_id": model_id,
        "genre": "genre"
    }
    req = client.patch("/policies/{}".format(policy_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Content Error'


def test_update_policies_with_blank_model():
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
    req = client.post("/policies/", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policy_id = next(iter(utilities.get_json(req.data)['policies']))

    data = {
        "name": policy_name,
        "description": "description of {}".format(policy_name),
        "model_id": "",
        "genre": "genre"
    }

    req = client.patch("/policies/{}".format(policy_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 200


def test_update_policies_connected_to_rules_with_blank_model():
    client = utilities.register_client()
    req, rules, policy_id = data_builder.add_rules(client)
    req = client.get("/policies")
    data = utilities.get_json(req.data)
    for policy_obj_id in data['policies']:
        if policy_obj_id == policy_id:
            policy = data['policies'][policy_obj_id]
    policy['model_id'] = ''
    req = client.patch("/policies/{}".format(policy_id), data=json.dumps(policy),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy update error'


def test_delete_policies():
    client = utilities.register_client()

    policy = policy_helper.add_policies()
    policy_id = list(policy.keys())[0]

    req = client.delete("/policies/{}".format(policy_id))
    assert req.status_code == 200


def test_delete_policy_with_dependencies_rule():
    client = utilities.register_client()
    req, rules, policy_id = data_builder.add_rules(client)
    req = client.delete("/policies/{}".format(policy_id))
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy With Rule Error'


def test_delete_policy_with_dependencies_subject_data():
    client = utilities.register_client()
    req, rules, policy_id = data_builder.add_rules(client)
    req = client.delete("/policies/{}/rules/{}".format(policy_id, next(iter(rules['rules']))))
    assert req.status_code == 200
    req = client.delete("/policies/{}".format(policy_id))
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy With Data Error'


def test_delete_policy_with_dependencies_perimeter():
    client = utilities.register_client()
    policy = policy_helper.add_policies()
    policy_id = next(iter(policy))

    data = {
        "name": 'testuser'+uuid4().hex,
        "description": "description of {}".format(uuid4().hex),
        "password": "password for {}".format(uuid4().hex),
        "email": "{}@moon".format(uuid4().hex)
    }
    req = client.post("/policies/{}/subjects".format(policy_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})

    assert req.status_code == 200
    req = client.delete("/policies/{}".format(policy_id))
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy With Perimeter Error'


def test_delete_policies_without_id():
    client = utilities.register_client()
    req = delete_policies_without_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Unknown'
