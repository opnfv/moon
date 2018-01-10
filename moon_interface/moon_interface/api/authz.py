# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Authz is the endpoint to get authorization response
"""

from flask import request
from flask_restful import Resource
import logging
import pickle
import time
from uuid import uuid4
from python_moonutilities import exceptions

from moon_interface.authz_requests import AuthzRequest

__version__ = "4.3.1"

logger = logging.getLogger("moon.interface.api.authz." + __name__)


def get_pdp_from_cache(cache, uuid):
    """Check if a PDP exist with this ID in the cache of this component

    :param cache: Cache to use
    :param uuid: Keystone Project ID
    :return: True or False
    """
    if uuid in cache.pdp:
        return cache.pdp.get(uuid)

    cache.update()

    if uuid in cache.pdp:
        return cache.pdp.get(uuid)

    raise exceptions.PdpUnknown


def create_authz_request(cache, interface_name, manager_url, pdp_id, subject_name, object_name, action_name):
    """Create the authorization request and make the first call to the Authz function

    :param cache: Cache to use
    :param interface_name: hostname of the interface
    :param manager_url: URL of the manager
    :param pdp_id: Keystone Project ID
    :param subject_name: name of the subject
    :param object_name: name of the object
    :param action_name: name of the action
    :return: Authorisation request
    """
    req_id = uuid4().hex
    keystone_project_id = cache.get_keystone_project_id_from_pdp_id(pdp_id)
    logger.info("keystone_project_id={}".format(keystone_project_id))
    ctx = {
        "project_id": keystone_project_id,
        "subject_name": subject_name,
        "object_name": object_name,
        "action_name": action_name,
        "request_id": req_id,
        "interface_name": interface_name,
        "manager_url": manager_url,
        "cookie": uuid4().hex
    }
    cache.authz_requests[req_id] = AuthzRequest(ctx)
    return cache.authz_requests[req_id]


def delete_authz_request(cache, req_id):
    cache.authz_requests.pop(req_id)


class Authz(Resource):
    """
    Endpoint for authz requests
    """

    __urls__ = (
        "/authz/<string:pdp_id>",
        "/authz/<string:pdp_id>/<string:subject_name>/<string:object_name>/<string:action_name>",
    )

    def __init__(self, **kwargs):
        self.CACHE = kwargs.get("cache")
        self.INTERFACE_NAME = kwargs.get("interface_name", "interface")
        self.MANAGER_URL = kwargs.get("manager_url", "http://manager:8080")
        self.TIMEOUT = 5

    def get(self, pdp_id, subject_name=None, object_name=None, action_name=None):
        """Get a response on an authorization request

        :param pdp_id: uuid of a tenant or an intra_extension
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
        try:
            get_pdp_from_cache(self.CACHE, pdp_id)
        except exceptions.PdpUnknown:
            return {
                   "result": False,
                   "message": "Unknown PDP ID."}, 403

        authz_request = create_authz_request(
            cache=self.CACHE,
            pdp_id=pdp_id,
            interface_name=self.INTERFACE_NAME,
            manager_url=self.MANAGER_URL,
            subject_name=subject_name,
            object_name=object_name,
            action_name=action_name)
        cpt = 0
        while True:
            if cpt > self.TIMEOUT*10:
                delete_authz_request(self.CACHE, authz_request.request_id)
                return {"result": False,
                        "message": "Authz request had timed out."}, 500
            if authz_request.is_authz():
                if authz_request.final_result == "Grant":
                    delete_authz_request(self.CACHE, authz_request.request_id)
                    return {"result": True, "message": ""}, 200
                delete_authz_request(self.CACHE, authz_request.request_id)
                return {"result": False, "message": ""}, 401
            cpt += 1
            time.sleep(0.1)

    def patch(self, uuid=None, subject_name=None, object_name=None, action_name=None):
        """Get a response on an authorization request

        :param uuid: uuid of the authorization request
        :param subject_name: not used
        :param object_name: not used
        :param action_name: not used
        :request body: a Context object
        :return: {}
        :internal_api: authz
        """
        if uuid in self.CACHE.authz_requests:
            self.CACHE.authz_requests[uuid].set_result(pickle.loads(request.data))
            return "", 201
        return {"result": False, "message": "The request ID is unknown"}, 500
