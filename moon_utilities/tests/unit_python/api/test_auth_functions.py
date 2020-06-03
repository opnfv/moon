# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import os
from uuid import uuid4
import pytest
from moon_utilities.auth_functions import xor_encode, xor_decode
from  moon_utilities import exceptions
from moon_utilities.auth_functions import init_db, add_user, authenticate_user
from moon_utilities.auth_functions import authenticate_key, get_api_key, del_api_key_for_user


def test_xor():
    uuid1 = uuid4().hex
    my_key = uuid4().hex
    crypted_data = xor_encode(uuid1, my_key)
    assert uuid1 != crypted_data
    decrypted_data = xor_decode(crypted_data, my_key)
    assert uuid1 == decrypted_data


def test_decrypt_exceptions():
    with pytest.raises(exceptions.DecryptError):
        uuid1 = uuid4().hex
        my_key = uuid4().hex
        crypted_data = xor_encode(uuid1, my_key)
        assert uuid1 != crypted_data
        my_key = False
        xor_decode(crypted_data, my_key)
    with pytest.raises(exceptions.DecryptError):
        uuid1 = uuid4().hex
        my_key = uuid4().hex
        crypted_data = xor_encode(uuid1, my_key)
        assert uuid1 != crypted_data
        my_key = ""
        xor_decode(crypted_data, my_key)


def test_encrypt_exceptions():
    with pytest.raises(exceptions.EncryptError):
        uuid1 = uuid4().hex
        my_key = False
        xor_encode(uuid1, my_key)
    with pytest.raises(exceptions.EncryptError):
        uuid1 = uuid4().hex
        my_key = ""
        xor_encode(uuid1, my_key)


def test_auth_api():
    try:
        os.remove("/tmp/test.db")
    except FileNotFoundError:
        pass
    init_db("/tmp/test.db")
    # create the user
    result = add_user("test_user", "1234567890")
    assert result
    # trying to auth the user
    assert authenticate_user("test_user", "1234567890")
    assert not authenticate_user("bad_test_user", "1234567890")
    assert not authenticate_key(None)
    assert not authenticate_key("")
    assert authenticate_key(result['api_key']) == "test_user"
    assert get_api_key("test_user", "1234567890") == result['api_key']
    # logout the user
    assert del_api_key_for_user("test_user")
    assert get_api_key("test_user", "1234567890") != result['api_key']
    assert get_api_key("test_user", "1234567890") is None
    # re-authent user
    assert authenticate_user("test_user", "1234567890")
    # check that the previous api_key is not valid again
    assert get_api_key("test_user", "1234567890") != result['api_key']
    assert get_api_key("test_user", "1234567890")
