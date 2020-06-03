# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
import requests
from uuid import uuid4


def test_pipeline_update_policy_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = response.json()
    key = next(iter(policies['policies']))
    policies['policies'][key]['name'] = "new " + policies['policies'][key]['name']
    req = hug.test.put(update, "/update/policy/{}".format(key),
                       policies['policies'][key], headers=auth_headers)
    assert req.status == hug.HTTP_208


def test_pipeline_update_policy_not_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = response.json()
    key = next(iter(policies['policies']))
    policies['policies'][key]['name'] = "new " + policies['policies'][key]['name']
    req = hug.test.put(update, "/update/policy/{}".format(uuid4().hex),
                       policies['policies'][key], headers=auth_headers)
    assert req.status == hug.HTTP_208


def test_pipeline_delete_policy():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    policies = response.json()
    key = next(iter(policies['policies']))
    req = hug.test.delete(update, "/update/policy/{}".format(key),
                          headers=auth_headers)
    assert req.status == hug.HTTP_202


def test_pipeline_update_pdp_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/pdp".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    pdps = response.json()
    key = next(iter(pdps['pdps']))
    pdps['pdps'][key]['name'] = "new " + pdps['pdps'][key]['name']
    req = hug.test.put(update, "/update/pdp/{}".format(key),
                       pdps['pdps'][key], headers=auth_headers)
    assert req.status == hug.HTTP_208


def test_pipeline_update_pdp_not_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/pdp".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    pdps = response.json()
    key = next(iter(pdps['pdps']))
    pdps['pdps'][key]['name'] = "new " + pdps['pdps'][key]['name']
    req = hug.test.put(update, "/update/pdp/{}".format(uuid4().hex),
                       pdps['pdps'][key], headers=auth_headers)
    assert req.status == hug.HTTP_208


def test_pipeline_delete_pdp_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/pdp".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    pdps = response.json()
    key = next(iter(pdps['pdps']))
    req = hug.test.delete(update, "/update/pdp/{}".format(key), headers=auth_headers)
    assert req.status == hug.HTTP_202


def test_pipeline_update_perimeter_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = response.json()
    policy_key = next(iter(policies['policies']))

    subject_response = requests.get("{}/policies/{}/subjects".format(get_configuration(
        "management").get("url"), policy_key), headers=auth_headers)
    subjects = subject_response.json()
    subj_key = next(iter(subjects['subjects']))
    subjects['subjects'][subj_key]['name'] = "updated_" + subjects['subjects'][subj_key]['name']

    subject_req = hug.test.put(update, "/update/perimeter/{}/{}/{}".format(subj_key, policy_key,
                                                                           "subject"),
                               subjects['subjects'][subj_key], headers=auth_headers)
    assert subject_req.status == hug.HTTP_208

    """  object category """
    object_response = requests.get("{}/policies/{}/objects".format(get_configuration(
        "management").get("url"), policy_key), headers=auth_headers)
    objects = object_response.json()
    obj_key = next(iter(objects['objects']))
    objects['objects'][obj_key]['name'] = "updated_" + objects['objects'][obj_key]['name']

    object_req = hug.test.put(update, "/update/perimeter/{}/{}/{}".format(obj_key, policy_key, "object")
                              , objects['objects'][obj_key], headers=auth_headers)
    assert object_req.status == hug.HTTP_208

    """  action category """
    action_response = requests.get("{}/policies/{}/actions".format(get_configuration(
        "management").get("url"), policy_key), headers=auth_headers)
    actions = action_response.json()
    action_key = next(iter(actions['actions']))
    actions['actions'][action_key]['name'] = "updated_" + actions['actions'][action_key]['name']

    action_req = hug.test.put(update, "/update/perimeter/{}/{}/{}".format(action_key, policy_key,
                                                                          "action"),
                              actions['actions'][action_key], headers=auth_headers)
    assert action_req.status == hug.HTTP_208


