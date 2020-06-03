# Software Name: MOON:

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

import pytest
import os
import yaml

pytest_plugins = ["pytester"]
CONF = """
debug: true

database:
  # url: mysql+pymysql://moon:p4sswOrd1@db/moon
  url: sqlite:////tmp/database.db
  driver: moon_manager.plugins.sql
  migration_dir: moon_manager.api.db.migrations
  # migration_dir: /home/tom/projets/moon/moon_manager/moon_manager/api/db/migrations/

management:
  url: http://127.0.0.1:8000
  user: admin
  password: admin
  token_file: moon.pwd

orchestration:
  driver: moon_manager.plugins.pyorchestrator
  connection: local
  #  driver: moon_manager.plugins.docker_compose
  #  connection: ssh://admin:admin@1.1.1.1
  #  driver: moon_manager.plugins.kubernetes
  #  connection: ~/.kube/config
  port: 10000...10100
  config_dir: /tmp

information:
#  driver: moon_manager.plugins.moon_openstack_plugin
#  subjects:
#    driver:
#    - moon_manager.plugins.openstack
#  objects:
#    driver:
#    - moon_manager.plugins.openstack
#  actions:
#    driver:
#    - moon_manager.plugins.openstack
  openstack:
    driver: moon_manager.plugins.moon_openstack_plugin
    url: http://keystone:5000/v3
    user: admin
    password: p4ssw0rd
    domain: default
    project: admin
    check_token: false
    certificate: false
  global_attrs:
    driver: moon_manager.plugins.global_attrs
    attributes:

plugins:
  directory: /var/moon/plugins

components:
  manager:
    port: 8080
    bind: 0.0.0.0
    hostname: manager

logging:
  version: 1

  formatters:
    brief:
      format: "%(levelname)s %(name)s %(message)-30s"
    custom:
      format: "%(asctime)-15s %(levelname)s %(name)s %(message)s"

  handlers:
    console:
      class : logging.StreamHandler
      formatter: custom
      level   : INFO
      stream  : ext://sys.stdout
    file:
      class : logging.handlers.RotatingFileHandler
      formatter: custom
      level   : DEBUG
      filename: /tmp/moon.log
      maxBytes: 1048576
      backupCount: 3

  loggers:
    moon:
      level: DEBUG
      handlers: [console, file]
      propagate: no

  root:
    level: ERROR
    handlers: [console]

"""
POLICY = """
{
    "policies": [
        {
            "name": "MLS Policy",
            "genre": "authz",
            "description": "MLS policy",
            "model": {
                "name": "MLS"
            },
            "mandatory": true,
            "override": true
        }
    ],
    "models": [
        {
            "name": "MLS",
            "description": "",
            "meta_rules": [
                {
                    "name": "mls"
                }
            ],
            "override": true
        }
    ],
    "subjects": [
        {
            "name": "admin",
            "description": "",
            "extra": {},
            "policies": [
                {
                    "name": "MLS Policy"
                }
            ]
        },
        {
            "name": "demo",
            "description": "",
            "extra": {},
            "policies": [
                {
                    "name": "MLS Policy"
                }
            ]
        }
    ],
    "subject_categories": [
        {
            "name": "level",
            "description": "subject level"
        }
    ],
    "subject_data": [
        {
            "name": "high",
            "description": "",
            "policies": [],
            "category": {
                "name": "level"
            }
        },
        {
            "name": "medium",
            "description": "",
            "policies": [],
            "category": {
                "name": "level"
            }
        },
        {
            "name": "low",
            "description": "",
            "policies": [],
            "category": {
                "name": "level"
            }
        }
    ],
    "subject_assignments": [
        {
            "subject": {"name": "admin"},
            "category": {"name": "level"},
            "assignments": [{"name": "high"}]
        }
    ],
    "objects": [
        {
            "name": "vm1",
            "description": "",
            "extra": {},
            "policies": [
                {
                    "name": "MLS Policy"
                }
            ]
        },
        {
            "name": "vm2",
            "description": "",
            "extra": {},
            "policies": [
                {
                    "name": "MLS Policy"
                }
            ]
        },
        {
            "name": "vm3",
            "description": "",
            "extra": {},
            "policies": [
                {
                    "name": "MLS Policy"
                }
            ]
        }
    ],
    "object_categories": [
        {
            "name": "level",
            "description": "object level"
        }
    ],
    "object_data": [
        {
            "name": "high",
            "description": "",
            "policies": [],
            "category": {
                "name": "level"
            }
        },
        {
            "name": "medium",
            "description": "",
            "policies": [],
            "category": {
                "name": "level"
            }
        },
        {
            "name": "low",
            "description": "",
            "policies": [],
            "category": {
                "name": "level"
            }
        }
    ],
    "object_assignments": [
        {
            "object": {"name": "vm1"},
            "category": {"name": "level"},
            "assignments": [{"name": "high"}]
        },
        {
            "object": {"name": "vm2"},
            "category": {"name": "level"},
            "assignments": [{"name": "medium"}]
        }
    ],
    "actions": [
        {
            "name": "use_image",
            "description": "use_image action for glance",
            "extra": {
                "component": "glance"
            },
            "policies": []
        },
        {
            "name": "get_images",
            "description": "get_images action for glance",
            "extra": {
                "component": "glance"
            },
            "policies": []
        },
        {
            "name": "update_image",
            "description": "update_image action for glance",
            "extra": {
                "component": "glance"
            },
            "policies": []
        },
        {
            "name": "set_image",
            "description": "set_image action for glance",
            "extra": {
                "component": "glance"
            },
            "policies": []
        }
    ],
    "action_categories": [
        {
            "name": "type",
            "description": ""
        }
    ],
    "action_data": [
        {
            "name": "read",
            "description": "read action",
            "policies": [],
            "category": {
                "name": "type"
            }
        },
        {
            "name": "write",
            "description": "write action",
            "policies": [],
            "category": {
                "name": "type"
            }
        },
        {
            "name": "execute",
            "description": "execute action",
            "policies": [],
            "category": {
                "name": "type"
            }
        }
    ],
    "action_assignments": [
        {
            "action": {"name": "use_image"},
            "category": {"name": "type"},
            "assignments": [{"name": "read"}, {"name": "execute"}]
        },
        {
            "action": {"name": "update_image"},
            "category": {"name": "type"},
            "assignments": [{"name": "read"}, {"name": "write"}]
        },
        {
            "action": {"name": "set_image"},
            "category": {"name": "type"},
            "assignments": [{"name": "write"}]
        }
    ],
    "meta_rules": [
        {
            "name": "mls",
            "description": "",
            "subject_categories": [{"name": "level"}],
            "object_categories": [{"name": "level"}],
            "action_categories": [{"name": "type"}]
        }
    ],
    "rules": [
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "high"}],
                "object_data": [{"name": "high"}],
                "action_data": [{"name": "read"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "high"}],
                "object_data": [{"name": "medium"}],
                "action_data": [{"name": "read"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "high"}],
                "object_data": [{"name": "low"}],
                "action_data": [{"name": "read"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "medium"}],
                "object_data": [{"name": "medium"}],
                "action_data": [{"name": "read"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "medium"}],
                "object_data": [{"name": "low"}],
                "action_data": [{"name": "read"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "low"}],
                "object_data": [{"name": "low"}],
                "action_data": [{"name": "read"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "high"}],
                "object_data": [{"name": "high"}],
                "action_data": [{"name": "write"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "high"}],
                "object_data": [{"name": "medium"}],
                "action_data": [{"name": "write"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "high"}],
                "object_data": [{"name": "low"}],
                "action_data": [{"name": "write"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "medium"}],
                "object_data": [{"name": "medium"}],
                "action_data": [{"name": "write"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "medium"}],
                "object_data": [{"name": "low"}],
                "action_data": [{"name": "write"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "low"}],
                "object_data": [{"name": "low"}],
                "action_data": [{"name": "write"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "high"}],
                "object_data": [{"name": "high"}],
                "action_data": [{"name": "execute"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "high"}],
                "object_data": [{"name": "medium"}],
                "action_data": [{"name": "execute"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "high"}],
                "object_data": [{"name": "low"}],
                "action_data": [{"name": "execute"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "medium"}],
                "object_data": [{"name": "medium"}],
                "action_data": [{"name": "execute"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "medium"}],
                "object_data": [{"name": "low"}],
                "action_data": [{"name": "execute"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        },
        {
            "meta_rule": {"name": "mls"},
            "rule": {
                "subject_data": [{"name": "low"}],
                "object_data": [{"name": "low"}],
                "action_data": [{"name": "execute"}]
            },
            "policy": {"name": "MLS Policy"},
            "instructions": [{"decision": "grant"}],
            "enabled": true
        }
    ]
}
"""
PWD = '{"_default": {"1": {"username": "admin", "password": ' \
      '"d2eeefe5df3be1d96c102bc91bd2b3c3a93d58f6c9949b91e4a478135f' \
      '383efcd66af2ede09aff03d579f44e4b6a0bd4e9d9de3dc28222fda7a70f34045fe777", ' \
      '"salt": "37df3e00b84ea5d1d5b17868b588e8c7a32fa2a18d031828ac2b6fd3c37687a2c0105' \
      '2a9c395a32b441bac2034dca1966e88039a1e83aac80795bac9c3fa92bf", "api_key": "4ec3' \
      'babcdfc765e81e099a29b9d69bb7dbe38b8f226663c09bf79061d3d97d87e30fc5e83a90557313' \
      'd4fc471d8ea4eecb4faabc9773594dc63018f503e36a22"}}}'

