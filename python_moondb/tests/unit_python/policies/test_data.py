# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import helpers.mock_data as mock_data
import helpers.data_helper as data_helper
import pytest
import logging
from python_moonutilities.exceptions import *

logger = logging.getLogger("python_moondb.tests.api.test_data")


def test_get_action_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    action_data = data_helper.add_action_data(policy_id=policy_id, category_id=action_category_id, value=value)
    data_id = list(action_data["data"])[0]
    found_action_data = data_helper.get_action_data(policy_id=policy_id, data_id=data_id,
                                                    category_id=action_category_id)
    assert found_action_data
    assert len(found_action_data[0]["data"]) == 1


def test_get_action_data_with_invalid_category_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    action_data = data_helper.get_action_data(policy_id=policy_id, category_id="invalid")
    assert len(action_data) == 0


def test_add_action_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    action_data = data_helper.add_action_data(policy_id=policy_id, category_id=action_category_id, value=value)
    assert action_data
    assert len(action_data['data']) == 1


def test_add_action_data_with_invalid_category_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    with pytest.raises(Exception) as exception_info:
        data_helper.add_action_data(policy_id=policy_id, value=value).get('data')
    assert str(exception_info.value) == 'Invalid category id'


def test_delete_action_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    data_helper.get_available_metadata(policy_id)
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    action_data = data_helper.add_action_data(policy_id=policy_id, category_id=action_category_id, value=value)
    data_id = list(action_data["data"])[0]
    data_helper.delete_action_data(policy_id, data_id)
    new_action_data = data_helper.get_action_data(policy_id)
    assert len(new_action_data[0]['data']) == 0


def test_get_object_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    object_data = data_helper.add_object_data(policy_id=policy_id, category_id=object_category_id, value=value)
    data_id = list(object_data["data"])[0]
    found_object_data = data_helper.get_object_data(policy_id=policy_id, data_id=data_id,
                                                    category_id=object_category_id)
    assert found_object_data
    assert len(found_object_data[0]['data']) == 1


def test_get_object_data_with_invalid_category_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    object_data = data_helper.get_object_data(policy_id=policy_id, category_id="invalid")
    assert len(object_data) == 0


def test_add_object_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    object_data = data_helper.add_object_data(policy_id=policy_id, category_id=object_category_id, value=value).get(
        'data')
    assert object_data
    object_data_id = list(object_data.keys())[0]
    assert object_data[object_data_id].get('policy_id') == policy_id


def test_add_object_data_with_invalid_category_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    with pytest.raises(MetaDataUnknown) as exception_info:
        data_helper.add_object_data(policy_id=policy_id, category_id="invalid", value=value).get('data')
    assert str(exception_info.value) == '400: Meta data Unknown'


def test_delete_object_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    object_data = data_helper.add_object_data(policy_id=policy_id, category_id=object_category_id, value=value).get(
        'data')
    object_data_id = list(object_data.keys())[0]
    data_helper.delete_object_data(policy_id=object_data[object_data_id].get('policy_id'), data_id=object_data_id)
    new_object_data = data_helper.get_object_data(policy_id)
    assert len(new_object_data[0]['data']) == 0


def test_get_subject_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    subject_data = data_helper.add_subject_data(policy_id=policy_id, category_id=subject_category_id, value=value).get(
        'data')
    subject_data_id = list(subject_data.keys())[0]
    subject_data = data_helper.get_subject_data(policy_id, subject_data_id, subject_category_id)
    assert subject_data
    assert len(subject_data[0]['data']) == 1


def test_get_subject_data_with_invalid_category_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    subject_data = data_helper.add_subject_data(policy_id=policy_id, category_id=subject_category_id, value=value).get(
        'data')
    subject_data_id = list(subject_data.keys())[0]
    found_subject_data = data_helper.get_subject_data(policy_id, subject_data_id, "invalid")
    assert len(found_subject_data) == 0


