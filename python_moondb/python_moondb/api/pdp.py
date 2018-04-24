# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
import logging
from python_moonutilities.security_functions import enforce
from python_moondb.api.managers import Managers
from python_moonutilities import exceptions

logger = logging.getLogger("moon.db.api.pdp")


class PDPManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.PDPManager = self

    @enforce(("read", "write"), "pdp")
    def update_pdp(self, user_id, pdp_id, value):
        if pdp_id not in self.driver.get_pdp(pdp_id=pdp_id):
            raise exceptions.PdpUnknown
        if value and 'security_pipeline' in value:
            for policy_id in value['security_pipeline']:
                if not Managers.PolicyManager.get_policies(user_id=user_id, policy_id=policy_id):
                    raise exceptions.PolicyUnknown
        return self.driver.update_pdp(pdp_id=pdp_id, value=value)

    @enforce(("read", "write"), "pdp")
    def delete_pdp(self, user_id, pdp_id):
        if pdp_id not in self.driver.get_pdp(pdp_id=pdp_id):
            raise exceptions.PdpUnknown
        return self.driver.delete_pdp(pdp_id=pdp_id)

    @enforce(("read", "write"), "pdp")
    def add_pdp(self, user_id, pdp_id=None, value=None):
        if pdp_id in self.driver.get_pdp(pdp_id=pdp_id):
            raise exceptions.PdpExisting
        if not pdp_id:
            pdp_id = uuid4().hex
        if value and 'security_pipeline' in value:
            for policy_id in value['security_pipeline']:
                if not Managers.PolicyManager.get_policies(user_id=user_id, policy_id=policy_id):
                    raise exceptions.PolicyUnknown
        return self.driver.add_pdp(pdp_id=pdp_id, value=value)

    @enforce("read", "pdp")
    def get_pdp(self, user_id, pdp_id=None):
        return self.driver.get_pdp(pdp_id=pdp_id)
