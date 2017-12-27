import pytest


def test_authz_request():
    from python_moonutilities import cache
    c = cache.Cache()
    assert isinstance(c.authz_requests, dict)


def test_get_subject_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    policy_id = 'policy_id_1'
    name = 'subject_name'
    subject_id = cache_obj.get_subject(policy_id, name)
    assert subject_id is not None


def test_get_subject_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    policy_id = 'policy_id_1'
    name = 'invalid name'
    with pytest.raises(Exception) as exception_info:
        cache_obj.get_subject(policy_id, name)
    assert str(exception_info.value) == '400: Subject Unknown'


def test_get_object_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    policy_id = 'policy_id_1'
    name = 'object_name'
    object_id = cache_obj.get_object(policy_id, name)
    assert object_id is not None


def test_get_object_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    policy_id = 'policy_id_1'
    name = 'invalid name'
    with pytest.raises(Exception) as exception_info:
        cache_obj.get_object(policy_id, name)
    assert str(exception_info.value) == '400: Object Unknown'


def test_get_action_success():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    policy_id = 'policy_id_1'
    name = 'action_name'
    action_id = cache_obj.get_action(policy_id, name)
    assert action_id is not None


def test_get_action_failure():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    policy_id = 'policy_id_1'
    name = 'invalid name'
    with pytest.raises(Exception) as exception_info:
        cache_obj.get_action(policy_id, name)
    assert str(exception_info.value) == '400: Action Unknown'


def test_cache_manager():
    from python_moonutilities import cache
    cache_obj = cache.Cache()
    assert cache_obj.pdp is not None
    assert cache_obj.meta_rules is not None
    assert len(cache_obj.meta_rules) == 2
    assert cache_obj.policies is not None
    assert len(cache_obj.policies) == 2
    assert cache_obj.models is not None