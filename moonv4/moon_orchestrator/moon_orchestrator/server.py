# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import sys
import os
import hashlib
from oslo_config import cfg
from oslo_log import log as logging
import oslo_messaging
from docker import Client
import docker.errors as docker_errors
from importlib.machinery import SourceFileLoader
from moon_utilities import options
from moon_orchestrator.security_router import SecurityRouter
from moon_orchestrator.security_interface import SecurityInterface
from moon_orchestrator.security_manager import SecurityManager
from moon_orchestrator.security_function import SecurityFunction
# from moon_orchestrator.security_policy import SecurityPolicy
# from moon_orchestrator.security_function import SecurityFunction
from moon_orchestrator import messenger

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

CONTAINERS = {}
SLAVES = {}
docker = Client(base_url=CONF.docker_url)


# def get_template(filename="template.dockerfile"):
#     simple_loader = FileSystemLoader(TEMPLATES_FOLDER)
#     env = Environment(loader=simple_loader)
#     return env.get_template(filename)


def create_docker_network(name="moon"):

    return docker.create_networking_config({
        name: docker.create_endpoint_config(),
        'aliases': ['orchestrator', ]
    })


def load_plugin(plugname):
    try:
        m = SourceFileLoader("scenario", os.path.join(CONF.plugin_dir, plugname+".py"))
        return m.load_module()
    except ImportError as e:
        LOG.error("Error in importing plugin {}".format(plugname))
        LOG.error("{}".format(e))


class DockerManager:

    @staticmethod
    def load(component, uuid):
        """Load a new docker mapping the component given

        :param component: the name of the component (policy or function)
        :param uuid: the uuid of the intra_extension linked to that component
        :return: the created component
        """
        component_id = "authz_"+hashlib.sha224(uuid.encode("utf-8")).hexdigest()
        if component_id not in CONTAINERS:
            plug = load_plugin(component)
            LOG.info("Creating {} with id {}".format(component, uuid))
            component = plug.run(uuid, options.filename, docker=docker, network_config=create_docker_network())
            CONTAINERS[component_id] = component
            return component

    @staticmethod
    def get_component(uuid=None):
        if uuid:
            return CONTAINERS.get(uuid, None)
        return CONTAINERS

    @staticmethod
    def kill(component_id, delete=True):
        LOG.info("Killing container {}".format(component_id))
        docker.kill(container=component_id)
        if delete:
            docker.remove_container(container=component_id)


def _exit(exit_number=0, docker=None, error=None):
    for _container in CONTAINERS:
        LOG.warning("Deleting containers named {}...".format(_container))
        # print(40 * "-" + _container)
        try:
            # print(docker.logs(container=_container).decode("utf-8"))
            docker.kill(container=_container)
        except docker_errors.NotFound:
            LOG.error("The container {} was not found".format(_container))
        except docker_errors.APIError as e:
            LOG.error(e)
        else:
            docker.remove_container(container=_container)

    # TODO (dthom): put in the debug log
    if error:
        LOG.info(str(error))
    sys.exit(exit_number)


def main():
    # conf_file = options.configure(DOMAIN)
    LOG.info("Starting server with IP {}".format(CONF.orchestrator.host))

    docker_manager = DockerManager()

    network_config = create_docker_network()

    LOG.info("Creating Security Router")
    router = SecurityRouter(options.filename, docker=docker, network_config=network_config)
    CONTAINERS[router.id] = router

    LOG.info("Creating Manager")
    manager = SecurityManager(options.filename, docker=docker, network_config=network_config)
    CONTAINERS[manager.id] = manager

    LOG.info("Creating Security Interface")
    interface = SecurityInterface(options.filename, docker=docker, network_config=network_config)
    CONTAINERS[interface.id] = interface

    try:
        router.get_status()
    except oslo_messaging.rpc.client.RemoteError as e:
        LOG.error("Cannot check status of remote container!")
        _exit(1, docker, e)
    serv = messenger.Server(containers=CONTAINERS, docker_manager=docker_manager, slaves=SLAVES)
    try:
        serv.run()
    finally:
        _exit(0, docker)


if __name__ == '__main__':
    main()
