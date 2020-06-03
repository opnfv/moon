# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from .category_helper import *
from .policy_helper import *
from .data_helper import *
from helpers import model_helper
from .meta_rule_helper import *
import api.utilities as utilities
import json
from uuid import uuid4


def create_subject_category(name):
    subject_category = add_subject_category(
        value={"name": name + uuid4().hex, "description": "description 1"})
    return list(subject_category.keys())[0]


def create_object_category(name):
    object_category = add_object_category(
        value={"name": name + uuid4().hex, "description": "description 1"})
    return list(object_category.keys())[0]


def create_action_category(name):
    action_category = add_action_category(
        value={"name": name + uuid4().hex, "description": "description 1"})
    return list(action_category.keys())[0]


def create_model(meta_rule_id, model_name="test_model"):
    value = {
        "name": model_name + uuid4().hex,
        "description": "test",
        "meta_rules": [meta_rule_id]

    }
    return value


def create_policy(model_id, policy_name="policy_1"):
    value = {
        "name": policy_name,
        "model_id": model_id,
        "genre": "authz",
        "description": "test",
    }
    return value


def create_pdp(policies_ids):
    value = {
        "name": "test_pdp",
        "security_pipeline": policies_ids,
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    return value


def create_new_policy(subject_category_name=None, object_category_name=None,
                      action_category_name=None, model_name=None, policy_name=None,
                      meta_rule_name=None):
    if not subject_category_name:
        subject_category_name = "subjectCategory_" + uuid4().hex
    if not object_category_name:
        object_category_name = "objectCategory_" + uuid4().hex
    if not action_category_name:
        action_category_name = "actionCategory_" + uuid4().hex

    if not meta_rule_name:
        meta_rule_name = "meta_rule_" + uuid4().hex

    if not model_name:
        model_name = "model_name_" + uuid4().hex
    if not policy_name:
        policy_name = "policy_name_" + uuid4().hex

    subject_category_id, object_category_id, action_category_id, meta_rule_id = create_new_meta_rule(
        subject_category_name=subject_category_name + uuid4().hex,
        object_category_name=object_category_name + uuid4().hex,
        action_category_name=action_category_name + uuid4().hex,
        meta_rule_name=meta_rule_name + uuid4().hex
    )

    model = model_helper.add_model(value=create_model(meta_rule_id, model_name + uuid4().hex))
    model_id = list(model.keys())[0]
    value = create_policy(model_id, policy_name + uuid4().hex)
    policy = add_policies(value=value)
    assert policy
    policy_id = list(policy.keys())[0]
    return subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id


def create_new_meta_rule(subject_category_name=None, object_category_name=None,
                         action_category_name=None, meta_rule_name=None):
    if not subject_category_name:
        subject_category_name = "subjectCategory_" + uuid4().hex
    if not object_category_name:
        object_category_name = "objectCategory_" + uuid4().hex
    if not action_category_name:
        action_category_name = "actionCategory_" + uuid4().hex

    if not meta_rule_name:
        meta_rule_name = "meta_rule_" + uuid4().hex

    subject_category_id = create_subject_category(subject_category_name)
    object_category_id = create_object_category(object_category_name)
    action_category_id = create_action_category(action_category_name)
    value = {"name": meta_rule_name,
             "description": "name of the meta rule algorithm",
             "subject_categories": [subject_category_id],
             "object_categories": [object_category_id],
             "action_categories": [action_category_id]
             }
    meta_rule = add_meta_rule(value=value)
    return subject_category_id, object_category_id, action_category_id, list(meta_rule.keys())[0]


def create_subject(policy_id):
    value = {
        "name": "testuser" + uuid4().hex,
        "description": "test",
    }
    subject = add_subject(policy_id=policy_id, value=value)
    return list(subject.keys())[0]


def create_object(policy_id):
    value = {
        "name": "testobject" + uuid4().hex,
        "description": "test",
    }
    object = add_object(policy_id=policy_id, value=value)
    return list(object.keys())[0]


def create_action(policy_id):
    value = {
        "name": "testaction" + uuid4().hex,
        "description": "test",
    }
    action = add_action(policy_id=policy_id, value=value)
    return list(action.keys())[0]


def create_subject_data(policy_id, category_id):
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    subject_data = add_subject_data(policy_id=policy_id, category_id=category_id, value=value).get(
        'data')
    assert subject_data
    return list(subject_data.keys())[0]


def create_object_data(policy_id, category_id):
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    object_data = add_object_data(policy_id=policy_id, category_id=category_id, value=value).get(
        'data')
    return list(object_data.keys())[0]


def create_action_data(policy_id, category_id):
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    action_data = add_action_data(policy_id=policy_id, category_id=category_id, value=value).get(
        'data')
    return list(action_data.keys())[0]


def get_policy_id_with_subject_assignment():
    client = utilities.register_client()
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex)
    subject_id = create_subject(policy_id)
    data_id = create_subject_data(policy_id=policy_id, category_id=subject_category_id)

    data = {
        "id": subject_id,
        "category_id": subject_category_id,
        "data_id": data_id
    }
    client.post("/policies/{}/subject_assignments".format(policy_id), data=json.dumps(data),
                headers={'Content-Type': 'application/json'})
    return policy_id


def get_policy_id_with_object_assignment():
    client = utilities.register_client()
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex)
    object_id = create_object(policy_id)
    data_id = create_object_data(policy_id=policy_id, category_id=object_category_id)

    data = {
        "id": object_id,
        "category_id": object_category_id,
        "data_id": data_id
    }

    client.post("/policies/{}/object_assignments".format(policy_id), data=json.dumps(data),
                headers={'Content-Type': 'application/json'})
    return policy_id


def get_policy_id_with_action_assignment():
    client = utilities.register_client()
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = create_new_policy(
        subject_category_name="subject_category1" + uuid4().hex,
        object_category_name="object_category1" + uuid4().hex,
        action_category_name="action_category1" + uuid4().hex,
        meta_rule_name="meta_rule_1" + uuid4().hex)
    action_id = create_action(policy_id)
    data_id = create_action_data(policy_id=policy_id, category_id=action_category_id)

    data = {
        "id": action_id,
        "category_id": action_category_id,
        "data_id": data_id
    }
    client.post("/policies/{}/action_assignments".format(policy_id), data=json.dumps(data),
                headers={'Content-Type': 'application/json'})
    return policy_id


def add_rules(client):
    sub_id, obj_id, act_id, meta_rule_id, policy_id = create_new_policy("sub_cat" + uuid4().hex,
                                                                        "obj_cat" + uuid4().hex,
                                                                        "act_cat" + uuid4().hex)
    sub_data_id = create_subject_data(policy_id, sub_id)
    obj_data_id = create_object_data(policy_id, obj_id)
    act_data_id = create_action_data(policy_id, act_id)
    data = {
        "meta_rule_id": meta_rule_id,
        "rule": [sub_data_id, obj_data_id, act_data_id],
        "instructions": (
            {"decision": "grant"},
        ),
        "enabled": True
    }
    req = client.post("/policies/{}/rules".format(policy_id), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    rules = utilities.get_json(req.data)
    return req, rules, policy_id
