# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
from moon_utilities import configuration, exceptions
from moon_interface.http_server import HTTPServer

LOG = logging.getLogger("moon.interface")


def main():
    configuration.init_logging()
    try:
        conf = configuration.get_configuration("components/interface")
        LOG.debug("interface.conf={}".format(conf))
        hostname = conf["components/interface"].get("hostname", "interface")
        port = conf["components/interface"].get("port", 80)
        bind = conf["components/interface"].get("bind", "127.0.0.1")
    except exceptions.ConsulComponentNotFound:
        hostname = "interface"
        bind = "127.0.0.1"
        port = 80
        configuration.add_component(uuid="interface", name=hostname, port=port, bind=bind)
    LOG.info("Starting server with IP {} on port {} bind to {}".format(hostname, port, bind))
    server = HTTPServer(host=bind, port=port)
    server.run()


if __name__ == '__main__':
    main()
