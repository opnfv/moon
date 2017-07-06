import random

pdp_name = "pdp1"
policy_name = "Session policy example"
model_name = "Session"
policy_genre = "session"

SUBJECT_NUMBER = 1000
OBJECT_NUMBER = 1000
ROLE_NUMBER = 700

subjects = {}
for _id in range(SUBJECT_NUMBER):
    subjects["user{}".format(_id)] = ""
objects = {"admin": "", }
for _id in range(ROLE_NUMBER):
    objects["role{}".format(_id)] = ""
actions = {"activate": "", "deactivate": ""}

subject_categories = {"subjectid": "", }
object_categories = {"role": "", }
action_categories = {"session-action": "", }

subject_data = {"subjectid": {}}
for _id in range(SUBJECT_NUMBER):
    subject_data["subjectid"]["user{}".format(_id)] = ""

object_data = {"role": {
    "admin": "",
    "*": ""
}}
for _id in range(ROLE_NUMBER):
    object_data["role"]["role{}".format(_id)] = ""
action_data = {"session-action": {"activate": "", "deactivate": "", "*": ""}}

subject_assignments = {}
for _id in range(SUBJECT_NUMBER):
    subject_assignments["user{}".format(_id)] = ({"subjectid": "user{}".format(_id)}, )
object_assignments = {"admin": ({"role": "admin"}, {"role": "*"})}
for _id in range(ROLE_NUMBER):
    _role = "role{}".format(_id)
    object_assignments[_role] = ({"role": _role}, {"role": "*"})
action_assignments = {"activate": ({"session-action": "activate"}, {"session-action": "*"}, ),
                      "deactivate": ({"session-action": "deactivate"}, {"session-action": "*"}, )
                      }

meta_rule = {
    "session": {"id": "", "value": ("subjectid", "role", "session-action")},
}

rules = {
    "session": []
}

for _id in range(SUBJECT_NUMBER):
    _subject = "user{}".format(_id)
    _object = "role{}".format(random.choice(range(ROLE_NUMBER)))
    rules["session"].append({
        "rule": (_subject, _object, "*"),
        "instructions": (
            {
                "update": {
                    "operation": "add",
                    "target": "rbac:role:admin"  # add the role admin to the current user
                }
            },
            {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
        )
    })
