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
from moon_utilities.json_utils import JsonImport
from moon_utilities.auth_functions import api_key_authentication


LOGGER = logging.getLogger("moon.manager.api." + __name__)

INST_CALLBACK = 0
DATA_CALLBACK = 1
ASSIGNMENT_CALLBACK = 2
CATEGORIES_CALLBACK = 3


class JsonImportAPI(object):

    @staticmethod
    @hug.post("/import", requires=api_key_authentication)
    def post(request, body, authed_user: hug.directives.user = None):
        """
        Import data inside the database
        :param request: the request send by the user
        :param body: the content of the request
        :param authed_user: the name of the authenticated user
        :return: "Import ok !" (if import is OK)
        :raises multiple exceptions depending on the context
        """
        json_import_ob = JsonImport(driver_name="db", driver=driver)
        imported_data = json_import_ob.import_json(moon_user_id=authed_user, request=request, body=body)
        LOGGER.info('Imported data: {}'.format(imported_data))
        return imported_data
