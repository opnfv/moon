# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import base64
import json
import os
import pickle
import pytest
import requests_mock
from uuid import uuid4

CONF = {
    "openstack": {
        "keystone": {
            "url": "http://keystone:5000/v3",
            "user": "admin",
            "check_token": False,
            "password": "p4ssw0rd",  # nosec
            "domain": "default",
            "certificate": False,
            "project": "admin"
        }
    },
    "components": {
        "wrapper": {
            "bind": "0.0.0.0",  # nosec
            "port": 8080,
            "container": "wukongsun/moon_wrapper:v4.3",
            "timeout": 5,
            "hostname": "wrapper"
        },
        "manager": {
            "bind": "0.0.0.0",  # nosec
            "port": 8082,
            "container": "wukongsun/moon_manager:v4.3",
            "hostname": "manager"
        },
        "port_start": 31001,
        "orchestrator": {
            "bind": "0.0.0.0",  # nosec
            "port": 8083,
            "container": "wukongsun/moon_orchestrator:v4.3",
            "hostname": "orchestrator"
        },
        "interface": {
            "bind": "0.0.0.0",
            "port": 8080,
            "container": "wukongsun/moon_interface:v4.3",
            "hostname": "interface"
        }
    },
    "plugins": {
        "session": {
            "port": 8082,
            "container": "asteroide/session:latest"
        },
        "authz": {
            "port": 8081,
            "container": "wukongsun/moon_authz:v4.3"
        }
    },
    "logging": {
        "handlers": {
            "file": {
                "filename": "/tmp/moon.log",  # nosec
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "custom",
                "backupCount": 3,
                "maxBytes": 1048576
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "brief",
                "level": "INFO",
                "stream": "ext://sys.stdout"
            }
        },
        "formatters": {
            "brief": {
                "format": "%(levelname)s %(name)s %(message)-30s"
            },
            "custom": {
                "format": "%(asctime)-15s %(levelname)s %(name)s %(message)s"
            }
        },
        "root": {
            "handlers": [
                "console"
            ],
            "level": "ERROR"
        },
        "version": 1,
        "loggers": {
            "moon": {
                "handlers": [
                    "console",
                    "file"
                ],
                "propagate": False,
                "level": "DEBUG"
            }
        }
    },
    "slave": {
        "name": None,
        "master": {
            "url": None,
            "login": None,
            "password": None  # nosec
        }
    },
    "docker": {
        "url": "tcp://172.88.88.1:2376",
        "network": "moon"
    },
    "database": {
        "url": "sqlite:///database.db",
        # "url": "mysql+pymysql://moon:p4sswOrd1@db/moon",
        "driver": "sql"
    },
    "messenger": {
        "url": "rabbit://moon:p4sswOrd1@messenger:5672/moon"
    }
}

COMPONENTS = (
    "logging",
    "openstack/keystone",
    "database",
    "slave",
    "components/manager",
    "components/orchestrator",
    "components/interface",
    "components/wrapper",
)

CONTEXT = {
        "project_id": "a64beb1cc224474fb4badd43173e7101",
        "pdp_id": "b3d3e18abf3340e8b635fd49e6634ccd",
        "invalid_project_id" : "invalid_project_id",
        "invalid_pdp_id": "invalid_pdp_id",
        "project_with_no_interface_key" : "232399a4-de5f-11e7-8001-3863bbb766f3",
        "subject_name": "testuser",
        "object_name": "vm1",
        "action_name": "boot",
        "request_id": uuid4().hex,
        "interface_name": "interface",
        "manager_url": "http://{}:{}".format(
            CONF["components"]["manager"]["hostname"],
            CONF["components"]["manager"]["port"]
        ),
        "cookie": uuid4().hex
    }


def get_b64_conf(component=None):
    if component == "components":
        return base64.b64encode(
            json.dumps(CONF["components"]).encode('utf-8')+b"\n").decode('utf-8')
    elif component in CONF:
        return base64.b64encode(
            json.dumps(
                CONF[component]).encode('utf-8')+b"\n").decode('utf-8')
    elif not component:
        return base64.b64encode(
            json.dumps(CONF).encode('utf-8')+b"\n").decode('utf-8')
    elif "/" in component:
        key1, _, key2 = component.partition("/")
        return base64.b64encode(
            json.dumps(
                CONF[key1][key2]).encode('utf-8')+b"\n").decode('utf-8')


