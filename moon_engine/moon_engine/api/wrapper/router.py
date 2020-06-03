# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from moon_utilities import exceptions
from moon_cache.cache import Cache
from uuid import uuid4
import logging
import requests
from moon_engine.api.configuration import get_configuration

LOGGER = logging.getLogger("moon.engine.wrapper." + __name__)


class Router(object):
    __CACHE = None

    def __init__(self, project_id, subject_name, object_name, action_name):

        if not self.__CACHE:
            self.__CACHE = Cache.getInstance(manager_url=get_configuration("manager_url"),
                                             incremental=get_configuration("incremental_updates"),
                                             manager_api_key=get_configuration("api_token"))

        self.pipeline_id = self.__check_pdp_from_cache(project_id)

        self.request_id = uuid4().hex

        self.ctx = {
            "project_id": project_id,
            "subject_name": subject_name,
            "object_name": object_name,
            "action_name": action_name
        }

        # ToDo add status of request
        self.__CACHE.authz_requests[self.request_id] = {}

        pdp_id = self.__CACHE.get_pdp_from_vim_project(project_id)
        self.__CACHE.update(pipeline=pdp_id)
        self.pipeline = []
        if self.pipeline_id in self.__CACHE.pipelines:
            self.pipeline = self.__CACHE.pipelines[self.pipeline_id]

        if len(self.pipeline) == 0 or not all(
                k in self.pipeline for k in ("host", "port")):
            raise exceptions.MoonError('Void container chaining')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__CACHE.authz_requests.pop(self.request_id)

    def auth_request(self):
        req = None
        endpoint = self.__CACHE.get_pipeline_url(self.ctx["project_id"])

        try:
            req = requests.get("{}/authz/{}/{}/{}".format(
                endpoint,
                self.ctx["subject_name"],
                self.ctx["object_name"],
                self.ctx["action_name"]),
                timeout=2
            )

            if req.status_code != 200 and req.status_code != 202 and req.status_code != 204:
                raise exceptions.AuthzException(
                    "Receive bad response from Authz function (with address - {})"
                        .format(req.status_code))

        except requests.exceptions.ConnectionError:
            LOGGER.error("Cannot connect to {}".format(
                "{}/authz".format(endpoint))
            )
        except requests.exceptions.ReadTimeout:
            LOGGER.error("Timeout error")
            return {"result": False, "message": "Timeout during request for pipeline"}, 400
        except Exception as e:
            LOGGER.error("Unexpected error:", e)
            return {"result": False, "message": e}, 400

        if not req:
            raise exceptions.AuthzException("Cannot connect to Authz function")

        if req.status_code == 204:
            return {"result": True, "message": ""}
        return {"result": False, "message": req.content}, 400

    def __check_pdp_from_cache(self, uuid):
        """Check if a PDP exist with this ID in the cache of this component

        :param uuid: Keystone Project ID
        :return: True or False
        """

        if self.__CACHE.get_pdp_from_vim_project(uuid):
            return self.__CACHE.get_pipeline_id_from_project_id(uuid)

        self.__CACHE.update()

        if self.__CACHE.get_pdp_from_vim_project(uuid):
            return self.__CACHE.get_pipeline_id_from_project_id(uuid)

        raise exceptions.MoonError("Unknown Project ID {}".format(uuid))

