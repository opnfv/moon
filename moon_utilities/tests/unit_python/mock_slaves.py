# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



def register_slaves(m):
    m.register_uri(
        'DELETE', 'http://127.0.0.1:10000/update/assignment/098764321/subject/098764321/098764321/098764321',
        json={}
    )
    m.register_uri(
        'DELETE', 'http://127.0.0.1:10000/update/data/098764321/subject',
        json={}
    )
    m.register_uri(
        'PUT', 'http://127.0.0.1:10000/update/perimeter/098764321/098764321/subject',
        json={}
    )
    m.register_uri(
        'PUT', 'http://127.0.0.1:10000/update/pdp/098764321',
        json={}
    )
    m.register_uri(
        'PUT', 'http://127.0.0.1:10000/update/policy/098764321',
        json={}
    )
    m.register_uri(
        'PUT', 'http://127.0.0.1:10000/update/rules/1234567890',
        json={}
    )
    m.register_uri(
        'PUT', 'http://127.0.0.1:10000/update/model/1234567890',
        json={}
    )
    m.register_uri(
        'PUT', 'http://127.0.0.1:10000/update/meta_data/1234567890',
        json={}
    )
    m.register_uri(
        'PUT', 'http://127.0.0.1:10000/update/meta_rule/1234567890',
        json={}
    )
