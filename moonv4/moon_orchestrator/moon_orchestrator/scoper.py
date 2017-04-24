# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from oslo_config import cfg
from oslo_log import log as logging
import oslo_messaging
from moon_orchestrator.dockers import DockerBase

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "moon_orchestrator"


class Scoper(DockerBase):

    id = "moon_scoper"

    def __init__(self, conf_file="", docker=None, network_config=None):
        super(Scoper, self).__init__(
            name="moon_scoper",
            id=self.id,
            run_cmd=["python3", "-m", "moon_scoper"],
            host=CONF.scoper.host,
            conf_file=conf_file,
            docker=docker,
            network_config=network_config,
            tag=CONF.scoper.container
        )

    @staticmethod
    def get_status():
        transport = oslo_messaging.get_transport(CONF)
        target = oslo_messaging.Target(topic='scoper', version='1.0')
        client = oslo_messaging.RPCClient(transport, target)
        LOG.info("Calling Status on scoper component...")
        ret = client.call({"component_id": "scoper"}, 'get_status', args=None)
        LOG.info(ret)
        return ret
