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
from keystone.contrib.moon.core import LogManager

CONF = cfg.CONF


class TestConfigurationManager(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestConfigurationManager, self).setUp()
        self.load_backends()
        self.load_fixtures(default_fixtures)
        self.manager = ConfigurationManager()

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager()
        }

    def config_overrides(self):
        super(TestConfigurationManager, self).config_overrides()
        self.config_fixture.config(
            group='moon',
            tenant_driver='keystone.contrib.moon.backends.sql.ConfigurationConnector')

    def test_get_policy_template_dict(self):
        pass

    def test_get_policy_template_id_from_name(self):
        pass

    def test_get_aggregation_algorithm_dict(self):
        pass

    def test_get_aggregation_algorithm_id_from_name(self):
        pass

    def test_get_sub_meta_rule_algorithm_dict(self):
        pass

    def test_get_sub_meta_rule_algorithm_id_from_name(self):
        pass

