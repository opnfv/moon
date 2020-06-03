# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from uuid import uuid4
import logging
from moon_utilities.security_functions import enforce
from moon_manager.api.db.managers import Managers
from moon_utilities import exceptions

logger = logging.getLogger("moon.db.api.pdp")


class PDPManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.PDPManager = self

    @enforce(("read", "write"), "pdp")
    def update_pdp(self, moon_user_id, pdp_id, value):
        if not value or 'name' not in value or not value['name'].strip():
            raise exceptions.PdpContentError
        
        exists_security_pipeline = value and 'security_pipeline' in value and \
                                    len(value['security_pipeline']) > 0
        exists_vim_project_id = value and 'vim_project_id' in value and \
                                    value['vim_project_id'] != None and \
                                    value['vim_project_id'].strip()
        if not exists_security_pipeline and exists_vim_project_id:
            raise exceptions.PdpContentError
        if exists_security_pipeline and not exists_vim_project_id:
            raise exceptions.PdpContentError
        
        self.__pdp_validated_pipeline_name_id(pdp_id, value, "update")

        if value and 'security_pipeline' in value:
            for policy_id in value['security_pipeline']:
                if not policy_id or not policy_id.strip() or not \
                        Managers.PolicyManager.get_policies(moon_user_id=moon_user_id, policy_id=policy_id):
                    raise exceptions.PolicyUnknown

        return self.driver.update_pdp(pdp_id=pdp_id, value=value)

    @enforce(("read", "write"), "pdp")
    def delete_pdp(self, moon_user_id, pdp_id):
        if pdp_id not in self.driver.get_pdp(pdp_id=pdp_id):
            raise exceptions.PdpUnknown
        return self.driver.delete_pdp(pdp_id=pdp_id)

    @enforce(("read", "write"), "pdp")
    def add_pdp(self, moon_user_id, pdp_id=None, value=None):
        if not value or 'name' not in value or not value['name'].strip():
            raise exceptions.PdpContentError

        exists_security_pipeline = value and 'security_pipeline' in value and \
                                    len(value['security_pipeline']) > 0
        exists_vim_project_id = value and 'vim_project_id' in value and \
                                    value['vim_project_id'] is not None and \
                                    value['vim_project_id'].strip()
        if not exists_security_pipeline and exists_vim_project_id:
            raise exceptions.PdpContentError
        if exists_security_pipeline and not exists_vim_project_id:
            raise exceptions.PdpContentError

        self.__pdp_validated_pipeline_name_id(pdp_id, value, "add")

        if value and 'security_pipeline' in value:
            for policy_id in value['security_pipeline']:
                if not policy_id or not policy_id.strip() or not \
                        Managers.PolicyManager.get_policies(moon_user_id=moon_user_id, policy_id=policy_id):
                    raise exceptions.PolicyUnknown

        return self.driver.add_pdp(pdp_id=pdp_id, value=value)

    @enforce("read", "pdp")
    def get_pdp(self, moon_user_id, pdp_id=None):
        return self.driver.get_pdp(pdp_id=pdp_id)

    @enforce("read", "pdp")
    def delete_policy_from_pdp(self, moon_user_id, pdp_id, policy_id):

        if pdp_id not in self.driver.get_pdp(pdp_id=pdp_id):
            raise exceptions.PdpUnknown
        if policy_id not in self.driver.get_policies(policy_id=policy_id):
            raise exceptions.PolicyUnknown
        x = self.driver.delete_policy_from_pdp(pdp_id=pdp_id, policy_id=policy_id)
        return x

    def __pdp_validated_pipeline_name_id(self, pdp_id, value, method_type=None):
        all_pdps = self.driver.get_pdp()
        if method_type == 'update':
            if pdp_id not in all_pdps:
                raise exceptions.PdpUnknown
        else:
            if pdp_id in all_pdps:
                raise exceptions.PdpExisting
            if not pdp_id:
                pdp_id = uuid4().hex

        for key in all_pdps:
            if pdp_id != key:
                if all_pdps[key]['name'] == value['name']:
                    raise exceptions.PdpExisting
                for policy_id in value['security_pipeline']:
                    if policy_id in all_pdps[key]['security_pipeline']:
                        raise exceptions.PdpInUse
