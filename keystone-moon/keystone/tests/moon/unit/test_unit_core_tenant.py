# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Unit tests for core tenant."""

import uuid
from oslo_config import cfg
from keystone.tests import unit as tests
from keystone.contrib.moon.core import TenantManager
from keystone.tests.unit.ksfixtures import database
from keystone.contrib.moon.exception import *
from keystone.tests.unit import default_fixtures
from keystone.contrib.moon.core import LogManager
from keystone.contrib.moon.core import ADMIN_ID
from keystone.common import dependency


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

@dependency.requires('admin_api')
class TestTenantManager(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestTenantManager, self).setUp()
        self.load_backends()
        self.load_fixtures(default_fixtures)
        self.admin = self.create_user(username="admin")
        self.demo = self.create_user(username="demo")
        self.manager = TenantManager()
        self.root_intra_extension = self.create_intra_extension(policy_model="policy_root")

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager()
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

    def create_user(self, username="admin"):

        _USER = dict(USER)
        _USER["name"] = username
        return self.identity_api.create_user(_USER)

    def create_intra_extension(self, policy_model="policy_authz"):

        IE["model"] = policy_model
        IE["name"] = uuid.uuid4().hex
        genre = "admin"
        if "authz" in policy_model:
            genre = "authz"
        IE["genre"] = genre
        ref = self.admin_api.load_intra_extension_dict(ADMIN_ID, intra_extension_dict=IE)
        self.assertIsInstance(ref, dict)
        return ref

    def test_add_tenant(self):
        authz_intra_extension = self.create_intra_extension(policy_model="policy_authz")
        admin_intra_extension = self.create_intra_extension(policy_model="policy_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension": authz_intra_extension['id'],
            "intra_admin_extension": admin_intra_extension['id'],
        }
        data = self.manager.add_tenant_dict(user_id=ADMIN_ID, tenant_dict=new_tenant)
        self.assertEquals(new_tenant["id"], data["id"])
        self.assertEquals(new_tenant["name"], data['tenant']["name"])
        self.assertEquals(new_tenant["intra_authz_extension"], data['tenant']["intra_authz_extension"])
        self.assertEquals(new_tenant["intra_admin_extension"], data['tenant']["intra_admin_extension"])
        data = self.manager.get_tenants_dict(ADMIN_ID)
        self.assertNotEqual(data, {})
        data = self.admin_api.get_intra_extension_dict(ADMIN_ID, new_tenant["intra_authz_extension"])
        self.assertEquals(new_tenant["intra_authz_extension"], data["id"])
        data = self.admin_api.get_intra_extension_dict(ADMIN_ID, new_tenant["intra_admin_extension"])
        self.assertEquals(new_tenant["intra_admin_extension"], data["id"])

    def test_del_tenant(self):
        authz_intra_extension = self.create_intra_extension(policy_model="policy_authz")
        admin_intra_extension = self.create_intra_extension(policy_model="policy_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension": authz_intra_extension['id'],
            "intra_admin_extension": admin_intra_extension['id'],
        }
        data = self.manager.add_tenant_dict(user_id=ADMIN_ID, tenant_dict=new_tenant)
        self.assertEquals(new_tenant["id"], data["id"])
        self.assertEquals(new_tenant["name"], data['tenant']["name"])
        self.assertEquals(new_tenant["intra_authz_extension"], data['tenant']["intra_authz_extension"])
        self.assertEquals(new_tenant["intra_admin_extension"], data['tenant']["intra_admin_extension"])
        data = self.manager.get_tenants_dict(ADMIN_ID)
        self.assertNotEqual(data, {})
        self.manager.del_tenant(ADMIN_ID, new_tenant["id"])
        data = self.manager.get_tenants_dict(ADMIN_ID)
        self.assertEqual(data, {})

    def test_set_tenant(self):
        authz_intra_extension = self.create_intra_extension(policy_model="policy_authz")
        admin_intra_extension = self.create_intra_extension(policy_model="policy_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension": authz_intra_extension['id'],
            "intra_admin_extension": admin_intra_extension['id'],
        }
        data = self.manager.add_tenant_dict(user_id=ADMIN_ID, tenant_dict=new_tenant)
        self.assertEquals(new_tenant["id"], data["id"])
        self.assertEquals(new_tenant["name"], data['tenant']["name"])
        self.assertEquals(new_tenant["intra_authz_extension"], data['tenant']["intra_authz_extension"])
        self.assertEquals(new_tenant["intra_admin_extension"], data['tenant']["intra_admin_extension"])
        data = self.manager.get_tenants_dict(ADMIN_ID)
        self.assertNotEqual(data, {})

        new_tenant["name"] = "demo2"
        data = self.manager.set_tenant_dict(user_id=ADMIN_ID, tenant_id=new_tenant["id"], tenant_dict=new_tenant)
        self.assertEquals(new_tenant["id"], data["id"])
        self.assertEquals(new_tenant["name"], data['tenant']["name"])
        self.assertEquals(new_tenant["intra_authz_extension"], data['tenant']["intra_authz_extension"])
        self.assertEquals(new_tenant["intra_admin_extension"], data['tenant']["intra_admin_extension"])

    def test_exception_tenant_unknown(self):
        self.assertRaises(TenantUnknown, self.manager.get_tenant_dict, ADMIN_ID, uuid.uuid4().hex)
        self.assertRaises(TenantUnknown, self.manager.del_tenant, ADMIN_ID, uuid.uuid4().hex)
        self.assertRaises(TenantUnknown, self.manager.set_tenant_dict, ADMIN_ID, uuid.uuid4().hex, {})

        authz_intra_extension = self.create_intra_extension(policy_model="policy_authz")
        admin_intra_extension = self.create_intra_extension(policy_model="policy_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension": authz_intra_extension['id'],
            "intra_admin_extension": admin_intra_extension['id'],
        }
        data = self.manager.add_tenant_dict(user_id=ADMIN_ID, tenant_dict=new_tenant)
        self.assertEquals(new_tenant["id"], data["id"])
        self.assertEquals(new_tenant["name"], data['tenant']["name"])
        self.assertEquals(new_tenant["intra_authz_extension"], data['tenant']["intra_authz_extension"])
        self.assertEquals(new_tenant["intra_admin_extension"], data['tenant']["intra_admin_extension"])
        data = self.manager.get_tenants_dict(ADMIN_ID)
        self.assertNotEqual(data, {})

        self.assertRaises(TenantUnknown, self.manager.get_tenant_dict, ADMIN_ID, uuid.uuid4().hex)

    def test_exception_tenant_added_name_existing(self):
        authz_intra_extension = self.create_intra_extension(policy_model="policy_authz")
        admin_intra_extension = self.create_intra_extension(policy_model="policy_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension": authz_intra_extension['id'],
            "intra_admin_extension": admin_intra_extension['id'],
        }
        data = self.manager.add_tenant_dict(user_id=ADMIN_ID, tenant_dict=new_tenant)
        self.assertEquals(new_tenant["id"], data["id"])
        self.assertEquals(new_tenant["name"], data['tenant']["name"])
        self.assertEquals(new_tenant["intra_authz_extension"], data['tenant']["intra_authz_extension"])
        self.assertEquals(new_tenant["intra_admin_extension"], data['tenant']["intra_admin_extension"])
        data = self.manager.get_tenants_dict(ADMIN_ID)
        self.assertNotEqual(data, {})

        self.assertRaises(TenantAddedNameExisting, self.manager.add_tenant_dict, ADMIN_ID, new_tenant)

    def test_exception_tenant_no_intra_extension(self):
        authz_intra_extension = self.create_intra_extension(policy_model="policy_authz")
        admin_intra_extension = self.create_intra_extension(policy_model="policy_admin")
        new_tenant = {
            "id": uuid.uuid4().hex,
            "name": "demo",
            "description": uuid.uuid4().hex,
            "intra_authz_extension": authz_intra_extension['id'],
            "intra_admin_extension": admin_intra_extension['id'],
        }
        new_tenant['intra_authz_extension'] = None
        self.assertRaises(TenantNoIntraAuthzExtension, self.manager.add_tenant_dict, ADMIN_ID, new_tenant)
        new_tenant['intra_authz_extension'] = authz_intra_extension['id']
        data = self.manager.add_tenant_dict(user_id=ADMIN_ID, tenant_dict=new_tenant)
        self.assertEquals(new_tenant["id"], data["id"])
        self.assertEquals(new_tenant["name"], data['tenant']["name"])
        self.assertEquals(new_tenant["intra_authz_extension"], data['tenant']["intra_authz_extension"])
        self.assertEquals(new_tenant["intra_admin_extension"], data['tenant']["intra_admin_extension"])
        data = self.manager.get_tenants_dict(ADMIN_ID)
        self.assertNotEqual(data, {})

        new_tenant['intra_authz_extension'] = None
        new_tenant['name'] = "demo2"
        self.assertRaises(TenantNoIntraAuthzExtension, self.manager.set_tenant_dict, ADMIN_ID, new_tenant["id"], new_tenant)
