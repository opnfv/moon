# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import mock_slaves
import os
import pytest
import requests_mock
import yaml


__CONF = """
debug: true

database:
  url: sqlite:////tmp/database_test.db
  driver: moon_manager.plugins.sql
  migration_dir: moon_manager.api.db.migrations

dashboard:
  root: ../dashboard/www/

management:
  url: http://127.0.0.1:8000
  user: admin
  password: admin
  token_file: db.json

orchestration:
  driver: moon_manager.plugins.pyorchestrator
  connection: local
  port: 10000...10100
  config_dir: /tmp

information:
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
      mode:
        values:
          - build
          - run
        default: build
        url: file:/etc/moon/mode
        #url: https://127.0.0.1:8080/mode
        #url: mysql+pymysql://moon:p4sswOrd1@db/moon_mode
        #url: sqlite:////tmp/database.db
        #url: driver://moon_manager.plugins.my_plugin

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


@pytest.fixture
def slaves():
    return {
        "slaves": {
            "d464cc58a0cd46dea3191ba70f4e7df8": {
                "name": "slave_test",
                "address": "",
                "description": "...",
                "extra": {
                    "description": "...",
                    "starttime": 1543851265.76279,
                    "port": 10000,
                    "server_ip": "127.0.0.1",
                    "status": "up",
                    "api_key": "e58a882a6b658a22660f00a0c273e7f6b4c4eb5abe54eccba2cae307905d67e374"
                               "6537bd790c41887e11840c2d186b6d6eeec0e426bcfa7a872cc3417a35124a"
                }
            }
        }
    }


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    with requests_mock.Mocker(real_http=True) as m:
        try:
            os.remove("/tmp/database_test.db")
        except FileNotFoundError:
            pass
        try:
            os.remove("/tmp/moon.pwd")
        except FileNotFoundError:
            pass
        print("Configure...")
        from moon_manager.api.configuration import init_database, set_configuration
        set_configuration(yaml.safe_load(__CONF))
        print("Create a new user")
        from moon_utilities.auth_functions import add_user, init_db, get_api_key_for_user
        init_db()
        # try:
        #     user = add_user("admin", "admin")
        #     manager_api_key = user["api_key"]
        # except KeyError:
        #     print("User already exists")
        #     manager_api_key = get_api_key_for_user("admin")
        print("Initialize the database")
        init_database()
        from moon_manager import db_driver
        db_driver.init()

        mock_slaves.register_slaves(m)

        print("End registering URI")

        # from moon_manager.pip_driver import InformationManager
        # InformationManager.set_auth()

        yield m

        # InformationManager.unset_auth()
