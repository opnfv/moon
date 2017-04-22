# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import sys
from oslo_config import cfg
from oslo_log import log as logging
from moon_utilities import __version__

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

__CWD__ = os.path.dirname(os.path.abspath(__file__))


def configure(domain="moon", version=__version__, usage=""):
    # FIXME (dthom): put DEBUG as default log level doesn't work
    extra_log_level_defaults = [
        '{}=DEBUG'.format(__name__),
    ]
    # LOG.setLevel(logging.DEBUG)
    logging.set_defaults(
        default_log_levels=logging.get_default_log_levels() + extra_log_level_defaults)

    logging.register_options(CONF)
    logging.setup(CONF, domain)

    CONF.register_opts(get_opts())

    # rabbit_group = cfg.OptGroup(name='messenger',
    #                             title='Messenger options')
    # CONF.register_group(rabbit_group)
    # CONF.register_opts(get_messenger_opts(), group="messenger")

    slave_group = cfg.OptGroup(name='slave',
                               title='Messenger options')
    CONF.register_group(slave_group)
    CONF.register_opts(get_slave_opts(), group="slave")

    database_group = cfg.OptGroup(name='database',
                                  title='Database options')
    CONF.register_group(database_group)
    CONF.register_opts(get_database_opts(), group="database")

    database_configuration_group = cfg.OptGroup(name='database_configuration',
                                                title='Database configuration options')
    CONF.register_group(database_configuration_group)
    CONF.register_opts(get_database_configuration_opts(), group="database_configuration")

    orchestrator_group = cfg.OptGroup(name='orchestrator',
                                      title='Orchestrator options')
    CONF.register_group(orchestrator_group)
    CONF.register_opts(get_orchestrator_opts(), group="orchestrator")

    secrouter_group = cfg.OptGroup(name='security_router',
                                   title='Security Router options')
    CONF.register_group(secrouter_group)
    CONF.register_opts(get_security_router_opts(), group="security_router")

    manager_group = cfg.OptGroup(name='security_manager',
                                 title='Manager options')
    CONF.register_group(manager_group)
    CONF.register_opts(get_manager_opts(), group="security_manager")

    secpolicy_group = cfg.OptGroup(name='security_policy',
                                   title='Security policy options')
    CONF.register_group(secpolicy_group)
    CONF.register_opts(get_security_policy_opts(), group="security_policy")

    secfunction_group = cfg.OptGroup(name='security_function',
                                     title='Security function options')
    CONF.register_group(secfunction_group)
    CONF.register_opts(get_security_function_opts(), group="security_function")

    interface_group = cfg.OptGroup(name='interface',
                                   title='Interface options')
    CONF.register_group(interface_group)
    CONF.register_opts(get_interface_opts(), group="interface")

    keystone_group = cfg.OptGroup(name='keystone',
                                  title='Keystone options')
    CONF.register_group(keystone_group)
    CONF.register_opts(get_keystone_opts(), group="keystone")

    filename = "moon.conf"
    for _filename in (
        "/etc/moon/{}",
        "conf/{}",
        "../conf/{}",
    ):
        try:
            default_config_files = (_filename.format(filename), )
            CONF(args=sys.argv[1:],
                 project=domain,
                 # version=pbr.version.VersionInfo('keystone').version_string(),
                 version=version,
                 usage=usage,
                 default_config_files=default_config_files)
        except cfg.ConfigFilesNotFoundError:
            continue
        else:
            LOG.info("Using {} configuration file".format(_filename.format(filename)))
            return _filename.format(filename)


def get_opts():
    return [
        cfg.StrOpt('proxy',
                   default="",
                   help='Proxy server to use'),
        cfg.StrOpt('dist_dir',
                   default="",
                   help='Directory where the python packages can be found'),
        cfg.StrOpt('plugin_dir',
                   default="",
                   help='Directory where the python plugins can be found'),
        cfg.StrOpt('docker_url',
                   default="unix://var/run/docker.sock",
                   help='Docker URL to connect to.'),
        cfg.StrOpt('policy_directory',
                   default="/etc/moon/policies",
                   help='Directory containing all the intra-extension templates'),
        cfg.StrOpt('root_policy_directory',
                   default="/etc/moon/policies/policy_root",
                   help='Directory containing the Root intra-extension template'),
        cfg.StrOpt('master',
                   default="",
                   help='URL of the Moon Master'),
        cfg.StrOpt('master_login',
                   default="",
                   help='Login to log into the Moon Master'),
        cfg.StrOpt('master_password',
                   default="",
                   help='Password for the Moon Master'),
    ]


