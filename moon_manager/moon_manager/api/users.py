# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Users
"""
import hug
import logging
import getpass
from tinydb import Query
from moon_utilities.auth_functions import db, init_db, add_user, get_api_key, change_password

LOGGER = logging.getLogger("moon.manager.api." + __name__)

UsersAPI = hug.API('users')


@hug.object(name='users', version='1.0.0', api=UsersAPI)
class UsersCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod  # nosec
    @hug.object.cli
    def add(username, password: hug.types.text = ""):
        """
        Add a user to the database
        """
        return add_user(username, password)

    @staticmethod  # nosec
    @hug.object.cli
    def change_password(username, password: hug.types.text = "", new_password: hug.types.text = ""):
        """
        Authenticate a username and password against our database
        """
        result = change_password(username, password, new_password)
        if not result:
            return "Wrong password"
        return result

    @staticmethod  # nosec
    @hug.object.cli
    def key(username, password: hug.types.text = ""):
        """
        Authenticate a username and password against our database
        """
        if password == "":
            password = getpass.getpass()
        return get_api_key(username, password)

    @staticmethod
    @hug.object.cli
    def list(human: bool = False):
        """
        List users from the database
        """
        global db
        if db is None:
            init_db()
        user_model = Query()
        users = db.search(user_model.username.matches('.*'))
        if human:
            result = "Users"
            if users:
                for user in users:
                    result += f"\n{user['username']} : \n"
                    result += f"\tusername : {user['username']}\n"
                    result += f"\tapi_key : {user['api_key']}"
            else:
                result += f"\nNo user"
            return result
        else:
            result = []
            if users:
                for user in users:
                    result.append({
                        'username': user['username'],
                        'api_key': user['api_key']
                    })
            return {'users': result}







