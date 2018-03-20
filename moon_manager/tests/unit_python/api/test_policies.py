# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import json
from uuid import uuid4
import api.utilities as utilities


def get_policies(client):
    req = client.get("/policies")
    policies = utilities.get_json(req.data)
    return req, policies


def add_policies(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "model_id": "modelId",
        "genre": "genre"
    }
    req = client.post("/policies", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policies = utilities.get_json(req.data)
    return req, policies


def delete_policies(client, name):
    request, policies = get_policies(client)
    for key, value in policies['policies'].items():
        if value['name'] == name:
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
    policy_name = "testuser"+uuid4().hex
    client = utilities.register_client()
    req, policies = add_policies(client, policy_name)
    assert req.status_code == 200
    assert isinstance(policies, dict)
    value = list(policies["policies"].values())[0]
    assert "policies" in policies
    assert value['name'] == policy_name
    assert value["description"] == "description of {}".format(policy_name)
    assert value["model_id"] == "modelId"
    assert value["genre"] == "genre"


def test_delete_policies():
    client = utilities.register_client()
    req = delete_policies(client, "testuser")
    assert req.status_code == 200


def test_delete_policies_without_id():
    client = utilities.register_client()
    req = delete_policies_without_id(client)
    assert req.status_code == 500

