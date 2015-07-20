# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
from glob import glob
import os
from keystone import config
from keystone.contrib.moon.core import ConfigurationDriver
from keystone.contrib.moon.core import TenantDriver
# from keystone.contrib.moon.core import SuperExtensionDriver



CONF = config.CONF


class ConfigurationConnector(ConfigurationDriver):

    def __init__(self):
        super(ConfigurationConnector, self).__init__()
        self.aggregation_algorithm_dict = dict()
        self.aggregation_algorithm_dict[uuid4().hex] = "all_true"
        self.sub_meta_rule_algorithm_dict = dict()
        self.sub_meta_rule_algorithm_dict[uuid4().hex] = "inclusion"
        self.sub_meta_rule_algorithm_dict[uuid4().hex] = "comparison"

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

# class SuperExtensionConnector(SuperExtensionDriver):
#
#     def __init__(self):
#         super(SuperExtensionConnector, self).__init__()
#         # Super_Extension is loaded every time the server is started
#         self.__uuid = uuid4().hex
#         # self.__super_extension = Extension()
#         _policy_abs_dir = os.path.join(CONF.moon.super_extension_directory, 'policy')
#         # self.__super_extension.load_from_json(_policy_abs_dir)
#
#     def get_super_extensions(self):
#         return None
#
#     def admin(self, sub, obj, act):
#         # return self.__super_extension.authz(sub, obj, act)
#         return True
