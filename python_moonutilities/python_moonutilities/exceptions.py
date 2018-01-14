# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
from werkzeug.exceptions import HTTPException

logger = logging.getLogger("moon.utilities.exceptions")
_ = str


class MoonErrorMetaClass(type):

    def __init__(cls, name, bases, dct):
        super(MoonErrorMetaClass, cls).__init__(name, bases, dct)
        cls.hierarchy += "/" + str(name)


class MoonError(HTTPException):
    __metaclass__ = MoonErrorMetaClass
    hierarchy = ""
    description = _("There is an error requesting the Moon platform.")
    code = 400
    title = 'Moon Error'
    logger = "ERROR"

    def __init__(self, message="", status_code=None, payload=""):
        if message:
            self.description = message
        if status_code:
            self.code = status_code
        self.payload = payload
        super(MoonError, self).__init__()

    def __str__(self):
        return "{}: {}".format(self.code, self.title)

    def __del__(self):
        message = "{} ({}) {}".format(self.hierarchy, self.description, self.payload)
        if self.logger == "ERROR":
            try:
                logger.error(message)
            except AttributeError:
                logger.error(message)
        elif self.logger == "WARNING":
            try:
                logger.warning(message)
            except AttributeError:
                logger.warning(message)
        elif self.logger == "CRITICAL":
            try:
                logger.critical(message)
            except AttributeError:
                logger.critical(message)
        elif self.logger == "AUTHZ":
            try:
                logger.authz(self.hierarchy)
                logger.error(message)
            except AttributeError:
                logger.error(message)
        else:
            try:
                logger.info(message)
            except AttributeError:
                logger.info(message)

    # def to_dict(self):
    #     rv = dict(self.payload or ())
    #     rv['message'] = "{} ({})".format(self.hierarchy, self.description)
    #     rv['title'] = self.title
    #     rv['code'] = self.code
    #     return rv


# Exceptions for Tenant

class TenantException(MoonError):
    description = _("There is an error requesting this tenant.")
    code = 400
    title = 'Tenant Error'
    logger = "ERROR"


class TenantUnknown(TenantException):
    description = _("The tenant is unknown.")
    code = 400
    title = 'Tenant Unknown'
    logger = "ERROR"


class TenantAddedNameExisting(TenantException):
    description = _("The tenant name is existing.")
    code = 400
    title = 'Added Tenant Name Existing'
    logger = "ERROR"


class TenantNoIntraExtension(TenantException):
    description = _("The tenant has not intra_extension.")
    code = 400
    title = 'Tenant No Intra_Extension'
    logger = "ERROR"


class TenantNoIntraAuthzExtension(TenantNoIntraExtension):
    description = _("The tenant has not intra_admin_extension.")
    code = 400
    title = 'Tenant No Intra_Admin_Extension'
    logger = "ERROR"


# Exceptions for IntraExtension


class IntraExtensionException(MoonError):
    description = _("There is an error requesting this IntraExtension.")
    code = 400
    title = 'Extension Error'


class IntraExtensionUnknown(IntraExtensionException):
    description = _("The intra_extension is unknown.")
    code = 400
    title = 'Intra Extension Unknown'
    logger = "Error"


class ModelUnknown(MoonError):
    description = _("The model is unknown.")
    code = 400
    title = 'Model Unknown'
    logger = "Error"


class ModelExisting(MoonError):
    description = _("The model already exists.")
    code = 409
    title = 'Model Error'
    logger = "Error"


# Authz exceptions

class AuthzException(MoonError):
    description = _("There is an authorization error requesting this IntraExtension.")
    code = 403
    title = 'Authz Exception'
    logger = "AUTHZ"


# Auth exceptions

class AuthException(MoonError):
    description = _("There is an authentication error requesting this API. "
                    "You must provide a valid token from Keystone.")
    code = 401
    title = 'Auth Exception'
    logger = "AUTHZ"


# Admin exceptions

class AdminException(MoonError):
    description = _("There is an error requesting this Authz IntraExtension.")
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
    description = _("The given subject category name already exists.")
    code = 409
    title = 'Subject Category Name Existing'
    logger = "ERROR"


class SubjectCategoryExisting(AdminMetaData):
    description = _("The given subject category already exists.")
    code = 409
    title = 'Subject Category Existing'
    logger = "ERROR"


class ObjectCategoryNameExisting(AdminMetaData):
    description = _("The given object category name already exists.")
    code = 409
    title = 'Object Category Name Existing'
    logger = "ERROR"


