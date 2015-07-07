# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Unit tests for LogManager"""

import json
import os
import uuid
import time
from oslo_config import cfg
from keystone.tests import unit as tests
from keystone.contrib.moon.core import IntraExtensionAdminManager
from keystone.tests.unit.ksfixtures import database
from keystone import resource
from keystone.contrib.moon.exception import *
from keystone.tests.unit import default_fixtures
from keystone.contrib.moon.core import LogManager, TenantManager

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
        self.load_backends()
        self.load_fixtures(default_fixtures)
        self.manager = IntraExtensionAdminManager()

    def __get_key_from_value(self, value, values_dict):
        return filter(lambda v: v[1] == value, values_dict.iteritems())[0][0]

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager(),
            "tenant_api": TenantManager(),
            # "resource_api": resource.Manager(),
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

    def create_intra_extension(self, policy_model="policy_rbac_admin"):
        # Create the admin user because IntraExtension needs it
        self.admin = self.identity_api.create_user(USER_ADMIN)
        IE["policymodel"] = policy_model
        self.ref = self.manager.load_intra_extension(IE)
        self.assertIsInstance(self.ref, dict)
        self.create_tenant(self.ref["id"])

    def create_tenant(self, authz_uuid):
        tenant = {
            "id": uuid.uuid4().hex,
            "name": "TestAuthzIntraExtensionManager",
            "enabled": True,
            "description": "",
            "domain_id": "default"
        }
        project = self.resource_api.create_project(tenant["id"], tenant)
        mapping = self.tenant_api.set_tenant_dict(project["id"], project["name"], authz_uuid, None)
        self.assertIsInstance(mapping, dict)
        self.assertIn("authz", mapping)
        self.assertEqual(mapping["authz"], authz_uuid)
        return mapping

    def create_user(self, username="TestAdminIntraExtensionManagerUser"):
        user = {
            "id": uuid.uuid4().hex,
            "name": username,
            "enabled": True,
            "description": "",
            "domain_id": "default"
        }
        _user = self.identity_api.create_user(user)
        return _user

    def delete_admin_intra_extension(self):
        self.manager.delete_intra_extension(self.ref["id"])

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

