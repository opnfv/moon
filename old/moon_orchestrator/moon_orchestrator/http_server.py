# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from flask import Flask, jsonify
from flask_restful import Resource, Api
import logging
import requests
import time
from moon_orchestrator import __version__
from moon_orchestrator.api.pods import Pods
from moon_orchestrator.api.slaves import Slaves
from moon_orchestrator.api.generic import Status
from moon_orchestrator.drivers import get_driver
from python_moonutilities import configuration, exceptions

logger = logging.getLogger("moon.orchestrator.http_server")

__API__ = (
    Status,
)


class Server:
    """Base class for HTTP server"""

    def __init__(self, host="localhost", port=80, api=None, **kwargs):
        """Run a server

        :param host: hostname of the server
        :param port: port for the running server
        :param kwargs: optional parameters
        :return: a running server
        """
        self._host = host
        self._port = port
        self._api = api
        self._extra = kwargs

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, name):
        self._host = name

    @host.deleter
    def host(self):
        self._host = ""

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, number):
        self._port = number

    @port.deleter
    def port(self):
        self._port = 80

    def run(self):
        raise NotImplementedError()


class Root(Resource):
    """
    The root of the web service
    """
    __urls__ = ("/",)
    __methods = ("get", "post", "put", "delete", "options")

    def get(self):
        tree = {"/": {"methods": ("get",), "description": "List all methods for that service."}}
        for item in __API__:
            tree[item.__name__] = {"urls": item.__urls__}
            _methods = []
            for _method in self.__methods:
                if _method in dir(item):
                    _methods.append(_method)
            tree[item.__name__]["methods"] = _methods
            tree[item.__name__]["description"] = item.__doc__.strip()
        return {
            "version": __version__,
            "tree": tree
        }


class HTTPServer(Server):

    def __init__(self, host="localhost", port=80, **kwargs):
        super(HTTPServer, self).__init__(host=host, port=port, **kwargs)
        self.app = Flask(__name__)
        conf = configuration.get_configuration("components/orchestrator")
        self.orchestrator_hostname = conf["components/orchestrator"].get("hostname", "orchestrator")
        self.orchestrator_port = conf["components/orchestrator"].get("port", 80)
        conf = configuration.get_configuration("components/manager")
        self.manager_hostname = conf["components/manager"].get("hostname", "manager")
        self.manager_port = conf["components/manager"].get("port", 80)
        # TODO : specify only few urls instead of *
        # CORS(self.app)
        self.api = Api(self.app)
        self.driver = get_driver()
        logger.info("Driver = {}".format(self.driver.__class__))
        self.__set_route()
        self.__hook_errors()
        pdp = None
        while True:
            try:
                pdp = requests.get(
                    "http://{}:{}/pdp".format(self.manager_hostname,
                                              self.manager_port))
            except requests.exceptions.ConnectionError:
                logger.warning("Manager is not ready, standby...")
                time.sleep(1)
            except KeyError:
                logger.warning("Manager is not ready, standby...")
                time.sleep(1)
            else:
                if "pdps" in pdp.json():
                    break
        logger.debug("pdp={}".format(pdp))
        # self.driver.create_wrappers()
        for _pdp_key, _pdp_value in pdp.json()['pdps'].items():
            if _pdp_value.get('keystone_project_id'):
                # TODO: select context to add security function
                self.driver.create_pipeline(
                    keystone_project_id=_pdp_value.get('keystone_project_id'),
                    pdp_id=_pdp_key,
                    policy_ids=_pdp_value.get('security_pipeline', []))

    def __hook_errors(self):

        def get_404_json(e):
            return jsonify({"result": False, "code": 404, "description": str(e)}), 404

        self.app.register_error_handler(404, get_404_json)

        def get_400_json(e):
            return jsonify({"result": False, "code": 400, "description": str(e)}), 400

        self.app.register_error_handler(400, lambda e: get_400_json)
        self.app.register_error_handler(403, exceptions.AuthException)

    def __set_route(self):
        self.api.add_resource(Root, '/')

        for api in __API__:
            self.api.add_resource(api, *api.__urls__)
        self.api.add_resource(Pods, *Pods.__urls__,
                              resource_class_kwargs={
                                  "driver": self.driver
                              })
        self.api.add_resource(Slaves, *Slaves.__urls__,
                              resource_class_kwargs={
                                  "driver": self.driver
                              })

    def run(self):
        self.app.run(host=self._host, port=self._port, threaded=True)  # nosec

    @staticmethod
    def __filter_str(data):
        return data.replace("@", "-")
