# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import json


def login(taskset):
    req = taskset.client.get("/auth", auth=("admin", "admin"))
    taskset.token = req.content.decode("utf-8").strip('"')


def logout(taskset):
    pass


def log(msg):
    open("/tmp/tests.log", 'a').write(str(msg) + "\n")


def import_policy(client, token):
    import_data = open("policy_rbac.json").read()
    req = client.post("/import", headers={"X-Api-Key": token}, data=json.loads(import_data))
    print(req)
    content = json.loads(req.content.decode("utf-8"))
    for policy_key, policy_value in content.get("policies", {}).items():
        if policy_value.get("name") == "Policy for Locust":
            return policy_key


def create_pdp(client, token, policy_id, vim_project_id=111111111111):
    req = client.post("/pdp", headers={"X-Api-Key": token}, data={
        "name": "PDP for Locust",
        "vim_project_id": vim_project_id,
        "security_pipeline": [policy_id]
    })
    content = json.loads(req.content.decode("utf-8"))
    for pdp_key, pdp_value in content.get("pdp", {}).items():
        if pdp_value.get("name") == "PDP for Locust":
            return pdp_key


def delete_policy(client, token, policy_id):
    print("deleting Policy {}".format(policy_id))
    client.delete("/policies/{}".format(policy_id), headers={"X-Api-Key": token})


def delete_pdp(client, token, pdp_id):
    print("deleting PDP {}".format(pdp_id))
    client.delete("/pdp/{}".format(pdp_id), headers={"X-Api-Key": token})


