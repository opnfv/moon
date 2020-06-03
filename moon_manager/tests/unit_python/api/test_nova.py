# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



def create_project(tenant_dict):
    from moon_manager.pip_driver import InformationManager
    return InformationManager["objects"][0].create_project(**tenant_dict)


def list_projects():
    from moon_manager.pip_driver import InformationManager
    return InformationManager["objects"][0].get_projects()


def list_objects():
    from moon_manager.pip_driver import InformationManager
    print(f"IM : {InformationManager['objects'][0].driver.__dict__}")
    return InformationManager["objects"][0].get_items()


def test_create_project():
    tenant_dict = {
        "description": "test_project",
        "domain": ['domain_id_1'],
        "enabled": True,
        "is_domain": False,
        "name": 'project_1'
    }
    project = create_project(tenant_dict)
    assert project
    assert project.get('name') == tenant_dict.get('name')


def test_list_objects():
    objects = list_objects()
    assert objects
    assert objects["servers"][0].get('name') == "vm1"

#  TODO TO BE UPDATED
# def test_create_project_without_name():
#     tenant_dict = {
#         "description": "test_project",
#         "domain_id": ['domain_id_1'],
#         "enabled": True,
#         "is_domain": False,
#     }
#     with pytest.raises(Exception) as exception_info:
#         create_project(tenant_dict)
#     assert '400: Keystone project error' == str(exception_info.value)