class ObjectCategoryExisting(AdminMetaData):
    description = _("The given object category already exists.")
    code = 409
    title = 'Object Category Existing'
    logger = "ERROR"


class ActionCategoryNameExisting(AdminMetaData):
    description = _("The given action category name already exists.")
    code = 409
    title = 'Action Category Name Existing'
    logger = "ERROR"


class ActionCategoryExisting(AdminMetaData):
    description = _("The given action category already exists.")
    code = 409
    title = 'Action Category Existing'
    logger = "ERROR"


class SubjectCategoryUnknown(AdminMetaData):
    description = _("The given subject category is unknown.")
    code = 400
    title = 'Subject Category Unknown'
    logger = "ERROR"


class ObjectCategoryUnknown(AdminMetaData):
    description = _("The given object category is unknown.")
    code = 400
    title = 'Object Category Unknown'
    logger = "ERROR"


class ActionCategoryUnknown(AdminMetaData):
    description = _("The given action category is unknown.")
    code = 400
    title = 'Action Category Unknown'
    logger = "ERROR"


class SubjectUnknown(AdminPerimeter):
    description = _("The given subject is unknown.")
    code = 400
    title = 'Subject Unknown'
    logger = "ERROR"


class ObjectUnknown(AdminPerimeter):
    description = _("The given object is unknown.")
    code = 400
    title = 'Object Unknown'
    logger = "ERROR"


class ActionUnknown(AdminPerimeter):
    description = _("The given action is unknown.")
    code = 400
    title = 'Action Unknown'
    logger = "ERROR"


class SubjectNameExisting(AdminPerimeter):
    description = _("The given subject name is existing.")
    code = 400
    title = 'Subject Name Existing'
    logger = "ERROR"


class ObjectNameExisting(AdminPerimeter):
    description = _("The given object name is existing.")
    code = 400
    title = 'Object Name Existing'
    logger = "ERROR"


class ActionNameExisting(AdminPerimeter):
    description = _("The given action name is existing.")
    code = 400
    title = 'Action Name Existing'
    logger = "ERROR"


class ObjectsWriteNoAuthorized(AdminPerimeter):
    description = _("The modification on Objects is not authorized.")
    code = 400
    title = 'Objects Write No Authorized'
    logger = "AUTHZ"


class ActionsWriteNoAuthorized(AdminPerimeter):
    description = _("The modification on Actions is not authorized.")
    code = 400
    title = 'Actions Write No Authorized'
    logger = "AUTHZ"


class SubjectScopeUnknown(AdminScope):
    description = _("The given subject scope is unknown.")
    code = 400
    title = 'Subject Scope Unknown'
    logger = "ERROR"


class ObjectScopeUnknown(AdminScope):
    description = _("The given object scope is unknown.")
    code = 400
    title = 'Object Scope Unknown'
    logger = "ERROR"


class ActionScopeUnknown(AdminScope):
    description = _("The given action scope is unknown.")
    code = 400
    title = 'Action Scope Unknown'
    logger = "ERROR"


class SubjectScopeNameExisting(AdminScope):
    description = _("The given subject scope name is existing.")
    code = 400
    title = 'Subject Scope Name Existing'
    logger = "ERROR"


class ObjectScopeNameExisting(AdminScope):
    description = _("The given object scope name is existing.")
    code = 400
    title = 'Object Scope Name Existing'
    logger = "ERROR"


class ActionScopeNameExisting(AdminScope):
    description = _("The given action scope name is existing.")
    code = 400
    title = 'Action Scope Name Existing'
    logger = "ERROR"


class SubjectAssignmentUnknown(AdminAssignment):
    description = _("The given subject assignment value is unknown.")
    code = 400
    title = 'Subject Assignment Unknown'
    logger = "ERROR"


class ObjectAssignmentUnknown(AdminAssignment):
    description = _("The given object assignment value is unknown.")
    code = 400
    title = 'Object Assignment Unknown'
    logger = "ERROR"


class ActionAssignmentUnknown(AdminAssignment):
    description = _("The given action assignment value is unknown.")
    code = 400
    title = 'Action Assignment Unknown'
    logger = "ERROR"


class SubjectAssignmentExisting(AdminAssignment):
    description = _("The given subject assignment value is existing.")
    code = 400
    title = 'Subject Assignment Existing'
    logger = "ERROR"


class ObjectAssignmentExisting(AdminAssignment):
    description = _("The given object assignment value is existing.")
    code = 400
    title = 'Object Assignment Existing'
    logger = "ERROR"


