# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import requests
import time
from functools import wraps
from flask import request
from oslo_log import log as logging
from python_moonutilities import exceptions, configuration


LOG = logging.getLogger(__name__)
KEYSTONE_CONFIG = configuration.get_configuration("openstack/keystone")["openstack/keystone"]
TOKENS = {}


def check_token(token, url=None):
    _verify = False
    if KEYSTONE_CONFIG['certificate']:
        _verify = KEYSTONE_CONFIG['certificate']
    try:
        os.environ.pop("http_proxy")
        os.environ.pop("https_proxy")
    except KeyError:
        pass
    if not url:
        url = KEYSTONE_CONFIG['url']
    headers = {
        "Content-Type": "application/json",
        'X-Subject-Token': token,
        'X-Auth-Token': token,
    }
    if KEYSTONE_CONFIG['check_token'].lower() in ("false", "no", "n"):
        # TODO (asteroide): must send the admin id
        return "admin" if not token else token
    if KEYSTONE_CONFIG['check_token'].lower() in ("yes", "y", "true"):
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
            LOG.error("{} - {}".format(req.status_code, req.text))
            raise exceptions.KeystoneError
    elif KEYSTONE_CONFIG['check_token'].lower() == "strict":
        req = requests.head("{}/auth/tokens".format(url), headers=headers, verify=_verify)
        if req.status_code in (200, 201):
            return token
        LOG.error("{} - {}".format(req.status_code, req.text))
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
