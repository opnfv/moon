from kubernetes import client, config
from utilities import CONF, get_b64_conf, COMPONENTS

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


def patch_k8s(monkeypatch):
    def _load_kube_config_mockreturn(*args, **kwargs):
        return
    monkeypatch.setattr(config, 'load_kube_config',
                        _load_kube_config_mockreturn)

    def list_kube_config_contexts_mockreturn(*args, **kwargs):
        return [{"name": "active_context"}], {"name": "active_context"}
    monkeypatch.setattr(config, 'list_kube_config_contexts',
                        list_kube_config_contexts_mockreturn)

    def new_client_from_config_mockreturn(*args, **kwargs):
        return {"client": True}
    monkeypatch.setattr(config, 'new_client_from_config',
                        new_client_from_config_mockreturn)

    def list_pod_for_all_namespaces_mockreturn(*args, **kwargs):
        class pods:
            items = []
        return pods
    monkeypatch.setattr(client.CoreV1Api, 'list_pod_for_all_namespaces',
                        list_pod_for_all_namespaces_mockreturn)

    def create_namespaced_deployment_mockreturn(*args, **kwargs):

        class metadata:
            uid = "123456789"

        class pod:
            def __init__(self):
                self.metadata = metadata()
        return pod()
    monkeypatch.setattr(client.ExtensionsV1beta1Api,
                        'create_namespaced_deployment',
                        create_namespaced_deployment_mockreturn)

    def delete_namespaced_deployment_mockreturn(*args, **kwargs):
        return None

    monkeypatch.setattr(client.ExtensionsV1beta1Api,
                        'delete_namespaced_deployment',
                        delete_namespaced_deployment_mockreturn)

    def create_namespaced_service_mockreturn(*args, **kwargs):
        return {}
    monkeypatch.setattr(client.CoreV1Api,
                        'create_namespaced_service',
                        create_namespaced_service_mockreturn)

    def delete_namespaced_service_mockreturn(*args, **kwargs):
        return {}
    monkeypatch.setattr(client.CoreV1Api,
                        'delete_namespaced_service',
                        delete_namespaced_service_mockreturn)


def register_pods(m):
    """ Modify the response from Requests module
    """
    register_consul(m)
    register_pdp(m)
    # register_meta_rules(m)
    register_policies(m)
    register_models(m)
    # register_policy_subject(m, "policy_id_1")
    # register_policy_subject(m, "policy_id_2")
    # register_policy_object(m, "policy_id_1")
    # register_policy_object(m, "policy_id_2")
    # register_policy_action(m, "policy_id_1")
    # register_policy_action(m, "policy_id_2")
    # register_policy_subject_assignment(m, "policy_id_1", "subject_id")
    # register_policy_subject_assignment_list(m1, "policy_id_1")
    # register_policy_subject_assignment(m, "policy_id_2", "subject_id")
    # register_policy_subject_assignment_list(m1, "policy_id_2")
    # register_policy_object_assignment(m, "policy_id_1", "object_id")
    # register_policy_object_assignment_list(m1, "policy_id_1")
    # register_policy_object_assignment(m, "policy_id_2", "object_id")
    # register_policy_object_assignment_list(m1, "policy_id_2")
    # register_policy_action_assignment(m, "policy_id_1", "action_id")
    # register_policy_action_assignment_list(m1, "policy_id_1")
    # register_policy_action_assignment(m, "policy_id_2", "action_id")
    # register_policy_action_assignment_list(m1, "policy_id_2")
    # register_rules(m, "policy_id1")


def register_consul(m):
    for component in COMPONENTS:
        m.register_uri(
            'GET', 'http://consul:8500/v1/kv/{}'.format(component),
            json=[{'Key': component, 'Value': get_b64_conf(component)}]
        )
    m.register_uri(
        'GET', 'http://consul:8500/v1/kv/components/port_start',
        json=[
            {
                "LockIndex": 0,
                "Key": "components/port_start",
                "Flags": 0,
                "Value": "MzEwMDE=",
                "CreateIndex": 9,
                "ModifyIndex": 9
            }
        ],
    )
    m.register_uri(
        'PUT', 'http://consul:8500/v1/kv/components/port_start',
        json=[],
    )
    # m.register_uri(
    #     'GET', 'http://consul:8500/v1/kv/plugins?recurse=true',
    #     json=[
    #         {
    #             "LockIndex": 0,
    #             "Key": "plugins/authz",
    #             "Flags": 0,
    #             "Value": "eyJjb250YWluZXIiOiAid3Vrb25nc3VuL21vb25fYXV0aHo6djQuMyIsICJwb3J0IjogODA4MX0=",
    #             "CreateIndex": 14,
    #             "ModifyIndex": 656
    #         }
    #     ],
    # )


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