# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from helpers import data_builder as builder
from uuid import uuid4


def get_models(model_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.get_models(user_id=None, model_id=model_id)


def add_model(model_id=None, value=None):
    from python_moondb.core import ModelManager
    if not value:
        subject_category_id, object_category_id, action_category_id, meta_rule_id = builder.create_new_meta_rule(
            subject_category_name="subject_category1"+uuid4().hex,
            object_category_name="object_category1"+uuid4().hex,
            action_category_name="action_category1"+uuid4().hex)
        name = "MLS" if model_id is None else "MLS " + model_id
        value = {
            "name": name,
            "description": "test",
            "meta_rules": [meta_rule_id]
        }
    return ModelManager.add_model(user_id=None, model_id=model_id, value=value)


def delete_models(uuid=None, name=None):
    from python_moondb.core import ModelManager
    if not uuid:
        for model_id, model_value in get_models():
            if name == model_value['name']:
                uuid = model_id
                break
    ModelManager.delete_model(user_id=None, model_id=uuid)


def delete_all_models():
    from python_moondb.core import ModelManager
    models_values = get_models()
    print(models_values)
    for model_id, model_value in models_values.items():
        ModelManager.delete_model(user_id=None, model_id=model_id)


def update_model(model_id=None, value=None):
    from python_moondb.core import ModelManager
    return ModelManager.update_model(user_id=None, model_id=model_id, value=value)
