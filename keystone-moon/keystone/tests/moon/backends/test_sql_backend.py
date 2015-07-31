# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Unit tests for core configuration."""

import uuid
from oslo_config import cfg
from keystone.tests import unit as tests
from keystone.contrib.moon.backends import sql
from keystone.tests.unit.ksfixtures import database
from keystone.contrib.moon.exception import *
from keystone.tests.unit import default_fixtures
from keystone.contrib.moon.core import LogManager

CONF = cfg.CONF


class TestSQL(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestSQL, self).setUp()
        self.load_backends()
        self.load_fixtures(default_fixtures)
        self.driver = sql.IntraExtensionConnector()

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager()
        }

    def config_overrides(self):
        super(TestSQL, self).config_overrides()
        self.config_fixture.config(
            group='moon',
            tenant_driver='keystone.contrib.moon.backends.sql.ConfigurationConnector')

    def test_intra_extensions(self):
        result = self.driver.get_intra_extensions_dict()
        print(type(result))
        self.assertIn("toto", result)
