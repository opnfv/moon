# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""Configuration API"""
import hug.interface
import os
import logging
import logging.config
import yaml
import copy
from importlib.machinery import SourceFileLoader

LOGGER = logging.getLogger("moon.engine.api.configuration")
__CONF = {}
CONF_FILE = ""


def init_logging(log_file=None):
    """Initialize the logging system

    :return: nothing
    """
    logging_conf = get_configuration(key='logging', file=log_file)
    if get_configuration(key='debug', default=False):
        logging_conf.get("handlers", {}).get("console", {})['level'] = logging.DEBUG
        LOGGER.warning("Setting debug to True!")
    logging.config.dictConfig(logging_conf)


def get_plugins_by_type(plugin_type):
    """

    :param plugin_type:
    :return:
    """
    plugins_dir = __CONF["plugins"]["directory"]
    LOGGER.info("Getting all plugins for {}".format(plugin_type))
    import moon_engine.plugins
    import glob
    for plugname in glob.glob(os.path.join(moon_engine.plugins.__path__[0], "*.py")):
        try:
            plugname = os.path.basename(plugname)[:-3]
            plug = __import__("moon_engine.plugins.{}".format(plugname), fromlist=["plugins", ])
            if getattr(plug, "PLUGIN_TYPE", "") == plugin_type:
                yield plug
            LOGGER.debug("Plug {} loaded".format(plugname))
        except ModuleNotFoundError:
            pass
    for plugname in glob.glob(os.path.join(plugins_dir, "*.py")):
        m = SourceFileLoader("myplugs", os.path.join(plugins_dir, plugname+".py"))
        plug = m.load_module()
        if getattr(plug, "PLUGIN_TYPE", "") == plugin_type:
            yield plug
        LOGGER.debug("Plug {} loaded".format(plugname))


def load_plugin(plugname):
    """Load a python module

    :param plugname: the name of the module to load
    :return: a reference to the module
    """
    plugins_dir = __CONF["plugins"]["directory"]
    LOGGER.info(f"load_plugin {plugname}")
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


def get_authz_driver():
    """Load and check the plugin module

    :return: a reference to the module
    """
    plug = load_plugin(__CONF["authorization"]["driver"])
    if plug.PLUGIN_TYPE != "authz":
        raise Exception("Trying to load a bad Authz plugin (got {} plugin instead)".format(
            plug.PLUGIN_TYPE))
    if "Connector" not in dir(plug):
        raise Exception("Trying to load a bad Authz plugin (cannot find Connector)")
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


def get_pipeline_driver():
    """Load and check the plugin module

    :return: a reference to the module
    """
    plug = load_plugin(__CONF["information"]["driver"])
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
    for _filename in (filename, "moon.conf", "moon.yaml"):
        for _dir in (
                "{}",
                "/conf/{}",
                "../{}",
                "../conf/{}",
                "/etc/moon/{}",
                "conf/{}",
        ):
            _file = _dir.format(_filename)
            try:
                data_config = yaml.safe_load(open(_file))
            except FileNotFoundError:
                data_config = None
                continue
            else:
                LOGGER.warning("Configuration file: {}".format(_file))
                break
        if data_config:
            break
    if not data_config:
        LOGGER.error("Configuration file not found ({})...".format(filename))
        raise Exception("Configuration file not found ({})...".format(filename))
    return data_config


def set_configuration(conf):
    """ Force the configuration dictionary

    :param conf: the configuration dictionary
    :return: nothing
    """
    global __CONF
    __CONF = conf


def reload_configuration():
    global __CONF, CONF_FILE
    __CONF = None
    set_configuration(search_config_file(CONF_FILE))


@hug.cli("get_conf")
@hug.local()
def get_configuration(key=None, default=None, file=None):
    """
    List configuration attributes
    :return: JSON configuration value
    """
    global __CONF
    if not __CONF:
        if file:
            __CONF = search_config_file(file)
        else:
            __CONF = search_config_file("moon.yaml")
        init_logging()
    if not key:
        # TODO: delete passwords!
        return copy.deepcopy(__CONF)
    else:
        return copy.deepcopy(__CONF.get(key, default))
