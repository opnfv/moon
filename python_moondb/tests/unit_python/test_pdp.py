import pytest


def update_pdp(pdp_id, value):
    from python_moondb.core import PDPManager
    return PDPManager.update_pdp("", pdp_id, value)


def delete_pdp(pdp_id):
    from python_moondb.core import PDPManager
    PDPManager.delete_pdp("", pdp_id)


def add_pdp(pdp_id=None, value=None):
    from python_moondb.core import PDPManager
    return PDPManager.add_pdp("", pdp_id, value)


def get_pdp(pdp_id=None):
    from python_moondb.core import PDPManager
    return PDPManager.get_pdp("", pdp_id)


def test_update_pdp(db):
    pdp_id = "pdp_id1"
    value = {
        "name": "test_pdp",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    add_pdp(pdp_id, value)
    pdp = update_pdp(pdp_id, value)
    assert pdp


def test_update_pdp_with_invalid_id(db):
    pdp_id = "pdp_id1"
    value = {
        "name": "test_pdp",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    with pytest.raises(Exception) as exception_info:
        update_pdp(pdp_id, value)
    assert str(exception_info.value) == '400: Pdp Unknown'


def test_delete_pdp(db):
    pdp_id = "pdp_id1"
    value = {
        "name": "test_pdp",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    add_pdp(pdp_id, value)
    delete_pdp(pdp_id)
    assert len(get_pdp(pdp_id)) == 0


def test_delete_pdp_with_invalid_id(db):
    pdp_id = "pdp_id1"
    with pytest.raises(Exception) as exception_info:
        delete_pdp(pdp_id)
    assert str(exception_info.value) == '400: Pdp Unknown'


def test_add_pdp(db):
    pdp_id = "pdp_id1"
    value = {
        "name": "test_pdp",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    pdp = add_pdp(pdp_id, value)
    assert pdp


def test_add_pdp_twice_with_same_id(db):
    pdp_id = "pdp_id1"
    value = {
        "name": "test_pdp",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    add_pdp(pdp_id, value)
    with pytest.raises(Exception) as exception_info:
        add_pdp(pdp_id, value)
    assert str(exception_info.value) == '409: Pdp Error'


def test_add_pdp_twice_with_same_name(db):
    value = {
        "name": "test_pdp",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    add_pdp(value=value)
    with pytest.raises(Exception) as exception_info:
        add_pdp(value=value)
    assert str(exception_info.value) == '409: Pdp Error'


def test_get_pdp(db):
    pdp_id = "pdp_id1"
    value = {
        "name": "test_pdp",
        "security_pipeline": ["policy_id_1", "policy_id_2"],
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    add_pdp(pdp_id, value)
    pdp = get_pdp(pdp_id)
    assert len(pdp) == 1


def test_get_pdp_with_invalid_id(db):
    pdp_id = "invalid"
    pdp = get_pdp(pdp_id)
    assert len(pdp) == 0
