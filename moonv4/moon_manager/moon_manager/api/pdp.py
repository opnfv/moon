# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import json
import copy
from uuid import uuid4
from oslo_log import log as logging
from oslo_config import cfg
from moon_utilities import exceptions
from moon_db.core import PDPManager
from moon_utilities.misc import get_uuid_from_name
from moon_utilities.security_functions import call

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class PDP(object):

    def __init__(self):
        self.manager = PDPManager

    def get_pdp(self, ctx, args=None):
        try:
            data = self.manager.get_pdp(user_id=ctx["user_id"], pdp_id=ctx.get("id"))
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"pdps": data}

    def add_pdp(self, ctx, args):
        try:
            data = self.manager.add_pdp(user_id=ctx["user_id"], pdp_id=None, value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"pdps": data}

    def delete_pdp(self, ctx, args):
        try:
            data = self.manager.delete_pdp(user_id=ctx["user_id"], pdp_id=ctx.get("id"))
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def update_pdp(self, ctx, args):
        try:
            data = self.manager.update_pdp(user_id=ctx["user_id"], pdp_id=ctx.get("id"), value=args)
            call("orchestrator", method="add_container",
                 ctx={"id": ctx.get("id"), "pipeline": data[ctx.get("id")]['security_pipeline']})
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"pdps": data}


