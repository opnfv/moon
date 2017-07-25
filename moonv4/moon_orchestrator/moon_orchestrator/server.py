# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import sys
import os
import hashlib
from oslo_log import log as logging
from docker import Client
import docker.errors as docker_errors
from moon_utilities import configuration, exceptions
from moon_orchestrator import messenger


LOG = logging.getLogger("moon.orchestrator")

CONTAINERS = {}
SLAVES = {}
docker_conf = configuration.get_configuration("docker")['docker']
docker = Client(base_url=docker_conf['url'])
LOG.info("docker_url={}".format(docker_conf['url']))
docker_network = docker_conf['network']


def kill_handler(signum, frame):
    _exit(0)


class DockerManager:

    def load(self, component, uuid=None, container_data=None):
        """Load a new docker mapping the component given

        :param component: the name of the component (policy or function)
        :param uuid: the uuid of the intra_extension linked to that component
        :return: the created component
        """
        component_id = component+"_"+hashlib.sha224(uuid.encode("utf-8")).hexdigest()
        plugins = configuration.get_plugins()
        if component in plugins.keys():
            components = configuration.get_components()
            configuration.add_component(
                name=component_id,
                uuid=component_id,
                port=configuration.increment_port(),
                bind="0.0.0.0",
                extra=container_data,
                container=plugins[component]['container']
            )
            _command = plugins[component]['command']
            try:
                _index = _command.index("<UUID>")
                _command[_index] = component_id
            except ValueError:
                pass
            self.run(component_id, environment={"UUID": component_id})
            CONTAINERS[component_id] = components.get(component_id)
            CONTAINERS[component_id]["running"] = True
            return CONTAINERS[component_id]

    def load_all_containers(self):
        LOG.info("Try to load all containers...")
        current_containers = [item["Names"][0] for item in docker.containers()]
        components = configuration.get_components()
        containers_not_running = []
        for c_name in (
                '/keystone',
                '/consul',
                '/db',
                '/messenger'
        ):
            if c_name not in current_containers:
                containers_not_running.append(c_name)
        if containers_not_running:
            raise exceptions.ContainerMissing(
                "Following containers are missing: {}".format(", ".join(containers_not_running)))
        for c_name in (
           '/interface',
           '/manager',
           '/router'):
            if c_name not in current_containers:
                LOG.info("Starting container {}...".format(c_name))
                self.run(c_name.strip("/"))
            else:
                LOG.info("Container {} already running...".format(c_name))
            CONTAINERS[c_name] = components.get(c_name.strip("/"))
            CONTAINERS[c_name]["running"] = True

    def run(self, name, environment=None):
        components = configuration.get_components()
        if name in components:
            image = components[name]['container']
            params = {
                'image': image,
                'name': name,
                'hostname': name,
                'detach': True,
                'host_config': docker.create_host_config(network_mode=docker_network)
            }
            if 'port' in components[name] and components[name]['port']:
                params["ports"] = [components[name]['port'], ]
                params["host_config"] = docker.create_host_config(
                    network_mode=docker_network,
                    port_bindings={components[name]['port']: components[name]['port']}
                )
            if environment:
                params["environment"] = environment
            container = docker.create_container(**params)
            docker.start(container=container.get('Id'))

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


def _exit(exit_number=0, error=None):
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
    LOG.info("Moon orchestrator: offline")

    # TODO (asteroide): put in the debug log
    if error:
        LOG.info(str(error))
    sys.exit(exit_number)


def __save_pid():
    try:
        open("/var/run/moon_orchestrator.pid", "w").write(str(os.getpid()))
    except PermissionError:
        LOG.warning("You don't have the right to write PID file in /var/run... Continuing anyway.")
        LOG.warning("Writing PID file in {}".format(os.getcwd()))
        open("./moon_orchestrator.pid", "w").write(str(os.getpid()))


def server():

    configuration.init_logging()
    conf = configuration.add_component("orchestrator", "orchestrator")
    LOG.info("Starting main server {}".format(conf["components/orchestrator"]["hostname"]))

    docker_manager = DockerManager()

    docker_manager.load_all_containers()
    serv = messenger.Server(containers=CONTAINERS, docker_manager=docker_manager, slaves=SLAVES)
    try:
        serv.run()
    finally:
        _exit(0)


def main():
    server()


if __name__ == '__main__':
    main()
