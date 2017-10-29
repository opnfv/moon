# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from kubernetes import client, config
import logging
import urllib3.exceptions
import time
from moon_utilities import configuration

logger = logging.getLogger("moon.orchestrator.drivers")


def get_driver():
    try:
        driver = K8S()
    except urllib3.exceptions.MaxRetryError as e:
        logger.exception(e)
        return Docker()
    else:
        return K8S()


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

    def get_pods(self, namespace=None):
        raise NotImplementedError

    def load_pod(self, data, api_client=None, ext_client=None):
        raise NotImplementedError

    def delete_pod(self, uuid=None, name=None):
        raise NotImplementedError

    def get_slaves(self):
        raise NotImplementedError


class K8S(Driver):

    def __init__(self):
        super(K8S, self).__init__()
        config.load_kube_config()
        self.client = client.CoreV1Api()

    def get_pods(self, name=None):
        # pods = self.client.list_pod_for_all_namespaces(watch=False)
        # if not namespace:
        #     return pods
        # # TODO: get pods with specific namespace
        # for pod in pods:
        #     logger.info("%s\t%s\t%s" % (pod.status.pod_ip,
        #                                 pod.metadata.namespace,
        #                                 pod.metadata.name))
        # return pods
        if name:
            pods = self.client.list_pod_for_all_namespaces(watch=False)
            for pod in pods:
                if pod.metadata.name == name:
                    return pod
            else:
                return None
        return self.cache

    def __create_pod(self, client, data):
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
                    # 'hostname': data.get('name'),
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
                    'ports': [
                        {"containerPort": _data.get('port', 80)},
                    ],
                    'env': [
                        {'name': "UUID", "value": _data.get('name', "None")},
                        {'name': "TYPE", "value": _data.get('genre', "None")},
                        {'name': "PORT", "value": str(_data.get('port', 80))},
                        {'name': "PDP_ID", "value": _data.get('pdp_id', "None")},
                        {'name': "META_RULE_ID", "value": "None"},
                        {'name': "KEYSTONE_PROJECT_ID",
                         "value": _data.get('keystone_project_id', "None")},
                    ]
                }
            )
        resp = client.create_namespaced_deployment(body=pod_manifest,
                                                   namespace='moon')
        logger.info("Pod {} created!".format(data[0].get('name')))
        return resp

    def __create_service(self, client, data, expose=False):
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
                'type': 'NodePort',
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
        return resp

    def load_pod(self, data, api_client=None, ext_client=None, expose=False):
        _client = api_client if api_client else self.client
        logger.info("Creating pod/service {}".format(data[0].get('name')))
        logger.info("Creating pod/service {}".format(data))
        pod = self.__create_pod(client=ext_client, data=data)
        service = self.__create_service(client=_client, data=data[0],
                                        expose=expose)
        # logger.info("data={}".format(data))
        # logger.info("service={}".format(service))
        self.cache[pod.metadata.uid] = data
        #     {
        #     "ip": "",
        #     "hostname": pod.metadata.name,
        #     "port": service.spec.ports[0].node_port,
        #     "pdp": "",
        #     "keystone_project_id": data[0].get('keystone_project_id'),
        #     "plugin_names": [d.get('genre') for d in data],
        #     "namespace": "moon"
        # }

    def delete_pod(self, uuid=None, name=None):
        logger.info("Deleting pod {}".format(uuid))

    def get_slaves(self):
        contexts, active_context = config.list_kube_config_contexts()
        return contexts, active_context


class Docker(Driver):

    def load_pod(self, data, api_client=None, ext_client=None):
        logger.info("Creating pod {}".format(data[0].get('name')))

    def delete_pod(self, uuid=None, name=None):
        logger.info("Deleting pod {}".format(uuid))
