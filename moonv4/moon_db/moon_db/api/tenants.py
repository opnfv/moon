# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
from moon_utilities import exceptions
from moon_db.api.managers import Managers
from moon_utilities.security_functions import filter_input, enforce
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class TenantManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.TenantManager = self

    @filter_input
    @enforce("read", "tenants")
    def get_tenants_dict(self, user_id):
        """
        Return a dictionary with all tenants
        :return: {
            tenant_id1: {
                name: xxx,
                description: yyy,
                intra_authz_extension_id: zzz,
                intra_admin_extension_id: zzz,
                },
            tenant_id2: {...},
            ...
            }
        """
        return self.driver.get_tenants_dict()

    def __get_keystone_tenant_dict(self, tenant_id="", tenant_name=""):
        tenants = Managers.KeystoneManager.list_projects()
        for tenant in tenants:
            if tenant_id and tenant_id == tenant['id']:
                return tenant
            if tenant_name and tenant_name == tenant['name']:
                return tenant
        if not tenant_id:
            tenant_id = uuid4().hex
        if not tenant_name:
            tenant_name = tenant_id
        tenant = {
            "id": tenant_id,
            "name": tenant_name,
            "description": "Auto generated tenant from Moon platform",
            "enabled": True,
            "domain_id": "default"
        }
        keystone_tenant = Managers.KeystoneManager.create_project(tenant["id"], tenant)
        return keystone_tenant

    @filter_input
    @enforce(("read", "write"), "tenants")
    def add_tenant_dict(self, user_id, tenant_id, tenant_dict):
        tenants_dict = self.driver.get_tenants_dict()
        for tenant_id in tenants_dict:
            if tenants_dict[tenant_id]['name'] == tenant_dict['name']:
                raise exceptions.TenantAddedNameExisting()

        # Check (and eventually sync) Keystone tenant
        if 'id' not in tenant_dict:
            tenant_dict['id'] = None
        keystone_tenant = self.__get_keystone_tenant_dict(tenant_dict['id'], tenant_dict['name'])
        for att in keystone_tenant:
            if keystone_tenant[att]:
                tenant_dict[att] = keystone_tenant[att]
        # Sync users between intra_authz_extension and intra_admin_extension
        LOG.debug("add_tenant_dict {}".format(tenant_dict))
        if 'intra_admin_extension_id' in tenant_dict and tenant_dict['intra_admin_extension_id']:
            if 'intra_authz_extension_id' in tenant_dict and tenant_dict['intra_authz_extension_id']:
                authz_subjects_dict = Managers.IntraExtensionAdminManager.get_subjects_dict(
                    Managers.IntraExtensionRootManager.root_admin_id, tenant_dict['intra_authz_extension_id'])
                authz_subject_names_list = [authz_subjects_dict[subject_id]["name"] for subject_id in authz_subjects_dict]
                admin_subjects_dict = Managers.IntraExtensionAdminManager.get_subjects_dict(
                    Managers.IntraExtensionRootManager.root_admin_id, tenant_dict['intra_admin_extension_id'])
                admin_subject_names_list = [admin_subjects_dict[subject_id]["name"] for subject_id in admin_subjects_dict]
                for _subject_id in authz_subjects_dict:
                    if authz_subjects_dict[_subject_id]["name"] not in admin_subject_names_list:
                        Managers.IntraExtensionAdminManager.add_subject_dict(
                            Managers.IntraExtensionRootManager.root_admin_id, tenant_dict['intra_admin_extension_id'], authz_subjects_dict[_subject_id])
                for _subject_id in admin_subjects_dict:
                    if admin_subjects_dict[_subject_id]["name"] not in authz_subject_names_list:
                        Managers.IntraExtensionAdminManager.add_subject_dict(
                            Managers.IntraExtensionRootManager.root_admin_id, tenant_dict['intra_authz_extension_id'], admin_subjects_dict[_subject_id])

        return self.driver.add_tenant_dict(tenant_dict['id'], tenant_dict)

    @filter_input
    @enforce("read", "tenants")
    def get_tenant_dict(self, user_id, tenant_id):
        tenants_dict = self.driver.get_tenants_dict()
        if tenant_id not in tenants_dict:
            raise exceptions.TenantUnknown()
        return tenants_dict[tenant_id]

    @filter_input
    @enforce(("read", "write"), "tenants")
    def del_tenant(self, user_id, tenant_id):
        if tenant_id not in self.driver.get_tenants_dict():
            raise exceptions.TenantUnknown()
        self.driver.del_tenant(tenant_id)

    @filter_input
    @enforce(("read", "write"), "tenants")
    def set_tenant_dict(self, user_id, tenant_id, tenant_dict):
        tenants_dict = self.driver.get_tenants_dict()
        if tenant_id not in tenants_dict:
            raise exceptions.TenantUnknown()

        # Sync users between intra_authz_extension and intra_admin_extension
        if 'intra_admin_extension_id' in tenant_dict:
            if 'intra_authz_extension_id' in tenant_dict:
                authz_subjects_dict = Managers.IntraExtensionAdminManager.get_subjects_dict(
                    Managers.IntraExtensionRootManager.root_admin_id, tenant_dict['intra_authz_extension_id'])
                authz_subject_names_list = [authz_subjects_dict[subject_id]["name"] for subject_id in authz_subjects_dict]
                admin_subjects_dict = Managers.IntraExtensionAdminManager.get_subjects_dict(
                    Managers.IntraExtensionRootManager.root_admin_id, tenant_dict['intra_admin_extension_id'])
                admin_subject_names_list = [admin_subjects_dict[subject_id]["name"] for subject_id in admin_subjects_dict]
                for _subject_id in authz_subjects_dict:
                    if authz_subjects_dict[_subject_id]["name"] not in admin_subject_names_list:
                        Managers.IntraExtensionAdminManager.add_subject_dict(
                            Managers.IntraExtensionRootManager.root_admin_id, tenant_dict['intra_admin_extension_id'], authz_subjects_dict[_subject_id])
                for _subject_id in admin_subjects_dict:
                    if admin_subjects_dict[_subject_id]["name"] not in authz_subject_names_list:
                        Managers.IntraExtensionAdminManager.add_subject_dict(
                            Managers.IntraExtensionRootManager.root_admin_id, tenant_dict['intra_authz_extension_id'], admin_subjects_dict[_subject_id])

        return self.driver.set_tenant_dict(tenant_id, tenant_dict)

