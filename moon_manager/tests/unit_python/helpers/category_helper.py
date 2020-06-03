# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



def add_subject_category(cat_id=None, value=None):
    from moon_manager.db_driver import ModelManager
    category = ModelManager.add_subject_category(moon_user_id=None, category_id=cat_id, value=value)
    return category


def get_subject_category(cat_id=None):
    from moon_manager.db_driver import ModelManager
    category = ModelManager.get_subject_categories(moon_user_id=None, category_id=cat_id)
    return category


def add_object_category(cat_id=None, value=None):
    from moon_manager.db_driver import ModelManager
    category = ModelManager.add_object_category(moon_user_id=None, category_id=cat_id, value=value)
    return category


def get_object_category(cat_id=None):
    from moon_manager.db_driver import ModelManager
    category = ModelManager.get_object_categories(moon_user_id=None, category_id=cat_id)
    return category


def add_action_category(cat_id=None, value=None):
    from moon_manager.db_driver import ModelManager
    category = ModelManager.add_action_category(moon_user_id=None, category_id=cat_id, value=value)
    return category


def get_action_category(cat_id=None):
    from moon_manager.db_driver import ModelManager
    category = ModelManager.get_action_categories(moon_user_id=None, category_id=cat_id)
    return category
