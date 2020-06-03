# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



shared_ids = {
    "policy": {
        "policy_id_1": "policy_id_1",
        "policy_id_2": "policy_id_2",
        "policy_id_3": "policy_id_3",
        "policy_id_invalid_response": "policy_id_invalid_response"
    },
    "category": {
        "category_id_1": "category_id_1",
        "invalid_category_id_1": " invalid_category_id_1"
    },
    "perimeter": {
        "perimeter_id_1": "subject_id_1",
        "perimeter_id_2": "object_id_1",
        "perimeter_id_3": "action_id_1"
    },
    "meta_rule": {
        "meta_rule_id_1": "meta_rule_id_1",
        "meta_rule_id_2": "meta_rule_id_2"
    },
    "rule": {
        "rule_id_1": "rule_id_2",
        "rule_id_2": "rule_id_2"
    },
    "model": {
        "model_id_1": "model_id_1"
    },
    "subject": {
        "subject_id_1": "subject_id_1",
        "invalid_subject_id": "invalid_subject_id",
        "invalid_category_id": "invalid_category_id",
        "invalid_assignment_id": "invalid_assignment_id"
    },
    "object": {
        "object_id_1": "object_id_1",
        "invalid_object_id": "invalid_object_id",
        "invalid_category_id": "invalid_category_id",
        "invalid_assignment_id": "invalid_assignment_id"
    },
    "action": {
        "action_id_1": "action_id_1",
        "invalid_action_id": "invalid_action_id",
        "invalid_category_id": "invalid_category_id",
        "invalid_assignment_id": "invalid_assignment_id"
    }
}

pdp_mock = {
    "pdp_id1": {
        "name": "...",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "vim_project_id": "vim_project_id1",
        "description": "...",
    }
}

meta_rules_mock = {
    shared_ids["meta_rule"]["meta_rule_id_1"]: {
        "name": "meta_rule1",
        "algorithm": "name of the meta rule algorithm",
        "subject_categories": ["subject_category_id1",
                               "subject_category_id2"],
        "object_categories": ["object_category_id1"],
        "action_categories": ["action_category_id1"]
    },
    shared_ids["meta_rule"]["meta_rule_id_2"]: {
        "name": "name of the meta rules2",
        "algorithm": "name of the meta rule algorithm",
        "subject_categories": ["subject_category_id1",
                               "subject_category_id2"],
        "object_categories": ["object_category_id1"],
        "action_categories": ["action_category_id1"]
    }
}

policies_mock = {
    shared_ids["policy"]["policy_id_1"]: {
        "name": "test_policy1",
        "model_id": shared_ids["model"]["model_id_1"],
        "genre": "authz",
        "description": "test",
    },
    shared_ids["policy"]["policy_id_2"]: {
        "name": "test_policy2",
        "model_id": shared_ids["model"]["model_id_1"],
        "genre": "authz",
        "description": "test",
    }
}

subject_mock = {
    shared_ids["policy"]["policy_id_1"]: {
        "subject_id": {
            "name": "subject_name",
            "vim_id": "vim_project_id1",
            "description": "a description"
        }
    },
    shared_ids["policy"]["policy_id_invalid_response"]: {
        "subject_id": {
            "name": "subject_name",
            "vim_id": "vim_project_id1",
            "description": "a description"
        }
    }

}

subject_assignment_mock = {
    shared_ids["subject"]["subject_id_1"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "subject_id": "subject_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"],
    }
}

subject_assignment_mock_invalid_subject_id = {
    shared_ids["subject"]["invalid_subject_id"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "subject_id_invalid": "subject_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"],
    }
}

subject_assignment_mock_invalid_category_id = {
    shared_ids["subject"]["invalid_category_id"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "subject_id": "subject_id_1",
        "category_id_invalid": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"],
    }
}

subject_assignment_mock_invalid_assignment_id = {
    shared_ids["subject"]["invalid_assignment_id"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "subject_id": "subject_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments_invalid": ["data_id_1, data_id_2"],
    }
}

object_mock = {
    shared_ids["policy"]["policy_id_1"]: {
        "object_id": {
            "name": "object_name",
            "description": "a description"
        }
    }
}

object_assignment_mock = {
    shared_ids["object"]["object_id_1"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "object_id": "object_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"]
    }
}

object_assignment_mock_invalid_object_id = {
    shared_ids["object"]["invalid_object_id"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "object_id": "object_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"]
    }
}

object_assignment_mock_invalid_category_id = {
    shared_ids["object"]["invalid_category_id"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "object_id": "object_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"]
    }
}

object_assignment_mock_invalid_assignment_id = {
    shared_ids["object"]["invalid_assignment_id"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "object_id": "object_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"]
    }
}

action_mock = {
    shared_ids["policy"]["policy_id_1"]: {
        "action_id": {
            "name": "action_name",
            "description": "a description"
        }
    }
}

action_assignment_mock = {
    shared_ids["action"]["action_id_1"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "action_id": "action_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"]
    }
}

action_assignment_mock_invalid_action_id = {
    shared_ids["action"]["invalid_action_id"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "action_id": "action_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"]
    }
}

action_assignment_mock_invalid_category_id = {
    shared_ids["action"]["invalid_category_id"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "action_id": "action_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"]
    }
}

action_assignment_mock_invalid_assignment_id = {
    shared_ids["action"]["invalid_assignment_id"]: {
        "policy_id": shared_ids["policy"]["policy_id_1"],
        "action_id": "action_id_1",
        "category_id": shared_ids["category"]["category_id_1"],
        "assignments": ["data_id_1, data_id_2"]
    }
}


models_mock = {
    shared_ids["model"]["model_id_1"]: {
        "name": "test_model",
        "description": "test",
        "meta_rules": [shared_ids["meta_rule"]["meta_rule_id_1"]]
    }
}

rules_mock = {
    "rules": {
        "meta_rule_id": shared_ids["meta_rule"]["meta_rule_id_1"],
        shared_ids["rule"]["rule_id_1"]: {
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
        shared_ids["rule"]["rule_id_2"]: {
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

pipelines_mock = {
    "policy_id_1": {
        "starttime": 1548688120.3931532,
        "port": 20000,
        "server_ip": "127.0.0.1",
        "status": "up",
        "log": "/tmp/moon_policy_id_1.log"
    },
    "policy_id_2": {
        "starttime": 1548688120.3931532,
        "port": 20001,
        "server_ip": "127.0.0.1",
        "status": "up",
        "log": "/tmp/moon_policy_id_2.log"
    }
}
