# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug


def test_get_authz_authorized():
    from moon_engine.api.pipeline import authz
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    # FIXME: https://gitlab.forge.orange-labs.fr/moon/moon_cache/issues/1
    # req = benchmark(hug.test.get, authz,
    #                 "/authz/89ba91c1-8dd5-4abf-bfde-7a66936c51a6/67b8008a-3f8d-4f8e-847e-b628f0f7ca0e/cdb3df22-0dc0"
    #                 "-5a6e-a333-4b994827b068", headers=auth_headers)
    # # req = hug.test.get(authz, "/authz/test/test/test", headers=auth_headers)
    # assert req.status == hug.HTTP_204


def test_get_authz_unauthorized():
    from moon_engine.api.pipeline import authz
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    # FIXME: https://gitlab.forge.orange-labs.fr/moon/moon_cache/issues/1
    # req = benchmark(hug.test.get, authz,
    #                 "/authz/31fd15ad-1478-4a96-96fc-c887dddbfaf9/67b8008a-3f8d-4f8e-847e-b628f0f7ca0e/cdb3df22-0dc0"
    #                 "-5a6e-a333-4b994827b068", headers=auth_headers)
    # # req = hug.test.get(authz, "/authz/test/test/test", headers=auth_headers)
    # assert req.status == hug.HTTP_403
