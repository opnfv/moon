# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
API to gather information from external component like OpenStack
"""

from uuid import uuid4
import logging
from moon_utilities.security_functions import enforce
from moon_manager.api.information.managers import Managers

LOGGER = logging.getLogger("moon.manager.information.api.information")


class InformationManager(Managers):
    """
    Manager use to get information from external components
    """

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.InformationManager = self

    def set_auth(self, **kwargs):
        """Set authorizations if necessary

        :param kwargs: arguments which are necessary to login to the server
        :return: headers to use
        """
        return self.driver.set_auth(**kwargs)

    def unset_auth(self, **kwargs):
        """Unset the authorization is necessary

        :param kwargs: arguments which are necessary to logout to the server
        :return: headers to use
        """
        return self.driver.unset_auth(**kwargs)

    @enforce("read", "pip")
    def get_items(self, item_id=None, **kwargs):
        """List items in the server

        :param item_id: the item name or item ID
        :param kwargs: all arguments necessary to list items
        :return: a list of items
        """
        return self.driver.get_items(item_id=item_id, **kwargs)

    @enforce("write", "pip")
    def add_item(self, item_id=None, **kwargs):
        """Add a item in the server

        :param item_id: the item name or item ID
        :param kwargs: all arguments necessary to add a item
        :return: the item added
        """
        if not item_id:
            item_id = uuid4().hex
        return self.driver.add_item(item_id=item_id, **kwargs)

    @enforce(("read", "write"), "pip")
    def update_item(self, item_id, **kwargs):
        """Update a item in the server

        :param item_id: the item name or item ID
        :param kwargs: all arguments necessary to update the item
        :return: the item updated
        """
        return self.driver.update_item(item_id=item_id, **kwargs)

    @enforce("write", "pip")
    def delete_item(self, item_id, **kwargs):
        """Delete a item in the server

        :param item_id: the item name or item ID
        :param kwargs: all arguments necessary to delete the item
        :return: True if the item has been deleted
        """
        return self.driver.delete_item(item_id=item_id, **kwargs)

    @enforce("read", "pip")
    def get_projects(self):
        """List projects in the server

        :return: the list of projects
        """
        return self.driver.get_projects()

    @enforce("write", "pip")
    def create_project(self, **tenant_dict):
        """Create a project in the server

        :param tenant_dict: all arguments necessary to create a project
        :return: True if the item has been deleted
        """
        return self.driver.create_project(**tenant_dict)
