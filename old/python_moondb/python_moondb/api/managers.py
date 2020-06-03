# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

logger = logging.getLogger("moon.db.api.managers")


class Managers(object):
    """Object that links managers together"""
    ModelManager = None
    KeystoneManager = None
    PDPManager = None
    PolicyManager = None
