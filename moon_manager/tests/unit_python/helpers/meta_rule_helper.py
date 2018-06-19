# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from helpers import data_builder as builder
from uuid import uuid4


def set_meta_rule(meta_rule_id, value=None):
    from python_moondb.core import ModelManager
    if not value:
        action_category_id = builder.create_action_category("action_category_id1"+uuid4().hex)
        subject_category_id = builder.create_subject_category("subject_category_id1"+uuid4().hex)
        object_category_id = builder.create_object_category("object_category_id1"+uuid4().hex)
        value = {
            "name": "MLS_meta_rule",
            "description": "test",
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }
    return ModelManager.set_meta_rule(user_id=None, meta_rule_id=meta_rule_id, value=value)


def add_meta_rule(meta_rule_id=None, value=None):
    from python_moondb.core import ModelManager
    if not value:
        action_category_id = builder.create_action_category("action_category_id1"+uuid4().hex)
        subject_category_id = builder.create_subject_category("subject_category_id1"+uuid4().hex)
        object_category_id = builder.create_object_category("object_category_id1"+uuid4().hex)
        value = {
            "name": "MLS_meta_rule"+uuid4().hex,
            "description": "test",
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }
    return ModelManager.add_meta_rule(user_id=None, meta_rule_id=meta_rule_id, value=value)


def get_meta_rules(meta_rule_id=None):
    from python_moondb.core import ModelManager
    return ModelManager.get_meta_rules(user_id=None, meta_rule_id=meta_rule_id)


def delete_meta_rules(meta_rule_id=None):
    from python_moondb.core import ModelManager
    ModelManager.delete_meta_rule(user_id=None, meta_rule_id=meta_rule_id)
