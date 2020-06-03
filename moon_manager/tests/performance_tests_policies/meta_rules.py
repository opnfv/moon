# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from locust import TaskSet, task
import json
from uuid import uuid4
import utils


class MetaRulesRequests(TaskSet):
    token = ""

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        utils.login(self)

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        utils.logout(self)

    def create_category(self, otype="subject"):
        self.client.get("/{}_categories".format(otype), headers={"X-Api-Key": self.token})
        category_name = "test_category_" + str(uuid4())
        req = self.client.post("/{}_categories".format(otype),
                               headers={"X-Api-Key": self.token},
                               data={
                                   "name": category_name,
                                   "description": "locust {} category tests".format(otype),
                               })
        content = json.loads(req.content.decode("utf-8"))
        for category_id, category_value in content.get("{}_categories".format(otype), {}).items():
            if category_value.get("name") == category_name:
                return category_id

    def delete_category(self, category_id, otype="subject"):
        self.client.delete("/{}_categories/{}".format(otype, category_id),
                           headers={"X-Api-Key": self.token})

    @task(10)
    def meta_rules(self):
        self.client.get("/meta_rules", headers={"X-Api-Key": self.token})
        subject_category_id = self.create_category("subject")
        object_category_id = self.create_category("object")
        action_category_id = self.create_category("action")
        meta_rule_name = "meta_rule_" + str(uuid4())
        data = {
            "name": meta_rule_name,
            "subject_categories": [subject_category_id],
            "object_categories": [object_category_id],
            "action_categories": [action_category_id]
        }
        req = self.client.post("/meta_rules",
                               headers={"X-Api-Key": self.token,
                                        "Content-Type": "application/json"},
                               data=json.dumps(data)
                               )
        content = json.loads(req.content.decode("utf-8"))
        for meta_rule_id, meta_rule_value in content.get("meta_rules", {}).items():
            if meta_rule_value.get("name") == meta_rule_name:
                self.client.delete("/meta_rules/{}".format(meta_rule_id),
                                   headers={"X-Api-Key": self.token})
                break
        self.delete_category(subject_category_id, "subject")
        self.delete_category(object_category_id, "object")
        self.delete_category(action_category_id, "action")

    @task(1)
    def status(self):
        self.client.get("/status", headers={"X-Api-Key": self.token})


