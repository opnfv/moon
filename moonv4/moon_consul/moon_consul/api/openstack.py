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


class Keystone(Resource):
    """
    Endpoint for Keystone requests
    """

    __urls__ = (
        "/configuration/os/keystone",
    )

    def __init__(self, *args, **kwargs):
        self.conf = kwargs.get('conf', {})

    # @check_auth
    def get(self):
        """Retrieve Keystone configuration

        :return: {
            "keystone": {
                "url": "hostname for the Keystone server",
                "user": "user for the Keystone server",
                "password": "password for the Keystone server",
                "domain": "domain to use against Keystone server",
                "project": "main project to use",
                "check_token": "yes, no or strict",
                "server_crt": "certificate to use when using https"
            }
        }
        """
        # TODO: password must be encrypted
        # TODO: check_token is a sensitive information it must not be update through the network
        return {
            "keystone": {
                "url": self.conf.KEYSTONE_URL,
                "user": self.conf.KEYSTONE_USER,
                "password": self.conf.KEYSTONE_PASSWORD,
                "domain": self.conf.KEYSTONE_DOMAIN,
                "project": self.conf.KEYSTONE_PROJECT,
                "check_token": self.conf.KEYSTONE_CHECK_TOKEN,
                "server_crt": self.conf.KEYSTONE_SERVER_CRT
            }
        }

