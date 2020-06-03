# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import pytest
import mock_repo.data as data_mock
import mock_repo.urls as register_urls
import requests
import requests_mock
from moon_utilities import exceptions


def test_authz_request(configuration):
    from moon_cache import cache
    c = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    assert isinstance(c.authz_requests, dict)


# ================================
# tests for get (subject) in cache
# ================================

def test_get_subject_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'subject_name'
    subject_id = cache_obj.get_subject(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert subject_id is not None


def test_get_subject_no_policy(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        cache_obj.get_subject(None, "")
    assert str(exception_info.value) == '400: Policy Unknown'


def test_get_subject_invalid_name(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'invalid name'
    with pytest.raises(exceptions.SubjectUnknown) as exception_info:
        cache_obj.get_subject(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert str(exception_info.value) == '400: Subject Unknown'


def test_get_subject_invalid_response(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'policy_id_invalid_response'
    with pytest.raises(exceptions.SubjectUnknown) as exception_info:
        cache_obj.get_subject(data_mock.shared_ids["policy"]["policy_id_invalid_response"], name)
    assert str(exception_info.value) == '400: Subject Unknown'


# ================================================
# tests for get (object) in cache
# ================================================

def test_get_object_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'object_name'
    object_id = cache_obj.get_object(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert object_id is not None


def test_get_object_no_policy(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        cache_obj.get_object(None, "")
    assert str(exception_info.value) == '400: Policy Unknown'


def test_get_object_invalid_name(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'invalid name'
    with pytest.raises(exceptions.ObjectUnknown) as exception_info:
        cache_obj.get_object(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert str(exception_info.value) == '400: Object Unknown'


def test_get_object_invalid_response(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'policy_id_invalid_response'
    with pytest.raises(exceptions.ObjectUnknown) as exception_info:
        cache_obj.get_object(data_mock.shared_ids["policy"]["policy_id_invalid_response"], name)
    assert str(exception_info.value) == '400: Object Unknown'


# ================================================
# tests for get (action) in cache
# ================================================

def test_get_action_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'action_name'
    action_id = cache_obj.get_action(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert action_id is not None


def test_get_action_no_policy(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        cache_obj.get_action(None, "")
    assert str(exception_info.value) == '400: Policy Unknown'


def test_get_action_invalid_name(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'invalid name'
    with pytest.raises(exceptions.ActionUnknown) as exception_info:
        cache_obj.get_action(data_mock.shared_ids["policy"]["policy_id_1"], name)
    assert str(exception_info.value) == '400: Action Unknown'


def test_get_action_invalid_response(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'policy_id_invalid_response'
    with pytest.raises(exceptions.ActionUnknown) as exception_info:
        cache_obj.get_action(data_mock.shared_ids["policy"]["policy_id_invalid_response"], name)
    assert str(exception_info.value) == '400: Action Unknown'


# ===========================================
# tests for get (subject_assignment) in cache
# ===========================================

def test_get_subject_assignment_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    subject_assignments = cache_obj.get_subject_assignments(
        data_mock.shared_ids["policy"]["policy_id_1"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert subject_assignments is not None


def test_get_subject_assignment_no_policy(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        cache_obj.get_subject_assignments(None,
                                          data_mock.shared_ids["perimeter"]["perimeter_id_1"],
                                          data_mock.shared_ids["category"]["category_id_1"])
    assert str(exception_info.value) == '400: Policy Unknown'


@requests_mock.Mocker(kw='mock')
def test_get_subject_assignment_invalid_subject_id(configuration, **kwargs):
    from moon_cache import cache
    kwargs['mock'].get('{}/policies/{}/subject_assignments/{}'
                       .format(
                            configuration["management"]["url"],
                            data_mock.shared_ids["subject"]["invalid_subject_id"],
                            data_mock.shared_ids["perimeter"]["perimeter_id_1"]),
                       json={
                           'subject_assignments':
                               data_mock.subject_assignment_mock_invalid_subject_id
                       }
                       )
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    subject_assignments = cache_obj.get_subject_assignments(
        data_mock.shared_ids["subject"]["invalid_subject_id"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(subject_assignments) == 0


@requests_mock.Mocker(kw='mock')
def test_get_subject_assignment_invalid_category_id(configuration, **kwargs):
    from moon_cache import cache
    kwargs['mock'].get('{}/policies/{}/subject_assignments/{}'
                       .format(
                                configuration["management"]["url"],
                                data_mock.shared_ids["subject"]["invalid_category_id"],
                                data_mock.shared_ids["perimeter"]["perimeter_id_1"]),
                       json={
                           'subject_assignments':
                               data_mock.subject_assignment_mock_invalid_category_id
                       }
                       )
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    subject_assignments = cache_obj.get_subject_assignments(
        data_mock.shared_ids["subject"]["invalid_category_id"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(subject_assignments) == 0


@requests_mock.Mocker(kw='mock')
def test_get_subject_assignment_invalid_assignment_id(configuration, **kwargs):
    from moon_cache import cache
    kwargs['mock'].get('{}/policies/{}/subject_assignments/{}'
                       .format(
                                configuration["management"]["url"],
                                data_mock.shared_ids["subject"]["invalid_assignment_id"],
                                data_mock.shared_ids["perimeter"]["perimeter_id_1"]),
                       json={
                           'subject_assignments':
                               data_mock.subject_assignment_mock_invalid_assignment_id
                       }
                       )

    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    subject_assignments = cache_obj.get_subject_assignments(
        data_mock.shared_ids["subject"]["invalid_assignment_id"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(subject_assignments) == 0


def test_get_subject_assignment_empty_perimeter(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    subject_assignments = cache_obj.get_subject_assignments(
        data_mock.shared_ids["policy"]["policy_id_2"],
        None,
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(subject_assignments) == 0


def test_get_subject_assignment_invalid_category_failure(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    subject_assignments = cache_obj.get_subject_assignments(
        data_mock.shared_ids["policy"]["policy_id_1"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["invalid_category_id_1"])
    assert len(subject_assignments) == 0


# ==========================================
# tests for get (object_assignment) in cache
# ==========================================

def test_get_object_assignment_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    object_assignments = cache_obj.get_object_assignments(
        data_mock.shared_ids["policy"]["policy_id_1"],
        data_mock.shared_ids["perimeter"]["perimeter_id_2"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert object_assignments is not None


def test_get_object_assignment_no_policy(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        cache_obj.get_object_assignments(None,
                                         data_mock.shared_ids["perimeter"]["perimeter_id_2"],
                                         data_mock.shared_ids["category"]["category_id_1"])
    assert str(exception_info.value) == '400: Policy Unknown'


@requests_mock.Mocker(kw='mock')
def test_get_object_assignment_invalid_object_id(configuration, **kwargs):
    from moon_cache import cache
    kwargs['mock'].get('{}/policies/{}/object_assignments/{}'
                       .format(configuration["management"]["url"],
                               data_mock.shared_ids["object"]["invalid_object_id"],
                               data_mock.shared_ids["perimeter"]["perimeter_id_1"]),
                       json={
                           'object_assignments':
                               data_mock.object_assignment_mock_invalid_object_id
                       }
                       )
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    object_assignments = cache_obj.get_object_assignments(
        data_mock.shared_ids["object"]["invalid_object_id"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(object_assignments) == 0


@requests_mock.Mocker(kw='mock')
def test_get_object_assignment_invalid_category_id(configuration, **kwargs):
    from moon_cache import cache
    kwargs['mock'].get('{}/policies/{}/object_assignments/{}'
                       .format(configuration["management"]["url"],
                               data_mock.shared_ids["object"]["invalid_category_id"],
                               data_mock.shared_ids["perimeter"]["perimeter_id_1"]),
                       json={
                           'object_assignments':
                               data_mock.object_assignment_mock_invalid_category_id
                       }
                       )
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    object_assignments = cache_obj.get_object_assignments(
        data_mock.shared_ids["object"]["invalid_category_id"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(object_assignments) == 0


@requests_mock.Mocker(kw='mock')
def test_get_object_assignment_invalid_assignment_id(configuration, **kwargs):
    from moon_cache import cache
    kwargs['mock'].get('{}/policies/{}/object_assignments/{}'
                       .format(configuration["management"]["url"],
                               data_mock.shared_ids["object"]["invalid_assignment_id"],
                               data_mock.shared_ids["perimeter"]["perimeter_id_1"]),
                       json={
                           'object_assignments':
                               data_mock.object_assignment_mock_invalid_assignment_id
                       }
                       )

    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    object_assignments = cache_obj.get_object_assignments(
        data_mock.shared_ids["object"]["invalid_assignment_id"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(object_assignments) == 0


def test_get_object_assignment_none_perimeter(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    object_assignments = cache_obj.get_object_assignments(
        data_mock.shared_ids["policy"]["policy_id_2"],
        None,
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(object_assignments) == 0


def test_get_object_assignment_invalid_category_failure(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    object_assignments = cache_obj.get_object_assignments(
        data_mock.shared_ids["policy"]["policy_id_1"],
        data_mock.shared_ids["perimeter"]["perimeter_id_2"],
        data_mock.shared_ids["category"]["invalid_category_id_1"])
    assert len(object_assignments) == 0


# ==========================================
#  tests for get (action_assignment) in cache
# ==========================================

def test_get_action_assignment_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    action_assignments = cache_obj.get_action_assignments(
        data_mock.shared_ids["policy"]["policy_id_1"],
        data_mock.shared_ids["perimeter"]["perimeter_id_3"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert action_assignments is not None


def test_get_action_assignment_no_policy(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    with pytest.raises(exceptions.PolicyUnknown) as exception_info:
        cache_obj.get_action_assignments(None,
                                         data_mock.shared_ids["perimeter"]["perimeter_id_2"],
                                         data_mock.shared_ids["category"]["category_id_1"])
    assert str(exception_info.value) == '400: Policy Unknown'


@requests_mock.Mocker(kw='mock')
def test_get_action_assignment_invalid_object_id(configuration, **kwargs):
    from moon_cache import cache
    kwargs['mock'].get('{}/policies/{}/action_assignments/{}'
                       .format(configuration["management"]["url"],
                               data_mock.shared_ids["action"]["invalid_action_id"],
                               data_mock.shared_ids["perimeter"]["perimeter_id_1"]),
                       json={
                           'action_assignments':
                               data_mock.action_assignment_mock_invalid_action_id
                       }
                       )
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    action_assignments = cache_obj.get_action_assignments(
        data_mock.shared_ids["action"]["invalid_action_id"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(action_assignments) == 0


@requests_mock.Mocker(kw='mock')
def test_get_action_assignment_invalid_category_id(configuration, **kwargs):
    from moon_cache import cache
    kwargs['mock'].get('{}/policies/{}/action_assignments/{}'
                       .format(configuration["management"]["url"],
                               data_mock.shared_ids["action"]["invalid_category_id"],
                               data_mock.shared_ids["perimeter"]["perimeter_id_1"]),
                       json={
                           'action_assignments':
                               data_mock.action_assignment_mock_invalid_category_id
                       }
                       )
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    action_assignments = cache_obj.get_action_assignments(
        data_mock.shared_ids["action"]["invalid_category_id"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(action_assignments) == 0


@requests_mock.Mocker(kw='mock')
def test_get_action_assignment_invalid_assignment_id(configuration, **kwargs):
    from moon_cache import cache
    kwargs['mock'].get('{}/policies/{}/action_assignments/{}'
                       .format(configuration["management"]["url"],
                               data_mock.shared_ids["action"]["invalid_assignment_id"],
                               data_mock.shared_ids["perimeter"]["perimeter_id_1"]),
                       json={
                           'action_assignments':
                               data_mock.action_assignment_mock_invalid_assignment_id
                       }
                       )

    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    action_assignments = cache_obj.get_action_assignments(
        data_mock.shared_ids["action"]["invalid_assignment_id"],
        data_mock.shared_ids["perimeter"]["perimeter_id_1"],
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(action_assignments) == 0


def test_get_action_assignment_none_perimeter(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    action_assignments = cache_obj.get_action_assignments(
        data_mock.shared_ids["policy"]["policy_id_2"],
        None,
        data_mock.shared_ids["category"]["category_id_1"])
    assert len(action_assignments) == 0


def test_get_action_assignment_invalid_category_failure(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    action_assignments = cache_obj.get_action_assignments(
        data_mock.shared_ids["policy"]["policy_id_1"],
        data_mock.shared_ids["perimeter"]["perimeter_id_3"],
        data_mock.shared_ids["category"]["invalid_category_id_1"])
    assert len(action_assignments) == 0


# ==================================
# tests for helper function in cache
# ==================================

def test_get_policy_from_meta_rules_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration.get("management")['url'])
    policy_id = cache_obj.get_policy_from_meta_rules(
        data_mock.shared_ids["meta_rule"]["meta_rule_id_1"])
    assert policy_id is not None


''' tests for containers function , security pipeline in cache which not used for now 
     need to mock pdp object, /pods correctly
'''


def test_get_policy_from_meta_rules_failure(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration.get("management")['url'])
    meta_rule_id = 'meta_rule_id3'
    policy_id = cache_obj.get_policy_from_meta_rules(meta_rule_id)
    assert policy_id is None


def test_get_pdp_from_vim_project_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration.get("management")['url'])
    vim_project_id = 'vim_project_id1'
    pdp_key = cache_obj.get_pdp_from_vim_project(vim_project_id)
    assert pdp_key is not None


def test_get_pdp_from_vim_project_failure(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration.get("management")['url'])
    vim_project_id = 'vim_project_id2'
    pdp_key = cache_obj.get_pdp_from_vim_project(vim_project_id)
    assert pdp_key is None


def test_get_vim_project_id_from_policy_id_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration.get("management")['url'])
    vim_project_id = cache_obj.get_vim_project_id_from_policy_id(
        data_mock.shared_ids["policy"]["policy_id_1"])
    assert vim_project_id is not None


def test_get_vim_project_id_from_policy_id_failure(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration.get("management")['url'])
    policy_id = 'policy_id_3'
    vim_project_id = cache_obj.get_vim_project_id_from_policy_id(policy_id)
    assert vim_project_id is None


def test_get_pipeline_url(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration.get("management")['url'])
    cache_obj.set_current_server(url="http://127.0.0.1:10000", api_key="")
    cache_obj.add_pipeline("policy_id_1", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20000,
                         })
    cache_obj.add_pipeline("policy_id_2", {
                             "name": "test",
                             "description": "test",
                             "host": "127.0.0.1",
                             "port": 20001,
                         })
    url = cache_obj.get_pipeline_url(pipeline_id="policy_id_1")
    assert url == "http://127.0.0.1:20000"
    url = cache_obj.get_pipeline_url(pipeline_id="policy_id_2")
    assert url == "http://127.0.0.1:20001"
