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
- Nova
"""

import json
import logging
import time
import requests
from moon_manager.pip_driver import InformationDriver
from moon_manager.api.configuration import get_configuration
from moon_utilities import exceptions

LOGGER = logging.getLogger("moon.manager.plugins.global_attrs")

PLUGIN_TYPE = "information"


class AttrsConnector(InformationDriver):

    def __init__(self, driver_name, engine_name):
        self.driver_name = driver_name
        self.engine_name = engine_name
        self.conf = get_configuration("information").get("global_attrs", {})
        self.drivers = {}

    def driver(self, driver_name="file"):
        if driver_name.startswith("file"):
            if not self.drivers.get("file"):
                self.drivers["file"] = AttrsConnectorFile()
            return self.drivers["file"]
        if driver_name == "http":
            if not self.drivers.get("file"):
                self.drivers["http"] = AttrsConnectorHTTP()
            return self.drivers["http"]
        if driver_name == "mysql":
            if not self.drivers.get("file"):
                self.drivers["mysql"] = AttrsConnectorSQL()
            return self.drivers["sql"]
        if driver_name == "sqlite":
            if not self.drivers.get("file"):
                self.drivers["sqlite"] = AttrsConnectorSQL()
            return self.drivers["sql"]
        if driver_name == "driver":
            if not self.drivers.get("file"):
                self.drivers["driver"] = AttrsConnectorDriver()
            return self.drivers["driver"]

    def set_auth(self, **kwargs):
        """Set authorizations if necessary

        :param kwargs: arguments which are necessary to login to the server
        :return: headers to use
        """
        raise NotImplementedError

    def unset_auth(self, **kwargs):
        """Unset the authorization is necessary

        :param kwargs: arguments which are necessary to logout to the server
        :return: headers to use
        """
        raise NotImplementedError

    def get_objects(self, object_id=None, object_type=None, **kwargs):
        """List objects in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        if not object_type:
            object_type = list(self.conf.get("attributes").keys())
        elif isinstance(object_type, str):
            object_type = [object_type, ]

        results = {}
        for _type in object_type:
            if _type in self.conf.get("attributes"):
                driver_name = self.conf.get("attributes").get(_type).get("url").split(":")[0]
                value = self.driver(driver_name).get_object(_type, **kwargs)
                results[_type] = {
                    "id": _type,
                    "value": value,
                    "values": self.conf.get("attributes").get(_type).get("values"),
                    "default": self.conf.get("attributes").get(_type).get("default")
                }
            else:
                raise exceptions.AttributeUnknownError(
                    "Cannot find global attribute {}".format(object_type))
        return results

    def get_object(self, object_type=None, **kwargs):
        """List specific object in the server

        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        if object_type in self.conf.get("attributes"):
            driver_name = self.conf.get("attributes").get(object_type).get("url").split(":")[0]
            value = self.driver(driver_name).get_object(object_type, **kwargs)
            return {
                "id": object_type,
                "value": value,
                "values": self.conf.get("attributes").get(object_type).get("values"),
                "default": self.conf.get("attributes").get(object_type).get("default")
            }
        else:
            raise exceptions.AttributeUnknownError(
                "Cannot find global attribute {}".format(object_type))

    def add_object(self, object_id=None, object_type=None, **kwargs):
        """Add an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to add the object
        :return: the object added
        """
        if object_type in self.conf.get("attributes"):
            driver_name = self.conf.get("attributes").get(object_type).get("url").split(":")[0]
            value = self.driver(driver_name).add_object(object_id, object_type, **kwargs)
            return {
                "id": object_type,
                "value": value,
                "values": self.conf.get("attributes").get(object_type).get("values"),
                "default": self.conf.get("attributes").get(object_type).get("default")
            }
        raise exceptions.AttributeUnknownError(
            "Cannot find global attribute {}".format(object_type))

    def update_object(self, object_id, object_type=None, **kwargs):
        """Update an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to update the object
        :return: the object updated
        """
        if object_type in self.conf.get("attributes"):
            driver_name = self.conf.get("attributes").get(object_type).get("url").split(":")[0]
            value = self.driver(driver_name).update_object(object_id, object_type, **kwargs)
            return {
                "id": object_type,
                "value": value,
                "values": self.conf.get("attributes").get(object_type).get("values"),
                "default": self.conf.get("attributes").get(object_type).get("default")
            }
        raise exceptions.AttributeUnknownError(
            "Cannot find global attribute {}".format(object_type))

    def delete_object(self, object_id=None, object_type=None, **kwargs):
        """Delete an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to delete the object
        :return: True if the object has been deleted
        """
        if object_type in self.conf.get("attributes"):
            driver_name = self.conf.get("attributes").get(object_type).get("url").split(":")[0]
            value = self.driver(driver_name).delete_object(object_id, object_type, **kwargs)
            return {
                "id": object_type,
                "value": value,
                "values": self.conf.get("attributes").get(object_type).get("values"),
                "default": self.conf.get("attributes").get(object_type).get("default")
            }
        raise exceptions.AttributeUnknownError(
            "Cannot find global attribute {}".format(object_type))


class AttrsConnectorFile:

    def __init__(self):
        self.conf = get_configuration("information").get("global_attrs", {})

    def set_auth(self, **kwargs):
        """Set authorizations if necessary

        :param kwargs: arguments which are necessary to login to the server
        :return: headers to use
        """
        raise NotImplementedError

    def unset_auth(self, **kwargs):
        """Unset the authorization is necessary

        :param kwargs: arguments which are necessary to logout to the server
        :return: headers to use
        """
        raise NotImplementedError

    def get_objects(self, object_id=None, object_type=None, **kwargs):
        """List objects in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        if not object_type:
            object_type = list(self.conf.get("attributes").keys())
        elif isinstance(object_type, str):
            object_type = [object_type, ]

        for _type in object_type:
            filename = self.conf.get("attributes").get(_type).get("url").split(":")[1].strip()
            try:
                yield {_type: open(filename).read().strip()}
            except FileNotFoundError:
                LOGGER.error("Cannot find file name {}".format(filename))
                yield {_type: self.conf.get("attributes").get(_type).get("default")}

    def get_object(self, object_type, **kwargs):
        """Get specific object in the server

        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        filename = self.conf.get("attributes").get(object_type).get("url").split(":")[1].strip()
        try:
            return open(filename).read().strip()
        except FileNotFoundError:
            LOGGER.error("Cannot find file name {}".format(filename))
            return self.conf.get("attributes").get(object_type).get("default")

    def add_object(self, object_id=None, object_type=None, **kwargs):
        """Add an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to add the object
        :return: the object added
        """
        filename = self.conf.get("attributes").get(object_type).get("url").split(":")[1].strip()
        default_value = self.conf.get("attributes").get(object_type).get("default")
        open(filename, "w").write(default_value)
        return default_value

    def update_object(self, object_id, object_type=None, **kwargs):
        """Update an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to update the object
        :return: the object updated
        """
        filename = self.conf.get("attributes").get(object_type).get("url").split(":")[1].strip()
        values = self.conf.get("attributes").get(object_type).get("values")
        if object_id in values:
            open(filename, "w").write(object_id)
            return object_id
        raise exceptions.AttributeValueUnknownError(
            "The given value ({}) is not part of the authorized values ({})".format(
                object_id, ", ".join(values)))

    def delete_object(self, object_id=None, object_type=None, **kwargs):
        """Delete an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to delete the object
        :return: True if the object has been deleted
        """
        filename = self.conf.get("attributes").get(object_type).get("url").split(":")[1].strip()
        default_value = self.conf.get("attributes").get(object_type).get("default")
        open(filename, "w").write(default_value)
        return default_value


class AttrsConnectorHTTP:

    def __init__(self):
        self.conf = get_configuration("information").get("global_attrs", {})

    def set_auth(self, **kwargs):
        """Set authorizations if necessary

        :param kwargs: arguments which are necessary to login to the server
        :return: headers to use
        """
        raise NotImplementedError

    def unset_auth(self, **kwargs):
        """Unset the authorization is necessary

        :param kwargs: arguments which are necessary to logout to the server
        :return: headers to use
        """
        raise NotImplementedError

    def get_users(self, user_id=None, **kwargs):
        """List users in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to list users
        :return: a list of users
        """
        raise NotImplementedError

    def add_user(self, user_id=None, **kwargs):
        """Add a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to add a user
        :return: the user added
        """
        raise NotImplementedError

    def update_user(self, user_id, **kwargs):
        """Update a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to update the user
        :return: the user updated
        """
        raise NotImplementedError

    def delete_user(self, user_id, **kwargs):
        """Delete a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to delete the user
        :return: True if the user has been deleted
        """
        raise NotImplementedError

    def get_objects(self, object_id=None, object_type=None, **kwargs):
        """List objects in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        raise NotImplementedError

    def add_object(self, object_id=None, object_type=None, **kwargs):
        """Add an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to add the object
        :return: the object added
        """
        raise NotImplementedError

    def update_object(self, object_id, object_type=None, **kwargs):
        """Update an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to update the object
        :return: the object updated
        """
        raise NotImplementedError

    def delete_object(self, object_id=None, object_type=None, **kwargs):
        """Delete an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to delete the object
        :return: True if the object has been deleted
        """
        raise NotImplementedError


