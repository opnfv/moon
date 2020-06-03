# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Abstract plugin to request OpenStack infrastructure
"""

import json
import logging
import time
import requests
from moon_manager.pip_driver import InformationDriver
from moon_manager.api.configuration import get_configuration
from moon_utilities.exceptions import MoonError

LOGGER = logging.getLogger("moon.manager.plugins.moon_openstack_plugin")

PLUGIN_TYPE = "information"
_ = str


# Keystone exceptions


class KeystoneError(MoonError):
    description = _("There is an error connecting to Keystone.")
    code = 400
    title = 'Keystone error'
    logger = "ERROR"


class KeystoneProjectError(KeystoneError):
    description = _("There is an error retrieving projects from the Keystone service.")
    code = 400
    title = 'Keystone project error'
    logger = "ERROR"


class KeystoneUserError(KeystoneError):
    description = _("There is an error retrieving users from the Keystone service.")
    code = 400
    title = 'Keystone user error'
    logger = "ERROR"


class KeystoneUserConflict(KeystoneUserError):
    description = _("A user with that name already exist.")
    code = 400
    title = 'Keystone user error'
    logger = "ERROR"


class OpenStackConnector(InformationDriver):

    def __init__(self, driver_name, engine_name, conf):
        self.driver_name = driver_name
        self.engine_name = engine_name
        self.opst_conf = get_configuration("information")

        if not self.opst_conf:
            raise Exception("Cannot find OpenStack configuration in configuration file")

        self.__headers = {}
        self.__user = conf.get("user", self.opst_conf['user'])
        self.__password = conf.get("password", self.opst_conf['password'])
        self.__domain = conf.get("domain", self.opst_conf['domain'])
        self.__project = conf.get("project", self.opst_conf['project'])
        self.__url = conf.get("url", self.opst_conf['url'])

    def set_auth(self, **kwargs):
        start_time = time.time()
        user = kwargs.get("user", self.opst_conf['user'])
        password = kwargs.get("password", self.opst_conf['password'])
        domain = kwargs.get("domain", self.opst_conf['domain'])
        project = kwargs.get("project", self.opst_conf['project'])
        url = kwargs.get("url", self.opst_conf['url'])
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
                                verify=kwargs.get("certificate", self.opst_conf['certificate']))

            if req.status_code in (200, 201, 204):
                self.__headers['X-Auth-Token'] = req.headers['X-Subject-Token']
                return self.__headers
            LOGGER.warning("Waiting for Keystone...")
            if time.time() - start_time == 100:
                LOGGER.error(req.text)
                raise KeystoneError
            time.sleep(5)

    def unset_auth(self, **kwargs):
        url = kwargs.get("url", self.opst_conf['url'])
        self.__headers['X-Subject-Token'] = self.__headers['X-Auth-Token']
        req = requests.delete("{}/auth/tokens".format(url), headers=self.__headers,
                              verify=kwargs.get("certificate", self.opst_conf['certificate']))
        if req.status_code in (200, 201, 204):
            return
        LOGGER.error(req.text)
        raise KeystoneError

    def _get(self, endpoint, url=None, _exception=KeystoneError):
        if not url:
            if not self.__url:
                LOGGER.warning("Cannot retrieve the URL for the OpenStack endpoint")
                return {'users': []}
            url = self.__url

        req = requests.get("{}{}".format(url, endpoint),
                           headers=self.__headers)
        if req.status_code not in (200, 201):
            LOGGER.error(req.text)
            raise _exception
        data = req.json()
        return data

    def _post(self, endpoint, url=None, data=None, _exception=KeystoneError):
        if not url:
            if not self.__url:
                LOGGER.warning("Cannot retrieve the URL for the OpenStack endpoint")
                return {'users': []}
            url = self.__url

        req = requests.post("{}{}".format(url, endpoint),
                            data=json.dumps(data),
                            headers=self.__headers)
        if req.status_code == 409:
            LOGGER.warning(req.text)
            raise KeystoneUserConflict
        if req.status_code not in (200, 201):
            LOGGER.error(req.text)
            raise _exception
        data = req.json()
        return data

    def create_project(self, **tenant_dict):
        if "name" not in tenant_dict:
            raise KeystoneProjectError("Cannot get the project name.")
        _project = {
            "project": {
                "description": tenant_dict['description'],
                "domain_id": tenant_dict['domain'],
                "enabled": tenant_dict['enabled'],
                "is_domain": tenant_dict['is_domain'],
                "name": tenant_dict['name']
            }
        }
        return self._post(endpoint="/projects/",
                          url=self.opst_conf["url"],
                          data=_project,
                          _exception=KeystoneProjectError)

    def get_projects(self):
        return self._get(endpoint="/projects/", url=self.opst_conf["url"], _exception=KeystoneProjectError)

    def get_items(self, item_id=None, **kwargs):
        raise NotImplementedError()  # pragma: no cover

    def add_item(self, item_id=None, **kwargs):
        raise NotImplementedError()  # pragma: no cover

    def update_item(self, item_id, **kwargs):
        raise NotImplementedError()  # pragma: no cover

    def delete_item(self, item_id, **kwargs):
        raise NotImplementedError()  # pragma: no cover
