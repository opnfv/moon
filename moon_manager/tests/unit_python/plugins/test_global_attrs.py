# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
from moon_manager.pip_driver import AttrsManager
from moon_manager.api.configuration import get_configuration


def test_mode_add_get():
    default_value = get_configuration(
        "information")["global_attrs"]["attributes"]["mode"]["default"]
    value = AttrsManager.delete_object(object_type="mode")
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    value = AttrsManager.get_object(object_type="mode")
    assert value["value"] == default_value
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == default_value


def test_mode_add_gets():
    default_value = \
        get_configuration("information")["global_attrs"]["attributes"]["mode"]["default"]
    value = AttrsManager.delete_object(object_type="mode")
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    values = AttrsManager.get_objects()
    assert "mode" in values
    assert values["mode"]["value"] == default_value
    assert isinstance(values["mode"], dict)
    for key in ("id", "value", "default", "values"):
        assert key in values["mode"]
    assert values["mode"]["value"] == default_value


def test_mode_update():
    value = AttrsManager.update_object(object_id="build", object_type="mode")
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == "build"
    value = AttrsManager.get_object(object_type="mode")
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == "build"


def test_mode_delete():
    value = AttrsManager.update_object(object_id="build", object_type="mode")
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == "build"
    value = AttrsManager.delete_object(object_type="mode")
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == "run"


def test_hug_mode_add_get():
    from moon_manager.api import attributes
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    default_value = get_configuration(
        "information")["global_attrs"]["attributes"]["mode"]["default"]

    req = hug.test.delete(attributes, "/attributes/{}".format("mode"), headers=auth_headers)
    assert req.status == hug.HTTP_200
    value = req.data
    assert isinstance(value, dict)
    assert "attributes" in value
    value = value["attributes"]
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == default_value
    value = AttrsManager.get_object(object_type="mode")
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == default_value


def test_hug_mode_update():
    from moon_manager.api import attributes
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}

    req = hug.test.put(attributes, "/attributes/{}/{}".format("mode", "build"), headers=auth_headers)
    assert req.status == hug.HTTP_200
    value = req.data
    assert isinstance(value, dict)
    assert "attributes" in value
    value = value["attributes"]
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == "build"
    value = AttrsManager.get_object(object_type="mode")
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == "build"


def test_hug_mode_delete():
    from moon_manager.api import attributes
    from moon_utilities.auth_functions import get_api_key_for_user
    auth_headers = {"X-Api-Key": get_api_key_for_user("admin")}
    default_value = get_configuration(
        "information")["global_attrs"]["attributes"]["mode"]["default"]

    req = hug.test.put(attributes, "/attributes/{}/{}".format("mode", "build"), headers=auth_headers)
    assert req.status == hug.HTTP_200
    value = req.data
    assert isinstance(value, dict)
    assert "attributes" in value
    value = value["attributes"]
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == "build"
    req = hug.test.delete(attributes, "/attributes/{}".format("mode"), headers=auth_headers)
    assert req.status == hug.HTTP_200
    value = req.data
    assert isinstance(value, dict)
    assert "attributes" in value
    value = value["attributes"]
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == default_value
    value = AttrsManager.get_object(object_type="mode")
    assert isinstance(value, dict)
    for key in ("id", "value", "default", "values"):
        assert key in value
    assert value["value"] == default_value
