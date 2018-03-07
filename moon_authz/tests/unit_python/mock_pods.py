from utilities import CONF, get_b64_conf, COMPONENTS

pdp_mock = {
    "b3d3e18abf3340e8b635fd49e6634ccd": {
        "description": "test",
        "security_pipeline": [
            "f8f49a779ceb47b3ac810f01ef71b4e0"
        ],
        "name": "pdp_rbac",
        "keystone_project_id": "a64beb1cc224474fb4badd43173e7101"
    },
    "pdp_id1": {
        "name": "pdp_id1",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    },
    "pdp_id12": {
        "name": "pdp_id2",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id2",
        "description": "...",
    }
}

meta_rules_mock = {
    "f8f49a779ceb47b3ac810f01ef71b4e0": {
        "subject_categories": [
            "14e6ae0ba34d458b876c791b73aa17bd"
        ],
        "action_categories": [
            "241a2a791554421a91c9f1bc564aa94d"
        ],
        "description": "",
        "name": "rbac",
        "object_categories": [
            "6d48500f639d4c2cab2b1f33ef93a1e8"
        ]
    },
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
    "f8f49a779ceb47b3ac810f01ef71b4e0": {
        "name": "RBAC policy example",
        "model_id": "cd923d8633ff4978ab0e99938f5153d6",
        "description": "test",
        "genre": "authz"
    },
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
    "f8f49a779ceb47b3ac810f01ef71b4e0": {
        "89ba91c18dd54abfbfde7a66936c51a6": {
            "description": "test",
            "policy_list": [
                "f8f49a779ceb47b3ac810f01ef71b4e0",
                "636cd473324f4c0bbd9102cb5b62a16d"
            ],
            "name": "testuser",
            "email": "mail",
            "id": "89ba91c18dd54abfbfde7a66936c51a6",
            "extra":  {}
        }
    },
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
            "keystone_id": "keystone_project_id2",
            "description": "a description"
        }
    }
}

subject_assignment_mock = {
    "826c1156d0284fc9b4b2ddb279f63c52": {
        "category_id": "14e6ae0ba34d458b876c791b73aa17bd",
        "assignments": [
            "24ea95256c5f4c888c1bb30a187788df",
            "6b227b77184c48b6a5e2f3ed1de0c02a",
            "31928b17ec90438ba5a2e50ae7650e63",
            "4e60f554dd3147af87595fb6b37dcb13",
            "7a5541b63a024fa88170a6b59f99ccd7",
            "dd2af27812f742029d289df9687d6126"
        ],
        "id": "826c1156d0284fc9b4b2ddb279f63c52",
        "subject_id": "89ba91c18dd54abfbfde7a66936c51a6",
        "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
    },
    "7407ffc1232944279b0cbcb0847c86f7": {
        "category_id": "315072d40d774c43a89ff33937ed24eb",
        "assignments": [
            "6b227b77184c48b6a5e2f3ed1de0c02a",
            "31928b17ec90438ba5a2e50ae7650e63",
            "7a5541b63a024fa88170a6b59f99ccd7",
            "dd2af27812f742029d289df9687d6126"
        ],
        "id": "7407ffc1232944279b0cbcb0847c86f7",
        "subject_id": "89ba91c18dd54abfbfde7a66936c51a6",
        "policy_id": "3e65256389b448cb9897917ea235f0bb"
    }
}

