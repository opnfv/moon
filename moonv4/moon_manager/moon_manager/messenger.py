# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import time
from oslo_config import cfg
import oslo_messaging
from oslo_log import log as logging
from moon_manager.api.generic import Status, Logs
from moon_utilities.api import APIList
from moon_manager.api.models import Models, MetaRules, MetaData
from moon_manager.api.policies import Policies, Perimeter, Data, Assignments, Rules
from moon_manager.api.pdp import PDP
from moon_manager.api.master import Master
from moon_utilities.security_functions import call
from moon_utilities.exceptions import IntraExtensionUnknown

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Server:

    def __init__(self):
        self.TOPIC = "moon_manager"
        self.transport = oslo_messaging.get_transport(cfg.CONF)
        self.target = oslo_messaging.Target(topic=self.TOPIC, server='moon_manager_server1')
        # ctx = {'user_id': 'admin', 'id': intra_extension_id, 'method': 'get_intra_extensions'}
        # if CONF.slave.slave_name:
        #     ctx['call_master'] = True
        # intra_extension = call(
        #     endpoint="security_router",
        #     ctx=ctx,
        #     method='route',
        #     args={}
        # )
        LOG.info("Starting MQ server with topic: {}".format(self.TOPIC))
        # if "intra_extensions" not in intra_extension:
        #     LOG.error("Error reading intra_extension from router")
        #     LOG.error("intra_extension: {}".format(intra_extension))
        #     raise IntraExtensionUnknown
        # intra_extension_id = list(intra_extension["intra_extensions"].keys())[0]
        self.endpoints = [
            APIList((Status, Logs)),
            Status(),
            Logs(),
            Models(),
            MetaRules(),
            MetaData(),
            Policies(),
            Perimeter(),
            Data(),
            Assignments(),
            Rules(),
            PDP(),
            Master()
        ]
        self.server = oslo_messaging.get_rpc_server(self.transport, self.target, self.endpoints,
                                                    executor='threading',
                                                    access_policy=oslo_messaging.DefaultRPCAccessPolicy)

    def run(self):
        try:
            self.server.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping server by crtl+c")
        except SystemExit:
            print("Stopping server")

        self.server.stop()
        self.server.wait()

