# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



from falcon.http_error import HTTPError
import hug
import logging.config
import json
import re
import requests
import sys
from uuid import uuid4
from moon_engine.api import ERROR_CODE
from moon_engine.api import status, logs, import_json, configuration
from moon_utilities import exceptions
from moon_utilities import auth_functions
from moon_utilities import json_utils
from moon_cache import cache
from moon_engine import authz_driver

LOGGER = logging.getLogger("moon.engine.server")
CACHE = None


@hug.directive()
def server_uuid(default="", **kwargs):
    """
    Hug directive allowing to get the UUID of the component everywhere
    :param default:
    :param kwargs:
    :return: UUID of the component
    """
    return configuration.get_configuration("uuid")


def get_updates_from_manager():
    """
    Request the Manager to get all data from the database
    :return: None
    """
    LOGGER.info("Retrieving all data from Manager")
    for attribute in (
        "pdp",
        "models",
        "policies",
        "subjects",
        "objects",
        "actions",
        "subject_categories",
        "object_categories",
        "action_categories",
        "subject_assignments",
        "object_assignments",
        "action_assignments",
        "meta_rules",
        # "rules",
    ):
        # Note: force updates by getting attributes
        LOGGER.info("Retrieving {} from manager {}".format(
            attribute, configuration.get_configuration("manager_url")))
        getattr(CACHE, attribute)


def get_updates_from_local_conf():
    """
    Read the local data file and update the cache
    :return: None
    """
    filename = configuration.get_configuration("data")
    LOGGER.info("Retrieving all data from configuration ({})".format(filename))
    data = json.load(open(filename))
    LOGGER.debug("keys={}".format(list(data.keys())))
    tool = json_utils.JsonImport(driver_name="cache", driver=CACHE)
    tool.import_json(body=data)


def get_attributes_from_config(filename):
    """
    Retrieve the configuration from the file given in the command line
    :param filename: filename of the configuration file
    :return: None
    """
    # TODO: manage the case if the filename attribute doesn't contain a true filename
    #       => case if it doesn't start with Gunicorn
    #       => generate a temporary RAM file and point to the moon.yaml in the source code
    for line in open(filename):
        _match_conf = re.match(r"moon\s*=\s*\"(.+)\"", line)
        if _match_conf:
            yaml_filename = _match_conf.groups()[0]
            configuration.CONF_FILE = yaml_filename
            _conf = configuration.search_config_file(yaml_filename)
            break
    else:
        LOGGER.warning("Cannot find Moon configuration filename in {}".format(filename))
        _conf = configuration.search_config_file("moon.yaml")

    configuration.set_configuration(_conf)


def get_bind_from_configfile(filename):
    """
    Retrieve the binding configuration from the file given in the command line
    :param filename: filename of the configuration file
    :return: URL
    """
    # TODO: manage the case if the filename attribute doesn't contain a true filename
    #       => case if it doesn't start with Gunicorn
    #       => case during tests
    #       => generate a temporary RAM file and point to the moon.yaml in the source code
    for line in open(filename):
        _match_conf = re.match(r"bind\s*=\s*\"(.+)\"", line)
        if _match_conf:
            return "http://" + _match_conf.groups()[0].replace("0.0.0.0", "127.0.0.1")  # nosec
    else:
        LOGGER.warning("Cannot find binding configuration in {}".format(filename))


def init_logging_system():
    """
    Initialize the logging system
    either by the configuration given in the configuration file
    either by the configuration in the Manager
    :return: None
    """
    logging_conf = configuration.get_configuration("logging")
    manager_url = configuration.get_configuration("manager_url")
    if logging_conf:
        configuration.init_logging()
    elif manager_url:
        req = requests.get("{}/config".format(manager_url))
        if req.status_code != 200:
            raise Exception("Error getting configuration data "
                            "from manager (code={})".format(req.status_code))
        logging.config.dictConfig(req.json().get("logging", {}))


def get_policy_configuration_from_manager():
    """
    Retrieve all data from the Manager
    :return: None
    """
    pdp_id = CACHE.get_pdp_from_vim_project(configuration.get_configuration("uuid"))
    CACHE.update(pdp_id=pdp_id)


