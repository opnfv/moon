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
from python_moonutilities.security_functions import check_auth
from python_moondb.core import PDPManager
from python_moondb.core import PolicyManager
from python_moondb.core import ModelManager
from python_moonutilities import configuration, exceptions

__version__ = "4.3.2"

logger = logging.getLogger("moon.manager.api." + __name__)


def delete_pod(uuid):
    conf = configuration.get_configuration("components/orchestrator")
    hostname = conf["components/orchestrator"].get("hostname", "orchestrator")
    port = conf["components/orchestrator"].get("port", 80)
    proto = conf["components/orchestrator"].get("protocol", "http")
    # while True:
    #     try:
    url = "{}://{}:{}/pods".format(proto, hostname, port)
    req = requests.get(url)
    # except requests.exceptions.ConnectionError:
    #     logger.warning("Orchestrator is not ready, standby... {}".format(url))
    #     time.sleep(1)
    # else:
    #     break
    for pod_key, pod_list in req.json().get("pods", {}).items():
        for pod_value in pod_list:
            if "pdp_id" in pod_value:
                if pod_value["pdp_id"] == uuid:
                    req = requests.delete("{}://{}:{}/pods/{}".format(proto, hostname, port, pod_key))
                    if req.status_code != 200:
                        logger.warning("Cannot delete pod {} - {}".format(pod_key, pod_value['name']))
                        logger.debug(req.content)
                    # Note (Asteroide): no need to go further if one match
                    break


def add_pod(uuid, data):
    if not data.get("keystone_project_id"):
        return
    logger.info("Add a new pod {}".format(data))
    if "pdp_id" not in data:
        data["pdp_id"] = uuid
    data['policies'] = PolicyManager.get_policies(user_id="admin")
    data['models'] = ModelManager.get_models(user_id="admin")
    conf = configuration.get_configuration("components/orchestrator")
    hostname = conf["components/orchestrator"].get("hostname", "orchestrator")
    port = conf["components/orchestrator"].get("port", 80)
    proto = conf["components/orchestrator"].get("protocol", "http")
    while True:
        try:
            req = requests.post(
                "{}://{}:{}/pods".format(proto, hostname, port),
                json=data,
                headers={"content-type": "application/json"})
        except requests.exceptions.ConnectionError as e:
            logger.warning("add_pod: Orchestrator is not ready, standby...")
            logger.exception(e)
            time.sleep(1)
        else:
            break
    logger.info("Pod add request answer : {}".format(req.text))


def check_keystone_pid(k_pid):
    data = PDPManager.get_pdp(user_id="admin")
    for pdp_key, pdp_value in data.items():
        logger.info("pdp={}".format(pdp_value))
        if pdp_value["keystone_project_id"] == k_pid:
            return True


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
                "description": "... (optional)",
            }
        }
        :internal_api: get_pdp
        """
        try:
            data = PDPManager.get_pdp(user_id=user_id, pdp_id=uuid)
        except Exception as e:
            logger.error(e, exc_info=True)
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
            "description": "... (optional)",
        }
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "keystone_project_id": "keystone_project_id1",
                "description": "... (optional)",
            }
        }
        :internal_api: add_pdp
        """
        try:
            data = dict(request.json)
            if not data.get("keystone_project_id"):
                data["keystone_project_id"] = None
            else:
                if check_keystone_pid(data.get("keystone_project_id")):
                    raise exceptions.PdpKeystoneMappingConflict
            data = PDPManager.add_pdp(
                user_id=user_id, pdp_id=None, value=request.json)
            uuid = list(data.keys())[0]
            logger.debug("data={}".format(data))
            logger.debug("uuid={}".format(uuid))
            add_pod(uuid=uuid, data=data[uuid])
        except Exception as e:
            logger.error(e, exc_info=True)
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
            "message": "optional message (optional)"
        }
        :internal_api: delete_pdp
        """
        try:
            data = PDPManager.delete_pdp(user_id=user_id, pdp_id=uuid)
            delete_pod(uuid)
        except Exception as e:
            logger.error(e, exc_info=True)
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
                "description": "... (optional)",
            }
        }
        :internal_api: update_pdp
        """
        try:
            _data = dict(request.json)
            if not _data.get("keystone_project_id"):
                _data["keystone_project_id"] = None
            else:
                if check_keystone_pid(_data.get("keystone_project_id")):
                    raise exceptions.PdpKeystoneMappingConflict
            data = PDPManager.update_pdp(
                user_id=user_id, pdp_id=uuid, value=_data)
            logger.debug("data={}".format(data))
            logger.debug("uuid={}".format(uuid))
            add_pod(uuid=uuid, data=data[uuid])
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e)}, 500
        return {"pdps": data}

