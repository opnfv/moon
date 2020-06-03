# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""Test hug API (local, command-line, and HTTP access)"""
import hug


@hug.local()
@hug.get("/logs/")
def list_logs():
    """List logs

    :return: JSON status output
    """

    return {"logs": []}
