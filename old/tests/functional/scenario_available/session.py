
pdp_name = "pdp1"
policy_name = "Session policy example"
model_name = "Session"
policy_genre = "session"

subjects = {"user0": "", "user1": "", }
objects = {"admin": "", "employee": "", }
actions = {"activate": "", "deactivate": ""}

subject_categories = {"subjectid": "", }
object_categories = {"role": "", }
action_categories = {"session-action": "", }

subject_data = {"subjectid": {"user0": "", "user1": ""}}
object_data = {"role": {"admin": "", "employee": "", "*": ""}}
action_data = {"session-action": {"activate": "", "deactivate": "", "*": ""}}

subject_assignments = {"user0": ({"subjectid": "user0"}, ), "user1": ({"subjectid": "user1"}, ), }
object_assignments = {"admin": ({"role": "admin"}, {"role": "*"}),
                      "employee": ({"role": "employee"}, {"role": "employee"})
                      }
action_assignments = {"activate": ({"session-action": "activate"}, {"session-action": "*"}, ),
                      "deactivate": ({"session-action": "deactivate"}, {"session-action": "*"}, )
                      }

meta_rule = {
    "session": {"id": "", "value": ("subjectid", "role", "session-action")},
}

rules = {
    "session": (
        {
            "rule": ("user0", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user1", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "delete",
                        "target": "rbac:role:employee"  # delete the role employee from the current user
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
    )
}


