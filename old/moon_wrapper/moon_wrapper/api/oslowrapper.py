# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Authz is the endpoint to get authorization response
"""

import logging
import json
import flask
from flask import request
from flask_restful import Resource
import requests
from python_moonutilities import exceptions

__version__ = "0.1.0"

LOGGER = logging.getLogger("moon.wrapper.api." + __name__)


class OsloWrapper(Resource):
    """
    Endpoint for authz requests
    """

    __urls__ = (
        "/authz/oslo",
        "/authz/oslo/",
    )

    def __init__(self, **kwargs):
        self.port = kwargs.get("port")
        self.CACHE = kwargs.get("cache", {})
        self.TIMEOUT = 5

    def post(self):
        LOGGER.debug("POST {}".format(request.form))
        response = flask.make_response("False")
        try:
            if self.manage_data():
                response = flask.make_response("True")
        except exceptions.AuthzException as exception:
            LOGGER.error(exception, exc_info=True)
        except Exception as exception:
            LOGGER.error(exception, exc_info=True)

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
        return "none"

    @staticmethod
    def __get_project_id(target, credentials):
        project_id = target.get("project_id", None)
        if not project_id:
            project_id = credentials.get("project_id", None)
        return project_id

    def get_interface_url(self, project_id):
        LOGGER.debug("project_id {}".format(project_id))
        for containers in self.CACHE.containers.values():
            LOGGER.info("containers {}".format(containers))
            for container in containers:
                if container.get("keystone_project_id") == project_id:
                    if "pipeline" in container['name']:
                        return "http://{}:{}".format(
                            container['name'],
                            container['port'])
        self.CACHE.update()
        # Note (asteroide): test an other time after the update
        for containers in self.CACHE.containers.values():
            for container in containers:
                if container.get("keystone_project_id") == project_id:
                    if "pipeline" in container['name']:
                        return "http://{}:{}".format(
                            container['name'],
                            container['port'])
        raise exceptions.AuthzException("Keystone Project "
                                        "ID ({}) is unknown or not mapped "
                                        "to a PDP.".format(project_id))

    def manage_data(self):
        data = request.form
        if not dict(request.form):
            data = json.loads(request.data.decode("utf-8"))
        target = json.loads(data.get('target', {}))
        credentials = json.loads(data.get('credentials', {}))
        rule = data.get('rule', "").strip('"').strip("'")
        _subject = self.__get_subject(target, credentials)
        _object = self.__get_object(target, credentials)
        _action = rule
        LOGGER.info("authz {} {} {}".format(_subject, _object, _action))
        _project_id = self.__get_project_id(target, credentials)
        _pdp_id = self.CACHE.get_pdp_from_keystone_project(_project_id)
        interface_url = self.get_interface_url(_project_id)
        LOGGER.debug("interface_url={}".format(interface_url))
        req = requests.get("{}/authz/{}/{}/{}/{}".format(
            interface_url,
            _pdp_id,
            _subject,
            _object,
            _action
        ))

        LOGGER.debug("Get interface {}".format(req.text))
        if req.status_code == 200:
            if req.json().get("result", False):
                return True

        raise exceptions.AuthzException("error in authz request")
