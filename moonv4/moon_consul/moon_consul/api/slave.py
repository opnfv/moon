# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Assignments allow to connect data with elements of perimeter

"""

from flask import request
from flask_restful import Resource
# from oslo_config import cfg
from oslo_log import log as logging
# from moon_interface.tools import check_auth

__version__ = "0.1.0"

LOG = logging.getLogger(__name__)
# CONF = cfg.CONF


class Slave(Resource):
    """
    Endpoint for slave requests
    """

    __urls__ = (
        "/configuration/slave",
    )

    def __init__(self, *args, **kwargs):
        self.conf = kwargs.get('conf', {})

    # @check_auth
    def get(self):
        """Retrieve slave configuration

        If current server is a slave:
        :return: {
            "slave": {
                "name": "name of the slave",
                "master_url": "URL of the master",
                "user": [ 
                    {
                        "username": "user to be used to connect to the master",
                        "password": "password to be used to connect to the master"
                    }
                ]
            }
        }
        else:
        :return: {
            "slave": {}
        }
        """
        # TODO: password must be encrypted
        if self.conf.SLAVE_NAME:
            return {
                "slave": {
                    "name": self.conf.SLAVE_NAME,
                    "master_url": self.conf.MASTER_URL,
                    "user": [
                        {
                            "username": self.conf.MASTER_LOGIN,
                            "password": self.conf.MASTER_PASSWORD
                        }
                    ]
                }
            }
        else:
            return {"slave": {}}

