# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from oslo_config import cfg
import oslo_messaging
import time
from oslo_log import log as logging
from moon_authz.api.generic import Status, Logs
from moon_authz.api.authorization import Authorization
from moon_utilities.api import APIList

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Server:

    def __init__(self, component_id, keystone_project_id):
        self.TOPIC = "authz-workers"
        transport = oslo_messaging.get_notification_transport(cfg.CONF)
        targets = [
            oslo_messaging.Target(topic=self.TOPIC),
        ]
        self.endpoints = [
            APIList((Status, Logs)),
            Status(),
            Logs(),
            Authorization(component_id)
        ]
        pool = "authz-workers"
        self.server = oslo_messaging.get_notification_listener(transport, targets,
                                                               self.endpoints, executor='threading',
                                                               pool=pool)
        LOG.info("Starting MQ notification server with topic: {}".format(self.TOPIC))

    def run(self):
        try:
            self.server.start()
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stopping server by crtl+c")
        except SystemExit:
            print("Stopping server")

        self.server.stop()


