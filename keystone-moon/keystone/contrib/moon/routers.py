# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""WSGI Routers for the Moon service."""

from keystone.contrib.moon import controllers
from keystone.common import wsgi
from oslo_log import log

LOG = log.getLogger(__name__)


class Routers(wsgi.ComposableRouter):
    """API Endpoints for the Moon extension.
    """

    PATH_PREFIX = ''

    def __init__(self, description):
        self.description = description

    @staticmethod
    def _get_rel(component):
        return 'http://docs.openstack.org/api/openstack-authz/3/param/{}'.format(component)

    @staticmethod
    def _get_path(component):
        return 'http://docs.openstack.org/api/openstack-authz/3/param/{}'.format(component)

    def add_routes(self, mapper):
        # Controllers creation
        authz_controller = controllers.Authz_v3()
        configuration_controller = controllers.Configuration()
        intra_ext_controller = controllers.IntraExtensions()
        tenants_controller = controllers.Tenants()
        logs_controller = controllers.Logs()
        auth_controller = controllers.MoonAuth()
        inter_ext_controller = controllers.InterExtensions()

        # Configuration route
        mapper.connect(
            self.PATH_PREFIX+'/configuration/templates',
            controller=configuration_controller,
            action='get_policy_templates',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/configuration/aggregation_algorithms',
            controller=configuration_controller,
            action='get_aggregation_algorithms',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/configuration/sub_meta_rule_algorithms',
            controller=configuration_controller,
            action='get_sub_meta_rule_algorithms',
            conditions=dict(method=['GET']))

        # Tenants route
        mapper.connect(
            self.PATH_PREFIX+'/tenants',
            controller=tenants_controller,
            action='get_tenants',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/tenants',
            controller=tenants_controller,
            action='add_tenant',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/tenants/{tenant_id}',
            controller=tenants_controller,
            action='get_tenant',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/tenants/{tenant_id}',
            controller=tenants_controller,
            action='del_tenant',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/tenants/{tenant_id}',
            controller=tenants_controller,
            action='set_tenant',
            conditions=dict(method=['POST']))

        # Authz route
        mapper.connect(
            self.PATH_PREFIX+'/authz/{tenant_id}/{subject_k_id}/{object_name}/{action_name}',
            controller=authz_controller,
            action='get_authz',
            conditions=dict(method=['GET']))

        # IntraExtensions/Admin route
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/init',
            controller=intra_ext_controller,
            action='load_root_intra_extension',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions',
            controller=intra_ext_controller,
            action='get_intra_extensions',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions',
            controller=intra_ext_controller,
            action='add_intra_extension',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}',
            controller=intra_ext_controller,
            action='get_intra_extension',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}',
            controller=intra_ext_controller,
            action='set_intra_extension',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}',
            controller=intra_ext_controller,
            action='del_intra_extension',
            conditions=dict(method=['DELETE']))

        # Metadata route
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_categories',
            controller=intra_ext_controller,
            action='get_subject_categories',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_categories',
            controller=intra_ext_controller,
            action='add_subject_category',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_categories/{subject_category_id}',
            controller=intra_ext_controller,
            action='get_subject_category',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_categories/{subject_category_id}',
            controller=intra_ext_controller,
            action='del_subject_category',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_categories/{subject_category_id}',
            controller=intra_ext_controller,
            action='set_subject_category',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_categories',
            controller=intra_ext_controller,
            action='get_object_categories',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_categories',
            controller=intra_ext_controller,
            action='add_object_category',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_categories/{object_category_id}',
            controller=intra_ext_controller,
            action='get_object_category',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_categories/{object_category_id}',
            controller=intra_ext_controller,
            action='del_object_category',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_categories/{object_category_id}',
            controller=intra_ext_controller,
            action='set_object_category',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_categories',
            controller=intra_ext_controller,
            action='get_action_categories',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_categories',
            controller=intra_ext_controller,
            action='add_action_category',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_categories/{action_category_id}',
            controller=intra_ext_controller,
            action='get_action_category',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_categories/{action_category_id}',
            controller=intra_ext_controller,
            action='del_action_category',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_categories/{action_category_id}',
            controller=intra_ext_controller,
            action='set_action_category',
            conditions=dict(method=['POST']))

        # Perimeter route
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subjects',
            controller=intra_ext_controller,
            action='get_subjects',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subjects',
            controller=intra_ext_controller,
            action='add_subject',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subjects/{subject_id}',
            controller=intra_ext_controller,
            action='get_subject',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subjects/{subject_id}',
            controller=intra_ext_controller,
            action='del_subject',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subjects/{subject_id}',
            controller=intra_ext_controller,
            action='set_subject',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/objects',
            controller=intra_ext_controller,
            action='get_objects',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/objects',
            controller=intra_ext_controller,
            action='add_object',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/objects/{object_id}',
            controller=intra_ext_controller,
            action='get_object',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/objects/{object_id}',
            controller=intra_ext_controller,
            action='del_object',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/objects/{object_id}',
            controller=intra_ext_controller,
            action='set_object',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/actions',
            controller=intra_ext_controller,
            action='get_actions',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/actions',
            controller=intra_ext_controller,
            action='add_action',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/actions/{action_id}',
            controller=intra_ext_controller,
            action='get_action',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/actions/{action_id}',
            controller=intra_ext_controller,
            action='del_action',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/actions/{action_id}',
            controller=intra_ext_controller,
            action='set_action',
            conditions=dict(method=['POST']))

        # Scope route
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_scopes/{subject_category_id}',
            controller=intra_ext_controller,
            action='get_subject_scopes',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_scopes/{subject_category_id}',
            controller=intra_ext_controller,
            action='add_subject_scope',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_scopes/{subject_category_id}/{subject_scope_id}',
            controller=intra_ext_controller,
            action='get_subject_scope',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_scopes/{subject_category_id}/{subject_scope_id}',
            controller=intra_ext_controller,
            action='del_subject_scope',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_scopes/{subject_category_id}/{subject_scope_id}',
            controller=intra_ext_controller,
            action='set_subject_scope',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_scopes/{object_category_id}',
            controller=intra_ext_controller,
            action='get_object_scopes',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_scopes/{object_category_id}',
            controller=intra_ext_controller,
            action='add_object_scope',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_scopes/{object_category_id}/{object_scope_id}',
            controller=intra_ext_controller,
            action='get_object_scope',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_scopes/{object_category_id}/{object_scope_id}',
            controller=intra_ext_controller,
            action='del_object_scope',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_scopes/{object_category_id}/{object_scope_id}',
            controller=intra_ext_controller,
            action='set_object_scope',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_scopes/{action_category_id}',
            controller=intra_ext_controller,
            action='get_action_scopes',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_scopes/{action_category_id}',
            controller=intra_ext_controller,
            action='add_action_scope',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_scopes/{action_category_id}/{action_scope_id}',
            controller=intra_ext_controller,
            action='get_action_scope',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_scopes/{action_category_id}/{action_scope_id}',
            controller=intra_ext_controller,
            action='del_action_scope',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_scopes/{action_category_id}/{action_scope_id}',
            controller=intra_ext_controller,
            action='set_action_scope',
            conditions=dict(method=['POST']))

        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_assignments',
            controller=intra_ext_controller,
            action='add_subject_assignment',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/'
                                  'subject_assignments/{subject_id}/{subject_category_id}',
            controller=intra_ext_controller,
            action='get_subject_assignment',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/'
                                  'subject_assignments/{subject_id}/{subject_category_id}/{subject_scope_id}',
            controller=intra_ext_controller,
            action='del_subject_assignment',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_assignments',
            controller=intra_ext_controller,
            action='add_object_assignment',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/'
                                  'object_assignments/{object_id}/{object_category_id}',
            controller=intra_ext_controller,
            action='get_object_assignment',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/'
                                  'object_assignments/{object_id}/{object_category_id}/{object_scope_id}',
            controller=intra_ext_controller,
            action='del_object_assignment',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_assignments',
            controller=intra_ext_controller,
            action='add_action_assignment',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/'
                                  'action_assignments/{action_id}/{action_category_id}',
            controller=intra_ext_controller,
            action='get_action_assignment',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/'
                                  'action_assignments/{action_id}/{action_category_id}/{action_scope_id}',
            controller=intra_ext_controller,
            action='del_action_assignment',
            conditions=dict(method=['DELETE']))

        # Metarule route
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/aggregation_algorithm',
            controller=intra_ext_controller,
            action='get_aggregation_algorithm',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/aggregation_algorithm',
            controller=intra_ext_controller,
            action='set_aggregation_algorithm',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/sub_meta_rules',
            controller=intra_ext_controller,
            action='get_sub_meta_rules',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/sub_meta_rules',
            controller=intra_ext_controller,
            action='add_sub_meta_rule',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/sub_meta_rules/{sub_meta_rule_id}',
            controller=intra_ext_controller,
            action='get_sub_meta_rule',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/sub_meta_rules/{sub_meta_rule_id}',
            controller=intra_ext_controller,
            action='del_sub_meta_rule',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/sub_meta_rules/{sub_meta_rule_id}',
            controller=intra_ext_controller,
            action='set_sub_meta_rule',
            conditions=dict(method=['POST']))

        # Rules route
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/rule/{sub_meta_rule_id}',
            controller=intra_ext_controller,
            action='get_rules',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/rule/{sub_meta_rule_id}',
            controller=intra_ext_controller,
            action='add_rule',
            conditions=dict(method=['POST']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/rule/{sub_meta_rule_id}/{rule_id}',
            controller=intra_ext_controller,
            action='get_rule',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/rule/{sub_meta_rule_id}/{rule_id}',
            controller=intra_ext_controller,
            action='del_rule',
            conditions=dict(method=['DELETE']))
        mapper.connect(
            self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/rule/{sub_meta_rule_id}/{rule_id}',
            controller=intra_ext_controller,
            action='set_rule',
            conditions=dict(method=['POST']))

        # Logs route
        mapper.connect(
            self.PATH_PREFIX+'/logs',
            controller=logs_controller,
            action='get_logs',
            conditions=dict(method=['GET']))
        mapper.connect(
            self.PATH_PREFIX+'/logs/{options}',
            controller=logs_controller,
            action='get_logs',
            conditions=dict(method=['GET']))

        # Auth route
        mapper.connect(
            self.PATH_PREFIX+'/auth/tokens',
            controller=auth_controller,
            action='get_token',
            conditions=dict(method=['POST']))

        # InterExtensions route
        # mapper.connect(
        #     controller=inter_ext_controller,
        #     self.PATH_PREFIX+'/inter_extensions',
        #     action='get_inter_extensions',
        #     action='create_inter_extension',
        #     rel=self._get_rel('inter_extensions'),
        #     path_vars={})
        # mapper.connect(
        #     controller=inter_ext_controller,
        #     self.PATH_PREFIX+'/inter_extensions/{inter_extension_id}',
        #     action='get_inter_extension',
        #     action='delete_inter_extension',
        #     rel=self._get_rel('inter_extensions'),
        #     path_vars={
        #         'inter_extension_id': self._get_path('inter_extensions'),
        #     })
