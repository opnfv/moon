# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import json
from locust import TaskSet, task
from uuid import uuid4
import utils


class ObjectRequests(TaskSet):
    token = ""

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        utils.login(self)

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        utils.logout(self)

    @task(10)
    def objects(self):
        policy_id = utils.create_policy(self.client, self.token)
        self.client.get("/objects", headers={"X-Api-Key": self.token})
        perimeter_name = "test_object_" + str(uuid4())
        req = self.client.post("/policies/{}/objects".format(policy_id),
                               headers={"X-Api-Key": self.token},
                               data={
                                    "name": perimeter_name,
                                    "description": "locust test",
                                })
        content = json.loads(req.content.decode("utf-8"))
        subject_id = None
        for subject_id, subject_value in content.get("objects", {}).items():
            if subject_value.get("name") == perimeter_name:
                break
        self.client.delete("/policies/{}/objects/{}".format(policy_id, subject_id),
                           headers={"X-Api-Key": self.token})
        utils.delete_policy(self.client, self.token, policy_id)

    @task(1)
    def status(self):
        self.client.get("/status", headers={"X-Api-Key": self.token})