MOCK_URLS = [
    ('GET', 'http://consul:8500/v1/kv/components?recurse=true',
        {'json': {"Key": key, "Value": get_b64_conf(key)}
         for key in COMPONENTS}
     ),
    ('POST', 'http://keystone:5000/v3/auth/tokens',
        {'headers': {'X-Subject-Token': "111111111"}}),
    ('DELETE', 'http://keystone:5000/v3/auth/tokens',
        {'headers': {'X-Subject-Token': "111111111"}}),
    ('POST', 'http://keystone:5000/v3/users?name=testuser&domain_id=default',
        {'json': {"users": {}}}),
    ('GET', 'http://keystone:5000/v3/users?name=testuser&domain_id=default',
        {'json': {"users": {}}}),
    ('POST', 'http://keystone:5000/v3/users/',
        {'json': {"users": [{
            "id": "1111111111111"
        }]}}),
]


@pytest.fixture
def db():
    return CONF['database']


@pytest.fixture
def context():
    return CONTEXT


def set_env_variables():
    os.environ['UUID'] = "1111111111"
    os.environ['TYPE'] = "authz"
    os.environ['PORT'] = "8081"
    os.environ['PDP_ID'] = "b3d3e18abf3340e8b635fd49e6634ccd"
    os.environ['META_RULE_ID'] = "f8f49a779ceb47b3ac810f01ef71b4e0"
    os.environ['KEYSTONE_PROJECT_ID'] = CONTEXT['project_id']


def get_pickled_context():
    from python_moonutilities.context import Context
    from python_moonutilities.cache import Cache
    CACHE = Cache()
    CACHE.update()
    _context = Context(context(), CACHE)
    _context.increment_index()
    _context.pdp_set['effect'] = 'grant'
    _context.pdp_set[os.environ['META_RULE_ID']]['effect'] = 'grant'
    return pickle.dumps(_context)