def test_pipeline_update_perimeter_not_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = response.json()
    policy_key = next(iter(policies['policies']))

    subject_response = requests.get("{}/policies/{}/subjects".format(get_configuration(
        "management").get("url"), policy_key), headers=auth_headers)
    subjects = subject_response.json()
    subj_key = next(iter(subjects['subjects']))
    subjects['subjects'][subj_key]['name'] = "updated_" + subjects['subjects'][subj_key]['name']

    subject_req = hug.test.put(update, "/update/perimeter/{}/{}/{}".format(uuid4().hex, policy_key,
                                                                           "subject"),
                               subjects['subjects'][subj_key], headers=auth_headers)
    assert subject_req.status == hug.HTTP_208

    """  object category """
    object_response = requests.get("{}/policies/{}/objects".format(get_configuration(
        "management").get("url"), policy_key), headers=auth_headers)
    objects = object_response.json()
    obj_key = next(iter(objects['objects']))
    objects['objects'][obj_key]['name'] = "updated_" + objects['objects'][obj_key]['name']

    object_req = hug.test.put(update, "/update/perimeter/{}/{}/{}".format(uuid4().hex, policy_key, "object")
                              , objects['objects'][obj_key], headers=auth_headers)
    assert object_req.status == hug.HTTP_208

    """  action category """
    action_response = requests.get("{}/policies/{}/actions".format(get_configuration(
        "management").get("url"), policy_key), headers=auth_headers)
    actions = action_response.json()
    action_key = next(iter(actions['actions']))
    actions['actions'][action_key]['name'] = "updated_" + actions['actions'][action_key]['name']

    action_req = hug.test.put(update, "/update/perimeter/{}/{}/{}".format(uuid4().hex, policy_key,
                                                                          "action"),
                              actions['actions'][action_key], headers=auth_headers)
    assert action_req.status == hug.HTTP_208


def test_pipeline_delete_perimeter_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    policies_response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = policies_response.json()
    policy_key = next(iter(policies['policies']))

    subject_response = requests.get("{}/policies/{}/subjects".format(get_configuration(
        "management").get("url"), policy_key), headers=auth_headers)
    subjects = subject_response.json()
    subj_key = next(iter(subjects['subjects']))
    subjects['subjects'][subj_key]['name'] = "updated_" + subjects['subjects'][subj_key]['name']

    delete_subject_response = hug.test.delete(update, "/update/perimeter/{}/{}/{}".format(subj_key, policy_key,
                                                                                          "subject"),
                                              headers=auth_headers)
    assert delete_subject_response.status == hug.HTTP_202

    object_response = requests.get("{}/policies/{}/objects".format(get_configuration(
        "management").get("url"), policy_key), headers=auth_headers)
    objects = object_response.json()
    assert 'objects' in objects and len(objects['objects'])

    for key in objects['objects']:
        delete_object_response = hug.test.delete(update, "/update/perimeter/{}/{}/{}".format(key, policy_key, 'object'),
                                                 headers=auth_headers)
        assert delete_object_response.status == hug.HTTP_202

    action_response = requests.get("{}/policies/{}/actions".format(get_configuration(
        "management").get("url"), policy_key), headers=auth_headers)
    actions = action_response.json()
    assert 'actions' in actions and len(actions['actions'])

    for key in actions['actions']:
        delete_action_response = hug.test.delete(update, "/update/perimeter/{}/{}/{}".format(key, policy_key, 'action'),
                                                 headers=auth_headers)
        assert delete_action_response.status == hug.HTTP_202


