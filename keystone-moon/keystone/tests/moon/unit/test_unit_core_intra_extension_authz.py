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
from keystone.contrib.moon.core import IntraExtensionAdminManager, IntraExtensionAuthzManager
from keystone.tests.unit.ksfixtures import database
from keystone import resource
from keystone.contrib.moon.exception import *
from keystone.tests.unit import default_fixtures
from keystone.contrib.moon.core import LogManager, TenantManager

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

class TestIntraExtensionAuthzManagerAuthz(tests.TestCase):

    def setUp(self):
        self.useFixture(database.Database())
        super(TestIntraExtensionAuthzManagerAuthz, self).setUp()
        self.load_backends()
        self.load_fixtures(default_fixtures)
        self.manager = IntraExtensionAuthzManager()
        self.admin_manager = IntraExtensionAdminManager()

    def __get_key_from_value(self, value, values_dict):
        return filter(lambda v: v[1] == value, values_dict.iteritems())[0][0]

    def load_extra_backends(self):
        return {
            "moonlog_api": LogManager(),
            "tenant_api": TenantManager(),
            # "resource_api": resource.Manager(),
        }

    def config_overrides(self):
        super(TestIntraExtensionAuthzManagerAuthz, self).config_overrides()
        self.policy_directory = 'examples/moon/policies'
        self.config_fixture.config(
            group='moon',
            intraextension_driver='keystone.contrib.moon.backends.sql.IntraExtensionConnector')
        self.config_fixture.config(
            group='moon',
            policy_directory=self.policy_directory)

    def create_tenant(self):
        tenant = {
            "id": uuid.uuid4().hex,
            "name": "TestIntraExtensionAuthzManager",
            "enabled": True,
            "description": "",
            "domain_id": "default"
        }
        return self.resource_api.create_project(tenant["id"], tenant)

    def create_mapping(self, tenant, authz_uuid=None, admin_uuid=None):

        mapping = self.tenant_api.set_tenant_dict(tenant["id"], tenant["name"], authz_uuid, admin_uuid)
        self.assertIsInstance(mapping, dict)
        self.assertIn("authz", mapping)
        self.assertEqual(mapping["authz"], authz_uuid)
        return mapping

    def create_user(self, username="admin"):

        _USER = dict(USER)
        _USER["name"] = username
        return self.identity_api.create_user(_USER)

    def create_intra_extension(self, policy_model="policy_authz"):

        IE["policymodel"] = policy_model
        IE["name"] = uuid.uuid4().hex
        ref = self.admin_manager.load_intra_extension(IE)
        self.assertIsInstance(ref, dict)
        return ref

    def test_tenant_exceptions(self):
        self.assertRaises(
            TenantListEmpty,
            self.manager.get_tenant_dict
        )
        self.assertRaises(
            TenantIDNotFound,
            self.manager.get_tenant_name,
            uuid.uuid4().hex
        )
        self.assertRaises(
            TenantIDNotFound,
            self.manager.set_tenant_name,
            uuid.uuid4().hex, uuid.uuid4().hex
        )
        self.assertRaises(
            TenantIDNotFound,
            self.manager.get_extension_uuid,
            uuid.uuid4().hex, "authz"
        )
        self.assertRaises(
            TenantIDNotFound,
            self.manager.get_extension_uuid,
            uuid.uuid4().hex, "admin"
        )

    def test_intra_extension_exceptions(self):

        tenant = self.create_tenant()
        self.assertRaises(
            IntraExtensionNotFound,
            self.manager.get_extension_uuid,
            tenant["id"], "authz"
        )
        self.assertRaises(
            IntraExtensionNotFound,
            self.manager.get_extension_uuid,
            tenant["id"], "admin"
        )
        # TODO

    def test_delete_admin_intra_extension(self):
        self.assertRaises(
            AdminException,
            self.manager.delete_intra_extension,
            self.ref["id"])

    def test_authz_exceptions(self):
        self.assertRaises(
            IntraExtensionNotFound,
            self.manager.authz,
            uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex
        )

        admin_user = self.create_user()
        tenant = self.create_tenant()
        ie_authz = self.create_intra_extension("policy_authz")
        ie_admin = self.create_intra_extension("policy_admin")
        mapping = self.create_mapping(tenant, ie_authz["id"], ie_admin["id"])

        # Test when subject is unknown
        self.assertRaises(
            SubjectUnknown,
            self.manager.authz,
            ie_authz["id"], uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex
        )

        # Test when subject is known but not the object
        demo_user = self.create_user("demo")
        self.manager.add_subject_dict(
            admin_user['id'],
            self.ref["id"],
            demo_user["id"]
        )

        self.assertRaises(
            ObjectUnknown,
            self.manager.authz,
            ie_authz["id"], demo_user["id"], uuid.uuid4().hex, uuid.uuid4().hex
        )

        # Test when subject and object are known but not the action
        _tmp = self.manager.add_object_dict(
            admin_user['id'],
            self.ref["id"],
            "my_object"
        ).items()[0]
        my_object = {"id": _tmp[0], "name": _tmp[1]}

        self.assertRaises(
            ActionUnknown,
            self.manager.authz,
            ie_authz["id"], demo_user["id"], my_object["id"], uuid.uuid4().hex
        )

        # Test when subject and object and action are known
        _tmp = self.manager.add_action_dict(
            admin_user['id'],
            self.ref["id"],
            "my_action"
        ).items()[0]
        my_action = {"id": _tmp[0], "name": _tmp[1]}

        self.assertRaises(
            SubjectCategoryAssignmentOutOfScope,
            self.manager.authz,
            ie_authz["id"], demo_user["id"], my_object["id"], my_action["id"]
        )

        # Add a subject scope and test ObjectCategoryAssignmentOutOfScope
        _tmp = self.manager.add_subject_category_dict(
            admin_user['id'],
            self.ref["id"],
            "my_subject_category"
        )
        my_subject_category = {"id": _tmp[0], "name": _tmp[1]}

        _tmp = self.manager.add_subject_category_scope_dict(
            admin_user['id'],
            self.ref["id"],
            my_subject_category["id"],
            "my_subject_scope",
        )
        my_subject_scope = {"id": _tmp[0], "name": _tmp[1]}

        self.assertRaises(
            ObjectCategoryAssignmentOutOfScope,
            self.manager.authz,
            ie_authz["id"], demo_user["id"], my_object["id"], my_action["id"]
        )

        # Add an object scope and test ActionCategoryAssignmentOutOfScope
        _tmp = self.manager.add_object_category_dict(
            admin_user['id'],
            self.ref["id"],
            "my_object_category"
        )
        my_object_category = {"id": _tmp[0], "name": _tmp[1]}

        _tmp = self.manager.add_object_category_scope_dict(
            admin_user['id'],
            self.ref["id"],
            my_object_category["id"],
            "my_object_scope",
        )
        my_object_scope = {"id": _tmp[0], "name": _tmp[1]}

        self.assertRaises(
            ActionCategoryAssignmentOutOfScope,
            self.manager.authz,
            ie_authz["id"], demo_user["id"], my_object["id"], my_action["id"]
        )

        # Add an action scope and test SubjectCategoryAssignmentUnknown
        _tmp = self.manager.add_action_category_dict(
            admin_user['id'],
            self.ref["id"],
            "my_action_category"
        )
        my_action_category = {"id": _tmp[0], "name": _tmp[1]}

        _tmp = self.manager.add_action_category_scope_dict(
            admin_user['id'],
            self.ref["id"],
            my_action_category["id"],
            "my_action_scope",
        )
        my_action_scope = {"id": _tmp[0], "name": _tmp[1]}

        self.assertRaises(
            SubjectCategoryAssignmentUnknown,
            self.manager.authz,
            ie_authz["id"], demo_user["id"], my_object["id"], my_action["id"]
        )

        # Add a subject assignment and test ObjectCategoryAssignmentUnknown
        self.manager.add_subject_category_assignment_dict(
            admin_user['id'],
            self.ref["id"],
            demo_user["id"],
            my_subject_category["id"],
            my_subject_scope["id"]
        )

        self.assertRaises(
            ObjectCategoryAssignmentUnknown,
            self.manager.authz,
            ie_authz["id"], demo_user["id"], my_object["id"], my_action["id"]
        )

        # Add an object assignment and test ActionCategoryAssignmentUnknown
        self.manager.add_object_category_assignment_dict(
            admin_user['id'],
            self.ref["id"],
            demo_user["id"],
            my_object_category["id"],
            my_object_scope["id"]
        )

        self.assertRaises(
            ActionCategoryAssignmentUnknown,
            self.manager.authz,
            ie_authz["id"], demo_user["id"], my_object["id"], my_action["id"]
        )

        # Add an action assignment and test RuleUnknown
        self.manager.add_action_category_assignment_dict(
            admin_user['id'],
            self.ref["id"],
            demo_user["id"],
            my_action_category["id"],
            my_action_scope["id"]
        )

        self.assertRaises(
            RuleUnknown,
            self.manager.authz,
            ie_authz["id"], demo_user["id"], my_object["id"], my_action["id"]
        )

        # Add the correct rule and test that no exception is raised
        my_meta_rule = {
            "relation_super": {
                "subject_categories": [my_subject_category["id"], ],
                "action_categories": [my_object_category["id"], ],
                "object_categories": [my_action_category["id"], ],
                "relation": "relation_super"
            }
        }
        self.manager.set_sub_meta_rule(
            admin_user['id'],
            self.ref["id"],
            my_meta_rule
        )
        self.manager.set_sub_rule(
            admin_user['id'],
            self.ref["id"],
            "relation_super",
            [my_subject_scope, my_object_scope, my_action_scope]
        )

        result = self.manager.authz(ie_authz["id"], demo_user["id"], my_object["id"], my_action["id"])
        self.assertEqual(True, result)

    def test_subjects(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        subjects = self.manager.get_subject_dict(admin_user["id"], tenant["id"])
        self.assertIsInstance(subjects, dict)
        self.assertIn("subjects", subjects)
        self.assertIn("id", subjects)
        self.assertIn("intra_extension_uuid", subjects)
        self.assertEqual(ref["id"], subjects["intra_extension_uuid"])
        self.assertIsInstance(subjects["subjects"], dict)

        new_subject = self.create_user("my_user")
        new_subjects = dict()
        new_subjects[new_subject["id"]] = new_subject["name"]
        self.assertRaises(
            SubjectAddNotAuthorized,
            self.manager.set_subject_dict,
            admin_user["id"], ref["id"], new_subjects)

        # Delete the new subject
        self.assertRaises(
            SubjectDelNotAuthorized,
            self.manager.del_subject,
            admin_user["id"], ref["id"], new_subject["id"])

        # Add a particular subject
        self.assertRaises(
            SubjectAddNotAuthorized,
            self.manager.add_subject_dict,
            admin_user["id"], ref["id"], new_subject["id"])

    def test_objects(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        objects = self.manager.get_object_dict(admin_user["id"], tenant["id"])
        self.assertIsInstance(objects, dict)
        self.assertIn("objects", objects)
        self.assertIn("id", objects)
        self.assertIn("intra_extension_uuid", objects)
        self.assertEqual(ref["id"], objects["intra_extension_uuid"])
        self.assertIsInstance(objects["objects"], dict)

        new_object = {"id": uuid.uuid4().hex, "name": "my_object"}
        new_objects = dict()
        new_objects[new_object["id"]] = new_object["name"]
        self.assertRaises(
            ObjectAddNotAuthorized,
            self.manager.set_object_dict,
            admin_user["id"], ref["id"], new_object["id"])

        # Delete the new object
        self.assertRaises(
            ObjectDelNotAuthorized,
            self.manager.del_object,
            admin_user["id"], ref["id"], new_object["id"])

        # Add a particular object
        self.assertRaises(
            ObjectAddNotAuthorized,
            self.manager.add_object_dict,
            admin_user["id"], ref["id"], new_object["name"])

    def test_actions(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        actions = self.manager.get_action_dict(admin_user["id"], tenant["id"])
        self.assertIsInstance(actions, dict)
        self.assertIn("actions", actions)
        self.assertIn("id", actions)
        self.assertIn("intra_extension_uuid", actions)
        self.assertEqual(ref["id"], actions["intra_extension_uuid"])
        self.assertIsInstance(actions["actions"], dict)

        new_action = {"id": uuid.uuid4().hex, "name": "my_action"}
        new_actions = dict()
        new_actions[new_action["id"]] = new_action["name"]
        self.assertRaises(
            ActionAddNotAuthorized,
            self.manager.set_action_dict,
            admin_user["id"], ref["id"], new_actions)

        # Delete the new action
        self.assertRaises(
            ActionDelNotAuthorized,
            self.manager.del_action,
            admin_user["id"], ref["id"], new_action["id"])

        # Add a particular action
        self.assertRaises(
            ActionAddNotAuthorized,
            self.manager.add_action_dict,
            admin_user["id"], ref["id"], new_action["id"])

    def test_subject_categories(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        subject_categories = self.manager.get_subject_category_dict(admin_user["id"], ref["id"])
        self.assertIsInstance(subject_categories, dict)
        self.assertIn("subject_categories", subject_categories)
        self.assertIn("id", subject_categories)
        self.assertIn("intra_extension_uuid", subject_categories)
        self.assertEqual(ref["id"], subject_categories["intra_extension_uuid"])
        self.assertIsInstance(subject_categories["subject_categories"], dict)

        new_subject_category = {"id": uuid.uuid4().hex, "name": "subject_category_test"}
        new_subject_categories = dict()
        new_subject_categories[new_subject_category["id"]] = new_subject_category["name"]
        self.assertRaises(
            SubjectCategoryAddNotAuthorized,
            self.manager.set_subject_category_dict,
            admin_user["id"], ref["id"], new_subject_categories)

        # Delete the new subject_category
        self.assertRaises(
            SubjectCategoryDelNotAuthorized,
            self.manager.del_subject_category,
            admin_user["id"], ref["id"], new_subject_category["id"])

        # Add a particular subject_category
        self.assertRaises(
            SubjectCategoryAddNotAuthorized,
            self.manager.add_subject_category_dict,
            admin_user["id"], ref["id"], new_subject_category["name"])

    def test_object_categories(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        object_categories = self.manager.get_object_category_dict(admin_user["id"], ref["id"])
        self.assertIsInstance(object_categories, dict)
        self.assertIn("object_categories", object_categories)
        self.assertIn("id", object_categories)
        self.assertIn("intra_extension_uuid", object_categories)
        self.assertEqual(ref["id"], object_categories["intra_extension_uuid"])
        self.assertIsInstance(object_categories["object_categories"], dict)

        new_object_category = {"id": uuid.uuid4().hex, "name": "object_category_test"}
        new_object_categories = dict()
        new_object_categories[new_object_category["id"]] = new_object_category["name"]
        self.assertRaises(
            ObjectCategoryAddNotAuthorized,
            self.manager.set_object_category_dict,
            admin_user["id"], ref["id"], new_object_categories)

        # Delete the new object_category
        self.assertRaises(
            ObjectCategoryDelNotAuthorized,
            self.manager.del_object_category,
            admin_user["id"], ref["id"], new_object_category["id"])

        # Add a particular object_category
        self.assertRaises(
            ObjectCategoryAddNotAuthorized,
            self.manager.add_object_category_dict,
            admin_user["id"], ref["id"], new_object_category["name"])

    def test_action_categories(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        action_categories = self.manager.get_action_category_dict(admin_user["id"], ref["id"])
        self.assertIsInstance(action_categories, dict)
        self.assertIn("action_categories", action_categories)
        self.assertIn("id", action_categories)
        self.assertIn("intra_extension_uuid", action_categories)
        self.assertEqual(ref["id"], action_categories["intra_extension_uuid"])
        self.assertIsInstance(action_categories["action_categories"], dict)

        new_action_category = {"id": uuid.uuid4().hex, "name": "action_category_test"}
        new_action_categories = dict()
        new_action_categories[new_action_category["id"]] = new_action_category["name"]
        self.assertRaises(
            ActionCategoryAddNotAuthorized,
            self.manager.set_action_category_dict,
            admin_user["id"], ref["id"], new_action_categories)

        # Delete the new action_category
        self.assertRaises(
            ActionCategoryDelNotAuthorized,
            self.manager.del_action_category,
            admin_user["id"], ref["id"], new_action_category["id"])

        # Add a particular action_category
        self.assertRaises(
            ActionCategoryAddNotAuthorized,
            self.manager.add_action_category_dict,
            admin_user["id"], ref["id"], new_action_category["name"])

    def test_subject_category_scope(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        subject_categories = self.admin_manager.set_subject_category_dict(
            admin_user["id"],
            ref["id"],
            {
                uuid.uuid4().hex: admin_user["id"],
                uuid.uuid4().hex: "dev",
            }
        )

        for subject_category in subject_categories["subject_categories"]:
            subject_category_scope = self.manager.get_subject_category_scope_dict(
                admin_user["id"],
                ref["id"],
                subject_category)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertIsInstance(subject_category_scope["subject_category_scope"], dict)

            new_subject_category_scope = dict()
            new_subject_category_scope_uuid = uuid.uuid4().hex
            new_subject_category_scope[new_subject_category_scope_uuid] = "new_subject_category_scope"
            self.assertRaises(
                SubjectCategoryScopeAddNotAuthorized,
                self.manager.set_subject_category_scope_dict,
                admin_user["id"], ref["id"], subject_category, new_subject_category_scope)

            # Delete the new subject_category_scope
            self.assertRaises(
                SubjectCategoryScopeDelNotAuthorized,
                self.manager.del_subject_category_scope,
                admin_user["id"], ref["id"], subject_category, new_subject_category_scope_uuid)

            # Add a particular subject_category_scope
            self.assertRaises(
                SubjectCategoryScopeAddNotAuthorized,
                self.manager.add_subject_category_scope_dict,
                admin_user["id"], ref["id"], subject_category, new_subject_category_scope[new_subject_category_scope_uuid])

    def test_object_category_scope(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        object_categories = self.admin_manager.set_object_category_dict(
            admin_user["id"],
            ref["id"],
            {
                uuid.uuid4().hex: "id",
                uuid.uuid4().hex: "domain",
            }
        )

        for object_category in object_categories["object_categories"]:
            object_category_scope = self.manager.get_object_category_scope_dict(
                admin_user["id"],
                ref["id"],
                object_category)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertIsInstance(object_category_scope["object_category_scope"], dict)

            new_object_category_scope = dict()
            new_object_category_scope_uuid = uuid.uuid4().hex
            new_object_category_scope[new_object_category_scope_uuid] = "new_object_category_scope"
            self.assertRaises(
                ObjectCategoryScopeAddNotAuthorized,
                self.manager.set_object_category_scope_dict,
                admin_user["id"], ref["id"], object_category, new_object_category_scope)

            # Delete the new object_category_scope
            self.assertRaises(
                ObjectCategoryScopeDelNotAuthorized,
                self.manager.del_object_category_scope,
                admin_user["id"], ref["id"], object_category, new_object_category_scope_uuid)

            # Add a particular object_category_scope
            self.assertRaises(
                ObjectCategoryScopeAddNotAuthorized,
                self.manager.add_object_category_scope_dict,
                admin_user["id"], ref["id"], object_category, new_object_category_scope[new_object_category_scope_uuid])

    def test_action_category_scope(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        action_categories = self.admin_manager.set_action_category_dict(
            admin_user["id"],
            ref["id"],
            {
                uuid.uuid4().hex: "compute",
                uuid.uuid4().hex: "identity",
            }
        )

        for action_category in action_categories["action_categories"]:
            action_category_scope = self.manager.get_action_category_scope_dict(
                admin_user["id"],
                ref["id"],
                action_category)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertIsInstance(action_category_scope["action_category_scope"], dict)

            new_action_category_scope = dict()
            new_action_category_scope_uuid = uuid.uuid4().hex
            new_action_category_scope[new_action_category_scope_uuid] = "new_action_category_scope"
            self.assertRaises(
                ActionCategoryScopeAddNotAuthorized,
                self.manager.set_action_category_scope_dict,
                admin_user["id"], ref["id"], action_category, new_action_category_scope)

            # Delete the new action_category_scope
            self.assertRaises(
                ActionCategoryScopeDelNotAuthorized,
                self.manager.del_action_category_scope,
                admin_user["id"], ref["id"], action_category, new_action_category_scope_uuid)

            # Add a particular action_category_scope
            self.assertRaises(
                ActionCategoryScopeAddNotAuthorized,
                self.manager.add_action_category_scope_dict,
                admin_user["id"], ref["id"], action_category, new_action_category_scope[new_action_category_scope_uuid])

    def test_subject_category_assignment(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        new_subject = self.create_user()
        new_subjects = dict()
        new_subjects[new_subject["id"]] = new_subject["name"]
        subjects = self.admin_manager.set_subject_dict(admin_user["id"], ref["id"], new_subjects)

        new_subject_category_uuid = uuid.uuid4().hex
        new_subject_category_value = "role"
        subject_categories = self.admin_manager.set_subject_category_dict(
            admin_user["id"],
            ref["id"],
            {
                new_subject_category_uuid: new_subject_category_value
            }
        )

        for subject_category in subject_categories["subject_categories"]:
            subject_category_scope = self.admin_manager.get_subject_category_scope_dict(
                admin_user["id"],
                ref["id"],
                subject_category)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertIsInstance(subject_category_scope["subject_category_scope"], dict)

            new_subject_category_scope = dict()
            new_subject_category_scope_uuid = uuid.uuid4().hex
            new_subject_category_scope[new_subject_category_scope_uuid] = admin_user["id"]
            subject_category_scope = self.admin_manager.set_subject_category_scope_dict(
                admin_user["id"],
                ref["id"],
                subject_category,
                new_subject_category_scope)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertIn(new_subject_category_scope[new_subject_category_scope_uuid],
                          subject_category_scope["subject_category_scope"][subject_category].values())

            new_subject_category_scope2 = dict()
            new_subject_category_scope2_uuid = uuid.uuid4().hex
            new_subject_category_scope2[new_subject_category_scope2_uuid] = "dev"
            subject_category_scope = self.admin_manager.set_subject_category_scope_dict(
                admin_user["id"],
                ref["id"],
                subject_category,
                new_subject_category_scope2)
            self.assertIsInstance(subject_category_scope, dict)
            self.assertIn("subject_category_scope", subject_category_scope)
            self.assertIn("id", subject_category_scope)
            self.assertIn("intra_extension_uuid", subject_category_scope)
            self.assertEqual(ref["id"], subject_category_scope["intra_extension_uuid"])
            self.assertIn(new_subject_category_scope2[new_subject_category_scope2_uuid],
                          subject_category_scope["subject_category_scope"][subject_category].values())

            subject_category_assignments = self.manager.get_subject_category_assignment_dict(
                admin_user["id"],
                ref["id"],
                new_subject["id"]
            )
            self.assertIsInstance(subject_category_assignments, dict)
            self.assertIn("subject_category_assignments", subject_category_assignments)
            self.assertIn("id", subject_category_assignments)
            self.assertIn("intra_extension_uuid", subject_category_assignments)
            self.assertEqual(ref["id"], subject_category_assignments["intra_extension_uuid"])
            self.assertEqual({}, subject_category_assignments["subject_category_assignments"][new_subject["id"]])

            self.assertRaises(
                SubjectCategoryAssignmentAddNotAuthorized,
                self.manager.set_subject_category_assignment_dict,
                admin_user["id"], ref["id"], new_subject["id"],
                {
                    new_subject_category_uuid: [new_subject_category_scope_uuid, new_subject_category_scope2_uuid],
                })

            self.assertRaises(
                SubjectCategoryAssignmentDelNotAuthorized,
                self.manager.del_subject_category_assignment,
                admin_user["id"], ref["id"], new_subject["id"],
                new_subject_category_uuid,
                new_subject_category_scope_uuid)

            self.assertRaises(
                SubjectCategoryAssignmentAddNotAuthorized,
                self.manager.add_subject_category_assignment_dict,
                admin_user["id"], ref["id"], new_subject["id"],
                new_subject_category_uuid,
                new_subject_category_scope_uuid)

    def test_object_category_assignment(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        new_object = {"id": uuid.uuid4().hex, "name": "my_object"}
        new_objects = dict()
        new_objects[new_object["id"]] = new_object["name"]
        objects = self.admin_manager.set_object_dict(admin_user["id"], ref["id"], new_objects)

        new_object_category_uuid = uuid.uuid4().hex
        new_object_category_value = "role"
        object_categories = self.admin_manager.set_object_category_dict(
            admin_user["id"],
            ref["id"],
            {
                new_object_category_uuid: new_object_category_value
            }
        )

        for object_category in object_categories["object_categories"]:
            object_category_scope = self.admin_manager.get_object_category_scope_dict(
                admin_user["id"],
                ref["id"],
                object_category)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertIsInstance(object_category_scope["object_category_scope"], dict)

            new_object_category_scope = dict()
            new_object_category_scope_uuid = uuid.uuid4().hex
            new_object_category_scope[new_object_category_scope_uuid] = admin_user["id"]
            object_category_scope = self.admin_manager.set_object_category_scope_dict(
                admin_user["id"],
                ref["id"],
                object_category,
                new_object_category_scope)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertIn(new_object_category_scope[new_object_category_scope_uuid],
                          object_category_scope["object_category_scope"][object_category].values())

            new_object_category_scope2 = dict()
            new_object_category_scope2_uuid = uuid.uuid4().hex
            new_object_category_scope2[new_object_category_scope2_uuid] = "dev"
            object_category_scope = self.admin_manager.set_object_category_scope_dict(
                admin_user["id"],
                ref["id"],
                object_category,
                new_object_category_scope2)
            self.assertIsInstance(object_category_scope, dict)
            self.assertIn("object_category_scope", object_category_scope)
            self.assertIn("id", object_category_scope)
            self.assertIn("intra_extension_uuid", object_category_scope)
            self.assertEqual(ref["id"], object_category_scope["intra_extension_uuid"])
            self.assertIn(new_object_category_scope2[new_object_category_scope2_uuid],
                          object_category_scope["object_category_scope"][object_category].values())

            object_category_assignments = self.manager.get_object_category_assignment_dict(
                admin_user["id"],
                ref["id"],
                new_object["id"]
            )
            self.assertIsInstance(object_category_assignments, dict)
            self.assertIn("object_category_assignments", object_category_assignments)
            self.assertIn("id", object_category_assignments)
            self.assertIn("intra_extension_uuid", object_category_assignments)
            self.assertEqual(ref["id"], object_category_assignments["intra_extension_uuid"])
            self.assertEqual({}, object_category_assignments["object_category_assignments"][new_object["id"]])

            self.assertRaises(
                ObjectCategoryAssignmentAddNotAuthorized,
                self.manager.set_object_category_assignment_dict,
                admin_user["id"], ref["id"], new_object["id"],
                {
                    new_object_category_uuid: [new_object_category_scope_uuid, new_object_category_scope2_uuid],
                })

            self.assertRaises(
                ObjectCategoryAssignmentDelNotAuthorized,
                self.manager.del_object_category_assignment,
                admin_user["id"], ref["id"], new_object["id"],
                new_object_category_uuid,
                new_object_category_scope_uuid)

            self.assertRaises(
                ObjectCategoryAssignmentAddNotAuthorized,
                self.manager.add_object_category_assignment_dict,
                admin_user["id"], ref["id"], new_object["id"],
                new_object_category_uuid,
                new_object_category_scope_uuid)

    def test_action_category_assignment(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        new_action = {"id": uuid.uuid4().hex, "name": "my_action"}
        new_actions = dict()
        new_actions[new_action["id"]] = new_action["name"]
        actions = self.admin_manager.set_action_dict(admin_user["id"], ref["id"], new_actions)

        new_action_category_uuid = uuid.uuid4().hex
        new_action_category_value = "role"
        action_categories = self.admin_manager.set_action_category_dict(
            admin_user["id"],
            ref["id"],
            {
                new_action_category_uuid: new_action_category_value
            }
        )

        for action_category in action_categories["action_categories"]:
            action_category_scope = self.admin_manager.get_action_category_scope_dict(
                admin_user["id"],
                ref["id"],
                action_category)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertIsInstance(action_category_scope["action_category_scope"], dict)

            new_action_category_scope = dict()
            new_action_category_scope_uuid = uuid.uuid4().hex
            new_action_category_scope[new_action_category_scope_uuid] = admin_user["id"]
            action_category_scope = self.admin_manager.set_action_category_scope_dict(
                admin_user["id"],
                ref["id"],
                action_category,
                new_action_category_scope)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertIn(new_action_category_scope[new_action_category_scope_uuid],
                          action_category_scope["action_category_scope"][action_category].values())

            new_action_category_scope2 = dict()
            new_action_category_scope2_uuid = uuid.uuid4().hex
            new_action_category_scope2[new_action_category_scope2_uuid] = "dev"
            action_category_scope = self.admin_manager.set_action_category_scope_dict(
                admin_user["id"],
                ref["id"],
                action_category,
                new_action_category_scope2)
            self.assertIsInstance(action_category_scope, dict)
            self.assertIn("action_category_scope", action_category_scope)
            self.assertIn("id", action_category_scope)
            self.assertIn("intra_extension_uuid", action_category_scope)
            self.assertEqual(ref["id"], action_category_scope["intra_extension_uuid"])
            self.assertIn(new_action_category_scope2[new_action_category_scope2_uuid],
                          action_category_scope["action_category_scope"][action_category].values())

            action_category_assignments = self.manager.get_action_category_assignment_dict(
                admin_user["id"],
                ref["id"],
                new_action["id"]
            )
            self.assertIsInstance(action_category_assignments, dict)
            self.assertIn("action_category_assignments", action_category_assignments)
            self.assertIn("id", action_category_assignments)
            self.assertIn("intra_extension_uuid", action_category_assignments)
            self.assertEqual(ref["id"], action_category_assignments["intra_extension_uuid"])
            self.assertEqual({}, action_category_assignments["action_category_assignments"][new_action["id"]])

            self.assertRaises(
                ActionCategoryAssignmentAddNotAuthorized,
                self.manager.set_action_category_assignment_dict,
                admin_user["id"], ref["id"], new_action["id"],
                {
                    new_action_category_uuid: [new_action_category_scope_uuid, new_action_category_scope2_uuid],
                })

            self.assertRaises(
                ActionCategoryAssignmentDelNotAuthorized,
                self.manager.del_action_category_assignment,
                admin_user["id"], ref["id"], new_action["id"],
                new_action_category_uuid,
                new_action_category_scope_uuid)

            self.assertRaises(
                ActionCategoryAssignmentAddNotAuthorized,
                self.manager.add_action_category_assignment_dict,
                admin_user["id"], ref["id"], new_action["id"],
                new_action_category_uuid,
                new_action_category_scope_uuid)

    def test_sub_meta_rules(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        aggregation_algorithms = self.manager.get_aggregation_algorithms(admin_user["id"], ref["id"])
        self.assertIsInstance(aggregation_algorithms, dict)
        self.assertIsInstance(aggregation_algorithms["aggregation_algorithms"], list)
        self.assertIn("and_true_aggregation", aggregation_algorithms["aggregation_algorithms"])
        self.assertIn("test_aggregation", aggregation_algorithms["aggregation_algorithms"])

        aggregation_algorithm = self.manager.get_aggregation_algorithm(admin_user["id"], ref["id"])
        self.assertIsInstance(aggregation_algorithm, dict)
        self.assertIn("aggregation", aggregation_algorithm)
        self.assertIn(aggregation_algorithm["aggregation"], aggregation_algorithms["aggregation_algorithms"])

        _aggregation_algorithm = list(aggregation_algorithms["aggregation_algorithms"])
        _aggregation_algorithm.remove(aggregation_algorithm["aggregation"])
        self.assertRaises(
            MetaRuleAddNotAuthorized,
            self.manager.set_aggregation_algorithm,
            admin_user["id"], ref["id"], _aggregation_algorithm[0])

        sub_meta_rules = self.manager.get_sub_meta_rule(admin_user["id"], ref["id"])
        self.assertIsInstance(sub_meta_rules, dict)
        self.assertIn("sub_meta_rules", sub_meta_rules)
        sub_meta_rules_conf = json.load(open(os.path.join(self.policy_directory, ref["model"], "metarule.json")))
        metarule = dict()
        categories = {
            "subject_categories": self.manager.get_subject_category_dict(admin_user["id"], ref["id"]),
            "object_categories": self.manager.get_object_category_dict(admin_user["id"], ref["id"]),
            "action_categories": self.manager.get_action_category_dict(admin_user["id"], ref["id"])
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
            data = self.admin_manager.add_subject_category_dict(
                admin_user["id"],
                ref["id"],
                new_subject_category["name"])
            new_subject_category["id"] = data["subject_category"]["uuid"]
            subject_categories = self.manager.get_subject_category_dict(
                admin_user["id"],
                ref["id"])
            self.assertIsInstance(subject_categories, dict)
            self.assertIn("subject_categories", subject_categories)
            self.assertIn("id", subject_categories)
            self.assertIn("intra_extension_uuid", subject_categories)
            self.assertEqual(ref["id"], subject_categories["intra_extension_uuid"])
            self.assertIn(new_subject_category["id"], subject_categories["subject_categories"])
            metarule[relation]["subject_categories"].append(new_subject_category["id"])
            self.assertRaises(
                MetaRuleAddNotAuthorized,
                self.manager.set_sub_meta_rule,
                admin_user["id"], ref["id"], metarule)

    def test_sub_rules(self):
        demo_user = self.create_user("demo")
        admin_user = self.create_user()
        tenant = self.create_tenant()
        ref = self.create_intra_extension("policy_authz")
        ref_admin = self.create_intra_extension("policy_admin")
        self.create_mapping(tenant, ref["id"], ref_admin["id"])

        sub_meta_rules = self.manager.get_sub_meta_rule(admin_user["id"], ref["id"])
        self.assertIsInstance(sub_meta_rules, dict)
        self.assertIn("sub_meta_rules", sub_meta_rules)

        sub_rules = self.manager.get_sub_rules(admin_user["id"], ref["id"])
        self.assertIsInstance(sub_rules, dict)
        self.assertIn("rules", sub_rules)
        rules = dict()
        for relation in sub_rules["rules"]:
            self.assertIn(relation, self.manager.get_sub_meta_rule_relations(admin_user["id"], ref["id"])["sub_meta_rule_relations"])
            rules[relation] = list()
            for rule in sub_rules["rules"][relation]:
                for cat, cat_func, func_name in (
                    ("subject_categories", self.manager.get_subject_category_scope_dict, "subject_category_scope"),
                    ("action_categories", self.manager.get_action_category_scope_dict, "action_category_scope"),
                    ("object_categories", self.manager.get_object_category_scope_dict, "object_category_scope"),
                ):
                    for cat_value in sub_meta_rules["sub_meta_rules"][relation][cat]:
                        scope = cat_func(
                            admin_user["id"],
                            ref["id"],
                            cat_value
                        )
                        a_scope = rule.pop(0)
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
                    admin_user["id"],
                    ref["id"],
                    cat_value
                )
                sub_rule.append(scope[func_name][cat_value].keys()[0])

        self.assertRaises(
            RuleAddNotAuthorized,
            self.manager.set_sub_rule,
            admin_user["id"], ref["id"], relation, sub_rule)

