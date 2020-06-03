# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from flask import request
from flask_restful import Resource
from python_moonutilities.security_functions import check_auth
from python_moonutilities import exceptions
import logging

logger = logging.getLogger("moon.orchestrator.api.pods")


class Pods(Resource):
    """
    Endpoint for pdp requests
    """

    __version__ = "4.3.1"
    POD_TYPES = ("authz", "wrapper")

    __urls__ = (
        "/pods",
        "/pods/",
        "/pods/<string:uuid>",
        "/pods/<string:uuid>/",
    )

    def __init__(self, **kwargs):
        self.driver = kwargs.get("driver")

    @check_auth
    def get(self, uuid=None, user_id=None):
        """Retrieve all pods

        :param uuid: uuid of the pod
        :param user_id: user ID who do the request
        :return: {
            "pod_id1": {
                "name": "...",
                "replicas": "...",
                "description": "...",
            }
        }
        :internal_api: get_pdp
        """
        pods = {}
        try:
            if uuid:
                return {"pods": self.driver.get_pods(uuid)}
            for _pod_key, _pod_values in self.driver.get_pods().items():
                pods[_pod_key] = []
                for _pod_value in _pod_values:
                    if "namespace" in _pod_value and _pod_value['namespace'] != "moon":
                        continue
                    pods[_pod_key].append(_pod_value)
            return {"pods": pods}
        except Exception as e:
            return {"result": False, "message": str(e)}, 500

    def __validate_pod_with_keystone_pid(self, keystone_pid):
        for pod_key, pod_values in self.driver.get_pods().items():
            if pod_values and "keystone_project_id" in pod_values[0] \
                    and pod_values[0]['keystone_project_id'] == keystone_pid:
                return True

    def __is_slave_exist(self, slave_name):
        for slave in self.driver.get_slaves():
            if "name" in slave and "configured" in slave \
                    and slave_name == slave["name"] and slave["configured"]:
                return True

    def __get_slave_names(self):
        for slave in self.driver.get_slaves():
            if "name" in slave:
                yield slave["name"]

    @check_auth
    def post(self, uuid=None, user_id=None):
        """Create a new pod.

        :param uuid: uuid of the pod (not used here)
        :param user_id: user ID who do the request
        :request body: {
            "pdp_id": "fa2323f7055d4a88b1b85d31fe5e8369",
            "name": "pdp_rbac3",
            "keystone_project_id": "ceacbb5564cc48ad929dd4f00e52bf63",
            "models": {...},
            "policies": {...},
            "description": "test",
            "security_pipeline": [...],
            "slave_name": ""
        }
        :return: {
            "pdp_id1": {
                "name": "...",
                "replicas": "...",
                "description": "...",
            }
        }
        """
        if "security_pipeline" in request.json:
            if self.__validate_pod_with_keystone_pid(request.json.get("keystone_project_id")):
                raise exceptions.PipelineConflict
            if not request.json.get("pdp_id"):
                raise exceptions.PdpUnknown
            if not request.json.get("security_pipeline"):
                raise exceptions.PolicyUnknown
            self.driver.create_pipeline(
                request.json.get("keystone_project_id"),
                request.json.get("pdp_id"),
                request.json.get("security_pipeline"),
                manager_data=request.json,
                slave_name=request.json.get("slave_name"))
        else:
            logger.info("------------------------------------")
            logger.info(list(self.__get_slave_names()))
            logger.info("------------------------------------")
            if self.__is_slave_exist(request.json.get("slave_name")):
                raise exceptions.WrapperConflict
            if request.json.get("slave_name") not in self.__get_slave_names():
                raise exceptions.SlaveNameUnknown
            slave_name = request.json.get("slave_name")
            if not slave_name:
                slave_name = self.driver.get_slaves(active=True)
            self.driver.create_wrappers(slave_name)
        return {"pods": self.driver.get_pods()}

    @check_auth
    def delete(self, uuid=None, user_id=None):
        """Delete a pod

        :param uuid: uuid of the pod to delete
        :param user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message"
        }
        """
        try:
            self.driver.delete_pipeline(uuid)
            return {'result': True}
        except exceptions.PipelineUnknown:
            for slave in self.driver.get_slaves():
                if "name" in slave and "wrapper_name" in slave:
                    if uuid in (slave['name'], slave["wrapper_name"]):
                        self.driver.delete_wrapper(name=slave["wrapper_name"])
                else:
                    raise exceptions.SlaveNameUnknown
        except Exception as e:
            return {"result": False, "message": str(e)}, 500

    # @check_auth
    # def patch(self, uuid=None, user_id=None):
    #     """Update a pod
    #
    #     :param uuid: uuid of the pdp to update
    #     :param user_id: user ID who do the request
    #     :request body: {
    #         "name": "...",
    #         "replicas": "...",
    #         "description": "...",
    #     }
    #     :return: {
    #         "pod_id1": {
    #             "name": "...",
    #             "replicas": "...",
    #             "description": "...",
    #         }
    #     }
    #     :internal_api: update_pdp
    #     """
    #     return {"pods": None}
