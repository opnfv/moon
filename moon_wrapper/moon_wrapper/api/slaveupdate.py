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


class SlaveUpdate(Resource):
    """
    Endpoint for authz requests
    """

    __urls__ = (
        "/update",
        "/update/",
    )

    def __init__(self, **kwargs):
        self.port = kwargs.get("port")
        self.CACHE = kwargs.get("cache", {})
        self.TIMEOUT = 5

    def put(self):
        LOGGER.warning("PUT {}".format(request.form))
        response = flask.make_response("False")
        try:
            if self.update_slave():
                response = flask.make_response("True")
        except Exception as exception:
            LOGGER.error(exception, exc_info=True)

        response.headers['content-type'] = 'application/octet-stream'
        return response

    def get_interface_url(self, pdp_id):
        LOGGER.debug("pdp_id {}".format(pdp_id))
        for containers in self.CACHE.containers.values():
            LOGGER.info("containers0 {}".format(containers))
            for container in containers:
                if container.get("pdp_id") == pdp_id:
                    if "pipeline" in container['name']:
                        yield "http://{}:{}".format(
                            container['name'],
                            container['port'])
        self.CACHE.update()
        # Note (asteroide): test an other time after the update
        for containers in self.CACHE.containers.values():
            LOGGER.info("containers1 {}".format(containers))
            for container in containers:
                if container.get("pdp_id") == pdp_id:
                    if "pipeline" in container['name']:
                        yield "http://{}:{}".format(
                            container['name'],
                            container['port'])

    def update_slave(self):
        result = {}
        result_list = []
        for _pdp_id in self.CACHE.pdp:
            result[_pdp_id] = {}
            for interface_url in self.get_interface_url(_pdp_id):

                req = requests.put("{}/update".format(interface_url), request.form)

                if req.status_code == 200:
                    if req.json().get("result", False):
                        result[_pdp_id][interface_url] = True
                        result_list.append(True)
                        continue
                LOGGER.warning("Error in {} {}: {}".format(_pdp_id, interface_url, req.text))
                result[_pdp_id][interface_url] = False
            result_list.append(False)
        return all(result_list)
