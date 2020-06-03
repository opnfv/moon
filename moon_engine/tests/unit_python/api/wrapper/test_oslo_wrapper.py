# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
import json
import requests


def get_subject_object_action():
    from moon_engine.api.configuration import get_configuration
    from moon_cache.cache import Cache
    from moon_utilities.auth_functions import get_api_key_for_user

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"),
                             api_key=get_api_key_for_user("admin"))

    # Note: patching the cache for the test
    CACHE.add_pipeline("b3d3e18a-bf33-40e8-b635-fd49e6634ccd", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    CACHE.add_pipeline("f8f49a77-9ceb-47b3-ac81-0f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    response = requests.get("{}/pdp".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    pdp = response.json()
    pdp_id = next(iter(pdp['pdps']))
    policy_id = pdp['pdps'][pdp_id].get("security_pipeline")[0]
    project_id = pdp['pdps'][pdp_id].get("vim_project_id")

    # response = requests.get("{}/policies".format(get_configuration("management").get("url")),
    #                         headers=auth_headers)
    # policies = response.json()
    # policy_id = next(iter(policies['policies']))

    response = requests.get("{}/policies/{}/subjects".format(
        get_configuration("management").get("url"), policy_id), headers=auth_headers)
    subjects = response.json()

    response = requests.get("{}/policies/{}/objects".format(
        get_configuration("management").get("url"), policy_id), headers=auth_headers)
    objects = response.json()

    response = requests.get("{}/policies/{}/actions".format(
        get_configuration("management").get("url"), policy_id), headers=auth_headers)
    actions = response.json()
    return subjects, objects, actions, project_id


def test_post_authz():
    from moon_engine.plugins import oslowrapper
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/pdp".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    pdp = response.json()
    pdp_id = next(iter(pdp['pdps']))
    policy_id = pdp['pdps'][pdp_id].get("security_pipeline")[0]
    project_id = pdp['pdps'][pdp_id].get("vim_project_id")

    response = requests.get("{}/policies/{}/subjects".format(get_configuration(
        "management").get("url"), policy_id), headers=auth_headers)
    subjects = response.json()

    response = requests.get("{}/policies/{}/objects".format(get_configuration(
        "management").get("url"), policy_id), headers=auth_headers)
    objects = response.json()

    response = requests.get("{}/policies/{}/actions".format(get_configuration(
        "management").get("url"), policy_id), headers=auth_headers)
    actions = response.json()

    subjects_name = subjects['subjects'][next(iter(subjects['subjects']))]['name']
    objects_name = objects['objects'][next(iter(objects['objects']))]['name']
    actions_name = actions['actions'][next(iter(actions['actions']))]['name']

    # Note: patching the cache for the test
    from moon_cache.cache import Cache
    CACHE = Cache.getInstance()
    CACHE.add_pipeline("b3d3e18abf3340e8b635fd49e6634ccd", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    CACHE.add_pipeline("f8f49a779ceb47b3ac810f01ef71b4e0", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })

    _target = {
        'target': {
            "name": objects_name,
        },
        "project_id": project_id,
        "user_id": subjects_name
    }
    _credentials = {
        "project_id": project_id,
        "user_id": subjects_name
    }

    authz_data = {
        'rule': actions_name,
        'target': json.dumps(_target),
        'credentials': json.dumps(_credentials)}
    req = hug.test.post(oslowrapper, "/authz/oslo", authz_data)
    assert req.status == hug.HTTP_200


def test_authz_true():
    from moon_engine.plugins import oslowrapper

    subjects, objects, actions, project_id = get_subject_object_action()

    _target = {
        'target': {
            "name": objects['objects'][next(iter(objects['objects']))]['name'],
        },
        "project_id": project_id,
        "user_id": subjects['subjects'][next(iter(subjects['subjects']))]['name']
    }
    _credentials = {
        "project_id": project_id,
        "user_id": subjects['subjects'][next(iter(subjects['subjects']))]['name']
    }
    authz_data = {
        'rule': actions['actions'][next(iter(actions['actions']))]['name'],
        'target': json.dumps(_target),
        'credentials': json.dumps(_credentials)}

    req = hug.test.post(oslowrapper, "/authz/oslo", body=authz_data)

    assert req.status == hug.HTTP_200 and req.data is not None and req.data


def test_authz_error_response_code():
    from moon_engine.plugins import oslowrapper

    subjects, objects, actions, project_id = get_subject_object_action()

    _target = {
        'target': {
            "name": objects['objects'][next(iter(objects['objects']))]['name'],
        },
        "project_id": "a64beb1cc224474fb4badd431f3e7106",  # invalid project id
        "user_id": subjects['subjects'][next(iter(subjects['subjects']))]['name']
    }
    authz_data = {
        'rule': actions['actions'][next(iter(actions['actions']))]['name'],
        'target': json.dumps(_target),
        'credentials': 'null'}

    print(authz_data)
    req = hug.test.post(oslowrapper, "/authz/oslo", body=authz_data)

    assert req.status != hug.HTTP_200

# def test_authz_error_no_interface_key(context):
#     import moon_wrapper.server
#     server = moon_wrapper.server.main()
#     client = server.app.test_client()
#     _target = {
#         'target': {
#             "name": context.get('object_name'),
#         },
#         "project_id": context.get('project_with_no_interface_key'),
#         "user_id": context.get('subject_name')
#     }
#     authz_data = {
#         'rule': context.get('action_name'),
#         'target': json.dumps(_target),
#         'credentials': 'null'}
#     req = client.post("/authz/oslo", data=json.dumps(authz_data))
#
#     assert req.data == b"False"