def test_pipeline_delete_assignments():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)
    policies = response.json()
    policy_id = next(iter(policies['policies']))

    sub_assig_response = requests.get("{}/policies/{}/subject_assignments".format(get_configuration("management").get("url"),
                                                                                  policy_id), headers=auth_headers)

    subject_assignments = sub_assig_response.json()
    assert 'subject_assignments' in subject_assignments and len(
        subject_assignments['subject_assignments'])
    req = hug.test.delete(update,
                          "/update/assignment/{}/{}/".format(policy_id, "subject"),
                          headers=auth_headers)
    assert req.status == hug.HTTP_202

    obj_assig_response = requests.get("{}/policies/{}/object_assignments".format(get_configuration(
        "management").get("url"), policy_id),
        headers=auth_headers)
    object_assignments = obj_assig_response.json()
    assert 'object_assignments' in object_assignments and len(
        object_assignments['object_assignments'])
    req = hug.test.delete(update,
                          "/update/assignment/{}/{}/".format(policy_id, "object"),
                          headers=auth_headers)
    assert req.status == hug.HTTP_202

    action_assig_response = requests.get("{}/policies/{}/action_assignments".format(get_configuration(
        "management").get("url"), policy_id),
        headers=auth_headers)
    action_assignments = action_assig_response.json()
    assert 'action_assignments' in action_assignments and len(
        action_assignments['action_assignments'])
    req = hug.test.delete(update,
                          "/update/assignment/{}/{}/".format(policy_id, "action"),
                          headers=auth_headers)
    assert req.status == hug.HTTP_202


def test_pipeline_delete_rule():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    policy_response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                                   headers=auth_headers)
    policies = policy_response.json()
    policy_id = next(iter(policies['policies']))

    rules_response = requests.get(
        "{}/policies/{}/rules".format(get_configuration("management").get("url"), policy_id),
        headers=auth_headers)
    rules = rules_response.json()

    assert len(rules['rules']['rules'])
    for i in range(0, len(rules['rules']['rules'])):
        req = hug.test.delete(update, "/update/rule/{}/{}".format(policy_id, rules['rules'][
            'rules'][i]['id']), headers=auth_headers)
        assert req.status == hug.HTTP_202


def test_pipeline_update_model_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    model_response = requests.get("{}/models".format(get_configuration("management").get("url")),
                                  headers=auth_headers)

    models = model_response.json()
    key = next(iter(models['models']))
    models['models'][key]['name'] = "new " + models['models'][key]['name']
    req = hug.test.put(update, "/update/model/{}".format(key),
                       models['models'][key], headers=auth_headers)
    assert req.status == hug.HTTP_208


def test_pipeline_update_model_not_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    model_response = requests.get("{}/models".format(get_configuration("management").get("url")),
                                  headers=auth_headers)

    models = model_response.json()
    key = next(iter(models['models']))
    models['models'][key]['name'] = "new " + models['models'][key]['name']
    req = hug.test.put(update, "/update/model/{}".format(uuid4().hex),
                       models['models'][key], headers=auth_headers)
    assert req.status == hug.HTTP_208


def test_pipeline_delete_model_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    model_response = requests.get("{}/models".format(get_configuration("management").get("url")),
                                  headers=auth_headers)

    models = model_response.json()
    key = next(iter(models['models']))
    req = hug.test.delete(update, "/update/model/{}".format(key), headers=auth_headers)
    assert req.status == hug.HTTP_202


def test_pipeline_delete_category():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    subject_cat_response = requests.get("{}/subject_categories".format(get_configuration(
        "management").get("url")), headers=auth_headers)
    subject_categories = subject_cat_response.json()
    category_id = next(iter(subject_categories['subject_categories']))
    req = hug.test.delete(update, "/update/meta_data/{}/{}".format(category_id, 'subject'),
                          headers=auth_headers)
    assert req.status == hug.HTTP_202

    action_cat_response = requests.get("{}/action_categories".format(get_configuration(
        "management").get("url")),
        headers=auth_headers)
    action_categories = action_cat_response.json()
    category_id = next(iter(action_categories['action_categories']))
    req = hug.test.delete(update, "/update/meta_data/{}/{}".format(category_id, 'action'),
                          headers=auth_headers)
    assert req.status == hug.HTTP_202

    obj_cat_response = requests.get("{}/object_categories".format(get_configuration(
        "management").get("url")),
        headers=auth_headers)
    object_categories = obj_cat_response.json()
    category_id = next(iter(object_categories['object_categories']))
    req = hug.test.delete(update, "/update/meta_data/{}/{}".format(category_id, 'object'),
                          headers=auth_headers)
    assert req.status == hug.HTTP_202


