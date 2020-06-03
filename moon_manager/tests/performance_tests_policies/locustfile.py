# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from locust import HttpLocust, TaskSet
import subjects
import objects
import actions
import meta_rules


class MoonRequests(TaskSet):
    tasks = {
        subjects.SubjectRequests: 10,
        objects.ObjectRequests: 10,
        actions.ActionRequests: 10,
        meta_rules.MetaRulesRequests: 5
    }


class MoonUser(HttpLocust):
    task_set = MoonRequests
    min_wait = 100
    max_wait = 1000
