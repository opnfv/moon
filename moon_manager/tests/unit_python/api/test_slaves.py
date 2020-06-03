# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from falcon import HTTP_200, HTTP_400, HTTP_405
import hug
from uuid import uuid4
from helpers import data_builder as builder


def test_get_slaves():
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import slave
    req = hug.test.get(slave, 'slaves/', headers=auth_headers)
    assert req.status == HTTP_200
    assert isinstance(req.data, dict)
    assert "slaves" in req.data
    for slave in req.data.get("slaves"):
        assert "name" in slave
        assert "description" in slave
        assert "status" in slave
        assert "server_ip" in slave
        assert "port" in slave


def test_add_slave(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import slave
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:10000")
    mocker.patch("subprocess.Popen", return_value=True)
    data = {
        "name": "test_slave_" + uuid4().hex,
        "description": "description of test_slave"
    }
    req = hug.test.post(slave, "slave/", data, headers=auth_headers)
    assert req.status == HTTP_200
    assert isinstance(req.data, dict)
    found = False
    assert "slaves" in req.data
    for value in req.data["slaves"].values():
        assert "name" in value
        assert "description" in value
        assert "api_key" in value
        assert "process" in value
        assert "log" in value
        assert "extra" in value
        if value['name'] == data['name']:
            found = True
            assert value["description"] == "description of test_slave"
            assert "port" in value.get("extra")
            assert "status" in value.get("extra")
            assert "server_ip" in value.get("extra")
            break
    assert found


def test_delete_slave(mocker):
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    from moon_manager.api import slave
    mocker.patch('moon_manager.plugins.pyorchestrator.get_server_url',
                 return_value="http://127.0.0.1:10000")
    mocker.patch("subprocess.Popen", return_value=True)
    data = {
        "name": "test_slave_" + uuid4().hex,
        "description": "description of test_slave"
    }
    req = hug.test.post(slave, "slave/", data, headers=auth_headers)
    assert req.status == HTTP_200
    assert isinstance(req.data, dict)
    req = hug.test.get(slave, 'slaves/', headers=auth_headers)
    success_req = None
    for key, value in req.data['slaves'].items():
        if value['name'] == data['name']:
            success_req = hug.test.delete(slave, 'slave/{}'.format(key), headers=auth_headers)
            break
    assert success_req
    assert success_req.status == HTTP_200

