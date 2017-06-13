
pdp_name = "pdp1"
policy_name = "Session policy example"
model_name = "Session"
policy_genre = "session"

subjects = {
    "user0": "",
    "user1": "",
    "user2": "",
    "user3": "",
    "user4": "",
    "user5": "",
    "user6": "",
    "user7": "",
    "user8": "",
    "user9": "",
    "user10": "",
    "user11": "",
    "user12": "",
    "user13": "",
    "user14": "",
    "user15": "",
    "user16": "",
    "user17": "",
    "user18": "",
    "user19": "",
}
objects = {"admin": "", "employee": "", "dev1": "", "dev3": "",
           "dev4": "", "dev5": "", "dev6": "", "dev7": "", "dev8": ""}
actions = {"activate": "", "deactivate": ""}

subject_categories = {"subjectid": "", }
object_categories = {"role": "", }
action_categories = {"session-action": "", }

subject_data = {"subjectid": {
    "user0": "",
    "user1": "",
    "user2": "",
    "user3": "",
    "user4": "",
    "user5": "",
    "user6": "",
    "user7": "",
    "user8": "",
    "user9": "",
    "user10": "",
    "user11": "",
    "user12": "",
    "user13": "",
    "user14": "",
    "user15": "",
    "user16": "",
    "user17": "",
    "user18": "",
    "user19": "",
}}
object_data = {"role": {
    "admin": "",
    "employee": "",
    "dev1": "",
    "dev2": "",
    "dev3": "",
    "dev4": "",
    "dev5": "",
    "dev6": "",
    "dev7": "",
    "dev8": "",
    "*": ""
}}
action_data = {"session-action": {"activate": "", "deactivate": "", "*": ""}}

subject_assignments = {
    "user0": ({"subjectid": "user0"}, ),
    "user1": ({"subjectid": "user1"}, ),
    "user2": ({"subjectid": "user2"}, ),
    "user3": ({"subjectid": "user3"}, ),
    "user4": ({"subjectid": "user4"}, ),
    "user5": ({"subjectid": "user5"}, ),
    "user6": ({"subjectid": "user6"}, ),
    "user7": ({"subjectid": "user7"}, ),
    "user8": ({"subjectid": "user8"}, ),
    "user9": ({"subjectid": "user9"}, ),
    "user10": ({"subjectid": "user10"}, ),
    "user11": ({"subjectid": "user11"}, ),
    "user12": ({"subjectid": "user12"}, ),
    "user13": ({"subjectid": "user13"}, ),
    "user14": ({"subjectid": "user14"}, ),
    "user15": ({"subjectid": "user15"}, ),
    "user16": ({"subjectid": "user16"}, ),
    "user17": ({"subjectid": "user17"}, ),
    "user18": ({"subjectid": "user18"}, ),
    "user19": ({"subjectid": "user19"}, ),
}
object_assignments = {"admin": ({"role": "admin"}, {"role": "*"}),
                      "employee": ({"role": "employee"}, {"role": "*"}),
                      "dev1": ({"role": "employee"}, {"role": "dev1"}, {"role": "*"}),
                      "dev2": ({"role": "employee"}, {"role": "dev2"}, {"role": "*"}),
                      "dev3": ({"role": "employee"}, {"role": "dev3"}, {"role": "*"}),
                      "dev4": ({"role": "employee"}, {"role": "dev4"}, {"role": "*"}),
                      "dev5": ({"role": "employee"}, {"role": "dev5"}, {"role": "*"}),
                      "dev6": ({"role": "employee"}, {"role": "dev6"}, {"role": "*"}),
                      "dev7": ({"role": "employee"}, {"role": "dev7"}, {"role": "*"}),
                      "dev8": ({"role": "employee"}, {"role": "dev8"}, {"role": "*"}),
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
        {
            "rule": ("user2", "employee", "*"),
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
            "rule": ("user2", "dev1", "*"),
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
            "rule": ("user2", "dev2", "*"),
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
            "rule": ("user3", "employee", "*"),
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
            "rule": ("user3", "dev1", "*"),
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
            "rule": ("user3", "dev2", "*"),
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
            "rule": ("user4", "employee", "*"),
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
            "rule": ("user4", "dev1", "*"),
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
            "rule": ("user4", "dev2", "*"),
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
            "rule": ("user5", "employee", "*"),
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
            "rule": ("user5", "dev1", "*"),
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
            "rule": ("user5", "dev2", "*"),
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
            "rule": ("user6", "employee", "*"),
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
            "rule": ("user6", "dev1", "*"),
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
            "rule": ("user6", "dev2", "*"),
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
            "rule": ("user7", "employee", "*"),
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
            "rule": ("user7", "dev1", "*"),
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
            "rule": ("user7", "dev2", "*"),
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
            "rule": ("user8", "employee", "*"),
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
            "rule": ("user8", "dev1", "*"),
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
            "rule": ("user8", "dev2", "*"),
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
            "rule": ("user9", "employee", "*"),
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
            "rule": ("user9", "dev1", "*"),
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
            "rule": ("user9", "dev2", "*"),
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
            "rule": ("user10", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user11", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "delete",
                        "target": "rbac:role:employee"  # delete the role employee from the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user12", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user12", "dev3", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user12", "dev4", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user13", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user13", "dev3", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user13", "dev4", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user14", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user14", "dev3", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user14", "dev4", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user15", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user15", "dev3", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user15", "dev4", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user16", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user16", "dev3", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user16", "dev4", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user17", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user17", "dev3", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user17", "dev4", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user18", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user18", "dev3", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user18", "dev4", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user19", "employee", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user19", "dev3", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
        {
            "rule": ("user19", "dev4", "*"),
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        "target": "rbac:role:admin"  # add the role admin to the current user1
                    }
                },
                {"chain": {"name": "rbac"}}  # chain with the meta_rule named rbac
            )
        },
    )
}


