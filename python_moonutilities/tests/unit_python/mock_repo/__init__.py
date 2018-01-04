import mock_repo.urls as register_urls
import mock_repo.data as data_mock


def register_cache(m):
    """ Modify the response from Requests module
    """
    register_urls.register_components(m)
    register_urls.register_keystone(m)

    register_urls.register_pdp(m)
    register_urls.register_meta_rules(m)
    register_urls.register_policies(m)
    register_urls.register_models(m)

    register_urls.register_policy_subject(m, data_mock.shared_ids["policy"]["policy_id_1"])
    register_urls.register_policy_subject_invalid_response(m, data_mock.shared_ids["policy"]["policy_id_invalid_response"])

    register_urls.register_policy_object(m, data_mock.shared_ids["policy"]["policy_id_1"])
    register_urls.register_policy_object_invalid_response(m, data_mock.shared_ids["policy"]["policy_id_invalid_response"])

    register_urls.register_policy_action(m, data_mock.shared_ids["policy"]["policy_id_1"])
    register_urls.register_policy_action_invalid_response(m, data_mock.shared_ids["policy"]["policy_id_invalid_response"])

    register_urls.register_policy_subject_assignment(m, data_mock.shared_ids["policy"]["policy_id_1"], data_mock.shared_ids["perimeter"]["perimeter_id_1"])

    register_urls.register_policy_subject_assignment_list(m, data_mock.shared_ids["policy"]["policy_id_2"])

    register_urls.register_policy_object_assignment(m, data_mock.shared_ids["policy"]["policy_id_1"], data_mock.shared_ids["perimeter"]["perimeter_id_2"])

    register_urls.register_policy_object_assignment_list(m, data_mock.shared_ids["policy"]["policy_id_2"])

    register_urls.register_policy_action_assignment(m, data_mock.shared_ids["policy"]["policy_id_1"], data_mock.shared_ids["perimeter"]["perimeter_id_3"])

    register_urls.register_policy_action_assignment_list(m, data_mock.shared_ids["policy"]["policy_id_2"])
    # register_urls.register_pods(m)

    # register_urls.register_policy_action_assignment(m, "policy_id_2", "perimeter_id_2")
    # register_urls.register_policy_action_assignment(m, "policy_id_2", "perimeter_id_2")
    # register_urls.register_policy_action_assignment(m, "policy_id_2", "perimeter_id_2")

    register_urls.register_rules(m, "policy_id1")
