# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import json
import logging
import hashlib
from glob import glob
from oslo_config import cfg
from moon_db.core import ConfigurationDriver

LOG = logging.getLogger("moon.db.driver.memory")
CONF = cfg.CONF


class ConfigurationConnector(object):

    def __init__(self, engine):
        super(ConfigurationConnector, self).__init__()
        self.policy_directory = CONF.policy_directory
        self.aggregation_algorithms_dict = dict()
        self.aggregation_algorithms_dict[hashlib.sha224("all_true".encode("utf-8")).hexdigest()[:32]] = \
            {'name': 'all_true', 'description': 'all rules must match'}
        self.aggregation_algorithms_dict[hashlib.sha224("one_true".encode("utf-8")).hexdigest()[:32]] = \
            {'name': 'one_true', 'description': 'only one rule has to match'}
        self.sub_meta_rule_algorithms_dict = dict()
        self.sub_meta_rule_algorithms_dict[hashlib.sha224("inclusion".encode("utf-8")).hexdigest()[:32]] = \
            {'name': 'inclusion', 'description': 'inclusion'}
        self.sub_meta_rule_algorithms_dict[hashlib.sha224("comparison".encode("utf-8")).hexdigest()[:32]] = \
            {'name': 'comparison', 'description': 'comparison'}

    def get_policy_templates_dict(self):
        """
        :return: {
            template_id1: {name: template_name, description: template_description},
            template_id2: {name: template_name, description: template_description},
            ...
            }
        """
        nodes = glob(os.path.join(self.policy_directory, "*"))
        LOG.info("get_policy_templates_dict {} {}".format(self.policy_directory, nodes))
        templates = dict()
        for node in nodes:
            try:
                metadata = json.load(open(os.path.join(node, "metadata.json")))
            except IOError:
                # Note (asteroide): it's not a true policy directory, so we forgive it
                continue
            templates[os.path.basename(node)] = dict()
            templates[os.path.basename(node)]["name"] = metadata["name"]
            templates[os.path.basename(node)]["description"] = metadata["description"]
        return templates

    def get_aggregation_algorithms_dict(self):
        return self.aggregation_algorithms_dict

    def get_sub_meta_rule_algorithms_dict(self):
        return self.sub_meta_rule_algorithms_dict