def test_add_subject_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    subject_data = data_helper.add_subject_data(policy_id=policy_id, category_id=subject_category_id, value=value).get(
        'data')
    assert subject_data
    subject_data_id = list(subject_data.keys())[0]
    assert subject_data[subject_data_id].get('policy_id') == policy_id


def test_add_subject_data_with_no_category_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    with pytest.raises(Exception) as exception_info:
        data_helper.add_subject_data(policy_id=policy_id, data_id=subject_category_id, value=value).get('data')
    assert str(exception_info.value) == 'Invalid category id'


def test_delete_subject_data(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    subject_data = data_helper.add_subject_data(policy_id=policy_id, category_id=subject_category_id, value=value).get(
        'data')
    subject_data_id = list(subject_data.keys())[0]
    data_helper.delete_subject_data(subject_data[subject_data_id].get('policy_id'), subject_data_id)
    new_subject_data = data_helper.get_subject_data(policy_id)
    assert len(new_subject_data[0]['data']) == 0


def test_get_actions(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "test_action",
        "description": "test",
    }
    data_helper.add_action(policy_id=policy_id, value=value)
    actions = data_helper.get_actions(policy_id, )
    assert actions
    assert len(actions) == 1
    action_id = list(actions.keys())[0]
    assert actions[action_id].get('policy_list')[0] == policy_id


def test_add_action(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "test_action",
        "description": "test",
    }
    action = data_helper.add_action(policy_id=policy_id, value=value)
    assert action
    action_id = list(action.keys())[0]
    assert len(action[action_id].get('policy_list')) == 1


def test_add_action_twice(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "test_action",
        "description": "test",
    }
    data_helper.add_action(policy_id=policy_id, value=value)
    with pytest.raises(ActionExisting):
        data_helper.add_action(policy_id=policy_id, value=value)


def test_add_action_multiple_times(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id1 = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "test_action",
        "description": "test",
    }
    action = data_helper.add_action(policy_id=policy_id1, value=value)
    logger.info("action : {}".format(action))
    action_id = list(action.keys())[0]
    perimeter_id = action[action_id].get('id')
    assert action
    value = {
        "name": "test_action",
        "description": "test",
        "policy_list": ['policy_id_3', 'policy_id_4']
    }
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id2 = mock_data.create_new_policy(
        subject_category_name="subject_category2",
        object_category_name="object_category2",
        action_category_name="action_category2",
        meta_rule_name="meta_rule_2",
        model_name="model2")
    action = data_helper.add_action(policy_id=policy_id2, perimeter_id=perimeter_id, value=value)
    logger.info("action : {}".format(action))
    assert action
    action_id = list(action.keys())[0]
    assert len(action[action_id].get('policy_list')) == 2


def test_delete_action(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "test_action",
        "description": "test",
    }
    action = data_helper.add_action(policy_id=policy_id, value=value)
    action_id = list(action.keys())[0]
    data_helper.delete_action(policy_id, action_id)
    actions = data_helper.get_actions(policy_id, )
    assert not actions


def test_delete_action_with_invalid_perimeter_id(db):
    policy_id = "invalid"
    perimeter_id = "invalid"
    with pytest.raises(Exception) as exception_info:
        data_helper.delete_action(policy_id, perimeter_id)
    assert str(exception_info.value) == '400: Policy Unknown'


def test_get_objects(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "test_object",
        "description": "test",
    }
    data_helper.add_object(policy_id=policy_id, value=value)
    objects = data_helper.get_objects(policy_id, )
    assert objects
    assert len(objects) == 1
    object_id = list(objects.keys())[0]
    assert objects[object_id].get('policy_list')[0] == policy_id


def test_add_object(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "test_object",
        "description": "test",
    }
    added_object = data_helper.add_object(policy_id=policy_id, value=value)
    assert added_object
    object_id = list(added_object.keys())[0]
    assert len(added_object[object_id].get('policy_list')) == 1

    with pytest.raises(ObjectExisting):
        data_helper.add_object(policy_id=policy_id, value=value)


def test_add_objects_multiple_times(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "test_object",
        "description": "test",
    }
    added_object = data_helper.add_object(policy_id=policy_id, value=value)
    object_id = list(added_object.keys())[0]
    perimeter_id = added_object[object_id].get('id')
    assert added_object
    value = {
        "name": "test_object",
        "description": "test",
    }
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category2",
        object_category_name="object_category2",
        action_category_name="action_category2",
        meta_rule_name="meta_rule_2",
        model_name="model2")
    added_object = data_helper.add_object(policy_id=policy_id, perimeter_id=perimeter_id, value=value)
    assert added_object
    object_id = list(added_object.keys())[0]
    assert len(added_object[object_id].get('policy_list')) == 2


