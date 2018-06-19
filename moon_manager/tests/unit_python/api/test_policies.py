# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import json
from uuid import uuid4
import api.utilities as utilities
from helpers import model_helper


def get_policies(client):
    req = client.get("/policies")
    policies = utilities.get_json(req.data)
    return req, policies


def add_policies(client, name):
    req = model_helper.add_model(model_id="mls_model_id"+uuid4().hex)
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


def delete_policies(client, name):
    request, policies = get_policies(client)
    for key, value in policies['policies'].items():
        req = client.delete("/policies/{}".format(key))
        break
    return req


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


def test_delete_policies():
    client = utilities.register_client()
    req = delete_policies(client, "testuser")
    assert req.status_code == 200


def test_delete_policies_without_id():
    client = utilities.register_client()
    req = delete_policies_without_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Unknown'

