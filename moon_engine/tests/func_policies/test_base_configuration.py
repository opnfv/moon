# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import json
import logging
import requests
import yaml
from moon_engine.api import configuration

LOGGER = logging.getLogger("moon.engine.server")


def test_rbac():
    filename = "moon.yaml"
    configuration.set_configuration(yaml.safe_load(open(filename)))
    data = json.loads(open(configuration.get_configuration("data")).read())
    for granted in data.get("checks", {}).get("granted", {}):
        req = requests.get("http://127.0.0.1:10000/authz/{}/{}/{}".format(
            granted[0], granted[1], granted[2]
        ))
        assert req.status_code == 204