object_mock = {
    "f8f49a779ceb47b3ac810f01ef71b4e0": {
        "9089b3d2ce5b4e929ffc7e35b55eba1a": {
            "name": "vm1",
            "description": "test",
            "id": "9089b3d2ce5b4e929ffc7e35b55eba1a",
            "extra":  {},
            "policy_list": [
                "f8f49a779ceb47b3ac810f01ef71b4e0",
                "636cd473324f4c0bbd9102cb5b62a16d"
            ]
        },
    },
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
    "201ad05fd3f940948b769ab9214fe295": {
        "object_id": "9089b3d2ce5b4e929ffc7e35b55eba1a",
        "assignments": [
            "030fbb34002e4236a7b74eeb5fd71e35",
            "06bcb8655b9d46a9b90e67ef7c825b50",
            "34eb45d7f46d4fb6bc4965349b8e4b83",
            "4b7793dbae434c31a77da9d92de9fa8c"
        ],
        "id": "201ad05fd3f940948b769ab9214fe295",
        "category_id": "6d48500f639d4c2cab2b1f33ef93a1e8",
        "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
    },
    "90c5e86f8be34c0298fbd1973e4fb043": {
        "object_id": "67b8008a3f8d4f8e847eb628f0f7ca0e",
        "assignments": [
            "a098918e915b4b12bccb89f9a3f3b4e4",
            "06bcb8655b9d46a9b90e67ef7c825b50",
            "7dc76c6142af47c88b60cc2b0df650ba",
            "4b7793dbae434c31a77da9d92de9fa8c"
        ],
        "id": "90c5e86f8be34c0298fbd1973e4fb043",
        "category_id": "33aece52d45b4474a20dc48a76800daf",
        "policy_id": "3e65256389b448cb9897917ea235f0bb"
    }
}

action_mock = {
    "f8f49a779ceb47b3ac810f01ef71b4e0": {
        "cdb3df220dc05a6ea3334b994827b068": {
            "name": "boot",
            "description": "test",
            "id": "cdb3df220dc04a6ea3334b994827b068",
            "extra":  {},
            "policy_list": [
                "f8f49a779ceb47b3ac810f01ef71b4e0",
                "636cd473324f4c0bbd9102cb5b62a16d"
            ]
        },
        "cdb3df220dc04a6ea3334b994827b068": {
            "name": "stop",
            "description": "test",
            "id": "cdb3df220dc04a6ea3334b994827b068",
            "extra":  {},
            "policy_list": [
                "f8f49a779ceb47b3ac810f01ef71b4e0",
                "636cd473324f4c0bbd9102cb5b62a16d"
            ]
        },
        "9f5112afe9b34a6c894eb87246ccb7aa": {
            "name": "start",
            "description": "test",
            "id": "9f5112afe9b34a6c894eb87246ccb7aa",
            "extra":  {},
            "policy_list": [
                "f8f49a779ceb47b3ac810f01ef71b4e0",
                "636cd473324f4c0bbd9102cb5b62a16d"
            ]
        }
    },
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
    "2128e3ffbd1c4ef5be515d625745c2d4": {
        "category_id": "241a2a791554421a91c9f1bc564aa94d",
        "action_id": "cdb3df220dc05a6ea3334b994827b068",
        "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
        "id": "2128e3ffbd1c4ef5be515d625745c2d4",
        "assignments": [
            "570c036781e540dc9395b83098c40ba7",
            "7fe17d7a2e3542719f8349c3f2273182",
            "015ca6f40338422ba3f692260377d638",
            "23d44c17bf88480f83e8d57d2aa1ea79"
        ]
    },
    "cffb98852f3a4110af7a0ddfc4e19201": {
        "category_id": "4a2c5abaeaf644fcaf3ca8df64000d53",
        "action_id": "cdb3df220dc04a6ea3334b994827b068",
        "policy_id": "3e65256389b448cb9897917ea235f0bb",
        "id": "cffb98852f3a4110af7a0ddfc4e19201",
        "assignments": [
            "570c036781e540dc9395b83098c40ba7",
            "7fe17d7a2e3542719f8349c3f2273182",
            "015ca6f40338422ba3f692260377d638",
            "23d44c17bf88480f83e8d57d2aa1ea79"
        ]
    }
}

models_mock = {
    "cd923d8633ff4978ab0e99938f5153d6": {
        "name": "RBAC",
        "meta_rules": [
            "f8f49a779ceb47b3ac810f01ef71b4e0"
        ],
        "description": "test"
    },
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
    "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
    "rules": [
        {
            "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
            "rule": [
                "24ea95256c5f4c888c1bb30a187788df",
                "030fbb34002e4236a7b74eeb5fd71e35",
                "570c036781e540dc9395b83098c40ba7"
            ],
            "enabled": True,
            "id": "0201a2bcf56943c1904dbac016289b71",
            "instructions": [
                {
                    "decision": "grant"
                }
            ],
            "meta_rule_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
        },
        {
            "policy_id": "ecc2451c494e47b5bca7250cd324a360",
            "rule": [
                "54f574cd2043468da5d65e4f6ed6e3c9",
                "6559686961a3490a978f246ac9f85fbf",
                "ac0d1f600bf447e8bd2f37b7cc47f2dc"
            ],
            "enabled": True,
            "id": "a83fed666af8436192dfd8b3c83a6fde",
            "instructions": [
                {
                    "decision": "grant"
                }
            ],
            "meta_rule_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
        }
    ]
}


