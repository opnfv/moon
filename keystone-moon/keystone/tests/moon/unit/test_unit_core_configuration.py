# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Unit tests for core configuration."""

import uuid
from oslo_config import cfg
from keystone.tests import unit as tests
from keystone.contrib.moon.core import ConfigurationManager
from keystone.tests.unit.ksfixtures import database
from keystone.contrib.moon.exception import *
from keystone.tests.unit import default_fixtures
from keystone.contrib.moon.core import ADMIN_ID
from keystone.contrib.moon.core import LogManager
from keystone.contrib.moon.core import IntraExtensionAdminManager
from keystone.tests.moon.unit import *

CONF = cfg.CONF


@dependency.requires('admin_api', 'authz_api', 'tenant_api', 'configuration_api', 'moonlog_api')
class TestConfigurationManager(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestConfigurationManager, self).setUp()
        self.load_backends()
        self.load_fixtures(default_fixtures)
        self.admin = create_user(self, username="admin")
        self.demo = create_user(self, username="demo")
        self.root_intra_extension = create_intra_extension(self, policy_model="policy_root")
        # force re-initialization of the ADMIN_ID variable
        from keystone.contrib.moon.core import ADMIN_ID
        self.ADMIN_ID = ADMIN_ID
        self.manager = self.configuration_api

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager(),
            "admin_api": IntraExtensionAdminManager()
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
        data = self.manager.get_policy_templates_dict(self.ADMIN_ID)
        self.assertIsInstance(data, dict)
        self.assertIn("authz_templates", data)
        self.assertIn("policy_root", data["authz_templates"])

    # def test_get_aggregation_algorithm_dict(self):
    #     admin_intra_extension = create_intra_extension(self, policy_model="policy_admin")
    #     print(admin_intra_extension)
    #     data = self.manager.get_aggregation_algorithm_dict(self.ADMIN_ID, admin_intra_extension['id'])
    #     print(data)

    # def test_get_sub_meta_rule_algorithm_dict(self):
    #     data = self.manager.get_sub_meta_rule_algorithm_dict(self.ADMIN_ID)
    #     print(data)
    #
    #     self.assertEqual("", "ee")

