# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
from oslo_config import cfg
from oslo_log import log as logging
from python_moonutilities import configuration, exceptions
from moon_manager.http_server import HTTPServer

LOG = logging.getLogger("moon.manager")
CONF = cfg.CONF
DOMAIN = "moon_manager"

__CWD__ = os.path.dirname(os.path.abspath(__file__))


def main():
    configuration.init_logging()
    try:
        conf = configuration.get_configuration("components/manager")
        hostname = conf["components/manager"].get("hostname", "manager")
        port = conf["components/manager"].get("port", 80)
        bind = conf["components/manager"].get("bind", "127.0.0.1")
    except exceptions.ConsulComponentNotFound:
        hostname = "manager"
        bind = "127.0.0.1"
        port = 80
        configuration.add_component(uuid="manager", name=hostname, port=port, bind=bind)
    LOG.info("Starting server with IP {} on port {} bind to {}".format(hostname, port, bind))
    server = HTTPServer(host=bind, port=port)
    return server


if __name__ == '__main__':
    server = main()
    server.run()
