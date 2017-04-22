
pdp_name = "pdp1"
policy_name = "RBAC policy example"
model_name = "RBAC"

subjects = {"user0": "", "user1": "", }
objects = {"vm0": "", }
actions = {"start": "", "stop": ""}

subject_categories = {"role": "", }
object_categories = {"id": "", }
action_categories = {"action-type": "", }

subject_data = {"role": {"admin": "", "employee": ""}}
object_data = {"id": {"vm1": "", "vm2": ""}}
action_data = {"action-type": {"vm-action": "", }}

subject_assignments = {"user0": {"role": "admin"}, "user1": {"role": "employee"}, }
object_assignments = {"vm0": {"id": "vm1"}}
action_assignments = {"start": {"action-type": "vm-action"}, "stop": {"action-type": "vm-action"}}

meta_rule = {
    "rbac": {"id": "", "value": ("role", "id", "action-type")},
}

rules = {
    "rbac": (
        ("admin", "vm1", "vm-action"),
    )
}


