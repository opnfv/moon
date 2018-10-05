# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from .category_helper import *
from .policy_helper import *
from .data_helper import *
from .model_helper import *
from .meta_rule_helper import *
from uuid import uuid4


def create_subject_category(name):
    subject_category = add_subject_category(
        value={"name": name, "description": "description 1"})
    return list(subject_category.keys())[0]


def create_object_category(name):
    object_category = add_object_category(
        value={"name": name, "description": "description 1"})
    return list(object_category.keys())[0]


def create_action_category(name):
    action_category = add_action_category(
        value={"name": name, "description": "description 1"})
    return list(action_category.keys())[0]


def create_model(meta_rule_id, model_name="test_model"):
    value = {
        "name": model_name,
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


def create_new_policy(subject_category_name="subjectCategory", object_category_name="objectCategory",
                      action_category_name="actionCategory",
                      model_name="test_model", policy_name="policy_name",
                      meta_rule_name="meta_rule_"):
    if policy_name == "policy_name":
        policy_name = "policy_name_" + uuid4().hex

    subject_category_id, object_category_id, action_category_id, meta_rule_id = create_new_meta_rule(
        subject_category_name=subject_category_name + uuid4().hex,
        object_category_name=object_category_name + uuid4().hex,
        action_category_name=action_category_name + uuid4().hex,
        meta_rule_name=meta_rule_name + uuid4().hex
    )
    model = add_model(value=create_model(meta_rule_id, model_name))
    model_id = list(model.keys())[0]
    value = create_policy(model_id, policy_name)
    policy = add_policies(value=value)
    assert policy
    policy_id = list(policy.keys())[0]
    return subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id


def create_new_meta_rule(subject_category_name="subject_category" + uuid4().hex,
                         object_category_name="object_category" + uuid4().hex,
                         action_category_name="action_category" + uuid4().hex,
                         meta_rule_name="meta_rule" + uuid4().hex):
    from python_moondb.core import ModelManager

    subject_category_id = create_subject_category(subject_category_name)
    object_category_id = create_object_category(object_category_name)
    action_category_id = create_action_category(action_category_name)
    value = {"name": meta_rule_name,
             "algorithm": "name of the meta rule algorithm",
             "subject_categories": [subject_category_id],
             "object_categories": [object_category_id],
             "action_categories": [action_category_id]
             }
    # meta_rule = add_meta_rule(value=value)
    meta_rule = ModelManager.add_meta_rule(user_id=None, meta_rule_id=None, value=value)
    return subject_category_id, object_category_id, action_category_id, list(meta_rule.keys())[0]


def create_subject(policy_id):
    value = {
        "name": "testuser",
        "description": "test",
    }
    subject = add_subject(policy_id=policy_id, value=value)
    return list(subject.keys())[0]


def create_object(policy_id):
    value = {
        "name": "testobject",
        "description": "test",
    }
    object = add_object(policy_id=policy_id, value=value)
    return list(object.keys())[0]


def create_action(policy_id):
    value = {
        "name": "testaction",
        "description": "test",
    }
    action = add_action(policy_id=policy_id, value=value)
    return list(action.keys())[0]


def create_subject_data(policy_id, category_id):
    value = {
        "name": uuid4().hex,
        "description": {uuid4().hex: "", uuid4().hex: "", uuid4().hex: ""},
    }
    subject_data = add_subject_data(policy_id=policy_id, category_id=category_id, value=value).get('data')
    assert subject_data
    return list(subject_data.keys())[0]


def create_object_data(policy_id, category_id):
    value = {
        "name": uuid4().hex,
        "description": {uuid4().hex: "", uuid4().hex: "", uuid4().hex: ""},
    }
    object_data = add_object_data(policy_id=policy_id, category_id=category_id, value=value).get('data')
    return list(object_data.keys())[0]


def create_action_data(policy_id, category_id):
    value = {
        "name": uuid4().hex,
        "description": {uuid4().hex: "", uuid4().hex: "", uuid4().hex: ""},
    }
    action_data = add_action_data(policy_id=policy_id, category_id=category_id, value=value).get('data')
    return list(action_data.keys())[0]
