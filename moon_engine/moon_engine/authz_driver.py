# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""Authorization compute Driver"""

import logging
from moon_engine.api import configuration
from moon_engine.api.authz import authz

LOGGER = logging.getLogger("moon.manager.authz_driver")


AuthzManager = None


class Driver:
    """
    Generic driver
    """

    def __init__(self, driver_name, engine_name):
        self.name = driver_name
        self.plug = configuration.get_authz_driver()
        self.driver = self.plug.Connector(driver_name, engine_name)


class AuthzDriver(Driver):
    """
    Driver for authorization computation
    """

    def __init__(self, driver_name, engine_name):
        super(AuthzDriver, self).__init__(driver_name, engine_name)
        self.engine = engine_name

    def get_authz(self, subject_name, object_name, action_name):
        """
        Get the result of the authorization process
        :param subject_name:
        :param object_name:
        :param action_name:
        :return:
        """
        raise NotImplementedError()  # pragma: no cover


def init():
    """Initialize the managers

    :return: nothing
    """
    global AuthzManager

    LOGGER.info("Initializing driver")
    conf = configuration.get_configuration("authorization")

    AuthzManager = authz.AuthzManager(
        AuthzDriver(conf['driver'], conf.get('url'))
    )
