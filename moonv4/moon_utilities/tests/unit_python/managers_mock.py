import data_mock as data


def mock_managers(m1):
    """ Modify the response from Requests module
    """
    register_pdp(m1)
    register_meta_rules(m1)
    register_policies(m1)
    register_models(m1)
    register_policy_subject(m1, "policy_id_1")
    register_policy_subject(m1, "policy_id_2")
    register_policy_object(m1, "policy_id_1")
    register_policy_object(m1, "policy_id_2")
    register_policy_action(m1, "policy_id_1")
    register_policy_action(m1, "policy_id_2")
    register_policy_subject_assignment(m1, "policy_id_1", "subject_id")
    # register_policy_subject_assignment_list(m1, "policy_id_1")
    register_policy_subject_assignment(m1, "policy_id_2", "subject_id")
    # register_policy_subject_assignment_list(m1, "policy_id_2")
    register_policy_object_assignment(m1, "policy_id_1", "object_id")
    # register_policy_object_assignment_list(m1, "policy_id_1")
    register_policy_object_assignment(m1, "policy_id_2", "object_id")
    # register_policy_object_assignment_list(m1, "policy_id_2")
    register_policy_action_assignment(m1, "policy_id_1", "action_id")
    # register_policy_action_assignment_list(m1, "policy_id_1")
    register_policy_action_assignment(m1, "policy_id_2", "action_id")
    # register_policy_action_assignment_list(m1, "policy_id_2")
    register_rules(m1, "policy_id1")


def register_pdp(m1):
    m1.register_uri(
        'GET', 'http://{}:{}/{}'.format(data.COMPONENTS['manager']['hostname'],
                                        data.COMPONENTS['manager']['port'], 'pdp'),
        json={'pdps': data.pdp_mock}
    )


def register_meta_rules(m1):
    m1.register_uri(
        'GET', 'http://{}:{}/{}'.format(data.COMPONENTS['manager']['hostname'],
                                        data.COMPONENTS['manager']['port'], 'meta_rules'),
        json={'meta_rules': data.meta_rules_mock}
    )


def register_policies(m1):
    m1.register_uri(
        'GET', 'http://{}:{}/{}'.format(data.COMPONENTS['manager']['hostname'],
                                        data.COMPONENTS['manager']['port'], 'policies'),
        json={'policies': data.policies_mock}
    )


def register_models(m1):
    m1.register_uri(
        'GET', 'http://{}:{}/{}'.format(data.COMPONENTS['manager']['hostname'],
                                        data.COMPONENTS['manager']['port'], 'models'),
        json={'models': data.models_mock}
    )


def register_policy_subject(m1, policy_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/subjects'.format(data.COMPONENTS['manager']['hostname'],
                                                    data.COMPONENTS['manager']['port'], 'policies', policy_id),
        json={'subjects': data.subject_mock[policy_id]}
    )


def register_policy_object(m1, policy_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/objects'.format(data.COMPONENTS['manager']['hostname'],
                                                   data.COMPONENTS['manager']['port'], 'policies', policy_id),
        json={'objects': data.object_mock[policy_id]}
    )


def register_policy_action(m1, policy_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/actions'.format(data.COMPONENTS['manager']['hostname'],
                                                   data.COMPONENTS['manager']['port'], 'policies', policy_id),
        json={'actions': data.action_mock[policy_id]}
    )


def register_policy_subject_assignment(m1, policy_id, subj_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/subject_assignments/{}'.format(data.COMPONENTS['manager']['hostname'],
                                                                  data.COMPONENTS['manager']['port'], 'policies',
                                                                  policy_id,
                                                                  subj_id),
        json={'subject_assignments': data.subject_assignment_mock}
    )


def register_policy_subject_assignment_list(m1, policy_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/subject_assignments'.format(data.COMPONENTS['manager']['hostname'],
                                                               data.COMPONENTS['manager']['port'], 'policies',
                                                               policy_id),
        json={'subject_assignments': data.subject_assignment_mock}
    )


def register_policy_object_assignment(m1, policy_id, obj_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/object_assignments/{}'.format(data.COMPONENTS['manager']['hostname'],
                                                                 data.COMPONENTS['manager']['port'], 'policies',
                                                                 policy_id,
                                                                 obj_id),
        json={'object_assignments': data.object_assignment_mock}
    )


def register_policy_object_assignment_list(m1, policy_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/object_assignments'.format(data.COMPONENTS['manager']['hostname'],
                                                              data.COMPONENTS['manager']['port'], 'policies',
                                                              policy_id),
        json={'object_assignments': data.object_assignment_mock}
    )


def register_policy_action_assignment(m1, policy_id, action_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/action_assignments/{}'.format(data.COMPONENTS['manager']['hostname'],
                                                                 data.COMPONENTS['manager']['port'], 'policies',
                                                                 policy_id,
                                                                 action_id),
        json={'action_assignments': data.action_assignment_mock}
    )


def register_policy_action_assignment_list(m1, policy_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/action_assignments'.format(data.COMPONENTS['manager']['hostname'],
                                                              data.COMPONENTS['manager']['port'], 'policies',
                                                              policy_id),
        json={'action_assignments': data.action_assignment_mock}
    )


def register_rules(m1, policy_id):
    m1.register_uri(
        'GET', 'http://{}:{}/{}/{}/{}'.format(data.COMPONENTS['manager']['hostname'],
                                              data.COMPONENTS['manager']['port'], 'policies',
                                              policy_id, 'rules'),
        json={'rules': data.rules_mock}
    )