# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


def get_policies():
    from python_moondb.core import PolicyManager
    return PolicyManager.get_policies("admin")


def add_policies(value=None):
    from python_moondb.core import PolicyManager
    if not value:
        value = {
            "name": "test_policiy",
            "model_id": "",
            "genre": "authz",
            "description": "test",
        }
    return PolicyManager.add_policy("admin", value=value)


def delete_policies(uuid=None, name=None):
    from python_moondb.core import PolicyManager
    if not uuid:
        for policy_id, policy_value in get_policies():
            if name == policy_value['name']:
                uuid = policy_id
                break
    PolicyManager.delete_policy("admin", uuid)


def test_get_policies(db):
    policies = get_policies()
    assert isinstance(policies, dict)
    assert not policies


def test_add_policies(db):
    value = {
        "name": "test_policy",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = add_policies(value)
    assert isinstance(policies, dict)
    assert policies
    assert len(policies.keys()) == 1
    policy_id = list(policies.keys())[0]
    for key in ("genre", "name", "model_id", "description"):
        assert key in policies[policy_id]
        assert policies[policy_id][key] == value[key]


def test_delete_policies(db):
    value = {
        "name": "test_policy1",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = add_policies(value)
    policy_id1 = list(policies.keys())[0]
    value = {
        "name": "test_policy2",
        "model_id": "",
        "genre": "authz",
        "description": "test",
    }
    policies = add_policies(value)
    policy_id2 = list(policies.keys())[0]
    assert policy_id1 != policy_id2
    delete_policies(policy_id1)
    policies = get_policies()
    assert policy_id1 not in policies
