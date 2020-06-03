# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


def get_headers():
    from moon_utilities.auth_functions import get_api_key_for_user

    auth_headers = {"X-Api-Key": get_api_key_for_user("admin"),
                    'Content-Type': 'application/json'}
    return auth_headers
