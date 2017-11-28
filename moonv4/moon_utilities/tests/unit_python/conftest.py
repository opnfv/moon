import base64
import json
import logging
import pytest
import requests_mock

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

COMPONENTS = (
    "logging",
    "openstack/keystone",
    "database",
    "slave",
    "components/manager",
)


def get_b64_conf(component=None):
    if component in CONF:
        return base64.b64encode(
            json.dumps(
                CONF[component]).encode('utf-8')+b"\n").decode('utf-8')
    elif component == "components":
        return base64.b64encode(
            json.dumps(CONF["components"]).encode('utf-8')+b"\n").decode('utf-8')
    elif not component:
        return base64.b64encode(
            json.dumps(CONF).encode('utf-8')+b"\n").decode('utf-8')
    elif "/" in component:
        key1, _, key2 = component.partition("/")
        return base64.b64encode(
            json.dumps(
                CONF[key1][key2]).encode('utf-8')+b"\n").decode('utf-8')


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    with requests_mock.Mocker(real_http=True) as m:
        for component in COMPONENTS:
            m.register_uri(
                'GET', 'http://consul:8500/v1/kv/{}'.format(component),
                json=[{'Key': component, 'Value': get_b64_conf(component)}]
                )
        m.register_uri(
            'GET', 'http://consul:8500/v1/kv/components?recurse=true',
            json=[{'Key': "components", 'Value': get_b64_conf("components")}]
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
        print("End registering URI")
        # from moon_db.db_manager import init_engine, run
        # engine = init_engine()
        # print("engine={}".format(engine))
        # run("upgrade", logging.getLogger("db_manager"), engine)
        # print("End populating the DB.")
        yield m


# @pytest.fixture(autouse=True, scope="session")
# def manage_database():
#     from moon_db.db_manager import init_engine, run
#     engine = init_engine()
#     run("upgrade", logging.getLogger("db_manager"), engine)
#     yield
#     print("Will close the DB")


