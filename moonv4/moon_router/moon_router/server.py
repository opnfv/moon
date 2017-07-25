# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import threading
import signal
from oslo_log import log as logging
from moon_utilities import configuration, exceptions
from moon_router.messenger import Server


class AsyncServer(threading.Thread):

    def __init__(self, add_master_cnx):
        threading.Thread.__init__(self)
        self.server = Server(add_master_cnx=add_master_cnx)

    def run(self):
        self.server.run()

LOG = logging.getLogger("moon.router")

__CWD__ = os.path.dirname(os.path.abspath(__file__))

background_threads = []


def stop_thread():
    for _t in background_threads:
        _t.stop()


def main():
    global background_threads
    configuration.init_logging()
    try:
        conf = configuration.get_configuration("components/router")
    except exceptions.ConsulComponentNotFound:
        conf = configuration.add_component("router", "router")
    signal.signal(signal.SIGALRM, stop_thread)
    signal.signal(signal.SIGTERM, stop_thread)
    signal.signal(signal.SIGABRT, stop_thread)
    background_master = None
    slave = configuration.get_configuration(configuration.SLAVE)["slave"]
    if slave['name']:
        background_master = AsyncServer(add_master_cnx=True)
        background_threads.append(background_master)
    background_slave = AsyncServer(add_master_cnx=False)
    background_threads.append(background_slave)
    if slave['name']:
        background_master.start()
        LOG.info("Connecting to master...")
    background_slave.start()
    LOG.info("Starting main server {}".format(conf["components/router"]["hostname"]))
    if slave['name']:
        background_master.join()
    background_slave.join()


if __name__ == '__main__':
    main()
