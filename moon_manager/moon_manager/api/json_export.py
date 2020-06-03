# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
import logging
from moon_manager import db_driver as driver
from moon_utilities.auth_functions import api_key_authentication
from moon_utilities.json_utils import JsonExport

logger = logging.getLogger("moon.manager.api." + __name__)


class Export(object):

    @staticmethod
    @hug.get("/export", requires=api_key_authentication)
    def get(authed_user: hug.directives.user = None):
        """Import file.

        :param authed_user: user ID who do the request
        :return: {

        }
        :internal_api:
        """
        json_file = JsonExport(driver_name="db", driver=driver).export_json(
            moon_user_id=authed_user)
        return {"content": json_file}
