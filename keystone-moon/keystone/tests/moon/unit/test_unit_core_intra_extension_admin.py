# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Unit tests for core IntraExtensionAdminManager"""

import json
import os
import uuid
from oslo_config import cfg
from keystone.tests import unit as tests
from keystone.contrib.moon.core import IntraExtensionAdminManager, IntraExtensionAuthzManager
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
        self.policy_directory = '../../../examples/moon/policies'
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

    def test_subjects(self):
        self.create_intra_extension()
        
        subjects = self.manager.get_subject_dict("admin", self.ref["id"])
        self.assertIsInstance(subjects, dict)
        self.assertIn("subjects", subjects)
        self.assertIn("id", subjects)
        self.assertIn("intra_extension_uuid", subjects)
        self.assertEqual(self.ref["id"], subjects["intra_extension_uuid"])
        self.assertIsInstance(subjects["subjects"], dict)

        new_subject = self.create_user()
        new_subjects = dict()
        new_subjects[new_subject["id"]] = new_subject["name"]
        subjects = self.manager.set_subject_dict("admin", self.ref["id"], new_subjects)
        self.assertIsInstance(subjects, dict)
        self.assertIn("subjects", subjects)
        self.assertIn("id", subjects)
        self.assertIn("intra_extension_uuid", subjects)
        self.assertEqual(self.ref["id"], subjects["intra_extension_uuid"])
        self.assertEqual(subjects["subjects"], new_subjects)
        self.assertIn(new_subject["id"], subjects["subjects"])
        
        # Delete the new subject
        self.manager.del_subject("admin", self.ref["id"], new_subject["id"])
        subjects = self.manager.get_subject_dict("admin", self.ref["id"])
        self.assertIsInstance(subjects, dict)
        self.assertIn("subjects", subjects)
        self.assertIn("id", subjects)
        self.assertIn("intra_extension_uuid", subjects)
        self.assertEqual(self.ref["id"], subjects["intra_extension_uuid"])
        self.assertNotIn(new_subject["id"], subjects["subjects"])
        
        # Add a particular subject
        subjects = self.manager.add_subject_dict("admin", self.ref["id"], new_subject["id"])
        self.assertIsInstance(subjects, dict)
        self.assertIn("subject", subjects)
        self.assertIn("uuid", subjects["subject"])
        self.assertEqual(new_subject["name"], subjects["subject"]["name"])
        subjects = self.manager.get_subject_dict("admin", self.ref["id"])
        self.assertIsInstance(subjects, dict)
        self.assertIn("subjects", subjects)
        self.assertIn("id", subjects)
        self.assertIn("intra_extension_uuid", subjects)
        self.assertEqual(self.ref["id"], subjects["intra_extension_uuid"])
        self.assertIn(new_subject["id"], subjects["subjects"])

    def test_objects(self):
        self.create_intra_extension()
        
        objects = self.manager.get_object_dict("admin", self.ref["id"])
        self.assertIsInstance(objects, dict)
        self.assertIn("objects", objects)
        self.assertIn("id", objects)
        self.assertIn("intra_extension_uuid", objects)
        self.assertEqual(self.ref["id"], objects["intra_extension_uuid"])
        self.assertIsInstance(objects["objects"], dict)

        new_object = self.create_user()
        new_objects = dict()
        new_objects[new_object["id"]] = new_object["name"]
        objects = self.manager.set_object_dict("admin", self.ref["id"], new_objects)
        self.assertIsInstance(objects, dict)
        self.assertIn("objects", objects)
        self.assertIn("id", objects)
        self.assertIn("intra_extension_uuid", objects)
        self.assertEqual(self.ref["id"], objects["intra_extension_uuid"])
        self.assertEqual(objects["objects"], new_objects)
        self.assertIn(new_object["id"], objects["objects"])
        
        # Delete the new object
        self.manager.del_object("admin", self.ref["id"], new_object["id"])
        objects = self.manager.get_object_dict("admin", self.ref["id"])
        self.assertIsInstance(objects, dict)
        self.assertIn("objects", objects)
        self.assertIn("id", objects)
        self.assertIn("intra_extension_uuid", objects)
        self.assertEqual(self.ref["id"], objects["intra_extension_uuid"])
        self.assertNotIn(new_object["id"], objects["objects"])
        
        # Add a particular object
        objects = self.manager.add_object_dict("admin", self.ref["id"], new_object["name"])
        self.assertIsInstance(objects, dict)
        self.assertIn("object", objects)
        self.assertIn("uuid", objects["object"])
        self.assertEqual(new_object["name"], objects["object"]["name"])
        new_object["id"] = objects["object"]["uuid"]
        objects = self.manager.get_object_dict("admin", self.ref["id"])
        self.assertIsInstance(objects, dict)
        self.assertIn("objects", objects)
        self.assertIn("id", objects)
        self.assertIn("intra_extension_uuid", objects)
        self.assertEqual(self.ref["id"], objects["intra_extension_uuid"])
        self.assertIn(new_object["id"], objects["objects"])

    def test_actions(self):
        self.create_intra_extension()

        actions = self.manager.get_action_dict("admin", self.ref["id"])
        self.assertIsInstance(actions, dict)
        self.assertIn("actions", actions)
        self.assertIn("id", actions)
        self.assertIn("intra_extension_uuid", actions)
        self.assertEqual(self.ref["id"], actions["intra_extension_uuid"])
        self.assertIsInstance(actions["actions"], dict)

        new_action = self.create_user()
        new_actions = dict()
        new_actions[new_action["id"]] = new_action["name"]
        actions = self.manager.set_action_dict("admin", self.ref["id"], new_actions)
        self.assertIsInstance(actions, dict)
        self.assertIn("actions", actions)
        self.assertIn("id", actions)
        self.assertIn("intra_extension_uuid", actions)
        self.assertEqual(self.ref["id"], actions["intra_extension_uuid"])
        self.assertEqual(actions["actions"], new_actions)
        self.assertIn(new_action["id"], actions["actions"])

        # Delete the new action
        self.manager.del_action("admin", self.ref["id"], new_action["id"])
        actions = self.manager.get_action_dict("admin", self.ref["id"])
        self.assertIsInstance(actions, dict)
        self.assertIn("actions", actions)
        self.assertIn("id", actions)
        self.assertIn("intra_extension_uuid", actions)
        self.assertEqual(self.ref["id"], actions["intra_extension_uuid"])
        self.assertNotIn(new_action["id"], actions["actions"])

        # Add a particular action
        actions = self.manager.add_action_dict("admin", self.ref["id"], new_action["name"])
        self.assertIsInstance(actions, dict)
        self.assertIn("action", actions)
        self.assertIn("uuid", actions["action"])
        self.assertEqual(new_action["name"], actions["action"]["name"])
        new_action["id"] = actions["action"]["uuid"]
        actions = self.manager.get_action_dict("admin", self.ref["id"])
        self.assertIsInstance(actions, dict)
        self.assertIn("actions", actions)
        self.assertIn("id", actions)
        self.assertIn("intra_extension_uuid", actions)
        self.assertEqual(self.ref["id"], actions["intra_extension_uuid"])
        self.assertIn(new_action["id"], actions["actions"])

    def test_subject_categories(self):
        self.create_intra_extension()

        subject_categories = self.manager.get_subject_category_dict("admin", self.ref["id"])
        self.assertIsInstance(subject_categories, dict)
        self.assertIn("subject_categories", subject_categories)
        self.assertIn("id", subject_categories)
        self.assertIn("intra_extension_uuid", subject_categories)
        self.assertEqual(self.ref["id"], subject_categories["intra_extension_uuid"])
        self.assertIsInstance(subject_categories["subject_categories"], dict)

        new_subject_category = {"id": uuid.uuid4().hex, "name": "subject_category_test"}
        new_subject_categories = dict()
        new_subject_categories[new_subject_category["id"]] = new_subject_category["name"]
        subject_categories = self.manager.set_subject_category_dict("admin", self.ref["id"], new_subject_categories)
        self.assertIsInstance(subject_categories, dict)
        self.assertIn("subject_categories", subject_categories)
        self.assertIn("id", subject_categories)
        self.assertIn("intra_extension_uuid", subject_categories)
        self.assertEqual(self.ref["id"], subject_categories["intra_extension_uuid"])
        self.assertEqual(subject_categories["subject_categories"], new_subject_categories)
        self.assertIn(new_subject_category["id"], subject_categories["subject_categories"])

        # Delete the new subject_category
        self.manager.del_subject_category("admin", self.ref["id"], new_subject_category["id"])
        subject_categories = self.manager.get_subject_category_dict("admin", self.ref["id"])
        self.assertIsInstance(subject_categories, dict)
        self.assertIn("subject_categories", subject_categories)
        self.assertIn("id", subject_categories)
        self.assertIn("intra_extension_uuid", subject_categories)
        self.assertEqual(self.ref["id"], subject_categories["intra_extension_uuid"])
        self.assertNotIn(new_subject_category["id"], subject_categories["subject_categories"])

        # Add a particular subject_category
        subject_categories = self.manager.add_subject_category_dict(
            "admin",
            self.ref["id"],
            new_subject_category["name"])
        self.assertIsInstance(subject_categories, dict)
        self.assertIn("subject_category", subject_categories)
        self.assertIn("uuid", subject_categories["subject_category"])
        self.assertEqual(new_subject_category["name"], subject_categories["subject_category"]["name"])
        new_subject_category["id"] = subject_categories["subject_category"]["uuid"]
        subject_categories = self.manager.get_subject_category_dict(
            "admin",
            self.ref["id"])
        self.assertIsInstance(subject_categories, dict)
        self.assertIn("subject_categories", subject_categories)
        self.assertIn("id", subject_categories)
        self.assertIn("intra_extension_uuid", subject_categories)
        self.assertEqual(self.ref["id"], subject_categories["intra_extension_uuid"])
        self.assertIn(new_subject_category["id"], subject_categories["subject_categories"])

    def test_object_categories(self):
        self.create_intra_extension()

        object_categories = self.manager.get_object_category_dict("admin", self.ref["id"])
        self.assertIsInstance(object_categories, dict)
        self.assertIn("object_categories", object_categories)
        self.assertIn("id", object_categories)
        self.assertIn("intra_extension_uuid", object_categories)
        self.assertEqual(self.ref["id"], object_categories["intra_extension_uuid"])
        self.assertIsInstance(object_categories["object_categories"], dict)

        new_object_category = {"id": uuid.uuid4().hex, "name": "object_category_test"}
        new_object_categories = dict()
        new_object_categories[new_object_category["id"]] = new_object_category["name"]
        object_categories = self.manager.set_object_category_dict("admin", self.ref["id"], new_object_categories)
        self.assertIsInstance(object_categories, dict)
        self.assertIn("object_categories", object_categories)
        self.assertIn("id", object_categories)
        self.assertIn("intra_extension_uuid", object_categories)
        self.assertEqual(self.ref["id"], object_categories["intra_extension_uuid"])
        self.assertEqual(object_categories["object_categories"], new_object_categories)
        self.assertIn(new_object_category["id"], object_categories["object_categories"])

        # Delete the new object_category
        self.manager.del_object_category("admin", self.ref["id"], new_object_category["id"])
        object_categories = self.manager.get_object_category_dict("admin", self.ref["id"])
        self.assertIsInstance(object_categories, dict)
        self.assertIn("object_categories", object_categories)
        self.assertIn("id", object_categories)
        self.assertIn("intra_extension_uuid", object_categories)
        self.assertEqual(self.ref["id"], object_categories["intra_extension_uuid"])
        self.assertNotIn(new_object_category["id"], object_categories["object_categories"])

        # Add a particular object_category
        object_categories = self.manager.add_object_category_dict(
            "admin",
            self.ref["id"],
            new_object_category["name"])
        self.assertIsInstance(object_categories, dict)
        self.assertIn("object_category", object_categories)
        self.assertIn("uuid", object_categories["object_category"])
        self.assertEqual(new_object_category["name"], object_categories["object_category"]["name"])
        new_object_category["id"] = object_categories["object_category"]["uuid"]
        object_categories = self.manager.get_object_category_dict(
            "admin",
            self.ref["id"])
        self.assertIsInstance(object_categories, dict)
        self.assertIn("object_categories", object_categories)
        self.assertIn("id", object_categories)
        self.assertIn("intra_extension_uuid", object_categories)
        self.assertEqual(self.ref["id"], object_categories["intra_extension_uuid"])
        self.assertIn(new_object_category["id"], object_categories["object_categories"])

    def test_action_categories(self):
        self.create_intra_extension()

        action_categories = self.manager.get_action_category_dict("admin", self.ref["id"])
        self.assertIsInstance(action_categories, dict)
        self.assertIn("action_categories", action_categories)
        self.assertIn("id", action_categories)
        self.assertIn("intra_extension_uuid", action_categories)
        self.assertEqual(self.ref["id"], action_categories["intra_extension_uuid"])
        self.assertIsInstance(action_categories["action_categories"], dict)

        new_action_category = {"id": uuid.uuid4().hex, "name": "action_category_test"}
        new_action_categories = dict()
        new_action_categories[new_action_category["id"]] = new_action_category["name"]
        action_categories = self.manager.set_action_category_dict("admin", self.ref["id"], new_action_categories)
        self.assertIsInstance(action_categories, dict)
        self.assertIn("action_categories", action_categories)
        self.assertIn("id", action_categories)
        self.assertIn("intra_extension_uuid", action_categories)
        self.assertEqual(self.ref["id"], action_categories["intra_extension_uuid"])
        self.assertEqual(action_categories["action_categories"], new_action_categories)
        self.assertIn(new_action_category["id"], action_categories["action_categories"])

        # Delete the new action_category
        self.manager.del_action_category("admin", self.ref["id"], new_action_category["id"])
        action_categories = self.manager.get_action_category_dict("admin", self.ref["id"])
        self.assertIsInstance(action_categories, dict)
        self.assertIn("action_categories", action_categories)
        self.assertIn("id", action_categories)
        self.assertIn("intra_extension_uuid", action_categories)
        self.assertEqual(self.ref["id"], action_categories["intra_extension_uuid"])
        self.assertNotIn(new_action_category["id"], action_categories["action_categories"])

        # Add a particular action_category
        action_categories = self.manager.add_action_category_dict(
            "admin",
            self.ref["id"],
            new_action_category["name"])
        self.assertIsInstance(action_categories, dict)
        self.assertIn("action_category", action_categories)
        self.assertIn("uuid", action_categories["action_category"])
        self.assertEqual(new_action_category["name"], action_categories["action_category"]["name"])
        new_action_category["id"] = action_categories["action_category"]["uuid"]
        action_categories = self.manager.get_action_category_dict(
            "admin",
            self.ref["id"])
        self.assertIsInstance(action_categories, dict)
        self.assertIn("action_categories", action_categories)
        self.assertIn("id", action_categories)
        self.assertIn("intra_extension_uuid", action_categories)
        self.assertEqual(self.ref["id"], action_categories["intra_extension_uuid"])
        self.assertIn(new_action_category["id"], action_categories["action_categories"])

    def test_subject_category_scope(self):
        self.create_intra_extension()

        subject_categories = self.manager.set_subject_category_dict(
            "admin",
            self.ref["id"],
            {
                uuid.uuid4().hex: "admin",
                uuid.uuid4().hex: "dev",
            }
        )

        for subject_category in subject_categories["subject_categories"]:
            subject_category_scope = self.manager.get_subject_category_scope_dict(
                "admin",
                self.ref["id"],
                subject_category)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(self.ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertIsInstance(subject_category_scope["subject_category_scope"], dict)

            new_subject_category_scope = dict()
            new_subject_category_scope_uuid = uuid.uuid4().hex
            new_subject_category_scope[new_subject_category_scope_uuid] = "new_subject_category_scope"
            subject_category_scope = self.manager.set_subject_category_scope_dict(
                "admin",
                self.ref["id"],
                subject_category,
                new_subject_category_scope)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(self.ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertIn(new_subject_category_scope[new_subject_category_scope_uuid],
                          subject_category_scope["subject_category_scope"][subject_category].values())

            # Delete the new subject_category_scope
            self.manager.del_subject_category_scope(
                "admin",
                self.ref["id"],
                subject_category,
                new_subject_category_scope_uuid)
            subject_category_scope = self.manager.get_subject_category_scope_dict(
                "admin",
                self.ref["id"],
                subject_category)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(self.ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertNotIn(new_subject_category_scope_uuid, subject_category_scope["subject_category_scope"])

            # Add a particular subject_category_scope
            subject_category_scope = self.manager.add_subject_category_scope_dict(
                "admin",
                self.ref["id"],
                subject_category,
                new_subject_category_scope[new_subject_category_scope_uuid])
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("uuid", subject_category_scope["subject_category_scope"])
            self.assertEqual(new_subject_category_scope[new_subject_category_scope_uuid],
                             subject_category_scope["subject_category_scope"]["name"])
            subject_category_scope = self.manager.get_subject_category_scope_dict(
                "admin",
                self.ref["id"],
                subject_category)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(self.ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertNotIn(new_subject_category_scope_uuid, subject_category_scope["subject_category_scope"])

    def test_object_category_scope(self):
        self.create_intra_extension()

        object_categories = self.manager.set_object_category_dict(
            "admin",
            self.ref["id"],
            {
                uuid.uuid4().hex: "id",
                uuid.uuid4().hex: "domain",
            }
        )

        for object_category in object_categories["object_categories"]:
            object_category_scope = self.manager.get_object_category_scope_dict(
                "admin",
                self.ref["id"],
                object_category)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(self.ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertIsInstance(object_category_scope["object_category_scope"], dict)

            new_object_category_scope = dict()
            new_object_category_scope_uuid = uuid.uuid4().hex
            new_object_category_scope[new_object_category_scope_uuid] = "new_object_category_scope"
            object_category_scope = self.manager.set_object_category_scope_dict(
                "admin",
                self.ref["id"],
                object_category,
                new_object_category_scope)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(self.ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertIn(new_object_category_scope[new_object_category_scope_uuid],
                          object_category_scope["object_category_scope"][object_category].values())

            # Delete the new object_category_scope
            self.manager.del_object_category_scope(
                "admin",
                self.ref["id"],
                object_category,
                new_object_category_scope_uuid)
            object_category_scope = self.manager.get_object_category_scope_dict(
                "admin",
                self.ref["id"],
                object_category)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(self.ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertNotIn(new_object_category_scope_uuid, object_category_scope["object_category_scope"])

            # Add a particular object_category_scope
            object_category_scope = self.manager.add_object_category_scope_dict(
                "admin",
                self.ref["id"],
                object_category,
                new_object_category_scope[new_object_category_scope_uuid])
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("uuid", object_category_scope["object_category_scope"])
            self.assertEqual(new_object_category_scope[new_object_category_scope_uuid],
                             object_category_scope["object_category_scope"]["name"])
            object_category_scope = self.manager.get_object_category_scope_dict(
                "admin",
                self.ref["id"],
                object_category)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(self.ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertNotIn(new_object_category_scope_uuid, object_category_scope["object_category_scope"])

    def test_action_category_scope(self):
        self.create_intra_extension()

        action_categories = self.manager.set_action_category_dict(
            "admin",
            self.ref["id"],
            {
                uuid.uuid4().hex: "compute",
                uuid.uuid4().hex: "identity",
            }
        )

        for action_category in action_categories["action_categories"]:
            action_category_scope = self.manager.get_action_category_scope_dict(
                "admin",
                self.ref["id"],
                action_category)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(self.ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertIsInstance(action_category_scope["action_category_scope"], dict)

            new_action_category_scope = dict()
            new_action_category_scope_uuid = uuid.uuid4().hex
            new_action_category_scope[new_action_category_scope_uuid] = "new_action_category_scope"
            action_category_scope = self.manager.set_action_category_scope_dict(
                "admin",
                self.ref["id"],
                action_category,
                new_action_category_scope)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(self.ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertIn(new_action_category_scope[new_action_category_scope_uuid],
                          action_category_scope["action_category_scope"][action_category].values())

            # Delete the new action_category_scope
            self.manager.del_action_category_scope(
                "admin",
                self.ref["id"],
                action_category,
                new_action_category_scope_uuid)
            action_category_scope = self.manager.get_action_category_scope_dict(
                "admin",
                self.ref["id"],
                action_category)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(self.ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertNotIn(new_action_category_scope_uuid, action_category_scope["action_category_scope"])

            # Add a particular action_category_scope
            action_category_scope = self.manager.add_action_category_scope_dict(
                "admin",
                self.ref["id"],
                action_category,
                new_action_category_scope[new_action_category_scope_uuid])
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("uuid", action_category_scope["action_category_scope"])
            self.assertEqual(new_action_category_scope[new_action_category_scope_uuid],
                             action_category_scope["action_category_scope"]["name"])
            action_category_scope = self.manager.get_action_category_scope_dict(
                "admin",
                self.ref["id"],
                action_category)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(self.ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertNotIn(new_action_category_scope_uuid, action_category_scope["action_category_scope"])

    def test_subject_category_assignment(self):
        self.create_intra_extension()

        new_subject = self.create_user()
        new_subjects = dict()
        new_subjects[new_subject["id"]] = new_subject["name"]
        subjects = self.manager.set_subject_dict("admin", self.ref["id"], new_subjects)

        new_subject_category_uuid = uuid.uuid4().hex
        new_subject_category_value = "role"
        subject_categories = self.manager.set_subject_category_dict(
            "admin",
            self.ref["id"],
            {
                new_subject_category_uuid: new_subject_category_value
            }
        )

        for subject_category in subject_categories["subject_categories"]:
            subject_category_scope = self.manager.get_subject_category_scope_dict(
                "admin",
                self.ref["id"],
                subject_category)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(self.ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertIsInstance(subject_category_scope["subject_category_scope"], dict)

            new_subject_category_scope = dict()
            new_subject_category_scope_uuid = uuid.uuid4().hex
            new_subject_category_scope[new_subject_category_scope_uuid] = "admin"
            subject_category_scope = self.manager.set_subject_category_scope_dict(
                "admin",
                self.ref["id"],
                subject_category,
                new_subject_category_scope)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(self.ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertIn(new_subject_category_scope[new_subject_category_scope_uuid],
                          subject_category_scope["subject_category_scope"][subject_category].values())

            new_subject_category_scope2 = dict()
            new_subject_category_scope2_uuid = uuid.uuid4().hex
            new_subject_category_scope2[new_subject_category_scope2_uuid] = "dev"
            subject_category_scope = self.manager.set_subject_category_scope_dict(
                "admin",
                self.ref["id"],
                subject_category,
                new_subject_category_scope2)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(self.ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertIn(new_subject_category_scope2[new_subject_category_scope2_uuid],
                          subject_category_scope["subject_category_scope"][subject_category].values())

            subject_category_assignments = self.manager.get_subject_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_subject["id"]
            )
            self.assertIsInstance(subject_category_assignments, dict)
            self.assertIn("subject_category_assignments", subject_category_assignments)
            self.assertIn("id", subject_category_assignments)
            self.assertIn("intra_extension_uuid", subject_category_assignments)
            self.assertEqual(self.ref["id"], subject_category_assignments["intra_extension_uuid"])
            self.assertEqual({}, subject_category_assignments["subject_category_assignments"][new_subject["id"]])

            subject_category_assignments = self.manager.set_subject_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_subject["id"],
                {
                    new_subject_category_uuid: [new_subject_category_scope_uuid, new_subject_category_scope2_uuid],
                }
            )
            self.assertIsInstance(subject_category_assignments, dict)
            self.assertIn("subject_category_assignments", subject_category_assignments)
            self.assertIn("id", subject_category_assignments)
            self.assertIn("intra_extension_uuid", subject_category_assignments)
            self.assertEqual(self.ref["id"], subject_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_subject_category_uuid: [new_subject_category_scope_uuid, new_subject_category_scope2_uuid]},
                subject_category_assignments["subject_category_assignments"][new_subject["id"]])
            subject_category_assignments = self.manager.get_subject_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_subject["id"]
            )
            self.assertIsInstance(subject_category_assignments, dict)
            self.assertIn("subject_category_assignments", subject_category_assignments)
            self.assertIn("id", subject_category_assignments)
            self.assertIn("intra_extension_uuid", subject_category_assignments)
            self.assertEqual(self.ref["id"], subject_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_subject_category_uuid: [new_subject_category_scope_uuid, new_subject_category_scope2_uuid]},
                subject_category_assignments["subject_category_assignments"][new_subject["id"]])

            self.manager.del_subject_category_assignment(
                "admin",
                self.ref["id"],
                new_subject["id"],
                new_subject_category_uuid,
                new_subject_category_scope_uuid
            )
            subject_category_assignments = self.manager.get_subject_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_subject["id"]
            )
            self.assertIsInstance(subject_category_assignments, dict)
            self.assertIn("subject_category_assignments", subject_category_assignments)
            self.assertIn("id", subject_category_assignments)
            self.assertIn("intra_extension_uuid", subject_category_assignments)
            self.assertEqual(self.ref["id"], subject_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_subject_category_uuid: [new_subject_category_scope2_uuid, ]},
                subject_category_assignments["subject_category_assignments"][new_subject["id"]])

            data = self.manager.add_subject_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_subject["id"],
                new_subject_category_uuid,
                new_subject_category_scope_uuid
            )

            subject_category_assignments = self.manager.get_subject_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_subject["id"]
            )
            self.assertIsInstance(subject_category_assignments, dict)
            self.assertIn("subject_category_assignments", subject_category_assignments)
            self.assertIn("id", subject_category_assignments)
            self.assertIn("intra_extension_uuid", subject_category_assignments)
            self.assertEqual(self.ref["id"], subject_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_subject_category_uuid: [new_subject_category_scope2_uuid, new_subject_category_scope_uuid]},
                subject_category_assignments["subject_category_assignments"][new_subject["id"]])

    def test_object_category_assignment(self):
        self.create_intra_extension()

        new_object = self.create_user()
        new_objects = dict()
        new_objects[new_object["id"]] = new_object["name"]
        objects = self.manager.set_object_dict("admin", self.ref["id"], new_objects)

        new_object_category_uuid = uuid.uuid4().hex
        new_object_category_value = "role"
        object_categories = self.manager.set_object_category_dict(
            "admin",
            self.ref["id"],
            {
                new_object_category_uuid: new_object_category_value
            }
        )

        for object_category in object_categories["object_categories"]:
            object_category_scope = self.manager.get_object_category_scope_dict(
                "admin",
                self.ref["id"],
                object_category)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(self.ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertIsInstance(object_category_scope["object_category_scope"], dict)

            new_object_category_scope = dict()
            new_object_category_scope_uuid = uuid.uuid4().hex
            new_object_category_scope[new_object_category_scope_uuid] = "admin"
            object_category_scope = self.manager.set_object_category_scope_dict(
                "admin",
                self.ref["id"],
                object_category,
                new_object_category_scope)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(self.ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertIn(new_object_category_scope[new_object_category_scope_uuid],
                          object_category_scope["object_category_scope"][object_category].values())

            new_object_category_scope2 = dict()
            new_object_category_scope2_uuid = uuid.uuid4().hex
            new_object_category_scope2[new_object_category_scope2_uuid] = "dev"
            object_category_scope = self.manager.set_object_category_scope_dict(
                "admin",
                self.ref["id"],
                object_category,
                new_object_category_scope2)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(self.ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertIn(new_object_category_scope2[new_object_category_scope2_uuid],
                          object_category_scope["object_category_scope"][object_category].values())

            object_category_assignments = self.manager.get_object_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_object["id"]
            )
            self.assertIsInstance(object_category_assignments, dict)
            self.assertIn("object_category_assignments", object_category_assignments)
            self.assertIn("id", object_category_assignments)
            self.assertIn("intra_extension_uuid", object_category_assignments)
            self.assertEqual(self.ref["id"], object_category_assignments["intra_extension_uuid"])
            self.assertEqual({}, object_category_assignments["object_category_assignments"][new_object["id"]])

            object_category_assignments = self.manager.set_object_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_object["id"],
                {
                    new_object_category_uuid: [new_object_category_scope_uuid, new_object_category_scope2_uuid],
                }
            )
            self.assertIsInstance(object_category_assignments, dict)
            self.assertIn("object_category_assignments", object_category_assignments)
            self.assertIn("id", object_category_assignments)
            self.assertIn("intra_extension_uuid", object_category_assignments)
            self.assertEqual(self.ref["id"], object_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_object_category_uuid: [new_object_category_scope_uuid, new_object_category_scope2_uuid]},
                object_category_assignments["object_category_assignments"][new_object["id"]])
            object_category_assignments = self.manager.get_object_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_object["id"]
            )
            self.assertIsInstance(object_category_assignments, dict)
            self.assertIn("object_category_assignments", object_category_assignments)
            self.assertIn("id", object_category_assignments)
            self.assertIn("intra_extension_uuid", object_category_assignments)
            self.assertEqual(self.ref["id"], object_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_object_category_uuid: [new_object_category_scope_uuid, new_object_category_scope2_uuid]},
                object_category_assignments["object_category_assignments"][new_object["id"]])

            self.manager.del_object_category_assignment(
                "admin",
                self.ref["id"],
                new_object["id"],
                new_object_category_uuid,
                new_object_category_scope_uuid
            )
            object_category_assignments = self.manager.get_object_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_object["id"]
            )
            self.assertIsInstance(object_category_assignments, dict)
            self.assertIn("object_category_assignments", object_category_assignments)
            self.assertIn("id", object_category_assignments)
            self.assertIn("intra_extension_uuid", object_category_assignments)
            self.assertEqual(self.ref["id"], object_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_object_category_uuid: [new_object_category_scope2_uuid, ]},
                object_category_assignments["object_category_assignments"][new_object["id"]])

            self.manager.add_object_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_object["id"],
                new_object_category_uuid,
                new_object_category_scope_uuid
            )

            object_category_assignments = self.manager.get_object_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_object["id"]
            )
            self.assertIsInstance(object_category_assignments, dict)
            self.assertIn("object_category_assignments", object_category_assignments)
            self.assertIn("id", object_category_assignments)
            self.assertIn("intra_extension_uuid", object_category_assignments)
            self.assertEqual(self.ref["id"], object_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_object_category_uuid: [new_object_category_scope2_uuid, new_object_category_scope_uuid]},
                object_category_assignments["object_category_assignments"][new_object["id"]])

    def test_action_category_assignment(self):
        self.create_intra_extension()

        new_action = self.create_user()
        new_actions = dict()
        new_actions[new_action["id"]] = new_action["name"]
        actions = self.manager.set_action_dict("admin", self.ref["id"], new_actions)

        new_action_category_uuid = uuid.uuid4().hex
        new_action_category_value = "role"
        action_categories = self.manager.set_action_category_dict(
            "admin",
            self.ref["id"],
            {
                new_action_category_uuid: new_action_category_value
            }
        )

        for action_category in action_categories["action_categories"]:
            action_category_scope = self.manager.get_action_category_scope_dict(
                "admin",
                self.ref["id"],
                action_category)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(self.ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertIsInstance(action_category_scope["action_category_scope"], dict)

            new_action_category_scope = dict()
            new_action_category_scope_uuid = uuid.uuid4().hex
            new_action_category_scope[new_action_category_scope_uuid] = "admin"
            action_category_scope = self.manager.set_action_category_scope_dict(
                "admin",
                self.ref["id"],
                action_category,
                new_action_category_scope)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(self.ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertIn(new_action_category_scope[new_action_category_scope_uuid],
                          action_category_scope["action_category_scope"][action_category].values())

            new_action_category_scope2 = dict()
            new_action_category_scope2_uuid = uuid.uuid4().hex
            new_action_category_scope2[new_action_category_scope2_uuid] = "dev"
            action_category_scope = self.manager.set_action_category_scope_dict(
                "admin",
                self.ref["id"],
                action_category,
                new_action_category_scope2)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(self.ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertIn(new_action_category_scope2[new_action_category_scope2_uuid],
                          action_category_scope["action_category_scope"][action_category].values())

            action_category_assignments = self.manager.get_action_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_action["id"]
            )
            self.assertIsInstance(action_category_assignments, dict)
            self.assertIn("action_category_assignments", action_category_assignments)
            self.assertIn("id", action_category_assignments)
            self.assertIn("intra_extension_uuid", action_category_assignments)
            self.assertEqual(self.ref["id"], action_category_assignments["intra_extension_uuid"])
            self.assertEqual({}, action_category_assignments["action_category_assignments"][new_action["id"]])

            action_category_assignments = self.manager.set_action_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_action["id"],
                {
                    new_action_category_uuid: [new_action_category_scope_uuid, new_action_category_scope2_uuid],
                }
            )
            self.assertIsInstance(action_category_assignments, dict)
            self.assertIn("action_category_assignments", action_category_assignments)
            self.assertIn("id", action_category_assignments)
            self.assertIn("intra_extension_uuid", action_category_assignments)
            self.assertEqual(self.ref["id"], action_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_action_category_uuid: [new_action_category_scope_uuid, new_action_category_scope2_uuid]},
                action_category_assignments["action_category_assignments"][new_action["id"]])
            action_category_assignments = self.manager.get_action_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_action["id"]
            )
            self.assertIsInstance(action_category_assignments, dict)
            self.assertIn("action_category_assignments", action_category_assignments)
            self.assertIn("id", action_category_assignments)
            self.assertIn("intra_extension_uuid", action_category_assignments)
            self.assertEqual(self.ref["id"], action_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_action_category_uuid: [new_action_category_scope_uuid, new_action_category_scope2_uuid]},
                action_category_assignments["action_category_assignments"][new_action["id"]])

            self.manager.del_action_category_assignment(
                "admin",
                self.ref["id"],
                new_action["id"],
                new_action_category_uuid,
                new_action_category_scope_uuid
            )
            action_category_assignments = self.manager.get_action_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_action["id"]
            )
            self.assertIsInstance(action_category_assignments, dict)
            self.assertIn("action_category_assignments", action_category_assignments)
            self.assertIn("id", action_category_assignments)
            self.assertIn("intra_extension_uuid", action_category_assignments)
            self.assertEqual(self.ref["id"], action_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_action_category_uuid: [new_action_category_scope2_uuid, ]},
                action_category_assignments["action_category_assignments"][new_action["id"]])

            self.manager.add_action_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_action["id"],
                new_action_category_uuid,
                new_action_category_scope_uuid
            )

            action_category_assignments = self.manager.get_action_category_assignment_dict(
                "admin",
                self.ref["id"],
                new_action["id"]
            )
            self.assertIsInstance(action_category_assignments, dict)
            self.assertIn("action_category_assignments", action_category_assignments)
            self.assertIn("id", action_category_assignments)
            self.assertIn("intra_extension_uuid", action_category_assignments)
            self.assertEqual(self.ref["id"], action_category_assignments["intra_extension_uuid"])
            self.assertEqual(
                {new_action_category_uuid: [new_action_category_scope2_uuid, new_action_category_scope_uuid]},
                action_category_assignments["action_category_assignments"][new_action["id"]])

    def test_sub_meta_rules(self):
        self.create_intra_extension()

        aggregation_algorithms = self.manager.get_aggregation_algorithms("admin", self.ref["id"])
        self.assertIsInstance(aggregation_algorithms, dict)
        self.assertIsInstance(aggregation_algorithms["aggregation_algorithms"], list)
        self.assertIn("and_true_aggregation", aggregation_algorithms["aggregation_algorithms"])
        self.assertIn("test_aggregation", aggregation_algorithms["aggregation_algorithms"])

        aggregation_algorithm = self.manager.get_aggregation_algorithm("admin", self.ref["id"])
        self.assertIsInstance(aggregation_algorithm, dict)
        self.assertIn("aggregation", aggregation_algorithm)
        self.assertIn(aggregation_algorithm["aggregation"], aggregation_algorithms["aggregation_algorithms"])

        _aggregation_algorithm = list(aggregation_algorithms["aggregation_algorithms"])
        _aggregation_algorithm.remove(aggregation_algorithm["aggregation"])
        aggregation_algorithm = self.manager.set_aggregation_algorithm("admin", self.ref["id"], _aggregation_algorithm[0])
        self.assertIsInstance(aggregation_algorithm, dict)
        self.assertIn("aggregation", aggregation_algorithm)
        self.assertIn(aggregation_algorithm["aggregation"], aggregation_algorithms["aggregation_algorithms"])

        sub_meta_rules = self.manager.get_sub_meta_rule("admin", self.ref["id"])
        self.assertIsInstance(sub_meta_rules, dict)
        self.assertIn("sub_meta_rules", sub_meta_rules)
        sub_meta_rules_conf = json.load(open(os.path.join(self.policy_directory, self.ref["model"], "metarule.json")))
        metarule = dict()
        categories = {
            "subject_categories": self.manager.get_subject_category_dict("admin", self.ref["id"]),
            "object_categories": self.manager.get_object_category_dict("admin", self.ref["id"]),
            "action_categories": self.manager.get_action_category_dict("admin", self.ref["id"])
        }
        for relation in sub_meta_rules_conf["sub_meta_rules"]:
            metarule[relation] = dict()
            for item in ("subject_categories", "object_categories", "action_categories"):
                metarule[relation][item] = list()
                for element in sub_meta_rules_conf["sub_meta_rules"][relation][item]:
                    metarule[relation][item].append(self.__get_key_from_value(
                        element,
                        categories[item][item]
                    ))

        for relation in sub_meta_rules["sub_meta_rules"]:
            self.assertIn(relation, metarule)
            for item in ("subject_categories", "object_categories", "action_categories"):
                self.assertEqual(
                    sub_meta_rules["sub_meta_rules"][relation][item],
                    metarule[relation][item]
                )

            new_subject_category = {"id": uuid.uuid4().hex, "name": "subject_category_test"}
            # Add a particular subject_category
            data = self.manager.add_subject_category_dict(
                "admin",
                self.ref["id"],
                new_subject_category["name"])
            new_subject_category["id"] = data["subject_category"]["uuid"]
            subject_categories = self.manager.get_subject_category_dict(
                "admin",
                self.ref["id"])
            self.assertIsInstance(subject_categories, dict)
            self.assertIn("subject_categories", subject_categories)
            self.assertIn("id", subject_categories)
            self.assertIn("intra_extension_uuid", subject_categories)
            self.assertEqual(self.ref["id"], subject_categories["intra_extension_uuid"])
            self.assertIn(new_subject_category["id"], subject_categories["subject_categories"])
            metarule[relation]["subject_categories"].append(new_subject_category["id"])
            _sub_meta_rules = self.manager.set_sub_meta_rule("admin", self.ref["id"], metarule)
            self.assertIn(relation, metarule)
            for item in ("subject_categories", "object_categories", "action_categories"):
                self.assertEqual(
                    _sub_meta_rules["sub_meta_rules"][relation][item],
                    metarule[relation][item]
                )

    def test_sub_rules(self):
        self.create_intra_extension()

        sub_meta_rules = self.manager.get_sub_meta_rule("admin", self.ref["id"])
        self.assertIsInstance(sub_meta_rules, dict)
        self.assertIn("sub_meta_rules", sub_meta_rules)

        sub_rules = self.manager.get_sub_rules("admin", self.ref["id"])
        self.assertIsInstance(sub_rules, dict)
        self.assertIn("rules", sub_rules)
        rules = dict()
        for relation in sub_rules["rules"]:
            self.assertIn(relation, self.manager.get_sub_meta_rule_relations("admin", self.ref["id"])["sub_meta_rule_relations"])
            rules[relation] = list()
            for rule in sub_rules["rules"][relation]:
                print(rule)
                for cat, cat_func, func_name in (
                    ("subject_categories", self.manager.get_subject_category_scope_dict, "subject_category_scope"),
                    ("action_categories", self.manager.get_action_category_scope_dict, "action_category_scope"),
                    ("object_categories", self.manager.get_object_category_scope_dict, "object_category_scope"),
                ):
                    for cat_value in sub_meta_rules["sub_meta_rules"][relation][cat]:
                        scope = cat_func(
                            "admin",
                            self.ref["id"],
                            cat_value
                        )
                        a_scope = rule.pop(0)
                        print(a_scope)
                        if type(a_scope) is not bool:
                            self.assertIn(a_scope, scope[func_name][cat_value])

        # add a new subrule

        relation = sub_rules["rules"].keys()[0]
        sub_rule = []
        for cat, cat_func, func_name in (
            ("subject_categories", self.manager.get_subject_category_scope_dict, "subject_category_scope"),
            ("action_categories", self.manager.get_action_category_scope_dict, "action_category_scope"),
            ("object_categories", self.manager.get_object_category_scope_dict, "object_category_scope"),
        ):
            for cat_value in sub_meta_rules["sub_meta_rules"][relation][cat]:
                scope = cat_func(
                    "admin",
                    self.ref["id"],
                    cat_value
                )
                sub_rule.append(scope[func_name][cat_value].keys()[0])

        sub_rule.append(True)
        sub_rules = self.manager.set_sub_rule("admin", self.ref["id"], relation, sub_rule)
        self.assertIsInstance(sub_rules, dict)
        self.assertIn("rules", sub_rules)
        rules = dict()
        self.assertIn(sub_rule, sub_rules["rules"][relation])
        for relation in sub_rules["rules"]:
            self.assertIn(relation, self.manager.get_sub_meta_rule_relations("admin", self.ref["id"])["sub_meta_rule_relations"])
            rules[relation] = list()
            for rule in sub_rules["rules"][relation]:
                for cat, cat_func, func_name in (
                    ("subject_categories", self.manager.get_subject_category_scope_dict, "subject_category_scope"),
                    ("action_categories", self.manager.get_action_category_scope_dict, "action_category_scope"),
                    ("object_categories", self.manager.get_object_category_scope_dict, "object_category_scope"),
                ):
                    for cat_value in sub_meta_rules["sub_meta_rules"][relation][cat]:
                        scope = cat_func(
                            "admin",
                            self.ref["id"],
                            cat_value
                        )
                        a_scope = rule.pop(0)
                        self.assertIn(a_scope, scope[func_name][cat_value])




