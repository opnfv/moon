# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
from glob import glob
import os
from keystone import config
from keystone.contrib.moon.core import ConfigurationDriver
# from keystone.contrib.moon.core import SuperExtensionDriver



CONF = config.CONF


class ConfigurationConnector(ConfigurationDriver):

    def __init__(self):
        super(ConfigurationConnector, self).__init__()
        self.aggregation_algorithm_dict = dict()
        self.aggregation_algorithm_dict[uuid4().hex] = {'name': 'all_true', 'description': 'all_true'}
        self.sub_meta_rule_algorithm_dict = dict()
        self.sub_meta_rule_algorithm_dict[uuid4().hex] = {'name': 'inclusion', 'description': 'inclusion'}
        self.sub_meta_rule_algorithm_dict[uuid4().hex] = {'name': 'comparison', 'description': 'comparison'}

    def get_policy_template_dict(self):
        nodes = glob(os.path.join(CONF.moon.policy_directory, "*"))
        return {
            "authz_templates":
                [os.path.basename(n) for n in nodes if os.path.isdir(n)]
        }

    def get_aggregation_algorithm_dict(self):
        return self.aggregation_algorithm_dict

    def get_sub_meta_rule_algorithm_dict(self):
        return self.sub_meta_rule_algorithm_dict