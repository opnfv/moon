import random

pdp_name = "pdp_100"
policy_name = "RBAC policy example 100 users"
model_name = "RBAC"
policy_genre = "authz"

SUBJECT_NUMBER = 100
OBJECT_NUMBER = 100
ROLE_NUMBER = 50

subjects = {}
for _id in range(SUBJECT_NUMBER):
    subjects["user{}".format(_id)] = ""
objects = {}
for _id in range(OBJECT_NUMBER):
    objects["vm{}".format(_id)] = ""
actions = {
    "start": "",
    "stop": "",
    "pause": "",
    "unpause": "",
    "destroy": "",
}

subject_categories = {"role": "", }
object_categories = {"id": "", }
action_categories = {"action-type": "", }

subject_data = {"role": {"admin": "", "*": ""}}
for _id in range(ROLE_NUMBER):
    subject_data["role"]["role{}".format(_id)] = ""
object_data = {"id": {"*": ""}}
for _id in range(OBJECT_NUMBER):
    object_data["id"]["vm{}".format(_id)] = ""
action_data = {"action-type": {
    "vm-read": "",
    "vm-write": "",
    "*": ""
}}

subject_assignments = {}
for _id in range(SUBJECT_NUMBER):
    _role = "role{}".format(random.randrange(ROLE_NUMBER))
    subject_assignments["user{}".format(_id)] = [{"role": _role}, {"role": "*"}]
object_assignments = {"vm0": ({"id": "vm0"}, {"id": "*"}), "vm1": ({"id": "vm1"}, {"id": "*"})}
for _id in range(OBJECT_NUMBER):
    object_assignments["vm{}".format(_id)] = [{"id": "vm{}".format(_id)}, {"id": "*"}]
action_assignments = {
    "start": ({"action-type": "vm-write"}, {"action-type": "*"}),
    "stop": ({"action-type": "vm-write"}, {"action-type": "*"}),
    "pause": ({"action-type": "vm-read"}, {"action-type": "*"}),
    "unpause": ({"action-type": "vm-read"}, {"action-type": "*"}),
    "destroy": ({"action-type": "vm-write"}, {"action-type": "*"}),
}

meta_rule = {
    "rbac": {"id": "", "value": ("role", "id", "action-type")},
}

rules = {
    "rbac": [
        {
            "rule": ("admin", "vm0", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("admin", "vm0", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
    ]
}

for _id in range(SUBJECT_NUMBER):
    _role = "role{}".format(random.randrange(ROLE_NUMBER))
    _vm = "vm{}".format(random.randrange(OBJECT_NUMBER))
    _action = random.choice(list(action_data['action-type'].keys()))
    rules["rbac"].append(
        {
            "rule": (_role, _vm, _action),
            "instructions": (
                {"decision": "grant"},
            )
        },
    )
