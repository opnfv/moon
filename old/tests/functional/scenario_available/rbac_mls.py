
pdp_name = "pdp1"
policy_name = "Multi policy example"
model_name = "RBAC"

subjects = {"user0": "", "user1": "", "user2": "", }
objects = {"vm0": "", "vm1": "", }
actions = {"start": "", "stop": ""}

subject_categories = {"role": "", "subject-security-level": "", }
object_categories = {"id": "", "object-security-level": "", }
action_categories = {"action-type": "", }

subject_data = {
    "role": {"admin": "", "employee": ""},
    "subject-security-level": {"low": "", "medium": "", "high": ""},
}
object_data = {
    "id": {"vm1": "", "vm2": ""},
    "object-security-level": {"low": "", "medium": "", "high": ""},
}
action_data = {"action-type": {"vm-action": "", "storage-action": "", }}

subject_assignments = {
    "user0": {"role": "admin", "subject-security-level": "high"},
    "user1": {"role": "employee", "subject-security-level": "medium"},
}
object_assignments = {
    "vm0": {"id": "vm1", "object-security-level": "medium"},
    "vm1": {"id": "vm2", "object-security-level": "low"},
}
action_assignments = {
    "start": {"action-type": "vm-action"},
    "stop": {"action-type": "vm-action"}
}

meta_rule = {
    "rbac": {"id": "", "value": ("role", "id", "action-type")},
    "mls": {"id": "", "value": ("subject-security-level", "object-security-level", "action-type")},
}

rules = {
    "rbac": (
        ("admin", "vm1", "vm-action"),
    ),
    "mls": (
        ("high", "medium", "vm-action"),
        ("medium", "low", "vm-action"),
    )
}
