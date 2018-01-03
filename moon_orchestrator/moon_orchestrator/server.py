# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
from python_moonutilities import configuration, exceptions
from moon_orchestrator.http_server import HTTPServer

logger = logging.getLogger("moon.orchestrator.server")


def create_server():
    configuration.init_logging()
    try:
        conf = configuration.get_configuration("components/orchestrator")
        hostname = conf["components/orchestrator"].get("hostname",
                                                       "orchestrator")
        port = conf["components/orchestrator"].get("port", 80)
        bind = conf["components/orchestrator"].get("bind", "127.0.0.1")
    except exceptions.ConsulComponentNotFound:
        hostname = "orchestrator"
        bind = "127.0.0.1"
        port = 80
        configuration.add_component(uuid="orchestrator", name=hostname,
                                    port=port, bind=bind)
    logger.info("Starting server with IP {} on port {} bind to {}".format(
        hostname, port, bind))
    return HTTPServer(host=bind, port=port)


def run():
    server = create_server()
    server.run()


if __name__ == '__main__':
    server = create_server()
    server.run()
