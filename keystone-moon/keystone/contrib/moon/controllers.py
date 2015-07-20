# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from keystone.common import controller
from keystone.common import dependency
from keystone import config
from keystone.models import token_model
from keystone.contrib.moon.exception import *
import os
import glob
from oslo_log import log

CONF = config.CONF
LOG = log.getLogger(__name__)


@dependency.requires('configuration_api')
class Configuration(controller.V3Controller):
    collection_name = 'configurations'
    member_name = 'configuration'

    def __init__(self):
        super(Configuration, self).__init__()

    def _get_user_id_from_token(self, token_id):
        response = self.token_provider_api.validate_token(token_id)
        token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
        return token_ref.get('user')

    @controller.protected()
    def get_policy_templates(self, context, **kw):
        user_id = self._get_user_uuid_from_token(context.get("token_id"))
        return self.configuration_api_get_policy_templete_dict(user_id)

    @controller.protected()
    def get_aggregation_algorithms(self, context, **kw):
        """
        :param context:
        :param kw:
        :return: {aggregation_algorithm_id: description}
        """
        user_id = self._get_user_uuid_from_token(context.get("token_id"))
        return self.configuration_api.get_aggregation_algorithm_dict(user_id)

    @controller.protected()
    def get_sub_meta_rule_algorithms(self, context, **kw):
        """
        :param context:
        :param kw:
        :return: {sub_meta_rule_algorithm_id: description}
        """
        user_id = self._get_user_uuid_from_token(context.get("token_id"))
        return self.configuration_api.get_sub_meta_rule_algorithm_dict(user_id)


