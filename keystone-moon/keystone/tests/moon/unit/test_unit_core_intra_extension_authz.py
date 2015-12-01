# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Unit tests for core IntraExtensionAuthzManager"""

import json
import os
import uuid
from oslo_config import cfg
from keystone.tests import unit as tests
from keystone.contrib.moon.core import IntraExtensionAdminManager, IntraExtensionAuthzManager, IntraExtensionRootManager
from keystone.contrib.moon.core import ConfigurationManager
from keystone.tests.unit.ksfixtures import database
from keystone import resource
from keystone.contrib.moon.exception import *
from keystone.tests.unit import default_fixtures
from keystone.contrib.moon.core import LogManager, TenantManager
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

#@dependency.requires('admin_api', 'authz_api', 'tenant_api', 'configuration_api', 'moonlog_api')
class TestIntraExtensionAuthzManagerAuthzOK(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestIntraExtensionAuthzManagerAuthzOK, self).setUp()
        self.load_fixtures(default_fixtures)
        self.load_backends()
        domain = {'id': "default", 'name': "default"}
        self.resource_api.create_domain(domain['id'], domain)
        self.admin = create_user(self, username="admin")
        self.demo = create_user(self, username="demo")
        self.root_intra_extension = self.root_api.get_root_extension_dict()
        self.root_intra_extension_id = self.root_intra_extension.keys()[0]
        self.ADMIN_ID = self.root_api.get_root_admin_id()
        self.authz_manager = self.authz_api
        self.admin_manager = self.admin_api

    def __get_key_from_value(self, value, values_dict):
        return filter(lambda v: v[1] == value, values_dict.iteritems())[0][0]

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager(),
            "tenant_api": TenantManager(),
            "admin_api": IntraExtensionAdminManager(),
            "authz_api": IntraExtensionAuthzManager(),
            "configuration_api": ConfigurationManager(),
            # "resource_api": resource.Manager(),
        }

    def config_overrides(self):
        super(TestIntraExtensionAuthzManagerAuthzOK, self).config_overrides()
        self.policy_directory = 'examples/moon/policies'
        self.config_fixture.config(
            group='moon',
            intraextension_driver='keystone.contrib.moon.backends.sql.IntraExtensionConnector')
        self.config_fixture.config(
            group='moon',
            policy_directory=self.policy_directory)

    def delete_admin_intra_extension(self):
        self.authz_manager.del_intra_extension(self.ref["id"])

    def test_subjects(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        subjects = self.authz_manager.get_subjects_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(subjects, dict)
        for key, value in subjects.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)
            self.assertIn("keystone_name", value)
            self.assertIn("keystone_id", value)

        create_user(self, "subject_test")
        new_subject = {"name": "subject_test", "description": "subject_test"}

        subjects = self.admin_manager.add_subject_dict(admin_subject_id, authz_ie_dict["id"], new_subject)
        _subjects = dict(subjects)
        self.assertEqual(len(_subjects.keys()), 1)
        new_subject["id"] = _subjects.keys()[0]
        value = subjects[new_subject["id"]]
        self.assertIsInstance(value, dict)
        self.assertIn("name", value)
        self.assertEqual(value["name"], new_subject["name"])
        self.assertIn("description", value)
        self.assertEqual(value["description"], new_subject["description"])

        # Delete the new subject
        self.admin_manager.del_subject(admin_subject_id, authz_ie_dict["id"], new_subject["id"])
        subjects = self.authz_manager.get_subjects_dict(admin_subject_id, authz_ie_dict["id"])
        for key, value in subjects.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIsNot(new_subject["name"], value["name"])
            self.assertIn("description", value)

    def test_objects(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        objects = self.authz_manager.get_objects_dict(admin_subject_id, authz_ie_dict["id"])
        objects_id_list = []
        self.assertIsInstance(objects, dict)
        for key, value in objects.iteritems():
            objects_id_list.append(key)
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

    def test_actions(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        actions = self.authz_manager.get_actions_dict(admin_subject_id, authz_ie_dict["id"])
        actions_id_list = []
        self.assertIsInstance(actions, dict)
        for key, value in actions.iteritems():
            actions_id_list.append(key)
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

    def test_subject_categories(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        subject_categories = self.authz_manager.get_subject_categories_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(subject_categories, dict)
        for key, value in subject_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

        new_subject_category = {"name": "subject_category_test", "description": "subject_category_test"}

        subject_categories = self.admin_manager.add_subject_category_dict(admin_subject_id, authz_ie_dict["id"], new_subject_category)
        _subject_categories = dict(subject_categories)
        self.assertEqual(len(_subject_categories.keys()), 1)
        new_subject_category["id"] = _subject_categories.keys()[0]
        value = subject_categories[new_subject_category["id"]]
        self.assertIsInstance(value, dict)
        self.assertIn("name", value)
        self.assertEqual(value["name"], new_subject_category["name"])
        self.assertIn("description", value)
        self.assertEqual(value["description"], new_subject_category["description"])

        # Delete the new subject_category
        self.admin_manager.del_subject_category(admin_subject_id, authz_ie_dict["id"], new_subject_category["id"])
        subject_categories = self.authz_manager.get_subject_categories_dict(admin_subject_id, authz_ie_dict["id"])
        for key, value in subject_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIsNot(new_subject_category["name"], value["name"])
            self.assertIn("description", value)

    def test_object_categories(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        object_categories = self.authz_manager.get_object_categories_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(object_categories, dict)
        for key, value in object_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

        new_object_category = {"name": "object_category_test", "description": "object_category_test"}

        object_categories = self.admin_manager.add_object_category_dict(admin_subject_id, authz_ie_dict["id"], new_object_category)
        _object_categories = dict(object_categories)
        self.assertEqual(len(_object_categories.keys()), 1)
        new_object_category["id"] = _object_categories.keys()[0]
        value = object_categories[new_object_category["id"]]
        self.assertIsInstance(value, dict)
        self.assertIn("name", value)
        self.assertEqual(value["name"], new_object_category["name"])
        self.assertIn("description", value)
        self.assertEqual(value["description"], new_object_category["description"])

        # Delete the new object_category

        self.admin_manager.del_object_category(admin_subject_id, authz_ie_dict["id"], new_object_category["id"])
        object_categories = self.authz_manager.get_object_categories_dict(admin_subject_id, authz_ie_dict["id"])
        for key, value in object_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIsNot(new_object_category["name"], value["name"])
            self.assertIn("description", value)

    def test_action_categories(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        action_categories = self.authz_manager.get_action_categories_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(action_categories, dict)
        for key, value in action_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

        new_action_category = {"name": "action_category_test", "description": "action_category_test"}

        action_categories = self.admin_manager.add_action_category_dict(admin_subject_id, authz_ie_dict["id"], new_action_category)
        _action_categories = dict(action_categories)
        self.assertEqual(len(_action_categories.keys()), 1)
        new_action_category["id"] = _action_categories.keys()[0]
        value = action_categories[new_action_category["id"]]
        self.assertIsInstance(value, dict)
        self.assertIn("name", value)
        self.assertEqual(value["name"], new_action_category["name"])
        self.assertIn("description", value)
        self.assertEqual(value["description"], new_action_category["description"])

        # Delete the new action_category

        self.admin_manager.del_action_category(admin_subject_id, authz_ie_dict["id"], new_action_category["id"])
        action_categories = self.authz_manager.get_action_categories_dict(admin_subject_id, authz_ie_dict["id"])
        for key, value in action_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIsNot(new_action_category["name"], value["name"])
            self.assertIn("description", value)

    def test_subject_category_scope(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        subject_categories = self.admin_manager.add_subject_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "country",
                "description": "country",
            }
        )

        for subject_category_id in subject_categories:

            subject_category_scope = self.authz_manager.get_subject_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertEqual({}, subject_category_scope)

            new_subject_category_scope = {
                "name": "france",
                "description": "france",
            }

            subject_category_scope = self.admin_manager.add_subject_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id,
                new_subject_category_scope)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertEqual(len(subject_category_scope.keys()), 1)
            subject_category_scope_id = subject_category_scope.keys()[0]
            subject_category_scope_value = subject_category_scope[subject_category_scope_id]
            self.assertIn("name", subject_category_scope_value)
            self.assertEqual(new_subject_category_scope["name"], subject_category_scope_value["name"])
            self.assertIn("description", subject_category_scope_value)
            self.assertEqual(new_subject_category_scope["description"], subject_category_scope_value["description"])

            # Delete the new subject_category_scope

            self.admin_manager.del_subject_scope(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id,
                subject_category_scope_id)
            subject_category_scope = self.admin_manager.get_subject_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertNotIn(subject_category_scope_id, subject_category_scope.keys())

    def test_object_category_scope(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        object_categories = self.admin_manager.add_object_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "country",
                "description": "country",
            }
        )

        for object_category_id in object_categories:

            object_category_scope = self.authz_manager.get_object_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id)
            self.assertIsInstance(object_category_scope, dict)
            self.assertEqual({}, object_category_scope)

            new_object_category_scope = {
                "name": "france",
                "description": "france",
            }

            object_category_scope = self.admin_manager.add_object_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id,
                new_object_category_scope)
            self.assertIsInstance(object_category_scope, dict)
            self.assertEqual(len(object_category_scope.keys()), 1)
            object_category_scope_id = object_category_scope.keys()[0]
            object_category_scope_value = object_category_scope[object_category_scope_id]
            self.assertIn("name", object_category_scope_value)
            self.assertEqual(new_object_category_scope["name"], object_category_scope_value["name"])
            self.assertIn("description", object_category_scope_value)
            self.assertEqual(new_object_category_scope["description"], object_category_scope_value["description"])

            # Delete the new object_category_scope

            self.admin_manager.del_object_scope(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id,
                object_category_scope_id)
            object_category_scope = self.admin_manager.get_object_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id)
            self.assertIsInstance(object_category_scope, dict)
            self.assertNotIn(object_category_scope_id, object_category_scope.keys())

    def test_action_category_scope(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        action_categories = self.admin_manager.add_action_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "swift",
                "description": "swift actions",
            }
        )

        for action_category_id in action_categories:

            action_category_scope = self.authz_manager.get_action_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id)
            self.assertIsInstance(action_category_scope, dict)
            self.assertEqual({}, action_category_scope)

            new_action_category_scope = {
                "name": "get",
                "description": "get swift files",
            }

            action_category_scope = self.admin_manager.add_action_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id,
                new_action_category_scope)
            self.assertIsInstance(action_category_scope, dict)
            self.assertEqual(len(action_category_scope.keys()), 1)
            action_category_scope_id = action_category_scope.keys()[0]
            action_category_scope_value = action_category_scope[action_category_scope_id]
            self.assertIn("name", action_category_scope_value)
            self.assertEqual(new_action_category_scope["name"], action_category_scope_value["name"])
            self.assertIn("description", action_category_scope_value)
            self.assertEqual(new_action_category_scope["description"], action_category_scope_value["description"])

            # Delete the new action_category_scope

            self.admin_manager.del_action_scope(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id,
                action_category_scope_id)
            action_category_scope = self.admin_manager.get_action_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id)
            self.assertIsInstance(action_category_scope, dict)
            self.assertNotIn(action_category_scope_id, action_category_scope.keys())

    def test_subject_category_assignment(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        admin_authz_subject_id, admin_authz_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], authz_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        demo_authz_subject_id, demo_authz_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], authz_ie_dict['id'], 'demo').iteritems().next()

        subjects_dict = self.authz_manager.get_subjects_dict(admin_subject_id, authz_ie_dict["id"])

        subject_categories = self.admin_manager.add_subject_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "country",
                "description": "country",
            }
        )

        for subject_category_id in subject_categories:
            subject_category_scope = self.authz_manager.get_subject_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertEqual({}, subject_category_scope)

            new_subject_category_scope_1 = {
                "name": "france",
                "description": "france",
            }

            subject_category_scope_1 = self.admin_manager.add_subject_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id,
                new_subject_category_scope_1)
            subject_category_scope_1_id = subject_category_scope_1.keys()[0]

            new_subject_category_scope_2 = {
                "name": "china",
                "description": "china",
            }

            subject_category_scope_2 = self.admin_manager.add_subject_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id,
                new_subject_category_scope_2)
            subject_category_scope_2_id = subject_category_scope_2.keys()[0]

            subject_category_assignments = self.authz_manager.get_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id,
                subject_category_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual([], subject_category_assignments)

            subject_category_assignments = self.authz_manager.get_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                demo_authz_subject_id,
                subject_category_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual([], subject_category_assignments)

            subject_category_assignments = self.admin_manager.add_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id, subject_category_scope_1_id
            )
            self.assertIsInstance(subject_category_assignments, list)

            self.assertEqual(len(subject_category_assignments), 1)

            subject_category_assignments = self.admin_manager.add_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id, subject_category_scope_2_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual(len(subject_category_assignments), 2)

            subject_category_assignments = self.admin_manager.add_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                demo_authz_subject_id, subject_category_id, subject_category_scope_2_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual(len(subject_category_assignments), 1)

            subject_category_assignments = self.admin_manager.get_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual(len(subject_category_assignments), 2)

            self.admin_manager.del_subject_assignment(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id, subject_category_scope_2_id
            )
            subject_category_assignments = self.admin_manager.get_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual(len(subject_category_assignments), 1)

    def test_object_category_assignment(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        objects_dict = self.authz_manager.get_objects_dict(admin_subject_id, authz_ie_dict["id"])

        object_vm1 = self.admin_manager.add_object_dict(admin_subject_id, authz_ie_dict["id"], {"name": "vm1", "description": "vm1"})
        object_vm2 = self.admin_manager.add_object_dict(admin_subject_id, authz_ie_dict["id"], {"name": "vm2", "description": "vm2"})
        object_vm1_id = object_vm1.keys()[0]
        object_vm2_id = object_vm2.keys()[0]
        if not object_vm1_id or not object_vm2_id:
            raise Exception("Cannot run tests, database is corrupted ? (need upload and list in objects)")

        object_categories = self.admin_manager.add_object_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "location",
                "description": "location",
            }
        )

        for object_category_id in object_categories:
            object_category_scope = self.authz_manager.get_object_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id)
            self.assertIsInstance(object_category_scope, dict)
            self.assertEqual({}, object_category_scope)

            new_object_category_scope_1 = {
                "name": "france",
                "description": "france",
            }

            object_category_scope_1 = self.admin_manager.add_object_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id,
                new_object_category_scope_1)
            object_category_scope_1_id = object_category_scope_1.keys()[0]

            new_object_category_scope_2 = {
                "name": "china",
                "description": "china",
            }

            object_category_scope_2 = self.admin_manager.add_object_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id,
                new_object_category_scope_2)
            object_category_scope_2_id = object_category_scope_2.keys()[0]

            object_category_assignments = self.authz_manager.get_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id,
                object_category_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual([], object_category_assignments)

            object_category_assignments = self.authz_manager.get_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm2_id,
                object_category_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual([], object_category_assignments)

            object_category_assignments = self.admin_manager.add_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id, object_category_scope_1_id
            )
            self.assertIsInstance(object_category_assignments, list)

            self.assertEqual(len(object_category_assignments), 1)

            object_category_assignments = self.admin_manager.add_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id, object_category_scope_2_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual(len(object_category_assignments), 2)

            object_category_assignments = self.admin_manager.add_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm2_id, object_category_id, object_category_scope_2_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual(len(object_category_assignments), 1)

            object_category_assignments = self.admin_manager.get_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual(len(object_category_assignments), 2)

            self.admin_manager.del_object_assignment(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id, object_category_scope_2_id
            )
            object_category_assignments = self.admin_manager.get_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual(len(object_category_assignments), 1)

    def test_action_category_assignment(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        actions_dict = self.authz_manager.get_actions_dict(admin_subject_id, authz_ie_dict["id"])

        action_upload_id = None
        action_list_id = None
        for _action_id in actions_dict:
            if actions_dict[_action_id]['name'] == 'upload':
                action_upload_id = _action_id
            if actions_dict[_action_id]['name'] == 'list':
                action_list_id = _action_id
        if not action_upload_id or not action_list_id:
            raise Exception("Cannot run tests, database is corrupted ? (need upload and list in actions)")

        action_categories = self.admin_manager.add_action_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "swift",
                "description": "swift actions",
            }
        )

        for action_category_id in action_categories:
            action_category_scope = self.authz_manager.get_action_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id)
            self.assertIsInstance(action_category_scope, dict)
            self.assertEqual({}, action_category_scope)

            new_action_category_scope_1 = {
                "name": "swift_admin",
                "description": "action require admin rights",
            }

            action_category_scope_1 = self.admin_manager.add_action_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id,
                new_action_category_scope_1)
            action_category_scope_1_id = action_category_scope_1.keys()[0]

            new_action_category_scope_2 = {
                "name": "swift_anonymous",
                "description": "action require no right",
            }

            action_category_scope_2 = self.admin_manager.add_action_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id,
                new_action_category_scope_2)
            action_category_scope_2_id = action_category_scope_2.keys()[0]

            action_category_assignments = self.authz_manager.get_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id,
                action_category_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual([], action_category_assignments)

            action_category_assignments = self.authz_manager.get_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_list_id,
                action_category_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual([], action_category_assignments)

            action_category_assignments = self.admin_manager.add_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id, action_category_scope_1_id
            )
            self.assertIsInstance(action_category_assignments, list)

            self.assertEqual(len(action_category_assignments), 1)

            action_category_assignments = self.admin_manager.add_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id, action_category_scope_2_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual(len(action_category_assignments), 2)

            action_category_assignments = self.admin_manager.add_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_list_id, action_category_id, action_category_scope_2_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual(len(action_category_assignments), 1)

            action_category_assignments = self.admin_manager.get_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual(len(action_category_assignments), 2)

            self.admin_manager.del_action_assignment(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id, action_category_scope_2_id
            )
            action_category_assignments = self.admin_manager.get_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual(len(action_category_assignments), 1)

    def test_sub_meta_rules(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        aggregation_algorithm = self.admin_manager.get_aggregation_algorithm_id(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(aggregation_algorithm, dict)

        # TODO: need more tests on aggregation_algorithms (set and del)

        sub_meta_rules = self.admin_manager.get_sub_meta_rules_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(sub_meta_rules, dict)
        categories = {
            "subject_categories": self.admin_manager.get_subject_categories_dict(admin_subject_id, authz_ie_dict["id"]),
            "object_categories": self.admin_manager.get_object_categories_dict(admin_subject_id, authz_ie_dict["id"]),
            "action_categories": self.admin_manager.get_action_categories_dict(admin_subject_id, authz_ie_dict["id"])
        }
        for key, value in sub_meta_rules.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("action_categories", value)
            self.assertIn("object_categories", value)
            self.assertIn("subject_categories", value)
            self.assertIn("algorithm", value)
            self.assertIn("name", value)
            for action_category_id in value["action_categories"]:
                self.assertIn(action_category_id, categories["action_categories"])
            for object_category_id in value["object_categories"]:
                self.assertIn(object_category_id, categories["object_categories"])
            for subject_category_id in value["subject_categories"]:
                self.assertIn(subject_category_id, categories["subject_categories"])
        # TODO: need more tests (set and del)

    def test_sub_rules(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        sub_meta_rules = self.admin_manager.get_sub_meta_rules_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(sub_meta_rules, dict)

        for relation_id in sub_meta_rules:
            rules = self.admin_manager.get_rules_dict(admin_subject_id, authz_ie_dict["id"], relation_id)
            rule_length = len(sub_meta_rules[relation_id]["subject_categories"]) + \
                len(sub_meta_rules[relation_id]["object_categories"]) + \
                len(sub_meta_rules[relation_id]["action_categories"]) + 1
            for rule_id in rules:
                self.assertEqual(rule_length, len(rules[rule_id]))
                rule = list(rules[rule_id])
                for cat, cat_func, func_name in (
                    ("subject_categories", self.admin_manager.get_subject_scopes_dict, "subject_scope"),
                    ("action_categories", self.admin_manager.get_action_scopes_dict, "action_scope"),
                    ("object_categories", self.admin_manager.get_object_scopes_dict, "object_scope"),
                ):
                    for cat_value in sub_meta_rules[relation_id][cat]:
                        scope = cat_func(
                            admin_subject_id,
                            authz_ie_dict["id"],
                            cat_value
                        )
                        a_scope = rule.pop(0)
                        if type(a_scope) is not bool:
                            self.assertIn(a_scope, scope.keys())

            # add a new subrule

            sub_rule = []
            for cat, cat_func, func_name in (
                ("subject_categories", self.admin_manager.get_subject_scopes_dict, "subject_scope"),
                ("action_categories", self.admin_manager.get_action_scopes_dict, "action_scope"),
                ("object_categories", self.admin_manager.get_object_scopes_dict, "object_scope"),
            ):
                for cat_value in sub_meta_rules[relation_id][cat]:
                    scope = cat_func(
                        admin_subject_id,
                        authz_ie_dict["id"],
                        cat_value
                    )
                    sub_rule.append(scope.keys()[0])

            sub_rule.append(False)

            sub_rules = self.admin_manager.add_rule_dict(admin_subject_id, authz_ie_dict["id"], relation_id, sub_rule)
            self.assertIsInstance(sub_rules, dict)
            self.assertIn(sub_rule, sub_rules.values())

            for rule_id, rule_value in sub_rules.iteritems():
                for cat, cat_func, func_name in (
                    ("subject_categories", self.admin_manager.get_subject_scopes_dict, "subject_category_scope"),
                    ("action_categories", self.admin_manager.get_action_scopes_dict, "action_category_scope"),
                    ("object_categories", self.admin_manager.get_object_scopes_dict, "object_category_scope"),
                ):
                    for cat_value in sub_meta_rules[relation_id][cat]:
                        scope = cat_func(
                            admin_subject_id,
                            authz_ie_dict["id"],
                            cat_value
                        )
                        a_scope = rule_value.pop(0)
                        self.assertIn(a_scope, scope.keys())

        # TODO: add test for the delete function


#@dependency.requires('admin_api', 'authz_api', 'tenant_api', 'configuration_api', 'moonlog_api', 'identity_api', 'root_api')
class TestIntraExtensionAuthzManagerAuthzKO(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestIntraExtensionAuthzManagerAuthzKO, self).setUp()
        self.load_fixtures(default_fixtures)
        self.load_backends()
        domain = {'id': "default", 'name': "default"}
        self.resource_api.create_domain(domain['id'], domain)
        self.admin = create_user(self, username="admin")
        self.demo = create_user(self, username="demo")
        self.root_intra_extension = self.root_api.get_root_extension_dict()
        self.root_intra_extension_id = self.root_intra_extension.keys()[0]
        self.ADMIN_ID = self.root_api.get_root_admin_id()
        self.authz_manager = self.authz_api
        self.admin_manager = self.admin_api

    def tearDown(self):
        # self.admin_manager.del_intra_extension(self.ADMIN_ID, self.root_intra_extension["id"])
        tests.TestCase.tearDown(self)

    def __get_key_from_value(self, value, values_dict):
        return filter(lambda v: v[1] == value, values_dict.iteritems())[0][0]

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager(),
            "tenant_api": TenantManager(),
            "configuration_api": ConfigurationManager(),
            "admin_api": IntraExtensionAdminManager(),
            "authz_api": IntraExtensionAuthzManager(),
            "root_api": IntraExtensionRootManager(),
            # "resource_api": resource.Manager(),
        }

    def config_overrides(self):
        super(TestIntraExtensionAuthzManagerAuthzKO, self).config_overrides()
        self.policy_directory = 'examples/moon/policies'
        self.root_policy_directory = 'policy_root'
        self.config_fixture.config(
            group='moon',
            intraextension_driver='keystone.contrib.moon.backends.sql.IntraExtensionConnector')
        self.config_fixture.config(
            group='moon',
            policy_directory=self.policy_directory)
        self.config_fixture.config(
            group='moon',
            root_policy_directory=self.root_policy_directory)

    def test_delete_admin_intra_extension(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        self.assertRaises(
            SubjectUnknown,
            self.authz_manager.del_intra_extension,
            uuid.uuid4().hex,
            admin_ie_dict["id"])

    def test_authz_exceptions(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        # Test when subject is unknown
        self.assertRaises(
            SubjectUnknown,
            self.authz_manager.authz,
            tenant["id"], uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex
        )

        # Test when subject is known but not the object
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], authz_ie_dict['id'], 'demo').iteritems().next()

        # self.manager.add_subject_dict(
        #     admin_subject_id,
        #     ie_authz["id"],
        #     demo_user["id"]
        # )

        self.assertRaises(
            ObjectUnknown,
            self.authz_manager.authz,
            tenant["id"], demo_subject_dict["keystone_id"], uuid.uuid4().hex, uuid.uuid4().hex
        )

        # Test when subject and object are known but not the action
        my_object = {"name": "my_object", "description": "my_object description"}
        _tmp = self.admin_manager.add_object_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            my_object
        )
        my_object["id"] = _tmp.keys()[0]

        self.assertRaises(
            ActionUnknown,
            self.authz_manager.authz,
            tenant["id"], demo_subject_dict["keystone_id"], my_object["name"], uuid.uuid4().hex
        )

        # Test when subject and object and action are known
        my_action = {"name": "my_action", "description": "my_action description"}
        _tmp = self.admin_manager.add_action_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            my_action
        )
        my_action["id"] = _tmp.keys()[0]

        self.assertRaises(
            AuthzException,
            self.authz_manager.authz,
            tenant["id"], demo_subject_dict["keystone_id"], my_object["name"], my_action["name"]
        )

        # Add a subject scope and test ObjectCategoryAssignmentOutOfScope
        my_subject_category = {"name": "my_subject_category", "description": "my_subject_category description"}
        _tmp = self.admin_manager.add_subject_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            my_subject_category
        )
        my_subject_category["id"] = _tmp.keys()[0]

        my_subject_scope = {"name": "my_subject_scope", "description": "my_subject_scope description"}
        _tmp = self.admin_manager.add_subject_scope_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            my_subject_category["id"],
            my_subject_scope
        )
        my_subject_scope["id"] = _tmp.keys()[0]

        self.assertRaises(
            AuthzException,
            self.authz_manager.authz,
            tenant["id"], demo_subject_dict["keystone_id"], my_object["name"], my_action["name"]
        )

        # Add an object scope and test ActionCategoryAssignmentOutOfScope
        my_object_category = {"name": "my_object_category", "description": "my_object_category description"}
        _tmp = self.admin_manager.add_object_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            my_object_category
        )
        my_object_category["id"] = _tmp.keys()[0]

        my_object_scope = {"name": "my_object_scope", "description": "my_object_scope description"}
        _tmp = self.admin_manager.add_object_scope_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            my_object_category["id"],
            my_object_scope
        )
        my_object_scope["id"] = _tmp.keys()[0]

        self.assertRaises(
            AuthzException,
            self.authz_manager.authz,
            tenant["id"], demo_subject_dict["keystone_id"], my_object["name"], my_action["name"]
        )

        # Add an action scope and test SubjectCategoryAssignmentUnknown
        my_action_category = {"name": "my_action_category", "description": "my_action_category description"}
        _tmp = self.admin_manager.add_action_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            my_action_category
        )
        my_action_category["id"] = _tmp.keys()[0]

        my_action_scope = {"name": "my_action_scope", "description": "my_action_scope description"}
        _tmp = self.admin_manager.add_action_scope_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            my_action_category["id"],
            my_action_scope
        )
        my_action_scope["id"] = _tmp.keys()[0]

        self.assertRaises(
            AuthzException,
            self.authz_manager.authz,
            tenant["id"], demo_subject_dict["keystone_id"], my_object["name"], my_action["name"]
        )

        # Add a subject assignment and test ObjectCategoryAssignmentUnknown
        self.admin_manager.add_subject_assignment_list(
            admin_subject_id,
            authz_ie_dict["id"],
            demo_subject_id,
            my_subject_category["id"],
            my_subject_scope["id"]
        )

        self.assertRaises(
            AuthzException,
            self.authz_manager.authz,
            tenant["id"], demo_subject_dict["keystone_id"], my_object["name"], my_action["name"]
        )

        # Add an object assignment and test ActionCategoryAssignmentUnknown
        self.admin_manager.add_object_assignment_list(
            admin_subject_id,
            authz_ie_dict["id"],
            my_object["id"],
            my_object_category["id"],
            my_object_scope["id"]
        )

        self.assertRaises(
            AuthzException,
            self.authz_manager.authz,
            tenant["id"], demo_subject_dict["keystone_id"], my_object["name"], my_action["name"]
        )

        # Add an action assignment and test RuleUnknown
        self.admin_manager.add_action_assignment_list(
            admin_subject_id,
            authz_ie_dict["id"],
            my_action["id"],
            my_action_category["id"],
            my_action_scope["id"]
        )

        self.assertRaises(
            AuthzException,
            self.authz_manager.authz,
            tenant["id"], admin_subject_dict["keystone_id"], my_object["name"], my_action["name"]
        )

        # Add the correct rule and test that no exception is raised
        my_meta_rule = {
            "name": "my_meta_rule",
            "algorithm": "test",
            "subject_categories": [my_subject_category["id"], ],
            "action_categories": [my_action_category["id"], ],
            "object_categories": [my_object_category["id"], ]
        }
        sub_meta_rules_dict = self.authz_manager.get_sub_meta_rules_dict(
            admin_subject_id,
            authz_ie_dict["id"]
        )

        self.assertRaises(
            SubMetaRuleAlgorithmNotExisting,
            self.admin_manager.add_sub_meta_rule_dict,
            admin_subject_id,
            authz_ie_dict["id"],
            my_meta_rule
        )

        # TODO: the next request should be called with demo_subject_id
        # but the demo user has no right in the root intra_extension
        # algorithms = self.configuration_api.get_sub_meta_rule_algorithms_dict(admin_subject_id)
        # for algorithm_id in algorithms:
        #     if algorithms[algorithm_id]["name"] == "inclusion":
        #         my_meta_rule["algorithm"] = algorithm_id
        my_meta_rule['algorithm'] = 'inclusion'

        sub_meta_rule = self.admin_manager.add_sub_meta_rule_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            my_meta_rule
        )
        sub_meta_rule_id, sub_meta_rule_dict = None, None
        for key, value in sub_meta_rule.iteritems():
            if value["name"] == my_meta_rule["name"]:
                sub_meta_rule_id, sub_meta_rule_dict = key, value
                break

        aggregation_algorithms = self.configuration_api.get_aggregation_algorithms_dict(admin_subject_id)
        for _id in aggregation_algorithms:
            if aggregation_algorithms[_id]["name"] == "one_true":
                agg = self.admin_manager.set_aggregation_algorithm_id(admin_subject_id, authz_ie_dict["id"], _id)

        rule = self.admin_manager.add_rule_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            sub_meta_rule_id,
            [my_subject_scope["id"], my_action_scope["id"], my_object_scope["id"], True]
        )

        self.assertRaises(
            AuthzException,
            self.authz_manager.authz,
            tenant["id"], admin_subject_dict["keystone_id"], my_object["name"], my_action["name"]
        )

        result = self.authz_manager.authz(tenant["id"], demo_subject_dict["keystone_id"], my_object["name"], my_action["name"])
        self.assertIsInstance(result, dict)
        self.assertIn('authz', result)
        self.assertEquals(result['authz'], True)

    def test_subjects(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        subjects = self.authz_manager.get_subjects_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(subjects, dict)
        for key, value in subjects.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)
            self.assertIn("keystone_name", value)
            self.assertIn("keystone_id", value)

        create_user(self, "subject_test")
        new_subject = {"name": "subject_test", "description": "subject_test"}
        self.assertRaises(
            AuthzException,
            self.admin_manager.add_subject_dict,
            demo_subject_id, admin_ie_dict["id"], new_subject)

        subjects = self.admin_manager.add_subject_dict(admin_subject_id, authz_ie_dict["id"], new_subject)
        _subjects = dict(subjects)
        self.assertEqual(len(_subjects.keys()), 1)
        new_subject["id"] = _subjects.keys()[0]
        value = subjects[new_subject["id"]]
        self.assertIsInstance(value, dict)
        self.assertIn("name", value)
        self.assertEqual(value["name"], new_subject["name"])
        self.assertIn("description", value)
        self.assertEqual(value["description"], new_subject["description"])

        # Delete the new subject
        self.assertRaises(
            AuthzException,
            self.authz_manager.del_subject,
            demo_subject_id, authz_ie_dict["id"], new_subject["id"])

        self.admin_manager.del_subject(admin_subject_id, authz_ie_dict["id"], new_subject["id"])
        subjects = self.authz_manager.get_subjects_dict(admin_subject_id, authz_ie_dict["id"])
        for key, value in subjects.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIsNot(new_subject["name"], value["name"])
            self.assertIn("description", value)

    def test_objects(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        objects = self.authz_manager.get_objects_dict(admin_subject_id, authz_ie_dict["id"])
        objects_id_list = []
        self.assertIsInstance(objects, dict)
        for key, value in objects.iteritems():
            objects_id_list.append(key)
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

        # create_user(self, "subject_test")
        new_object = {"name": "object_test", "description": "object_test"}
        self.assertRaises(
            AuthzException,
            self.authz_manager.add_object_dict,
            demo_subject_id, admin_ie_dict["id"], new_object)

        self.assertRaises(
            ObjectsWriteNoAuthorized,
            self.admin_manager.add_object_dict,
            admin_subject_id, admin_ie_dict["id"], new_object
        )

        # Delete the new object
        for key in objects_id_list:
            self.assertRaises(
                AuthzException,
                self.authz_manager.del_object,
                demo_subject_id, authz_ie_dict["id"], key)
            self.assertRaises(
                AuthzException,
                self.authz_manager.del_object,
                admin_subject_id, authz_ie_dict["id"], key)

        for key in objects_id_list:
            self.assertRaises(
                ObjectsWriteNoAuthorized,
                self.admin_manager.del_object,
                demo_subject_id, admin_ie_dict["id"], key)
            self.assertRaises(
                ObjectsWriteNoAuthorized,
                self.admin_manager.del_object,
                admin_subject_id, admin_ie_dict["id"], key)

    def test_actions(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        actions = self.authz_manager.get_actions_dict(admin_subject_id, authz_ie_dict["id"])
        actions_id_list = []
        self.assertIsInstance(actions, dict)
        for key, value in actions.iteritems():
            actions_id_list.append(key)
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

        create_user(self, "subject_test")
        new_action = {"name": "action_test", "description": "action_test"}
        self.assertRaises(
            AuthzException,
            self.authz_manager.add_action_dict,
            demo_subject_id, admin_ie_dict["id"], new_action)

        self.assertRaises(
            ActionsWriteNoAuthorized,
            self.admin_manager.add_action_dict,
            admin_subject_id, admin_ie_dict["id"], new_action
        )

        # Delete all actions
        for key in actions_id_list:
            self.assertRaises(
                AuthzException,
                self.authz_manager.del_action,
                demo_subject_id, authz_ie_dict["id"], key)
            self.assertRaises(
                AuthzException,
                self.authz_manager.del_action,
                admin_subject_id, authz_ie_dict["id"], key)

        for key in actions_id_list:
            self.assertRaises(
                ActionsWriteNoAuthorized,
                self.admin_manager.del_action,
                demo_subject_id, admin_ie_dict["id"], key)
            self.assertRaises(
                ActionsWriteNoAuthorized,
                self.admin_manager.del_action,
                admin_subject_id, admin_ie_dict["id"], key)

    def test_subject_categories(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        subject_categories = self.authz_manager.get_subject_categories_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(subject_categories, dict)
        for key, value in subject_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

        new_subject_category = {"name": "subject_category_test", "description": "subject_category_test"}
        self.assertRaises(
            AuthzException,
            self.authz_manager.add_subject_category_dict,
            demo_subject_id, admin_ie_dict["id"], new_subject_category)

        subject_categories = self.admin_manager.add_subject_category_dict(admin_subject_id, authz_ie_dict["id"], new_subject_category)
        _subject_categories = dict(subject_categories)
        self.assertEqual(len(_subject_categories.keys()), 1)
        new_subject_category["id"] = _subject_categories.keys()[0]
        value = subject_categories[new_subject_category["id"]]
        self.assertIsInstance(value, dict)
        self.assertIn("name", value)
        self.assertEqual(value["name"], new_subject_category["name"])
        self.assertIn("description", value)
        self.assertEqual(value["description"], new_subject_category["description"])

        # Delete the new subject_category
        self.assertRaises(
            AuthzException,
            self.authz_manager.del_subject_category,
            demo_subject_id, authz_ie_dict["id"], new_subject_category["id"])

        self.admin_manager.del_subject_category(admin_subject_id, authz_ie_dict["id"], new_subject_category["id"])
        subject_categories = self.authz_manager.get_subject_categories_dict(admin_subject_id, authz_ie_dict["id"])
        for key, value in subject_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIsNot(new_subject_category["name"], value["name"])
            self.assertIn("description", value)

    def test_object_categories(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        object_categories = self.authz_manager.get_object_categories_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(object_categories, dict)
        for key, value in object_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

        new_object_category = {"name": "object_category_test", "description": "object_category_test"}
        self.assertRaises(
            AuthzException,
            self.authz_manager.add_object_category_dict,
            demo_subject_id, admin_ie_dict["id"], new_object_category)

        object_categories = self.admin_manager.add_object_category_dict(admin_subject_id, authz_ie_dict["id"], new_object_category)
        _object_categories = dict(object_categories)
        self.assertEqual(len(_object_categories.keys()), 1)
        new_object_category["id"] = _object_categories.keys()[0]
        value = object_categories[new_object_category["id"]]
        self.assertIsInstance(value, dict)
        self.assertIn("name", value)
        self.assertEqual(value["name"], new_object_category["name"])
        self.assertIn("description", value)
        self.assertEqual(value["description"], new_object_category["description"])

        # Delete the new object_category
        self.assertRaises(
            AuthzException,
            self.authz_manager.del_object_category,
            demo_subject_id, authz_ie_dict["id"], new_object_category["id"])

        self.admin_manager.del_object_category(admin_subject_id, authz_ie_dict["id"], new_object_category["id"])
        object_categories = self.authz_manager.get_object_categories_dict(admin_subject_id, authz_ie_dict["id"])
        for key, value in object_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIsNot(new_object_category["name"], value["name"])
            self.assertIn("description", value)

    def test_action_categories(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        action_categories = self.authz_manager.get_action_categories_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(action_categories, dict)
        for key, value in action_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("description", value)

        new_action_category = {"name": "action_category_test", "description": "action_category_test"}
        self.assertRaises(
            AuthzException,
            self.authz_manager.add_action_category_dict,
            demo_subject_id, admin_ie_dict["id"], new_action_category)

        action_categories = self.admin_manager.add_action_category_dict(admin_subject_id, authz_ie_dict["id"], new_action_category)
        _action_categories = dict(action_categories)
        self.assertEqual(len(_action_categories.keys()), 1)
        new_action_category["id"] = _action_categories.keys()[0]
        value = action_categories[new_action_category["id"]]
        self.assertIsInstance(value, dict)
        self.assertIn("name", value)
        self.assertEqual(value["name"], new_action_category["name"])
        self.assertIn("description", value)
        self.assertEqual(value["description"], new_action_category["description"])

        # Delete the new action_category
        self.assertRaises(
            AuthzException,
            self.authz_manager.del_action_category,
            demo_subject_id, authz_ie_dict["id"], new_action_category["id"])

        self.admin_manager.del_action_category(admin_subject_id, authz_ie_dict["id"], new_action_category["id"])
        action_categories = self.authz_manager.get_action_categories_dict(admin_subject_id, authz_ie_dict["id"])
        for key, value in action_categories.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIsNot(new_action_category["name"], value["name"])
            self.assertIn("description", value)

    def test_subject_category_scope(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        subject_categories = self.admin_manager.add_subject_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "country",
                "description": "country",
            }
        )

        for subject_category_id in subject_categories:

            subject_category_scope = self.authz_manager.get_subject_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertEqual({}, subject_category_scope)

            new_subject_category_scope = {
                "name": "france",
                "description": "france",
            }

            self.assertRaises(
                AuthzException,
                self.admin_manager.add_subject_scope_dict,
                demo_subject_id, authz_ie_dict["id"], subject_category_id, new_subject_category_scope)

            subject_category_scope = self.admin_manager.add_subject_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id,
                new_subject_category_scope)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertEqual(len(subject_category_scope.keys()), 1)
            subject_category_scope_id = subject_category_scope.keys()[0]
            subject_category_scope_value = subject_category_scope[subject_category_scope_id]
            self.assertIn("name", subject_category_scope_value)
            self.assertEqual(new_subject_category_scope["name"], subject_category_scope_value["name"])
            self.assertIn("description", subject_category_scope_value)
            self.assertEqual(new_subject_category_scope["description"], subject_category_scope_value["description"])

            # Delete the new subject_category_scope
            self.assertRaises(
                AuthzException,
                self.admin_manager.del_subject_scope,
                demo_subject_id, authz_ie_dict["id"], subject_category_id, subject_category_scope_id)

            self.admin_manager.del_subject_scope(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id,
                subject_category_scope_id)
            subject_category_scope = self.admin_manager.get_subject_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertNotIn(subject_category_scope_id, subject_category_scope.keys())

    def test_object_category_scope(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        object_categories = self.admin_manager.add_object_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "country",
                "description": "country",
            }
        )

        for object_category_id in object_categories:

            object_category_scope = self.authz_manager.get_object_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id)
            self.assertIsInstance(object_category_scope, dict)
            self.assertEqual({}, object_category_scope)

            new_object_category_scope = {
                "name": "france",
                "description": "france",
            }

            self.assertRaises(
                AuthzException,
                self.admin_manager.add_object_scope_dict,
                demo_subject_id, authz_ie_dict["id"], object_category_id, new_object_category_scope)

            object_category_scope = self.admin_manager.add_object_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id,
                new_object_category_scope)
            self.assertIsInstance(object_category_scope, dict)
            self.assertEqual(len(object_category_scope.keys()), 1)
            object_category_scope_id = object_category_scope.keys()[0]
            object_category_scope_value = object_category_scope[object_category_scope_id]
            self.assertIn("name", object_category_scope_value)
            self.assertEqual(new_object_category_scope["name"], object_category_scope_value["name"])
            self.assertIn("description", object_category_scope_value)
            self.assertEqual(new_object_category_scope["description"], object_category_scope_value["description"])

            # Delete the new object_category_scope
            self.assertRaises(
                AuthzException,
                self.admin_manager.del_object_scope,
                demo_subject_id, authz_ie_dict["id"], object_category_id, object_category_scope_id)

            self.admin_manager.del_object_scope(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id,
                object_category_scope_id)
            object_category_scope = self.admin_manager.get_object_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id)
            self.assertIsInstance(object_category_scope, dict)
            self.assertNotIn(object_category_scope_id, object_category_scope.keys())

    def test_action_category_scope(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        action_categories = self.admin_manager.add_action_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "swift",
                "description": "swift actions",
            }
        )

        for action_category_id in action_categories:

            action_category_scope = self.authz_manager.get_action_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id)
            self.assertIsInstance(action_category_scope, dict)
            self.assertEqual({}, action_category_scope)

            new_action_category_scope = {
                "name": "get",
                "description": "get swift files",
            }

            self.assertRaises(
                AuthzException,
                self.admin_manager.add_action_scope_dict,
                demo_subject_id, authz_ie_dict["id"], action_category_id, new_action_category_scope)

            action_category_scope = self.admin_manager.add_action_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id,
                new_action_category_scope)
            self.assertIsInstance(action_category_scope, dict)
            self.assertEqual(len(action_category_scope.keys()), 1)
            action_category_scope_id = action_category_scope.keys()[0]
            action_category_scope_value = action_category_scope[action_category_scope_id]
            self.assertIn("name", action_category_scope_value)
            self.assertEqual(new_action_category_scope["name"], action_category_scope_value["name"])
            self.assertIn("description", action_category_scope_value)
            self.assertEqual(new_action_category_scope["description"], action_category_scope_value["description"])

            # Delete the new action_category_scope
            self.assertRaises(
                AuthzException,
                self.admin_manager.del_action_scope,
                demo_subject_id, authz_ie_dict["id"], action_category_id, action_category_scope_id)

            self.admin_manager.del_action_scope(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id,
                action_category_scope_id)
            action_category_scope = self.admin_manager.get_action_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id)
            self.assertIsInstance(action_category_scope, dict)
            self.assertNotIn(action_category_scope_id, action_category_scope.keys())

    def test_subject_category_assignment(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        admin_authz_subject_id, admin_authz_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], authz_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()
        demo_authz_subject_id, demo_authz_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], authz_ie_dict['id'], 'demo').iteritems().next()

        subjects_dict = self.authz_manager.get_subjects_dict(admin_subject_id, authz_ie_dict["id"])

        subject_categories = self.admin_manager.add_subject_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "country",
                "description": "country",
            }
        )

        for subject_category_id in subject_categories:
            subject_category_scope = self.authz_manager.get_subject_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertEqual({}, subject_category_scope)

            new_subject_category_scope_1 = {
                "name": "france",
                "description": "france",
            }

            subject_category_scope_1 = self.admin_manager.add_subject_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id,
                new_subject_category_scope_1)
            subject_category_scope_1_id = subject_category_scope_1.keys()[0]

            new_subject_category_scope_2 = {
                "name": "china",
                "description": "china",
            }

            subject_category_scope_2 = self.admin_manager.add_subject_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                subject_category_id,
                new_subject_category_scope_2)
            subject_category_scope_2_id = subject_category_scope_2.keys()[0]

            subject_category_assignments = self.authz_manager.get_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id,
                subject_category_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual([], subject_category_assignments)

            subject_category_assignments = self.authz_manager.get_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                demo_authz_subject_id,
                subject_category_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual([], subject_category_assignments)

            self.assertRaises(
                AuthzException,
                self.authz_manager.add_subject_assignment_list,
                demo_subject_id, authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id, subject_category_scope_1_id
            )

            self.assertRaises(
                AuthzException,
                self.authz_manager.add_subject_assignment_list,
                demo_subject_id, authz_ie_dict["id"],
                demo_authz_subject_id, subject_category_id, subject_category_scope_2_id
            )

            subject_category_assignments = self.admin_manager.add_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id, subject_category_scope_1_id
            )
            self.assertIsInstance(subject_category_assignments, list)

            self.assertEqual(len(subject_category_assignments), 1)

            subject_category_assignments = self.admin_manager.add_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id, subject_category_scope_2_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual(len(subject_category_assignments), 2)

            subject_category_assignments = self.admin_manager.add_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                demo_authz_subject_id, subject_category_id, subject_category_scope_2_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual(len(subject_category_assignments), 1)

            subject_category_assignments = self.admin_manager.get_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual(len(subject_category_assignments), 2)

            self.assertRaises(
                AuthzException,
                self.admin_manager.del_subject_assignment,
                demo_subject_id, authz_ie_dict["id"],
                demo_authz_subject_id, subject_category_id, subject_category_scope_2_id
            )

            self.admin_manager.del_subject_assignment(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id, subject_category_scope_2_id
            )
            subject_category_assignments = self.admin_manager.get_subject_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id
            )
            self.assertIsInstance(subject_category_assignments, list)
            self.assertEqual(len(subject_category_assignments), 1)

            self.assertRaises(
                SubjectAssignmentUnknown,
                self.admin_manager.del_subject_assignment,
                admin_subject_id,
                authz_ie_dict["id"],
                admin_authz_subject_id, subject_category_id, subject_category_scope_2_id
            )

    def test_object_category_assignment(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        objects_dict = self.authz_manager.get_objects_dict(admin_subject_id, authz_ie_dict["id"])

        object_vm1 = self.admin_manager.add_object_dict(admin_subject_id, authz_ie_dict["id"], {"name": "vm1", "description": "vm1"})
        object_vm2 = self.admin_manager.add_object_dict(admin_subject_id, authz_ie_dict["id"], {"name": "vm2", "description": "vm2"})
        object_vm1_id = object_vm1.keys()[0]
        object_vm2_id = object_vm2.keys()[0]
        if not object_vm1_id or not object_vm2_id:
            raise Exception("Cannot run tests, database is corrupted ? (need upload and list in objects)")

        object_categories = self.admin_manager.add_object_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "location",
                "description": "location",
            }
        )

        for object_category_id in object_categories:
            object_category_scope = self.authz_manager.get_object_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id)
            self.assertIsInstance(object_category_scope, dict)
            self.assertEqual({}, object_category_scope)

            new_object_category_scope_1 = {
                "name": "france",
                "description": "france",
            }

            object_category_scope_1 = self.admin_manager.add_object_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id,
                new_object_category_scope_1)
            object_category_scope_1_id = object_category_scope_1.keys()[0]

            new_object_category_scope_2 = {
                "name": "china",
                "description": "china",
            }

            object_category_scope_2 = self.admin_manager.add_object_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                object_category_id,
                new_object_category_scope_2)
            object_category_scope_2_id = object_category_scope_2.keys()[0]

            object_category_assignments = self.authz_manager.get_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id,
                object_category_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual([], object_category_assignments)

            object_category_assignments = self.authz_manager.get_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm2_id,
                object_category_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual([], object_category_assignments)

            self.assertRaises(
                AuthzException,
                self.authz_manager.add_object_assignment_list,
                demo_subject_id, authz_ie_dict["id"],
                object_vm1_id, object_category_id, object_category_scope_1_id
            )

            self.assertRaises(
                AuthzException,
                self.authz_manager.add_object_assignment_list,
                demo_subject_id, authz_ie_dict["id"],
                object_vm2_id, object_category_id, object_category_scope_2_id
            )

            object_category_assignments = self.admin_manager.add_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id, object_category_scope_1_id
            )
            self.assertIsInstance(object_category_assignments, list)

            self.assertEqual(len(object_category_assignments), 1)

            object_category_assignments = self.admin_manager.add_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id, object_category_scope_2_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual(len(object_category_assignments), 2)

            object_category_assignments = self.admin_manager.add_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm2_id, object_category_id, object_category_scope_2_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual(len(object_category_assignments), 1)

            object_category_assignments = self.admin_manager.get_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual(len(object_category_assignments), 2)

            self.assertRaises(
                AuthzException,
                self.admin_manager.del_object_assignment,
                demo_subject_id, authz_ie_dict["id"],
                object_vm2_id, object_category_id, object_category_scope_2_id
            )

            self.admin_manager.del_object_assignment(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id, object_category_scope_2_id
            )
            object_category_assignments = self.admin_manager.get_object_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id
            )
            self.assertIsInstance(object_category_assignments, list)
            self.assertEqual(len(object_category_assignments), 1)

            self.assertRaises(
                ObjectAssignmentUnknown,
                self.admin_manager.del_object_assignment,
                admin_subject_id,
                authz_ie_dict["id"],
                object_vm1_id, object_category_id, object_category_scope_2_id
            )

    def test_action_category_assignment(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        actions_dict = self.authz_manager.get_actions_dict(admin_subject_id, authz_ie_dict["id"])

        action_upload_id = None
        action_list_id = None
        for _action_id in actions_dict:
            if actions_dict[_action_id]['name'] == 'upload':
                action_upload_id = _action_id
            if actions_dict[_action_id]['name'] == 'list':
                action_list_id = _action_id
        if not action_upload_id or not action_list_id:
            raise Exception("Cannot run tests, database is corrupted ? (need upload and list in actions)")

        action_categories = self.admin_manager.add_action_category_dict(
            admin_subject_id,
            authz_ie_dict["id"],
            {
                "name": "swift",
                "description": "swift actions",
            }
        )

        for action_category_id in action_categories:
            action_category_scope = self.authz_manager.get_action_scopes_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id)
            self.assertIsInstance(action_category_scope, dict)
            self.assertEqual({}, action_category_scope)

            new_action_category_scope_1 = {
                "name": "swift_admin",
                "description": "action require admin rights",
            }

            action_category_scope_1 = self.admin_manager.add_action_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id,
                new_action_category_scope_1)
            action_category_scope_1_id = action_category_scope_1.keys()[0]

            new_action_category_scope_2 = {
                "name": "swift_anonymous",
                "description": "action require no right",
            }

            action_category_scope_2 = self.admin_manager.add_action_scope_dict(
                admin_subject_id,
                authz_ie_dict["id"],
                action_category_id,
                new_action_category_scope_2)
            action_category_scope_2_id = action_category_scope_2.keys()[0]

            action_category_assignments = self.authz_manager.get_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id,
                action_category_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual([], action_category_assignments)

            action_category_assignments = self.authz_manager.get_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_list_id,
                action_category_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual([], action_category_assignments)

            self.assertRaises(
                AuthzException,
                self.authz_manager.add_action_assignment_list,
                demo_subject_id, authz_ie_dict["id"],
                action_upload_id, action_category_id, action_category_scope_1_id
            )

            self.assertRaises(
                AuthzException,
                self.authz_manager.add_action_assignment_list,
                demo_subject_id, authz_ie_dict["id"],
                action_list_id, action_category_id, action_category_scope_2_id
            )

            action_category_assignments = self.admin_manager.add_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id, action_category_scope_1_id
            )
            self.assertIsInstance(action_category_assignments, list)

            self.assertEqual(len(action_category_assignments), 1)

            action_category_assignments = self.admin_manager.add_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id, action_category_scope_2_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual(len(action_category_assignments), 2)

            action_category_assignments = self.admin_manager.add_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_list_id, action_category_id, action_category_scope_2_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual(len(action_category_assignments), 1)

            action_category_assignments = self.admin_manager.get_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual(len(action_category_assignments), 2)

            self.assertRaises(
                AuthzException,
                self.admin_manager.del_action_assignment,
                demo_subject_id, authz_ie_dict["id"],
                action_list_id, action_category_id, action_category_scope_2_id
            )

            self.admin_manager.del_action_assignment(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id, action_category_scope_2_id
            )
            action_category_assignments = self.admin_manager.get_action_assignment_list(
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id
            )
            self.assertIsInstance(action_category_assignments, list)
            self.assertEqual(len(action_category_assignments), 1)

            self.assertRaises(
                ActionAssignmentUnknown,
                self.admin_manager.del_action_assignment,
                admin_subject_id,
                authz_ie_dict["id"],
                action_upload_id, action_category_id, action_category_scope_2_id
            )

    def test_sub_meta_rules(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        aggregation_algorithm = self.admin_manager.get_aggregation_algorithm_id(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(aggregation_algorithm, dict)

        # TODO: need more tests on aggregation_algorithms (set and del)

        sub_meta_rules = self.admin_manager.get_sub_meta_rules_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(sub_meta_rules, dict)
        categories = {
            "subject_categories": self.admin_manager.get_subject_categories_dict(admin_subject_id, authz_ie_dict["id"]),
            "object_categories": self.admin_manager.get_object_categories_dict(admin_subject_id, authz_ie_dict["id"]),
            "action_categories": self.admin_manager.get_action_categories_dict(admin_subject_id, authz_ie_dict["id"])
        }
        for key, value in sub_meta_rules.iteritems():
            self.assertIsInstance(value, dict)
            self.assertIn("action_categories", value)
            self.assertIn("object_categories", value)
            self.assertIn("subject_categories", value)
            self.assertIn("algorithm", value)
            self.assertIn("name", value)
            for action_category_id in value["action_categories"]:
                self.assertIn(action_category_id, categories["action_categories"])
            for object_category_id in value["object_categories"]:
                self.assertIn(object_category_id, categories["object_categories"])
            for subject_category_id in value["subject_categories"]:
                self.assertIn(subject_category_id, categories["subject_categories"])
                # TODO: need more tests (set and del)

    def test_sub_rules(self):
        authz_ie_dict = create_intra_extension(self, "policy_authz")
        admin_ie_dict = create_intra_extension(self, "policy_rbac_admin")
        tenant, mapping = create_mapping(self, "demo", authz_ie_dict['id'], admin_ie_dict['id'])

        admin_subject_id, admin_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'admin').iteritems().next()
        demo_subject_id, demo_subject_dict = \
            self.admin_api.get_subject_dict_from_keystone_name(tenant['id'], admin_ie_dict['id'], 'demo').iteritems().next()

        sub_meta_rules = self.admin_manager.get_sub_meta_rules_dict(admin_subject_id, authz_ie_dict["id"])
        self.assertIsInstance(sub_meta_rules, dict)

        for relation_id in sub_meta_rules:
            rules = self.admin_manager.get_rules_dict(admin_subject_id, authz_ie_dict["id"], relation_id)
            rule_length = len(sub_meta_rules[relation_id]["subject_categories"]) + \
                          len(sub_meta_rules[relation_id]["object_categories"]) + \
                          len(sub_meta_rules[relation_id]["action_categories"]) + 1
            for rule_id in rules:
                self.assertEqual(rule_length, len(rules[rule_id]))
                rule = list(rules[rule_id])
                for cat, cat_func, func_name in (
                        ("subject_categories", self.admin_manager.get_subject_scopes_dict, "subject_scope"),
                        ("action_categories", self.admin_manager.get_action_scopes_dict, "action_scope"),
                        ("object_categories", self.admin_manager.get_object_scopes_dict, "object_scope"),
                ):
                    for cat_value in sub_meta_rules[relation_id][cat]:
                        scope = cat_func(
                            admin_subject_id,
                            authz_ie_dict["id"],
                            cat_value
                        )
                        a_scope = rule.pop(0)
                        if type(a_scope) is not bool:
                            self.assertIn(a_scope, scope.keys())

            # add a new subrule

            sub_rule = []
            for cat, cat_func, func_name in (
                    ("subject_categories", self.admin_manager.get_subject_scopes_dict, "subject_scope"),
                    ("action_categories", self.admin_manager.get_action_scopes_dict, "action_scope"),
                    ("object_categories", self.admin_manager.get_object_scopes_dict, "object_scope"),
            ):
                for cat_value in sub_meta_rules[relation_id][cat]:
                    scope = cat_func(
                        admin_subject_id,
                        authz_ie_dict["id"],
                        cat_value
                    )
                    sub_rule.append(scope.keys()[0])

            sub_rule.append(False)
            self.assertRaises(
                AuthzException,
                self.admin_manager.add_rule_dict,
                demo_subject_id, authz_ie_dict["id"], relation_id, sub_rule
            )

            sub_rules = self.admin_manager.add_rule_dict(admin_subject_id, authz_ie_dict["id"], relation_id, sub_rule)
            self.assertIsInstance(sub_rules, dict)
            self.assertIn(sub_rule, sub_rules.values())

            for rule_id, rule_value in sub_rules.iteritems():
                for cat, cat_func, func_name in (
                        ("subject_categories", self.admin_manager.get_subject_scopes_dict, "subject_category_scope"),
                        ("action_categories", self.admin_manager.get_action_scopes_dict, "action_category_scope"),
                        ("object_categories", self.admin_manager.get_object_scopes_dict, "object_category_scope"),
                ):
                    for cat_value in sub_meta_rules[relation_id][cat]:
                        scope = cat_func(
                            admin_subject_id,
                            authz_ie_dict["id"],
                            cat_value
                        )
                        a_scope = rule_value.pop(0)
                        self.assertIn(a_scope, scope.keys())

                        # TODO: add test for the delete function
