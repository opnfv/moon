import policies.mock_data as mock_data
from python_moonutilities.exceptions import *
import pytest

def get_action_assignments(policy_id, action_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_action_assignments("", policy_id, action_id, category_id)


def add_action_assignment(policy_id, action_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_action_assignment("", policy_id, action_id, category_id, data_id)


def delete_action_assignment(policy_id, action_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_action_assignment("", policy_id, action_id, category_id, data_id)


def get_object_assignments(policy_id, object_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_object_assignments("", policy_id, object_id, category_id)


def add_object_assignment(policy_id, object_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_object_assignment("", policy_id, object_id, category_id, data_id)


def delete_object_assignment(policy_id, object_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_object_assignment("", policy_id, object_id, category_id, data_id)


def get_subject_assignments(policy_id, subject_id=None, category_id=None):
    from python_moondb.core import PolicyManager
    return PolicyManager.get_subject_assignments("", policy_id, subject_id, category_id)


def add_subject_assignment(policy_id, subject_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    return PolicyManager.add_subject_assignment("", policy_id, subject_id, category_id, data_id)


def delete_subject_assignment(policy_id, subject_id, category_id, data_id):
    from python_moondb.core import PolicyManager
    PolicyManager.delete_subject_assignment("", policy_id, subject_id, category_id, data_id)


def test_get_action_assignments(db):
    policy_id = mock_data.get_policy_id()
    action_id = "action_id_1"
    category_id = "category_id_1"
    data_id = "data_id_1"
    add_action_assignment(policy_id, action_id, category_id, data_id)
    act_assignments = get_action_assignments(policy_id, action_id, category_id)
    action_id_1 = list(act_assignments.keys())[0]
    assert act_assignments[action_id_1]["policy_id"] == policy_id
    assert act_assignments[action_id_1]["action_id"] == action_id
    assert act_assignments[action_id_1]["category_id"] == category_id
    assert len(act_assignments[action_id_1].get("assignments")) == 1
    assert data_id in act_assignments[action_id_1].get("assignments")


def test_get_action_assignments_by_policy_id(db):
    policy_id = mock_data.get_policy_id()
    action_id = "action_id_1"
    category_id = "category_id_1"
    data_id = "data_id_1"
    add_action_assignment(policy_id, action_id, category_id, data_id)
    data_id = "data_id_2"
    add_action_assignment(policy_id, action_id, category_id, data_id)
    data_id = "data_id_3"
    add_action_assignment(policy_id, action_id, category_id, data_id)
    act_assignments = get_action_assignments(policy_id)
    action_id_1 = list(act_assignments.keys())[0]
    assert act_assignments[action_id_1]["policy_id"] == policy_id
    assert act_assignments[action_id_1]["action_id"] == action_id
    assert act_assignments[action_id_1]["category_id"] == category_id
    assert len(act_assignments[action_id_1].get("assignments")) == 3


def test_add_action_assignments(db):
    policy_id = mock_data.get_policy_id()
    action_id = "action_id_1"
    category_id = "category_id_1"
    data_id = "data_id_1"
    action_assignments = add_action_assignment(policy_id, action_id, category_id, data_id)
    assert action_assignments
    action_id_1 = list(action_assignments.keys())[0]
    assert action_assignments[action_id_1]["policy_id"] == policy_id
    assert action_assignments[action_id_1]["action_id"] == action_id
    assert action_assignments[action_id_1]["category_id"] == category_id
    assert len(action_assignments[action_id_1].get("assignments")) == 1
    assert data_id in action_assignments[action_id_1].get("assignments")

    with pytest.raises(ActionAssignmentExisting) as exception_info:
        add_action_assignment(policy_id, action_id, category_id, data_id)

def test_delete_action_assignment(db):
    policy_id = mock_data.get_policy_id()
    add_action_assignment(policy_id, "", "", "")
    policy_id = mock_data.get_policy_id(model_name="test_model2", policy_name="policy_2", meta_rule_name="meta_rule2", category_prefix="_")
    action_id = "action_id_2"
    category_id = "category_id_2"
    data_id = "data_id_2"
    add_action_assignment(policy_id, action_id, category_id, data_id)
    delete_action_assignment(policy_id, "", "", "")
    assignments = get_action_assignments(policy_id, )
    assert len(assignments) == 1


def test_delete_action_assignment_with_invalid_policy_id(db):
    policy_id = "invalid_id"
    delete_action_assignment(policy_id, "", "", "")
    assignments = get_action_assignments(policy_id, )
    assert len(assignments) == 0


def test_get_object_assignments(db):
    policy_id = mock_data.get_policy_id()
    object_id = "object_id_1"
    category_id = "category_id_1"
    data_id = "data_id_1"
    add_object_assignment(policy_id, object_id, category_id, data_id)
    obj_assignments = get_object_assignments(policy_id, object_id, category_id)
    object_id_1 = list(obj_assignments.keys())[0]
    assert obj_assignments[object_id_1]["policy_id"] == policy_id
    assert obj_assignments[object_id_1]["object_id"] == object_id
    assert obj_assignments[object_id_1]["category_id"] == category_id
    assert len(obj_assignments[object_id_1].get("assignments")) == 1
    assert data_id in obj_assignments[object_id_1].get("assignments")


def test_get_object_assignments_by_policy_id(db):
    policy_id = mock_data.get_policy_id()
    object_id_1 = "object_id_1"
    category_id_1 = "category_id_1"
    data_id = "data_id_1"
    add_action_assignment(policy_id, object_id_1, category_id_1, data_id)
    object_id_2 = "object_id_2"
    category_id_2 = "category_id_2"
    data_id = "data_id_2"
    add_action_assignment(policy_id, object_id_2, category_id_2, data_id)
    object_id_3 = "object_id_3"
    category_id_3 = "category_id_3"
    data_id = "data_id_3"
    add_action_assignment(policy_id, object_id_3, category_id_3, data_id)
    act_assignments = get_action_assignments(policy_id)
    assert len(act_assignments) == 3


def test_add_object_assignments(db):
    policy_id = mock_data.get_policy_id()
    object_id = "object_id_1"
    category_id = "category_id_1"
    data_id = "data_id_1"
    object_assignments = add_object_assignment(policy_id, object_id, category_id, data_id)
    assert object_assignments
    object_id_1 = list(object_assignments.keys())[0]
    assert object_assignments[object_id_1]["policy_id"] == policy_id
    assert object_assignments[object_id_1]["object_id"] == object_id
    assert object_assignments[object_id_1]["category_id"] == category_id
    assert len(object_assignments[object_id_1].get("assignments")) == 1
    assert data_id in object_assignments[object_id_1].get("assignments")

    with pytest.raises(ObjectAssignmentExisting):
        add_object_assignment(policy_id, object_id, category_id, data_id)


def test_delete_object_assignment(db):
    policy_id = mock_data.get_policy_id()
    add_object_assignment(policy_id, "", "", "")
    object_id = "action_id_2"
    category_id = "category_id_2"
    data_id = "data_id_2"
    add_object_assignment(policy_id, object_id, category_id, data_id)
    delete_object_assignment(policy_id, "", "", "")
    assignments = get_object_assignments(policy_id, )
    assert len(assignments) == 1


def test_delete_object_assignment_with_invalid_policy_id(db):
    policy_id = "invalid_id"
    delete_object_assignment(policy_id, "", "", "")
    assignments = get_object_assignments(policy_id, )
    assert len(assignments) == 0


def test_get_subject_assignments(db):
    policy_id = mock_data.get_policy_id()
    subject_id = "object_id_1"
    category_id = "category_id_1"
    data_id = "data_id_1"
    add_subject_assignment(policy_id, subject_id, category_id, data_id)
    subj_assignments = get_subject_assignments(policy_id, subject_id, category_id)
    subject_id_1 = list(subj_assignments.keys())[0]
    assert subj_assignments[subject_id_1]["policy_id"] == policy_id
    assert subj_assignments[subject_id_1]["subject_id"] == subject_id
    assert subj_assignments[subject_id_1]["category_id"] == category_id
    assert len(subj_assignments[subject_id_1].get("assignments")) == 1
    assert data_id in subj_assignments[subject_id_1].get("assignments")


def test_get_subject_assignments_by_policy_id(db):
    policy_id = mock_data.get_policy_id()
    subject_id_1 = "subject_id_1"
    category_id_1 = "category_id_1"
    data_id = "data_id_1"
    add_subject_assignment(policy_id, subject_id_1, category_id_1, data_id)
    subject_id_2 = "subject_id_2"
    category_id_2 = "category_id_2"
    data_id = "data_id_2"
    add_subject_assignment(policy_id, subject_id_2, category_id_2, data_id)
    subject_id_3 = "subject_id_3"
    category_id_3 = "category_id_3"
    data_id = "data_id_3"
    add_subject_assignment(policy_id, subject_id_3, category_id_3, data_id)
    subj_assignments = get_subject_assignments(policy_id)
    assert len(subj_assignments) == 3


def test_add_subject_assignments(db):
    policy_id = mock_data.get_policy_id()
    subject_id = "subject_id_1"
    category_id = "category_id_1"
    data_id = "data_id_1"
    subject_assignments = add_subject_assignment(policy_id, subject_id, category_id, data_id)
    assert subject_assignments
    subject_id_1 = list(subject_assignments.keys())[0]
    assert subject_assignments[subject_id_1]["policy_id"] == policy_id
    assert subject_assignments[subject_id_1]["subject_id"] == subject_id
    assert subject_assignments[subject_id_1]["category_id"] == category_id
    assert len(subject_assignments[subject_id_1].get("assignments")) == 1
    assert data_id in subject_assignments[subject_id_1].get("assignments")

    with pytest.raises(SubjectAssignmentExisting):
        add_subject_assignment(policy_id, subject_id, category_id, data_id)


def test_delete_subject_assignment(db):
    policy_id = mock_data.get_policy_id()
    add_subject_assignment(policy_id, "", "", "")
    subject_id = "subject_id_2"
    category_id = "category_id_2"
    data_id = "data_id_2"
    add_subject_assignment(policy_id, subject_id, category_id, data_id)
    delete_subject_assignment(policy_id, "", "", "")
    assignments = get_subject_assignments(policy_id, )
    assert len(assignments) == 1


def test_delete_subject_assignment_with_invalid_policy_id(db):
    policy_id = "invalid_id"
    delete_subject_assignment(policy_id, "", "", "")
    assignments = get_subject_assignments(policy_id, )
    assert len(assignments) == 0
