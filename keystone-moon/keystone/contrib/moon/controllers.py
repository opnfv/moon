# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from keystone.common import controller
from keystone.common import dependency
from keystone import config
from keystone.models import token_model
from keystone import exception
import os
import glob
from oslo_log import log

CONF = config.CONF
LOG = log.getLogger(__name__)


@dependency.requires('authz_api')
class Authz_v3(controller.V3Controller):

    def __init__(self):
        super(Authz_v3, self).__init__()

    @controller.protected()
    def get_authz(self, context, tenant_id, subject_id, object_id, action_id):
        # TODO (dthom): build the authz functionality
        try:
            _authz = self.authz_api.authz(tenant_id, subject_id, object_id, action_id)
        except exception.NotFound:
            _authz = True
        except:
            _authz = False
        return {"authz": _authz,
                "tenant_id": tenant_id,
                "subject_id": subject_id,
                "object_id": object_id,
                "action_id": action_id}


@dependency.requires('admin_api', 'authz_api')
class IntraExtensions(controller.V3Controller):
    collection_name = 'intra_extensions'
    member_name = 'intra_extension'

    def __init__(self):
        super(IntraExtensions, self).__init__()

    def _get_user_from_token(self, token_id):
        response = self.token_provider_api.validate_token(token_id)
        token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
        return token_ref['user']

    # IntraExtension functions
    @controller.protected()
    def get_intra_extensions(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        return {
            "intra_extensions":
                self.admin_api.get_intra_extension_list()
        }

    @controller.protected()
    def get_intra_extension(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        return {
            "intra_extensions":
                self.admin_api.get_intra_extension(uuid=kw['intra_extensions_id'])
        }

    @controller.protected()
    def create_intra_extension(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        return self.admin_api.load_intra_extension(kw)

    @controller.protected()
    def delete_intra_extension(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        if "intra_extensions_id" not in kw:
            raise exception.Error
        return self.admin_api.delete_intra_extension(kw["intra_extensions_id"])

    # Perimeter functions
    @controller.protected()
    def get_subjects(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_subject_dict(user, ie_uuid)

    @controller.protected()
    def add_subject(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        subject = kw["subject_id"]
        return self.admin_api.add_subject_dict(user, ie_uuid, subject)

    @controller.protected()
    def del_subject(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        subject = kw["subject_id"]
        return self.admin_api.del_subject(user, ie_uuid, subject)

    @controller.protected()
    def get_objects(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_object_dict(user, ie_uuid)

    @controller.protected()
    def add_object(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        object_id = kw["object_id"]
        return self.admin_api.add_object_dict(user, ie_uuid, object_id)

    @controller.protected()
    def del_object(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        object_id = kw["object_id"]
        return self.admin_api.del_object(user, ie_uuid, object_id)

    @controller.protected()
    def get_actions(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_action_dict(user, ie_uuid)

    @controller.protected()
    def add_action(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        action = kw["action_id"]
        return self.admin_api.add_action_dict(user, ie_uuid, action)

    @controller.protected()
    def del_action(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        action = kw["action_id"]
        return self.admin_api.del_action(user, ie_uuid, action)

    # Metadata functions
    @controller.protected()
    def get_subject_categories(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_subject_category_dict(user, ie_uuid)

    @controller.protected()
    def add_subject_category(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        subject_category = kw["subject_category_id"]
        return self.admin_api.add_subject_category_dict(user, ie_uuid, subject_category)

    @controller.protected()
    def del_subject_category(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        subject_category = kw["subject_category_id"]
        return self.admin_api.del_subject_category(user, ie_uuid, subject_category)

    @controller.protected()
    def get_object_categories(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_object_category_dict(user, ie_uuid)

    @controller.protected()
    def add_object_category(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        object_category = kw["object_category_id"]
        return self.admin_api.add_object_category_dict(user, ie_uuid, object_category)

    @controller.protected()
    def del_object_category(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        object_category = kw["object_category_id"]
        return self.admin_api.del_object_category(user, ie_uuid, object_category)

    @controller.protected()
    def get_action_categories(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_action_category_dict(user, ie_uuid)

    @controller.protected()
    def add_action_category(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        action_category = kw["action_category_id"]
        return self.admin_api.add_action_category_dict(user, ie_uuid, action_category)

    @controller.protected()
    def del_action_category(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        action_category = kw["action_category_id"]
        return self.admin_api.del_action_category(user, ie_uuid, action_category)

    # Scope functions
    @controller.protected()
    def get_subject_category_scope(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        category_id = kw["subject_category_id"]
        return self.admin_api.get_subject_category_scope_dict(user, ie_uuid, category_id)

    @controller.protected()
    def add_subject_category_scope(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        subject_category = kw["subject_category_id"]
        subject_category_scope = kw["subject_category_scope_id"]
        return self.admin_api.add_subject_category_scope_dict(
                    user,
                    ie_uuid,
                    subject_category,
                    subject_category_scope)

    @controller.protected()
    def del_subject_category_scope(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        subject_category = kw["subject_category_id"]
        subject_category_scope = kw["subject_category_scope_id"]
        return self.admin_api.del_subject_category_scope(
                    user,
                    ie_uuid,
                    subject_category,
                    subject_category_scope)

    @controller.protected()
    def get_object_category_scope(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        category_id = kw["object_category_id"]
        return self.admin_api.get_object_category_scope_dict(user, ie_uuid, category_id)

    @controller.protected()
    def add_object_category_scope(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        object_category = kw["object_category_id"]
        object_category_scope = kw["object_category_scope_id"]
        return self.admin_api.add_object_category_scope_dict(
                    user,
                    ie_uuid,
                    object_category,
                    object_category_scope)

    @controller.protected()
    def del_object_category_scope(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        object_category = kw["object_category_id"]
        object_category_scope = kw["object_category_scope_id"]
        return self.admin_api.del_object_category_scope(
                    user,
                    ie_uuid,
                    object_category,
                    object_category_scope)

    @controller.protected()
    def get_action_category_scope(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        category_id = kw["action_category_id"]
        return self.admin_api.get_action_category_scope_dict(user, ie_uuid, category_id)

    @controller.protected()
    def add_action_category_scope(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        action_category = kw["action_category_id"]
        action_category_scope = kw["action_category_scope_id"]
        return self.admin_api.add_action_category_scope_dict(
                    user,
                    ie_uuid,
                    action_category,
                    action_category_scope)

    @controller.protected()
    def del_action_category_scope(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        action_category = kw["action_category_id"]
        action_category_scope = kw["action_category_scope_id"]
        return self.admin_api.del_action_category_scope(
                    user,
                    ie_uuid,
                    action_category,
                    action_category_scope)

    # Assignment functions
    @controller.protected()
    def get_subject_assignments(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        subject_id = kw["subject_id"]
        return self.admin_api.get_subject_category_assignment_dict(user, ie_uuid, subject_id)

    @controller.protected()
    def add_subject_assignment(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        subject_id = kw["subject_id"]
        subject_category = kw["subject_category"]
        subject_category_scope = kw["subject_category_scope"]
        return self.admin_api.add_subject_category_assignment_dict(
                    user,
                    ie_uuid,
                    subject_id,
                    subject_category,
                    subject_category_scope)

    @controller.protected()
    def del_subject_assignment(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        subject_id = kw["subject_id"]
        subject_category = kw["subject_category"]
        subject_category_scope = kw["subject_category_scope"]
        return self.admin_api.del_subject_category_assignment(
                    user,
                    ie_uuid,
                    subject_id,
                    subject_category,
                    subject_category_scope)

    @controller.protected()
    def get_object_assignments(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        object_id = kw["object_id"]
        return self.admin_api.get_object_category_assignment_dict(user, ie_uuid, object_id)

    @controller.protected()
    def add_object_assignment(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        object_id = kw["object_id"]
        object_category = kw["object_category"]
        object_category_scope = kw["object_category_scope"]
        return self.admin_api.add_object_category_assignment_dict(
                    user,
                    ie_uuid,
                    object_id,
                    object_category,
                    object_category_scope)

    @controller.protected()
    def del_object_assignment(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        object_id = kw["object_id"]
        object_category = kw["object_category"]
        object_category_scope = kw["object_category_scope"]
        return self.admin_api.del_object_category_assignment(
                    user,
                    ie_uuid,
                    object_id,
                    object_category,
                    object_category_scope)

    @controller.protected()
    def get_action_assignments(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        action_id = kw["action_id"]
        return self.admin_api.get_action_category_assignment_dict(user, ie_uuid, action_id)

    @controller.protected()
    def add_action_assignment(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        action_id = kw["action_id"]
        action_category = kw["action_category"]
        action_category_scope = kw["action_category_scope"]
        return self.admin_api.add_action_category_assignment_dict(
                    user,
                    ie_uuid,
                    action_id,
                    action_category,
                    action_category_scope)

    @controller.protected()
    def del_action_assignment(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        action_id = kw["action_id"]
        action_category = kw["action_category"]
        action_category_scope = kw["action_category_scope"]
        return self.admin_api.del_object_category_assignment(
                    user,
                    ie_uuid,
                    action_id,
                    action_category,
                    action_category_scope)

    # Metarule functions
    @controller.protected()
    def get_aggregation_algorithms(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_aggregation_algorithms(user, ie_uuid)

    @controller.protected()
    def get_aggregation_algorithm(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_aggregation_algorithm(user, ie_uuid)

    @controller.protected()
    def set_aggregation_algorithm(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        aggregation_algorithm = kw["aggregation_algorithm"]
        return self.admin_api.set_aggregation_algorithm(user, ie_uuid, aggregation_algorithm)

    @controller.protected()
    def get_sub_meta_rule(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_sub_meta_rule(user, ie_uuid)

    @controller.protected()
    def set_sub_meta_rule(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw.pop("intra_extensions_id")
        # subject_categories = kw["subject_categories"]
        # action_categories = kw["action_categories"]
        # object_categories = kw["object_categories"]
        # relation = kw["relation"]
        # aggregation_algorithm = kw["aggregation_algorithm"]
        return self.admin_api.set_sub_meta_rule(
                    user,
                    ie_uuid,
                    kw)

    @controller.protected()
    def get_sub_meta_rule_relations(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_sub_meta_rule_relations(user, ie_uuid)

    # Rules functions
    @controller.protected()
    def get_sub_rules(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        return self.admin_api.get_sub_rules(user, ie_uuid)

    @controller.protected()
    def set_sub_rule(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        sub_rule = kw["rule"]
        relation = kw["relation"]
        return self.admin_api.set_sub_rule(user, ie_uuid, relation, sub_rule)

    @controller.protected()
    def del_sub_rule(self, context, **kw):
        user = self._get_user_from_token(context["token_id"])
        ie_uuid = kw["intra_extensions_id"]
        relation_name = kw["relation_name"]
        rule = kw["rule"]
        return self.admin_api.del_sub_rule(
                    user,
                    ie_uuid,
                    relation_name,
                    rule)


class AuthzPolicies(controller.V3Controller):
    collection_name = 'authz_policies'
    member_name = 'authz_policy'

    def __init__(self):
        super(AuthzPolicies, self).__init__()

    @controller.protected()
    def get_authz_policies(self, context, **kw):
        nodes = glob.glob(os.path.join(CONF.moon.policy_directory, "*"))
        return {
            "authz_policies":
                [os.path.basename(n) for n in nodes if os.path.isdir(n)]
        }


@dependency.requires('tenant_api', 'resource_api')
class Tenants(controller.V3Controller):

    def __init__(self):
        super(Tenants, self).__init__()

    def _get_user_from_token(self, token_id):
        response = self.token_provider_api.validate_token(token_id)
        token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
        return token_ref['user']

    @controller.protected()
    def get_tenants(self, context, **kw):
        # user = self._get_user_from_token(context["token_id"])
        return {
            "tenants":
                self.tenant_api.get_tenant_dict()
        }

    @controller.protected()
    def get_tenant(self, context, **kw):
        # user = self._get_user_from_token(context["token_id"])
        tenant_uuid = kw.get("tenant_uuid")
        return {
            "tenant":
                self.tenant_api.get_tenant_dict()[tenant_uuid]
        }

    @controller.protected()
    def set_tenant(self, context, **kw):
        # user = self._get_user_from_token(context["token_id"])
        tenant_uuid = kw.get("id")
        name = self.resource_api.get_project(tenant_uuid)["name"]
        authz = kw.get("authz")
        admin = kw.get("admin")
        self.tenant_api.set_tenant_dict(tenant_uuid, name, authz, admin)
        return {
            "tenant":
                self.tenant_api.get_tenant_dict()[tenant_uuid]
        }

    @controller.protected()
    def delete_tenant(self, context, **kw):
        # user = self._get_user_from_token(context["token_id"])
        tenant_uuid = kw.get("tenant_uuid")
        self.tenant_api.set_tenant_dict(tenant_uuid, None, None, None)


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
    #     user = self._get_user_from_token(context["token_id"])
    #     return {
    #         "inter_extensions":
    #             self.interextension_api.get_inter_extensions()
    #     }

    # @controller.protected()
    # def get_inter_extension(self, context, **kw):
    #     user = self._get_user_from_token(context["token_id"])
    #     return {
    #         "inter_extensions":
    #             self.interextension_api.get_inter_extension(uuid=kw['inter_extensions_id'])
    #     }

    # @controller.protected()
    # def create_inter_extension(self, context, **kw):
    #     user = self._get_user_from_token(context["token_id"])
    #     return self.interextension_api.create_inter_extension(kw)

    # @controller.protected()
    # def delete_inter_extension(self, context, **kw):
    #     user = self._get_user_from_token(context["token_id"])
    #     if "inter_extensions_id" not in kw:
    #         raise exception.Error
    #     return self.interextension_api.delete_inter_extension(kw["inter_extensions_id"])


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
        user = self._get_user_from_token(context["token_id"])
        options = kw.get("options", "")
        # FIXME (dthom): the authorization for get_logs must be done with an intra_extension
        #if self.authz_api.admin(user["name"], "logs", "read"):
        return {
            "logs":
                self.moonlog_api.get_logs(options)
        }

