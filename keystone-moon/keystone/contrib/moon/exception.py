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


class TenantUnknown(TenantException):
    message_format = _("The tenant is unknown.")
    code = 400
    title = 'Tenant Unknown'
    logger = "ERROR"


class TenantAddedNameExisting(TenantException):
    message_format = _("The tenant name is existing.")
    code = 400
    title = 'Added Tenant Name Existing'
    logger = "ERROR"


class TenantNoIntraExtension(TenantException):
    message_format = _("The tenant has not intra_extension.")
    code = 400
    title = 'Tenant No Intra_Extension'
    logger = "ERROR"


class TenantNoIntraAuthzExtension(TenantNoIntraExtension):
    message_format = _("The tenant has not intra_admin_extension.")
    code = 400
    title = 'Tenant No Intra_Admin_Extension'
    logger = "ERROR"

# Exceptions for IntraExtension


class IntraExtensionException(MoonError):
    message_format = _("There is an error requesting this IntraExtension.")
    code = 400
    title = 'Extension Error'


class IntraExtensionUnknown(IntraExtensionException):
    message_format = _("The intra_extension is unknown.")
    code = 400
    title = 'Intra Extension Unknown'
    logger = "Error"


class RootExtensionUnknown(IntraExtensionUnknown):
    message_format = _("The root_extension is unknown.")
    code = 400
    title = 'Root Extension Unknown'
    logger = "Error"

class RootExtensionNotInitialized(IntraExtensionException):
    message_format = _("The root_extension is not initialized.")
    code = 400
    title = 'Root Extension Not Initialized'
    logger = "Error"


class IntraExtensionCreationError(IntraExtensionException):
    message_format = _("The arguments for the creation of this Extension were malformed.")
    code = 400
    title = 'Intra Extension Creation Error'


# Authz exceptions

class AuthzException(MoonError):
    message_format = _("There is an authorization error requesting this IntraExtension.")
    code = 403
    title = 'Authz Exception'
    logger = "AUTHZ"


# Admin exceptions

class AdminException(MoonError):
    message_format = _("There is an error requesting this Authz IntraExtension.")
    code = 400
    title = 'Authz Exception'
    logger = "AUTHZ"


class AdminMetaData(AdminException):
    code = 400
    title = 'Metadata Exception'


class AdminPerimeter(AdminException):
    code = 400
    title = 'Perimeter Exception'


class AdminScope(AdminException):
    code = 400
    title = 'Scope Exception'


class AdminAssignment(AdminException):
    code = 400
    title = 'Assignment Exception'


class AdminMetaRule(AdminException):
    code = 400
    title = 'Aggregation Algorithm Exception'


class AdminRule(AdminException):
    code = 400
    title = 'Rule Exception'


class SubjectCategoryNameExisting(AdminMetaData):
    message_format = _("The given subject category name is existing.")
    code = 400
    title = 'Subject Category Name Existing'
    logger = "ERROR"


class ObjectCategoryNameExisting(AdminMetaData):
    message_format = _("The given object category name is existing.")
    code = 400
    title = 'Object Category Name Existing'
    logger = "ERROR"


class ActionCategoryNameExisting(AdminMetaData):
    message_format = _("The given action category name is existing.")
    code = 400
    title = 'Action Category Name Existing'
    logger = "ERROR"


class SubjectCategoryUnknown(AdminMetaData):
    message_format = _("The given subject category is unknown.")
    code = 400
    title = 'Subject Category Unknown'
    logger = "ERROR"


class ObjectCategoryUnknown(AdminMetaData):
    message_format = _("The given object category is unknown.")
    code = 400
    title = 'Object Category Unknown'
    logger = "ERROR"


class ActionCategoryUnknown(AdminMetaData):
    message_format = _("The given action category is unknown.")
    code = 400
    title = 'Action Category Unknown'
    logger = "ERROR"


class SubjectUnknown(AdminPerimeter):
    message_format = _("The given subject is unknown.")
    code = 400
    title = 'Subject Unknown'
    logger = "ERROR"


class ObjectUnknown(AdminPerimeter):
    message_format = _("The given object is unknown.")
    code = 400
    title = 'Object Unknown'
    logger = "ERROR"


class ActionUnknown(AdminPerimeter):
    message_format = _("The given action is unknown.")
    code = 400
    title = 'Action Unknown'
    logger = "ERROR"


class SubjectNameExisting(AdminPerimeter):
    message_format = _("The given subject name is existing.")
    code = 400
    title = 'Subject Name Existing'
    logger = "ERROR"


