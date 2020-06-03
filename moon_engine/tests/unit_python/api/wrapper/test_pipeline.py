# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug


def test_get_pipelines():
    from moon_engine.api.wrapper.api import pipeline
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_cache.cache import Cache
    from moon_engine.api.configuration import get_configuration
    CACHE = Cache.getInstance(manager_url=get_configuration("management").get("url"),
                              incremental=get_configuration("incremental_updates"),
                              manager_api_key=get_configuration("api_token"))

    CACHE.set_current_server(url=get_configuration("management").get("url"), api_key=get_api_key_for_user(
        "admin"))

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    req = hug.test.get(pipeline, "/pipelines", headers=auth_headers )
    assert req.status == hug.HTTP_200
    assert isinstance(req.data, dict)
    assert "pipelines" in req.data
