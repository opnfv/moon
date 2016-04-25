# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import unittest
import json
import requests


class AuthTest(unittest.TestCase):

    def setUp(self):
        self.data_auth = {
            "username": "",
            "password": ""
        }

    def tearDown(self):
        pass

    def test_authz(self):
        self.data_auth['username'] = 'admin'
        self.data_auth['password'] = ''
        req = requests.post("http://localhost:5000/moon/auth/tokens",
                            json=self.data_auth,
                            headers={"Content-Type": "application/json"}
                            )
        self.assertIn(req.status_code, (200, 201))
        result = req.json()
        self.assertIn("token", result.keys())
        self.assertEqual(result["token"], None)

        self.data_auth['username'] = 'admin'
        self.data_auth['password'] = 'nomoresecrete'
        req = requests.post("http://localhost:5000/moon/auth/tokens",
                            json=self.data_auth,
                            headers={"Content-Type": "application/json"}
                            )
        self.assertIn(req.status_code, (200, 201))
        result = req.json()
        self.assertIn("token", result.keys())
        self.assertNotEqual(result["token"], None)

if __name__ == "__main__":
    unittest.main()