class ObjectNameExisting(AdminPerimeter):
    message_format = _("The given object name is existing.")
    code = 400
    title = 'Object Name Existing'
    logger = "ERROR"


class ActionNameExisting(AdminPerimeter):
    message_format = _("The given action name is existing.")
    code = 400
    title = 'Action Name Existing'
    logger = "ERROR"


class ObjectsWriteNoAuthorized(AdminPerimeter):
    message_format = _("The modification on Objects is not authorized.")
    code = 400
    title = 'Objects Write No Authorized'
    logger = "AUTHZ"


class ActionsWriteNoAuthorized(AdminPerimeter):
    message_format = _("The modification on Actions is not authorized.")
    code = 400
    title = 'Actions Write No Authorized'
    logger = "AUTHZ"


class SubjectScopeUnknown(AdminScope):
    message_format = _("The given subject scope is unknown.")
    code = 400
    title = 'Subject Scope Unknown'
    logger = "ERROR"


class ObjectScopeUnknown(AdminScope):
    message_format = _("The given object scope is unknown.")
    code = 400
    title = 'Object Scope Unknown'
    logger = "ERROR"


class ActionScopeUnknown(AdminScope):
    message_format = _("The given action scope is unknown.")
    code = 400
    title = 'Action Scope Unknown'
    logger = "ERROR"


class SubjectScopeNameExisting(AdminScope):
    message_format = _("The given subject scope name is existing.")
    code = 400
    title = 'Subject Scope Name Existing'
    logger = "ERROR"


class ObjectScopeNameExisting(AdminScope):
    message_format = _("The given object scope name is existing.")
    code = 400
    title = 'Object Scope Name Existing'
    logger = "ERROR"


class ActionScopeNameExisting(AdminScope):
    message_format = _("The given action scope name is existing.")
    code = 400
    title = 'Action Scope Name Existing'
    logger = "ERROR"


class SubjectAssignmentUnknown(AdminAssignment):
    message_format = _("The given subject assignment value is unknown.")
    code = 400
    title = 'Subject Assignment Unknown'
    logger = "ERROR"


class ObjectAssignmentUnknown(AdminAssignment):
    message_format = _("The given object assignment value is unknown.")
    code = 400
    title = 'Object Assignment Unknown'
    logger = "ERROR"


class ActionAssignmentUnknown(AdminAssignment):
    message_format = _("The given action assignment value is unknown.")
    code = 400
    title = 'Action Assignment Unknown'
    logger = "ERROR"


class SubjectAssignmentExisting(AdminAssignment):
    message_format = _("The given subject assignment value is existing.")
    code = 400
    title = 'Subject Assignment Existing'
    logger = "ERROR"


class ObjectAssignmentExisting(AdminAssignment):
    message_format = _("The given object assignment value is existing.")
    code = 400
    title = 'Object Assignment Existing'
    logger = "ERROR"


class ActionAssignmentExisting(AdminAssignment):
    message_format = _("The given action assignment value is existing.")
    code = 400
    title = 'Action Assignment Existing'
    logger = "ERROR"


class AggregationAlgorithmNotExisting(AdminMetaRule):
    message_format = _("The given aggregation algorithm is not existing.")
    code = 400
    title = 'Aggregation Algorithm Not Existing'
    logger = "ERROR"


class AggregationAlgorithmUnknown(AdminMetaRule):
    message_format = _("The given aggregation algorithm is unknown.")
    code = 400
    title = 'Aggregation Algorithm Unknown'
    logger = "ERROR"


class SubMetaRuleAlgorithmNotExisting(AdminMetaRule):
    message_format = _("The given sub_meta_rule algorithm is unknown.")
    code = 400
    title = 'Sub_meta_rule Algorithm Unknown'
    logger = "ERROR"


class SubMetaRuleUnknown(AdminMetaRule):
    message_format = _("The given sub meta rule is unknown.")
    code = 400
    title = 'Sub Meta Rule Unknown'
    logger = "ERROR"


class SubMetaRuleNameExisting(AdminMetaRule):
    message_format = _("The sub meta rule name already exists.")
    code = 400
    title = 'Sub Meta Rule Name Existing'
    logger = "ERROR"


class SubMetaRuleExisting(AdminMetaRule):
    message_format = _("The sub meta rule already exists.")
    code = 400
    title = 'Sub Meta Rule Existing'
    logger = "ERROR"


class RuleExisting(AdminRule):
    message_format = _("The rule already exists.")
    code = 400
    title = 'Rule Existing'
    logger = "ERROR"


class RuleUnknown(AdminRule):
    message_format = _("The rule for that request doesn't exist.")
    code = 400
    title = 'Rule Unknown'
    logger = "ERROR"

