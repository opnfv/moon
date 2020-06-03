# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import json
from uuid import uuid4


def login(taskset):
    req = taskset.client.get("/auth", auth=("admin", "admin"))
    taskset.token = req.content.decode("utf-8").strip('"')


def logout(taskset):
    pass


def log(msg):
    open("/tmp/tests.log", 'a').write(str(msg) + "\n")


def create_policy(client, token):
    policy_name = "test_policy_" + str(uuid4())
    req = client.post("/policies", headers={"X-Api-Key": token}, data={
            "name": policy_name,
            "description": "locust test policy",
        })
    content = json.loads(req.content.decode("utf-8"))
    for policy_key, policy_value in content.get("policies", {}).items():
        if policy_value.get("name") == policy_name:
            return policy_key


def delete_policy(client, token, policy_id):
    client.delete("/policies/{}".format(policy_id), headers={"X-Api-Key": token})


