
pdp_name = "pdp_mls"
policy_name = "MLS Policy example"
model_name = "MLS"
policy_genre = "authz"

subjects = {"adminuser": "", "user1": "", "user2": "", }
objects = {"vm0": "", "vm1": "", }
actions = {"start": "", "stop": ""}

subject_categories = {"subject-security-level": "", }
object_categories = {"object-security-level": "", }
action_categories = {"action-type": "", }

subject_data = {
    "subject-security-level": {"low": "", "medium": "", "high": ""},
}
object_data = {
    "object-security-level": {"low": "", "medium": "", "high": ""},
}
action_data = {"action-type": {"vm-action": "", "storage-action": "", }}

subject_assignments = {
    "adminuser": {"subject-security-level": "high"},
    "user1": {"subject-security-level": "medium"},
}
object_assignments = {
    "vm0": {"object-security-level": "medium"},
    "vm1": {"object-security-level": "low"},
}
action_assignments = {
    "start": {"action-type": "vm-action"},
    "stop": {"action-type": "vm-action"}
}

meta_rule = {
    "mls": {
        "id": "",
        "value": ("subject-security-level",
                  "object-security-level",
                  "action-type")},
}

rules = {
    "mls": (
        {
            "rule": ("high", "medium", "vm-action"),
            "instructions": ({"decision": "grant"})
        },
        {
            "rule": ("high", "low", "vm-action"),
            "instructions": ({"decision": "grant"})
        },
        {
            "rule": ("medium", "low", "vm-action"),
            "instructions": ({"decision": "grant"})
        },
    )
}