@pytest.fixture(autouse=True)
def set_consul_and_db(monkeypatch):
    """ Modify the response from Requests module
    """
    set_env_variables()
    with requests_mock.Mocker(real_http=True) as m:
        for component in COMPONENTS:
            m.register_uri(
                'GET', 'http://consul:8500/v1/kv/{}'.format(component),
                json=[{'Key': component, 'Value': get_b64_conf(component)}]
                )
        # for _data in MOCK_URLS:
        #     m.register_uri(_data[0], _data[1], **_data[2])
        m.register_uri(
            'GET', 'http://consul:8500/v1/kv/components?recurse=true',
            json=[
                {"Key": key, "Value": get_b64_conf(key)} for key in COMPONENTS
            ],
            )
        m.register_uri(
            'GET', 'http://consul:8500/v1/kv/plugins/authz',
            json=[
                {
                    "LockIndex": 0,
                    "Key": "plugins/authz",
                    "Flags": 0,
                    "Value": "eyJjb250YWluZXIiOiAid3Vrb25nc3VuL21vb25fYXV0aHo6djQuMyIsICJwb3J0IjogODA4MX0=",
                    "CreateIndex": 14,
                    "ModifyIndex": 656
                }
            ],
            )
        m.register_uri(
            'POST', 'http://keystone:5000/v3/auth/tokens',
            headers={'X-Subject-Token': "111111111"}
        )
        m.register_uri(
            'DELETE', 'http://keystone:5000/v3/auth/tokens',
            headers={'X-Subject-Token': "111111111"}
        )
        m.register_uri(
            'POST', 'http://keystone:5000/v3/users?name=testuser&domain_id=default',
            json={"users": {}}
        )
        m.register_uri(
            'GET', 'http://keystone:5000/v3/users?name=testuser&domain_id=default',
            json={"users": {}}
        )
        m.register_uri(
            'POST', 'http://keystone:5000/v3/users/',
            json={"users": [{
                "id": "1111111111111"
            }]}
        )
        m.register_uri(
            'GET', 'http://orchestrator:8083/pods',
            json={
              "pods": {
                "721760dd-de5f-11e7-8001-3863bbb766f3": [
                  {
                    "pdp_id": "b3d3e18abf3340e8b635fd49e6634ccd",
                    "port": 8080,
                    "genre": "interface",
                    "name": "pipeline-paltry",
                    "keystone_project_id": "a64beb1cc224474fb4badd43173e7101",
                    "namespace": "moon",
                    "container": "wukongsun/moon_pipeline:v4.3"
                  },
                  {
                    "pdp_id": "b3d3e18abf3340e8b635fd49e6634ccd",
                    "meta_rule_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
                    "port": 8081,
                    "genre": "authz",
                    "name": "authz-economic",
                    "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0",
                    "keystone_project_id": "a64beb1cc224474fb4badd43173e7101",
                    "namespace": "moon",
                    "container": "wukongsun/moon_authz:v4.3"
                  },
                  {
                    "pdp_id": "invalid_pdp_id",
                    "port": 8080,
                    "genre": "interface",
                    "name": "pipeline-paltry",
                    "keystone_project_id": "invalid_project_id",
                    "namespace": "moon",
                    "container": "wukongsun/moon_authz:v4.3"
                  }
                ],
                "232399a4-de5f-11e7-8001-3863bbb766f3": [
                  {
                    "port": 8080,
                    "namespace": "moon",
                    "name": "wrapper-paltry",
                    "container": "wukongsun/moon_wrapper:v4.3.1"
                  }
                ]
              }
            }
        )
        m.register_uri(
            'GET', 'http://orchestrator:8083/pods/authz-economic',
            json={
              "pods": None
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/pdp',
            json={
                "pdps": {
                    "b3d3e18abf3340e8b635fd49e6634ccd": {
                        "description": "test",
                        "security_pipeline": [
                            "f8f49a779ceb47b3ac810f01ef71b4e0"
                        ],
                        "name": "pdp_rbac",
                        "keystone_project_id": "a64beb1cc224474fb4badd43173e7101"
                    },
                    "invalid_pdp_id":{

                        "description": "test",
                        "security_pipeline": [
                            "f8f49a779ceb47b3ac810f01ef71b4e0"
                        ],
                        "name": "pdp_rbac",
                        "keystone_project_id": "invalid_project_id"
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/policies',
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
            'GET', 'http://manager:8082/models',
            json={
                "models": {
                    "cd923d8633ff4978ab0e99938f5153d6": {
                        "name": "RBAC",
                        "meta_rules": [
                            "f8f49a779ceb47b3ac810f01ef71b4e0"
                        ],
                        "description": "test"
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/meta_rules',
            json={
                "meta_rules": {
                    "f8f49a779ceb47b3ac810f01ef71b4e0": {
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
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/subjects',
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
                        "extra":  {}
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
                        "extra":  {}
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/objects',
            json={
                "objects": {
                    "67b8008a3f8d4f8e847eb628f0f7ca0e": {
                        "name": "vm1",
                        "description": "test",
                        "id": "67b8008a3f8d4f8e847eb628f0f7ca0e",
                        "extra":  {},
                        "policy_list": [
                            "f8f49a779ceb47b3ac810f01ef71b4e0",
                            "636cd473324f4c0bbd9102cb5b62a16d"
                        ]
                    },
                    "9089b3d2ce5b4e929ffc7e35b55eba1a": {
                        "name": "vm0",
                        "description": "test",
                        "id": "9089b3d2ce5b4e929ffc7e35b55eba1a",
                        "extra":  {},
                        "policy_list": [
                            "f8f49a779ceb47b3ac810f01ef71b4e0",
                            "636cd473324f4c0bbd9102cb5b62a16d"
                        ]
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/actions',
            json={
                "actions": {
                    "cdb3df220dc05a6ea3334b994827b068": {
                        "name": "boot",
                        "description": "test",
                        "id": "cdb3df220dc04a6ea3334b994827b068",
                        "extra":  {},
                        "policy_list": [
                            "f8f49a779ceb47b3ac810f01ef71b4e0",
                            "636cd473324f4c0bbd9102cb5b62a16d"
                        ]
                    },
                    "cdb3df220dc04a6ea3334b994827b068": {
                        "name": "stop",
                        "description": "test",
                        "id": "cdb3df220dc04a6ea3334b994827b068",
                        "extra":  {},
                        "policy_list": [
                            "f8f49a779ceb47b3ac810f01ef71b4e0",
                            "636cd473324f4c0bbd9102cb5b62a16d"
                        ]
                    },
                    "9f5112afe9b34a6c894eb87246ccb7aa": {
                        "name": "start",
                        "description": "test",
                        "id": "9f5112afe9b34a6c894eb87246ccb7aa",
                        "extra":  {},
                        "policy_list": [
                            "f8f49a779ceb47b3ac810f01ef71b4e0",
                            "636cd473324f4c0bbd9102cb5b62a16d"
                        ]
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/subject_assignments',
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
                            "dd2af27812f742029d289df9687d6126"
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
                            "dd2af27812f742029d289df9687d6126"
                        ],
                        "id": "7407ffc1232944279b0cbcb0847c86f7",
                        "subject_id": "89ba91c18dd54abfbfde7a66936c51a6",
                        "policy_id": "3e65256389b448cb9897917ea235f0bb"
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/object_assignments',
            json={
                "object_assignments": {
                    "201ad05fd3f940948b769ab9214fe295": {
                        "object_id": "9089b3d2ce5b4e929ffc7e35b55eba1a",
                        "assignments": [
                            "030fbb34002e4236a7b74eeb5fd71e35",
                            "06bcb8655b9d46a9b90e67ef7c825b50",
                            "34eb45d7f46d4fb6bc4965349b8e4b83",
                            "4b7793dbae434c31a77da9d92de9fa8c"
                        ],
                        "id": "201ad05fd3f940948b769ab9214fe295",
                        "category_id": "6d48500f639d4c2cab2b1f33ef93a1e8",
                        "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
                    },
                    "90c5e86f8be34c0298fbd1973e4fb043": {
                        "object_id": "67b8008a3f8d4f8e847eb628f0f7ca0e",
                        "assignments": [
                            "a098918e915b4b12bccb89f9a3f3b4e4",
                            "06bcb8655b9d46a9b90e67ef7c825b50",
                            "7dc76c6142af47c88b60cc2b0df650ba",
                            "4b7793dbae434c31a77da9d92de9fa8c"
                        ],
                        "id": "90c5e86f8be34c0298fbd1973e4fb043",
                        "category_id": "33aece52d45b4474a20dc48a76800daf",
                        "policy_id": "3e65256389b448cb9897917ea235f0bb"
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/action_assignments',
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
                            "23d44c17bf88480f83e8d57d2aa1ea79"
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
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/subject_assignments/89ba91c18dd54abfbfde7a66936c51a6',
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
                            "dd2af27812f742029d289df9687d6126"
                        ],
                        "id": "826c1156d0284fc9b4b2ddb279f63c52",
                        "subject_id": "89ba91c18dd54abfbfde7a66936c51a6",
                        "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/object_assignments/67b8008a3f8d4f8e847eb628f0f7ca0e',
            json={
                "object_assignments": {
                    "201ad05fd3f940948b769ab9214fe295": {
                        "object_id": "67b8008a3f8d4f8e847eb628f0f7ca0e",
                        "assignments": [
                            "030fbb34002e4236a7b74eeb5fd71e35",
                            "06bcb8655b9d46a9b90e67ef7c825b50",
                            "34eb45d7f46d4fb6bc4965349b8e4b83",
                            "4b7793dbae434c31a77da9d92de9fa8c"
                        ],
                        "id": "201ad05fd3f940948b769ab9214fe295",
                        "category_id": "6d48500f639d4c2cab2b1f33ef93a1e8",
                        "policy_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/action_assignments/cdb3df220dc05a6ea3334b994827b068',
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
                            "23d44c17bf88480f83e8d57d2aa1ea79"
                        ]
                    }
                }
            }
        )
        m.register_uri(
            'GET', 'http://manager:8082/policies/f8f49a779ceb47b3ac810f01ef71b4e0/rules',
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
                            "meta_rule_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
                        },
                        {
                            "policy_id": "ecc2451c494e47b5bca7250cd324a360",
                            "rule": [
                                "54f574cd2043468da5d65e4f6ed6e3c9",
                                "6559686961a3490a978f246ac9f85fbf",
                                "ac0d1f600bf447e8bd2f37b7cc47f2dc"
                            ],
                            "enabled": True,
                            "id": "a83fed666af8436192dfd8b3c83a6fde",
                            "instructions": [
                                {
                                    "decision": "grant"
                                }
                            ],
                            "meta_rule_id": "f8f49a779ceb47b3ac810f01ef71b4e0"
                        }
                    ]
                }
            }
        )
        m.register_uri(
            'POST', 'http://127.0.0.1:8081/authz',
            content=get_pickled_context()
        )
        m.register_uri(
            'GET', 'http://pipeline-paltry:8080/authz/{}/{}/{}/{}'.format(
                CONTEXT.get("pdp_id"),
                CONTEXT.get("subject_name"),
                CONTEXT.get("object_name"),
                CONTEXT.get("action_name"),
            ),
            json={"result": True, "message": "================"}
        )
        m.register_uri(
            'GET', 'http://pipeline-paltry:8080/authz/{}/{}/{}/{}'.format(
                CONTEXT.get("invalid_pdp_id"),
                CONTEXT.get("subject_name"),
                CONTEXT.get("object_name"),
                CONTEXT.get("action_name"),
            ),
            status_code=500
        )
        # from moon_db.db_manager import init_engine, run
        # engine = init_engine()
        # run("upgrade", logging.getLogger("db_manager"), engine)
        yield m
        # os.unlink(CONF['database']['url'].replace("sqlite:///", ""))


