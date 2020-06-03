# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Plugin to request OpenStack infrastructure:
- Nova
"""

from moon_manager.plugins.moon_openstack_plugin import *

LOGGER = logging.getLogger("moon.manager.plugins.moon_nova_plugin")

PLUGIN_TYPE = "information"
_ = str

# Nova exceptions


class NovaError(MoonError):
    description = _("There is an error connecting to Nova.")
    code = 400
    title = 'Nova error'
    logger = "ERROR"


class NovaProjectError(NovaError):
    description = _("There is an error retrieving projects from the Nova service.")
    code = 400
    title = 'Nova project error'
    logger = "ERROR"


class NovaUserError(NovaError):
    description = _("There is an error retrieving users from the Nova service.")
    code = 400
    title = 'Nova user error'
    logger = "ERROR"


class NovaUserConflict(NovaUserError):
    description = _("A user with that name already exist.")
    code = 400
    title = 'Nova user error'
    logger = "ERROR"


class NovaConnector(OpenStackConnector):

    def get_items(self, item_id=None, **kwargs):
        return self._get(endpoint="/servers", _exception=NovaProjectError)

    def add_item(self, object_id=None, **kwargs):
        raise NotImplementedError()  # pragma: no cover

    def update_item(self, item_id, **kwargs):
        raise NotImplementedError()  # pragma: no cover

    def delete_item(self, item_id, **kwargs):
        raise NotImplementedError()  # pragma: no cover


class Connector(NovaConnector):
    pass