try:
    PWD = open("moon.pwd").read()
except FileNotFoundError:
    PWD = open("/etc/moon/moon.pwd").read()

os.environ["MOON_USERNAME"] = "admin"
os.environ["MOON_PASSWORD"] = "admin"


def get_policy_id(policies, name="MLS Policy"):
    for policy_id, policy_value in policies.get("policies").items():
        if policy_value.get("name") == name:
            return policy_id


@pytest.fixture
def run(testdir):
    open(os.path.join(str(testdir), "moon.yaml"), "w").write(CONF)
    open(os.path.join(str(testdir), "policy_example.json"), "w").write(POLICY)
    open(os.path.join(str(testdir), "moon.pwd"), "w").write(PWD)

    def do_run(*args):
        args = ["moon_manager"] + list(args)
        ret = testdir.run(*args)
        print(testdir)
        try:
            return yaml.safe_load(ret.stdout.lines[-1])
        except Exception as e:
            print(e)
            return ret.stdout
    return do_run


@pytest.fixture
def import_policy(run):
    if not get_policy_id(run("policies", "list")):
        run("import", "policy_example.json")
        assert get_policy_id(run("policies", "list"))
    return get_policy_id(run("policies", "list"))


# def test_import(run):
#     ret = run("import", "policy_example.json")
#     assert ret
#     # TODO: check if policy, meta-rule, ... have been created.


