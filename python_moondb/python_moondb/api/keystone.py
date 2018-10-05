# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import requests
import json
from uuid import uuid4
import logging
from python_moonutilities import exceptions, configuration
from python_moonutilities.security_functions import filter_input, login, logout
from python_moondb.api.managers import Managers

logger = logging.getLogger("moon.db.api.keystone")


class KeystoneManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.KeystoneManager = self
        conf = configuration.get_configuration("openstack/keystone")['openstack/keystone']

        self.__url = conf['url']
        self.__user = conf['user']
        self.__password = conf['password']
        self.__domain = conf['domain']
        self.__project = conf['project']
        try:
            os.environ.pop("http_proxy")
            os.environ.pop("https_proxy")
        except KeyError:
            pass

    def __get(self, endpoint, _exception=exceptions.KeystoneError):
        _headers = login()
        req = requests.get("{}{}".format(self.__url, endpoint), headers=_headers, verify=False)
        if req.status_code not in (200, 201):
            logger.error(req.text)
            raise _exception
        data = req.json()
        logout(_headers)
        return data

    def __post(self, endpoint, data=None, _exception=exceptions.KeystoneError):
        _headers = login()
        req = requests.post("{}{}".format(self.__url, endpoint),
                            data=json.dumps(data),
                            headers=_headers, verify=False)
        if req.status_code == 409:
            logger.warning(req.text)
            raise exceptions.KeystoneUserConflict
        if req.status_code not in (200, 201):
            logger.error(req.text)
            raise _exception
        data = req.json()
        logout(_headers)
        return data

    def list_projects(self):
        return self.__get(endpoint="/projects/", _exception=exceptions.KeystoneProjectError)

    @filter_input
    def create_project(self, tenant_dict):
        if "name" not in tenant_dict:
            raise exceptions.KeystoneProjectError("Cannot get the project name.")
        _project = {
            "project": {
                "description": tenant_dict['description'] if 'description' in tenant_dict else "",
                "domain_id": tenant_dict['domain'] if 'domain' in tenant_dict else "default",
                "enabled": True,
                "is_domain": False,
                "name": tenant_dict['name']
            }
        }
        return self.__post(endpoint="/projects/",
                           data=_project,
                           _exception=exceptions.KeystoneProjectError)

    @filter_input
    def get_user_by_name(self, username, domain_id="default"):
        return self.__get(endpoint="/users?name={}&domain_id={}".format(username, domain_id),
                          _exception=exceptions.KeystoneUserError)

    @filter_input
    def create_user(self, subject_dict):
        _user = {
            "user": {
                "enabled": True,
                "name": subject_dict['name'] if 'name' in subject_dict else uuid4().hex,
            }
        }
        if 'project' in subject_dict:
            _user['user']['default_project_id'] = subject_dict['project']
        if 'domain' in subject_dict:
            _user['user']['domain_id'] = subject_dict['domain']
        if 'password' in subject_dict:
            _user['user']['password'] = subject_dict['password']
        try:
            return self.__post(endpoint="/users/",
                               data=_user,
                               _exception=exceptions.KeystoneUserError)
        except exceptions.KeystoneUserConflict:
            return True
