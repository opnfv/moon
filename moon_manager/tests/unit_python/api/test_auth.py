# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from falcon import HTTP_200, HTTP_204, HTTP_401
import hug
import base64
from uuid import uuid4
from helpers import data_builder as builder


def test_get_auth():
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_manager.api import auth
    from moon_manager.api import policy
    headers = {"Authorization": "Basic {}".format(base64.b64encode(b"admin:admin").decode("utf-8"))}
    req = hug.test.get(auth, 'auth/', headers=headers)
    assert req.status == HTTP_200
    key = req.data
    assert get_api_key_for_user("admin") == req.data
    headers = {"x-api-key": key}
    req = hug.test.get(policy, 'policies/', headers=headers)
    assert req.status == HTTP_200


def test_del_auth():
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_manager.api import auth
    from moon_manager.api import policy
    headers = {"Authorization": "Basic {}".format(base64.b64encode(b"admin:admin").decode("utf-8"))}
    req = hug.test.get(auth, 'auth/', headers=headers)
    assert req.status == HTTP_200
    key = req.data
    headers = {"x-api-key": key}
    req = hug.test.delete(auth, 'auth/', headers=headers)
    assert req.status == HTTP_204
    req = hug.test.get(policy, 'policies/', headers=headers)
    assert req.status == HTTP_401
    assert not get_api_key_for_user("admin")


def test_readd_auth():
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_manager.api import auth
    from moon_manager.api import policy
    headers = {"Authorization": "Basic {}".format(base64.b64encode(b"admin:admin").decode("utf-8"))}
    req = hug.test.get(auth, 'auth/', headers=headers)
    assert req.status == HTTP_200
    key = req.data
    headers = {"x-api-key": key}
    req = hug.test.delete(auth, 'auth/', headers=headers)
    assert req.status == HTTP_204
    headers = {"Authorization": "Basic {}".format(base64.b64encode(b"admin:admin").decode("utf-8"))}
    req = hug.test.get(auth, 'auth/', headers=headers)
    assert req.status == HTTP_200
    new_key = req.data
    headers = {"x-api-key": new_key}
    req = hug.test.get(policy, 'policies/', headers=headers)
    assert req.status == HTTP_200
    assert get_api_key_for_user("admin")
    assert get_api_key_for_user("admin") == new_key
    assert get_api_key_for_user("admin") != key

