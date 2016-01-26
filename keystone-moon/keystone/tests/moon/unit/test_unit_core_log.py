# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Unit tests for LogManager"""

import time
from oslo_config import cfg
from keystone.tests import unit as tests
from keystone.contrib.moon.core import ConfigurationManager
from keystone.contrib.moon.core import IntraExtensionAuthzManager
from keystone.tests.unit.ksfixtures import database
from keystone.contrib.moon.exception import *
from keystone.tests.unit import default_fixtures
from keystone.contrib.moon.core import LogManager, TenantManager
from keystone.tests.moon.unit import *

CONF = cfg.CONF

USER_ADMIN = {
    'name': 'admin',
    'domain_id': "default",
    'password': 'admin'
}

IE = {
    "name": "test IE",
    "policymodel": "policy_rbac_authz",
    "description": "a simple description."
}

TIME_FORMAT = '%Y-%m-%d-%H:%M:%S'


class TestIntraExtensionAdminManager(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestIntraExtensionAdminManager, self).setUp()
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

    def __get_key_from_value(self, value, values_dict):
        return filter(lambda v: v[1] == value, values_dict.iteritems())[0][0]

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager(),
            "authz_api": IntraExtensionAuthzManager(),
            "tenant_api": TenantManager(),
            "configuration_api": ConfigurationManager(),
        }

    def config_overrides(self):
        super(TestIntraExtensionAdminManager, self).config_overrides()
        self.policy_directory = 'examples/moon/policies'
        self.config_fixture.config(
            group='moon',
            intraextension_driver='keystone.contrib.moon.backends.sql.IntraExtensionConnector')
        self.config_fixture.config(
            group='moon',
            policy_directory=self.policy_directory)

    def send_logs(self):
        log_authz = "Test for authz " + uuid.uuid4().hex
        logs = []
        self.moonlog_api.authz(log_authz)
        logs.append("Test for critical " + uuid.uuid4().hex)
        self.moonlog_api.critical(logs[-1])
        logs.append("Test for error " + uuid.uuid4().hex)
        self.moonlog_api.error(logs[-1])
        logs.append("Test for warning " + uuid.uuid4().hex)
        self.moonlog_api.warning(logs[-1])
        logs.append("Test for info " + uuid.uuid4().hex)
        self.moonlog_api.info(logs[-1])
        logs.append("Test for debug " + uuid.uuid4().hex)
        self.moonlog_api.debug(logs[-1])
        return log_authz, logs

    def test_get_set_logs(self):
        previous_authz_logs = self.moonlog_api.get_logs(logger="authz")
        previous_sys_logs = self.moonlog_api.get_logs(logger="sys")

        log_authz, logs = self.send_logs()
        time.sleep(1)

        authz_logs = self.moonlog_api.get_logs(logger="authz")
        sys_logs = self.moonlog_api.get_logs(logger="sys")

        self.assertIsInstance(authz_logs, list)
        self.assertIsInstance(sys_logs, list)

        self.assertIn(log_authz, " ".join(authz_logs))

        self.assertEqual(len(authz_logs), len(previous_authz_logs)+1)
        self.assertTrue(len(sys_logs) >= len(previous_sys_logs)+5)
        for log in logs:
            self.assertIn(log, " ".join(sys_logs))

    def test_get_syslogger_with_options(self):

        all_logs = self.moonlog_api.get_logs(logger="sys")

        time_1 = time.strftime(TIME_FORMAT)
        time.sleep(1)

        log_authz, logs = self.send_logs()

        NUMBER_OF_LOG = 5
        sys_logs = self.moonlog_api.get_logs(logger="sys", event_number=NUMBER_OF_LOG)
        self.assertIsInstance(sys_logs, list)
        self.assertEqual(len(sys_logs), NUMBER_OF_LOG)

        sys_logs = self.moonlog_api.get_logs(logger="sys", time_from=time_1)
        self.assertIsInstance(sys_logs, list)
        self.assertEqual(len(sys_logs), NUMBER_OF_LOG)

        log_authz, logs = self.send_logs()

        time.sleep(1)
        time_2 = time.strftime(TIME_FORMAT)

        log_authz, logs = self.send_logs()

        sys_logs = self.moonlog_api.get_logs(logger="sys", time_to=time_2)
        self.assertIsInstance(sys_logs, list)
        self.assertEqual(len(sys_logs), len(all_logs)+3*NUMBER_OF_LOG)

        sys_logs = self.moonlog_api.get_logs(logger="sys", time_from=time_1, time_to=time_2)
        self.assertIsInstance(sys_logs, list)
        self.assertEqual(len(sys_logs), 3*NUMBER_OF_LOG)

