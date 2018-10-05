# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
from python_moonutilities import configuration, exceptions
from moon_wrapper.http_server import HTTPServer

LOG = logging.getLogger("moon.wrapper.server")


def main():
    configuration.init_logging()
    try:
        conf = configuration.get_configuration("components/wrapper")
        LOG.debug("wrapper.conf={}".format(conf))
        hostname = conf["components/wrapper"].get("hostname", "wrapper")
        port = conf["components/wrapper"].get("port", 80)
        bind = conf["components/wrapper"].get("bind", "127.0.0.1")
    except exceptions.ConsulComponentNotFound:
        hostname = "wrapper"
        bind = "127.0.0.1"
        port = 80
        configuration.add_component(uuid="wrapper", name=hostname, port=port, bind=bind)
    LOG.info("Starting server with IP {} on port {} bind to {}".format(hostname, port, bind))
    return HTTPServer(host=bind, port=port)


if __name__ == '__main__':
    SERVER = main()
    SERVER.run()
