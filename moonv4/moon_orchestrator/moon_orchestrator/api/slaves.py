# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from oslo_config import cfg
from oslo_log import log as logging
from uuid import uuid4

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Slaves(object):
    """
    Manage containers.
    """

    __version__ = "0.1.0"

    def __init__(self, slaves):
        self.slaves = slaves

    def add_slave(self, ctx, args=None):
        """Add a new slave in the global list

        :param ctx: {
            "name": "name of the slave",
            "description": "description"
        }
        :param args: {}
        :return: {
            "uuid_of_the_slave": {
                "name": "name of the slave",
                "description": "description"
            }
        }
        """
        if "name" in ctx:
            for _id, _dict in self.slaves.items():
                if _dict['name'] == ctx['name']:
                    LOG.warning("A slave named {} already exists!".format(ctx['name']))
                    return {"slaves": {_id: _dict}}
            uuid = uuid4().hex
            ctx.pop("method")
            ctx.pop("call_master")
            self.slaves[uuid] = ctx
            return {"slaves": {uuid: ctx}}

    def get_slaves(self, ctx, args=None):
        """Get all the known slaves

        :param ctx: {}
        :param args: {}
        :return: {
            "uuid_of_the_slave": {
                "name": "name of the slave",
                "description": "description"
            }
        }
        """
        return {"slaves": self.slaves}

    def delete_slave(self, ctx, args=None):
        """Delete a previous slave in the global list

        :param ctx: {
            "id": "ID of the slave"
        }
        :param args: {}
        :return: None
        """
        if "id" in ctx:
            if ctx['id'] in self.slaves:
                self.slaves.pop(ctx['id'])
        return {"slaves": self.slaves}
