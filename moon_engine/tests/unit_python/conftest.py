# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import os
import pytest
import requests_mock
import mock_require_data


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    global manager_api_key
    with requests_mock.Mocker(real_http=True) as m:
        try:
            os.remove("/tmp/database_test.db")
        except FileNotFoundError:
            pass
        try:
            os.remove("/tmp/moon.pwd")
        except FileNotFoundError:
            pass
        print("Configure...")
        mock_require_data.register_require_data(m)
        #from moon_engine.api.configuration import set_configuration
        #set_configuration(yaml.safe_load(__CONF))
        print("Create a new user")
        from moon_utilities.auth_functions import add_user, init_db, get_api_key_for_user
        init_db("/tmp/moon.pwd")
        try:
            user = add_user("admin", "admin")
            manager_api_key = user["api_key"]
        except KeyError:
            print("User already exists")
            manager_api_key = get_api_key_for_user("admin")
        print("Initialize the database")
        # init_database()
        # from moon_manager import db_driver
        # db_driver.init()

        # mock_engine.register_engine(m)
        # mock_slaves.register_slaves(m)

        # from moon_manager.pip_driver import InformationManager
        # InformationManager.set_auth()

        from moon_cache.cache import Cache
        Cache.deleteInstance()
        yield m
        # InformationManager.unset_auth()
