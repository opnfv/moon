# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import re
import types
import json
import copy
from uuid import uuid4
from oslo_config import cfg
from oslo_log import log as logging
import requests
from moon_utilities import exceptions
from moon_utilities.security_functions import filter_input, enforce
# from moon_db.api import algorithms
from moon_db.api.managers import Managers


LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class PDPManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.PDPManager = self

    @enforce(("read", "write"), "pdp")
    def update_pdp(self, user_id, pdp_id, value):
        return self.driver.update_pdp(pdp_id=pdp_id, value=value)

    @enforce(("read", "write"), "pdp")
    def delete_pdp(self, user_id, pdp_id):
        return self.driver.delete_pdp(pdp_id=pdp_id)

    @enforce(("read", "write"), "pdp")
    def add_pdp(self, user_id, pdp_id=None, value=None):
        if not pdp_id:
            pdp_id = uuid4().hex
        return self.driver.add_pdp(pdp_id=pdp_id, value=value)

    @enforce("read", "pdp")
    def get_pdp(self, user_id, pdp_id=None):
        return self.driver.get_pdp(pdp_id=pdp_id)

