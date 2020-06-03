# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import pytest
import requests_mock
import yaml
import mock_repo
import mock_repo.urls as register_urls
import mock_repo.data as data_mock

__CONF = """
database:
  url: sqlite:////tmp/database_test.db
  driver: moon_manager.plugins.sql
  migration_dir: moon_manager.api.db.migrations

management:
  url: http://127.0.0.1:8000
  user: admin
  password: admin
  token_file: /tmp/moon.pwd

orchestration:
  driver: moon_manager.plugins.pyorchestrator
  connection: local
  slaves:
    port: 10000...10100
  pipelines:
    port: 20000...20100

information:
  driver: moon_manager.plugins.moon_openstack_plugin
  openstack:
    url: http://keystone:5000/v3
    user: admin
    password: p4ssw0rd
    domain: default
    project: admin
    check_token: false
    certificate: false

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
      format: "%(levelname)s %(name)s %(m, confessage)-30s"
    custom:
      format: "%(asctime)-15s %(levelname)s %(name)s %(m, confessage)s"

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


@pytest.fixture
def configuration():
    return yaml.load(__CONF)


def register_cache(m):
    """ Modify the response from Requests module
    """
    conf = yaml.load(__CONF)
    # register_urls.register_components(m, conf)
    # register_urls.register_keystone(m, conf)

    register_urls.register_pdp(m, conf)
    register_urls.register_pipelines(m, conf)
    register_urls.register_meta_rules(m, conf)
    register_urls.register_policies(m, conf)
    register_urls.register_slaves(m, conf)
    register_urls.register_models(m, conf)

    register_urls.register_policy_subject(m, conf, data_mock.shared_ids["policy"]["policy_id_1"])
    register_urls.register_policy_subject_invalid_response(m, conf, data_mock.shared_ids["policy"]["policy_id_invalid_response"])

    register_urls.register_policy_object(m, conf, data_mock.shared_ids["policy"]["policy_id_1"])
    register_urls.register_policy_object_invalid_response(m, conf, data_mock.shared_ids["policy"]["policy_id_invalid_response"])

    register_urls.register_policy_action(m, conf, data_mock.shared_ids["policy"]["policy_id_1"])
    register_urls.register_policy_action_invalid_response(m, conf, data_mock.shared_ids["policy"]["policy_id_invalid_response"])

    register_urls.register_policy_subject_assignment(m, conf, data_mock.shared_ids["policy"]["policy_id_1"], data_mock.shared_ids["perimeter"]["perimeter_id_1"])

    register_urls.register_policy_subject_assignment_list(m, conf, data_mock.shared_ids["policy"]["policy_id_2"])

    register_urls.register_policy_object_assignment(m, conf, data_mock.shared_ids["policy"]["policy_id_1"], data_mock.shared_ids["perimeter"]["perimeter_id_2"])

    register_urls.register_policy_object_assignment_list(m, conf, data_mock.shared_ids["policy"]["policy_id_2"])

    register_urls.register_policy_action_assignment(m, conf, data_mock.shared_ids["policy"]["policy_id_1"], data_mock.shared_ids["perimeter"]["perimeter_id_3"])

    register_urls.register_policy_action_assignment_list(m, conf, data_mock.shared_ids["policy"]["policy_id_2"])

    register_urls.register_attributes(m, conf)

    # register_urls.register_policy_action_assignment(m, conf, "policy_id_2", "perimeter_id_2")
    # register_urls.register_policy_action_assignment(m, conf, "policy_id_2", "perimeter_id_2")
    # register_urls.register_policy_action_assignment(m, conf, "policy_id_2", "perimeter_id_2")

    register_urls.register_rules(m, conf, "policy_id1")


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    with requests_mock.Mocker(real_http=True) as m:
        register_cache(m)
        print("End registering URI")
        yield m
