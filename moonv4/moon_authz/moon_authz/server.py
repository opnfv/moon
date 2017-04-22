# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
from oslo_config import cfg
from oslo_log import log as logging
# cfg.CONF.register_cli_opt(cfg.StrOpt('function_type', positional=True,
#                                      help="The type of function managed by this component (example 'authz')."))
cfg.CONF.register_cli_opt(cfg.StrOpt('uuid', positional=True,
                                     help="The ID of the component managed here."))
cfg.CONF.register_cli_opt(cfg.StrOpt('keystone_project_id', positional=True,
                                     help="The ID of the component managed here."))
from moon_utilities import options  # noqa
from moon_authz.messenger import Server

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "moon_authz"

__CWD__ = os.path.dirname(os.path.abspath(__file__))


def main():
    component_id = CONF.uuid
    keystone_project_id = CONF.keystone_project_id
    # function_type = CONF.intra_extension_id.replace(component_id, "").strip('_')
    LOG.info("Starting server with IP {} on component {}".format(
        CONF.security_router.host, component_id))
    server = Server(component_id=component_id, keystone_project_id=keystone_project_id)
    server.run()


if __name__ == '__main__':
    main()
