# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from kubernetes import client, config
import logging
import requests
import urllib3.exceptions
from python_moonutilities import configuration, exceptions
from python_moonutilities.misc import get_random_name

logger = logging.getLogger("moon.orchestrator.drivers")


def get_driver():
    try:
        return K8S()
    except urllib3.exceptions.MaxRetryError as e:
        logger.exception(e)
        return Docker()


class Driver:

    def __init__(self):
        self.cache = {}
        # example of cache:
        # {
        #     "uuid_of_pod": {
        #         "ip": "",
        #         "hostname": "",
        #         "port": 30001,
        #         "pdp": "",
        #         "keystone_project_id": "",
        #         "plugin_name": "",
        #         "namespace": ""
        #     }
        # }

    def get_slaves(self):
        raise NotImplementedError

    def create_wrappers(self):
        raise NotImplementedError

    def delete_wrapper(self, name):
        raise NotImplementedError

    def create_pipeline(self, keystone_project_id,
                        pdp_id, policy_ids, manager_data=None,
                        active_context=None,
                        active_context_name=None):
        raise NotImplementedError

    def delete_pipeline(self, uuid=None, name=None, namespace="moon",
                        active_context=None,
                        active_context_name=None):
        raise NotImplementedError


class K8S(Driver):

    def __init__(self):
        super(K8S, self).__init__()
        config.load_kube_config()
        self.client = client.CoreV1Api()
        conf = configuration.get_configuration("components/orchestrator")
        self.orchestrator_hostname = conf["components/orchestrator"].get("hostname", "orchestrator")
        self.orchestrator_port = conf["components/orchestrator"].get("port", 80)
        conf = configuration.get_configuration("components/manager")
        self.manager_hostname = conf["components/manager"].get("hostname", "manager")
        self.manager_port = conf["components/manager"].get("port", 80)

    def get_pods(self, name=None):
        if name:
            pods = self.client.list_pod_for_all_namespaces(watch=False)
            for pod in pods.items:
                logger.debug("get_pods {}".format(pod.metadata.name))
                if name in pod.metadata.name:
                    return pod
            else:
                return None
        logger.debug("get_pods cache={}".format(self.cache))
        return self.cache

    @staticmethod
    def __create_deployment(client, data):
        pod_manifest = {
            'apiVersion': 'extensions/v1beta1',
            'kind': 'Deployment',
            'metadata': {
                'name': data[0].get('name')
            },
            'spec': {
                'replicas': 1,
                'template': {
                    'metadata': {'labels': {'app': data[0].get('name')}},
                    'hostname': data[0].get('name'),
                    'spec': {
                        'containers': []
                    }
                },
            }
        }
        for _data in data:
            pod_manifest['spec']['template']['spec']['containers'].append(
                {
                    'image': _data.get('container', "busybox"),
                    'name': _data.get('name'),
                    'hostname': _data.get('name'),
                    'ports': [
                        {"containerPort": _data.get('port', 80)},
                    ],
                    'env': [
                        {'name': "UUID", "value": _data.get('name', "None")},
                        {'name': "TYPE", "value": _data.get('genre', "None")},
                        {'name': "PORT", "value": str(_data.get('port', 80))},
                        {'name': "PDP_ID", "value": _data.get('pdp_id', "None")},
                        {'name': "META_RULE_ID", "value": _data.get('meta_rule_id', "None")},
                        {'name': "KEYSTONE_PROJECT_ID",
                         "value": _data.get('keystone_project_id', "None")},
                    ]
                }
            )
        resp = client.create_namespaced_deployment(body=pod_manifest,
                                                   namespace='moon')
        logger.info("Pod {} created!".format(data[0].get('name')))
        return resp

    @staticmethod
    def __create_service(client, data, expose=False):
        service_manifest = {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': data.get('name'),
                'namespace': 'moon'
            },
            'spec': {
                'ports': [{
                    'port': data.get('port', 80),
                    'targetPort': data.get('port', 80)
                }],
                'selector': {
                    'app': data.get('name')
                },
                # 'type': 'NodePort',
                'endpoints': [{
                    'port': data.get('port', 80),
                    'protocol': 'TCP',
                }],
            }
        }
        if expose:
            service_manifest['spec']['ports'][0]['nodePort'] = \
                configuration.increment_port()
            service_manifest['spec']['type'] = "NodePort"
        resp = client.create_namespaced_service(namespace="moon",
                                                body=service_manifest)
        logger.info("Service {} created!".format(data.get('name')))
        return service_manifest

    def load_deployment_and_service(self, data, api_client=None, ext_client=None, expose=False):
        _client = api_client if api_client else self.client
        manifest = self.__create_service(client=_client, data=data[0],
                                         expose=expose)
        data[0]["external_port"] = manifest['spec']['ports'][0].get('nodePort')
        pod = self.__create_deployment(client=ext_client, data=data)
        self.cache[pod.metadata.uid] = data

    def delete_deployment(self, name=None, namespace="moon", ext_client=None):
        logger.info("Deleting deployment {}".format(name))
        body = client.V1DeleteOptions(propagation_policy='Foreground')
        ret = ext_client.delete_namespaced_deployment(
            name=name,
            namespace=namespace,
            body=body
        )
        logger.debug(ret)
        _uid = None
        for uid, value in self.cache.items():
            if value[0]['name'] == name:
                _uid = uid
                break
        if _uid:
            self.cache.pop(_uid)
        else:
            raise exceptions.DockerError("Cannot find and delete pod named {}".format(name))

    def delete_service(self, name, namespace="moon", api_client=None):
        if not api_client:
            api_client = self.client
        ret = api_client.delete_namespaced_service(name=name, namespace=namespace)
        logger.debug("delete_service {}".format(ret))

    def get_slaves(self, active=False):
        contexts, active_context = self.get_contexts()
        pods = self.get_pods()
        # logger.info("pods = {}".format(pods))
        slaves = []
        if active:
            for key, value in pods.items():
                # logger.info("ctx={}".format(active_context))
                # logger.info("value={}".format(value))
                if "name" in active_context and value and "name" in value[0]:
                    if active_context["name"] == value[0].get('slave_name'):
                        data = dict(active_context)
                        data["wrapper_name"] = value[0]['name']
                        data["ip"] = value[0].get("ip", "NC")
                        data["port"] = value[0].get("external_port", "NC")
                        slaves.append(data)
                        break
            return slaves
        for ctx in contexts:
            data = dict(ctx)
            data["configured"] = False
            for key, value in pods.items():
                # logger.info("ctx={}".format(ctx))
                # logger.info("value={}".format(value))
                if "name" in ctx and value and "name" in value[0]:
                    if ctx["name"] == value[0].get('slave_name'):
                        data["wrapper_name"] = value[0]['name']
                        data["ip"] = value[0].get("ip", "NC")
                        data["port"] = value[0].get("external_port", "NC")
                        data["configured"] = True
                        break
            slaves.append(data)
        return slaves

    @staticmethod
    def get_contexts():
        contexts, active_context = config.list_kube_config_contexts()
        return contexts, active_context

    def create_wrappers(self, slave_name=None):
        contexts, active_context = self.get_contexts()
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
            if slave_name and slave_name != _ctx['name']:
                continue
            _config = config.new_client_from_config(context=_ctx['name'])
            logger.debug("_config={}".format(_config))
            api_client = client.CoreV1Api(_config)
            ext_client = client.ExtensionsV1beta1Api(_config)
            data = [{
                "name": hostname + "-" + get_random_name(),
                "container": container,
                "port": port,
                "namespace": "moon",
                "slave_name": _ctx['name']
            }, ]
            self.load_deployment_and_service(data, api_client, ext_client, expose=True)

    def delete_wrapper(self, uuid=None, name=None, namespace="moon",
                       active_context=None,
                       active_context_name=None):
        name_to_delete = None
        if uuid and uuid in self.get_pods():
            name_to_delete = self.get_pods()[uuid][0]['name']
        elif name:
            for pod_key, pod_list in self.get_pods().items():
                for pod_value in pod_list:
                    if pod_value.get("name") == name:
                        name_to_delete = pod_value.get("name")
                        break
        if not name_to_delete:
            raise exceptions.WrapperUnknown
        contexts, _active_context = self.get_contexts()
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
            self.delete_deployment(name=name_to_delete, namespace=namespace,
                                   ext_client=ext_client)
            self.delete_service(name=name_to_delete, api_client=api_client)
            return
        logger.debug("contexts={}".format(contexts))
        for _ctx in contexts:
            _config = config.new_client_from_config(context=_ctx['name'])
            logger.debug("_config={}".format(_config))
            api_client = client.CoreV1Api(_config)
            ext_client = client.ExtensionsV1beta1Api(_config)
            self.delete_deployment(name=name_to_delete, namespace=namespace,
                                   ext_client=ext_client)
            self.delete_service(name=name_to_delete, api_client=api_client)

    def create_pipeline(self, keystone_project_id,
                        pdp_id, policy_ids, manager_data=None,
                        active_context=None,
                        slave_name=None):
        """ Create security functions

        :param keystone_project_id: the Keystone project id
        :param pdp_id: the PDP ID mapped to this pipeline
        :param policy_ids: the policy IDs mapped to this pipeline
        :param manager_data: data needed to create pods
        :param active_context: if present, add the security function in this
                               context
        :param slave_name: if present,  add the security function in
                                    this context name
        if active_context_name and active_context are not present, add the
        security function in all context (ie, in all slaves)
        :return: None
        """
        if not manager_data:
            manager_data = dict()
        for key, value in self.get_pods().items():
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
        #   When policies and models are empty, is it right that it returns 200 ?
        #   Should it return no found policies or models ?
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

        if not policy_ids:
            raise exceptions.PolicyUnknown
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
        contexts, _active_context = self.get_contexts()
        logger.debug("active_context_name={}".format(slave_name))
        logger.debug("active_context={}".format(active_context))
        if slave_name:
            for _context in contexts:
                if _context["name"] == slave_name:
                    active_context = _context
                    break
        if active_context:
            active_context = _active_context
            _config = config.new_client_from_config(
                context=active_context['name'])
            logger.debug("_config={}".format(_config))
            api_client = client.CoreV1Api(_config)
            ext_client = client.ExtensionsV1beta1Api(_config)
            self.load_deployment_and_service(data, api_client, ext_client, expose=False)
            return
        logger.debug("contexts={}".format(contexts))
        for _ctx in contexts:
            if slave_name and slave_name != _ctx['name']:
                continue
            _config = config.new_client_from_config(context=_ctx['name'])
            logger.debug("_config={}".format(_config))
            api_client = client.CoreV1Api(_config)
            ext_client = client.ExtensionsV1beta1Api(_config)
            self.load_deployment_and_service(data, api_client, ext_client, expose=False)

    def delete_pipeline(self, uuid=None, name=None, namespace="moon",
                        active_context=None,
                        active_context_name=None):
        """Delete a pipeline

        :param uuid:
        :param name:
        :param namespace:
        :param active_context:
        :param active_context_name:
        :return:
        """
        name_to_delete = None
        if uuid and uuid in self.get_pods():
            name_to_delete = self.get_pods()[uuid][0]['name']
        elif name:
            for pod_key, pod_list in self.get_pods().items():
                for pod_value in pod_list:
                    if pod_value.get("name") == name:
                        name_to_delete = pod_value.get("name")
                        break
        if not name_to_delete:
            raise exceptions.PipelineUnknown
        logger.info("Will delete deployment and service named {}".format(name_to_delete))
        contexts, _active_context = self.get_contexts()
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
            self.delete_deployment(name=name_to_delete, namespace=namespace,
                                   ext_client=ext_client)
            self.delete_service(name=name_to_delete, api_client=api_client)
            return
        logger.debug("contexts={}".format(contexts))
        for _ctx in contexts:
            _config = config.new_client_from_config(context=_ctx['name'])
            logger.debug("_config={}".format(_config))
            api_client = client.CoreV1Api(_config)
            ext_client = client.ExtensionsV1beta1Api(_config)
            self.delete_deployment(name=name_to_delete, namespace=namespace,
                                   ext_client=ext_client)
            self.delete_service(name=name_to_delete, api_client=api_client)


class Docker(Driver):

    def get_slaves(self):
        raise NotImplementedError

    def create_wrappers(self):
        raise NotImplementedError

    def delete_wrapper(self, name):
        raise NotImplementedError

    def create_pipeline(self, keystone_project_id,
                        pdp_id, policy_ids, manager_data=None,
                        active_context=None,
                        active_context_name=None):
        raise NotImplementedError

    def delete_pipeline(self, uuid=None, name=None, namespace="moon",
                        active_context=None,
                        active_context_name=None):
        raise NotImplementedError
