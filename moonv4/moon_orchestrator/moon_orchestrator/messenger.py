# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from oslo_config import cfg
import oslo_messaging
from oslo_log import log as logging
import time
from moon_utilities.api import APIList
from moon_utilities.security_functions import call
from moon_utilities.exceptions import RootPDPNotInitialized

from oslo_config import cfg
from moon_orchestrator.api.generic import Status, Logs
# from moon_orchestrator.api.configuration import Configuration
from moon_orchestrator.api.containers import Containers
from moon_orchestrator.api.slaves import Slaves

TOPIC = "orchestrator"
LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Server:

    def __init__(self, containers, docker_manager, slaves):
        self.CONTAINERS = containers
        self.transport = oslo_messaging.get_transport(cfg.CONF)
        self.target = oslo_messaging.Target(topic=TOPIC, server='server1')
        LOG.info("Starting MQ server with topic: {}".format(TOPIC))
        self.docker_manager = docker_manager
        for _container in containers:
            Status._container = containers[_container]
        self.endpoints = [
            APIList((Status, Logs, Containers)),
            Status(),
            Logs(),
            Containers(self.docker_manager),
            # Configuration(),
            Slaves(slaves)
        ]
        self.server = oslo_messaging.get_rpc_server(self.transport, self.target, self.endpoints,
                                                    executor='threading',
                                                    access_policy=oslo_messaging.DefaultRPCAccessPolicy)

    # @staticmethod
    # def __check_root_pdp():
    #     root_exist = False
    #     for key, value in call("manager", ctx={"user_id": "admin"},
    #                            method="get_pdp", args={})["pdp"].items():
    #         if value["name"] == CONF.root_policy_directory:
    #             root_exist = True
    #     if not root_exist:
    #         ie = call("manager", ctx={"user_id": "admin"}, method="add_pdp",
    #                   args={
    #                       "name": "policy_root",
    #                       "model": CONF.root_policy_directory,
    #                       "genre": "admin",
    #                       "description": "policy_root"
    #                   })
    #         if "result" in ie and not ie["result"]:
    #             raise RootPDPNotInitialized

    def run(self):
        try:
            self.server.start()
            # try:
            #     raise NotImplementedError
            #     # self.__check_root_pdp()
            # except Exception as e:
            #     LOG.error("Exception occurred when creating Root PDP: {}".format(e))
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            LOG.warning("Stopping server by crtl+c (please be patient, closing connections...)")
        except SystemExit:
            LOG.warning("Stopping server (please be patient, closing connections...)")
        except Exception as e:
            LOG.error("Exception occurred: {}".format(e))

        self.server.stop()
        self.server.wait()

