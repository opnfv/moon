# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from locust import TaskSet, task
import logging
import json

LOGGER = logging.getLogger("locust")


class AuthzPipelineRequests(TaskSet):
    token = ""
    moon_errors = 0
    moon_requests = 0
    stats_filename = "/tmp/perf_stats.log"

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.moon_errors = []

    def __del__(self):
        """ on_stop is called when the TaskSet is stopping """
        stats = {}
        try:
            stats = json.loads(open(self.stats_filename).read())
        except Exception:
            pass
        _num = stats.get("errors", 0)
        _num += len(self.moon_errors)
        _total = stats.get("total", 0)
        _total += self.moon_requests
        _list = stats.get("list", [])
        _list.extend(self.moon_errors)
        _percent = _num * 100 / _total
        json.dump({"errors": _num, "total": _total,
                   "percentage": "{0:.2f}".format(_percent),
                   "list": _list},
                  open(self.stats_filename, "w"), indent=4)

    def get(self, url, status_code=200):
        with self.client.get(url, catch_response=True) as response:
            self.moon_requests += 1
            if response.status_code != status_code:
                self.moon_errors.append((url, f"{response.status_code}/{status_code}"))
            response.success()

    @task(10)
    def authz_ok1(self):
        url = "/authz/{}/{}/{}".format(
            "admin", "vm1", "use_image"
        )
        self.get(url)

    @task(10)
    def authz_ok2(self):
        url = "/authz/{}/{}/{}".format(
            "admin", "vm1", "get_images"
        )
        self.get(url)

    @task(10)
    def authz_ok3(self):
        url = "/authz/{}/{}/{}".format(
            "admin", "vm1", "set_image"
        )
        self.get(url)

    @task(10)
    def authz_ok4(self):
        url = "/authz/{}/{}/{}".format(
            "demo", "vm1", "set_image"
        )
        self.get(url)

    @task(10)
    def authz_ok5(self):
        url = "/authz/{}/{}/{}".format(
            "demo", "vm1", "get_images"
        )
        self.get(url)

    @task(10)
    def authz_rule_ko(self):
        url = "/authz/{}/{}/{}".format("demo", "vm1", "use_image")
        self.get(url, 403)

    @task(10)
    def authz_subject_ko(self):
        url = "/authz/{}/{}/{}".format("admins", "vm1", "use_image")
        self.get(url, 403)

    @task(10)
    def authz_object_ko(self):
        url = "/authz/{}/{}/{}".format("admin", "vm4", "use_image")
        self.get(url, 403)

    @task(10)
    def authz_action_ko(self):
        url = "/authz/{}/{}/{}".format("admin", "vm1", "use_images")
        self.get(url, 403)

    @task(1)
    def status(self):
        self.client.get("/status/")


