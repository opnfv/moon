# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Plugin to request OpenStack infrastructure:
- Keystone
"""

from moon_manager.plugins.moon_openstack_plugin import *

LOGGER = logging.getLogger("moon.manager.plugins.moon_keystone_plugin")

PLUGIN_TYPE = "information"
_ = str


class KeystoneConnector(OpenStackConnector):

    def get_items(self, item_id=None, **kwargs):
        username = ""
        domain_id = ""
        if "username" in kwargs:
            username = kwargs['username']
        if "domain_id" in kwargs:
            domain_id = kwargs['domain_id']
        if username and domain_id:
            return self._get(endpoint="/users?name={}&domain_id={}".format(username, domain_id),
                             _exception=KeystoneUserError)
        elif username:
            return self._get(endpoint="/users?name={}".format(username),
                             _exception=KeystoneUserError)
        elif domain_id:
            return self._get(endpoint="/users?domain_id={}".format(domain_id),
                             _exception=KeystoneUserError)
        else:
            return self._get(endpoint="/users",
                             _exception=KeystoneUserError)

    def add_item(self, item_id=None, **kwargs):
        if 'name' not in kwargs:
            raise KeystoneError("Cannot find name in request")
        _user = {
            "user": {
                "enabled": True,
                "name": kwargs['name'],
            }
        }
        if 'project' in kwargs:
            _user['user']['default_project_id'] = kwargs['project']
        if 'domain' in kwargs:
            _user['user']['domain_id'] = kwargs['domain']
        if 'password' in kwargs:
            _user['user']['password'] = kwargs['password']
        try:
            return self._post(endpoint="/users/",
                               data=_user,
                               _exception=KeystoneUserError)
        except KeystoneUserConflict:
            return True

    def update_item(self, item_id, **kwargs):
        raise NotImplementedError()  # pragma: no cover

    def delete_item(self, item_id, **kwargs):
        raise NotImplementedError()  # pragma: no cover


class Connector(KeystoneConnector):
    pass
