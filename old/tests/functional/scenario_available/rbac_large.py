
pdp_name = "pdp1"
policy_name = "RBAC policy example"
model_name = "RBAC"
policy_genre = "authz"

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
}
objects = {
    "vm0": "",
    "vm1": "",
    "vm2": "",
    "vm3": "",
    "vm4": "",
    "vm5": "",
    "vm6": "",
    "vm7": "",
    "vm8": "",
    "vm9": "",
}
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

subject_data = {"role": {
    "admin": "", 
    "employee": "", 
    "dev1": "", 
    "dev2": "", 
    "*": ""
}}
object_data = {"id": {
    "vm0": "", 
    "vm1": "", 
    "vm2": "",
    "vm3": "",
    "vm4": "",
    "vm5": "",
    "vm6": "",
    "vm7": "",
    "vm8": "",
    "vm9": "",
    "*": ""
}}
action_data = {"action-type": {
    "vm-read": "", 
    "vm-write": "", 
    "*": ""
}}

subject_assignments = {
    "user0": ({"role": "employee"}, {"role": "*"}), 
    "user1": ({"role": "employee"}, {"role": "*"}),
    "user2": ({"role": "dev1"}, {"role": "*"}),
    "user3": ({"role": "dev1"}, {"role": "*"}),
    "user4": ({"role": "dev1"}, {"role": "*"}),
    "user5": ({"role": "dev1"}, {"role": "*"}),
    "user6": ({"role": "dev2"}, {"role": "*"}),
    "user7": ({"role": "dev2"}, {"role": "*"}),
    "user8": ({"role": "dev2"}, {"role": "*"}),
    "user9": ({"role": "dev2"}, {"role": "*"}),
}
object_assignments = {
    "vm0": ({"id": "vm0"}, {"id": "*"}), 
    "vm1": ({"id": "vm1"}, {"id": "*"}),
    "vm2": ({"id": "vm2"}, {"id": "*"}),
    "vm3": ({"id": "vm3"}, {"id": "*"}),
    "vm4": ({"id": "vm4"}, {"id": "*"}),
    "vm5": ({"id": "vm5"}, {"id": "*"}),
    "vm6": ({"id": "vm6"}, {"id": "*"}),
    "vm7": ({"id": "vm7"}, {"id": "*"}),
    "vm8": ({"id": "vm8"}, {"id": "*"}),
    "vm9": ({"id": "vm9"}, {"id": "*"}),
}
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
    "rbac": (
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
        # Rules for grant all employee to do read actions to all VM except vm0 
        {
            "rule": ("employee", "vm1", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("employee", "vm2", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("employee", "vm3", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("employee", "vm4", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("employee", "vm5", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("employee", "vm6", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("employee", "vm7", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("employee", "vm8", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("employee", "vm9", "vm-read"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        # Rules for grant all dev1 to do read actions to some VM
        {
            "rule": ("dev1", "vm1", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev1", "vm2", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev1", "vm3", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev1", "vm4", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        # Rules for grant all dev2 to do read actions to some VM
        {
            "rule": ("dev2", "vm5", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev2", "vm6", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev2", "vm7", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev2", "vm8", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev2", "vm9", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
    )
}


