import base64
import json


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
        "pipeline": {
            "interface": {
                "bind": "0.0.0.0",
                "port": 8080,
                "container": "wukongsun/moon_interface:v4.3",
                "hostname": "interface"
            },
            "authz": {
                "bind": "0.0.0.0",
                "port": 8081,
                "container": "wukongsun/moon_authz:v4.3",
                "hostname": "authz"
            },
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
    else:
        return base64.b64encode(component.encode('utf-8')+b"\n").decode('utf-8')
