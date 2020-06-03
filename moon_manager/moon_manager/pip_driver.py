# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Drivers fot the Policy Information Point
"""

import logging
from moon_manager.api import configuration
from moon_manager.api.information import information, global_attrs

LOGGER = logging.getLogger("moon.manager.pip_driver")


InformationManager = None
AttrsManager = None


class Driver:
    """
    Generic driver
    """

    def __init__(self, driver_name, engine_name, conf={}):
        self.name = driver_name
        self.plug = configuration.get_information_driver(driver_name)
        if self.plug:
            self.driver = self.plug.Connector(driver_name, engine_name, conf)
        else:
            self.driver = VoidConnector(driver_name, engine_name)


class InformationDriver(Driver):
    """
    Driver for information retrieval for external components like OpenStack
    """

    def __init__(self, driver_name, engine_name, conf):
        super(InformationDriver, self).__init__(driver_name, engine_name, conf)
        self.engine = engine_name

    def set_auth(self, **kwargs):
        """Set authorizations if necessary

        :param kwargs: arguments which are necessary to login to the server
        :return: headers to use
        """
        raise NotImplementedError()  # pragma: no cover

    def unset_auth(self, **kwargs):
        """Unset the authorization is necessary

        :param kwargs: arguments which are necessary to logout to the server
        :return: headers to use
        """
        raise NotImplementedError()  # pragma: no cover

    def get_items(self, item_id=None, **kwargs):
        """List items in the server

        :param item_id: the item name or item ID
        :param kwargs: all arguments necessary to list items
        :return: a list of items
        """
        raise NotImplementedError()  # pragma: no cover

    def add_item(self, item_id=None, **kwargs):
        """Add a item in the server

        :param item_id: the item name or item ID
        :param kwargs: all arguments necessary to add a item
        :return: the item added
        """
        raise NotImplementedError()  # pragma: no cover

    def update_item(self, item_id, **kwargs):
        """Update a item in the server

        :param item_id: the item name or item ID
        :param kwargs: all arguments necessary to update the item
        :return: the item updated
        """
        raise NotImplementedError()  # pragma: no cover

    def delete_item(self, item_id, **kwargs):
        """Delete a item in the server

        :param item_id: the item name or item ID
        :param kwargs: all arguments necessary to delete the item
        :return: True if the item has been deleted
        """
        raise NotImplementedError()  # pragma: no coverl


class GlobalAttrsDriver:
    """
    Driver for global attributes in Moon
    """

    def __init__(self, driver_name, engine_name):
        self.name = driver_name
        self.plug = configuration.get_global_attrs_driver()
        if self.plug:
            self.driver = self.plug.Connector(driver_name, engine_name)
        else:
            self.driver = VoidConnector(driver_name, engine_name)
        self.engine = engine_name

    def set_auth(self, **kwargs):
        """Set authorizations if necessary

        :param kwargs: arguments which are necessary to login to the server
        :return: headers to use
        """
        raise NotImplementedError()  # pragma: no cover

    def unset_auth(self, **kwargs):
        """Unset the authorization is necessary

        :param kwargs: arguments which are necessary to logout to the server
        :return: headers to use
        """
        raise NotImplementedError()  # pragma: no cover

    def get_users(self, user_id=None, **kwargs):
        """List users in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to list users
        :return: a list of users
        """
        raise NotImplementedError()  # pragma: no cover

    def add_user(self, user_id=None, **kwargs):
        """Add a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to add a user
        :return: the user added
        """
        raise NotImplementedError()  # pragma: no cover

    def update_user(self, user_id, **kwargs):
        """Update a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to update the user
        :return: the user updated
        """
        raise NotImplementedError()  # pragma: no cover

    def delete_user(self, user_id, **kwargs):
        """Delete a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to delete the user
        :return: True if the user has been deleted
        """
        raise NotImplementedError()  # pragma: no cover

    def get_objects(self, object_id=None, object_type=None, **kwargs):
        """List objects in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        raise NotImplementedError()  # pragma: no cover

    def get_object(self, object_type=None, **kwargs):
        """List a specific object in the server

        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        raise NotImplementedError()  # pragma: no cover

    def add_object(self, object_id=None, object_type=None, **kwargs):
        """Add an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to add the object
        :return: the object added
        """
        raise NotImplementedError()  # pragma: no cover

    def update_object(self, object_id, object_type=None, **kwargs):
        """Update an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to update the object
        :return: the object updated
        """
        raise NotImplementedError()  # pragma: no cover

    def delete_object(self, object_id, object_type=None, **kwargs):
        """Delete an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to delete the object
        :return: True if the object has been deleted
        """
        raise NotImplementedError()  # pragma: no cover


class VoidConnector(InformationDriver):
    """
    Driver for information retrieval for external components like OpenStack
    """

    def __init__(self, driver_name, engine_name):
        self.engine = engine_name

    def set_auth(self, **kwargs):
        """Set authorizations if necessary

        :param kwargs: arguments which are necessary to login to the server
        :return: headers to use
        """
        return

    def unset_auth(self, **kwargs):
        """Unset the authorization is necessary

        :param kwargs: arguments which are necessary to logout to the server
        :return: headers to use
        """
        return

    def get_users(self, user_id=None, **kwargs):
        """List users in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to list users
        :return: a list of users
        """
        return {}

    def add_user(self, user_id=None, **kwargs):
        """Add a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to add a user
        :return: the user added
        """
        return {}

    def update_user(self, user_id, **kwargs):
        """Update a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to update the user
        :return: the user updated
        """
        return {}

    def delete_user(self, user_id, **kwargs):
        """Delete a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to delete the user
        :return: True if the user has been deleted
        """
        return {}

    def get_objects(self, object_id=None, object_type=None, **kwargs):
        """List objects in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        return {}

    def add_object(self, object_id=None, object_type=None, **kwargs):
        """Add an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to add the object
        :return: the object added
        """
        return {}

    def update_object(self, object_id, object_type=None, **kwargs):
        """Update an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to update the object
        :return: the object updated
        """
        return {}

    def delete_object(self, object_id, object_type=None, **kwargs):
        """Delete an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to delete the object
        :return: True if the object has been deleted
        """
        return {}


def init():
    """Initialize the managers

    :return: nothing
    """
    global InformationManager, AttrsManager

    InformationManager = {"subjects": [], "objects": [], "actions": []}

    LOGGER.info("Initializing driver")
    conf = configuration.get_configuration("information")

    for category in InformationManager:
        if category not in conf:
            continue
        drivers = conf.get(category).get("drivers")
        for driver in drivers:
            InformationManager[category].append(
                information.InformationManager(
                    InformationDriver(driver, drivers[driver].get("url"), conf[category]["drivers"].get(driver, {}))
                )
            )

    conf = configuration.get_configuration("information").get("global_attrs")

    AttrsManager = global_attrs.GlobalAttrsManager(
        GlobalAttrsDriver(conf['driver'], "")
    )


init()
