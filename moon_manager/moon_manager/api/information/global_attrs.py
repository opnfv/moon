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

LOGGER = logging.getLogger("moon.manager.information.global_attrs")


class GlobalAttrsManager(Managers):
    """
    Manager use to get information from external components
    """

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.GlobalAttrsManager = self

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
    def get_users(self, user_id=None, **kwargs):
        """List users in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to list users
        :return: a list of users
        """
        return self.driver.get_users(user_id=user_id, **kwargs)

    @enforce("write", "pip")
    def add_user(self, user_id=None, **kwargs):
        """Add a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to add a user
        :return: the user added
        """
        if not user_id:
            user_id = uuid4().hex
        return self.driver.add_user(user_id=user_id, **kwargs)

    @enforce(("read", "write"), "pip")
    def update_user(self, user_id, **kwargs):
        """Update a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to update the user
        :return: the user updated
        """
        return self.driver.update_user(user_id=user_id, **kwargs)

    @enforce("write", "pip")
    def delete_user(self, user_id, **kwargs):
        """Delete a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to delete the user
        :return: True if the user has been deleted
        """
        return self.driver.delete_user(user_id=user_id, **kwargs)

    @enforce("read", "pip")
    def get_objects(self, object_id=None, object_type=None, **kwargs):
        """List objects in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        return self.driver.get_objects(object_id=object_id, object_type=object_type, **kwargs)

    @enforce("read", "pip")
    def get_object(self, object_type, **kwargs):
        """List objects in the server

        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        return self.driver.get_object(object_type=object_type, **kwargs)

    @enforce("write", "pip")
    def add_object(self, object_id=None, object_type=None, **kwargs):
        """Add an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to add the object
        :return: the object added
        """
        if not object_id:
            object_id = uuid4().hex
        return self.driver.add_object(object_id=object_id, object_type=object_type, **kwargs)

    @enforce(("read", "write"), "pip")
    def update_object(self, object_id, object_type=None, **kwargs):
        """Update an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to update the object
        :return: the object updated
        """
        return self.driver.update_object(object_id=object_id, object_type=object_type, **kwargs)

    @enforce("write", "pip")
    def delete_object(self, object_id=None, object_type=None, **kwargs):
        """Delete an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to delete the object
        :return: True if the object has been deleted
        """
        return self.driver.delete_object(object_id=object_id, object_type=object_type, **kwargs)
