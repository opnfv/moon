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
from python_moonutilities.security_functions import check_auth

from python_moonutilities import configuration
from python_moonutilities.security_functions import validate_input


__version__ = "4.3.0"

logger = logging.getLogger("moon.manager.api." + __name__)


class Slaves(Resource):
    """
    Endpoint for pdp requests
    """

    __urls__ = (
        "/slaves",
        "/slaves/",
        "/slaves/<string:uuid>",
        "/slaves/<string:uuid>/",
    )

    def __init__(self, **kwargs):
        conf = configuration.get_configuration("components/orchestrator")
        self.orchestrator_hostname = conf["components/orchestrator"].get("hostname",
                                                                         "orchestrator")
        self.orchestrator_port = conf["components/orchestrator"].get("port",
                                                                     80)

    @validate_input("get", kwargs_state=[False, False])
    @check_auth
    def get(self, uuid=None, user_id=None):
        """Retrieve all slaves

        :param uuid: uuid of the slave
        :param user_id: user ID who do the request
        :return: {
            "slaves": {
                "XXX": {
                    "name": "...",
                    "installed": True
                },
                "YYY": {
                    "name": "...",
                    "installed": False
                }
            }
        }
        """
        req = requests.get("http://{}:{}/slaves".format(
            self.orchestrator_hostname, self.orchestrator_port
        ))
        return {"slaves": req.json().get("slaves", dict())}

    @validate_input("patch", kwargs_state=[False, False],
                    body_state={"op": True, "variable": True, "value": True})
    @check_auth
    def patch(self, uuid=None, user_id=None):
        """Update a slave

        :param uuid: uuid of the slave to update
        :param user_id: user ID who do the request
        :request body: {
            "op": "replace",
            "variable": "configured",
            "value": True,
        }
        :return: 204
        :internal_api: add_pdp
        """
        logger.info("Will made a request for {}".format(uuid))
        if request.json.get("op") == "replace" \
            and request.json.get("variable") == "configured" \
                and request.json.get("value"):
            req = requests.post("http://{}:{}/pods".format(
                self.orchestrator_hostname, self.orchestrator_port,
                ),
                json={"slave_name": uuid}
            )
            if req.status_code != 200:
                logger.warning("Get error from Orchestrator {} {}".format(
                    req.reason, req.status_code
                ))
                return "Orchestrator: " + str(req.reason), req.status_code
        elif request.json.get("op") == "replace" \
            and request.json.get("variable") == "configured" \
                and not request.json.get("value"):
            req = requests.delete("http://{}:{}/pods/{}".format(
                self.orchestrator_hostname, self.orchestrator_port, uuid
            ))
            if req.status_code != 200:
                logger.warning("Get error from Orchestrator {} {}".format(
                    req.reason, req.status_code
                ))
                return "Orchestrator: " + str(req.reason), req.status_code
        else:
            return "Malformed request", 400
        return {"slaves": req.json()}
