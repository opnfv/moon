# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import json
from oslo_config import cfg
from oslo_log import log as logging
from moon_db.core import IntraExtensionRootManager
from moon_db.core import ConfigurationManager

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Configuration(object):
    """
    Retrieve the global configuration.
    """

    __version__ = "0.1.0"

    def get_policy_templates(self, ctx, args):
        """List all policy templates

        :param ctx: {"id": "intra_extension_id"}
        :param args: {}
        :return: {
            "template_id": {
            "name": "name of the template",
            "description": "description of the template",
        }
        """
        templates = ConfigurationManager.get_policy_templates_dict(ctx["user_id"])
        return {"policy_templates": templates}

    def get_aggregation_algorithms(self, ctx, args):
        """List all aggregation algorithms

        :param ctx: {"id": "intra_extension_id"}
        :param args: {}
        :return: {
            "algorithm_id": {
                "name": "name of the algorithm",
                "description": "description of the algorithm",
            }
        }
        """
        return {'aggregation_algorithms': ConfigurationManager.get_aggregation_algorithms_dict(ctx["user_id"])}

    def get_sub_meta_rule_algorithms(self, ctx, args):
        """List all sub meta rule algorithms

        :param ctx: {"id": "intra_extension_id"}
        :param args: {}
        :return: {
            "algorithm_id": {
                "name": "name of the algorithm",
                "description": "description of the algorithm",
            }
        }
        """
        return {'sub_meta_rule_algorithms': ConfigurationManager.get_sub_meta_rule_algorithms_dict(ctx["user_id"])}
