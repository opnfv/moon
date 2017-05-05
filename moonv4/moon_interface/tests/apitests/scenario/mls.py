
pdp_name = "pdp1"
policy_name = "MLS Policy example"
model_name = "MLS"

subjects = {"user0": "", "user1": "", "user2": "", }
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
    "user0": {"subject-security-level": "high"},
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
    "mls": {"id": "", "value": ("subject-security-level", "object-security-level", "action-type")},
}

rules = {
    "mls": (
        ("high", "medium", "vm-action"),
        ("high", "low", "vm-action"),
        ("medium", "low", "vm-action"),
    )
}
