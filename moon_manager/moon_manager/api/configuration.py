# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""Configuration API"""
import glob
import hug.interface
import json
import logging
import logging.config
import os
import requests
import sys
import yaml
import importlib
from importlib.machinery import SourceFileLoader
from moon_utilities.auth_functions import init_db, get_api_key_for_user

LOGGER = logging.getLogger("moon.manager.api.configuration")
__CONF = {}


def init_logging():
    """Initialize the logging system

    :return: nothing
    """
    logging_conf = get_configuration(key='logging')
    if get_configuration(key='debug', default=False):
        logging_conf.get("handlers", {}).get("console", {})['level'] = logging.DEBUG
        LOGGER.info("Setting debug to True!")
    logging.config.dictConfig(logging_conf)


def load_plugin(plugname):
    """Load a python module

    :param plugname: the name of the module to load
    :return: a reference to the module
    """
    plugins_dir = __CONF["plugins"]["directory"]
    try:
        return __import__(plugname, fromlist=["plugins", ])
    except ImportError as e:
        LOGGER.warning("Cannot import module ({})".format(e))
        try:
            m = SourceFileLoader("myplugs", os.path.join(plugins_dir, plugname+".py"))
            return m.load_module()
        except ImportError as e:
            LOGGER.error("Error in importing plugin {} from {}".format(plugname, plugins_dir))
            LOGGER.exception(e)


def get_db_driver():
    """Load and check the plugin module

    :return: a reference to the module
    """
    plug = load_plugin(__CONF["database"]["driver"])
    if plug.PLUGIN_TYPE != "db":
        raise Exception("Trying to load a bad DB plugin (got {} plugin instead)".format(
            plug.PLUGIN_TYPE))
    if "Connector" not in dir(plug):
        raise Exception("Trying to load a bad DB plugin (cannot find Connector)")
    return plug


def get_orchestration_driver():
    """Load and check the plugin module

    :return: a reference to the module
    """
    plug = load_plugin(__CONF["orchestration"]["driver"])
    if plug.PLUGIN_TYPE != "orchestration":
        raise Exception("Trying to load a bad Orchestration plugin (got {} plugin instead)".format(
            plug.PLUGIN_TYPE))
    if "Connector" not in dir(plug):
        raise Exception("Trying to load a bad Orchestration plugin (cannot find Connector)")
    return plug


def get_information_driver(driver_name):
    """Load and check the plugin module

    :return: a reference to the module
    """
    plug = load_plugin(driver_name)
    if plug.PLUGIN_TYPE != "information":
        raise Exception("Trying to load a bad Information plugin (got {} plugin instead)".format(
            plug.PLUGIN_TYPE))
    if "Connector" not in dir(plug):
        raise Exception("Trying to load a bad Information plugin (cannot find Connector)")
    return plug


def get_global_attrs_driver():
    """Load and check the plugin module

    :return: a reference to the module
    """
    driver_name = __CONF["information"].get("global_attrs", {}).get("driver")
    if not driver_name:
        return
    plug = load_plugin(driver_name)
    if plug.PLUGIN_TYPE != "information":
        raise Exception("Trying to load a bad Information plugin (got {} plugin instead)".format(
            plug.PLUGIN_TYPE))
    if "Connector" not in dir(plug):
        raise Exception("Trying to load a bad Information plugin (cannot find Connector)")
    return plug


def search_config_file(filename):
    """Look for the configuration file

    :param filename: a filename to search for
    :return: the content of the configuration file
    """
    data_config = None
    for _dir in (
            "{}",
            "/conf/{}",
            "../{}",
            "../conf/{}",
            "/etc/moon/{}",
            "conf/{}",
    ):
        for _filename in (filename, "moon.conf", "moon.yaml"):
            _file = _dir.format(_filename)
            try:
                data_config = yaml.safe_load(open(_file))
            except FileNotFoundError:
                data_config = None
                continue
            else:
                break
        if data_config:
            LOGGER.warning("Using {} as configuration file".format(_file))
            break
    if not data_config:
        raise Exception("Configuration file not found...")
    return data_config


def set_configuration(conf):
    """ Force the configuration dictionary

    :param conf: the configuration dictionary
    :return: nothing
    """
    global __CONF
    __CONF = conf


@hug.cli("get_conf")
@hug.local()
@hug.get("/conf")
@hug.get("/conf/{key}")
def get_configuration(key=None, default=None):
    """
    List configuration attributes
    :return: JSON configuration output
    """
    global __CONF
    if not __CONF:
        __CONF = search_config_file("moon.yaml")
        init_logging()
    if not key:
        # TODO: delete passwords!
        return __CONF
    else:
        return __CONF.get(key, default)


@hug.cli("import_json")
def import_json(filename):
    """
    Import data in json file
    """
    LOGGER.info("Importing policy from {}".format(filename))
    db_conf = get_configuration(key='management')
    init_db(db_conf.get("token_file"))
    manager_api_key = get_api_key_for_user("admin")
    try:
        dict_to_import = json.loads(open(filename).read())
    except json.JSONDecodeError as e:
        LOGGER.error("Error in decoding the input file")
        LOGGER.exception(e)
    else:
        req = requests.post("{}/import".format(db_conf.get("url")),
                            data=json.dumps(dict_to_import),
                            headers={
                                "x-api-key": manager_api_key,
                                "Content-Type": "application/json"
                            })
        if req.status_code == 200:
            LOGGER.warning("Import OK!")
            parsed = json.loads(req.content)
            LOGGER.info("Response: {}".format(json.dumps(parsed, indent=4, sort_keys=True)))
        else:
            LOGGER.error("Error when importing data: {} {}".format(req.status_code, req.content))


@hug.cli("init_db")
@hug.local()
def init_database():
    """Initialize the database

    :return: nothing
    """
    LOGGER.info("Initialize the database")
    cwd = os.getcwd()
    db_conf = get_configuration(key='database')
    migration_dir = db_conf.get("migration_dir", ".")
    migration_files = glob.glob(os.path.join(migration_dir, "*[0-9][0-9][0-9].py"))
    migration_files.sort()
    if not migration_files:
        # the migration_dir is a python module so we must find the files inside this dir
        mod = __import__(migration_dir, fromlist=[migration_dir.split(".")[-1], ])
        migration_files = glob.glob(os.path.join(mod.__path__[0], "*[0-9][0-9][0-9].py"))
    for filename in migration_files:
        # we execute the upgrade/downgrade functions inside each file
        os.chdir(os.path.dirname(filename))
        # we add the current directory in order to import the file
        sys.path.append("")
        mod = importlib.import_module(os.path.basename(filename.replace(".py", "")))
        # TODO: manage the downgrade function
        mod.upgrade(db_conf.get("url"))
    os.chdir(cwd)
