# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
"""

import binascii
import hashlib
import os
import hug
import logging
import os
import getpass
from tinydb import TinyDB, Query
from moon_utilities import exceptions

LOGGER = logging.getLogger("moon.utilities.auth_functions")
db = None


def init_db(db_filename="db.json"):
    global db
    db = TinyDB(db_filename)


def xor_encode(data, key):
    """
    Encode data with the given key

    :param data: the data to encode
    :param key: the key ie password
    :return: a xor-ed version of the 2 strings
    """
    if not data:
        return ""
    if not key:
        raise exceptions.EncryptError
    return binascii.hexlify(
        ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(data, key)).encode("utf-8")).decode("utf-8")


def xor_decode(data, key):
    """
    Decode data with the given key

    :param data: the data to decode
    :param key: the key ie password
    :return: a xor-ed version of the 2 strings
    """
    if not data:
        return ""
    if not key:
        raise exceptions.DecryptError
    data = binascii.a2b_hex(data.encode("utf-8")).decode("utf-8")
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(data, key))


# From https://github.com/timothycrosley/hug/blob/develop/examples/secure_auth_with_db_example.py

def hash_password(password, salt):
    """
    Securely hash a password using a provided salt
    :param password:
    :param salt:
    :return: Hex encoded SHA512 hash of provided password
    """
    password = str(password).encode('utf-8')
    salt = str(salt).encode('utf-8')
    return hashlib.sha512(password + salt).hexdigest()


def gen_api_key(username):
    """
    Create a random API key for a user
    :param username:
    :return: Hex encoded SHA512 random string
    """
    salt = str(os.urandom(64)).encode('utf-8')
    return hash_password(username, salt)


def get_api_key_for_user(username):
    """
    Return the API key for a particular user
    :param username:
    :return: API key
    """
    global db
    if db is None:
        init_db()
    user_model = Query()
    user = db.get(user_model.username == username)

    if not user:
        LOGGER.warning("User %s not found", username)
        return False

    return user['api_key']


def del_api_key_for_user(username):
    """
    Delete the API key for a particular user
    :param username:
    :return: API key
    """
    global db
    if db is None:
        init_db()
    user_model = Query()
    users = db.search(user_model.username == username)

    if not users:
        LOGGER.warning("User %s not found", username)
        return False
    try:
        for user in users:
            user['api_key'] = None
        db.write_back(users)
        return True
    except Exception as e:
        LOGGER.exception(e)
        return False


def connect_from_env():
    try:
        user = os.environ["MOON_USERNAME"]
        pw = os.environ["MOON_PASSWORD"]
    except KeyError:
        LOGGER.error("Set your credentials with moonrc")
        exit(-1)

    return get_api_key(user, pw)


@hug.cli("get_key")
def get_api_key(username, password):
    """
    Authenticate a username and password against our database
    :param username:
    :param password:
    :return: authenticated username
    """
    global db
    if db is None:
        init_db()
    user_model = Query()
    user = db.get(user_model.username == username)

    if not user:
        LOGGER.warning("User %s not found", username)
        return False

    if user['password'] == hash_password(password, user.get('salt')):
        return user['api_key']

    return False


@hug.cli()
def authenticate_user(username, password):
    """
    Authenticate a username and password against our database
    :param username:
    :param password:
    :return: authenticated username
    """
    global db
    if db is None:
        init_db()
    user_model = Query()
    users = db.search(user_model.username == username)

    if not users:
        LOGGER.warning("User %s not found", username)
        return False

    for user in users:
        # Note: will only update the first item
        if user['password'] == hash_password(password, user.get('salt')):
            if not user['api_key']:
                api_key = gen_api_key(username)
                user['api_key'] = api_key
                db.write_back(users)
            return user['username']
        LOGGER.warning("Wrong password for user %s", username)
        return False


@hug.cli()
def change_password(username, current_password, new_password):
    """
    Change the password of the user in the database
    :param username:
    :param current_password:
    :param new_password:
    :return: True or False
    """

    if current_password == "":         # nosec (not a hardcoded password)
        current_password = getpass.getpass()

    is_password_ok = authenticate_user(username, current_password)
    if not is_password_ok:
        return False

    if new_password == "":              # nosec (not a hardcoded password)
        new_password = getpass.getpass()

    global db
    if db is None:
        init_db()
    user_model = Query()
    user = db.search(user_model.username == username)[0]

    salt = user['salt']
    password = hash_password(new_password, salt)
    api_key = gen_api_key(username)

    user_id = db.update({'password': password, 'api_key': api_key}, doc_ids=[user.doc_id])

    return {
       'result': 'success',
       'eid': user_id,
       'user_created': user,
       'api_key': api_key
    }


@hug.cli()
def authenticate_key(api_key):
    """
    Authenticate an API key against our database
    :param api_key:
    :return: authenticated username
    """
    global db
    if db is None:
        init_db()
    try:
        if not api_key:
            return False
        user_model = Query()
        user = db.search(user_model.api_key == api_key)[0]
        if user:
            return user['username']
    except Exception as e:
        LOGGER.exception(e)
        LOGGER.error("Cannot retrieve user for this authentication key {}".format(api_key))
    return False


"""
  API Methods start here
"""

api_key_authentication = hug.authentication.api_key(authenticate_key)
basic_authentication = hug.authentication.basic(authenticate_user)


@hug.cli("add_user")  # nosec (not a hardcoded password)
def add_user(username, password=""):
    """
    CLI Parameter to add a user to the database
    :param username:
    :param password: if not given, a password prompt is displayed
    :return: JSON status output
    """
    global db
    if db is None:
        init_db()
    user_model = Query()
    if db.search(user_model.username == username):
        return {
            'error': 'User {0} already exists'.format(username)
        }

    if password == "":  # nosec (not a hardcoded password)
        password = getpass.getpass()

    salt = hashlib.sha512(str(os.urandom(64)).encode('utf-8')).hexdigest()
    password = hash_password(password, salt)
    api_key = gen_api_key(username)

    user = {
        'username': username,
        'password': password,
        'salt': salt,
        'api_key': api_key
    }
    user_id = db.insert(user)

    return {
       'result': 'success',
       'eid': user_id,
       'user_created': user,
       'api_key': api_key
    }
