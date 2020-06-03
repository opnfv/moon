# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
from moon_engine.api.authz.managers import Managers

logger = logging.getLogger("moon.engine.api.authz.pipeline")


class AuthzManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.AuthzManager = self

    def get_authz(self, subject_name, object_name, action_name):
        return self.driver.get_authz(subject_name=subject_name,
                                     object_name=object_name,
                                     action_name=action_name)
