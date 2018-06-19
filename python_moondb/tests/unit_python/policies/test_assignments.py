# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import helpers.mock_data as mock_data
import helpers.assignment_helper as assignment_helper
from python_moonutilities.exceptions import *
import pytest


def test_get_action_assignments(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    action_id = mock_data.create_action(policy_id)
    data_id = mock_data.create_action_data(policy_id=policy_id, category_id=action_category_id)

    assignment_helper.add_action_assignment(policy_id, action_id, action_category_id, data_id)
    act_assignments = assignment_helper.get_action_assignments(policy_id, action_id, action_category_id)
    action_id_1 = list(act_assignments.keys())[0]
    assert act_assignments[action_id_1]["policy_id"] == policy_id
    assert act_assignments[action_id_1]["action_id"] == action_id
    assert act_assignments[action_id_1]["category_id"] == action_category_id
    assert len(act_assignments[action_id_1].get("assignments")) == 1
    assert data_id in act_assignments[action_id_1].get("assignments")


def test_add_action_assignments(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    action_id = mock_data.create_action(policy_id)
    data_id = mock_data.create_action_data(policy_id=policy_id, category_id=action_category_id)
    action_assignments = assignment_helper.add_action_assignment(policy_id, action_id, action_category_id, data_id)
    assert action_assignments
    action_id_1 = list(action_assignments.keys())[0]
    assert action_assignments[action_id_1]["policy_id"] == policy_id
    assert action_assignments[action_id_1]["action_id"] == action_id
    assert action_assignments[action_id_1]["category_id"] == action_category_id
    assert len(action_assignments[action_id_1].get("assignments")) == 1
    assert data_id in action_assignments[action_id_1].get("assignments")

    with pytest.raises(ActionAssignmentExisting) as exception_info:
        assignment_helper.add_action_assignment(policy_id, action_id, action_category_id, data_id)


def test_delete_action_assignment(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    action_id = mock_data.create_action(policy_id)
    data_id = mock_data.create_action_data(policy_id=policy_id, category_id=action_category_id)
    assignment_helper.add_action_assignment(policy_id, action_id, action_category_id, data_id)
    assignment_helper.delete_action_assignment(policy_id, "", "", "")
    assignments = assignment_helper.get_action_assignments(policy_id, )
    assert len(assignments) == 1


def test_delete_action_assignment_with_invalid_policy_id(db):
    policy_id = "invalid_id"
    assignment_helper.delete_action_assignment(policy_id, "", "", "")
    assignments = assignment_helper.get_action_assignments(policy_id, )
    assert len(assignments) == 0


def test_get_object_assignments(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    object_id = mock_data.create_object(policy_id)
    data_id = mock_data.create_object_data(policy_id=policy_id, category_id=object_category_id)
    assignment_helper.add_object_assignment(policy_id, object_id, object_category_id, data_id)
    obj_assignments = assignment_helper.get_object_assignments(policy_id, object_id, object_category_id)
    object_id_1 = list(obj_assignments.keys())[0]
    assert obj_assignments[object_id_1]["policy_id"] == policy_id
    assert obj_assignments[object_id_1]["object_id"] == object_id
    assert obj_assignments[object_id_1]["category_id"] == object_category_id
    assert len(obj_assignments[object_id_1].get("assignments")) == 1
    assert data_id in obj_assignments[object_id_1].get("assignments")


def test_get_object_assignments_by_policy_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    object_id = mock_data.create_object(policy_id)
    data_id = mock_data.create_object_data(policy_id=policy_id, category_id=object_category_id)
    assignment_helper.add_object_assignment(policy_id, object_id, object_category_id, data_id)
    obj_assignments = assignment_helper.get_object_assignments(policy_id)
    assert len(obj_assignments) == 1


def test_add_object_assignments(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    object_id = mock_data.create_object(policy_id)
    data_id = mock_data.create_object_data(policy_id=policy_id, category_id=object_category_id)
    object_assignments = assignment_helper.add_object_assignment(policy_id, object_id, object_category_id, data_id)
    assert object_assignments
    object_id_1 = list(object_assignments.keys())[0]
    assert object_assignments[object_id_1]["policy_id"] == policy_id
    assert object_assignments[object_id_1]["object_id"] == object_id
    assert object_assignments[object_id_1]["category_id"] == object_category_id
    assert len(object_assignments[object_id_1].get("assignments")) == 1
    assert data_id in object_assignments[object_id_1].get("assignments")

    with pytest.raises(ObjectAssignmentExisting):
        assignment_helper.add_object_assignment(policy_id, object_id, object_category_id, data_id)


def test_delete_object_assignment(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    object_id = mock_data.create_object(policy_id)
    data_id = mock_data.create_object_data(policy_id=policy_id, category_id=object_category_id)
    assignment_helper.add_object_assignment(policy_id, object_id, object_category_id, data_id)

    assignment_helper.delete_object_assignment(policy_id, object_id, object_category_id, data_id=data_id)
    assignments = assignment_helper.get_object_assignments(policy_id)
    assert len(assignments) == 0


def test_delete_object_assignment_with_invalid_policy_id(db):
    policy_id = "invalid_id"
    assignment_helper.delete_object_assignment(policy_id, "", "", "")
    assignments = assignment_helper.get_object_assignments(policy_id, )
    assert len(assignments) == 0


def test_get_subject_assignments(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    subject_id = mock_data.create_subject(policy_id)
    data_id = mock_data.create_subject_data(policy_id=policy_id, category_id=subject_category_id)

    assignment_helper.add_subject_assignment(policy_id, subject_id, subject_category_id, data_id)
    subj_assignments = assignment_helper.get_subject_assignments(policy_id, subject_id, subject_category_id)
    subject_id_1 = list(subj_assignments.keys())[0]
    assert subj_assignments[subject_id_1]["policy_id"] == policy_id
    assert subj_assignments[subject_id_1]["subject_id"] == subject_id
    assert subj_assignments[subject_id_1]["category_id"] == subject_category_id
    assert len(subj_assignments[subject_id_1].get("assignments")) == 1
    assert data_id in subj_assignments[subject_id_1].get("assignments")


def test_get_subject_assignments_by_policy_id(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    subject_id = mock_data.create_subject(policy_id)
    data_id = mock_data.create_subject_data(policy_id=policy_id, category_id=subject_category_id)

    assignment_helper.add_subject_assignment(policy_id, subject_id, subject_category_id, data_id)
    subj_assignments = assignment_helper.get_subject_assignments(policy_id)
    assert len(subj_assignments) == 1


def test_add_subject_assignments(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    subject_id = mock_data.create_subject(policy_id)
    data_id = mock_data.create_subject_data(policy_id=policy_id, category_id=subject_category_id)

    subject_assignments = assignment_helper.add_subject_assignment(policy_id, subject_id, subject_category_id, data_id)
    assert subject_assignments
    subject_id_1 = list(subject_assignments.keys())[0]
    assert subject_assignments[subject_id_1]["policy_id"] == policy_id
    assert subject_assignments[subject_id_1]["subject_id"] == subject_id
    assert subject_assignments[subject_id_1]["category_id"] == subject_category_id
    assert len(subject_assignments[subject_id_1].get("assignments")) == 1
    assert data_id in subject_assignments[subject_id_1].get("assignments")

    with pytest.raises(SubjectAssignmentExisting):
        assignment_helper.add_subject_assignment(policy_id, subject_id, subject_category_id, data_id)


def test_delete_subject_assignment(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1")
    subject_id = mock_data.create_subject(policy_id)
    data_id = mock_data.create_subject_data(policy_id=policy_id, category_id=subject_category_id)
    assignment_helper.add_subject_assignment(policy_id, subject_id, subject_category_id, data_id)
    assignment_helper.delete_subject_assignment(policy_id, subject_id, subject_category_id, data_id)
    assignments = assignment_helper.get_subject_assignments(policy_id)
    assert len(assignments) == 0


def test_delete_subject_assignment_with_invalid_policy_id(db):
    policy_id = "invalid_id"
    assignment_helper.delete_subject_assignment(policy_id, "", "", "")
    assignments = assignment_helper.get_subject_assignments(policy_id, )
    assert len(assignments) == 0
