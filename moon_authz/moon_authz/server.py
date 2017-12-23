# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
from oslo_log import log as logging
from moon_authz.http_server import HTTPServer as Server
from python_moonutilities import configuration

LOG = logging.getLogger("moon.server")
DOMAIN = "moon_authz"

__CWD__ = os.path.dirname(os.path.abspath(__file__))


def main():
    component_id = os.getenv("UUID")
    component_type = os.getenv("TYPE")
    tcp_port = os.getenv("PORT")
    pdp_id = os.getenv("PDP_ID")
    meta_rule_id = os.getenv("META_RULE_ID")
    keystone_project_id = os.getenv("KEYSTONE_PROJECT_ID")
    configuration.init_logging()
    LOG.info("component_type={}".format(component_type))
    conf = configuration.get_configuration("plugins/{}".format(component_type))
    conf["plugins/{}".format(component_type)]['id'] = component_id
    hostname = conf["plugins/{}".format(component_type)].get('hostname', component_id)
    port = conf["plugins/{}".format(component_type)].get('port', tcp_port)
    bind = conf["plugins/{}".format(component_type)].get('bind', "0.0.0.0")

    LOG.info("Starting server with IP {} on port {} bind to {}".format(hostname, port, bind))
    server = Server(
        host=bind,
        port=int(port),
        component_data={
            'component_id': component_id,
            'component_type': component_type,
            'pdp_id': pdp_id,
            'meta_rule_id': meta_rule_id,
            'keystone_project_id': keystone_project_id,
        }
    )
    return server


if __name__ == '__main__':
    main()