def test_delete_object(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "test_object",
        "description": "test",
    }
    added_object = data_helper.add_object(policy_id=policy_id, value=value)
    object_id = list(added_object.keys())[0]
    data_helper.delete_object(policy_id, object_id)
    objects = data_helper.get_objects(policy_id, )
    assert not objects


def test_delete_object_with_invalid_perimeter_id(db):
    policy_id = "invalid"
    perimeter_id = "invalid"
    with pytest.raises(Exception) as exception_info:
        data_helper.delete_object(policy_id, perimeter_id)
    assert str(exception_info.value) == '400: Policy Unknown'


def test_get_subjects(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "testuser",
        "description": "test",
    }
    data_helper.add_subject(policy_id=policy_id, value=value)
    subjects = data_helper.get_subjects(policy_id=policy_id)
    assert subjects
    assert len(subjects) == 1
    subject_id = list(subjects.keys())[0]
    assert subjects[subject_id].get('policy_list')[0] == policy_id


def test_get_subjects_with_invalid_policy_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "testuser",
        "description": "test",
    }
    data_helper.add_subject(policy_id=policy_id, value=value)
    with pytest.raises(PolicyUnknown):
        data_helper.get_subjects(policy_id="invalid")


def test_add_subject(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "testuser",
        "description": "test",
    }
    subject = data_helper.add_subject(policy_id=policy_id, value=value)
    assert subject
    subject_id = list(subject.keys())[0]
    assert len(subject[subject_id].get('policy_list')) == 1


def test_add_subjects_multiple_times(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "testuser",
        "description": "test",
    }
    subject = data_helper.add_subject(policy_id=policy_id, value=value)
    subject_id = list(subject.keys())[0]
    perimeter_id = subject[subject_id].get('id')
    assert subject
    value = {
        "name": "testuser",
        "description": "test",
    }
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category2",
        object_category_name="object_category2",
        action_category_name="action_category2",
        meta_rule_name="meta_rule_2",
        model_name="model2")
    subject = data_helper.add_subject(policy_id=policy_id, perimeter_id=perimeter_id, value=value)
    assert subject
    subject_id = list(subject.keys())[0]
    assert len(subject[subject_id].get('policy_list')) == 2


def test_delete_subject(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    value = {
        "name": "testuser",
        "description": "test",
    }
    subject = data_helper.add_subject(policy_id=policy_id, value=value)
    subject_id = list(subject.keys())[0]
    data_helper.delete_subject(policy_id, subject_id)
    subjects = data_helper.get_subjects(policy_id, )
    assert not subjects


def test_delete_subject_with_invalid_perimeter_id(db):
    policy_id = "invalid"
    perimeter_id = "invalid"
    with pytest.raises(Exception) as exception_info:
        data_helper.delete_subject(policy_id, perimeter_id)
    assert str(exception_info.value) == '400: Policy Unknown'


def test_get_available_metadata(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    metadata = data_helper.get_available_metadata(policy_id=policy_id)
    assert metadata
    assert metadata['object'][0] == object_category_id
    assert metadata['subject'][0] == subject_category_id
    assert metadata['action'][0] == action_category_id


def test_get_available_metadata_with_invalid_policy_id(db):
    with pytest.raises(Exception) as exception_info:
        data_helper.get_available_metadata(policy_id='invalid')
    assert '400: Policy Unknown' == str(exception_info.value)
