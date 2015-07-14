# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
from keystone import config
from keystone.contrib.moon.core import ConfigurationDriver
from keystone.contrib.moon.core import TenantDriver
# from keystone.contrib.moon.core import SuperExtensionDriver



CONF = config.CONF


class ConfigurationConnector(ConfigurationDriver):

    def __init__(self):
        super(ConfigurationConnector, self).__init__()

    def get_policy_templete_dict(self):
        # TODO (dthom)
        pass

    def get_aggregation_algorithm_dict(self):
        aggregation_algorithm_dict = dict()
        aggregation_algorithm_dict[uuid4()] = "all_true"
        return aggregation_algorithm_dict

    def get_sub_meta_rule_algorithm_dict(self):
        sub_meta_rule_algorithm_dict = dict()
        sub_meta_rule_algorithm_dict[uuid4()] = "inclusion"
        sub_meta_rule_algorithm_dict[uuid4()] = "comparison"
        return sub_meta_rule_algorithm_dict


class TenantConnector(TenantDriver):

    def get_tenant_dict(self):
        # TODO (dthom)
        pass

    def set_tenant(self, tenant_id, tenant_name, intra_authz_ext_id, intra_admin_ext_id):
        # TODO (dthom)
        pass


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
