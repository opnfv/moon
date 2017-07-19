# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from oslo_config import cfg
import oslo_messaging
import time
from oslo_log import log as logging
from moon_secrouter.api.generic import Status, Logs
from moon_secrouter.api.route import Router
from moon_utilities.api import APIList

LOG = logging.getLogger(__name__)


class Server:

    TOPIC = "security_router"

    def __init__(self, add_master_cnx=False):
        if add_master_cnx and cfg.CONF.slave.master_url:
            self.transport = oslo_messaging.get_transport(cfg.CONF, cfg.CONF.slave.master_url)
            self.TOPIC = self.TOPIC + "_" + cfg.CONF.slave.slave_name
        else:
            self.transport = oslo_messaging.get_transport(cfg.CONF)
        self.target = oslo_messaging.Target(topic=self.TOPIC, server='server1')
        LOG.info("Starting MQ server with topic: {}".format(self.TOPIC))
        self.endpoints = [
            APIList((Status, Logs, Router)),
            Status(),
            Logs(),
            Router(add_master_cnx)
        ]
        self.server = oslo_messaging.get_rpc_server(self.transport, self.target, self.endpoints,
                                                    executor='threading',
                                                    access_policy=oslo_messaging.DefaultRPCAccessPolicy)
        self.__is_alive = False

    def stop(self):
        self.__is_alive = False
        self.endpoints[-1].delete()

    def run(self):
        try:
            self.__is_alive = True
            self.server.start()
            while True:
                if self.__is_alive:
                    time.sleep(1)
                else:
                    break
        except KeyboardInterrupt:
            print("Stopping server by crtl+c")
        except SystemExit:
            print("Stopping server with SystemExit")
        print("Stopping server")

        self.server.stop()
        self.server.wait()

