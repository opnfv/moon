# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import unittest
import json
import httplib
import time
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


class MappingsTest(unittest.TestCase):

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

    def test_get_tenants(self):
        data = get_url("/v3/OS-MOON/tenants", authtoken=True)
        self.assertIn("tenants", data)
        self.assertIsInstance(data["tenants"], dict)
        print(data)

    def test_add_delete_mapping(self):
        data = get_url("/v3/projects", authtoken=True)
        project_id = None
        for project in data["projects"]:
            if project["name"] == "demo":
                project_id = project["id"]
        data = get_url("/v3/OS-MOON/tenant",
                       post_data={
                           "id": project_id,
                            "name": "tenant1",
                            "authz": "intra_extension_uuid1",
                            "admin": "intra_extension_uuid2"
                       },
                       authtoken=True)
        self.assertIn("tenant", data)
        self.assertIsInstance(data["tenant"], dict)
        uuid = data["tenant"]["id"]
        data = get_url("/v3/OS-MOON/tenants", authtoken=True)
        self.assertIn("tenants", data)
        self.assertIsInstance(data["tenants"], dict)
        print(data)
        data = get_url("/v3/OS-MOON/tenant/{}".format(uuid),
                       method="DELETE",
                       authtoken=True)
        data = get_url("/v3/OS-MOON/tenants", authtoken=True)
        self.assertIn("tenants", data)
        self.assertIsInstance(data["tenants"], dict)
        print(data)

if __name__ == "__main__":
    unittest.main()
