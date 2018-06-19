import pytest
import helpers.mock_data as mock_data
import helpers.pdp_helper as pdp_helper


def test_update_pdp(db):
    pdp_id = "pdp_id1"
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "test_pdp",
        "security_pipeline": [policy_id],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    pdp_helper.add_pdp(pdp_id, value)
    pdp = pdp_helper.update_pdp(pdp_id, value)
    assert pdp


def test_update_pdp_with_invalid_id(db):
    pdp_id = "pdp_id1"
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "test_pdp",
        "security_pipeline": [policy_id],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    with pytest.raises(Exception) as exception_info:
        pdp_helper.update_pdp(pdp_id, value)
    assert str(exception_info.value) == '400: Pdp Unknown'


def test_delete_pdp(db):
    pdp_id = "pdp_id1"
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "test_pdp",
        "security_pipeline": [policy_id],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    pdp_helper.add_pdp(pdp_id, value)
    pdp_helper.delete_pdp(pdp_id)
    assert len(pdp_helper.get_pdp(pdp_id)) == 0


def test_delete_pdp_with_invalid_id(db):
    pdp_id = "pdp_id1"
    with pytest.raises(Exception) as exception_info:
        pdp_helper.delete_pdp(pdp_id)
    assert str(exception_info.value) == '400: Pdp Unknown'


def test_add_pdp(db):
    pdp_id = "pdp_id1"
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "test_pdp",
        "security_pipeline": [policy_id],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    pdp = pdp_helper.add_pdp(pdp_id, value)
    assert pdp


def test_add_pdp_twice_with_same_id(db):
    pdp_id = "pdp_id1"
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "test_pdp",
        "security_pipeline": [policy_id],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    pdp_helper.add_pdp(pdp_id, value)
    with pytest.raises(Exception) as exception_info:
        pdp_helper.add_pdp(pdp_id, value)
    assert str(exception_info.value) == '409: Pdp Error'


def test_add_pdp_twice_with_same_name(db):
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "test_pdp",
        "security_pipeline": [policy_id],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    pdp_helper.add_pdp(value=value)
    with pytest.raises(Exception) as exception_info:
        pdp_helper.add_pdp(value=value)
    assert str(exception_info.value) == '409: Pdp Error'


def test_get_pdp(db):
    pdp_id = "pdp_id1"
    subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = mock_data.create_new_policy(
        subject_category_name="subject_category1",
        object_category_name="object_category1",
        action_category_name="action_category1",
        meta_rule_name="meta_rule_1",
        model_name="model1")
    value = {
        "name": "test_pdp",
        "security_pipeline": [policy_id],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    pdp_helper.add_pdp(pdp_id, value)
    pdp = pdp_helper.get_pdp(pdp_id)
    assert len(pdp) == 1


def test_get_pdp_with_invalid_id(db):
    pdp_id = "invalid"
    pdp = pdp_helper.get_pdp(pdp_id)
    assert len(pdp) == 0
