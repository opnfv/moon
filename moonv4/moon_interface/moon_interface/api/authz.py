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
import requests
import time
from uuid import uuid4

from moon_interface.containers import DockerManager
from moon_interface.authz_requests import AuthzRequest
from moon_utilities import configuration

__version__ = "0.1.0"

LOG = logging.getLogger("moon.interface.api." + __name__)


def pdp_in_cache(cache, uuid):
    """Check if a PDP exist with this Keystone Project ID in the cache of this component

    :param cache: Cache to use
    :param uuid: Keystone Project ID
    :return: True or False
    """
    for item_uuid, item_value in cache.pdp.items():
        if uuid == item_value['keystone_project_id']:
            return item_uuid, item_value
    return None, None


def pdp_in_manager(cache, uuid):
    """Check if a PDP exist with this Keystone Project ID in the Manager component

    :param cache: Cache to use
    :param uuid: Keystone Project ID
    :return: True or False
    """
    cache.update()
    return pdp_in_cache(cache, uuid)


def container_exist(cache, uuid):
    """Check if a PDP exist with this Keystone Project ID in the Manager component

    :param cache: Cache to use
    :param uuid: Keystone Project ID
    :return: True or False
    """
    for key, value in cache.containers.items():
        if "keystone_project_id" not in value:
            continue
        if value["keystone_project_id"] == uuid:
            try:
                req = requests.head("http://{}:{}/".format(
                    value.get("hostname"),
                    value.get("port")[0].get("PublicPort")))
                LOG.info("container_exist {}".format(req.status_code))
                if req.status_code in (200, 201):
                    return value
                return
            except requests.exceptions.ConnectionError:
                pass
            # maybe hostname is not working so trying with IP address
            try:
                req = requests.head("http://{}:{}/".format(
                    value.get("ip"),
                    value.get("port")[0].get("PublicPort")))
                if req.status_code in (200, 201):
                    return value
                return
            except requests.exceptions.ConnectionError:
                return


def build_container(cache, manager_url, uuid, meta_rule_id, plugin_name="authz"):
    """Create the container and update the cache with the given perimeter elements

    :param cache: Cache to use
    :param manager_url: URL of the manager
    :param uuid: Keystone Project ID
    :param meta_rule_id: UUID of the meta_rule
    :param plugin_name: name of the plugin to use
    :return: True or False
    """
    LOG.info("Building a new container for {}".format(plugin_name))
    manager = DockerManager()
    tcp_port = configuration.increment_port()
    container_name = configuration.get_plugins()[plugin_name]['container']
    name = "{}_{}".format(plugin_name, uuid4().hex)
    policy_id = cache.get_policy_from_meta_rules(meta_rule_id)
    container_data = {
        "name": name,
        "hostname": name,
        "port": {
            "PrivatePort": tcp_port,
            "Type": "tcp",
            "IP": "0.0.0.0",
            "PublicPort": tcp_port
        },
        "keystone_project_id": uuid,
        "pdp_id": cache.get_pdp_from_keystone_project(uuid),
        "meta_rule_id": meta_rule_id,
        "policy_id": policy_id,
        "container_name": container_name,
        "plugin_name": plugin_name
    }
    container = manager.create_container(container_data)
    container_data['container_id'] = container.id
    container_data['port']["IP"] = container.ip
    container_data['start_time'] = time.time()
    req = requests.post("{}/containers".format(manager_url),
                        json=container_data)
    if req.status_code == 200:
        cache.add_container(container_data)
        return True


def create_containers(cache, manager_url, uuid, plugin_name="authz"):
    """Create the container and update the cache with the given perimeter elements

    :param cache: Cache to use
    :param manager_url: URL of the manager
    :param uuid: Keystone Project ID
    :param plugin_name: name of the plugin to use
    :return: True or False
    """
    LOG.info("Need to create some containers for {}".format(uuid))
    for pdp_id, pdp_value in cache.pdp.items():
        LOG.info("pdp {}".format(pdp_value))
        if uuid == pdp_value.get("keystone_project_id", ""):
            LOG.info("uuid {}".format(uuid))
            for policy_id in pdp_value.get("security_pipeline", []):
                LOG.info("policy {}".format(policy_id))
                model_id = cache.policies[policy_id]["model_id"]
                model_value = cache.models[model_id]
                for meta_rule_id in model_value["meta_rules"]:
                    LOG.info("meta_rule {}".format(meta_rule_id))
                    build_container(
                        cache=cache,
                        uuid=uuid,
                        manager_url=manager_url,
                        meta_rule_id=meta_rule_id,
                        plugin_name=plugin_name)
            return


def create_authz_request(cache, interface_name, manager_url, uuid, subject_name, object_name, action_name):
    """Create the authorization request and make the first call to the Authz function

    :param cache: Cache to use
    :param interface_name: hostname of the interface
    :param manager_url: URL of the manager
    :param uuid: Keystone Project ID
    :param subject_name: name of the subject
    :param object_name: name of the object
    :param action_name: name of the action
    :return: Authorisation request
    """
    req_id = uuid4().hex
    ctx = {
        "project_id": uuid,
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


class Authz(Resource):
    """
    Endpoint for authz requests
    """

    __urls__ = (
        "/authz/<string:uuid>",
        "/authz/<string:uuid>/<string:subject_name>/<string:object_name>/<string:action_name>",
    )

    def __init__(self, **kwargs):
        self.CACHE = kwargs.get("cache")
        self.INTERFACE_NAME = kwargs.get("interface_name", "interface")
        self.MANAGER_URL = kwargs.get("manager_url", "http://manager:8080")
        self.TIMEOUT = 5

    def get(self, uuid=None, subject_name=None, object_name=None, action_name=None):
        """Get a response on an authorization request

        :param uuid: uuid of a tenant or an intra_extension
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
        pdp_id, pdp_value = pdp_in_cache(self.CACHE, uuid)
        if not pdp_id:
            pdp_id, pdp_value = pdp_in_manager(self.CACHE, uuid)
            if not pdp_id:
                return {
                           "result": False,
                           "message": "Unknown Project ID or "
                                      "Project ID is not bind to a PDP."}, 403
        if not container_exist(self.CACHE, uuid):
            create_containers(
                cache=self.CACHE,
                uuid=uuid,
                manager_url=self.MANAGER_URL,
                plugin_name="authz")
        authz_request = create_authz_request(
            cache=self.CACHE,
            uuid=uuid,
            interface_name=self.INTERFACE_NAME,
            manager_url=self.MANAGER_URL,
            subject_name=subject_name,
            object_name=object_name,
            action_name=action_name)
        cpt = 0
        while True:
            if cpt > self.TIMEOUT*10:
                return {"result": False,
                        "message": "Authz request had timed out."}, 500
            if authz_request.is_authz():
                if authz_request.final_result == "Grant":
                    return {"result": True, "message": ""}, 200
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
