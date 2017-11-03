# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
PDP are Policy Decision Point.

"""

from flask import request
from flask_restful import Resource
import logging
import requests
import time
from moon_utilities.security_functions import check_auth
from moon_db.core import PDPManager
from moon_utilities import configuration

__version__ = "0.1.0"

LOG = logging.getLogger("moon.manager.api." + __name__)


def delete_pod(uuid):
    raise NotImplementedError


def add_pod(uuid, data):
    LOG.info("Add a new pod {}".format(data))
    conf = configuration.get_configuration("components/orchestrator")
    hostname = conf["components/orchestrator"].get("hostname", "orchestrator")
    port = conf["components/orchestrator"].get("port", 80)
    proto = conf["components/orchestrator"].get("protocol", "http")
    while True:
        try:
            req = requests.post("{}://{}:{}/pods".format(proto, hostname, port),
                                data=data)
        except requests.exceptions.ConnectionError:
            LOG.warning("Orchestrator is not ready, standby...")
            time.sleep(1)
        else:
            break
    LOG.info(req.text)


class PDP(Resource):
    """
    Endpoint for pdp requests
    """

    __urls__ = (
        "/pdp",
        "/pdp/",
        "/pdp/<string:uuid>",
        "/pdp/<string:uuid>/",
    )

    @check_auth
    def get(self, uuid=None, user_id=None):
        """Retrieve all pdp

        :param uuid: uuid of the pdp
        :param user_id: user ID who do the request
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "keystone_project_id": "keystone_project_id1",
                "description": "...",
            }
        }
        :internal_api: get_pdp
        """
        try:
            data = PDPManager.get_pdp(user_id=user_id, pdp_id=uuid)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"pdps": data}

    @check_auth
    def post(self, uuid=None, user_id=None):
        """Create pdp.

        :param uuid: uuid of the pdp (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "name": "...",
            "security_pipeline": [...],
            "keystone_project_id": "keystone_project_id1",
            "description": "...",
        }
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "keystone_project_id": "keystone_project_id1",
                "description": "...",
            }
        }
        :internal_api: add_pdp
        """
        try:
            data = dict(request.json)
            if not data.get("keystone_project_id"):
                data["keystone_project_id"] = None
            data = PDPManager.add_pdp(
                user_id=user_id, pdp_id=None, value=request.json)
            uuid = list(data.keys())[0]
            LOG.info("data={}".format(data))
            LOG.info("uuid={}".format(uuid))
            add_pod(uuid=uuid, data=data[uuid])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"pdps": data}

    @check_auth
    def delete(self, uuid=None, user_id=None):
        """Delete a pdp

        :param uuid: uuid of the pdp to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        :internal_api: delete_pdp
        """
        try:
            data = PDPManager.delete_pdp(user_id=user_id, pdp_id=uuid)
            delete_pod(uuid)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"result": True}

    @check_auth
    def patch(self, uuid=None, user_id=None):
        """Update a pdp

        :param uuid: uuid of the pdp to update
        :param user_id: user ID who do the request
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "keystone_project_id": "keystone_project_id1",
                "description": "...",
            }
        }
        :internal_api: update_pdp
        """
        try:
            _data = dict(request.json)
            if not _data.get("keystone_project_id"):
                _data["keystone_project_id"] = None
            data = PDPManager.update_pdp(
                user_id=user_id, pdp_id=uuid, value=_data)
            LOG.info("data={}".format(data))
            LOG.info("uuid={}".format(uuid))
            add_pod(uuid=uuid, data=data[uuid])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"pdps": data}

