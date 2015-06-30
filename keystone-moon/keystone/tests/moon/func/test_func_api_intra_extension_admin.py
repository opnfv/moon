# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import unittest
import json
import httplib
from uuid import uuid4
import copy

CREDENTIALS = {
    "host": "127.0.0.1",
    "port": "35357",
    "login": "admin",
    "password": "nomoresecrete",
    "tenant_name": "demo",
    "sessionid": "kxb50d9uusiywfcs2fiidmu1j5nsyckr",
    "csrftoken": "",
    "x-subject-token": ""
}


def get_url(url, post_data=None, delete_data=None, crsftoken=None, method="GET", authtoken=None):
    # MOON_SERVER_IP["URL"] = url
    # _url = "http://{HOST}:{PORT}".format(**MOON_SERVER_IP)
    if post_data:
        method = "POST"
    if delete_data:
        method = "DELETE"
    # print("\033[32m{} {}\033[m".format(method, url))
    conn = httplib.HTTPConnection(CREDENTIALS["host"], CREDENTIALS["port"])
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        # "Accept": "text/plain",
        "Accept": "text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Cookie': 'sessionid={}'.format(CREDENTIALS["sessionid"]),
    }
    if crsftoken:
        headers["Cookie"] = "csrftoken={}; sessionid={}; NG_TRANSLATE_LANG_KEY:\"en\"".format(crsftoken, CREDENTIALS["sessionid"])
        CREDENTIALS["crsftoken"] = crsftoken
    if authtoken:
        headers["X-Auth-Token"] = CREDENTIALS["x-subject-token"]
    if post_data:
        method = "POST"
        headers["Content-type"] = "application/json"
        if crsftoken:
            post_data = "&".join(map(lambda x: "=".join(x), post_data))
        elif "crsftoken" in CREDENTIALS and "sessionid" in CREDENTIALS:
            post_data = json.dumps(post_data)
            headers["Cookie"] = "csrftoken={}; sessionid={}; NG_TRANSLATE_LANG_KEY:\"en\"".format(
                CREDENTIALS["crsftoken"],
                CREDENTIALS["sessionid"])
        else:
            post_data = json.dumps(post_data)
        # conn.request(method, url, json.dumps(post_data), headers=headers)
        conn.request(method, url, post_data, headers=headers)
    elif delete_data:
        method = "DELETE"
        conn.request(method, url, json.dumps(delete_data), headers=headers)
    else:
        conn.request(method, url, headers=headers)
    resp = conn.getresponse()
    headers = resp.getheaders()
    try:
        CREDENTIALS["x-subject-token"] = dict(headers)["x-subject-token"]
    except KeyError:
        pass
    if crsftoken:
        sessionid_start = dict(headers)["set-cookie"].index("sessionid=")+len("sessionid=")
        sessionid_end = dict(headers)["set-cookie"].index(";", sessionid_start)
        sessionid = dict(headers)["set-cookie"][sessionid_start:sessionid_end]
        CREDENTIALS["sessionid"] = sessionid
    content = resp.read()
    conn.close()
    try:
        return json.loads(content)
    except ValueError:
        return {"content": content}

def get_keystone_user(name="demo", intra_extension_uuid=None):
    users = get_url("/v3/users", authtoken=True)["users"]
    demo_user_uuid = None
    for user in users:
        if user["name"] == name:
            demo_user_uuid = user["id"]
            break
        # if user "name" is not present, fallback to admin
        if user["name"] == "admin":
            demo_user_uuid = user["id"]
    if intra_extension_uuid:
        post_data = {"subject_id": demo_user_uuid}
        get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(
            intra_extension_uuid), post_data=post_data, authtoken=True)
    return demo_user_uuid

