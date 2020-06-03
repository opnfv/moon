# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
import requests


def test_wrapper_update_policy_existed():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"),
                             api_key=get_api_key_for_user("admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = response.json()
    key = next(iter(policies['policies']))
    policies['policies'][key]['name'] = "new " + policies['policies'][key]['name']
    req = hug.test.put(update, "/update/policy/{}".format(key),
                       policies['policies'][key], headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_delete_policy():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"),
                             api_key=get_api_key_for_user("admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    policies = response.json()
    key = next(iter(policies['policies']))
    req = hug.test.delete(update, "/update/policy/{}".format(key),
                          headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_update_policy_not_existed():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"),
                             api_key=get_api_key_for_user("admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    policies = response.json()
    key = next(iter(policies['policies']))
    policies['policies'][key]['name'] = "new " + policies['policies'][key]['name']
    req = hug.test.put(update, "/update/policy/{}".format("eac0ecd09ceb47b3ac810f01ef71b4e0"),
                       policies['policies'][key], headers=auth_headers)
    assert req.status == hug.HTTP_208


def test_wrapper_update_pdp_existed():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/pdp".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    pdps = response.json()
    key = next(iter(pdps['pdps']))
    pdps['pdps'][key]['name'] = "new " + pdps['pdps'][key]['name']
    req = hug.test.put(update, "/update/pdp/{}".format(key),
                       pdps['pdps'][key], headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_delete_pdp():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/pdp".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    pdps = response.json()
    key = next(iter(pdps['pdps']))
    req = hug.test.delete(update, "/update/pdp/{}".format(key), headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_delete_assignments():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    policies = response.json()
    policy_id = next(iter(policies['policies']))

    response = requests.get("{}/policies/{}/subject_assignments".format(get_configuration(
        "management").get("url"), policy_id),
        headers=auth_headers)
    subject_assignments = response.json()
    assert 'subject_assignments' in subject_assignments and len(
        subject_assignments['subject_assignments'])
    req = hug.test.delete(update,
                          "/update/assignment/{}/{}/".format(policy_id, "subject"),
                          headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get("{}/policies/{}/object_assignments".format(get_configuration(
        "management").get("url"), policy_id),
        headers=auth_headers)
    object_assignments = response.json()
    assert 'object_assignments' in object_assignments and len(
        object_assignments['object_assignments'])
    req = hug.test.delete(update,
                          "/update/assignment/{}/{}/".format(policy_id, "object"),
                          headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get("{}/policies/{}/action_assignments".format(get_configuration(
        "management").get("url"), policy_id),
        headers=auth_headers)
    action_assignments = response.json()
    assert 'action_assignments' in action_assignments and len(
        action_assignments['action_assignments'])
    req = hug.test.delete(update,
                          "/update/assignment/{}/{}/".format(policy_id, "action"),
                          headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_update_perimeter_existed():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = response.json()
    policy_id = next(iter(policies['policies']))

    response = requests.get("{}/policies/{}/subjects".format(get_configuration(
        "management").get("url"), policy_id), headers=auth_headers)
    subjects = response.json()
    assert 'subjects' in subjects and len(subjects['subjects'])

    for key in subjects['subjects']:
        subjects['subjects'][key]['name'] = "new " + subjects['subjects'][key]['name']
        req = hug.test.put(update, "/update/perimeter/{}/{}/{}".format(key, policy_id, 'subject'),
                           subjects['subjects'][key], headers=auth_headers)
        assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get("{}/policies/{}/objects".format(get_configuration(
        "management").get("url"), policy_id), headers=auth_headers)
    objects = response.json()
    assert 'objects' in objects and len(objects['objects'])

    for key in objects['objects']:
        objects['objects'][key]['name'] = "new " + objects['objects'][key]['name']
        req = hug.test.put(update, "/update/perimeter/{}/{}/{}".format(key, policy_id, 'object'),
                           objects['objects'][key], headers=auth_headers)
        assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get("{}/policies/{}/actions".format(get_configuration(
        "management").get("url"), policy_id), headers=auth_headers)
    actions = response.json()
    assert 'actions' in actions and len(actions['actions'])

    for key in actions['actions']:
        actions['actions'][key]['name'] = "new " + actions['actions'][key]['name']
        req = hug.test.put(update, "/update/perimeter/{}/{}/{}".format(key, policy_id, 'action'),
                           actions['actions'][key], headers=auth_headers)
        assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_delete_perimeter():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), 
                             api_key=get_api_key_for_user("admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = response.json()
    policy_id = next(iter(policies['policies']))

    response = requests.get("{}/policies/{}/subjects".format(get_configuration(
        "management").get("url"), policy_id), headers=auth_headers)
    subjects = response.json()
    assert 'subjects' in subjects and len(subjects['subjects'])

    for key in subjects['subjects']:
        req = hug.test.delete(update,
                              "/update/perimeter/{}/{}/{}".format(key, policy_id, 'subject'),
                              headers=auth_headers)
        assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get("{}/policies/{}/objects".format(get_configuration(
        "management").get("url"), policy_id), headers=auth_headers)
    objects = response.json()
    assert 'objects' in objects and len(objects['objects'])

    for key in objects['objects']:
        req = hug.test.delete(update, "/update/perimeter/{}/{}/{}".format(key, policy_id, 'object'),
                              headers=auth_headers)
        assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get("{}/policies/{}/actions".format(get_configuration(
        "management").get("url"), policy_id), headers=auth_headers)
    actions = response.json()
    assert 'actions' in actions and len(actions['actions'])

    for key in actions['actions']:
        req = hug.test.delete(update, "/update/perimeter/{}/{}/{}".format(key, policy_id, 'action'),
                              headers=auth_headers)

        assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_delete_rule():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    policies = response.json()
    policy_id = next(iter(policies['policies']))

    response = requests.get(
        "{}/policies/{}/rules".format(get_configuration("management").get("url"), policy_id),
        headers=auth_headers)
    rules = response.json()
    assert 'rules' in rules and 'policy_id' in rules['rules']
    assert rules['rules']['policy_id'] == policy_id
    assert len(rules['rules']['rules'])
    for i in range(0, len(rules['rules']['rules'])):
        req = hug.test.delete(update, "/update/rule/{}/{}".format(policy_id,
                              rules['rules']['rules'][i]['id']), headers=auth_headers)

        assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_update_model_existed():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/models".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    models = response.json()
    key = next(iter(models['models']))
    models['models'][key]['name'] = "new " + models['models'][key]['name']
    req = hug.test.put(update, "/update/model/{}".format(key),
                       models['models'][key], headers=auth_headers)

    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_delete_model():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/models".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    models = response.json()
    key = next(iter(models['models']))
    req = hug.test.delete(update, "/update/model/{}".format(key), headers=auth_headers)

    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_delete_category():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/subject_categories".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    subject_categories = response.json()
    category_id = next(iter(subject_categories['subject_categories']))
    req = hug.test.delete(update, "/update/meta_data/{}/{}".format(category_id, 'subject'),
                          headers=auth_headers)

    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get("{}/action_categories".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    action_categories = response.json()
    category_id = next(iter(action_categories['action_categories']))
    req = hug.test.delete(update, "/update/meta_data/{}/{}".format(category_id, 'action'),
                          headers=auth_headers)

    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get("{}/object_categories".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    object_categories = response.json()
    category_id = next(iter(object_categories['object_categories']))
    req = hug.test.delete(update, "/update/meta_data/{}/{}".format(category_id, 'object'),
                          headers=auth_headers)
    assert (req.status == hug.HTTP_202 or  req.status == hug.HTTP_200)


def test_wrapper_update_meta_rule_existed():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/meta_rules".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    meta_rules = response.json()
    key = next(iter(meta_rules['meta_rules']))
    meta_rules['meta_rules'][key]['name'] = "new " + meta_rules['meta_rules'][key]['name']
    req = hug.test.put(update, "/update/meta_rule/{}".format(key),
                       meta_rules['meta_rules'][key], headers=auth_headers)

    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)


def test_wrapper_delete_meta_rule():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/meta_rules".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    meta_rules = response.json()
    key = next(iter(meta_rules['meta_rules']))
    req = hug.test.delete(update, "/update/meta_rule/{}".format(key), headers=auth_headers)
    assert (req.status == hug.HTTP_202 or  req.status == hug.HTTP_200)


def test_wrapper_delete_data():
    from moon_engine.api.wrapper.api import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    CACHE.add_pipeline("eac0ecd09ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = response.json()
    policy_id = next(iter(policies['policies']))

    response = requests.get(
        "{}/policies/{}/subject_data".format(get_configuration("management").get("url"), policy_id),
        headers=auth_headers)
    subject_data_id = next(iter(response.json()['subject_data'][0]['data']))
    req = hug.test.delete(update, "/update/data/{}/{}".format(subject_data_id,'subject'),
                          headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get(
        "{}/policies/{}/object_data".format(get_configuration("management").get("url"), policy_id),
        headers=auth_headers)
    object_data_id = next(iter(response.json()['object_data'][0]['data']))
    req = hug.test.delete(update, "/update/data/{}/{}".format(object_data_id, 'object'),
                          headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)

    response = requests.get(
        "{}/policies/{}/action_data".format(get_configuration("management").get("url"), policy_id),
        headers=auth_headers)
    action_data_id = next(iter(response.json()['action_data'][0]['data']))
    req = hug.test.delete(update, "/update/data/{}/{}".format(action_data_id, 'action'),
                          headers=auth_headers)
    assert (req.status == hug.HTTP_202 or req.status == hug.HTTP_200)
