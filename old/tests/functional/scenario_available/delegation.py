
pdp_name = "pdp1"
policy_name = "Delegation policy example"
model_name = "Delegation"

subjects = {"user0": "", }
objects = {"user1": "", }
actions = {"delegate": ""}

subject_categories = {"subjectid": "", }
object_categories = {"delegated": "", }
action_categories = {"delegation-action": "", }

subject_data = {"subjectid": {"user0": ""}}
object_data = {"delegated": {"user1": ""}}
action_data = {"delegation-action": {"delegate": ""}}

subject_assignments = {"user0": {"subjectid": "user0"}}
object_assignments = {"user1": {"delegated": "user1"}}
action_assignments = {"delegate": {"delegation-action": "delegate"}}

meta_rule = {
    "session": {"id": "", "value": ("subjectid", "delegated", "delegation-action")},
}

rules = {
    "session": (
        {
            "rule": ("user0", "user1", "delegate"),
            "instructions": (
                {
                    "update": {"request:subject": "user1"}  # update the current user with "user1"
                },
                {"chain": {"security_pipeline": "rbac"}}
            )
        },
    )
}


