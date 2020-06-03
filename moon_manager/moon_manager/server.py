# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



import hug
import logging
from moon_manager.api import status, logs, configuration, pdp, policy, slave, auth, \
    perimeter, assignments, meta_data, meta_rules, models, \
    json_import, json_export, rules, data, attributes
from moon_manager import db_driver,orchestration_driver
from moon_utilities.auth_functions import init_db
from falcon.http_error import HTTPError
from moon_manager.api import ERROR_CODE
from moon_utilities import exceptions
LOGGER = logging.getLogger("moon.manager.server")
configuration.init_logging()


@hug.response_middleware()
def CORS(request, response, resource):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE, PATCH')
    response.set_header(
        'Access-Control-Allow-Headers',
        'Authorization,Keep-Alive,User-Agent,x-api-key'
        'If-Modified-Since,Cache-Control,Content-Type,x-api-key'
    )
    response.set_header(
        'Access-Control-Expose-Headers',
        'Authorization,Keep-Alive,User-Agent,'
        'If-Modified-Since,Cache-Control,Content-Type'
    )
    if request.method == 'OPTIONS':
        response.set_header('Access-Control-Max-Age', 1728000)
        response.set_header('Content-Type', 'text/plain charset=UTF-8')
        response.set_header('Content-Length', 0)
        response.status_code = hug.HTTP_204


@hug.startup()
def add_data(api):
    """Adds initial data to the api on startup"""
    LOGGER.warning("Starting the server and initializing data")
    init_db(configuration.get_configuration("management").get("token_file"))
    db_driver.init()
    orchestration_driver.init()


def __get_status_code(exception):
    if isinstance(exception, HTTPError):
        return exception.status
    status_code = getattr(exception, "code", 500)
    if status_code in ERROR_CODE:
        status_code = ERROR_CODE[status_code]
    else:
        status_code = hug.HTTP_500
    return status_code


@hug.exception(exceptions.MoonError)
def handle_custom_exceptions(exception, response):
    response.status = __get_status_code(exception)
    error_message = {"result": False,
                     'message': str(exception),
                     "code": getattr(exception, "code", 500)}
    LOGGER.exception(exception)
    return error_message


@hug.exception(Exception)
def handle_exception(exception, response):
    response.status = __get_status_code(exception)
    LOGGER.exception(exception)
    return {"result": False, 'message': str(exception), "code": getattr(exception, "code", 500)}


@hug.extend_api()
def with_other_apis():
    return [status, logs, configuration, pdp, policy, slave, auth,
            perimeter, assignments, meta_data, meta_rules, models, json_import, json_export,
            rules, data, attributes]


@hug.static('/static')
def static_front():
    return (configuration.get_configuration("dashboard").get("root"), )
