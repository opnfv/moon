# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import time
from oslo_config import cfg
from oslo_log import log as logging
import oslo_messaging
from moon_orchestrator.dockers import DockerBase

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "moon_orchestrator"

__CWD__ = os.path.dirname(os.path.abspath(__file__))
# TODO (dthom): select the right template folder
TEMPLATES_FOLDER = os.path.join(__CWD__, "..", "conf", "dockers")


class SecurityManager(DockerBase):

    id = "moon_manager"
    __build = """RUN mkdir -p /etc/moon/
COPY conf /etc/moon/
ADD dist/{py_pkg}.tar.gz /root
WORKDIR /root/{py_pkg}
RUN pip3 install -r requirements.txt
RUN pip3 install .
"""

    def __init__(self, conf_file="", docker=None, network_config=None):
        self.id = "moon_manager"
        super(SecurityManager, self).__init__(
            name="moon_manager",
            run_cmd=["python3", "-m", "moon_manager"],
            conf_file=conf_file,
            docker=docker,
            network_config=network_config,
            build_cmd=self.__build,
            id=self.id,
            tag=CONF.security_manager.container
        )
        # note(asteroide): time to let the new docker boot
        time.sleep(3)
        self.get_status()

    def get_status(self):
        transport = oslo_messaging.get_transport(CONF)
        target = oslo_messaging.Target(topic=self.id, version='1.0')
        client = oslo_messaging.RPCClient(transport, target)
        LOG.info("Calling Status on {}".format(self.id))
        ret = client.call({"component_id": self.id}, 'get_status', args=None)
        LOG.info(ret)
        return ret
