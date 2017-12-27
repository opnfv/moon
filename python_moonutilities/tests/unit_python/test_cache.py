import pytest
import mock_repo.data as data_mock


def test_authz_request():
    from python_moonutilities import cache
    c = cache.Cache()
    assert isinstance(c.authz_requests, dict)


# tests for get (subject, object, action) in cache
# ================================================
def test_get_subject_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    name = 'subject_name'
    subject_id = cache_obj.get_subject(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert subject_id is not None


def test_get_subject_not_found():
    from python_moonutilities import cache
    cache_obj2 = cache.Cache()
    name = 'invalid name'
    with pytest.raises(Exception) as exception_info:
        cache_obj2.get_subject(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert str(exception_info.value) == '400: Subject Unknown'


# [TODO] this test used to test the invalid response
# it should be un commented and run after refactoring the related part
def test_get_subject_invalid_response():
    from python_moonutilities import cache
    cache_obj2 = cache.Cache()
    # policy_id = 'policy_id_invalid_response'
    name = 'invalid name'


#   with pytest.raises(Exception) as exception_info:
#       cache_obj2.get_subject(data_mock.shared_ids["policy"]["policy_id_invalid_response"], name)
#   assert str(exception_info.value) == '400: Subject Unknown'


def test_get_object_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    name = 'object_name'
    object_id = cache_obj.get_object(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert object_id is not None


def test_get_object_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    name = 'invalid name'
    with pytest.raises(Exception) as exception_info:
        cache_obj.get_object(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert str(exception_info.value) == '400: Subject Unknown'


def test_get_action_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    name = 'action_name'
    action_id = cache_obj.get_action(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert action_id is not None


def test_get_action_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    name = 'invalid name'
    with pytest.raises(Exception) as exception_info:
        cache_obj.get_action(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert str(exception_info.value) == '400: Subject Unknown'


# ====================================================================================================

# tests for get (subject_assignment, object_assignment, action_assignment) in cache
# =================================================================================

def test_get_subject_assignment_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    subject_assignments = cache_obj.get_subject_assignments(data_mock.shared_ids["policy"]["policy_id_1"],
                                                            data_mock.shared_ids["perimeter"]["perimeter_id_1"],
                                                            data_mock.shared_ids["category"]["category_id_1"])
    assert subject_assignments is not None


def test_get_subject_assignment_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    subject_assignments = cache_obj.get_subject_assignments(data_mock.shared_ids["policy"]["policy_id_2"],
                                                            '',
                                                            data_mock.shared_ids["category"]["category_id_1"])
    assert len(subject_assignments) == 0


def test_get_subject_assignment_invalid_category_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    subject_assignments = cache_obj.get_subject_assignments(data_mock.shared_ids["policy"]["policy_id_1"],
                                                            data_mock.shared_ids["perimeter"]["perimeter_id_1"],
                                                            data_mock.shared_ids["category"]["invalid_category_id_1"])
    assert len(subject_assignments) == 0


def test_get_object_assignment_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    object_assignments = cache_obj.get_object_assignments(data_mock.shared_ids["policy"]["policy_id_1"],
                                                          data_mock.shared_ids["perimeter"]["perimeter_id_2"],
                                                          data_mock.shared_ids["category"]["category_id_1"])
    assert object_assignments is not None


def test_get_object_assignment_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    object_assignments = cache_obj.get_object_assignments(data_mock.shared_ids["policy"]["policy_id_2"],
                                                          '',
                                                          data_mock.shared_ids["category"]["category_id_1"])
    assert len(object_assignments) == 0


def test_get_object_assignment_invalid_category_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    object_assignments = cache_obj.get_object_assignments(data_mock.shared_ids["policy"]["policy_id_1"],
                                                          data_mock.shared_ids["perimeter"]["perimeter_id_1"],
                                                          data_mock.shared_ids["category"]["invalid_category_id_1"])
    assert len(object_assignments) == 0


def test_get_action_assignment_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    action_assignments = cache_obj.get_action_assignments(data_mock.shared_ids["policy"]["policy_id_1"],
                                                          data_mock.shared_ids["perimeter"]["perimeter_id_3"],
                                                          data_mock.shared_ids["category"]["category_id_1"])
    assert action_assignments is not None


def test_get_action_assignment_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    action_assignments = cache_obj.get_action_assignments(data_mock.shared_ids["policy"]["policy_id_2"],
                                                          '',
                                                          data_mock.shared_ids["category"]["category_id_1"])
    assert len(action_assignments) == 0


def test_get_action_assignment_invalid_category_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    action_assignments = cache_obj.get_action_assignments(data_mock.shared_ids["policy"]["policy_id_1"],
                                                          data_mock.shared_ids["perimeter"]["perimeter_id_1"],
                                                          data_mock.shared_ids["category"]["invalid_category_id_1"])
    assert len(action_assignments) == 0


# ====================================================================================================

# tests for helper function in cache
# ==================================
def test_get_policy_from_meta_rules_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    policy_id = cache_obj.get_policy_from_meta_rules(data_mock.shared_ids["meta_rule"]["meta_rule_id_1"])
    assert policy_id is not None


# def test_get_policy_from_meta_rules_failure():
#     from python_moonutilities import cache
#     cache_obj = cache.Cache()
#     meta_rule_id = 'meta_rule_id3'
#     policy_id = cache_obj.get_policy_from_meta_rules(meta_rule_id)
#     assert policy_id is None


def test_get_pdp_from_keystone_project_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    keystone_project_id = 'keystone_project_id1'
    pdp_key = cache_obj.get_pdp_from_keystone_project(keystone_project_id)
    assert pdp_key is not None


def test_get_pdp_from_keystone_project_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    keystone_project_id = 'keystone_project_id2'
    pdp_key = cache_obj.get_pdp_from_keystone_project(keystone_project_id)
    assert pdp_key is None


def test_get_keystone_project_id_from_policy_id_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    keystone_project_id = cache_obj.get_keystone_project_id_from_policy_id(
        data_mock.shared_ids["policy"]["policy_id_1"])
    assert keystone_project_id is not None


def test_get_keystone_project_id_from_policy_id_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    policy_id = 'policy_id_3'
    keystone_project_id = cache_obj.get_keystone_project_id_from_policy_id(policy_id)
    assert keystone_project_id is None


# def test_get_containers_from_keystone_project_id_success():
#     from python_moonutilities import cache
#     cache_obj = cache.Cache()
#     keystone_project_id = 1
#     meta_rule_id = 'meta_rule_id1'
#     container_id, container_value = cache_obj.get_containers_from_keystone_project_id(keystone_project_id, meta_rule_id)
#     assert container_id, container_value is not None


def test_cache_manager():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    assert cache_obj.pdp is not None
    assert cache_obj.meta_rules is not None
    assert len(cache_obj.meta_rules) == 2
    assert cache_obj.policies is not None
    assert len(cache_obj.policies) == 1
    assert cache_obj.models is not None
