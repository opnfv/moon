# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Authz is the endpoint to get authorization response
"""

from uuid import uuid4
import time
from flask_restful import Resource
from oslo_log import log as logging
from moon_utilities.security_functions import call

__version__ = "0.1.0"

LOG = logging.getLogger("moon.interface.api." + __name__)


class Authz(Resource):
    """
    Endpoint for authz requests
    """

    __urls__ = ("/authz/<string:uuid>/<string:subject_name>/<string:object_name>/<string:action_name>", )

    def get(self, uuid=None, subject_name=None, object_name=None, action_name=None):
        """Get a response on an authorization request

        :param uuid: uuid of a tenant or an intra_extension
        :param subject_name: name of the subject or the request
        :param object_name: name of the object
        :param action_name: name of the action
        :return: {
            "args": {},
            "ctx": {
                "action_name": "4567",
                "id": "123456",
                "method": "authz",
                "object_name": "234567",
                "subject_name": "123456",
                "user_id": "admin"
            },
            "error": {
                "code": 500,
                "description": "",
                "title": "Moon Error"
            },
            "intra_extension_id": "123456",
            "result": false
        }
        :internal_api: authz
        """
        # Note (asteroide): user_id default to admin to be able to read the database
        # it would be better to have a read-only user.
        start_time = time.time()
        result = call("security_router", ctx={"id": uuid,
                         "call_master": False,
                         "method": "authz",
                         "subject_name": subject_name,
                         "object_name": object_name,
                         "action_name": action_name,
                         "user_id": "admin",
                         "request_id": uuid4().hex}, args={})
        end_time = time.time()
        result['time'] = {"start": start_time, "end": end_time}
        return result