class ActionAssignmentExisting(AdminAssignment):
    description = _("The given action assignment value is existing.")
    code = 400
    title = 'Action Assignment Existing'
    logger = "ERROR"


class AggregationAlgorithmNotExisting(AdminMetaRule):
    description = _("The given aggregation algorithm is not existing.")
    code = 400
    title = 'Aggregation Algorithm Not Existing'
    logger = "ERROR"


class AggregationAlgorithmUnknown(AdminMetaRule):
    description = _("The given aggregation algorithm is unknown.")
    code = 400
    title = 'Aggregation Algorithm Unknown'
    logger = "ERROR"


class SubMetaRuleAlgorithmNotExisting(AdminMetaRule):
    description = _("The given sub_meta_rule algorithm is unknown.")
    code = 400
    title = 'Sub_meta_rule Algorithm Unknown'
    logger = "ERROR"


class MetaRuleUnknown(AdminMetaRule):
    description = _("The given sub meta rule is unknown.")
    code = 400
    title = 'Sub Meta Rule Unknown'
    logger = "ERROR"


class SubMetaRuleNameExisting(AdminMetaRule):
    description = _("The sub meta rule name already exists.")
    code = 400
    title = 'Sub Meta Rule Name Existing'
    logger = "ERROR"


class MetaRuleExisting(AdminMetaRule):
    description = _("The sub meta rule already exists.")
    code = 400
    title = 'Sub Meta Rule Existing'
    logger = "ERROR"


class MetaRuleContentError(AdminMetaRule):
    description = _("Invalid content of meta rule.")
    code = 400
    title = 'Meta Rule Error'
    logger = "ERROR"


class RuleExisting(AdminRule):
    description = _("The rule already exists.")
    code = 400
    title = 'Rule Existing'
    logger = "ERROR"


class RuleUnknown(AdminRule):
    description = _("The rule for that request doesn't exist.")
    code = 400
    title = 'Rule Unknown'
    logger = "ERROR"


# Keystone exceptions


class KeystoneError(MoonError):
    description = _("There is an error connecting to Keystone.")
    code = 400
    title = 'Keystone error'
    logger = "ERROR"


class KeystoneProjectError(KeystoneError):
    description = _("There is an error retrieving projects from the Keystone service.")
    code = 400
    title = 'Keystone project error'
    logger = "ERROR"


class KeystoneUserError(KeystoneError):
    description = _("There is an error retrieving users from the Keystone service.")
    code = 400
    title = 'Keystone user error'
    logger = "ERROR"


class KeystoneUserConflict(KeystoneUserError):
    description = _("A user with that name already exist.")
    code = 400
    title = 'Keystone user error'
    logger = "ERROR"


# Consul exceptions


class ConsulError(MoonError):
    description = _("There is an error connecting to Consul.")
    code = 400
    title = 'Consul error'
    logger = "ERROR"


class ConsulComponentNotFound(ConsulError):
    description = _("The component do not exist in Consul database.")
    code = 500
    title = 'Consul error'
    logger = "WARNING"


class ConsulComponentContentError(ConsulError):
    description = _("invalid content of component .")
    code = 500
    title = 'Consul Content error'
    logger = "WARNING"

# Containers exceptions


class DockerError(MoonError):
    description = _("There is an error with Docker.")
    code = 400
    title = 'Docker error'
    logger = "ERROR"


class ContainerMissing(DockerError):
    description = _("Some containers are missing.")
    code = 400
    title = 'Container missing'
    logger = "ERROR"


class PdpUnknown(MoonError):
    description = _("The pdp is unknown.")
    code = 400
    title = 'Pdp Unknown'
    logger = "Error"


class PdpExisting(MoonError):
    description = _("The pdp already exists.")
    code = 409
    title = 'Pdp Error'
    logger = "Error"


class PdpContentError(MoonError):
    description = _("Invalid content of pdp.")
    code = 409
    title = 'Pdp Error'
    logger = "Error"


class PdpKeystoneMappingConflict(MoonError):
    description = _("A pdp is already mapped to that Keystone project.")
    code = 409
    title = 'Pdp Mapping Error'
    logger = "Error"


class PolicyUnknown(MoonError):
    description = _("The policy is unknown.")
    code = 400
    title = 'Policy Unknown'
    logger = "Error"


class PolicyExisting(MoonError):
    description = _("The policy already exists.")
    code = 409
    title = 'Policy Error'
    logger = "Error"