def register_pods(m):
    """ Modify the response from Requests module
    """
    register_consul(m)
    register_pdp(m)
    register_meta_rules(m)
    register_policies(m)
    register_models(m)
    register_orchestrator(m)
    register_policy_subject(m, "f8f49a779ceb47b3ac810f01ef71b4e0")
    # register_policy_subject(m, "policy_id_2")
    register_policy_object(m, "f8f49a779ceb47b3ac810f01ef71b4e0")
    # register_policy_object(m, "policy_id_2")
    register_policy_action(m, "f8f49a779ceb47b3ac810f01ef71b4e0")
    # register_policy_action(m, "policy_id_2")
    register_policy_subject_assignment(m, "f8f49a779ceb47b3ac810f01ef71b4e0", "89ba91c18dd54abfbfde7a66936c51a6")
    # register_policy_subject_assignment_list(m, "f8f49a779ceb47b3ac810f01ef71b4e0")
    # register_policy_subject_assignment(m, "policy_id_2", "subject_id")
    # register_policy_subject_assignment_list(m1, "policy_id_2")
    register_policy_object_assignment(m, "f8f49a779ceb47b3ac810f01ef71b4e0", "9089b3d2ce5b4e929ffc7e35b55eba1a")
    # register_policy_object_assignment_list(m, "f8f49a779ceb47b3ac810f01ef71b4e0")
    # register_policy_object_assignment(m, "policy_id_2", "object_id")
    # register_policy_object_assignment_list(m1, "policy_id_2")
    register_policy_action_assignment(m, "f8f49a779ceb47b3ac810f01ef71b4e0", "cdb3df220dc05a6ea3334b994827b068")
    # register_policy_action_assignment_list(m, "f8f49a779ceb47b3ac810f01ef71b4e0")
    # register_policy_action_assignment(m, "policy_id_2", "action_id")
    # register_policy_action_assignment_list(m1, "policy_id_2")
    register_rules(m, "f8f49a779ceb47b3ac810f01ef71b4e0")
    register_rules(m, "policy_id_1")
    register_rules(m, "policy_id_2")


def register_consul(m):
    for component in COMPONENTS:
        m.register_uri(
            'GET', 'http://consul:8500/v1/kv/{}'.format(component),
            json=[{'Key': component, 'Value': get_b64_conf(component)}]
        )
    m.register_uri(
        'GET', 'http://consul:8500/v1/kv/components_port_start',
        json=[
            {
                "LockIndex": 0,
                "Key": "components_port_start",
                "Flags": 0,
                "Value": "MzEwMDE=",
                "CreateIndex": 9,
                "ModifyIndex": 9
            }
        ],
    )
    m.register_uri(
        'PUT', 'http://consul:8500/v1/kv/components_port_start',
        json=[],
    )
    m.register_uri(
        'GET', 'http://consul:8500/v1/kv/plugins?recurse=true',
        json=[
            {
                "LockIndex": 0,
                "Key": "plugins/authz",
                "Flags": 0,
                "Value": "eyJjb250YWluZXIiOiAid3Vrb25nc3VuL21vb25fYXV0aHo6djQuMyIsICJwb3J0IjogODA4MX0=",
                "CreateIndex": 14,
                "ModifyIndex": 656
            }
        ],
    )
    m.register_uri(
        'GET', 'http://consul:8500/v1/kv/components?recurse=true',
        json=[
            {"Key": key, "Value": get_b64_conf(key)} for key in COMPONENTS
        ],
    )
    m.register_uri(
        'GET', 'http://consul:8500/v1/kv/plugins/authz',
        json=[
            {
                "LockIndex": 0,
                "Key": "plugins/authz",
                "Flags": 0,
                "Value": "eyJjb250YWluZXIiOiAid3Vrb25nc3VuL21vb25fYXV0aHo6djQuMyIsICJwb3J0IjogODA4MX0=",
                "CreateIndex": 14,
                "ModifyIndex": 656
            }
        ],
    )


