# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging

logger = logging.getLogger("moon.manager.test.api." + __name__)


def clean_models():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    keys = list(_cache.models.keys())
    for key in keys:
        _cache.delete_model(key)


def clean_policies():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    keys = list(_cache.policies.keys())
    for key in keys:
        _cache.delete_policy(key)


def clean_subjects():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    
    policy_keys = list(_cache.policies.keys())
    subjects = _cache.subjects
    for policy_key in policy_keys:
        for key in subjects:
            try:
                _cache.delete_subject(policy_key, key)
            except AttributeError:
                pass
    _cache.delete_subject()


def clean_objects():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    policy_keys = list(_cache.policies.keys())
    objects = _cache.objects
    for policy_key in policy_keys:
        for key in objects:
            try:
                _cache.delete_object(policy_key, key)
            except AttributeError:
                pass
    _cache.delete_object()


def clean_actions():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    policy_keys = list(_cache.policies.keys())
    actions = _cache.actions
    for policy_key in policy_keys:
        for key in actions:
            try:
                _cache.delete_action(policy_key, key)
            except AttributeError:
                pass
    _cache.delete_action()


def clean_subject_categories():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    categories = list(_cache.subject_categories.keys())
    for key in categories:
        _cache.delete_subject_category(key)


def clean_object_categories():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    categories = list(_cache.object_categories.keys())
    for key in categories:
        _cache.delete_object_category(key)


def clean_action_categories():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    categories = list(_cache.action_categories.keys())
    for key in categories:
        _cache.delete_action_category(key)


def clean_subject_data():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    _cache.delete_subject_data()


def clean_object_data():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    _cache.delete_object_data()


def clean_action_data():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()
    _cache.delete_action_data()


def clean_meta_rule():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    categories = list(_cache.meta_rules.keys())
    for key in categories:
        _cache.delete_meta_rule(key)


def clean_subject_assignments():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    if not _cache.subject_assignments:
        return
    for policy_key in _cache.policies.keys():
        if policy_key not in _cache.subject_assignments:
            continue
        for key in _cache.subject_assignments[policy_key]:
            # policy_key = _cache.subject_assignments[policy_key][key]["policy_id"]
            subject_key = _cache.subject_assignments[policy_key][key]["subject_id"]
            cat_key = _cache.subject_assignments[policy_key][key]["category_id"]
            data_keys = _cache.subject_assignments[policy_key][key]["assignments"]
            for data_key in data_keys:
                _cache.delete_subject_assignment(
                    policy_id=policy_key,
                    perimeter_id=subject_key,
                    category_id=cat_key,
                    data_id=data_key
                )
        _cache.delete_subject_assignment()


def clean_object_assignments():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    if not _cache.object_assignments:
        return
    for policy_key in _cache.policies.keys():
        if policy_key not in _cache.object_assignments:
            continue
        for key in _cache.object_assignments[policy_key]:
            # policy_key = _cache.object_assignments[policy_key][key]["policy_id"]
            object_key = _cache.object_assignments[policy_key][key]["object_id"]
            cat_key = _cache.object_assignments[policy_key][key]["category_id"]
            data_keys = _cache.object_assignments[policy_key][key]["assignments"]
            for data_key in data_keys:
                _cache.delete_object_assignment(
                    policy_id=policy_key,
                    perimeter_id=object_key,
                    category_id=cat_key,
                    data_id=data_key
                )
        _cache.delete_object_assignment()


def clean_action_assignments():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    if not _cache.action_assignments:
        return
    for policy_key in _cache.policies.keys():
        if policy_key not in _cache.action_assignments:
            continue
        for key in _cache.action_assignments[policy_key]:
            action_key = _cache.action_assignments[policy_key][key]["action_id"]
            cat_key = _cache.action_assignments[policy_key][key]["category_id"]
            data_keys = _cache.action_assignments[policy_key][key]["assignments"]
            for data_key in data_keys:
                _cache.delete_action_assignment(
                    policy_id=policy_key,
                    perimeter_id=action_key,
                    category_id=cat_key,
                    data_id=data_key
                )
        _cache.delete_action_assignment()


def clean_rules():
    from moon_cache.cache import Cache
    _cache = Cache.getInstance()

    rules = list(_cache.rules.keys())
    for key in rules:
        _cache.delete_rule(key)


def clean_all():
    clean_rules()

    clean_subject_assignments()
    clean_object_assignments()
    clean_action_assignments()

    clean_subject_data()
    clean_object_data()
    clean_action_data()

    clean_actions()
    clean_objects()
    clean_subjects()

    clean_policies()
    clean_models()
    clean_meta_rule()

    clean_subject_categories()
    clean_object_categories()
    clean_action_categories()
