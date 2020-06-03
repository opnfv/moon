# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
from moon_engine.api.pipeline.validator import Validator


class Authz(object):

    @staticmethod
    @hug.local()
    @hug.get("/authz/{subject_name}/{object_name}/{action_name}")
    def get(subject_name: hug.types.text, object_name: hug.types.text,
            action_name: hug.types.text, response):
        """Get a response on Main Authorization request

            :param subject_name: name of the subject or the request
            :param object_name: name of the object
            :param action_name: name of the action
            :return:
                "result": {true or false }
            :internal_api: authz
            """

        validator = Validator()
        response.status = validator.authz(subject_name, object_name, action_name)