def test_pipeline_update_meta_rule_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    meta_rules_response = requests.get("{}/meta_rules".format(get_configuration("management").get("url")),
                                       headers=auth_headers)

    meta_rules = meta_rules_response.json()
    key = next(iter(meta_rules['meta_rules']))
    meta_rules['meta_rules'][key]['name'] = "new " + meta_rules['meta_rules'][key]['name']
    req = hug.test.put(update, "/update/meta_rule/{}".format(key),
                       meta_rules['meta_rules'][key], headers=auth_headers)
    assert req.status == hug.HTTP_208


def test_pipeline_update_meta_rule_not_existed():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    meta_rules_response = requests.get("{}/meta_rules".format(get_configuration("management").get("url")),
                                       headers=auth_headers)

    meta_rules = meta_rules_response.json()
    key = next(iter(meta_rules['meta_rules']))
    meta_rules['meta_rules'][key]['name'] = "new " + meta_rules['meta_rules'][key]['name']
    req = hug.test.put(update, "/update/meta_rule/{}".format(uuid4().hex),
                       meta_rules['meta_rules'][key], headers=auth_headers)
    assert req.status == hug.HTTP_208


def test_pipeline_delete_meta_rule():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    meta_rules_response = requests.get("{}/meta_rules".format(get_configuration("management").get("url")),
                                       headers=auth_headers)

    meta_rules = meta_rules_response.json()
    key = next(iter(meta_rules['meta_rules']))
    req = hug.test.delete(update, "/update/meta_rule/{}".format(key), headers=auth_headers)
    assert req.status == hug.HTTP_202


def test_pipeline_delete_data():
    from moon_engine.api.pipeline import update
    from moon_utilities.auth_functions import get_api_key_for_user
    from moon_engine.api.configuration import get_configuration

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    policies_response = requests.get("{}/policies".format(get_configuration("management").get("url")),
                            headers=auth_headers)

    policies = policies_response.json()
    policy_id = next(iter(policies['policies']))

    subject_data_response = requests.get(
        "{}/policies/{}/subject_data".format(get_configuration("management").get("url"), policy_id),
        headers=auth_headers)
    subject_data_id = next(iter(subject_data_response.json()['subject_data'][0]['data']))
    delete_subject_data_response = hug.test.delete(update, "/update/data/{}/{}".format(subject_data_id, 'subject'),
                                                   headers=auth_headers)
    assert delete_subject_data_response.status == hug.HTTP_202

    object_data_response = requests.get(
        "{}/policies/{}/object_data".format(get_configuration("management").get("url"), policy_id),
        headers=auth_headers)
    object_data_id = next(iter(object_data_response.json()['object_data'][0]['data']))
    delete_object_data_response = hug.test.delete(update, "/update/data/{}/{}".format(object_data_id, 'object'),
                                                  headers=auth_headers)
    assert delete_object_data_response.status == hug.HTTP_202

    action_data_response = requests.get(
        "{}/policies/{}/action_data".format(get_configuration("management").get("url"), policy_id),
        headers=auth_headers)
    action_data_id = next(iter(action_data_response.json()['action_data'][0]['data']))
    delete_action_data_response = hug.test.delete(update, "/update/data/{}/{}".format(action_data_id, 'action'),
                                                  headers=auth_headers)
    assert delete_action_data_response.status == hug.HTTP_202


# def test_pipeline_delete_attributes():
#     from moon_engine.api.pipeline import update
#     from moon_utilities.auth_functions import get_api_key_for_user
#     from moon_engine.api.configuration import get_configuration
#
#     auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
#
#     attributes_response = requests.get(
#         "{}/attributes".format(get_configuration("management").get("url")),
#         headers=auth_headers)
#
#     attributes = attributes_response.json()
#     key = next(iter(attributes['attributes']))
#     req = hug.test.delete(update, "/update/attributes/{}".format(key), headers=auth_headers)
#     assert req.status == hug.HTTP_202


