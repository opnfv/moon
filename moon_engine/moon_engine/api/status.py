# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""Status API"""
import hug
from moon_engine.api import configuration

@hug.local()
@hug.get("/status/")
def list_status():
    """
    List statuses
    :return: JSON status output
    """

    return {"status": {
        "uuid": configuration.get_configuration("uuid"),
        "type": configuration.get_configuration("type"),
        "log" : configuration.get_configuration("logging").get(
            "handlers", {}).get("file", {}).get("filename", "")
    }}
