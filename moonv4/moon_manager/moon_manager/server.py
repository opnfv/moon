# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
from oslo_config import cfg
from oslo_log import log as logging
from moon_utilities import options  # noqa
from moon_manager.messenger import Server

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "moon_manager"

__CWD__ = os.path.dirname(os.path.abspath(__file__))


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
