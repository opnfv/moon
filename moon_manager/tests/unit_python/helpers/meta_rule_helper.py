# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from helpers import data_builder as builder
from uuid import uuid4


def set_meta_rule(meta_rule_id, value=None):
    from moon_manager.db_driver import ModelManager
    if not value:
        action_category_id = builder.create_action_category("action_category_id1" + uuid4().hex)
        subject_category_id = builder.create_subject_category("subject_category_id1" + uuid4().hex)
        object_category_id = builder.create_object_category("object_category_id1" + uuid4().hex)
        value = {
            "name": "MLS_meta_rule",
            "description": "test",
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }
    return ModelManager.set_meta_rule(moon_user_id=None, meta_rule_id=meta_rule_id, value=value)


def add_meta_rule(meta_rule_id=None, value=None):
    from moon_manager.db_driver import ModelManager
    if not value:
        action_category_id = builder.create_action_category("action_category_id1" + uuid4().hex)
        subject_category_id = builder.create_subject_category("subject_category_id1" + uuid4().hex)
        object_category_id = builder.create_object_category("object_category_id1" + uuid4().hex)
        value = {
            "name": "MLS_meta_rule" + uuid4().hex,
            "description": "test",
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }
    return ModelManager.add_meta_rule(moon_user_id=None, meta_rule_id=meta_rule_id, value=value)


def get_body_meta_rule_with_empty_category_in_mid(type=None):
    action_category_id1 = builder.create_action_category("action_category_id1" + uuid4().hex)
    subject_category_id1 = builder.create_subject_category("subject_category_id1" + uuid4().hex)
    object_category_id1 = builder.create_object_category("object_category_id1" + uuid4().hex)

    action_category_id2 = builder.create_action_category("action_category_id1" + uuid4().hex)
    subject_category_id2 = builder.create_subject_category("subject_category_id1" + uuid4().hex)
    object_category_id2 = builder.create_object_category("object_category_id1" + uuid4().hex)
    value = {
        "name": "MLS_meta_rule" + uuid4().hex,
        "description": "test",
        "subject_categories": [subject_category_id1],
        "object_categories": [object_category_id1],
        "action_categories": [action_category_id1]
    }
    if type == 'subject':
        value['subject_categories'].append("")
    if type == 'object':
        value['object_categories'].append("")
    if type == 'action':
        value['action_categories'].append("")

    value['subject_categories'].append(subject_category_id2)
    value['object_categories'].append(object_category_id2)
    value['action_categories'].append(action_category_id2)
    return value


def get_meta_rules(meta_rule_id=None):
    from moon_manager.db_driver import ModelManager
    return ModelManager.get_meta_rules(moon_user_id=None, meta_rule_id=meta_rule_id)


def delete_meta_rules(meta_rule_id=None):
    from moon_manager.db_driver import ModelManager
    ModelManager.delete_meta_rule(moon_user_id=None, meta_rule_id=meta_rule_id)
