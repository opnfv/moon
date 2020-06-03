# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import mock_repo.data as data_mock


def register_model_any(m, conf, module_name, mocked_data, key=None):
    if key is None:
        key = module_name
    m.register_uri(
        'GET', '{}/{}'.format(conf['management']['url'],
                              module_name),

        json={key: mocked_data}
    )


def register_policy_any(m, conf, policy_id, module_name, mocked_data, key=None):
    if key is None:
        key = module_name
    m.register_uri(
        'GET', '{}/{}/{}/{}'.format(conf['management']['url'],
                                    'policies',
                                    policy_id,
                                    module_name),
        json={key: mocked_data}
    )


def register_policy(m, conf, policy_id, mocked_data):
    m.register_uri(
        'GET', '{}/{}/{}'.format(conf['management']['url'],
                                    'policies',
                                    policy_id),
        json={"policies": mocked_data}
    )


def register_pipelines(m, conf):
    m.register_uri(
        'GET', 'http://127.0.0.1:20000/pipelines/policy_id_1',
        json={'pipelines': data_mock.pipelines_mock}
    )


def register_slaves(m, conf):
    m.register_uri(
        'GET', 'http://127.0.0.1:10000/pipelines',
        json={'pipelines': data_mock.pipelines_mock}
    )


def register_pdp(m, conf):
    register_model_any(m, conf, 'pdp', data_mock.pdp_mock, 'pdps')


def register_meta_rules(m, conf):
    register_model_any(m, conf, 'meta_rules', data_mock.meta_rules_mock)


def register_policies(m, conf):
    for _policy_id in data_mock.policies_mock:
        register_policy(m, conf, _policy_id, data_mock.policies_mock[_policy_id])
    register_model_any(m, conf, 'policies', data_mock.policies_mock)


def register_models(m, conf):
    register_model_any(m, conf, 'models', data_mock.models_mock)


def register_policy_subject(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'subjects', data_mock.subject_mock[policy_id])


def register_policy_subject_invalid_response(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'subjects', data_mock.subject_mock[policy_id],
                        'subjects_invalid_key')


def register_policy_object(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'objects', data_mock.object_mock[policy_id])


def register_policy_object_invalid_response(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'objects', data_mock.subject_mock[policy_id],
                        'objects_invalid_key')


def register_policy_action(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'actions', data_mock.action_mock[policy_id])


def register_policy_action_invalid_response(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'actions', data_mock.subject_mock[policy_id],
                        'actions_invalid_key')


def register_policy_subject_assignment_list(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'subject_assignments',
                        data_mock.subject_assignment_mock)


def register_policy_object_assignment_list(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'object_assignments',
                        data_mock.object_assignment_mock)


def register_policy_action_assignment_list(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'action_assignments',
                        data_mock.action_assignment_mock)


def register_policy_subject_assignment(m, conf, policy_id, perimeter_id):
    m.register_uri(
        'GET', '{}/{}/{}/subject_assignments/{}'.format(conf['management']['url'],
                                                        'policies',
                                                        policy_id,
                                                        perimeter_id),
        json={'subject_assignments': data_mock.subject_assignment_mock}
    )


def register_policy_object_assignment(m, conf, policy_id, perimeter_id):
    m.register_uri(
        'GET', '{}/{}/{}/object_assignments/{}'.format(conf['management']['url'],
                                                       'policies',
                                                       policy_id,
                                                       perimeter_id),
        json={'object_assignments': data_mock.object_assignment_mock}
    )


def register_policy_action_assignment(m, conf, policy_id, perimeter_id):
    m.register_uri(
        'GET', '{}/{}/{}/action_assignments/{}'.format(conf['management']['url'],
                                                       'policies',
                                                       policy_id,
                                                       perimeter_id),
        json={'action_assignments': data_mock.action_assignment_mock}
    )


def register_rules(m, conf, policy_id):
    register_policy_any(m, conf, policy_id, 'rules', data_mock.rules_mock)


def register_attributes(m, conf):
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/attributes/mode',
        json={
            'attributes': {
                'id': 'mode', 'value': 'build', 'values': ['build', 'run'], 'default': 'run'
            }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/attributes',
        json={
            'attributes': {
                'mode': {
                    'id': 'mode', 'value': 'build', 'values': ['build', 'run'], 'default': 'run'}
            }
        }
    )