# def get_messenger_opts():
#     return [
#         cfg.StrOpt('host',
#                    default="0.0.0.0",
#                    help='RabbitMQ server name or IP.'),
#         cfg.IntOpt('port',
#                    default=8800,
#                    help='RabbitMQ server port.'),
#     ]


def get_orchestrator_opts():
    return [
        cfg.StrOpt('host',
                   default="127.0.0.1",
                   help='Host binding'),
        cfg.IntOpt('port',
                   default=38000,
                   help='Port number of the server'),
    ]


def get_slave_opts():
    return [
        cfg.StrOpt('slave_name',
                   default="",
                   help='name of the slave'),
        cfg.StrOpt('master_url',
                   default="",
                   help='URL of the RabbitMQ bus of the Master, '
                        'example: master_url=rabbit://moon:p4sswOrd1@messenger:5672/moon'),
        cfg.StrOpt('master_login',
                   default="",
                   help='login name of the master administrator, example: master_login=admin'),
        cfg.StrOpt('master_password',
                   default="",
                   help='password of the master administrator, example: master_password=XXXXXXX'),
    ]


def get_security_router_opts():
    return [
        cfg.StrOpt('container',
                   default="",
                   help='Name of the container to download (if empty build from scratch)'),
        cfg.StrOpt('host',
                   default="127.0.0.1",
                   help='Host binding'),
        cfg.IntOpt('port',
                   default=38001,
                   help='Port number of the server'),
    ]


def get_manager_opts():
    return [
        cfg.StrOpt('container',
                   default="",
                   help='Name of the container to download (if empty build from scratch)'),
        cfg.StrOpt('host',
                   default="127.0.0.1",
                   help='Host binding'),
        cfg.IntOpt('port',
                   default=38001,
                   help='Port number of the server'),
    ]


def get_security_policy_opts():
    return [
        cfg.StrOpt('container',
                   default="",
                   help='Name of the container to download (if empty build from scratch)'),
    ]


def get_security_function_opts():
    return [
        cfg.StrOpt('container',
                   default="",
                   help='Name of the container to download (if empty build from scratch)'),
    ]


def get_interface_opts():
    return [
        cfg.StrOpt('container',
                   default="",
                   help='Name of the container to download (if empty build from scratch)'),
        cfg.StrOpt('host',
                   default="127.0.0.1",
                   help='Host binding'),
        cfg.IntOpt('port',
                   default=38002,
                   help='Port number of the server'),
    ]


def get_database_opts():
    return [
        cfg.StrOpt('url',
                   default="mysql+pymysql://moonuser:password@localhost/moon",
                   help='URL of the database'),
        cfg.StrOpt('driver',
                   default="sql",
                   help='Driver binding'),
    ]


def get_database_configuration_opts():
    return [
        cfg.StrOpt('url',
                   default="",
                   help='URL of the database'),
        cfg.StrOpt('driver',
                   default="memory",
                   help='Driver binding'),
    ]


def get_keystone_opts():
    return [
        cfg.StrOpt('url',
                   default="http://localhost:35357",
                   help='URL of the Keystone manager.'),
        cfg.StrOpt('user',
                   default="admin",
                   help='Username of the Keystone manager.'),
        cfg.StrOpt('password',
                   default="nomoresecrete",
                   help='Password of the Keystone manager.'),
        cfg.StrOpt('project',
                   default="admin",
                   help='Project used to connect to the Keystone manager.'),
        cfg.StrOpt('domain',
                   default="Default",
                   help='Default domain for the Keystone manager.'),
        cfg.StrOpt('check_token',
                   default="true",
                   help='If true, yes or strict, always check Keystone tokens against the server'),
        cfg.StrOpt('server_crt',
                   default="",
                   help='If using Keystone in HTTPS mode, give a certificate filename here'),
    ]

filename = configure()


def get_docker_template_dir(templatename="template.dockerfile"):
    path = os.path.dirname(os.path.abspath(filename))
    PATHS = (
        path,
        os.path.join(path, "dockers"),
        "/etc/moon/"
        "~/.moon/"
    )
    for _path in PATHS:
        if os.path.isfile(os.path.join(_path, templatename)):
            return _path
    raise Exception("Configuration error, cannot find docker template in {}".format(PATHS))

