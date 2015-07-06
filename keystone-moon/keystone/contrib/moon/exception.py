# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from keystone.common import dependency
from keystone.exception import Error
from keystone.i18n import _, _LW


class MoonErrorMetaClass(type):

    def __init__(cls, name, bases, dct):
        super(MoonErrorMetaClass, cls).__init__(name, bases, dct)
        cls.hierarchy += "/"+str(name)


@dependency.requires('moonlog_api')
class MoonError(Error):
    __metaclass__ = MoonErrorMetaClass
    hierarchy = ""
    message_format = _("There is an error requesting the Moon platform.")
    code = 400
    title = 'Moon Error'
    logger = "ERROR"

    def __del__(self):
        message = "{} ({})".format(self.hierarchy, self.message_format)
        if self.logger == "ERROR":
            self.moonlog_api.error(message)
        elif self.logger == "WARNING":
            self.moonlog_api.warning(message)
        elif self.logger == "CRITICAL":
            self.moonlog_api.critical(message)
        elif self.logger == "AUTHZ":
            self.moonlog_api.authz(self.hierarchy)
            self.moonlog_api.error(message)
        else:
            self.moonlog_api.info(message)


# Exceptions for Tenant


class TenantException(MoonError):
    message_format = _("There is an error requesting this tenant.")
    code = 400
    title = 'Tenant Error'
    logger = "ERROR"


class TenantListEmpty(TenantException):
    message_format = _("The tenant list mapping is empty, you must set the mapping first.")
    code = 400
    title = 'Tenant List Empty Error'
    logger = "WARNING"


class TenantNotFound(TenantException):
    message_format = _("The tenant UUID was not found.")
    code = 400
    title = 'Tenant UUID Not Found Error'


# Exceptions for IntraExtension


class IntraExtensionException(MoonError):
    message_format = _("There is an error requesting this IntraExtension.")
    code = 400
    title = 'Extension Error'


class IntraExtensionUnMapped(IntraExtensionException):
    message_format = _("The Extension is not mapped to a tenant.")
    code = 400
    title = 'Extension UUID Not Found Error'
    logger = "WARNING"


class IntraExtensionNotFound(IntraExtensionException):
    message_format = _("The Extension for that tenant is unknown.")
    code = 400
    title = 'Extension UUID Not Found Error'
    logger = "WARNING"


class IntraExtensionCreationError(IntraExtensionException):
    message_format = _("The arguments for the creation of this Extension were malformed.")
    code = 400
    title = 'Intra Extension Creation Error'


# Authz exceptions


class AuthzException(MoonError):
    message_format = _("There is an error requesting this Authz IntraExtension.")
    code = 400
    title = 'Authz Exception'
    logger = "AUTHZ"


class AuthzPerimeter(AuthzException):
    code = 400
    title = 'Perimeter Exception'


class AuthzScope(AuthzException):
    code = 400
    title = 'Scope Exception'


class AuthzMetadata(AuthzException):
    code = 400
    title = 'Metadata Exception'


class AuthzAssignment(AuthzException):
    code = 400
    title = 'Assignment Exception'


class AuthzRule(AuthzException):
    code = 400
    title = 'Rule Exception'


class SubjectUnknown(AuthzPerimeter):
    message_format = _("The given subject is unknown.")
    code = 400
    title = 'Subject Unknown'
    logger = "ERROR"


class ObjectUnknown(AuthzPerimeter):
    message_format = _("The given object is unknown.")
    code = 400
    title = 'Object Unknown'
    logger = "ERROR"


class ActionUnknown(AuthzPerimeter):
    message_format = _("The given action is unknown.")
    code = 400
    title = 'Action Unknown'
    logger = "ERROR"


class SubjectCategoryAssignmentOutOfScope(AuthzScope):
    message_format = _("The given subject category scope value is out of scope.")
    code = 400
    title = 'Subject Category Assignment Out Of Scope'
    logger = "WARNING"


class ActionCategoryAssignmentOutOfScope(AuthzScope):
    message_format = _("The given action category scope value is out of scope.")
    code = 400
    title = 'Action Category Assignment Out Of Scope'
    logger = "WARNING"


class ObjectCategoryAssignmentOutOfScope(AuthzScope):
    message_format = _("The given object category scope value is out of scope.")
    code = 400
    title = 'Object Category Assignment Out Of Scope'
    logger = "WARNING"


class SubjectCategoryAssignmentUnknown(AuthzAssignment):
    message_format = _("The given subject category assignment value is unknown.")
    code = 400
    title = 'Subject Category Assignment Unknown'
    logger = "ERROR"


class ObjectCategoryAssignmentUnknown(AuthzAssignment):
    message_format = _("The given object category assignment value is unknown.")
    code = 400
    title = 'Object Category Assignment Unknown'
    logger = "ERROR"


class ActionCategoryAssignmentUnknown(AuthzAssignment):
    message_format = _("The given action category assignment value is unknown.")
    code = 400
    title = 'Action Category Assignment Unknown'
    logger = "ERROR"


class RuleOKNotExisting(AuthzRule):
    message_format = _("The positive rule for that request doen't exist.")
    code = 400
    title = 'Rule OK Not Existing'
    logger = "WARNING"


class RuleKOExisting(AuthzRule):
    message_format = _("The request match a negative rule.")
    code = 400
    title = 'Rule KO Existing'
    logger = "ERROR"


class RuleUnknown(AuthzRule):
    message_format = _("The rule for that request doesn't exist.")
    code = 400
    title = 'Rule Unknown'
    logger = "ERROR"


# Admin exceptions


