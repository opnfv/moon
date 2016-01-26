# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Unit tests for core configuration."""

from oslo_config import cfg
from keystone.tests import unit as tests
from keystone.tests.unit.ksfixtures import database
from keystone.tests.unit import default_fixtures
from keystone.contrib.moon.core import LogManager
from keystone.contrib.moon.core import IntraExtensionAdminManager
from keystone.contrib.moon.core import IntraExtensionRootManager
from keystone.contrib.moon.core import ConfigurationManager
from keystone.contrib.moon.core import IntraExtensionAuthzManager
from keystone.tests.moon.unit import *

CONF = cfg.CONF


class TestConfigurationManager(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestConfigurationManager, self).setUp()
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
        self.configuration_manager = self.configuration_api

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager(),
            "admin_api": IntraExtensionAdminManager(),
            "configuration_api": ConfigurationManager(),
            "root_api": IntraExtensionRootManager(),
            "authz_api": IntraExtensionAuthzManager()
        }

    def config_overrides(self):
        super(TestConfigurationManager, self).config_overrides()
        self.config_fixture.config(
            group='moon',
            configuration_driver='keystone.contrib.moon.backends.memory.ConfigurationConnector'
        )
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

    def test_get_policy_template_dict(self):
        data = self.configuration_manager.get_policy_templates_dict(self.ADMIN_ID)
        self.assertIsInstance(data, dict)
        self.assertIn("policy_root", data)

