# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
from oslo_config import cfg
from oslo_log import log as logging
from moon_orchestrator.dockers import DockerBase

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "moon_orchestrator"

__CWD__ = os.path.dirname(os.path.abspath(__file__))
# TODO (dthom): select the right template folder
TEMPLATES_FOLDER = os.path.join(__CWD__, "..", "conf", "dockers")


class SecurityInterface(DockerBase):

    id = "moon_interface"
    __build = """RUN mkdir -p /etc/moon/
    COPY conf /etc/moon/
    ADD dist/{py_pkg}.tar.gz /root
    WORKDIR /root/{py_pkg}
    RUN pip3 install -r requirements.txt
    RUN pip3 install .
    EXPOSE {port}
    """

    def __init__(self, conf_file="", docker=None, network_config=None):
        super(SecurityInterface, self).__init__(
            name="moon_interface",
            id=self.id,
            run_cmd=["python3", "-m", "moon_interface"],
            host=CONF.interface.host,
            conf_file=conf_file,
            docker=docker,
            network_config=network_config,
            tag=CONF.interface.container,
            build_cmd=self.__build,
            port=CONF.interface.port
        )

