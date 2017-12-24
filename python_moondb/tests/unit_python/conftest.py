import base64
import json
import logging
import os
import pytest
import requests_mock
import mock_components
import mock_keystone

CONF = {
    "openstack": {
        "keystone": {
            "url": "http://keystone:5000/v3",
            "user": "admin",
            "check_token": False,
            "password": "p4ssw0rd",
            "domain": "default",
            "certificate": False,
            "project": "admin"
        }
    },
    "components": {
        "wrapper": {
            "bind": "0.0.0.0",
            "port": 8080,
            "container": "wukongsun/moon_wrapper:v4.3",
            "timeout": 5,
            "hostname": "wrapper"
        },
        "manager": {
            "bind": "0.0.0.0",
            "port": 8082,
            "container": "wukongsun/moon_manager:v4.3",
            "hostname": "manager"
        },
        "port_start": 31001,
        "orchestrator": {
            "bind": "0.0.0.0",
            "port": 8083,
            "container": "wukongsun/moon_orchestrator:v4.3",
            "hostname": "interface"
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
                "filename": "/tmp/moon.log",
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
            "password": None
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


@pytest.fixture
def db():
    return CONF['database']


@pytest.fixture(autouse=True)
def set_consul_and_db(monkeypatch):
    """ Modify the response from Requests module
    """
    with requests_mock.Mocker(real_http=True) as m:
        mock_components.register_components(m)
        mock_keystone.register_keystone(m)

        from python_moondb.db_manager import init_engine, main
        engine = init_engine()
        main("upgrade", logging.getLogger("db_manager"), engine)
        yield m
        os.unlink(CONF['database']['url'].replace("sqlite:///", ""))