def init_pipeline():
    """
    Initialize the pipeline configuration
    :return: None
    """
    if configuration.get_configuration("management").get("url"):
        get_policy_configuration_from_manager()


def initialize():
    """Adds initial data to the api on startup"""
    global CACHE
    LOGGER.warning("Starting the server and initializing data")
    filename = sys.argv[-1]
    try:
        get_attributes_from_config(filename)
    except FileNotFoundError:
        LOGGER.warning("{} file not found".format(filename))
    except IsADirectoryError:
        LOGGER.warning("{} file is a directory.".format(filename))

    init_logging_system()

    LOGGER.info("management={}".format(configuration.get_configuration("management")))
    auth_functions.init_db(configuration.get_configuration("management").get("token_file"))
    CACHE = cache.Cache.getInstance(
        manager_url=configuration.get_configuration("management").get('url'),
        incremental=configuration.get_configuration("incremental_updates"),
        manager_api_key=configuration.get_configuration("api_token"))

    if configuration.get_configuration("type") == "pipeline":
        init_pipeline()

    if not configuration.get_configuration("incremental_updates"):
        if configuration.get_configuration("manager_url"):
            get_updates_from_manager()
        elif configuration.get_configuration("data"):
            get_updates_from_local_conf()
    auth_functions.add_user("admin", uuid4().hex)
    # NOTE: the password is not saved anywhere but
    #       the API key is printed in the log
    #       and is xor-ed with the Manager API key
    api_key = auth_functions.get_api_key_for_user("admin")
    LOGGER.info(f"api_key={api_key}")
    LOGGER.info(f"configuration.get_configuration('api_token')={configuration.get_configuration('api_token')}")
    try:
        encrypt_key = auth_functions.xor_encode(api_key,
                                                configuration.get_configuration("api_token"))
    except exceptions.EncryptError:
        encrypt_key = ""
    try:
        local_server = get_bind_from_configfile(filename)
        CACHE.set_current_server(url=local_server, api_key=api_key)
    except (FileNotFoundError, IsADirectoryError):
        LOGGER.warning("Cannot find configuration file {}".format(filename))
    LOGGER.critical("APIKEY={}".format(encrypt_key))
    authz_driver.init()


def __get_status_code(exception):
    """
    Return the status code to send depending on the exception thrown
    :param exception: the exception that will be sent
    :return:
    """
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
    """
    Handle Moon exceptions
    :param exception: the exception that has been raised
    :param response: the response to send to the client
    :return: JSON data to send to the client
    """
    response.status = __get_status_code(exception)
    error_message = {"result": False,
                     'message': str(exception),
                     "code": getattr(exception, "code", 500)}
    LOGGER.exception(exception)
    return error_message


@hug.exception(Exception)
def handle_exception(exception, response):
    """
    Handle general exceptions
    :param exception: the exception that has been raised
    :param response: the response to send to the client
    :return: JSON data to send to the client
    """
    response.status = __get_status_code(exception)
    LOGGER.exception(exception)
    return {"result": False, 'message': str(exception), "code": getattr(exception, "code", 500)}


def get_api_from_plugins(api_type):
    return configuration.get_plugins_by_type(api_type)


@hug.extend_api()
def with_other_apis():
    """
    Give to Hug all available APIs
    :return: list of APIs
    """
    initialize()
    _type = configuration.get_configuration("type")
    if _type == "wrapper":
        from moon_engine.api.wrapper.api import pipeline
        from moon_engine.api.wrapper.api import update as wrapper_update
        from moon_engine.api.wrapper.api import authz as wrapper_authz
        LOGGER.info("Starting the Wrapper API interfaces")
        return [status, logs, import_json, wrapper_update, pipeline, wrapper_authz] + \
            list(configuration.get_plugins_by_type("wrapper_api"))
    elif _type == "pipeline":
        from moon_engine.api.pipeline import update as pipeline_update
        from moon_engine.api.pipeline import authz as pipeline_authz
        LOGGER.info("Starting the Pipeline API interfaces")
        return [status, logs, import_json, pipeline_update, pipeline_authz] + \
            list(configuration.get_plugins_by_type("engine_api"))
    raise Exception("The type of component must be 'wrapper' or 'pipeline' (got {} instead)".format(
        _type
    ))


