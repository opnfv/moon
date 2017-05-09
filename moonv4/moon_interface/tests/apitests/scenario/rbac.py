
pdp_name = "pdp1"
policy_name = "RBAC policy example"
model_name = "RBAC"

subjects = {"user0": "", "user1": "", }
objects = {"vm0": "", "vm1": "", }
actions = {"start": "", "stop": ""}

subject_categories = {"role": "", }
object_categories = {"id": "", }
action_categories = {"action-type": "", }

subject_data = {"role": {"admin": "", "employee": ""}}
object_data = {"id": {"vm0": "", "vm1": ""}}
action_data = {"action-type": {"vm-action": "", }}

subject_assignments = {"user0": {"role": "employee"}, "user1": {"role": "employee"}, }
object_assignments = {"vm0": {"id": "vm0"}, "vm1": {"id": "vm1"}}
action_assignments = {"start": {"action-type": "vm-action"}, "stop": {"action-type": "vm-action"}}

meta_rule = {
    "rbac": {"id": "", "value": ("role", "id", "action-type")},
}

rules = {
    "rbac": (
        {
            "rule": ("admin", "vm0", "vm-action"),
            "instructions": (
                {"decision": "grant"}  # "grant" to immediately exit, "continue" to wait for the result of next policy
            )
        },
        {
            "rule": ("admin", "vm1", "vm-action"),
            "instructions": (
                {"decision": "grant"}
            )
        },
    )
}


