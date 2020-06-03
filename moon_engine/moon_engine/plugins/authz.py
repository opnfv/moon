# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
from moon_engine.authz_driver import AuthzDriver

PLUGIN_TYPE = "authz"
LOGGER = logging.getLogger("moon.engine.plugins.authz")


class AuthzConnector(AuthzDriver):

    def __init__(self, driver_name, engine_name):
        self.driver_name = driver_name
        self.engine_name = engine_name

    def get_authz(self, subject_name, object_name, action_name):
        # FIXME: must add the real authorization engine here
        return True


class Connector(AuthzConnector):
    pass