def test_slaves(run):
    ret = run("slaves", "list")
    assert "slaves" in ret


def test_pdp(run):
    ret = run("pdp", "list")
    assert "pdps" in ret


def test_policies(run):
    ret = run("policies", "list")
    assert "policies" in ret


def test_subjects(run):
    ret = run("subjects", "list")
    assert "subjects" in ret


def test_objects(run):
    ret = run("objects", "list")
    assert "objects" in ret


def test_actions(run):
    ret = run("actions", "list")
    assert "actions" in ret


def test_subject_categories(run):
    ret = run("subject_categories", "list")
    assert "subject_categories" in ret


def test_object_categories(run):
    ret = run("object_categories", "list")
    assert "object_categories" in ret


def test_action_categories(run):
    ret = run("action_categories", "list")
    assert "action_categories" in ret


# def test_subject_data(run):
#     ret = run("subject_data", "get")
#     assert "subject_data" in ret
#
#
# def test_object_data(run):
#     ret = run("object_data", "get")
#     assert "object_data" in ret
#
#
# def test_action_data(run):
#     ret = run("action_data", "get")
#     assert "action_data" in ret


def test_rules(run, import_policy):
    ret = run("rules", "list", import_policy)
    assert "rules" in ret


def test_meta_rules(run):
    ret = run("meta_rules", "list")
    assert "meta_rules" in ret


def test_models(run):
    ret = run("models", "list")
    print(ret)
    assert "models" in ret


def test_subject_assignments(run, import_policy):
    ret = run("subject_assignments", "list", "MLS Policy")
    assert "subject_assignments" in ret
    ret = run("subject_assignments", "add", "MLS Policy", "demo", "level", "low")
    assert "subject_assignments" in ret
    ret = run("subject_assignments", "delete", "MLS Policy", "demo", "level", "low")
    assert ret


def test_object_assignments(run, import_policy):
    ret = run("object_assignments", "list", "MLS Policy")
    assert "object_assignments" in ret
    ret = run("object_assignments", "add", "MLS Policy", "vm3", "level", "low")
    assert "object_assignments" in ret
    ret = run("object_assignments", "delete", "MLS Policy", "vm3", "level", "low")
    assert ret


def test_action_assignments(run, import_policy):
    ret = run("action_assignments", "list", "MLS Policy")
    assert "action_assignments" in ret
    ret = run("action_assignments", "add", "MLS Policy", "get_images", "type", "read")
    assert "action_assignments" in ret
    ret = run("action_assignments", "delete", "MLS Policy", "get_images", "type", "read")
    assert ret


# def test_complete(run, import_policy):
#     slaves = run("slaves", "get").get("slaves")
#     if not slaves:
#         ret = run("slaves", "create")
#         assert "slaves" in ret
#     if not get_policy_id(run("policies", "get")):
#         ret = run("import", "policy_example.json")
#         assert ret
# 
#     ret = run("subject_assignments", "create", "MLS Policy", "admin", "level", "high")
#     assert "subject_assignments" in ret
# 
#     subjects = run("subjects", "get", "-n", "admin").get("subjects")
#     subject_id = subjects
# 
#     ret = run("slaves", "delete", "-n", "default")
#     assert ret

def test_users(run):
    ret = run("users", "add", "bob", "-p password_bob")
    if ret != {'error': 'User bob already exists'}:
        assert ret['user_created']['username'] == 'bob'

    ret = run("users", "key", "bob", "-p password_bob")
    assert ret

    ret = run("users", "list")
    assert "users" in ret

    ret = run("users", "change_password", "bob", "-p passwordbob", "-n new_password")
    assert ret == "Wrong password"

    ret = run("users", "change_password", "bob", "-p password_bob", "-n new_password")
    assert ret['result'] == "success"

    ret = run("users", "key", "bob", "-p password_bob")
    assert not ret

    ret = run("users", "key", "bob", "-p new_password")
    assert ret