class IntraExtensionsTest(unittest.TestCase):

    def setUp(self):
        post = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "id": "Default"
                            },
                            "name": "admin",
                            "password": "nomoresecrete"
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {
                            "id": "Default"
                        },
                        "name": "demo"
                    }
                }
            }
        }
        data = get_url("/v3/auth/tokens", post_data=post)
        self.assertIn("token", data)

    def tearDown(self):
        pass

    def test_create_intra_extensions(self):
        data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
        self.assertIn("intra_extensions", data)
        data = get_url("/v3/OS-MOON/authz_policies", authtoken=True)
        self.assertIn("authz_policies", data)
        for model in data["authz_policies"]:
            # Create a new intra_extension
            new_ie = {
                "name": "new_intra_extension",
                "description": "new_intra_extension",
                "policymodel": model
            }
            data = get_url("/v3/OS-MOON/intra_extensions/", post_data=new_ie, authtoken=True)
            for key in [u'model', u'id', u'name', u'description']:
                self.assertIn(key, data)
            ie_id = data["id"]
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertIn(ie_id, data["intra_extensions"])

            # Get all subjects
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(ie_id), authtoken=True)
            self.assertIn("subjects", data)
            self.assertIs(type(data["subjects"]), dict)

            # Get all objects
            data = get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(ie_id), authtoken=True)
            self.assertIn("objects", data)
            self.assertIsInstance(data["objects"], dict)

            # Get all actions
            data = get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(ie_id), authtoken=True)
            self.assertIn("actions", data)
            self.assertIsInstance(data["actions"], dict)

            # # get current tenant
            # data = get_url("/v3/OS-MOON/intra_extensions/{}/tenant".format(ie_id), authtoken=True)
            # self.assertIn("tenant", data)
            # self.assertIn(type(data["tenant"]), (str, unicode))
            #
            # # set current tenant
            # tenants = get_url("/v3/projects", authtoken=True)["projects"]
            # post_data = {"tenant_id": ""}
            # for tenant in tenants:
            #     if tenant["name"] == "admin":
            #         post_data = {"tenant_id": tenant["id"]}
            #         break
            # data = get_url("/v3/OS-MOON/intra_extensions/{}/tenant".format(ie_id),
            #                post_data=post_data,
            #                authtoken=True)
            # self.assertIn("tenant", data)
            # self.assertIn(type(data["tenant"]), (str, unicode))
            # self.assertEqual(data["tenant"], post_data["tenant_id"])
            #
            # # check current tenant
            # data = get_url("/v3/OS-MOON/intra_extensions/{}/tenant".format(ie_id), authtoken=True)
            # self.assertIn("tenant", data)
            # self.assertIn(type(data["tenant"]), (str, unicode))
            # self.assertEqual(data["tenant"], post_data["tenant_id"])

            # Delete the intra_extension
            data = get_url("/v3/OS-MOON/intra_extensions/{}".format(ie_id), method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertNotIn(ie_id, data["intra_extensions"])

    def test_perimeter_data(self):
        data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
        self.assertIn("intra_extensions", data)
        data = get_url("/v3/OS-MOON/authz_policies", authtoken=True)
        self.assertIn("authz_policies", data)
        for model in data["authz_policies"]:
            # Create a new intra_extension
            new_ie = {
                "name": "new_intra_extension",
                "description": "new_intra_extension",
                "policymodel": model
            }
            data = get_url("/v3/OS-MOON/intra_extensions/", post_data=new_ie, authtoken=True)
            for key in [u'model', u'id', u'name', u'description']:
                self.assertIn(key, data)
            ie_id = data["id"]
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertIn(ie_id, data["intra_extensions"])

            # Get all subjects
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(ie_id), authtoken=True)
            self.assertIn("subjects", data)
            self.assertIs(type(data["subjects"]), dict)
            self.assertTrue(len(data["subjects"]) > 0)

            # Add a new subject
            users = get_url("/v3/users", authtoken=True)["users"]
            demo_user_uuid = None
            for user in users:
                if user["name"] == "demo":
                    demo_user_uuid = user["id"]
                    break
                # if user demo is not present
                if user["name"] == "admin":
                    demo_user_uuid = user["id"]
            post_data = {"subject_id": demo_user_uuid}
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(ie_id), post_data=post_data, authtoken=True)
            self.assertIn("subject", data)
            self.assertIs(type(data["subject"]), dict)
            self.assertEqual(post_data["subject_id"], data["subject"]["uuid"])
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(ie_id), authtoken=True)
            self.assertIn("subjects", data)
            self.assertIsInstance(data["subjects"], dict)
            self.assertIn(post_data["subject_id"], data["subjects"])
            # delete the previous subject
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subjects/{}".format(ie_id, post_data["subject_id"]),
                           method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(ie_id), authtoken=True)
            self.assertIn("subjects", data)
            self.assertIsInstance(data["subjects"], dict)
            self.assertNotIn(post_data["subject_id"], data["subjects"])

            # Get all objects
            data = get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(ie_id), authtoken=True)
            self.assertIn("objects", data)
            self.assertIs(type(data["objects"]), dict)
            self.assertTrue(len(data["objects"]) > 0)

            # Add a new object
            post_data = {"object_id": "my_new_object"}
            data = get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(ie_id), post_data=post_data, authtoken=True)
            self.assertIn("object", data)
            self.assertIsInstance(data["object"], dict)
            self.assertEqual(post_data["object_id"], data["object"]["name"])
            object_id = data["object"]["uuid"]
            data = get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(ie_id), authtoken=True)
            self.assertIn("objects", data)
            self.assertIsInstance(data["objects"], dict)
            self.assertIn(post_data["object_id"], data["objects"].values())

            # delete the previous object
            data = get_url("/v3/OS-MOON/intra_extensions/{}/objects/{}".format(ie_id, object_id),
                           method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(ie_id), authtoken=True)
            self.assertIn("objects", data)
            self.assertIsInstance(data["objects"], dict)
            self.assertNotIn(post_data["object_id"], data["objects"].values())

            # Get all actions
            data = get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(ie_id), authtoken=True)
            self.assertIn("actions", data)
            self.assertIs(type(data["actions"]), dict)
            self.assertTrue(len(data["actions"]) > 0)

            # Add a new action
            post_data = {"action_id": "create2"}
            data = get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(ie_id), post_data=post_data, authtoken=True)
            action_id = data["action"]["uuid"]
            self.assertIn("action", data)
            self.assertIsInstance(data["action"], dict)
            self.assertEqual(post_data["action_id"], data["action"]["name"])
            data = get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(ie_id), authtoken=True)
            self.assertIn("actions", data)
            self.assertIsInstance(data["actions"], dict)
            self.assertIn(post_data["action_id"], data["actions"].values())

            # delete the previous action
            data = get_url("/v3/OS-MOON/intra_extensions/{}/actions/{}".format(ie_id, action_id),
                           method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(ie_id), authtoken=True)
            self.assertIn("actions", data)
            self.assertIsInstance(data["actions"], dict)
            self.assertNotIn(post_data["action_id"], data["actions"])

            # Delete the intra_extension
            data = get_url("/v3/OS-MOON/intra_extensions/{}".format(ie_id), method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertNotIn(ie_id, data["intra_extensions"])

    def test_assignments_data(self):
        data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
        self.assertIn("intra_extensions", data)
        data = get_url("/v3/OS-MOON/authz_policies", authtoken=True)
        self.assertIn("authz_policies", data)
        for model in data["authz_policies"]:
            # Create a new intra_extension
            new_ie = {
                "name": "new_intra_extension",
                "description": "new_intra_extension",
                "policymodel": model
            }
            data = get_url("/v3/OS-MOON/intra_extensions/", post_data=new_ie, authtoken=True)
            for key in [u'model', u'id', u'name', u'description']:
                self.assertIn(key, data)
            ie_id = data["id"]
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertIn(ie_id, data["intra_extensions"])

            # Get all subject_assignments
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_assignments/{}".format(
                ie_id, get_keystone_user(intra_extension_uuid=ie_id)), authtoken=True)
            self.assertIn("subject_category_assignments", data)
            self.assertIs(type(data["subject_category_assignments"]), dict)

            # Add subject_assignments
            # get one subject
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(ie_id), authtoken=True)
            self.assertIn("subjects", data)
            self.assertIs(type(data["subjects"]), dict)
            # subject_id = data["subjects"].keys()[0]
            subject_id = get_keystone_user()
            # get one subject category
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(ie_id), authtoken=True)
            self.assertIn("subject_categories", data)
            self.assertIs(type(data["subject_categories"]), dict)
            subject_category_id = data["subject_categories"].keys()[0]
            # get all subject category scope
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope/{}".format(
                ie_id, subject_category_id), authtoken=True)
            self.assertIn("subject_category_scope", data)
            self.assertIs(type(data["subject_category_scope"]), dict)
            subject_category_scope_id = data["subject_category_scope"][subject_category_id].keys()[0]
            post_data = {
                "subject_id": subject_id,
                "subject_category": subject_category_id,
                "subject_category_scope": subject_category_scope_id
            }
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_assignments".format(ie_id), post_data=post_data, authtoken=True)
            self.assertIn("subject_category_assignments", data)
            self.assertIs(type(data["subject_category_assignments"]), dict)
            self.assertIn(post_data["subject_category"], data["subject_category_assignments"][subject_id])
            self.assertIn(post_data["subject_category"], data["subject_category_assignments"][subject_id])
            self.assertIn(post_data["subject_category_scope"],
                          data["subject_category_assignments"][subject_id][post_data["subject_category"]])
            # data = get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(ie_id), authtoken=True)
            # self.assertIn("subjects", data)
            # self.assertIsInstance(data["subjects"], dict)
            # self.assertIn(post_data["subject_id"], data["subjects"])

            # delete the previous subject assignment
            get_url("/v3/OS-MOON/intra_extensions/{}/subject_assignments/{}/{}/{}".format(
                ie_id,
                post_data["subject_id"],
                post_data["subject_category"],
                post_data["subject_category_scope"],
                ),
                method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_assignments/{}".format(
                ie_id, get_keystone_user()), authtoken=True)
            self.assertIn("subject_category_assignments", data)
            self.assertIs(type(data["subject_category_assignments"]), dict)
            if post_data["subject_category"] in data["subject_category_assignments"][subject_id]:
                if post_data["subject_category"] in data["subject_category_assignments"][subject_id]:
                    self.assertNotIn(post_data["subject_category_scope"],
                          data["subject_category_assignments"][subject_id][post_data["subject_category"]])

            # Get all object_assignments

            # get one object
            post_data = {"object_id": "my_new_object"}
            new_object = get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(ie_id), post_data=post_data, authtoken=True)
            object_id = new_object["object"]["uuid"]

            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_assignments/{}".format(
                ie_id, object_id), authtoken=True)
            self.assertIn("object_category_assignments", data)
            self.assertIsInstance(data["object_category_assignments"], dict)

            # Add object_assignments
            # get one object category
            post_data = {"object_category_id": uuid4().hex}
            object_category = get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            object_category_id = object_category["object_category"]["uuid"]
            # get all object category scope
            post_data = {
                "object_category_id": object_category_id,
                "object_category_scope_id": uuid4().hex
            }
            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            object_category_scope_id = data["object_category_scope"]["uuid"]
            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope/{}".format(
                ie_id, object_category_id), authtoken=True)
            self.assertIn("object_category_scope", data)
            self.assertIs(type(data["object_category_scope"]), dict)
            post_data = {
                "object_id": object_id,
                "object_category": object_category_id,
                "object_category_scope": object_category_scope_id
            }
            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_assignments".format(ie_id), post_data=post_data, authtoken=True)
            self.assertIn("object_category_assignments", data)
            self.assertIs(type(data["object_category_assignments"]), dict)
            self.assertIn(post_data["object_id"], data["object_category_assignments"])
            self.assertIn(post_data["object_category"], data["object_category_assignments"][post_data["object_id"]])
            self.assertIn(post_data["object_category_scope"],
                          data["object_category_assignments"][post_data["object_id"]][post_data["object_category"]])
            data = get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(ie_id), authtoken=True)
            self.assertIn("objects", data)
            self.assertIsInstance(data["objects"], dict)
            self.assertIn(post_data["object_id"], data["objects"])
            # delete the previous object
            data = get_url("/v3/OS-MOON/intra_extensions/{}/objects/{}".format(ie_id, post_data["object_id"]),
                           method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(ie_id), authtoken=True)
            self.assertIn("objects", data)
            self.assertIsInstance(data["objects"], dict)
            self.assertNotIn(post_data["object_id"], data["objects"])

            # Get all actions_assignments

            # get one action
            post_data = {"action_id": "my_new_action"}
            new_object = get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(ie_id), post_data=post_data, authtoken=True)
            action_id = new_object["action"]["uuid"]

            post_data = {"action_category_id": uuid4().hex}
            action_category = get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            action_category_id = action_category["action_category"]["uuid"]

            data = get_url("/v3/OS-MOON/intra_extensions/{}/action_assignments/{}".format(
                ie_id, action_id), authtoken=True)
            self.assertIn("action_category_assignments", data)
            self.assertIsInstance(data["action_category_assignments"], dict)

            # Add action_assignments
            # get one action category
            # data = get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(ie_id), authtoken=True)
            # self.assertIn("action_categories", data)
            # self.assertIs(type(data["action_categories"]), dict)
            # action_category_id = data["action_categories"][0]
            # get all action category scope
            post_data = {
                "action_category_id": action_category_id,
                "action_category_scope_id": uuid4().hex
            }
            data = get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            action_category_scope_id = data["action_category_scope"]["uuid"]
            data = get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope/{}".format(
                ie_id, action_category_id), authtoken=True)
            self.assertIn("action_category_scope", data)
            self.assertIs(type(data["action_category_scope"]), dict)
            # action_category_scope_id = data["action_category_scope"][action_category_id].keys()[0]
            post_data = {
                "action_id": action_id,
                "action_category": action_category_id,
                "action_category_scope": action_category_scope_id
            }
            data = get_url("/v3/OS-MOON/intra_extensions/{}/action_assignments".format(ie_id), post_data=post_data, authtoken=True)
            self.assertIn("action_category_assignments", data)
            self.assertIs(type(data["action_category_assignments"]), dict)
            self.assertIn(post_data["action_id"], data["action_category_assignments"])
            self.assertIn(post_data["action_category"], data["action_category_assignments"][post_data["action_id"]])
            self.assertIn(post_data["action_category_scope"],
                          data["action_category_assignments"][post_data["action_id"]][post_data["action_category"]])
            data = get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(ie_id), authtoken=True)
            self.assertIn("actions", data)
            self.assertIsInstance(data["actions"], dict)
            self.assertIn(post_data["action_id"], data["actions"])
            # delete the previous action
            data = get_url("/v3/OS-MOON/intra_extensions/{}/actions/{}".format(ie_id, post_data["action_id"]),
                           method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(ie_id), authtoken=True)
            self.assertIn("actions", data)
            self.assertIsInstance(data["actions"], dict)
            self.assertNotIn(post_data["action_id"], data["actions"])

            # Delete the intra_extension
            get_url("/v3/OS-MOON/intra_extensions/{}".format(ie_id), method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertNotIn(ie_id, data["intra_extensions"])

    def test_metadata_data(self):
        data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
        self.assertIn("intra_extensions", data)
        data = get_url("/v3/OS-MOON/authz_policies", authtoken=True)
        self.assertIn("authz_policies", data)
        for model in data["authz_policies"]:
            # Create a new intra_extension
            new_ie = {
                "name": "new_intra_extension",
                "description": "new_intra_extension",
                "policymodel": model
            }
            data = get_url("/v3/OS-MOON/intra_extensions/", post_data=new_ie, authtoken=True)
            for key in [u'model', u'id', u'name', u'description']:
                self.assertIn(key, data)
            ie_id = data["id"]
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertIn(ie_id, data["intra_extensions"])

            # Get all subject_categories
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(ie_id), authtoken=True)
            self.assertIn("subject_categories", data)
            self.assertIs(type(data["subject_categories"]), dict)

            # Add a new subject_category
            post_data = {"subject_category_id": uuid4().hex}
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            self.assertIn("subject_category", data)
            self.assertIsInstance(data["subject_category"], dict)
            self.assertEqual(post_data["subject_category_id"], data["subject_category"]["name"])
            subject_category_id = data["subject_category"]["uuid"]
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(ie_id), authtoken=True)
            self.assertIn("subject_categories", data)
            self.assertIsInstance(data["subject_categories"], dict)
            self.assertIn(post_data["subject_category_id"], data["subject_categories"].values())
            # delete the previous subject_category
            get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories/{}".format(ie_id,
                                                                                   subject_category_id),
                    method="DELETE",
                    authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(ie_id), authtoken=True)
            self.assertIn("subject_categories", data)
            self.assertIsInstance(data["subject_categories"], dict)
            self.assertNotIn(post_data["subject_category_id"], data["subject_categories"].values())

            # Get all object_categories
            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(ie_id), authtoken=True)
            self.assertIn("object_categories", data)
            self.assertIsInstance(data["object_categories"], dict)

            # Add a new object_category
            post_data = {"object_category_id": uuid4().hex}
            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            self.assertIn("object_category", data)
            self.assertIsInstance(data["object_category"], dict)
            self.assertIn(post_data["object_category_id"], data["object_category"]["name"])
            object_category_id = data["object_category"]["uuid"]
            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(ie_id), authtoken=True)
            self.assertIn("object_categories", data)
            self.assertIsInstance(data["object_categories"], dict)
            self.assertIn(post_data["object_category_id"], data["object_categories"].values())
            # delete the previous subject_category
            get_url("/v3/OS-MOON/intra_extensions/{}/object_categories/{}".format(ie_id,
                                                                                  object_category_id),
                    method="DELETE",
                    authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(ie_id), authtoken=True)
            self.assertIn("object_categories", data)
            self.assertIsInstance(data["object_categories"], dict)
            self.assertNotIn(post_data["object_category_id"], data["object_categories"].values())

            # Get all action_categories
            data = get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(ie_id), authtoken=True)
            self.assertIn("action_categories", data)
            self.assertIsInstance(data["action_categories"], dict)

            # Add a new action_category
            post_data = {"action_category_id": uuid4().hex}
            data = get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            self.assertIn("action_category", data)
            self.assertIsInstance(data["action_category"], dict)
            self.assertIn(post_data["action_category_id"], data["action_category"]["name"])
            action_category_id = data["action_category"]["uuid"]
            data = get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(ie_id), authtoken=True)
            self.assertIn("action_categories", data)
            self.assertIsInstance(data["action_categories"], dict)
            self.assertIn(post_data["action_category_id"], data["action_categories"].values())
            # delete the previous subject_category
            get_url("/v3/OS-MOON/intra_extensions/{}/action_categories/{}".format(ie_id,
                                                                                  action_category_id),
                    method="DELETE",
                    authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(ie_id), authtoken=True)
            self.assertIn("action_categories", data)
            self.assertIsInstance(data["action_categories"], dict)
            self.assertNotIn(post_data["action_category_id"], data["action_categories"].values())

            # Delete the intra_extension
            get_url("/v3/OS-MOON/intra_extensions/{}".format(ie_id), method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertNotIn(ie_id, data["intra_extensions"])

    def test_scope_data(self):
        data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
        self.assertIn("intra_extensions", data)
        data = get_url("/v3/OS-MOON/authz_policies", authtoken=True)
        self.assertIn("authz_policies", data)
        for model in data["authz_policies"]:
            # Create a new intra_extension
            new_ie = {
                "name": "new_intra_extension",
                "description": "new_intra_extension",
                "policymodel": model
            }
            data = get_url("/v3/OS-MOON/intra_extensions/", post_data=new_ie, authtoken=True)
            for key in [u'model', u'id', u'name', u'description']:
                self.assertIn(key, data)
            ie_id = data["id"]
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertIn(ie_id, data["intra_extensions"])

            # Get all subject_category_scope
            categories = get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(ie_id), authtoken=True)
            for category in categories["subject_categories"]:
                data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope/{}".format(
                    ie_id, category), authtoken=True)
                self.assertIn("subject_category_scope", data)
                self.assertIs(type(data["subject_category_scope"]), dict)

                # Add a new subject_category_scope
                post_data = {
                    "subject_category_id": category,
                    "subject_category_scope_id": uuid4().hex
                }
                data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope".format(ie_id),
                               post_data=post_data,
                               authtoken=True)
                self.assertIn("subject_category_scope", data)
                self.assertIsInstance(data["subject_category_scope"], dict)
                self.assertEqual(post_data["subject_category_scope_id"], data["subject_category_scope"]["name"])
                data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope/{}".format(
                    ie_id, category), authtoken=True)
                self.assertIn("subject_category_scope", data)
                self.assertIsInstance(data["subject_category_scope"], dict)
                self.assertIn(post_data["subject_category_id"], data["subject_category_scope"])
                self.assertIn(post_data["subject_category_scope_id"],
                              data["subject_category_scope"][category].values())
                # delete the previous subject_category_scope
                get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope/{}/{}".format(
                    ie_id,
                    post_data["subject_category_id"],
                    post_data["subject_category_scope_id"]),
                    method="DELETE",
                    authtoken=True)
                data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope/{}".format(
                    ie_id, category), authtoken=True)
                self.assertIn("subject_category_scope", data)
                self.assertIsInstance(data["subject_category_scope"], dict)
                self.assertIn(post_data["subject_category_id"], data["subject_category_scope"])
                self.assertNotIn(post_data["subject_category_scope_id"],
                                 data["subject_category_scope"][post_data["subject_category_id"]])

            # Get all object_category_scope
            # get object_categories
            categories = get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(ie_id), authtoken=True)
            for category in categories["object_categories"]:
                post_data = {
                    "object_category_id": category,
                    "object_category_scope_id": uuid4().hex
                }
                data = get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope".format(ie_id),
                               post_data=post_data,
                               authtoken=True)
                self.assertIn("object_category_scope", data)
                self.assertIsInstance(data["object_category_scope"], dict)
                self.assertEqual(post_data["object_category_scope_id"], data["object_category_scope"]["name"])
                data = get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope/{}".format(
                    ie_id, category), authtoken=True)
                self.assertIn("object_category_scope", data)
                self.assertIsInstance(data["object_category_scope"], dict)
                self.assertIn(post_data["object_category_id"], data["object_category_scope"])
                self.assertIn(post_data["object_category_scope_id"],
                              data["object_category_scope"][category].values())
                # delete the previous object_category_scope
                get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope/{}/{}".format(
                    ie_id,
                    post_data["object_category_id"],
                    post_data["object_category_scope_id"]),
                    method="DELETE",
                    authtoken=True)
                data = get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope/{}".format(
                    ie_id, category), authtoken=True)
                self.assertIn("object_category_scope", data)
                self.assertIsInstance(data["object_category_scope"], dict)
                self.assertIn(post_data["object_category_id"], data["object_category_scope"])
                self.assertNotIn(post_data["object_category_scope_id"],
                                 data["object_category_scope"][post_data["object_category_id"]])

            # Get all action_category_scope
            categories = get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(ie_id), authtoken=True)
            print(categories)
            for category in categories["action_categories"]:
                print(category)
                data = get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope/{}".format(
                    ie_id, category), authtoken=True)
                self.assertIn("action_category_scope", data)
                self.assertIsInstance(data["action_category_scope"], dict)

                # Add a new action_category_scope
                post_data = {
                    "action_category_id": category,
                    "action_category_scope_id": uuid4().hex
                }
                data = get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope".format(ie_id),
                               post_data=post_data,
                               authtoken=True)
                self.assertIn("action_category_scope", data)
                self.assertIsInstance(data["action_category_scope"], dict)
                self.assertEqual(post_data["action_category_scope_id"], data["action_category_scope"]["name"])
                data = get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope/{}".format(
                    ie_id, category), authtoken=True)
                self.assertIn("action_category_scope", data)
                self.assertIsInstance(data["action_category_scope"], dict)
                self.assertIn(post_data["action_category_id"], data["action_category_scope"])
                self.assertIn(post_data["action_category_scope_id"],
                              data["action_category_scope"][category].values())
                # delete the previous action_category_scope
                get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope/{}/{}".format(
                    ie_id,
                    post_data["action_category_id"],
                    post_data["action_category_scope_id"]),
                    method="DELETE",
                    authtoken=True)
                data = get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope/{}".format(
                    ie_id, category), authtoken=True)
                self.assertIn("action_category_scope", data)
                self.assertIsInstance(data["action_category_scope"], dict)
                self.assertIn(post_data["action_category_id"], data["action_category_scope"])
                self.assertNotIn(post_data["action_category_scope_id"],
                                 data["action_category_scope"][post_data["action_category_id"]])

            # Delete the intra_extension
            get_url("/v3/OS-MOON/intra_extensions/{}".format(ie_id), method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertNotIn(ie_id, data["intra_extensions"])

    def test_metarule_data(self):
        data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
        self.assertIn("intra_extensions", data)
        data = get_url("/v3/OS-MOON/authz_policies", authtoken=True)
        self.assertIn("authz_policies", data)
        for model in data["authz_policies"]:
            # Create a new intra_extension
            new_ie = {
                "name": "new_intra_extension",
                "description": "new_intra_extension",
                "policymodel": model
            }
            data = get_url("/v3/OS-MOON/intra_extensions/", post_data=new_ie, authtoken=True)
            for key in [u'model', u'id', u'name', u'description']:
                self.assertIn(key, data)
            ie_id = data["id"]
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertIn(ie_id, data["intra_extensions"])

            # Get all aggregation_algorithms
            data = get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithms".format(ie_id), authtoken=True)
            self.assertIn("aggregation_algorithms", data)
            self.assertIs(type(data["aggregation_algorithms"]), list)
            aggregation_algorithms = data["aggregation_algorithms"]

            # Get all sub_meta_rule_relations
            data = get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rule_relations".format(ie_id), authtoken=True)
            self.assertIn("sub_meta_rule_relations", data)
            self.assertIs(type(data["sub_meta_rule_relations"]), list)
            sub_meta_rule_relations = data["sub_meta_rule_relations"]

            # Get current aggregation_algorithm
            data = get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithm".format(ie_id), authtoken=True)
            self.assertIn("aggregation", data)
            self.assertIn(type(data["aggregation"]), (str, unicode))
            aggregation_algorithm = data["aggregation"]

            # Set current aggregation_algorithm
            post_data = {"aggregation_algorithm": ""}
            for _algo in aggregation_algorithms:
                if _algo != aggregation_algorithm:
                    post_data = {"aggregation_algorithm": _algo}
            data = get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithm".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            self.assertIn("aggregation", data)
            self.assertIn(type(data["aggregation"]), (str, unicode))
            self.assertEqual(post_data["aggregation_algorithm"], data["aggregation"])
            new_aggregation_algorithm = data["aggregation"]
            data = get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithm".format(ie_id), authtoken=True)
            self.assertIn("aggregation", data)
            self.assertIn(type(data["aggregation"]), (str, unicode))
            self.assertEqual(post_data["aggregation_algorithm"], new_aggregation_algorithm)
            # Get back to the old value
            post_data = {"aggregation_algorithm": aggregation_algorithm}
            data = get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithm".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            self.assertIn("aggregation", data)
            self.assertIn(type(data["aggregation"]), (str, unicode))
            self.assertEqual(post_data["aggregation_algorithm"], aggregation_algorithm)

            # Get current sub_meta_rule
            data = get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rule".format(ie_id), authtoken=True)
            self.assertIn("sub_meta_rules", data)
            self.assertIs(type(data["sub_meta_rules"]), dict)
            self.assertGreater(len(data["sub_meta_rules"].keys()), 0)
            relation = data["sub_meta_rules"].keys()[0]
            new_relation = ""
            self.assertIn(relation, sub_meta_rule_relations)
            sub_meta_rule = data["sub_meta_rules"]
            post_data = dict()
            for _relation in sub_meta_rule_relations:
                if _relation != data["sub_meta_rules"].keys()[0]:
                    post_data[_relation] = copy.deepcopy(sub_meta_rule[relation])
                    post_data[_relation]["relation"] = _relation
                    new_relation = _relation
                    break
            # Add a new subject category
            subject_category = uuid4().hex
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(ie_id), 
                           post_data={"subject_category_id": subject_category},
                           authtoken=True)
            self.assertIn("subject_category", data)
            self.assertIsInstance(data["subject_category"], dict)
            self.assertIn(subject_category, data["subject_category"].values())
            subject_category_id = data["subject_category"]['uuid']
            # Add a new object category
            object_category = uuid4().hex
            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(ie_id), 
                           post_data={"object_category_id": object_category},
                           authtoken=True)
            self.assertIn("object_category", data)
            self.assertIsInstance(data["object_category"], dict)
            self.assertIn(object_category, data["object_category"].values())
            object_category_id = data["object_category"]['uuid']
            # Add a new action category
            action_category = uuid4().hex
            data = get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(ie_id), 
                           post_data={"action_category_id": action_category},
                           authtoken=True)
            self.assertIn("action_category", data)
            self.assertIsInstance(data["action_category"], dict)
            self.assertIn(action_category, data["action_category"].values())
            action_category_id = data["action_category"]['uuid']
            # Modify the post_data to add new categories
            post_data[new_relation]["subject_categories"].append(subject_category_id)
            post_data[new_relation]["object_categories"].append(object_category_id)
            post_data[new_relation]["action_categories"].append(action_category_id)
            data = get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rule".format(ie_id),
                           post_data=post_data,
                           authtoken=True)
            self.assertIn("sub_meta_rules", data)
            self.assertIs(type(data["sub_meta_rules"]), dict)
            self.assertGreater(len(data["sub_meta_rules"].keys()), 0)
            self.assertEqual(new_relation, data["sub_meta_rules"].keys()[0])
            self.assertIn(subject_category_id, data["sub_meta_rules"][new_relation]["subject_categories"])
            self.assertIn(object_category_id, data["sub_meta_rules"][new_relation]["object_categories"])
            self.assertIn(action_category_id, data["sub_meta_rules"][new_relation]["action_categories"])
            self.assertEqual(new_relation, data["sub_meta_rules"][new_relation]["relation"])

            # Delete the intra_extension
            data = get_url("/v3/OS-MOON/intra_extensions/{}".format(ie_id), method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertNotIn(ie_id, data["intra_extensions"])

    def test_rules_data(self):
        data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
        self.assertIn("intra_extensions", data)
        data = get_url("/v3/OS-MOON/authz_policies", authtoken=True)
        self.assertIn("authz_policies", data)
        for model in data["authz_policies"]:
            # Create a new intra_extension
            print("=====> {}".format(model))
            new_ie = {
                "name": "new_intra_extension",
                "description": "new_intra_extension",
                "policymodel": model
            }
            data = get_url("/v3/OS-MOON/intra_extensions/", post_data=new_ie, authtoken=True)
            for key in [u'model', u'id', u'name', u'description']:
                self.assertIn(key, data)
            ie_id = data["id"]
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertIn(ie_id, data["intra_extensions"])

            # Get all sub_meta_rule_relations
            data = get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rule_relations".format(ie_id), authtoken=True)
            self.assertIn("sub_meta_rule_relations", data)
            self.assertIs(type(data["sub_meta_rule_relations"]), list)
            sub_meta_rule_relations = data["sub_meta_rule_relations"]

            # Get current sub_meta_rule
            data = get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rule".format(ie_id), authtoken=True)
            self.assertIn("sub_meta_rules", data)
            self.assertIs(type(data["sub_meta_rules"]), dict)
            self.assertGreater(len(data["sub_meta_rules"].keys()), 0)
            relation = data["sub_meta_rules"].keys()[0]
            self.assertIn(relation, sub_meta_rule_relations)
            sub_meta_rule = data["sub_meta_rules"]
            sub_meta_rule_length = dict()
            sub_meta_rule_length[relation] = len(data["sub_meta_rules"][relation]["subject_categories"]) + \
                len(data["sub_meta_rules"][relation]["object_categories"]) + \
                len(data["sub_meta_rules"][relation]["action_categories"]) +1

            # Get all rules
            data = get_url("/v3/OS-MOON/intra_extensions/{}/sub_rules".format(ie_id), authtoken=True)
            self.assertIn("rules", data)
            self.assertIs(type(data["rules"]), dict)
            length = dict()
            for key in data["rules"]:
                self.assertIn(key, sub_meta_rule_relations)
                self.assertGreater(len(data["rules"][key]), 0)
                self.assertIs(type(data["rules"][key]), list)
                for sub_rule in data["rules"][key]:
                    self.assertEqual(len(sub_rule), sub_meta_rule_length[key])
                    length[key] = len(data["rules"][key])

            # Get one value of subject category scope
            # FIXME: a better test would be to add a new value in scope and then add it to a new sub-rule
            categories = get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(ie_id),
                                 authtoken=True)["subject_categories"].keys()
            data = get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope/{}".format(
                ie_id, categories[0]), authtoken=True)
            self.assertIn("subject_category_scope", data)
            self.assertIs(type(data["subject_category_scope"]), dict)
            subject_category = categories.pop()
            subject_value = data["subject_category_scope"][subject_category].keys()[0]
            # Get one value of object category scope
            # FIXME: a better test would be to add a new value in scope and then add it to a new sub-rule
            categories = get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(ie_id),
                                 authtoken=True)["object_categories"].keys()
            data = get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope/{}".format(
                ie_id, categories[0]), authtoken=True)
            self.assertIn("object_category_scope", data)
            self.assertIs(type(data["object_category_scope"]), dict)
            object_category = categories.pop()
            object_value = data["object_category_scope"][object_category].keys()[0]
            # Get one or more values in action category scope
            _sub_meta_action_value = list()
            for _sub_meta_cat in sub_meta_rule[relation]["action_categories"]:
                data = get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope/{}".format(
                               ie_id, _sub_meta_cat), authtoken=True)
                action_value = data["action_category_scope"][_sub_meta_cat].keys()[0]
                _sub_meta_action_value.append(action_value)
            _sub_meta_rules = list()
            _sub_meta_rules.append(subject_value)
            _sub_meta_rules.extend(_sub_meta_action_value)
            _sub_meta_rules.append(object_value)
            # Must append True because the sub_rule need a boolean to know if it is a positive or a negative value
            _sub_meta_rules.append(True)
            post_data = {
                "rule": _sub_meta_rules,
                "relation": "relation_super"
            }
            # Add a new sub-rule
            data = get_url("/v3/OS-MOON/intra_extensions/{}/sub_rules".format(ie_id),
                           post_data=post_data, authtoken=True)
            self.assertIn("rules", data)
            self.assertIs(type(data["rules"]), dict)
            for key in data["rules"]:
                self.assertIn(key, sub_meta_rule_relations)
                self.assertGreater(len(data["rules"][key]), 0)
                for sub_rule in data["rules"][key]:
                    self.assertEqual(len(sub_rule), sub_meta_rule_length[key])
                    if key == "relation_super":
                        self.assertEqual(len(data["rules"][key]), length[key]+1)
                    else:
                        self.assertEqual(len(data["rules"][key]), length[key])

            # Delete the new sub-rule
            data = get_url("/v3/OS-MOON/intra_extensions/{}/sub_rules/{rel}/{rule}".format(
                ie_id,
                rel=post_data["relation"],
                rule="+".join(map(lambda x: str(x), post_data["rule"]))),
                method="DELETE", authtoken=True)
            self.assertIn("rules", data)
            self.assertIs(type(data["rules"]), dict)
            for key in data["rules"]:
                self.assertIn(key, sub_meta_rule_relations)
                self.assertGreater(len(data["rules"][key]), 0)
                for sub_rule in data["rules"][key]:
                    if key == "relation_super":
                        self.assertEqual(len(data["rules"][key]), length[key])
                    else:
                        self.assertEqual(len(data["rules"][key]), length[key])

            # Delete the intra_extension
            data = get_url("/v3/OS-MOON/intra_extensions/{}".format(ie_id), method="DELETE", authtoken=True)
            data = get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
            self.assertNotIn(ie_id, data["intra_extensions"])


if __name__ == "__main__":
    unittest.main()