def register_orchestrator(m):
    m.register_uri(
        'GET', 'http://orchestrator:8083/pods',
        json={
            "pods": {
                "1234567890": [
                    {"name": "wrapper-quiet", "port": 8080,
                     "container": "wukongsun/moon_wrapper:v4.3.1",
                     "namespace": "moon"}]}}
    )


def register_pdp(m):
    m.register_uri(
        'GET', 'http://{}:{}/{}'.format(CONF['components']['manager']['hostname'],
                                        CONF['components']['manager']['port'], 'pdp'),
        json={'pdps': pdp_mock}
    )


def register_meta_rules(m):
    m.register_uri(
        'GET', 'http://{}:{}/{}'.format(CONF['components']['manager']['hostname'],
                                        CONF['components']['manager']['port'], 'meta_rules'),
        json={'meta_rules': meta_rules_mock}
    )


def register_policies(m):
    m.register_uri(
        'GET', 'http://{}:{}/{}'.format(CONF['components']['manager']['hostname'],
                                        CONF['components']['manager']['port'], 'policies'),
        json={'policies': policies_mock}
    )


def register_models(m):
    m.register_uri(
        'GET', 'http://{}:{}/{}'.format(CONF['components']['manager']['hostname'],
                                        CONF['components']['manager']['port'], 'models'),
        json={'models': models_mock}
    )


def register_policy_subject(m, policy_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/subjects'.format(CONF['components']['manager']['hostname'],
                                                    CONF['components']['manager']['port'], 'policies', policy_id),
        json={'subjects': subject_mock[policy_id]}
    )


def register_policy_object(m, policy_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/objects'.format(CONF['components']['manager']['hostname'],
                                                   CONF['components']['manager']['port'], 'policies', policy_id),
        json={'objects': object_mock[policy_id]}
    )


def register_policy_action(m, policy_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/actions'.format(CONF['components']['manager']['hostname'],
                                                   CONF['components']['manager']['port'], 'policies', policy_id),
        json={'actions': action_mock[policy_id]}
    )


def register_policy_subject_assignment(m, policy_id, subj_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/subject_assignments/{}'.format(CONF['components']['manager']['hostname'],
                                                                  CONF['components']['manager']['port'], 'policies',
                                                                  policy_id,
                                                                  subj_id),
        json={'subject_assignments': subject_assignment_mock}
    )


def register_policy_subject_assignment_list(m, policy_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/subject_assignments'.format(CONF['components']['manager']['hostname'],
                                                               CONF['components']['manager']['port'], 'policies',
                                                               policy_id),
        json={'subject_assignments': subject_assignment_mock}
    )


def register_policy_object_assignment(m, policy_id, obj_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/object_assignments/{}'.format(CONF['components']['manager']['hostname'],
                                                                 CONF['components']['manager']['port'], 'policies',
                                                                 policy_id,
                                                                 obj_id),
        json={'object_assignments': object_assignment_mock}
    )


def register_policy_object_assignment_list(m, policy_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/object_assignments'.format(CONF['components']['manager']['hostname'],
                                                              CONF['components']['manager']['port'], 'policies',
                                                              policy_id),
        json={'object_assignments': object_assignment_mock}
    )


def register_policy_action_assignment(m, policy_id, action_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/action_assignments/{}'.format(CONF['components']['manager']['hostname'],
                                                                 CONF['components']['manager']['port'], 'policies',
                                                                 policy_id,
                                                                 action_id),
        json={'action_assignments': action_assignment_mock}
    )


def register_policy_action_assignment_list(m, policy_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/action_assignments'.format(CONF['components']['manager']['hostname'],
                                                              CONF['components']['manager']['port'], 'policies',
                                                              policy_id),
        json={'action_assignments': action_assignment_mock}
    )


def register_rules(m, policy_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/{}'.format(CONF['components']['manager']['hostname'],
                                              CONF['components']['manager']['port'], 'policies',
                                              policy_id, 'rules'),
        json={'rules': rules_mock}
    )