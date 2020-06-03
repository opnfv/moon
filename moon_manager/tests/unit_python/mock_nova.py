# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

import requests_mock


def register_nova(m):
    m.register_uri(
        'POST', 'http://keystone:5000/v3/auth/tokens',
        headers={'X-Subject-Token': "b34e5a29-5494-4cc5-9356-daa244b8c254"}
    )
    m.register_uri(
        'DELETE', 'http://keystone:5000/v3/auth/tokens',
        headers={'X-Subject-Token': "b34e5a29-5494-4cc5-9356-daa244b8c254"}
    )
    m.register_uri(
        'GET', 'http://keystone:5000/compute/v2.1/servers',
        json={"servers": [{"name": "vm1"}]}
    )

