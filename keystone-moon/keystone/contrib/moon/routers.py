# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""WSGI Routers for the Moon service."""

from keystone.contrib.moon import controllers
from keystone.common import wsgi


class Routers(wsgi.RoutersBase):
    """API Endpoints for the Moon extension.
    """

    PATH_PREFIX = '/OS-MOON'

    @staticmethod
    def _get_rel(component):
        return 'http://docs.openstack.org/api/openstack-authz/3/param/{}'.format(component)

    @staticmethod
    def _get_path(component):
        return 'http://docs.openstack.org/api/openstack-authz/3/param/{}'.format(component)

    def append_v3_routers(self, mapper, routers):
        # Controllers creation
        authz_controller = controllers.Authz_v3()
        configuration_controller = controllers.Configuration()
        intra_ext_controller = controllers.IntraExtensions()
        tenants_controller = controllers.Tenants()
        logs_controller = controllers.Logs()
        inter_ext_controller = controllers.InterExtensions()

        # Authz route
        self._add_resource(
            mapper, authz_controller,
            path=self.PATH_PREFIX+'/authz/{tenant_id}/{subject_id}/{object_id}/{action_id}',
            get_action='get_authz',
            rel=self._get_rel('authz'),
            path_vars={
                'tenant_id': self._get_path('tenants'),
                'subject_id': self._get_path('subjects'),
                'object_id': self._get_path('objects'),
                'action_id': self._get_path('actions'),
            })

        # Configuration route
        self._add_resource(
            mapper, configuration_controller,
            path=self.PATH_PREFIX+'/configuration/templetes',
            get_action='get_templetes',
            rel=self._get_rel('templetes'),
            path_vars={})
        self._add_resource(
            mapper, configuration_controller,
            path=self.PATH_PREFIX+'/configuration/aggregation_algorithms',
            get_action='get_aggregation_algorithms',
            rel=self._get_rel('aggregation_algorithms'),
            path_vars={})
        self._add_resource(
            mapper, configuration_controller,
            path=self.PATH_PREFIX+'/configuration/sub_meta_rule_relations',
            get_action='get_sub_meta_rule_algorithms',
            rel=self._get_rel('sub_meta_rule_algorithms'),
            path_vars={})

        # IntraExtensions route
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions',
            get_action='get_intra_extensions',
            post_action='add_intra_extension',
            rel=self._get_rel('intra_extensions'),
            path_vars={})
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}',
            get_action='get_intra_extension',
            delete_action='del_intra_extension',
            rel=self._get_rel('intra_extensions'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })

        # Metadata route
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_categories',
            get_action='get_subject_categories',
            post_action='add_subject_category',
            rel=self._get_rel('subject_categories'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_categories/{subject_category_id}',
            get_action='get_subject_category',
            delete_action='del_subject_category',
            rel=self._get_rel('subject_categories'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_categories',
            get_action='get_object_categories',
            post_action='add_object_category',
            rel=self._get_rel('object_categories'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_categories/{object_category_id}',
            get_action='get_object_category',
            delete_action='del_object_category',
            rel=self._get_rel('object_categories'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_categories',
            get_action='get_action_categories',
            post_action='add_action_category',
            rel=self._get_rel('action_categories'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_categories/{action_category_id}',
            get_action='get_action_category',
            delete_action='del_action_category',
            rel=self._get_rel('action_categories'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })

        # Perimeter route
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subjects',
            get_action='get_subjects',
            post_action='add_subject',
            rel=self._get_rel('subjects'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subjects/{subject_id}',
            get_action='get_subject',
            delete_action='del_subject',
            rel=self._get_rel('subjects'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/objects',
            get_action='get_objects',
            post_action='add_object',
            rel=self._get_rel('subjects'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/objects/{object_id}',
            get_action='get_object',
            delete_action='del_object',
            rel=self._get_rel('objects'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/actions',
            get_action='get_actions',
            post_action='add_action',
            rel=self._get_rel('actions'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/actions/{action_id}',
            get_action='get_action',
            delete_action='del_action',
            rel=self._get_rel('actions'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })

        # Scope route
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_category_scopes/{subject_category_id}',
            get_action='get_subject_category_scopes',
            post_action='add_subject_category_scope',
            rel=self._get_rel('subject_category_scope'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_category_scopes/{subject_category_id}/{subject_category_scope_id}',
            get_action='get_subject_category_scope',
            delete_action='del_subject_category_scope',
            rel=self._get_rel('subject_category_scope'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_category_scopes/{object_category_id}',
            get_action='get_object_category_scopes',
            post_action='add_object_category_scope',
            rel=self._get_rel('object_category_scope'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_category_scopes/{object_category_id}/{object_category_scope_id}',
            get_action='get_object_category_scope',
            delete_action='del_object_category_scope',
            rel=self._get_rel('object_category_scope'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_category_scopes/{action_category_id}',
            get_action='get_action_category_scopes',
            post_action='add_action_category_scope',
            rel=self._get_rel('action_category_scope'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_category_scopes/{action_category_id}/{action_category_scope_id}',
            get_action='get_action_category_scope',
            delete_action='del_action_category_scope',
            rel=self._get_rel('action_category_scope'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })

        # Assignment route
        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_assignments/{subject_id}',
            get_action='get_subject_assignments',
            rel=self._get_rel('subject_assignments'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/subject_assignments',
            post_action='add_subject_assignment',
            rel=self._get_rel('subject_assignments'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/'
                                  'subject_assignments/{subject_id}/{subject_category_id}/{subject_category_scope_id}',
            delete_action='del_subject_assignment',
            rel=self._get_rel('subject_assignments'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_assignments/{object_id}',
            get_action='get_object_assignments',
            rel=self._get_rel('object_assignments'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/object_assignments',
            post_action='add_object_assignment',
            rel=self._get_rel('object_assignments'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/'
                                  'object_assignments/{object_id}/{object_category}/{object_category_scope}',
            delete_action='del_object_assignment',
            rel=self._get_rel('object_assignments'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_assignments/{action_id}',
            get_action='get_action_assignments',
            rel=self._get_rel('action_assignments'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/action_assignments',
            post_action='add_action_assignment',
            rel=self._get_rel('action_assignments'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/'
                                  'action_assignments/{action_id}/{action_category}/{action_category_scope}',
            delete_action='del_action_assignment',
            rel=self._get_rel('action_assignments'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })

        # Metarule route
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/aggregation_algorithms',
            post_action='add_aggregation_algorithm',
            rel=self._get_rel('aggregation_algorithms'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/aggregation_algorithms/{aggregation_algorithm_id}',
            get_action='get_aggregation_algorithm',
            delete_action='del_aggregation_algorithm',
            rel=self._get_rel('aggregation_algorithms'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/sub_meta_rules',
            get_action='get_sub_meta_rules',
            post_action='add_sub_meta_rule',
            rel=self._get_rel('sub_meta_rules'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/sub_meta_rule/{sub_meta_rule_id}',
            get_action='get_sub_meta_rule',
            delete_action='del_sub_meta_rule',
            rel=self._get_rel('sub_meta_rules'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })

        # Rules route
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/rules/{sub_meta_rule_id}',
            get_action='get_rules',
            post_action='add_rule',
            rel=self._get_rel('rules'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })
        self._add_resource(
            mapper, intra_ext_controller,
            path=self.PATH_PREFIX+'/intra_extensions/{intra_extension_id}/rules/{sub_meta_rule_id}/{rule_id}',
            get_action='get_rule',
            delete_action='del_rule',
            rel=self._get_rel('rules'),
            path_vars={
                'intra_extension_id': self._get_path('intra_extensions'),
            })

        # Tenants route
        self._add_resource(
            mapper, tenants_controller,
            path=self.PATH_PREFIX+'/tenants',
            get_action='get_tenants',
            post_action='add_tenant',
            rel=self._get_rel('tenants'),
            path_vars={})
        self._add_resource(
            mapper, tenants_controller,
            path=self.PATH_PREFIX+'/tenant/{tenant_uuid}',
            get_action='get_tenant',
            delete_action='del_tenant',
            rel=self._get_rel('tenants'),
            path_vars={
                'tenant_uuid': self._get_path('tenants'),
            })

        # Logs route
        self._add_resource(
            mapper, logs_controller,
            path=self.PATH_PREFIX+'/logs',
            get_action='get_logs',
            rel=self._get_rel('logs'),
            path_vars={
            })
        self._add_resource(
            mapper, logs_controller,
            path=self.PATH_PREFIX+'/logs/{options}',
            get_action='get_logs',
            rel=self._get_rel('logs'),
            path_vars={
            })

        # InterExtensions route
        # self._add_resource(
        #     mapper, inter_ext_controller,
        #     path=self.PATH_PREFIX+'/inter_extensions',
        #     get_action='get_inter_extensions',
        #     post_action='create_inter_extension',
        #     rel=self._get_rel('inter_extensions'),
        #     path_vars={})
        # self._add_resource(
        #     mapper, inter_ext_controller,
        #     path=self.PATH_PREFIX+'/inter_extensions/{inter_extension_id}',
        #     get_action='get_inter_extension',
        #     delete_action='delete_inter_extension',
        #     rel=self._get_rel('inter_extensions'),
        #     path_vars={
        #         'inter_extension_id': self._get_path('inter_extensions'),
        #     })
