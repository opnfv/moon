# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import json
import glob
import uuid
import shutil
import errno
from uuid import uuid4
from oslo_config import cfg
from oslo_log import log as logging
from jinja2 import FileSystemLoader, Environment
from moon_utilities.options import get_docker_template_dir

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "moon_orchestrator"

__CWD__ = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_FOLDER = get_docker_template_dir()


class DockerBase:

    docker = None
    image_id = None
    tag = 'moon/component'
    tmp_dir = os.path.join("/tmp", uuid.uuid4().hex)
    name = ""
    __build = """RUN mkdir -p /etc/moon/
COPY conf /etc/moon/
ADD dist/{py_pkg}.tar.gz /root
WORKDIR /root/{py_pkg}
RUN pip3 install --upgrade -r requirements.txt
RUN pip3 install --upgrade .
"""

    def __init__(self,
                 name,
                 run_cmd,
                 host=None,
                 build_cmd=None,
                 conf_file="",
                 id=None,
                 docker=None,
                 network_config=None,
                 tag="",
                 port=None
                 ):
        self.conf_file = conf_file
        self.docker = docker
        self.network_config = network_config
        self.name = name
        self.id = id if id else name + "_" + uuid4().hex
        self.tag = "moon/{}".format(name)
        self.build_cmd = build_cmd if build_cmd else self.__build
        self.run_cmd = run_cmd
        self.host = host
        self.docker_id = id
        self.port = port
        containers = self.docker.containers()
        if self.id not in map(lambda x: x['Id'], containers):
            self.create_container(tag)
            self.run_docker()
        else:
            LOG.info("Component {} already running...".format(name))

    def create_container(self, container=None):
        if not container:
            proxy = CONF.proxy
            if CONF.proxy:
                proxy = "ENV http_proxy {0}\nENV https_proxy {0}\n".format(CONF.proxy)
            run = self.build_cmd.format(
                py_pkg=self.__get_last_version_of_pkg(self.name).replace(".tar.gz", "").replace("dist/", ""),
                port=self.port
            )
            docker_str = self.__get_template().render(run=run, cmd=self.run_cmd, proxy=proxy)
            self.__create_tmp_dir(docker_str)
            self.create_docker(docker_str)
        else:
            self.tag = container

    def __create_tmp_dir(self, docker_str):
        try:
            os.mkdir(self.tmp_dir)
        except OSError as e:
            LOG.warning("Problem when creating temporary directory ({})".format(e))

        try:
            os.mkdir(os.path.join(self.tmp_dir, "dist"))
        except OSError as e:
            LOG.warning("Problem when creating temporary directory ({})".format(e))
        for _file in glob.glob("{}/*".format(CONF.dist_dir)):
            LOG.info("Copying {}".format(_file))
            shutil.copy(_file, os.path.join(self.tmp_dir, "dist"))

        try:
            # TODO: check the symbol link
            shutil.copytree(os.path.dirname(self.conf_file), os.path.join(self.tmp_dir, "conf"))
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(os.path.dirname(self.conf_file), os.path.join(self.tmp_dir, "conf"))
            elif exc.errno == errno.EEXIST:
                pass
            else:
                LOG.info("exc.errno = {}".format(exc.errno))
                raise

        open("{}/Dockerfile".format(self.tmp_dir), "w").write(docker_str)

    def __get_docker_network(self, name="moon"):
        if self.host:
            return self.docker.create_networking_config({
                name: self.docker.create_endpoint_config(
                    aliases=[self.id, ],
                    ipv4_address=self.host,
                )
            })
        else:
            return self.docker.create_networking_config({
                name: self.docker.create_endpoint_config(
                    aliases=[self.id, ]
                )
            })

    @staticmethod
    def __get_last_version_of_pkg(name):
        files = []
        for filename in glob.glob("{}/{}*".format(CONF.dist_dir, name)):
            files.append(filename)
        files.sort()
        try:
            return os.path.basename(files[-1])
        except Exception as e:
            LOG.error("__get_last_version_of_pkg {}/{}*".format(CONF.dist_dir, name))
            raise e

    def run_docker(self):
        LOG.info("run_docker hostname={}".format(self.id.replace("_", "-")))
        if self.port:
            host_config = self.docker.create_host_config(port_bindings={
                self.port: self.port
            })
        else:
            host_config = self.docker.create_host_config()

        output = self.docker.create_container(image=self.tag,
                                              command=list(self.run_cmd),
                                              hostname=str(self.id.replace("_", "-"))[:63],
                                              name=str(self.id),
                                              networking_config=self.__get_docker_network(),
                                              host_config=host_config
                                              )
        container_data = self.docker.inspect_container(output['Id'])
        name = container_data["Name"]
        LOG.info("Running container {} with ID {}".format(self.tag, output))
        LOG.info("output id = {}".format(output['Id']))
        self.docker.start(container=output['Id'])
        LOG.info("Running container output {}".format(self.docker.logs(
            container=name,
            # stdout=True,
            # stderr=True
        ).decode("utf-8")))
        self.name = name
        self.docker_id = output['Id']

    def create_docker(self, docker_str):
        # f = BytesIO(docker_str.encode('utf-8'))
        LOG.info("Building {}".format(self.tmp_dir))
        # TODO (dthom): halt on built errors (or emit a log)
        _output = self.docker.build(path=self.tmp_dir, rm=True, tag=self.tag)
        # _output = self.cli.build(fileobj=f, rm=True, tag=self.tag, stream=True)
        for line in _output:
            jline = json.loads(line.decode("utf-8"))
            if "stream" in jline:
                LOG.info("\033[33m" + jline["stream"].strip() + "\033[m")
            else:
                LOG.info("\033[33m" + str(jline).strip() + "\033[m")
        else:
            LOG.debug(_output)
        LOG.info("tag = {}".format(self.tag))
        LOG.info("images = {}".format(self.docker.images(name=self.tag)))
        self.image_id = self.docker.images(name=self.tag)[0]['Id']

    @staticmethod
    def __get_template(filename="template.dockerfile"):
        simple_loader = FileSystemLoader(TEMPLATES_FOLDER)
        env = Environment(loader=simple_loader)
        return env.get_template(filename)
