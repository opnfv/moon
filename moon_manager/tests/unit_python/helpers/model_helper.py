# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from helpers import data_builder as builder
from uuid import uuid4


def get_models(model_id=None):
    from moon_manager.db_driver import ModelManager
    return ModelManager.get_models(moon_user_id=None, model_id=model_id)


def add_model(model_id=None, value=None):
    from moon_manager.db_driver import ModelManager
    if not value:
        subject_category_id, object_category_id, action_category_id, meta_rule_id = builder.create_new_meta_rule()
        name = "MLS"+uuid4().hex if model_id is None else "MLS " + model_id
        value = {
            "name": name,
            "description": "test",
            "meta_rules": [meta_rule_id]
        }
    return ModelManager.add_model(moon_user_id=None, model_id=model_id, value=value)


def add_model_without_meta_rule(model_id=None, value=None):
    from moon_manager.db_driver import ModelManager
    if not value:
        name = "MLS"+uuid4().hex if model_id is None else "MLS " + model_id
        value = {
            "name": name,
            "description": "test",
            "meta_rules": ""
        }
    return ModelManager.add_model(moon_user_id=None, model_id=model_id, value=value)


def add_model_with_blank_subject_meta_rule(model_id=None, value=None):
    from moon_manager.db_driver import ModelManager
    if not value:
        subject_category_id, object_category_id, action_category_id, meta_rule_id = builder.create_new_meta_rule(empty='subject')
        name = "MLS"+uuid4().hex if model_id is None else "MLS " + model_id
        value = {
            "name": name,
            "description": "test",
            "meta_rules": [meta_rule_id]
        }
    return ModelManager.add_model(moon_user_id=None, model_id=model_id, value=value)



def delete_models(uuid=None, name=None):
    from moon_manager.db_driver import ModelManager
    if not uuid:
        for model_id, model_value in get_models():
            if name == model_value['name']:
                uuid = model_id
                break
    ModelManager.delete_model(moon_user_id=None, model_id=uuid)


def delete_all_models():
    from moon_manager.db_driver import ModelManager
    models_values = get_models()
    print(models_values)
    for model_id, model_value in models_values.items():
        ModelManager.delete_model(moon_user_id=None, model_id=model_id)


def update_model(model_id=None, value=None):
    from moon_manager.db_driver import ModelManager
    return ModelManager.update_model(moon_user_id=None, model_id=model_id, value=value)
