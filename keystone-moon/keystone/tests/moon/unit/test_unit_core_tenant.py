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

CONF = cfg.CONF


class TestTenantManager(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestTenantManager, self).setUp()
        self.load_backends()
        self.load_fixtures(default_fixtures)
        self.manager = TenantManager()

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager()
        }

    def config_overrides(self):
        super(TestTenantManager, self).config_overrides()
        self.config_fixture.config(
            group='moon',
            tenant_driver='keystone.contrib.moon.backends.sql.TenantConnector')

    def test_add_tenant(self):
        _uuid = uuid.uuid4().hex
        new_mapping = {
            _uuid: {
                "name": uuid.uuid4().hex,
                "authz": uuid.uuid4().hex,
                "admin": uuid.uuid4().hex,
            }
        }
        data = self.manager.set_tenant_dict(
            tenant_id=_uuid,
            tenant_name=new_mapping[_uuid]["name"],
            intra_authz_ext_id=new_mapping[_uuid]["authz"],
            intra_admin_ext_id=new_mapping[_uuid]["admin"]
        )
        self.assertEquals(_uuid, data["id"])
        self.assertEquals(data["name"], new_mapping[_uuid]["name"])
        self.assertEquals(data["authz"], new_mapping[_uuid]["authz"])
        self.assertEquals(data["admin"], new_mapping[_uuid]["admin"])
        data = self.manager.get_tenant_dict()
        self.assertNotEqual(data, {})
        data = self.manager.get_tenant_uuid(new_mapping[_uuid]["authz"])
        self.assertEquals(_uuid, data)
        data = self.manager.get_tenant_uuid(new_mapping[_uuid]["admin"])
        self.assertEquals(_uuid, data)
        data = self.manager.get_admin_extension_uuid(new_mapping[_uuid]["authz"])
        self.assertEquals(new_mapping[_uuid]["admin"], data)

    def test_tenant_list_empty(self):
        data = self.manager.get_tenant_dict()
        self.assertEqual(data, {})

    def test_set_tenant_name(self):
        _uuid = uuid.uuid4().hex
        new_mapping = {
            _uuid: {
                "name": uuid.uuid4().hex,
                "authz": uuid.uuid4().hex,
                "admin": uuid.uuid4().hex,
            }
        }
        data = self.manager.set_tenant_dict(
            tenant_id=_uuid,
            tenant_name=new_mapping[_uuid]["name"],
            intra_authz_ext_id=new_mapping[_uuid]["authz"],
            intra_admin_ext_id=new_mapping[_uuid]["admin"]
        )
        self.assertEquals(_uuid, data["id"])
        self.assertEquals(data["name"], new_mapping[_uuid]["name"])
        data = self.manager.set_tenant_name(_uuid, "new name")
        self.assertEquals(_uuid, data["id"])
        self.assertEquals(data["name"], "new name")
        data = self.manager.get_tenant_name(_uuid)
        self.assertEquals(data, "new name")

    def test_delete_tenant(self):
        _uuid = uuid.uuid4().hex
        new_mapping = {
            _uuid: {
                "name": uuid.uuid4().hex,
                "authz": uuid.uuid4().hex,
                "admin": uuid.uuid4().hex,
            }
        }
        data = self.manager.set_tenant_dict(
            tenant_id=_uuid,
            tenant_name=new_mapping[_uuid]["name"],
            intra_authz_ext_id=new_mapping[_uuid]["authz"],
            intra_admin_ext_id=new_mapping[_uuid]["admin"]
        )
        self.assertEquals(_uuid, data["id"])
        self.assertEquals(data["name"], new_mapping[_uuid]["name"])
        self.assertEquals(data["authz"], new_mapping[_uuid]["authz"])
        self.assertEquals(data["admin"], new_mapping[_uuid]["admin"])
        data = self.manager.get_tenant_dict()
        self.assertNotEqual(data, {})
        self.manager.delete(new_mapping[_uuid]["authz"])
        data = self.manager.get_tenant_dict()
        self.assertEqual(data, {})

    def test_get_extension_uuid(self):
        _uuid = uuid.uuid4().hex
        new_mapping = {
            _uuid: {
                "name": uuid.uuid4().hex,
                "authz": uuid.uuid4().hex,
                "admin": uuid.uuid4().hex,
            }
        }
        data = self.manager.set_tenant_dict(
            tenant_id=_uuid,
            tenant_name=new_mapping[_uuid]["name"],
            intra_authz_ext_id=new_mapping[_uuid]["authz"],
            intra_admin_ext_id=new_mapping[_uuid]["admin"]
        )
        self.assertEquals(_uuid, data["id"])
        data = self.manager.get_extension_id(_uuid)
        self.assertEqual(data, new_mapping[_uuid]["authz"])
        data = self.manager.get_extension_id(_uuid, "admin")
        self.assertEqual(data, new_mapping[_uuid]["admin"])

    def test_unkown_tenant_uuid(self):
        self.assertRaises(TenantIDNotFound, self.manager.get_tenant_name, uuid.uuid4().hex)
        self.assertRaises(TenantIDNotFound, self.manager.set_tenant_name, uuid.uuid4().hex, "new name")
        self.assertRaises(TenantIDNotFound, self.manager.get_extension_id, uuid.uuid4().hex)
        _uuid = uuid.uuid4().hex
        new_mapping = {
            _uuid: {
                "name": uuid.uuid4().hex,
                "authz": uuid.uuid4().hex,
                "admin": uuid.uuid4().hex,
            }
        }
        data = self.manager.set_tenant_dict(
            tenant_id=_uuid,
            tenant_name=new_mapping[_uuid]["name"],
            intra_authz_ext_id=new_mapping[_uuid]["authz"],
            intra_admin_ext_id=""
        )
        self.assertEquals(_uuid, data["id"])
        self.assertRaises(IntraExtensionNotFound, self.manager.get_extension_id, _uuid, "admin")
        self.assertRaises(TenantIDNotFound, self.manager.get_tenant_uuid, uuid.uuid4().hex)
        # self.assertRaises(AdminIntraExtensionNotFound, self.manager.get_admin_extension_uuid, uuid.uuid4().hex)
