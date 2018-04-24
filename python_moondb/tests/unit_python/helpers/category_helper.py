# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

def add_subject_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_subject_category(user_id=None, category_id=cat_id, value=value)
    return category


def get_subject_category(cat_id=None):
    from python_moondb.core import ModelManager
    category = ModelManager.get_subject_categories(user_id=None, category_id=cat_id)
    return category


def add_object_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_object_category(user_id=None, category_id=cat_id, value=value)
    return category


def get_object_category(cat_id=None):
    from python_moondb.core import ModelManager
    category = ModelManager.get_object_categories(user_id=None, category_id=cat_id)
    return category


def add_action_category(cat_id=None, value=None):
    from python_moondb.core import ModelManager
    category = ModelManager.add_action_category(user_id=None, category_id=cat_id, value=value)
    return category


def get_action_category(cat_id=None):
    from python_moondb.core import ModelManager
    category = ModelManager.get_action_categories(user_id=None, category_id=cat_id)
    return category
