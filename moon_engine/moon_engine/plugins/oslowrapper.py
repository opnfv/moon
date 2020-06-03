# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""
Authz is the endpoint to get authorization response
"""

import logging
import json
import hug
import requests
from moon_utilities import exceptions
from moon_cache.cache import Cache
from moon_engine.api.configuration import get_configuration

PLUGIN_TYPE = "wrapper_api"
LOGGER = logging.getLogger("moon.wrapper.api." + __name__)


class OsloWrapper(object):
    """
    Endpoint for authz requests
    """

    def __init__(self, **kwargs):
        self.TIMEOUT = 5

    @staticmethod
    @hug.local()
    @hug.post("/authz/oslo", output=hug.output_format.text)
    def post(body, response):
        LOGGER.debug("POST {}".format(body))
        response.status = hug.HTTP_400
        response_data = "False"
        response.set_header('content-type', 'application/octet-stream')
        try:
            oslo_wrapper_checker = OsloWrapperChecker()
            if oslo_wrapper_checker.manage_data(body):
                response.status = hug.HTTP_200
                response_data = "True"
        except exceptions.AuthzException as exception:
            LOGGER.error(exception, exc_info=True)
        except Exception as exception:
            LOGGER.error(exception, exc_info=True)

        return response_data


class OsloWrapperChecker(object):

    def __init__(self):
        self.CACHE = Cache.getInstance()

    @staticmethod
    def __get_subject(target, credentials):
        # FIXME: we should use the ID instead of the name
        _subject = target.get("target.user.name", "")
        if not _subject and credentials:
            _subject = credentials.get("token", {}).get("user", {}).get(
                "name",
                credentials.get("user_id", "none"))
        if not _subject:
            _subject = target.get("user_id", "")
        return _subject

    @staticmethod
    def __get_object(target, credentials):
        try:
            # note: case of Glance
            return target['target']['name']
        except KeyError:
            pass

        # note: default case
        return "all"

    @staticmethod
    def __get_project_id(target, credentials):
        project_id = credentials.get("project_id")
        LOGGER.info("project_id {}".format(project_id))
        return project_id

    def manage_data(self, body):
        data = body
        if not dict(body):
            data = json.loads(body.decode("utf-8"))
        try:
            target = json.loads(data.get('target', {}))
        except TypeError:
            target = data.get('target', {})
        try:
            credentials = json.loads(data.get('credentials', {}))
        except TypeError:
            credentials = data.get('credentials', {})
        rule = data.get('rule', "")
        _subject = self.__get_subject(target, credentials)
        _object = self.__get_object(target, credentials)
        _action = rule.strip('"')
        _project_id = self.__get_project_id(target, credentials)

        host_url = self.CACHE.get_pipeline_url(project_id=_project_id)
        if not host_url:
            if get_configuration("grant_if_unknown_project"):
                LOGGER.info("No interface found for {}, "
                            "granted anyway : grant_if_unknown_project is true in the conf file".format(_project_id))
                return True
            LOGGER.error("No interface found for {}".format(_project_id))
        else:
            LOGGER.debug("interface_url={}".format(host_url))
            _url = "{}/authz/{}/{}/{}".format(
                host_url,
                _subject,
                _object,
                _action
            )
            LOGGER.debug("url={}".format(_url))
            req = requests.get(_url, timeout=2)

            if req.status_code == 204:
                LOGGER.info("The request has been granted")
                return True
            LOGGER.debug("authz request: {} {}".format(req.status_code, req.content))
        raise exceptions.AuthzException("error in authz request")


def get_apis():
    yield OsloWrapper

