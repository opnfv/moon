# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



def register_require_data(m):
    m.register_uri(
        'GET', 'http://127.0.0.1:20000/authz/testuser/vm1/boot',
        json={},
        status_code=204
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:10000/authz/a64beb1cc224474fb4badd43173e7101/testuser/vm1/boot',
        json={},
        status_code=204
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/pdp',
        json={
            "pdps": {
                "b3d3e18abf3340e8b635fd49e6634ccd": {
                    "description": "test",
                    "security_pipeline": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0"
                    ],
                    "name": "pdp_rbac",
                    "vim_project_id": "a64beb1cc224474fb4badd43173e7101"
                },
                "eac0ecd09ceb47b3ac810f01ef71b4e0": {
                    "description": "test",
                    "security_pipeline": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0"
                    ],
                    "name": "pdp_rbac2",
                    "vim_project_id": "z64beb1cc224474fb4badd43173e7108"
                }
            }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/pdp/b3d3e18abf3340e8b635fd49e6634ccd',
        json={
            "pdps": {
                "b3d3e18abf3340e8b635fd49e6634ccd": {
                    "description": "test",
                    "security_pipeline": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0"
                    ],
                    "name": "pdp_rbac",
                    "vim_project_id": "a64beb1cc224474fb4badd43173e7101"
                }
            }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/pdp/eac0ecd09ceb47b3ac810f01ef71b4e0',
        json={
            "pdps": {
                "eac0ecd09ceb47b3ac810f01ef71b4e0": {
                    "description": "test",
                    "security_pipeline": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0"
                    ],
                    "name": "pdp_rbac",
                    "vim_project_id": "z64beb1cc224474fb4badd43173e7108"
                }
            }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/policies',
        json={
            "policies": {
                "f8f49a779ceb47b3ac810f01ef71b4e0": {
                    "name": "RBAC policy example",
                    "model_id": "cd923d8633ff4978ab0e99938f5153d6",
                    "description": "test",
                    "genre": "authz"
                }
            }
        }
    )

    m.register_uri(
        'GET', 'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0',
        json={
            "f8f49a779ceb47b3ac810f01ef71b4e0": {
                "name": "RBAC policy example",
                "model_id": "cd923d8633ff4978ab0e99938f5153d6",
                "description": "test",
                "genre": "authz"
            }
        }
    )

    m.register_uri(
        'GET', 'http://127.0.0.1:8000/models',
        json={
            "models": {
                "cd923d8633ff4978ab0e99938f5153d6": {
                    "name": "RBAC",
                    "meta_rules": [
                        "4700cc0e38ef4cffa34025602d267c9e"
                    ],
                    "description": "test"
                }
            }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/meta_rules',
        json={
            "meta_rules": {
                "4700cc0e38ef4cffa34025602d267c9e": {
                    "subject_categories": [
                        "14e6ae0ba34d458b876c791b73aa17bd"
                    ],
                    "action_categories": [
                        "241a2a791554421a91c9f1bc564aa94d"
                    ],
                    "description": "",
                    "name": "rbac",
                    "object_categories": [
                        "6d48500f639d4c2cab2b1f33ef93a1e8"
                    ]
                }
            }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/subject_categories',
        json={
            'subject_categories':
                {
                    '14e6ae0ba34d458b876c791b73aa17bd':
                        {
                            'id': '14e6ae0ba34d458b876c791b73aa17bd',
                            'name': 'testuser14e6ae0ba34d458b876c791b73aa17bd',
                            'description': 'description of testuser14e6ae0ba34d458b876c791b73aa17bd'
                        }
                }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/action_categories',
        json={
            'action_categories':
                {
                    '241a2a791554421a91c9f1bc564aa94d':
                        {
                            'id': '241a2a791554421a91c9f1bc564aa94d',
                            'name': 'testuser241a2a791554421a91c9f1bc564aa94d',
                            'description': 'description of testuser241a2a791554421a91c9f1bc564aa94d'
                        }
                }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/object_categories',
        json={
            'object_categories':
                {
                    '6d48500f639d4c2cab2b1f33ef93a1e8':
                        {
                            'id': '6d48500f639d4c2cab2b1f33ef93a1e8',
                            'name': '6d48500f639d4c2cab2b1f33ef93a1e8',
                            'description': 'description of testuser6d48500f639d4c2cab2b1f33ef93a1e8'
                        }
                }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/subjects',
        json={
            "subjects": {
                "89ba91c18dd54abfbfde7a66936c51a6": {
                    "description": "test",
                    "policy_list": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0",
                        "636cd473324f4c0bbd9102cb5b62a16d"
                    ],
                    "name": "testuser",
                    "email": "mail",
                    "id": "89ba91c18dd54abfbfde7a66936c51a6",
                    "extra": {}
                },
                "31fd15ad14784a9696fcc887dddbfaf9": {
                    "description": "test",
                    "policy_list": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0",
                        "636cd473324f4c0bbd9102cb5b62a16d"
                    ],
                    "name": "adminuser",
                    "email": "mail",
                    "id": "31fd15ad14784a9696fcc887dddbfaf9",
                    "extra": {}
                }
            }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/objects',
        json={
            "objects": {
                "67b8008a3f8d4f8e847eb628f0f7ca0e": {
                    "name": "vm1",
                    "description": "test",
                    "id": "67b8008a3f8d4f8e847eb628f0f7ca0e",
                    "extra": {},
                    "policy_list": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0",
                        "636cd473324f4c0bbd9102cb5b62a16d"
                    ]
                },
                "9089b3d2ce5b4e929ffc7e35b55eba1a": {
                    "name": "vm0",
                    "description": "test",
                    "id": "9089b3d2ce5b4e929ffc7e35b55eba1a",
                    "extra": {},
                    "policy_list": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0",
                        "636cd473324f4c0bbd9102cb5b62a16d"
                    ]
                }
            }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/actions',
        json={
            "actions": {
                "cdb3df220dc05a6ea3334b994827b068": {
                    "name": "boot",
                    "description": "test",
                    "id": "cdb3df220dc05a6ea3334b994827b068",
                    "extra": {},
                    "policy_list": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0",
                        "636cd473324f4c0bbd9102cb5b62a16d"
                    ]
                },
                "9f5112afe9b34a6c894eb87246ccb7aa": {
                    "name": "start",
                    "description": "test",
                    "id": "9f5112afe9b34a6c894eb87246ccb7aa",
                    "extra": {},
                    "policy_list": [
                        "f8f49a779ceb47b3ac810f01ef71b4e0",
                        "636cd473324f4c0bbd9102cb5b62a16d"
                    ]
                }
            }
        }
    )
    m.register_uri(
        'GET',
        'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/subject_assignments',
        json={
            "subject_assignments": {
                "826c1156d0284fc9b4b2ddb279f63c52": {
                    "category_id": "14e6ae0ba34d458b876c791b73aa17bd",
                    "assignments": [
                        "24ea95256c5f4c888c1bb30a187788df",
                        "6b227b77184c48b6a5e2f3ed1de0c02a",
                        "31928b17ec90438ba5a2e50ae7650e63",
                        "4e60f554dd3147af87595fb6b37dcb13",
                        "7a5541b63a024fa88170a6b59f99ccd7",
                        "dd2af27812f742029d289df9687d6126",
                        "4d4b3c3ba45e48589b382a6e369bafbe",
                    ],
                    "id": "826c1156d0284fc9b4b2ddb279f63c52",
                    "subject_id": "89ba91c18dd54abfbfde7a66936c51a6",
                    "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
                },
                "7407ffc1232944279b0cbcb0847c86f7": {
                    "category_id": "315072d40d774c43a89ff33937ed24eb",
                    "assignments": [
                        "6b227b77184c48b6a5e2f3ed1de0c02a",
                        "31928b17ec90438ba5a2e50ae7650e63",
                        "7a5541b63a024fa88170a6b59f99ccd7",
                        "dd2af27812f742029d289df9687d6126",
                    ],
                    "id": "7407ffc1232944279b0cbcb0847c86f7",
                    "subject_id": "89ba91c18dd54abfbfde7a66936c51a6",
                    "policy_id": "3e65256389b448cb9897917ea235f0bb"
                }
            }
        }
    )
    m.register_uri(
        'GET',
        'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/object_assignments',
        json={
            "object_assignments": {
                "201ad05fd3f940948b769ab9214fe295": {
                    "object_id": "9089b3d2ce5b4e929ffc7e35b55eba1a",
                    "assignments": [
                        "030fbb34002e4236a7b74eeb5fd71e35",
                        "4b7793dbae434c31a77da9d92de9fa8c",
                        '11209d83b167438cb8ab3e5d5351329e',
                    ],
                    "id": "201ad05fd3f940948b769ab9214fe295",
                    "category_id": "33aece52d45b4474a20dc48a76800daf",
                    "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
                },
                "90c5e86f8be34c0298fbd1973e4fb043": {
                    "object_id": "67b8008a3f8d4f8e847eb628f0f7ca0e",
                    "assignments": [
                        "7dc76c6142af47c88b60cc2b0df650ba",
                        "4b7793dbae434c31a77da9d92de9fa8c",
                        '11209d83b167438cb8ab3e5d5351329e'
                    ],
                    "id": "90c5e86f8be34c0298fbd1973e4fb043",
                    "category_id": "6d48500f639d4c2cab2b1f33ef93a1e8",
                    "policy_id": "3e65256389b448cb9897917ea235f0bb"
                }
            }
        }
    )
    m.register_uri(
        'GET',
        'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/action_assignments',
        json={
            "action_assignments": {
                "2128e3ffbd1c4ef5be515d625745c2d4": {
                    "category_id": "241a2a791554421a91c9f1bc564aa94d",
                    "action_id": "cdb3df220dc05a6ea3334b994827b068",
                    "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
                    "id": "2128e3ffbd1c4ef5be515d625745c2d4",
                    "assignments": [
                        "570c036781e540dc9395b83098c40ba7",
                        "7fe17d7a2e3542719f8349c3f2273182",
                        "015ca6f40338422ba3f692260377d638",
                        "23d44c17bf88480f83e8d57d2aa1ea79",
                        '5ced7ea5e1714f0888d6b4f94c32c29c',
                    ]
                },
                "cffb98852f3a4110af7a0ddfc4e19201": {
                    "category_id": "4a2c5abaeaf644fcaf3ca8df64000d53",
                    "action_id": "cdb3df220dc04a6ea3334b994827b068",
                    "policy_id": "3e65256389b448cb9897917ea235f0bb",
                    "id": "cffb98852f3a4110af7a0ddfc4e19201",
                    "assignments": [
                        "570c036781e540dc9395b83098c40ba7",
                        "7fe17d7a2e3542719f8349c3f2273182",
                        "015ca6f40338422ba3f692260377d638",
                        "23d44c17bf88480f83e8d57d2aa1ea79"
                    ]
                }
            }
        }
    )
    m.register_uri(
        'GET',
        'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/subject_assignments/'
        '89ba91c18dd54abfbfde7a66936c51a6',
        json={
            "subject_assignments": {
                "826c1156d0284fc9b4b2ddb279f63c52": {
                    "category_id": "14e6ae0ba34d458b876c791b73aa17bd",
                    "assignments": [
                        "24ea95256c5f4c888c1bb30a187788df",
                        "6b227b77184c48b6a5e2f3ed1de0c02a",
                        "31928b17ec90438ba5a2e50ae7650e63",
                        "4e60f554dd3147af87595fb6b37dcb13",
                        "7a5541b63a024fa88170a6b59f99ccd7",
                        "4d4b3c3ba45e48589b382a6e369bafbe"
                    ],
                    "id": "826c1156d0284fc9b4b2ddb279f63c52",
                    "subject_id": "89ba91c18dd54abfbfde7a66936c51a6",
                    "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
                }
            }
        }
    )
    m.register_uri(
        'GET',
        'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/object_assignments/'
        '67b8008a3f8d4f8e847eb628f0f7ca0e',
        json={
            "object_assignments": {
                "201ad05fd3f940948b769ab9214fe295": {
                    "object_id": "67b8008a3f8d4f8e847eb628f0f7ca0e",
                    "assignments": [
                        "030fbb34002e4236a7b74eeb5fd71e35",
                        "11209d83b167438cb8ab3e5d5351329e"
                    ],
                    "id": "201ad05fd3f940948b769ab9214fe295",
                    "category_id": "6d48500f639d4c2cab2b1f33ef93a1e8",
                    "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
                }
            }
        }
    )
    m.register_uri(
        'GET',
        'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/action_assignments/'
        'cdb3df220dc05a6ea3334b994827b068',
        json={
            "action_assignments": {
                "2128e3ffbd1c4ef5be515d625745c2d4": {
                    "category_id": "241a2a791554421a91c9f1bc564aa94d",
                    "action_id": "cdb3df220dc05a6ea3334b994827b068",
                    "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
                    "id": "2128e3ffbd1c4ef5be515d625745c2d4",
                    "assignments": [
                        "570c036781e540dc9395b83098c40ba7",
                        "7fe17d7a2e3542719f8349c3f2273182",
                        "015ca6f40338422ba3f692260377d638",
                        "f8f49a779ceb47b3ac810f01ef71b4e0"
                    ]
                }
            }
        }
    )
    m.register_uri(
        'GET', 'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/rules',
        json={
            "rules": {
                "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
                "rules": [
                    {
                        "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
                        "rule": [
                            "24ea95256c5f4c888c1bb30a187788df",
                            "030fbb34002e4236a7b74eeb5fd71e35",
                            "570c036781e540dc9395b83098c40ba7"
                        ],
                        "enabled": True,
                        "id": "0201a2bcf56943c1904dbac016289b71",
                        "instructions": [
                            {
                                "decision": "grant"
                            }
                        ],
                        "meta_rule_id": "4700cc0e38ef4cffa34025602d267c9e"
                    },
                    {
                        "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
                        "rule": [
                            "4d4b3c3ba45e48589b382a6e369bafbe",
                            '11209d83b167438cb8ab3e5d5351329e',
                            '5ced7ea5e1714f0888d6b4f94c32c29c'
                        ],
                        "enabled": True,
                        "id": "0bd7da3b20bb4b57af10c0e362aac847",
                        "instructions": [
                            {
                                "decision": "grant"
                            }
                        ],
                        "meta_rule_id": "4700cc0e38ef4cffa34025602d267c9e"
                    }
                ]
            }
        }
    )

    m.register_uri(
        'GET', 'http://127.0.0.1:8000/pipelines',
        json={
            "pipelines": {
                'b3d3e18abf3340e8b635fd49e6634ccd': {
                    'starttime': '1548688120.3931532',
                    "port": '20000',
                    "server_ip": '127.0.0.1',
                    "status": 'up',
                    "log": '/tmp/moon_policy_id_2.log'
                }

            }
        }
    )

    m.register_uri(
        'GET', 'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/subject_data',
        json={
            'subject_data': [
                {
                    'policy_id': 'f8f49a779ceb47b3ac810f01ef71b4e0',
                    'category_id': '14e6ae0ba34d458b876c791b73aa17bd',
                    'data': {
                        '4d4b3c3ba45e48589b382a6e369bafbe': {
                            'id': '4d4b3c3ba45e48589b382a6e369bafbe',
                            'name': 'testuser',
                            'description': 'description of testuser',
                            'category_id': '14e6ae0ba34d458b876c791b73aa17bd',
                            'policy_id': 'f8f49a779ceb47b3ac810f01ef71b4e0'
                        }
                    }
                },
            ]
        }
    )

    m.register_uri(
        'GET', 'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/object_data',
        json={
            'object_data': [
                {
                    'policy_id': 'f8f49a779ceb47b3ac810f01ef71b4e0',
                    'category_id': '6d48500f639d4c2cab2b1f33ef93a1e8',
                    'data': {
                        '11209d83b167438cb8ab3e5d5351329e': {
                            'id': '11209d83b167438cb8ab3e5d5351329e',
                            'name': 'testuser',
                            'description': 'description of testuser',
                            'category_id': '6d48500f639d4c2cab2b1f33ef93a1e8',
                            'policy_id': 'f8f49a779ceb47b3ac810f01ef71b4e0'
                        }
                    }
                },
            ]
        }
    )

    m.register_uri(
        'GET', 'http://127.0.0.1:8000/policies/f8f49a779ceb47b3ac810f01ef71b4e0/action_data',
        json={
            'action_data': [
                {
                    'policy_id': 'f8f49a779ceb47b3ac810f01ef71b4e0',
                    'category_id': '241a2a791554421a91c9f1bc564aa94d',
                    'data': {
                        '5ced7ea5e1714f0888d6b4f94c32c29c': {
                            'id': '5ced7ea5e1714f0888d6b4f94c32c29c',
                            'name': 'testuser',
                            'description': 'description of testuser',
                            'category_id': '241a2a791554421a91c9f1bc564aa94d',
                            'policy_id': 'f8f49a779ceb47b3ac810f01ef71b4e0'
                        }
                    }
                }
            ]
        }
    )

    m.register_uri(
        'GET', 'http://127.0.0.1:8000/slaves',
        json={
            "slaves": {
                "24aa2a391554421a98c9f1bc564ae94d": {
                    "name": "slave name",
                    "address": "http://slave"
                }
            }
        }
    )

    m.register_uri(
        'PUT', 'http://127.0.0.1:20000/update/policy/f8f49a779ceb47b3ac810f01ef71b4e0',
        json={}
    )
    m.register_uri(
        'DELETE', 'http://127.0.0.1:20000/update/policy/f8f49a779ceb47b3ac810f01ef71b4e0',
        json={}
    )
    m.register_uri(
        'PUT', 'http://127.0.0.1:20000/update/policy/eac0ecd09ceb47b3ac810f01ef71b4e0',
        json={},
        status_code=208
    )
    m.register_uri(
        'DELETE', 'http://127.0.0.1:20000/update/policy/eac0ecd09ceb47b3ac810f01ef71b4e0',
        json={}
    )
    m.register_uri(
        'PUT', 'http://127.0.0.1:20000/update/pdp/b3d3e18abf3340e8b635fd49e6634ccd',
        json={}
    )
    m.register_uri(
        'DELETE', 'http://127.0.0.1:20000/update/pdp/b3d3e18abf3340e8b635fd49e6634ccd',
        json={}
    )
    m.register_uri(
        'DELETE', 'http://127.0.0.1:20000/update/assignment/'
                  'f8f49a779ceb47b3ac810f01ef71b4e0/subject',
        json={}
    )
    m.register_uri(
        'DELETE', 'http://127.0.0.1:20000/update/assignment/'
                  'f8f49a779ceb47b3ac810f01ef71b4e0/object',
        json={}
    )
    m.register_uri(
        'DELETE', 'http://127.0.0.1:20000/update/assignment/'
                  'f8f49a779ceb47b3ac810f01ef71b4e0/action',
        json={}
    )
    m.register_uri(
        'PUT',
        'http://127.0.0.1:20000/update/perimeter/89ba91c18dd54abfbfde7a66936c51a6/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/subject',
        json={}
    )
    m.register_uri(
        'PUT',
        'http://127.0.0.1:20000/update/perimeter/31fd15ad14784a9696fcc887dddbfaf9/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/subject',
        json={}
    )
    m.register_uri(
        'PUT',
        'http://127.0.0.1:20000/update/perimeter/67b8008a3f8d4f8e847eb628f0f7ca0e/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/object',
        json={}
    )
    m.register_uri(
        'PUT',
        'http://127.0.0.1:20000/update/perimeter/9089b3d2ce5b4e929ffc7e35b55eba1a/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/object',
        json={}
    )
    m.register_uri(
        'PUT',
        'http://127.0.0.1:20000/update/perimeter/cdb3df220dc05a6ea3334b994827b068/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/action',
        json={}
    )
    m.register_uri(
        'PUT',
        'http://127.0.0.1:20000/update/perimeter/9f5112afe9b34a6c894eb87246ccb7aa/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/action',
        json={}
    )

    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/perimeter/89ba91c18dd54abfbfde7a66936c51a6/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/subject',
        json={}
    )
    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/perimeter/31fd15ad14784a9696fcc887dddbfaf9/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/subject',
        json={}
    )
    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/perimeter/67b8008a3f8d4f8e847eb628f0f7ca0e/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/object',
        json={}
    )
    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/perimeter/9089b3d2ce5b4e929ffc7e35b55eba1a/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/object',
        json={}
    )
    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/perimeter/cdb3df220dc05a6ea3334b994827b068/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/action',
        json={}
    )
    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/perimeter/9f5112afe9b34a6c894eb87246ccb7aa/'
        'f8f49a779ceb47b3ac810f01ef71b4e0/action',
        json={}
    )

    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/rule/f8f49a779ceb47b3ac810f01ef71b4e0/'
        '0201a2bcf56943c1904dbac016289b71',
        json={}
    )

    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/rule/f8f49a779ceb47b3ac810f01ef71b4e0/'
        '0bd7da3b20bb4b57af10c0e362aac847',
        json={}
    )
    m.register_uri(
        'PUT',
        'http://127.0.0.1:20000/update/model/cd923d8633ff4978ab0e99938f5153d6',
        json={}
    )
    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/model/cd923d8633ff4978ab0e99938f5153d6',
        json={}
    )

    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/meta_data/14e6ae0ba34d458b876c791b73aa17bd/subject',
        json={}
    )

    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/meta_data/241a2a791554421a91c9f1bc564aa94d/action',
        json={}
    )

    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/meta_data/6d48500f639d4c2cab2b1f33ef93a1e8/object',
        json={}
    )

    m.register_uri(
        'PUT',
        'http://127.0.0.1:20000/update/meta_rule/4700cc0e38ef4cffa34025602d267c9e',
        json={}
    )
    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/meta_rule/4700cc0e38ef4cffa34025602d267c9e',
        json={}
    )
    m.register_uri(
        'GET',
        'http://127.0.0.1:20000/authz/testuser/vm1/boot',
        json={},
        status_code=204
    )
    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/data/4d4b3c3ba45e48589b382a6e369bafbe/subject',
        json={}
    )

    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/data/11209d83b167438cb8ab3e5d5351329e/object',
        json={}
    )
    m.register_uri(
        'DELETE',
        'http://127.0.0.1:20000/update/data/5ced7ea5e1714f0888d6b4f94c32c29c/action',
        json={}
    )
    m.register_uri(
        'PUT',
        'http://127.0.0.1:20000/update/slave/24aa2a391554421a98c9f1bc564ae94d',
        json={}
    )
    m.register_uri(
        'GET',
        '/authz/a64beb1cc224474fb4badd43173e7101/testuser/vm1/boot',
        json={"result": True}
    )
    m.register_uri(
        'GET',
        'http://127.0.0.1:20000/authz/a64beb1cc224474fb4badd43173e7101/testuser/vm1/boot',
        json={"result": True}
    )


