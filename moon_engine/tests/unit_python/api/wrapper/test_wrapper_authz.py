# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
import requests


def test_wrapper_get_authz():
    from moon_engine.api.wrapper.api import authz
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"),
                             api_key=get_api_key_for_user("admin"))

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

    req = hug.test.get(authz, "/authz/{}/{}/{}/{}".format(
        project_id, subjects_name, objects_name, actions_name))
    assert req.status == hug.HTTP_200
