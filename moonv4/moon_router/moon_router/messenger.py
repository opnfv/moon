# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from oslo_config import cfg
import oslo_messaging
import time
from oslo_log import log as logging
from moon_router.api.generic import Status, Logs
from moon_router.api.route import Router
from moon_utilities.api import APIList
from moon_utilities import configuration

LOG = logging.getLogger("moon.router.messenger")


class Server:

    TOPIC = "security_router"

    def __init__(self, add_master_cnx=False):
        slave = configuration.get_configuration(configuration.SLAVE)["slave"]
        cfg.CONF.transport_url = self.__get_transport_url()
        if add_master_cnx and slave["master"]["url"]:
            self.transport = oslo_messaging.get_transport(cfg.CONF, slave["master"]["url"])
            self.TOPIC = self.TOPIC + "_" + slave["name"]
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

    @staticmethod
    def __get_transport_url():
        messenger = configuration.get_configuration(configuration.MESSENGER)["messenger"]
        return messenger['url']

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