class AttrsConnectorSQL:

    def __init__(self):
        self.conf = get_configuration("information").get("global_attrs", {})

    def set_auth(self, **kwargs):
        """Set authorizations if necessary

        :param kwargs: arguments which are necessary to login to the server
        :return: headers to use
        """
        raise NotImplementedError

    def unset_auth(self, **kwargs):
        """Unset the authorization is necessary

        :param kwargs: arguments which are necessary to logout to the server
        :return: headers to use
        """
        raise NotImplementedError

    def get_users(self, user_id=None, **kwargs):
        """List users in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to list users
        :return: a list of users
        """
        raise NotImplementedError

    def add_user(self, user_id=None, **kwargs):
        """Add a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to add a user
        :return: the user added
        """
        raise NotImplementedError

    def update_user(self, user_id, **kwargs):
        """Update a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to update the user
        :return: the user updated
        """
        raise NotImplementedError

    def delete_user(self, user_id, **kwargs):
        """Delete a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to delete the user
        :return: True if the user has been deleted
        """
        raise NotImplementedError

    def get_objects(self, object_id=None, object_type=None, **kwargs):
        """List objects in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        raise NotImplementedError

    def add_object(self, object_id=None, object_type=None, **kwargs):
        """Add an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to add the object
        :return: the object added
        """
        raise NotImplementedError

    def update_object(self, object_id, object_type=None, **kwargs):
        """Update an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to update the object
        :return: the object updated
        """
        raise NotImplementedError

    def delete_object(self, object_id=None, object_type=None, **kwargs):
        """Delete an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to delete the object
        :return: True if the object has been deleted
        """
        raise NotImplementedError


class AttrsConnectorDriver:

    def __init__(self):
        self.conf = get_configuration("information").get("global_attrs", {})

    def set_auth(self, **kwargs):
        """Set authorizations if necessary

        :param kwargs: arguments which are necessary to login to the server
        :return: headers to use
        """
        raise NotImplementedError

    def unset_auth(self, **kwargs):
        """Unset the authorization is necessary

        :param kwargs: arguments which are necessary to logout to the server
        :return: headers to use
        """
        raise NotImplementedError

    def get_users(self, user_id=None, **kwargs):
        """List users in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to list users
        :return: a list of users
        """
        raise NotImplementedError

    def add_user(self, user_id=None, **kwargs):
        """Add a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to add a user
        :return: the user added
        """
        raise NotImplementedError

    def update_user(self, user_id, **kwargs):
        """Update a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to update the user
        :return: the user updated
        """
        raise NotImplementedError

    def delete_user(self, user_id, **kwargs):
        """Delete a user in the server

        :param user_id: the user name or user ID
        :param kwargs: all arguments necessary to delete the user
        :return: True if the user has been deleted
        """
        raise NotImplementedError

    def get_objects(self, object_id=None, object_type=None, **kwargs):
        """List objects in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to list the object
        :return: a list of objects
        """
        raise NotImplementedError

    def add_object(self, object_id=None, object_type=None, **kwargs):
        """Add an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to add the object
        :return: the object added
        """
        raise NotImplementedError

    def update_object(self, object_id, object_type=None, **kwargs):
        """Update an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to update the object
        :return: the object updated
        """
        raise NotImplementedError

    def delete_object(self, object_id=None, object_type=None, **kwargs):
        """Delete an object in the server

        :param object_id: the object name or user ID
        :param object_type: the object type (project, vms, ...)
        :param kwargs: all arguments necessary to delete the object
        :return: True if the object has been deleted
        """
        raise NotImplementedError


class Connector(AttrsConnector):
    pass