@dependency.requires('tenant_api', 'resource_api')
class Tenants(controller.V3Controller):

    def __init__(self):
        super(Tenants, self).__init__()

    def _get_user_id_from_token(self, token_id):
        response = self.token_provider_api.validate_token(token_id)
        token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
        return token_ref.get('user')

    @controller.protected()
    def get_tenants(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get("token_id"))
        return self.tenant_api.get_tenants_dict(user_id)

    @controller.protected()
    def add_tenant(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get("token_id"))
        # TODO: get tenant name from keystone
        tenant_dict = dict()
        tenant_dict['name'] = kw.get("name")
        tenant_dict['description'] = kw.get("description")
        tenant_dict['intra_authz_ext_id'] = kw.get("intra_authz_ext_id")
        tenant_dict['intra_admin_ext_id'] = kw.get("intra_admin_ext_id")
        return self.tenant_api.add_tenant_dict(user_id, tenant_dict)

    @controller.protected()
    def get_tenant(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        tenant_id = kw.get("tenant_id")
        return self.tenant_api.get_tenants_dict(user_id, tenant_id)

    @controller.protected()
    def del_tenant(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        tenant_id = kw.get("tenant_id")
        return self.tenant_api.del_tenant(user_id, tenant_id)

    def set_tenant(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        tenant_id = kw["id"]
        tenant_dict = dict()
        tenant_dict['name'] = kw.get("name")
        tenant_dict['description'] = kw.get("description")
        tenant_dict['intra_authz_ext_id'] = kw.get("intra_authz_ext_id")
        tenant_dict['intra_admin_ext_id'] = kw.get("intra_admin_ext_id")
        self.tenant_api.set_tenant_dict(user_id, tenant_id, tenant_dict)


@dependency.requires('authz_api')
class Authz_v3(controller.V3Controller):

    def __init__(self):
        super(Authz_v3, self).__init__()

    @controller.protected()
    def get_authz(self, context, tenant_name, subject_name, object_name, action_name):
        try:
            return self.authz_api.authz(tenant_name, subject_name, object_name, action_name)
        except:
            return False


@dependency.requires('admin_api', 'authz_api')
class IntraExtensions(controller.V3Controller):
    collection_name = 'intra_extensions'
    member_name = 'intra_extension'

    def __init__(self):
        super(IntraExtensions, self).__init__()

    def _get_user_id_from_token(self, token_id):
        response = self.token_provider_api.validate_token(token_id)
        token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
        return token_ref['user']

    # IntraExtension functions
    @controller.protected()
    def get_intra_extensions(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        return self.admin_api.get_intra_extensions_dict(user_id)

    @controller.protected()
    def add_intra_extension(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        intra_extension_dict = dict()
        intra_extension_dict["intra_extension_name"] = kw.get("intra_extension_name", dict())
        intra_extension_dict["subject_categories"] = kw.get("subject_categories", dict())
        intra_extension_dict["object_categories"] = kw.get("object_categories", dict())
        intra_extension_dict["action_categories"] = kw.get("action_categories", dict())
        intra_extension_dict["subjects"] = kw.get("subjects", dict())
        intra_extension_dict["objects"] = kw.get("objects", dict())
        intra_extension_dict["actions"] = kw.get("actions", dict())
        intra_extension_dict["subject_category_scopes"] = kw.get("subject_category_scopes", dict())
        intra_extension_dict["object_category_scopes"] = kw.get("object_category_scopes", dict())
        intra_extension_dict["action_category_scopes"] = kw.get("action_category_scopes", dict())
        intra_extension_dict["subject_assignments"] = kw.get("subject_assignments", dict())
        intra_extension_dict["object_assignments"] = kw.get("object_assignments", dict())
        intra_extension_dict["action_assignments"] = kw.get("action_assignments", dict())
        intra_extension_dict["aggregation_algorithm"] = kw.get("aggregation_algorithm", dict())
        intra_extension_dict["sub_meta_rules"] = kw.get("sub_meta_rules", dict())
        intra_extension_dict["rules"] = kw.get("rules", dict())
        return self.admin_api.load_intra_extension_dict(user_id, intra_extension_dict)

    @controller.protected()
    def get_intra_extension_dict(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        return self.admin_api.get_intra_extensions_dict(user_id)[ie_id]

    @controller.protected()
    def del_intra_extension(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        if "ie_id" not in kw:
            raise IntraExtensionUnknown
        ie_id = kw.get('intra_extension_id', None)
        self.admin_api.del_intra_extension(user_id, ie_id)

    @controller.protected()
    def set_intra_extension(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        if "ie_id" not in kw:
            raise IntraExtensionUnknown
        ie_id = kw.get('intra_extension_id', None)
        self.admin_api.set_intra_extension(user_id, ie_id)

    # Metadata functions
    @controller.protected()
    def get_subject_categories(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        return self.admin_api.get_subject_category_dict(user_id, ie_id)

    @controller.protected()
    def add_subject_category(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        subject_category_name = kw.get("subject_category_name", None)
        return self.admin_api.add_subject_category(user_id, ie_id, subject_category_name)

    @controller.protected()
    def get_subject_category(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        subject_category_id = kw.get("subject_category_id", None)
        return self.admin_api.get_subject_category_dict(user_id, ie_id)[subject_category_id]

    @controller.protected()
    def del_subject_category(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        subject_category_id = kw["subject_category_id"]
        return self.admin_api.del_subject_category(user_id, ie_id, subject_category_id)

    @controller.protected()
    def get_object_categories(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        return self.admin_api.get_object_category_dict(user_id, ie_id)

    @controller.protected()
    def add_object_category(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        object_category_name = kw["object_category_name"]
        return self.admin_api.add_object_category(user_id, ie_id, object_category_name)

    @controller.protected()
    def get_object_category(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        object_category_id = kw["object_category_id"]
        return self.admin_api.get_object_category_dict(user_id, ie_id)[object_category_id]

    @controller.protected()
    def del_object_category(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        object_category_id = kw["object_category_id"]
        return self.admin_api.del_object_category(user_id, ie_id, object_category_id)

    @controller.protected()
    def get_action_categories(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        return self.admin_api.get_action_category_dict(user_id, ie_id)

    @controller.protected()
    def add_action_category(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        action_category_name = kw["action_category_name"]
        return self.admin_api.add_action_category(user_id, ie_id, action_category_name)

    @controller.protected()
    def get_action_category(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        action_category_id = kw["action_category_id"]
        return self.admin_api.get_action_category_dict(user_id, ie_id)[action_category_id]

    @controller.protected()
    def del_action_category(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        action_category_id = kw["action_category_id"]
        return self.admin_api.del_action_category(user_id, ie_id, action_category_id)

    # Perimeter functions
    @controller.protected()
    def get_subjects(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        return self.admin_api.get_subject_dict(user_id, ie_id)

    @controller.protected()
    def add_subject(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        subject_name = kw["subject_name"]
        return self.admin_api.add_subject(user_id, ie_id, subject_name)

    @controller.protected()
    def get_subject(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        subject_id = kw["subject_id"]
        return self.admin_api.get_subject_dict(user_id, ie_id)[subject_id]

    @controller.protected()
    def del_subject(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get('intra_extension_id', None)
        subject_id = kw["subject_id"]
        return self.admin_api.del_subject(user_id, ie_id, subject_id)

    @controller.protected()
    def get_objects(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        return self.admin_api.get_object_dict(user_id, ie_id)

    @controller.protected()
    def add_object(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_name = kw["object_name"]
        return self.admin_api.add_object(user_id, ie_id, object_name)

    @controller.protected()
    def get_object(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_id = kw["object_id"]
        return self.admin_api.get_object_dict(user_id, ie_id)[object_id]

    @controller.protected()
    def del_object(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_id = kw["object_id"]
        return self.admin_api.del_object(user_id, ie_id, object_id)

    @controller.protected()
    def get_actions(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        return self.admin_api.get_action_dict(user_id, ie_id)

    @controller.protected()
    def add_action(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_name = kw["action_name"]
        return self.admin_api.add_action(user_id, ie_id, action_name)

    @controller.protected()
    def get_action(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_id = kw["action_id"]
        return self.admin_api.get_action_dict(user_id, ie_id)[action_id]

    @controller.protected()
    def del_action(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_id = kw["action_id"]
        return self.admin_api.del_action(user_id, ie_id, action_id)

    # Scope functions
    @controller.protected()
    def get_subject_scopes(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        subject_category_id = kw["subject_category_id"]
        return self.admin_api.get_subject_scope_dict(user_id, ie_id, subject_category_id)

    @controller.protected()
    def add_subject_scope(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        subject_category_id = kw["subject_category_id"]
        subject_scope_name = kw["subject_scope_name"]
        return self.admin_api.add_subject_scope(
            user_id,
            ie_id,
            subject_category_id,
            subject_scope_name)

    @controller.protected()
    def get_subject_scope(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        subject_category_id = kw["subject_category_id"]
        subject_scope_id = kw["subject_scope_id"]
        return self.admin_api.get_subject_scope(user_id, ie_id, subject_category_id, subject_scope_id)

    @controller.protected()
    def del_subject_scope(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        subject_category_id = kw["subject_category_id"]
        subject_scope_id = kw["subject_scope_id"]
        return self.admin_api.del_subject_scope(
            user_id,
            ie_id,
            subject_category_id,
            subject_scope_id)

    @controller.protected()
    def get_object_scopes(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_category_id = kw["object_category_id"]
        return self.admin_api.get_object_scope_dict(user_id, ie_id, object_category_id)

    @controller.protected()
    def add_object_scope(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_category_id = kw["object_category_id"]
        object_scope_name = kw["object_scope_name"]
        return self.admin_api.add_object_scope(
            user_id,
            ie_id,
            object_category_id,
            object_scope_name)

    @controller.protected()
    def get_object_scope(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_category_id = kw["object_category_id"]
        object_scope_id = kw["object_scope_id"]
        return self.admin_api.get_object_category_scope(user_id, ie_id, object_category_id, object_scope_id)

    @controller.protected()
    def del_object_scope(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_category_id = kw["object_category_id"]
        object_scope_id = kw["object_scope_id"]
        return self.admin_api.del_object_scope(
            user_id,
            ie_id,
            object_category_id,
            object_scope_id)

    @controller.protected()
    def get_action_scopes(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_category_id = kw["action_category_id"]
        return self.admin_api.get_action_scope_dict(user_id, ie_id, action_category_id)

    @controller.protected()
    def add_action_scope(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_category_id = kw["action_category_id"]
        action_scope_name = kw["action_scope_name"]
        return self.admin_api.add_action_scope(
            user_id,
            ie_id,
            action_category_id,
            action_scope_name)

    @controller.protected()
    def get_action_scope(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_category_id = kw["action_category_id"]
        action_scope_id = kw["action_scope_id"]
        return self.admin_api.get_action_scope_dict(user_id, ie_id, action_category_id)[action_scope_id]

    @controller.protected()
    def del_action_scope(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_category_id = kw["action_category_id"]
        action_scope_id = kw["action_scope_id"]
        return self.admin_api.del_action_scope(
            user_id,
            ie_id,
            action_category_id,
            action_scope_id)

    # Assignment functions
    @controller.protected()
    def get_subject_assignments(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        subject_id = kw["subject_id"]
        return self.admin_api.get_subject_assignment_dict(user_id, ie_id, subject_id)

    @controller.protected()
    def add_subject_assignment(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        subject_id = kw["subject_id"]
        subject_category_id = kw["subject_category_id"]
        subject_scope_id = kw["subject_scope_id"]
        return self.admin_api.add_subject_assignment(
            user_id,
            ie_id,
            subject_id,
            subject_category_id,
            subject_scope_id)

    @controller.protected()
    def get_subject_assignment(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        subject_id = kw["subject_id"]
        subject_category_id = kw["subject_category_id"]
        return self.admin_api.get_subject_assignment_dict(user_id, ie_id, subject_id, subject_category_id)

    @controller.protected()
    def del_subject_assignment(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        subject_id = kw["subject_id"]
        subject_category_id = kw["subject_category_id"]
        subject_scope_id = kw["subject_scope_id"]
        return self.admin_api.del_subject_assignment(
            user_id,
            ie_id,
            subject_id,
            subject_category_id,
            subject_scope_id)

    @controller.protected()
    def get_object_assignments(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_id = kw["object_id"]
        return self.admin_api.get_object_assignment_dict(user_id, ie_id, object_id)

    @controller.protected()
    def add_object_assignment(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_id = kw["object_id"]
        object_category_id = kw["object_category_id"]
        object_scope_id = kw["object_scope_id"]
        return self.admin_api.add_objecty_assignment(
            user_id,
            ie_id,
            object_id,
            object_category_id,
            object_scope_id)

    @controller.protected()
    def get_object_assignment(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_id = kw["object_id"]
        object_category_id = kw["object_category_id"]
        return self.admin_api.get_object_assignment_dict(user_id, ie_id, object_id, object_category_id)

    @controller.protected()
    def del_object_assignment(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        object_id = kw["object_id"]
        object_category_id = kw["object_category_id"]
        object_scope_id = kw["object_scope_id"]
        return self.admin_api.del_object_assignment(
            user_id,
            ie_id,
            object_id,
            object_category_id,
            object_scope_id)

    @controller.protected()
    def get_action_assignments(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_id = kw["action_id"]
        return self.admin_api.get_action_assignment_dict(user_id, ie_id, action_id)

    @controller.protected()
    def add_action_assignment(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_id = kw["action_id"]
        action_category_id = kw["action_category_id"]
        action_scope_id = kw["action_scope_id"]
        return self.admin_api.add_action_assignment(
            user_id,
            ie_id,
            action_id,
            action_category_id,
            action_scope_id)

    @controller.protected()
    def get_action_assignment(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_id = kw["action_id"]
        action_category_id = kw["action_category_id"]
        return self.admin_api.get_action_assignment_dict(user_id, ie_id, action_id, action_category_id)

    @controller.protected()
    def del_action_assignment(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        action_id = kw["action_id"]
        action_category_id = kw["action_category_id"]
        action_scope_id = kw["action_scope_id"]
        return self.admin_api.del_action_assignment(
            user_id,
            ie_id,
            action_id,
            action_category_id,
            action_scope_id)

    # Metarule functions
    @controller.protected()
    def add_aggregation_algorithm(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        aggregation_algorithm_id = kw["aggregation_algorithm_id"]
        return self.admin_api.add_aggregation_algorithm(
            user_id,
            ie_id,
            aggregation_algorithm_id)

    @controller.protected()
    def get_aggregation_algorithm(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        return self.admin_api.get_aggregation_algorithm(user_id, ie_id)

    @controller.protected()
    def del_aggregation_algorithm(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        aggregation_algorithm_id = kw["aggregation_algorithm_id"]
        return self.admin_api.del_aggregation_algorithm(
            user_id,
            ie_id,
            aggregation_algorithm_id)

    @controller.protected()
    def get_sub_meta_rules(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        return self.admin_api.get_sub_meta_rule_dict(user_id, ie_id)

    @controller.protected()
    def add_sub_meta_rule(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        sub_meta_rule_name = kw["sub_meta_rule_name"]
        subject_category_list = kw["subject_categories"]
        object_category_list = kw["object_categories"]
        action_category_list = kw["action_categories"]
        sub_meta_rule_algorithm = kw["sub_meta_rule_algorithm"]

        return self.admin_api.add_sub_meta_rule(
            user_id,
            ie_id,
            sub_meta_rule_name,
            subject_category_list,
            object_category_list,
            action_category_list,
            sub_meta_rule_algorithm
        )

    @controller.protected()
    def get_sub_meta_rule(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        sub_meta_rule_id = kw["sub_meta_rule_id"]
        return self.admin_api.get_sub_meta_rule(user_id, ie_id, sub_meta_rule_id)

    @controller.protected()
    def del_sub_meta_rule(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id")
        sub_meta_rule_id = kw["sub_meta_rule_id"]
        return self.admin_api.get_sub_meta_rule(user_id, ie_id, sub_meta_rule_id)

    # Rules functions
    @controller.protected()
    def get_rules(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        sub_meta_rule_id = kw["sub_meta_rule_id"]
        return self.admin_api.get_rule_dict(user_id, ie_id, sub_meta_rule_id)

    @controller.protected()
    def add_rule(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        sub_meta_rule_id = kw.get("sub_meta_rule_id")
        rule_list = list()
        subject_category_list = kw.get('subject_categories')
        object_category_list = kw.get('object_categories')
        action_category_list = kw.get('action_categories')
        rule_list = subject_category_list + object_category_list + action_category_list
        return self.admin_api.add_rule_list(user_id, ie_id, sub_meta_rule_id, rule_list)

    @controller.protected()
    def get_rule(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        sub_meta_rule_id = kw.get("sub_meta_rule_id")
        rule_id = kw.get("rule_id")
        return self.admin_api.get_rule(user_id, ie_id, sub_meta_rule_id, rule_id)

    @controller.protected()
    def del_rule(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        ie_id = kw.get("intra_extension_id", None)
        sub_meta_rule_id = kw["sub_meta_rule_id"]
        rule_id = kw["rule_id"]
        return self.admin_api.del_rule(user_id, ie_id, sub_meta_rule_id, rule_id)


@dependency.requires('authz_api')
class InterExtensions(controller.V3Controller):

    def __init__(self):
        super(InterExtensions, self).__init__()

    def _get_user_from_token(self, token_id):
        response = self.token_provider_api.validate_token(token_id)
        token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
        return token_ref['user']

    # @controller.protected()
    # def get_inter_extensions(self, context, **kw):
    #     user = self._get_user_from_token(context.get('token_id'))
    #     return {
    #         "inter_extensions":
    #             self.interextension_api.get_inter_extensions()
    #     }

    # @controller.protected()
    # def get_inter_extension(self, context, **kw):
    #     user = self._get_user_from_token(context.get('token_id'))
    #     return {
    #         "inter_extensions":
    #             self.interextension_api.get_inter_extension(uuid=kw['inter_extension_id'])
    #     }

    # @controller.protected()
    # def create_inter_extension(self, context, **kw):
    #     user = self._get_user_from_token(context.get('token_id'))
    #     return self.interextension_api.create_inter_extension(kw)

    # @controller.protected()
    # def delete_inter_extension(self, context, **kw):
    #     user = self._get_user_from_token(context.get('token_id'))
    #     if "inter_extension_id" not in kw:
    #         raise exception.Error
    #     return self.interextension_api.delete_inter_extension(kw["inter_extension_id"])


@dependency.requires('authz_api')
class SuperExtensions(controller.V3Controller):

    def __init__(self):
        super(SuperExtensions, self).__init__()


@dependency.requires('moonlog_api', 'authz_api')
class Logs(controller.V3Controller):

    def __init__(self):
        super(Logs, self).__init__()

    def _get_user_from_token(self, token_id):
        response = self.token_provider_api.validate_token(token_id)
        token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
        return token_ref['user']

    @controller.protected()
    def get_logs(self, context, **kw):
        user_id = self._get_user_id_from_token(context.get('token_id'))
        options = kw.get("options", "")
        # FIXME (dthom): the authorization for get_logs must be done with an intra_extension
        #if self.authz_api.admin(user["name"], "logs", "read"):
        return self.moonlog_api.get_logs(user_id, options)

