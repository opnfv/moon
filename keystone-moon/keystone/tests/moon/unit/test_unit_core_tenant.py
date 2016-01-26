# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Unit tests for core tenant."""

from oslo_config import cfg
from keystone.tests import unit as tests
from keystone.contrib.moon.core import ConfigurationManager
from keystone.tests.unit.ksfixtures import database
from keystone.contrib.moon.exception import *
from keystone.tests.unit import default_fixtures
from keystone.contrib.moon.core import LogManager
from keystone.contrib.moon.core import IntraExtensionRootManager
from keystone.contrib.moon.core import IntraExtensionAdminManager
from keystone.contrib.moon.core import IntraExtensionAuthzManager
from keystone.tests.moon.unit import *


CONF = cfg.CONF
USER = {
    'name': 'admin',
    'domain_id': "default",
    'password': 'admin'
}
IE = {
    "name": "test IE",
    "policymodel": "policy_authz",
    "description": "a simple description."
}


class TestTenantManager(tests.TestCase):
    ADMIN_ID = None

    def setUp(self):
        self.useFixture(database.Database())
        super(TestTenantManager, self).setUp()
        self.load_fixtures(default_fixtures)
        self.load_backends()
        domain = {'id': "default", 'name': "default"}
        self.resource_api.create_domain(domain['id'], domain)
        self.admin = create_user(self, username="admin")
        self.demo = create_user(self, username="demo")
        ref = self.root_api.load_root_intra_extension_dict()
        self.root_api.populate_default_data(ref)
        self.root_intra_extension = self.root_api.get_root_extension_dict()
        self.root_intra_extension_id = self.root_intra_extension.keys()[0]
        self.ADMIN_ID = self.root_api.root_admin_id
        self.authz_manager = self.authz_api
        self.admin_manager = self.admin_api
        self.tenant_manager = self.tenant_api

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager(),
            "admin_api": IntraExtensionAdminManager(),
            "authz_api": IntraExtensionAuthzManager(),
            "configuration_api": ConfigurationManager(),
            "root_api": IntraExtensionRootManager(),
        }

    def config_overrides(self):
        super(TestTenantManager, self).config_overrides()
        self.config_fixture.config(
            group='moon',
            tenant_driver='keystone.contrib.moon.backends.sql.TenantConnector')
        self.policy_directory = 'examples/moon/policies'
        self.config_fixture.config(
            group='moon',
            intraextension_driver='keystone.contrib.moon.backends.sql.IntraExtensionConnector')
        self.config_fixture.config(
            group='moon',
            policy_directory=self.policy_directory)

    def test_add_tenant(self):
        authz_intra_extension = create_intra_extension(self, policy_model="policy_authz")
        admin_intra_extension = create_intra_extension(self, policy_model="policy_rbac_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension_id": authz_intra_extension['id'],
            "intra_admin_extension_id": admin_intra_extension['id'],
        }
        data = self.tenant_manager.add_tenant_dict(user_id=self.ADMIN_ID, tenant_id=new_tenant['id'], tenant_dict=new_tenant)
        data_id = data.keys()[0]
        self.assertEquals(new_tenant["id"], data_id)
        self.assertEquals(new_tenant["name"], data[data_id]["name"])
        self.assertEquals(new_tenant["intra_authz_extension_id"], data[data_id]["intra_authz_extension_id"])
        self.assertEquals(new_tenant["intra_admin_extension_id"], data[data_id]["intra_admin_extension_id"])
        data = self.tenant_manager.get_tenants_dict(self.ADMIN_ID)
        self.assertNotEqual(data, {})
        data = self.admin_api.get_intra_extension_dict(self.ADMIN_ID, new_tenant["intra_authz_extension_id"])
        data_id = data["id"]
        self.assertEquals(new_tenant["intra_authz_extension_id"], data_id)
        data = self.admin_api.get_intra_extension_dict(self.ADMIN_ID, new_tenant["intra_admin_extension_id"])
        data_id = data["id"]
        self.assertEquals(new_tenant["intra_admin_extension_id"], data_id)

    def test_del_tenant(self):
        authz_intra_extension = create_intra_extension(self, policy_model="policy_authz")
        admin_intra_extension = create_intra_extension(self, policy_model="policy_rbac_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension_id": authz_intra_extension['id'],
            "intra_admin_extension_id": admin_intra_extension['id'],
        }
        data = self.tenant_manager.add_tenant_dict(user_id=self.ADMIN_ID, tenant_id=new_tenant['id'], tenant_dict=new_tenant)
        data_id = data.keys()[0]
        self.assertEquals(new_tenant["name"], data[data_id]["name"])
        self.assertEquals(new_tenant["intra_authz_extension_id"], data[data_id]["intra_authz_extension_id"])
        self.assertEquals(new_tenant["intra_admin_extension_id"], data[data_id]["intra_admin_extension_id"])
        data = self.tenant_manager.get_tenants_dict(self.ADMIN_ID)
        self.assertNotEqual(data, {})
        self.tenant_manager.del_tenant(self.ADMIN_ID, data_id)
        data = self.tenant_manager.get_tenants_dict(self.ADMIN_ID)
        self.assertEqual(data, {})

    def test_set_tenant(self):
        authz_intra_extension = create_intra_extension(self, policy_model="policy_authz")
        admin_intra_extension = create_intra_extension(self, policy_model="policy_rbac_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension_id": authz_intra_extension['id'],
            "intra_admin_extension_id": admin_intra_extension['id'],
        }
        data = self.tenant_manager.add_tenant_dict(user_id=self.ADMIN_ID, tenant_id=new_tenant['id'], tenant_dict=new_tenant)
        data_id = data.keys()[0]
        self.assertEquals(new_tenant["name"], data[data_id]["name"])
        self.assertEquals(new_tenant["intra_authz_extension_id"], data[data_id]["intra_authz_extension_id"])
        self.assertEquals(new_tenant["intra_admin_extension_id"], data[data_id]["intra_admin_extension_id"])
        data = self.tenant_manager.get_tenants_dict(self.ADMIN_ID)
        self.assertNotEqual(data, {})

        new_tenant["name"] = "demo2"
        print(new_tenant)
        data = self.tenant_manager.set_tenant_dict(user_id=self.ADMIN_ID, tenant_id=data_id, tenant_dict=new_tenant)
        data_id = data.keys()[0]
        self.assertEquals(new_tenant["name"], data[data_id]["name"])
        self.assertEquals(new_tenant["intra_authz_extension_id"], data[data_id]["intra_authz_extension_id"])
        self.assertEquals(new_tenant["intra_admin_extension_id"], data[data_id]["intra_admin_extension_id"])

    def test_exception_tenant_unknown(self):
        self.assertRaises(TenantUnknown, self.tenant_manager.get_tenant_dict, self.ADMIN_ID, uuid.uuid4().hex)
        self.assertRaises(TenantUnknown, self.tenant_manager.del_tenant, self.ADMIN_ID, uuid.uuid4().hex)
        self.assertRaises(TenantUnknown, self.tenant_manager.set_tenant_dict, self.ADMIN_ID, uuid.uuid4().hex, {})

        authz_intra_extension = create_intra_extension(self, policy_model="policy_authz")
        admin_intra_extension = create_intra_extension(self, policy_model="policy_rbac_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension_id": authz_intra_extension['id'],
            "intra_admin_extension_id": admin_intra_extension['id'],
        }
        data = self.tenant_manager.add_tenant_dict(user_id=self.ADMIN_ID, tenant_id=new_tenant['id'], tenant_dict=new_tenant)
        data_id = data.keys()[0]
        self.assertEquals(new_tenant["name"], data[data_id]["name"])
        self.assertEquals(new_tenant["intra_authz_extension_id"], data[data_id]["intra_authz_extension_id"])
        self.assertEquals(new_tenant["intra_admin_extension_id"], data[data_id]["intra_admin_extension_id"])
        data = self.tenant_manager.get_tenants_dict(self.ADMIN_ID)
        self.assertNotEqual(data, {})

        self.assertRaises(TenantUnknown, self.tenant_manager.get_tenant_dict, self.ADMIN_ID, uuid.uuid4().hex)

    def test_exception_tenant_added_name_existing(self):
        authz_intra_extension = create_intra_extension(self, policy_model="policy_authz")
        admin_intra_extension = create_intra_extension(self, policy_model="policy_rbac_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension_id": authz_intra_extension['id'],
            "intra_admin_extension_id": admin_intra_extension['id'],
        }
        data = self.tenant_manager.add_tenant_dict(user_id=self.ADMIN_ID, tenant_id=new_tenant['id'], tenant_dict=new_tenant)
        data_id = data.keys()[0]
        self.assertEquals(new_tenant["name"], data[data_id]["name"])
        self.assertEquals(new_tenant["intra_authz_extension_id"], data[data_id]["intra_authz_extension_id"])
        self.assertEquals(new_tenant["intra_admin_extension_id"], data[data_id]["intra_admin_extension_id"])
        data = self.tenant_manager.get_tenants_dict(self.ADMIN_ID)
        self.assertNotEqual(data, {})

        self.assertRaises(TenantAddedNameExisting, self.tenant_manager.add_tenant_dict, self.ADMIN_ID, new_tenant['id'], new_tenant)
