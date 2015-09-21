# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
from glob import glob
import os
import json
from keystone import config
from keystone.contrib.moon.core import ConfigurationDriver
from oslo_log import log
import hashlib

CONF = config.CONF
LOG = log.getLogger(__name__)


class ConfigurationConnector(ConfigurationDriver):

    def __init__(self):
        super(ConfigurationConnector, self).__init__()
        self.aggregation_algorithms_dict = dict()
        self.aggregation_algorithms_dict[hashlib.sha224("all_true").hexdigest()[:32]] = \
            {'name': 'all_true', 'description': 'all rules must match'}
        self.aggregation_algorithms_dict[hashlib.sha224("one_true").hexdigest()[:32]] = \
            {'name': 'one_true', 'description': 'only one rule has to match'}
        self.sub_meta_rule_algorithms_dict = dict()
        self.sub_meta_rule_algorithms_dict[uuid4().hex] = {'name': 'inclusion', 'description': 'inclusion'}
        self.sub_meta_rule_algorithms_dict[uuid4().hex] = {'name': 'comparison', 'description': 'comparison'}

    def get_policy_templates_dict(self):
        """
        :return: {
            template_id1: {name: template_name, description: template_description},
            template_id2: {name: template_name, description: template_description},
            ...
            }
        """
        nodes = glob(os.path.join(CONF.moon.policy_directory, "*"))
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
