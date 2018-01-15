import mock_repo.components_utilities as comp_util
import mock_repo.data as data_mock


def register_components(m):
    for component in data_mock.components:
        m.register_uri(
            'GET', 'http://consul:8500/v1/kv/{}'.format(component),
            json=[{'Key': component, 'Value': comp_util.get_b64_conf(component)}]
        )

    m.register_uri(
        'PUT', 'http://consul:8500/v1/kv/components/port_start',
        json=[]
    )

    m.register_uri(
        'GET', 'http://consul:8500/v1/kv/components?recurse=true',
        json=[
            {"Key": key, "Value": comp_util.get_b64_conf(key)} for key in data_mock.components
        ],
        # json={'Key': "components", 'Value': get_b64_comp_util.CONF("components")}
    )


def register_keystone(m):
    m.register_uri(
        'POST', 'http://keystone:5000/v3/auth/tokens',
        headers={'X-Subject-Token': "111111111"}
    )
    m.register_uri(
        'DELETE', 'http://keystone:5000/v3/auth/tokens',
        headers={'X-Subject-Token': "111111111"}
    )
    m.register_uri(
        'POST', 'http://keystone:5000/v3/users?name=testuser&domain_id=default',
        json={"users": {}}
    )
    m.register_uri(
        'GET', 'http://keystone:5000/v3/users?name=testuser&domain_id=default',
        json={"users": {}}
    )
    m.register_uri(
        'POST', 'http://keystone:5000/v3/users/',
        json={"users": [{
            "id": "1111111111111"
        }]}
    )

def register_model_any(m, module_name, mocked_data, key=None):
    if key is None:
        key = module_name
    m.register_uri(
        'GET', 'http://{}:{}/{}'.format(comp_util.CONF['components']['manager']['hostname'],
                                        comp_util.CONF['components']['manager']['port'], module_name),

        json={key: mocked_data}
    )

def register_policy_any(m, policy_id, module_name, mocked_data, key=None):
    if key is None:
        key = module_name
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/{}'.format(comp_util.CONF['components']['manager']['hostname'],
                                                    comp_util.CONF['components']['manager']['port'], 'policies',
                                                    policy_id, module_name),
        json={key: mocked_data}
    )

def register_pdp(m):
    register_model_any(m, 'pdp', data_mock.pdp_mock,'pdps')

def register_meta_rules(m):
    register_model_any(m, 'meta_rules',data_mock.meta_rules_mock)

def register_policies(m):
    register_model_any(m, 'policies', data_mock.policies_mock)


def register_models(m):
    register_model_any(m, 'models', data_mock.models_mock)

def register_policy_subject(m, policy_id):
    register_policy_any(m, policy_id, 'subjects', data_mock.subject_mock[policy_id])


def register_policy_subject_invalid_response(m, policy_id):
    register_policy_any(m, policy_id, 'subjects', data_mock.subject_mock[policy_id],'subjects_invalid_key')

def register_policy_object(m, policy_id):
    register_policy_any(m, policy_id, 'objects', data_mock.object_mock[policy_id])

def register_policy_object_invalid_response(m, policy_id):
    register_policy_any(m, policy_id, 'objects', data_mock.subject_mock[policy_id],'objects_invalid_key')

def register_policy_action(m, policy_id):
    register_policy_any(m, policy_id, 'actions', data_mock.action_mock[policy_id])

def register_policy_action_invalid_response(m, policy_id):
    register_policy_any(m, policy_id, 'actions', data_mock.subject_mock[policy_id],'actions_invalid_key')

def register_policy_subject_assignment_list(m, policy_id):
    register_policy_any(m, policy_id, 'subject_assignments', data_mock.subject_assignment_mock)

def register_policy_object_assignment_list(m, policy_id):
    register_policy_any(m, policy_id, 'object_assignments', data_mock.object_assignment_mock)


def register_policy_action_assignment_list(m, policy_id):
    register_policy_any(m, policy_id, 'action_assignments', data_mock.action_assignment_mock)

def register_policy_subject_assignment(m, policy_id, perimeter_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/subject_assignments/{}'.format(comp_util.CONF['components']['manager']['hostname'],
                                                                  comp_util.CONF['components']['manager']['port'],
                                                                  'policies',
                                                                  policy_id,
                                                                  perimeter_id),
        json={'subject_assignments': data_mock.subject_assignment_mock}
    )

def register_policy_object_assignment(m, policy_id, perimeter_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/object_assignments/{}'.format(comp_util.CONF['components']['manager']['hostname'],
                                                                 comp_util.CONF['components']['manager']['port'],
                                                                 'policies',
                                                                 policy_id,
                                                                 perimeter_id),
        json={'object_assignments': data_mock.object_assignment_mock}
    )

def register_policy_action_assignment(m, policy_id, perimeter_id):
    m.register_uri(
        'GET', 'http://{}:{}/{}/{}/action_assignments/{}'.format(comp_util.CONF['components']['manager']['hostname'],
                                                                 comp_util.CONF['components']['manager']['port'],
                                                                 'policies',
                                                                 policy_id,
                                                                 perimeter_id),
        json={'action_assignments': data_mock.action_assignment_mock}
    )

def register_rules(m, policy_id):
    register_policy_any(m, policy_id, 'rules', data_mock.rules_mock)

# def register_pods(m):
#     m.register_uri(
#         'GET', 'http://{}:{}/pods'.format(comp_util.CONF['components']['orchestrator']['hostname'],
#                                               comp_util.CONF['components']['orchestrator']['port']),
#         json={'pods': data_mock.pods_mock}
#     )
