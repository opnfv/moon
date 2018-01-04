# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from flask import Flask, jsonify
from flask_restful import Resource, Api
from kubernetes import client, config
import logging
import requests
import time
from moon_orchestrator import __version__
from moon_orchestrator.api.pods import Pods
from moon_orchestrator.api.generic import Status
from moon_orchestrator.drivers import get_driver
from python_moonutilities import configuration, exceptions
from python_moonutilities.misc import get_random_name

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
    __urls__ = ("/", )
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
        self.create_wrappers()
        for _pdp_key, _pdp_value in pdp.json()['pdps'].items():
            if _pdp_value.get('keystone_project_id'):
                # TODO: select context to add security function
                self.create_pipeline(
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
                                  "driver": self.driver,
                                  "create_pipeline_hook":
                                      self.create_pipeline,
                              })

    def run(self):
        self.app.run(host=self._host, port=self._port)  # nosec

    @staticmethod
    def __filter_str(data):
        return data.replace("@", "-")

    def create_wrappers(self):
        contexts, active_context = self.driver.get_slaves()
        logger.debug("contexts: {}".format(contexts))
        logger.debug("active_context: {}".format(active_context))
        conf = configuration.get_configuration("components/wrapper")
        hostname = conf["components/wrapper"].get(
            "hostname", "wrapper")
        port = conf["components/wrapper"].get("port", 80)
        container = conf["components/wrapper"].get(
            "container",
            "wukongsun/moon_wrapper:v4.3")
        for _ctx in contexts:
            _config = config.new_client_from_config(context=_ctx['name'])
            logger.debug("_config={}".format(_config))
            api_client = client.CoreV1Api(_config)
            ext_client = client.ExtensionsV1beta1Api(_config)
            data = [{
                "name": hostname + "-" + get_random_name(),
                "container": container,
                "port": port,
                "namespace": "moon"
            }, ]
            pod = self.driver.load_pod(data, api_client, ext_client, expose=True)
            logger.debug('wrapper pod={}'.format(pod))

    def create_pipeline(self, keystone_project_id,
                        pdp_id, policy_ids, manager_data=None,
                        active_context=None,
                        active_context_name=None):
        """ Create security functions

        :param keystone_project_id: the Keystone project id
        :param pdp_id: the PDP ID mapped to this pipeline
        :param policy_ids: the policy IDs mapped to this pipeline
        :param manager_data: data needed to create pods
        :param active_context: if present, add the security function in this
                               context
        :param active_context_name: if present,  add the security function in
                                    this context name
        if active_context_name and active_context are not present, add the
        security function in all context (ie, in all slaves)
        :return: None
        """
        if not manager_data:
            manager_data = dict()
        for key, value in self.driver.get_pods().items():
            for _pod in value:
                if _pod.get('keystone_project_id') == keystone_project_id:
                    logger.warning("A pod for this Keystone project {} "
                                   "already exists.".format(keystone_project_id))
                    return

        plugins = configuration.get_plugins()
        conf = configuration.get_configuration("components/pipeline")
        # i_hostname = conf["components/pipeline"].get("interface").get("hostname", "interface")
        i_port = conf["components/pipeline"].get("interface").get("port", 80)
        i_container = conf["components/pipeline"].get("interface").get(
            "container",
            "wukongsun/moon_interface:v4.3")
        data = [
            {
                "name": "pipeline-" + get_random_name(),
                "container": i_container,
                "port": i_port,
                'pdp_id': pdp_id,
                'genre': "interface",
                'keystone_project_id': keystone_project_id,
                "namespace": "moon"
            },
        ]
        logger.debug("data={}".format(data))
        policies = manager_data.get('policies')
        if not policies:
            logger.info("No policy data from Manager, trying to get them")
            policies = requests.get("http://{}:{}/policies".format(
                self.manager_hostname, self.manager_port)).json().get(
                "policies", dict())
        logger.debug("policies={}".format(policies))
        models = manager_data.get('models')
        if not models:
            logger.info("No models data from Manager, trying to get them")
            models = requests.get("http://{}:{}/models".format(
                self.manager_hostname, self.manager_port)).json().get(
                "models", dict())
        logger.debug("models={}".format(models))

        for policy_id in policy_ids:
            if policy_id in policies:
                genre = policies[policy_id].get("genre", "authz")
                if genre in plugins:
                    for meta_rule in models[policies[policy_id]['model_id']]['meta_rules']:
                        data.append({
                            "name": genre + "-" + get_random_name(),
                            "container": plugins[genre]['container'],
                            'pdp_id': pdp_id,
                            "port": plugins[genre].get('port', 8080),
                            'genre': genre,
                            'policy_id': policy_id,
                            'meta_rule_id': meta_rule,
                            'keystone_project_id': keystone_project_id,
                            "namespace": "moon"
                        })
        logger.debug("data={}".format(data))
        contexts, _active_context = self.driver.get_slaves()
        logger.debug("active_context_name={}".format(active_context_name))
        logger.debug("active_context={}".format(active_context))
        if active_context_name:
            for _context in contexts:
                if _context["name"] == active_context_name:
                    active_context = _context
                    break
        if active_context:
            active_context = _active_context
            _config = config.new_client_from_config(
                context=active_context['name'])
            logger.debug("_config={}".format(_config))
            api_client = client.CoreV1Api(_config)
            ext_client = client.ExtensionsV1beta1Api(_config)
            self.driver.load_pod(data, api_client, ext_client, expose=False)
            return
        logger.debug("contexts={}".format(contexts))
        for _ctx in contexts:
            _config = config.new_client_from_config(context=_ctx['name'])
            logger.debug("_config={}".format(_config))
            api_client = client.CoreV1Api(_config)
            ext_client = client.ExtensionsV1beta1Api(_config)
            self.driver.load_pod(data, api_client, ext_client, expose=False)


