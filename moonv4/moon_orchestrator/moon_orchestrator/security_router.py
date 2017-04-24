# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import json
import glob
import uuid
import shutil
from oslo_config import cfg
from oslo_log import log as logging
import oslo_messaging
from io import BytesIO
from docker import Client
from jinja2 import FileSystemLoader, Environment
from moon_orchestrator.dockers import DockerBase

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "moon_orchestrator"

__CWD__ = os.path.dirname(os.path.abspath(__file__))
# TODO (dthom): select the right template folder
TEMPLATES_FOLDER = os.path.join(__CWD__, "..", "conf", "dockers")


class SecurityRouter(DockerBase):

    id = "moon_router"

    def __init__(self, conf_file="", docker=None, network_config=None):
        super(SecurityRouter, self).__init__(
            name="moon_secrouter",
            id=self.id,
            run_cmd=["python3", "-m", "moon_secrouter"],
            host=CONF.security_router.host,
            conf_file=conf_file,
            docker=docker,
            network_config=network_config,
            tag=CONF.security_router.container
        )

    @staticmethod
    def get_status():
        transport = oslo_messaging.get_transport(CONF)
        target = oslo_messaging.Target(topic='security_router', version='1.0')
        client = oslo_messaging.RPCClient(transport, target)
        LOG.info("Calling Status on security_server...")
        ret = client.call({"component_id": "security_router"}, 'get_status', args=None)
        LOG.info(ret)
        return ret
