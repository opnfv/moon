COMPONENTS = {
    "manager": {
        "port": 8082,
        "hostname": "manager"
    }
}

pdp_mock = {
    "pdp_id1": {
        "name": "...",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    },
    "pdp_id12": {
        "name": "...",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
}

meta_rules_mock = {
    "meta_rule_id1": {
        "name": "meta_rule1",
        "algorithm": "name of the meta rule algorithm",
        "subject_categories": ["subject_category_id1",
                               "subject_category_id2"],
        "object_categories": ["object_category_id1"],
        "action_categories": ["action_category_id1"]
    },
    "meta_rule_id2": {
        "name": "name of the meta rules2",
        "algorithm": "name of the meta rule algorithm",
        "subject_categories": ["subject_category_id1",
                               "subject_category_id2"],
        "object_categories": ["object_category_id1"],
        "action_categories": ["action_category_id1"]
    }
}

policies_mock = {
    "policy_id_1": {
        "name": "test_policy1",
        "model_id": "model_id_1",
        "genre": "authz",
        "description": "test",
    },
    "policy_id_2": {
        "name": "test_policy2",
        "model_id": "model_id_2",
        "genre": "authz",
        "description": "test",
    }
}
subject_mock = {
    "policy_id_1": {
        "subject_id": {
            "name": "subject_name",
            "keystone_id": "keystone_project_id1",
            "description": "a description"
        }
    },
    "policy_id_2": {
        "subject_id": {
            "name": "subject_name",
            "keystone_id": "keystone_project_id1",
            "description": "a description"
        }
    }
}
subject_assignment_mock = {
    "subject_id": {
        "policy_id": "ID of the policy",
        "subject_id": "ID of the subject",
        "category_id": "ID of the category",
        "assignments": [],
    }
}
object_mock = {
    "policy_id_1": {
        "object_id": {
            "name": "object_name",
            "description": "a description"
        }
    },
    "policy_id_2": {
        "object_id": {
            "name": "object_name",
            "description": "a description"
        }
    }
}

object_assignment_mock = {
    "object_id": {
        "policy_id": "ID of the policy",
        "object_id": "ID of the object",
        "category_id": "ID of the category",
        "assignments": [],
    }
}

action_mock = {
    "policy_id_1": {
        "action_id": {
            "name": "action_name",
            "description": "a description"
        }
    },
    "policy_id_2": {
        "action_id": {
            "name": "action_name",
            "description": "a description"
        }
    }
}

action_assignment_mock = {
    "action_id": {
        "policy_id": "ID of the policy",
        "action_id": "ID of the action",
        "category_id": "ID of the category",
        "assignments": [],
    }
}

models_mock = {
    "model_id_1": {
        "name": "test_model",
        "description": "test",
        "meta_rules": ["meta_rule_id1"]
    },
    "model_id_2": {
        "name": "test_model",
        "description": "test",
        "meta_rules": ["meta_rule_id2"]
    },
}

rules_mock = {
    "rules": {
        "meta_rule_id": "meta_rule_id1",
        "rule_id1": {
            "rule": ["subject_data_id1",
                     "object_data_id1",
                     "action_data_id1"],
            "instructions": (
                {"decision": "grant"},
                # "grant" to immediately exit,
                # "continue" to wait for the result of next policy
                # "deny" to deny the request
            )
        },
        "rule_id2": {
            "rule": ["subject_data_id2",
                     "object_data_id2",
                     "action_data_id2"],
            "instructions": (
                {
                    "update": {
                        "operation": "add",
                        # operations may be "add" or "delete"
                        "target": "rbac:role:admin"
                        # add the role admin to the current user
                    }
                },
                {"chain": {"name": "rbac"}}
                # chain with the policy named rbac
            )
        }
    }
}