class AdminException(MoonError):
    message_format = _("There is an authorization error requesting this IntraExtension.")
    code = 403
    title = 'Admin Exception'
    logger = "AUTHZ"


class AdminPerimeter(AuthzException):
    title = 'Perimeter Exception'


class AdminScope(AuthzException):
    title = 'Scope Exception'


class AdminMetadata(AuthzException):
    title = 'Metadata Exception'


class AdminAssignment(AuthzException):
    title = 'Assignment Exception'


class AdminRule(AuthzException):
    title = 'Rule Exception'

class AdminMetaRule(AuthzException):
    title = 'MetaRule Exception'


class SubjectReadNotAuthorized(AdminPerimeter):
    title = 'Subject Read Not Authorized'


class SubjectAddNotAuthorized(AdminPerimeter):
    title = 'Subject Add Not Authorized'


class SubjectDelNotAuthorized(AdminPerimeter):
    title = 'Subject Del Not Authorized'


class ObjectReadNotAuthorized(AdminPerimeter):
    title = 'Object Read Not Authorized'


class ObjectAddNotAuthorized(AdminPerimeter):
    title = 'Object Add Not Authorized'


class ObjectDelNotAuthorized(AdminPerimeter):
    title = 'Object Del Not Authorized'


class ActionReadNotAuthorized(AdminPerimeter):
    title = 'Action Read Not Authorized'


class ActionAddNotAuthorized(AdminPerimeter):
    title = 'Action Add Not Authorized'


class ActionDelNotAuthorized(AdminPerimeter):
    title = 'Action Del Not Authorized'


class SubjectCategoryScopeReadNotAuthorized(AuthzException):
    title = 'Subject Category Scope Read Not Authorized'


class SubjectCategoryScopeAddNotAuthorized(AuthzException):
    title = 'Subject Category Scope Add Not Authorized'


class SubjectCategoryScopeDelNotAuthorized(AuthzException):
    title = 'Subject Category Scope Del Not Authorized'


class ObjectCategoryScopeReadNotAuthorized(AuthzException):
    title = 'Object Category Scope Read Not Authorized'


class ObjectCategoryScopeAddNotAuthorized(AuthzException):
    title = 'Object Category Scope Add Not Authorized'


class ObjectCategoryScopeDelNotAuthorized(AuthzException):
    title = 'Object Category Scope Del Not Authorized'


class ActionCategoryScopeReadNotAuthorized(AuthzException):
    title = 'Action Category Scope Read Not Authorized'


class ActionCategoryScopeAddNotAuthorized(AuthzException):
    title = 'Action Category Scope Add Not Authorized'


class ActionCategoryScopeDelNotAuthorized(AuthzException):
    title = 'Action Category Scope Del Not Authorized'


class SubjectCategoryReadNotAuthorized(AdminMetadata):
    title = 'Subject Category Read Not Authorized'
    logger = "AUTHZ"


class SubjectCategoryAddNotAuthorized(AdminMetadata):
    title = 'Subject Category Add Not Authorized'


class SubjectCategoryDelNotAuthorized(AdminMetadata):
    title = 'Subject Category Del Not Authorized'


class ObjectCategoryReadNotAuthorized(AdminMetadata):
    title = 'Object Category Read Not Authorized'


class ObjectCategoryAddNotAuthorized(AdminMetadata):
    title = 'Object Category Add Not Authorized'


class ObjectCategoryDelNotAuthorized(AdminMetadata):
    title = 'Object Category Del Not Authorized'


class ActionCategoryReadNotAuthorized(AdminMetadata):
    title = 'Action Category Read Not Authorized'


class ActionCategoryAddNotAuthorized(AdminMetadata):
    title = 'Action Category Add Not Authorized'


class ActionCategoryDelNotAuthorized(AdminMetadata):
    title = 'Action Category Del Not Authorized'


class SubjectCategoryAssignmentReadNotAuthorized(AdminAssignment):
    title = 'Subject Category Assignment Read Not Authorized'


class SubjectCategoryAssignmentAddNotAuthorized(AdminAssignment):
    title = 'Subject Category Assignment Add Not Authorized'


class SubjectCategoryAssignmentDelNotAuthorized(AdminAssignment):
    title = 'Subject Category Assignment Del Not Authorized'


class ObjectCategoryAssignmentReadNotAuthorized(AdminAssignment):
    title = 'Object Category Assignment Read Not Authorized'


class ObjectCategoryAssignmentAddNotAuthorized(AdminAssignment):
    title = 'Object Category Assignment Add Not Authorized'


class ObjectCategoryAssignmentDelNotAuthorized(AdminAssignment):
    title = 'Object Category Assignment Del Not Authorized'


class ActionCategoryAssignmentReadNotAuthorized(AdminAssignment):
    title = 'Action Category Assignment Read Not Authorized'


class ActionCategoryAssignmentAddNotAuthorized(AdminAssignment):
    title = 'Action Category Assignment Add Not Authorized'


class ActionCategoryAssignmentDelNotAuthorized(AdminAssignment):
    title = 'Action Category Assignment Del Not Authorized'


class RuleReadNotAuthorized(AdminRule):
    title = 'Rule Read Not Authorized'


class RuleAddNotAuthorized(AdminRule):
    title = 'Rule Add Not Authorized'


class RuleDelNotAuthorized(AdminRule):
    title = 'Rule Del Not Authorized'


class MetaRuleReadNotAuthorized(AdminRule):
    title = 'MetaRule Read Not Authorized'


class MetaRuleAddNotAuthorized(AdminRule):
    title = 'MetaRule Add Not Authorized'


class MetaRuleDelNotAuthorized(AdminRule):
    title = 'MetaRule Del Not Authorized'
