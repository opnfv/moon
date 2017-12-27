import pytest


def create_project(tenant_dict):
    from python_moondb.core import KeystoneManager
    return KeystoneManager.create_project(tenant_dict)


def list_projects():
    from python_moondb.core import KeystoneManager
    return KeystoneManager.list_projects()


def create_user(subject_dict):
    from python_moondb.core import KeystoneManager
    return KeystoneManager.create_user(subject_dict)


def test_create_project():
    tenant_dict = {
        "description": "test_project",
        "domain_id": ['domain_id_1'],
        "enabled": True,
        "is_domain": False,
        "name": 'project_1'
    }
    project = create_project(tenant_dict)
    assert project
    assert project.get('name') == tenant_dict.get('name')


def test_create_project_without_name():
    tenant_dict = {
        "description": "test_project",
        "domain_id": ['domain_id_1'],
        "enabled": True,
        "is_domain": False,
    }
    with pytest.raises(Exception) as exception_info:
        create_project(tenant_dict)
    assert '400: Keystone project error' == str(exception_info.value)


def test_create_user():
    subject_dict = {
        "password": "password",
        "domain_id": ['domain_id_1'],
        "enabled": True,
        "project": 'test_project',
        "name": 'user_id_1'
    }
    user = create_user(subject_dict)
    assert user
