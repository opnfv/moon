# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Authz is the endpoint to get authorization response
"""

import flask
from flask import request
from flask_restful import Resource
import logging
import json
import requests
import time
from uuid import uuid4

from moon_interface.api.authz import pdp_in_cache, pdp_in_manager, container_exist, \
    create_containers, create_authz_request
from moon_interface.authz_requests import AuthzRequest
from moon_utilities import configuration

__version__ = "0.1.0"

LOG = logging.getLogger("moon.wrapper.api." + __name__)


class Wrapper(Resource):
    """
    Endpoint for authz requests
    """

    __urls__ = (
        "/",
    )

    def __init__(self, **kwargs):
        self.port = kwargs.get("port")
        self.CACHE = kwargs.get("cache", {})
        self.TIMEOUT = 5

    # def get(self):
    #     LOG.info("GET")
    #     return self.manage_data()

    def post(self):
        LOG.info("POST {}".format(request.form))
        response = flask.make_response("False")
        if self.manage_data():
            response = flask.make_response("True")
        response.headers['content-type'] = 'application/octet-stream'
        return response

    @staticmethod
    def __get_subject(target, credentials):
        _subject = target.get("user_id", "")
        if not _subject:
            _subject = credentials.get("user_id", "none")
        return _subject

    @staticmethod
    def __get_object(target, credentials):
        try:
            # note: case of Glance
            return target['target']['name']
        except KeyError:
            pass

        # note: default case
        return target.get("project_id", "none")

    @staticmethod
    def __get_project_id(target, credentials):
        return target.get("project_id", "none")

    def get_interface_url(self, project_id):
        for container in self.CACHE.containers.values():
            if container.get("keystone_project_id") == project_id:
                return "http://{}:{}".format(container['hostname'],
                                             container['port'][0]["PublicPort"])

    def manage_data(self):
        target = json.loads(request.form.get('target', {}))
        credentials = json.loads(request.form.get('credentials', {}))
        rule = request.form.get('rule', "")
        _subject = self.__get_subject(target, credentials)
        _object = self.__get_object(target, credentials)
        _project_id = self.__get_project_id(target, credentials)
        LOG.info("POST with args project={} / "
                 "subject={} - object={} - action={}".format(
                    _project_id, _subject, _object, rule))
        interface_url = self.get_interface_url(_project_id)
        req = requests.get("{}/{}/{}/{}".format(
            interface_url,
            _subject,
            _object,
            rule
        ))
        if req.status_code == 200:
            if req.json().get("result", False):
                return True
