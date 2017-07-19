# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
# from oslo_config import cfg
from oslo_log import log as logging
# from moon_utilities import options  # noqa
from moon_consul.http_server import HTTPServer

LOG = logging.getLogger(__name__)
# CONF = cfg.CONF
# DOMAIN = "moon_consul"

# __CWD__ = os.path.dirname(os.path.abspath(__file__))


class Configuration:
    DB_URL = None
    DB_DRIVER = None
    TRANSPORT_URL = None
    DOCKER_URL = None
    SLAVE_NAME = None
    MASTER_URL = None
    MASTER_LOGIN = None
    MASTER_PASSWORD = None
    INTERFACE_PORT = None
    CONSUL_HOST = None
    CONSUL_PORT = None
    KEYSTONE_URL = None
    KEYSTONE_USER = None
    KEYSTONE_PASSWORD = None
    KEYSTONE_DOMAIN = None
    KEYSTONE_PROJECT = None
    KEYSTONE_CHECK_TOKEN = None
    KEYSTONE_SERVER_CRT = None
    PLUGIN_CONTAINERS = None


def get_configuration():
    conf = Configuration()
    conf.DB_URL = os.getenv("DB_URL", "mysql+pymysql://moon:p4sswOrd1@db/moon")
    conf.DB_DRIVER = os.getenv("DB_DRIVER", "sql")
    conf.TRANSPORT_URL = os.getenv("TRANSPORT_URL", "rabbit://moon:p4sswOrd1@messenger:5672/moon")
    conf.DOCKER_URL = os.getenv("DOCKER_URL", "unix://var/run/docker.sock")
    conf.SLAVE_NAME = os.getenv("SLAVE_NAME", "")
    conf.MASTER_URL = os.getenv("MASTER_URL", "")
    conf.MASTER_LOGIN = os.getenv("MASTER_LOGIN", "")
    conf.MASTER_PASSWORD = os.getenv("MASTER_PASSWORD", "")
    conf.INTERFACE_PORT = os.getenv("INTERFACE_PORT", "8080")
    conf.CONSUL_HOST = os.getenv("CONSUL_HOST", "172.88.88.88")
    conf.CONSUL_PORT = os.getenv("CONSUL_PORT", "88")
    conf.KEYSTONE_URL = os.getenv("KEYSTONE_URL", "http://keystone:5000/v3")
    conf.KEYSTONE_USER = os.getenv("KEYSTONE_USER", "admin")
    conf.KEYSTONE_PASSWORD = os.getenv("KEYSTONE_PASSWORD", "p4ssw0rd")
    conf.KEYSTONE_DOMAIN = os.getenv("KEYSTONE_DOMAIN", "default")
    conf.KEYSTONE_PROJECT = os.getenv("KEYSTONE_PROJECT", "admin")
    conf.KEYSTONE_CHECK_TOKEN = os.getenv("KEYSTONE_CHECK_TOKEN", False)
    conf.KEYSTONE_SERVER_CRT = os.getenv("KEYSTONE_SERVER_CRT", False)
    conf.PLUGIN_CONTAINERS = os.getenv("PLUGIN_CONTAINERS", "asteroide/authz:latest,asteroide/session:latest")
    conf.COMPONENTS_PORT_START = int(os.getenv("COMPONENTS_PORT_START", "38001"))
    conf.COMPONENTS = [
        {
            "hostname": conf.CONSUL_HOST,
            "port": conf.CONSUL_PORT,
            "id": "consul",
            "keystone_id": None
        },
    ]
    return conf


def main():
    conf = get_configuration()
    LOG.info("Starting server with IP {} on port {}".format(conf.CONSUL_HOST, conf.CONSUL_PORT))
    server = HTTPServer(host=conf.CONSUL_HOST, port=int(conf.CONSUL_PORT), conf=conf)
    server.run()


if __name__ == '__main__':
    main()
