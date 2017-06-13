
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
    "user20": "",
    "user21": "",
    "user22": "",
    "user23": "",
    "user24": "",
    "user25": "",
    "user26": "",
    "user27": "",
    "user28": "",
    "user29": "",
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
    "dev3": "",
    "dev4": "",
    "dev5": "",
    "dev6": "",
    "dev7": "",
    "dev8": "",
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
    "user10": ({"role": "employee"}, {"role": "*"}),
    "user11": ({"role": "employee"}, {"role": "*"}),
    "user12": ({"role": "dev3"}, {"role": "*"}),
    "user13": ({"role": "dev3"}, {"role": "*"}),
    "user14": ({"role": "dev4"}, {"role": "*"}),
    "user15": ({"role": "dev4"}, {"role": "*"}),
    "user16": ({"role": "dev5"}, {"role": "*"}),
    "user17": ({"role": "dev6"}, {"role": "*"}),
    "user18": ({"role": "dev7"}, {"role": "*"}),
    "user19": ({"role": "dev8"}, {"role": "*"}),
    "user20": ({"role": "employee"}, {"role": "*"}),
    "user21": ({"role": "employee"}, {"role": "*"}),
    "user22": ({"role": "dev3"}, {"role": "*"}),
    "user23": ({"role": "dev3"}, {"role": "*"}),
    "user24": ({"role": "dev4"}, {"role": "*"}),
    "user25": ({"role": "dev4"}, {"role": "*"}),
    "user26": ({"role": "dev5"}, {"role": "*"}),
    "user27": ({"role": "dev6"}, {"role": "*"}),
    "user28": ({"role": "dev7"}, {"role": "*"}),
    "user29": ({"role": "dev8"}, {"role": "*"}),
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
        # Rules for grant all dev3 to do read actions to some VM
        {
            "rule": ("dev3", "vm1", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev3", "vm2", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev3", "vm3", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev3", "vm4", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        # Rules for grant all dev4 to do read actions to some VM
        {
            "rule": ("dev4", "vm5", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev4", "vm6", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev4", "vm7", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev4", "vm8", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev4", "vm9", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        # Rules for grant all dev5 to do read actions to some VM
        {
            "rule": ("dev5", "vm1", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev5", "vm2", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev5", "vm3", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev5", "vm4", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        # Rules for grant all dev6 to do read actions to some VM
        {
            "rule": ("dev6", "vm5", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev6", "vm6", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev6", "vm7", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev6", "vm8", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
        {
            "rule": ("dev6", "vm9", "vm-write"),
            "instructions": (
                {"decision": "grant"},
            )
        },
    )
}


