# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""Import JSON API"""
import hug


@hug.local()
@hug.post("/import/")
def import_json(body):
    """Import data into the cache of the pipeline

    :return: OK if imported
    """
    if "attributes" in body:
        description = "Will update " + ", ".join(body.get("attributes"))
    else:
        description = "Will update all attributes"
    # FIXME: dev the real import functionality
    return {"status": "OK", "description": description}
