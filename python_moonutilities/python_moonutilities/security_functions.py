# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import re
import os
import types
import requests
import time
from functools import wraps
from flask import request
import logging
from python_moonutilities import exceptions, configuration

logger = logging.getLogger("moon.utilities." + __name__)

keystone_config = configuration.get_configuration("openstack/keystone")["openstack/keystone"]
TOKENS = {}
__targets = {}

'''
[Note] is the asseration done here ?
what i mean that you have checked the content but you don't assert if true or not
'''
def filter_input(func_or_str):

    def __filter(string):
        if string and type(string) is str:
            return "".join(re.findall("[\w\- +]*", string))
        return string

    def __filter_dict(arg):
        result = dict()
        for key in arg.keys():
            if key == "email":
                result["email"] = __filter_email(arg[key])
            elif key == "password":
                result["password"] = arg['password']
            else:
                result[key] = __filter(arg[key])
        return result

    def __filter_email(string):
        if string and type(string) is str:
            return "".join(re.findall("[\w@\._\- +]*", string))
        return string

    def wrapped(*args, **kwargs):
        _args = []
        for arg in args:
            if isinstance(arg, str):
                arg = __filter(arg)
            elif isinstance(arg, list):
                arg = [__filter(item) for item in arg]
            elif isinstance(arg, tuple):
                arg = (__filter(item) for item in arg)
            elif isinstance(arg, dict):
                arg = __filter_dict(arg)
            _args.append(arg)
        for arg in kwargs:
            if type(kwargs[arg]) is str:
                kwargs[arg] = __filter(kwargs[arg])
            if isinstance(kwargs[arg], str):
                kwargs[arg] = __filter(kwargs[arg])
            elif isinstance(kwargs[arg], list):
                kwargs[arg] = [__filter(item) for item in kwargs[arg]]
            elif isinstance(kwargs[arg], tuple):
                kwargs[arg] = (__filter(item) for item in kwargs[arg])
            elif isinstance(kwargs[arg], dict):
                kwargs[arg] = __filter_dict(kwargs[arg])
        return func_or_str(*_args, **kwargs)

    if isinstance(func_or_str, str):
        return __filter(func_or_str)
    if isinstance(func_or_str, list):
        return [__filter(item) for item in func_or_str]
    if isinstance(func_or_str, tuple):
        return (__filter(item) for item in func_or_str)
    if isinstance(func_or_str, dict):
        return __filter_dict(func_or_str)
    if isinstance(func_or_str, types.FunctionType):
        return wrapped
    return None


def enforce(action_names, object_name, **extra):
    """Fake version of the enforce decorator"""
    def wrapper_func(func):
        def wrapper_args(*args, **kwargs):
            # LOG.info("kwargs={}".format(kwargs))
            # kwargs['user_id'] = kwargs.pop('user_id', "admin")
            # LOG.info("Calling enforce on {} with args={} kwargs={}".format(func.__name__, args, kwargs))
            return func(*args, **kwargs)
        return wrapper_args
    return wrapper_func


def login(user=None, password=None, domain=None, project=None, url=None):
    start_time = time.time()
    if not user:
        user = keystone_config['user']
    if not password:
        password = keystone_config['password']
    if not domain:
        domain = keystone_config['domain']
    if not project:
        project = keystone_config['project']
    if not url:
        url = keystone_config['url']
    headers = {
        "Content-Type": "application/json"
    }
    data_auth = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "id": domain
                        },
                        "name": user,
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "id": domain
                    },
                    "name": project
                }
            }
        }
    }

    while True:
        req = requests.post("{}/auth/tokens".format(url),
                            json=data_auth, headers=headers,
                            verify=keystone_config['certificate'])

        if req.status_code in (200, 201, 204):
            headers['X-Auth-Token'] = req.headers['X-Subject-Token']
            return headers
        logger.warning("Waiting for Keystone...")
        if time.time() - start_time == 100:
            logger.error(req.text)
            raise exceptions.KeystoneError
        time.sleep(5)


def logout(headers, url=None):
    if not url:
        url = keystone_config['url']
    headers['X-Subject-Token'] = headers['X-Auth-Token']
    req = requests.delete("{}/auth/tokens".format(url), headers=headers, verify=keystone_config['certificate'])
    if req.status_code in (200, 201, 204):
        return
    logger.error(req.text)
    raise exceptions.KeystoneError


def check_token(token, url=None):
    _verify = False
    if keystone_config['certificate']:
        _verify = keystone_config['certificate']
    try:
        os.environ.pop("http_proxy")
        os.environ.pop("https_proxy")
    except KeyError:
        pass
    if not url:
        url = keystone_config['url']
    headers = {
        "Content-Type": "application/json",
        'X-Subject-Token': token,
        'X-Auth-Token': token,
    }
    if not keystone_config['check_token']:
        # TODO (asteroide): must send the admin id
        return "admin" if not token else token
    elif keystone_config['check_token'].lower() in ("false", "no", "n"):
        # TODO (asteroide): must send the admin id
        return "admin" if not token else token
    if keystone_config['check_token'].lower() in ("yes", "y", "true"):
        if token in TOKENS:
            delta = time.mktime(TOKENS[token]["expires_at"]) - time.mktime(time.gmtime())
            if delta > 0:
                return TOKENS[token]["user"]
            raise exceptions.KeystoneError
        else:
            req = requests.get("{}/auth/tokens".format(url), headers=headers, verify=_verify)
            if req.status_code in (200, 201):
                # Note (asteroide): the time stamps is not in ISO 8601, so it is necessary to delete
                # characters after the dot
                token_time = req.json().get("token").get("expires_at").split(".")
                TOKENS[token] = dict()
                TOKENS[token]["expires_at"] = time.strptime(token_time[0], "%Y-%m-%dT%H:%M:%S")
                TOKENS[token]["user"] = req.json().get("token").get("user").get("id")
                return TOKENS[token]["user"]
            logger.error("{} - {}".format(req.status_code, req.text))
            raise exceptions.KeystoneError
    elif keystone_config['check_token'].lower() == "strict":
        req = requests.head("{}/auth/tokens".format(url), headers=headers, verify=_verify)
        if req.status_code in (200, 201):
            return token
        logger.error("{} - {}".format(req.status_code, req.text))
        raise exceptions.KeystoneError
    raise exceptions.KeystoneError


def check_auth(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-Auth-Token')
        token = check_token(token)
        if not token:
            raise exceptions.AuthException
        user_id = kwargs.pop("user_id", token)
        result = function(*args, **kwargs, user_id=user_id)
        return result
    return wrapper
