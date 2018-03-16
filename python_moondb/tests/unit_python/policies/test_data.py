import policies.mock_data as mock_data
import pytest
import logging
from python_moonutilities.exceptions import *

logger = logging.getLogger("python_moondb.tests.api.test_data")


def get_action_data(policy_id, data_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_action_data("", policy_id, data_id, category_id)


def add_action_data(policy_id, data_id=None, category_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_action_data("", policy_id, data_id, category_id, value)


def delete_action_data(policy_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_action_data("", policy_id, data_id)


def get_object_data(policy_id, data_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_object_data("", policy_id, data_id, category_id)


def add_object_data(policy_id, data_id=None, category_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_object_data("", policy_id, data_id, category_id, value)


def delete_object_data(policy_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_object_data("", policy_id, data_id)


def get_subject_data(policy_id, data_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_subject_data("", policy_id, data_id, category_id)


def add_subject_data(policy_id, data_id=None, category_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.set_subject_data("", policy_id, data_id, category_id, value)


def delete_subject_data(policy_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_subject_data("", policy_id, data_id)


def get_actions(policy_id, perimeter_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_actions("", policy_id, perimeter_id)


def add_action(policy_id, perimeter_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_action("", policy_id, perimeter_id, value)


def delete_action(policy_id, perimeter_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_action("", policy_id, perimeter_id)


def get_objects(policy_id, perimeter_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_objects("", policy_id, perimeter_id)


def add_object(policy_id, perimeter_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_object("", policy_id, perimeter_id, value)


def delete_object(policy_id, perimeter_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_object("", policy_id, perimeter_id)


def get_subjects(policy_id, perimeter_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_subjects("", policy_id, perimeter_id)


def add_subject(policy_id, perimeter_id=None, value=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_subject("", policy_id, perimeter_id, value)


def delete_subject(policy_id, perimeter_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_subject("", policy_id, perimeter_id)


def get_available_metadata(policy_id):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_available_metadata("", policy_id)


def test_get_action_data(db):
    policy_id = mock_data.get_policy_id()
    get_available_metadata(policy_id)

    policy_id = policy_id
    data_id = "data_id_1"
    category_id = "action_category_id1"
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    add_action_data(policy_id, data_id, category_id, value)
    action_data = get_action_data(policy_id, data_id, category_id)
    assert action_data
    assert len(action_data[0]['data']) == 1


def test_get_action_data_with_invalid_category_id(db):
    policy_id = mock_data.get_policy_id()
    get_available_metadata(policy_id)
    data_id = "data_id_1"
    category_id = "action_category_id1"
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    add_action_data(policy_id, data_id, category_id, value)
    action_data = get_action_data(policy_id)
    assert action_data
    assert len(action_data[0]['data']) == 1


def test_add_action_data(db):
    policy_id = mock_data.get_policy_id()
    data_id = "data_id_1"
    category_id = "category_id_1"
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    action_data = add_action_data(policy_id, data_id, category_id, value).get('data')
    assert action_data
    action_data_id = list(action_data.keys())[0]
    assert action_data[action_data_id].get('policy_id') == policy_id

    with pytest.raises(ActionScopeExisting) as exception_info:
        add_action_data(policy_id, category_id=category_id, value=value).get('data')


def test_add_action_data_with_invalid_category_id(db):
    policy_id = mock_data.get_policy_id()
    data_id = "data_id_1"
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    with pytest.raises(Exception) as exception_info:
        add_action_data(policy_id=policy_id, data_id=data_id, value=value).get('data')
    assert str(exception_info.value) == 'Invalid category id'


def test_delete_action_data(db):
    policy_id = mock_data.get_policy_id()
    get_available_metadata(policy_id)
    data_id = "data_id_1"
    category_id = "category_id_1"
    value = {
        "name": "action-type",
        "description": {"vm-action": "", "storage-action": "", },
    }
    action_data = add_action_data(policy_id, data_id, category_id, value).get('data')
    action_data_id = list(action_data.keys())[0]
    delete_action_data(action_data[action_data_id].get('policy_id'), None)
    new_action_data = get_action_data(policy_id)
    assert len(new_action_data[0]['data']) == 0


def test_get_object_data(db):
    policy_id = mock_data.get_policy_id()
    get_available_metadata(policy_id)
    data_id = "data_id_1"
    category_id = "object_category_id1"
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    add_object_data(policy_id, data_id, category_id, value)
    object_data = get_object_data(policy_id, data_id, category_id)
    assert object_data
    assert len(object_data[0]['data']) == 1


def test_get_object_data_with_invalid_category_id(db):
    policy_id = mock_data.get_policy_id()
    get_available_metadata(policy_id)
    data_id = "data_id_1"
    category_id = "object_category_id1"
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    add_object_data(policy_id, data_id, category_id, value)
    object_data = get_object_data(policy_id)
    assert object_data
    assert len(object_data[0]['data']) == 1


def test_add_object_data(db):
    policy_id = mock_data.get_policy_id()
    data_id = "data_id_1"
    category_id = "object_category_id1"
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    object_data = add_object_data(policy_id, data_id, category_id, value).get('data')
    assert object_data
    object_data_id = list(object_data.keys())[0]
    assert object_data[object_data_id].get('policy_id') == policy_id

    with pytest.raises(ObjectScopeExisting) as exception_info:
        add_object_data(policy_id, category_id=category_id, value=value).get('data')


def test_add_object_data_with_invalid_category_id(db):
    policy_id = mock_data.get_policy_id()
    data_id = "data_id_1"
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    with pytest.raises(Exception) as exception_info:
        add_object_data(policy_id=policy_id, data_id=data_id, value=value).get('data')
    assert str(exception_info.value) == 'Invalid category id'


def test_delete_object_data(db):
    policy_id = mock_data.get_policy_id()
    get_available_metadata(policy_id)
    data_id = "data_id_1"
    category_id = "object_category_id1"
    value = {
        "name": "object-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    object_data = add_object_data(policy_id, data_id, category_id, value).get('data')
    object_data_id = list(object_data.keys())[0]
    delete_object_data(object_data[object_data_id].get('policy_id'), data_id)
    new_object_data = get_object_data(policy_id)
    assert len(new_object_data[0]['data']) == 0


def test_get_subject_data(db):
    policy_id = mock_data.get_policy_id()
    get_available_metadata(policy_id)
    data_id = "data_id_1"
    category_id = "subject_category_id1"
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    add_subject_data(policy_id, data_id, category_id, value)
    subject_data = get_subject_data(policy_id, data_id, category_id)
    assert subject_data
    assert len(subject_data[0]['data']) == 1


def test_get_subject_data_with_invalid_category_id(db):
    policy_id = mock_data.get_policy_id()
    get_available_metadata(policy_id)
    data_id = "data_id_1"
    category_id = "subject_category_id1"
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    add_subject_data(policy_id, data_id, category_id, value)
    subject_data = get_subject_data(policy_id)
    assert subject_data
    assert len(subject_data[0]['data']) == 1


def test_add_subject_data(db):
    policy_id = mock_data.get_policy_id()
    data_id = "data_id_1"
    category_id = "subject_category_id1"
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    subject_data = add_subject_data(policy_id, data_id, category_id, value).get('data')
    assert subject_data
    subject_data_id = list(subject_data.keys())[0]
    assert subject_data[subject_data_id].get('policy_id') == policy_id
    with pytest.raises(SubjectScopeExisting):
        add_subject_data(policy_id, category_id=category_id, value=value).get('data')


def test_add_subject_data_with_no_category_id(db):
    policy_id = mock_data.get_policy_id()
    data_id = "data_id_1"
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    with pytest.raises(Exception) as exception_info:
        add_subject_data(policy_id=policy_id, data_id=data_id, value=value).get('data')
    assert str(exception_info.value) == 'Invalid category id'


def test_delete_subject_data(db):
    policy_id = mock_data.get_policy_id()
    get_available_metadata(policy_id)
    data_id = "data_id_1"
    category_id = "subject_category_id1"
    value = {
        "name": "subject-security-level",
        "description": {"low": "", "medium": "", "high": ""},
    }
    subject_data = add_subject_data(policy_id, data_id, category_id, value).get('data')
    subject_data_id = list(subject_data.keys())[0]
    delete_subject_data(subject_data[subject_data_id].get('policy_id'), data_id)
    new_subject_data = get_subject_data(policy_id)
    assert len(new_subject_data[0]['data']) == 0


def test_get_actions(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "test_action",
        "description": "test",
    }
    add_action(policy_id=policy_id, value=value)
    actions = get_actions(policy_id, )
    assert actions
    assert len(actions) == 1
    action_id = list(actions.keys())[0]
    assert actions[action_id].get('policy_list')[0] == policy_id


def test_add_action(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "test_action",
        "description": "test",
    }
    action = add_action(policy_id=policy_id, value=value)
    assert action
    action_id = list(action.keys())[0]
    assert len(action[action_id].get('policy_list')) == 1

    with pytest.raises(ActionExisting):
        add_action(policy_id=policy_id, value=value)


def test_add_action_multiple_times(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "test_action",
        "description": "test",
    }
    action = add_action(policy_id=policy_id, value=value)
    logger.info("action : {}".format(action))
    action_id = list(action.keys())[0]
    perimeter_id = action[action_id].get('id')
    assert action
    value = {
        "name": "test_action",
        "description": "test",
        "policy_list": ['policy_id_3', 'policy_id_4']
    }
    action = add_action(mock_data.get_policy_id(model_name="test_model2", policy_name="policy_2", meta_rule_name="meta_rule2", category_prefix="_"), perimeter_id, value)
    logger.info("action : {}".format(action))
    assert action
    action_id = list(action.keys())[0]
    assert len(action[action_id].get('policy_list')) == 2


def test_delete_action(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "test_action",
        "description": "test",
    }
    action = add_action(policy_id=policy_id, value=value)
    action_id = list(action.keys())[0]
    delete_action(policy_id, action_id)
    actions = get_actions(policy_id, )
    assert not actions


def test_delete_action_with_invalid_perimeter_id(db):
    policy_id = "invalid"
    perimeter_id = "invalid"
    with pytest.raises(Exception) as exception_info:
        delete_action(policy_id, perimeter_id)
    assert str(exception_info.value) == '400: Action Unknown'


def test_get_objects(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "test_object",
        "description": "test",
    }
    add_object(policy_id=policy_id, value=value)
    objects = get_objects(policy_id, )
    assert objects
    assert len(objects) == 1
    object_id = list(objects.keys())[0]
    assert objects[object_id].get('policy_list')[0] == policy_id


def test_add_object(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "test_object",
        "description": "test",
    }
    added_object = add_object(policy_id=policy_id, value=value)
    assert added_object
    object_id = list(added_object.keys())[0]
    assert len(added_object[object_id].get('policy_list')) == 1

    with pytest.raises(ObjectExisting):
        add_object(policy_id=policy_id, value=value)


def test_add_objects_multiple_times(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "test_object",
        "description": "test",
    }
    added_object = add_object(policy_id=policy_id, value=value)
    object_id = list(added_object.keys())[0]
    perimeter_id = added_object[object_id].get('id')
    assert added_object
    value = {
        "name": "test_object",
        "description": "test",
        "policy_list": ['policy_id_3', 'policy_id_4']
    }
    added_object = add_object(mock_data.get_policy_id(model_name="test_model2", policy_name="policy_2", meta_rule_name="meta_rule2", category_prefix="_"), perimeter_id, value)
    assert added_object
    object_id = list(added_object.keys())[0]
    assert len(added_object[object_id].get('policy_list')) == 2


def test_delete_object(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "test_object",
        "description": "test",
    }
    added_object = add_object(policy_id=policy_id, value=value)
    object_id = list(added_object.keys())[0]
    delete_object(policy_id, object_id)
    objects = get_objects(policy_id, )
    assert not objects


def test_delete_object_with_invalid_perimeter_id(db):
    policy_id = "invalid"
    perimeter_id = "invalid"
    with pytest.raises(Exception) as exception_info:
        delete_object(policy_id, perimeter_id)
    assert str(exception_info.value) == '400: Object Unknown'


def test_get_subjects(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "testuser",
        "description": "test",
    }
    add_subject(policy_id=policy_id, value=value)
    subjects = get_subjects(policy_id, )
    assert subjects
    assert len(subjects) == 1
    subject_id = list(subjects.keys())[0]
    assert subjects[subject_id].get('policy_list')[0] == policy_id


def test_add_subject(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "testuser",
        "description": "test",
    }
    subject = add_subject(policy_id=policy_id, value=value)
    assert subject
    subject_id = list(subject.keys())[0]
    assert len(subject[subject_id].get('policy_list')) == 1

    with pytest.raises(SubjectExisting):
        add_subject(policy_id=policy_id, value=value)


def test_add_subjects_multiple_times(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "testuser",
        "description": "test",
    }
    subject = add_subject(policy_id=policy_id, value=value)
    subject_id = list(subject.keys())[0]
    perimeter_id = subject[subject_id].get('id')
    assert subject
    value = {
        "name": "testuser",
        "description": "test",
        "policy_list": ['policy_id_3', 'policy_id_4']
    }
    subject = add_subject(mock_data.get_policy_id(model_name="test_model2", policy_name="policy_2", meta_rule_name="meta_rule2", category_prefix="_"), perimeter_id, value)
    assert subject
    subject_id = list(subject.keys())[0]
    assert len(subject[subject_id].get('policy_list')) == 2


def test_delete_subject(db):
    policy_id = mock_data.get_policy_id()
    value = {
        "name": "testuser",
        "description": "test",
    }
    subject = add_subject(policy_id=policy_id, value=value)
    subject_id = list(subject.keys())[0]
    delete_subject(policy_id, subject_id)
    subjects = get_subjects(policy_id, )
    assert not subjects


def test_delete_subject_with_invalid_perimeter_id(db):
    policy_id = "invalid"
    perimeter_id = "invalid"
    with pytest.raises(Exception) as exception_info:
        delete_subject(policy_id, perimeter_id)
    assert str(exception_info.value) == '400: Subject Unknown'


def test_get_available_metadata(db):
    policy_id = mock_data.get_policy_id()
    metadata = get_available_metadata(policy_id=policy_id)
    assert metadata
    assert metadata['object'][0] == "object_category_id1"
    assert metadata['subject'][0] == "subject_category_id1"
    assert metadata['subject'][1] == "subject_category_id2"


def test_get_available_metadata_empty_model(db):
    import policies.test_policies as test_policies
    value = mock_data.create_policy("invalid")
    policy = test_policies.add_policies(value=value)
    assert policy
    policy_id = list(policy.keys())[0]
    metadata = get_available_metadata(policy_id=policy_id)
    assert metadata


def test_get_available_metadata_with_invalid_policy_id(db):
    with pytest.raises(Exception) as exception_info:
        get_available_metadata(policy_id='invalid')
    assert '400: Policy Unknown' == str(exception_info.value)
