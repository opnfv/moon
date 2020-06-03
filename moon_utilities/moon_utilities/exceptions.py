# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging

logger = logging.getLogger("moon.utilities.exceptions")
_ = str


class MoonErrorMetaClass(type):

    def __init__(cls, name, bases, dct):
        super(MoonErrorMetaClass, cls).__init__(name, bases, dct)
        cls.hierarchy += "/" + str(name)


class MoonError(BaseException):
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


class ModelContentError(MoonError):
    description = _("The model content is invalid.")
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


class CategoryNameInvalid(AdminMetaData):
    description = _("The given category name is invalid.")
    code = 400
    title = 'Category Name Invalid'
    logger = "ERROR"


class SubjectCategoryExisting(AdminMetaData):
    description = _("The given subject category already exists.")
    code = 409
    title = 'Subject Category Existing'
    logger = "ERROR"


class ObjectCategoryExisting(AdminMetaData):
    description = _("The given object category already exists.")
    code = 409
    title = 'Object Category Existing'
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


class DeleteSubjectCategoryWithMetaRule(MoonError):
    description = _("Cannot delete subject category used in meta rule ")
    code = 400
    title = 'Subject Category With Meta Rule Error'
    logger = "Error"


class DeleteObjectCategoryWithMetaRule(MoonError):
    description = _("Cannot delete Object category used in meta rule ")
    code = 400
    title = 'Object Category With Meta Rule Error'
    logger = "Error"


class ObjectCategoryUnknown(AdminMetaData):
    description = _("The given object category is unknown.")
    code = 400
    title = 'Object Category Unknown'
    logger = "ERROR"


class DeleteActionCategoryWithMetaRule(MoonError):
    description = _("Cannot delete Action category used in meta rule ")
    code = 400
    title = 'Action Category With Meta Rule Error'
    logger = "Error"


class ActionCategoryUnknown(AdminMetaData):
    description = _("The given action category is unknown.")
    code = 400
    title = 'Action Category Unknown'
    logger = "ERROR"


class PerimeterContentError(AdminPerimeter):
    description = _("Perimeter content is invalid.")
    code = 400
    title = 'Perimeter content is invalid.'
    logger = "ERROR"


class DeletePerimeterWithAssignment(MoonError):
    description = _("Cannot delete perimeter with assignment")
    code = 400
    title = 'Perimeter With Assignment Error'
    logger = "Error"


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


class SubjectExisting(AdminPerimeter):
    description = _("The given subject is existing.")
    code = 409
    title = 'Subject Existing'
    logger = "ERROR"


class ObjectExisting(AdminPerimeter):
    description = _("The given object is existing.")
    code = 409
    title = 'Object Existing'
    logger = "ERROR"


class ActionExisting(AdminPerimeter):
    description = _("The given action is existing.")
    code = 409
    title = 'Action Existing'
    logger = "ERROR"


class SubjectNameExisting(AdminPerimeter):
    description = _("The given subject name is existing.")
    code = 409
    title = 'Subject Name Existing'
    logger = "ERROR"


class ObjectNameExisting(AdminPerimeter):
    description = _("The given object name is existing.")
    code = 409
    title = 'Object Name Existing'
    logger = "ERROR"


class ActionNameExisting(AdminPerimeter):
    description = _("The given action name is existing.")
    code = 409
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


class SubjectScopeExisting(AdminScope):
    description = _("The given subject scope is existing.")
    code = 409
    title = 'Subject Scope Existing'
    logger = "ERROR"


class ObjectScopeExisting(AdminScope):
    description = _("The given object scope is existing.")
    code = 409
    title = 'Object Scope Existing'
    logger = "ERROR"


class ActionScopeExisting(AdminScope):
    description = _("The given action scope is existing.")
    code = 409
    title = 'Action Scope Existing'
    logger = "ERROR"


class SubjectScopeNameExisting(AdminScope):
    description = _("The given subject scope name is existing.")
    code = 409
    title = 'Subject Scope Name Existing'
    logger = "ERROR"


class ObjectScopeNameExisting(AdminScope):
    description = _("The given object scope name is existing.")
    code = 409
    title = 'Object Scope Name Existing'
    logger = "ERROR"


class ActionScopeNameExisting(AdminScope):
    description = _("The given action scope name is existing.")
    code = 409
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
    code = 409
    title = 'Subject Assignment Existing'
    logger = "ERROR"


class ObjectAssignmentExisting(AdminAssignment):
    description = _("The given object assignment value is existing.")
    code = 409
    title = 'Object Assignment Existing'
    logger = "ERROR"


class ActionAssignmentExisting(AdminAssignment):
    description = _("The given action assignment value is existing.")
    code = 409
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
    description = _("The given meta rule is unknown.")
    code = 400
    title = 'Meta Rule Unknown'
    logger = "ERROR"


class MetaRuleNotLinkedWithPolicyModel(MoonError):
    description = _("The meta rule is not found in the model attached to the policy.")
    code = 400
    title = 'MetaRule Not Linked With Model - Policy'
    logger = "Error"


class CategoryNotAssignedMetaRule(MoonError):
    description = _("The category is not found in the meta rules attached to the policy.")
    code = 400
    title = 'Category Not Linked With Meta Rule - Policy'
    logger = "Error"


class SubMetaRuleNameExisting(AdminMetaRule):
    description = _("The sub meta rule name already exists.")
    code = 409
    title = 'Sub Meta Rule Name Existing'
    logger = "ERROR"


class MetaRuleExisting(AdminMetaRule):
    description = _("The meta rule already exists.")
    code = 409
    title = 'Meta Rule Existing'
    logger = "ERROR"


class MetaRuleContentError(AdminMetaRule):
    description = _("Invalid content of meta rule.")
    code = 400
    title = 'Meta Rule Error'
    logger = "ERROR"


class MetaRuleUpdateError(AdminMetaRule):
    description = _("Meta_rule is used in Rule.")
    code = 400
    title = 'Meta_Rule Update Error'
    logger = "ERROR"


class RuleExisting(AdminRule):
    description = _("The rule already exists.")
    code = 409
    title = 'Rule Existing'
    logger = "ERROR"


class RuleContentError(AdminRule):
    description = _("Invalid content of rule.")
    code = 400
    title = 'Rule Error'
    logger = "ERROR"


class RuleUnknown(AdminRule):
    description = _("The rule for that request doesn't exist.")
    code = 400
    title = 'Rule Unknown'
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


class WrapperConflict(MoonError):
    description = _("A Wrapper already exist for the specified slave.")
    code = 409
    title = 'Wrapper conflict'
    logger = "ERROR"


class PipelineConflict(MoonError):
    description = _("A Pipeline already exist for the specified slave.")
    code = 409
    title = 'Pipeline conflict'
    logger = "ERROR"


class PipelineUnknown(MoonError):
    description = _("This Pipeline is unknown from the system.")
    code = 400
    title = 'Pipeline Unknown'
    logger = "ERROR"


class WrapperUnknown(MoonError):
    description = _("This Wrapper is unknown from the system.")
    code = 400
    title = 'Wrapper Unknown'
    logger = "ERROR"


class SlaveNameUnknown(MoonError):
    description = _("The slave is unknown.")
    code = 400
    title = 'Slave Unknown'
    logger = "Error"


class SlaveExisting(MoonError):
    description = _("The slave already exists.")
    code = 409
    title = 'Slave Error'
    logger = "Error"


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
    code = 400
    title = 'Pdp Error'
    logger = "Error"


class PdpInUse(MoonError):
    description = _("The pdp is inuse.")
    code = 400
    title = 'Pdp Inuse'
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


class PolicyContentError(MoonError):
    description = _("The policy content is invalid.")
    code = 400
    title = 'Policy Content Error'
    logger = "Error"


class PolicyExisting(MoonError):
    description = _("The policy already exists.")
    code = 409
    title = 'Policy Already Exists'
    logger = "Error"


class PolicyUpdateError(MoonError):
    description = _("The policy data is used.")
    code = 400
    title = 'Policy update error'
    logger = "Error"


class DeleteData(MoonError):
    description = _("Cannot delete data with assignment")
    code = 400
    title = 'Data Error'
    logger = "Error"


class DeleteCategoryWithData(MoonError):
    description = _("Cannot delete category with data")
    code = 400
    title = 'Category With Data Error'
    logger = "Error"


class DeleteCategoryWithMetaRule(MoonError):
    description = _("Cannot delete category with meta rule")
    code = 400
    title = 'Category With MetaRule Error'
    logger = "Error"


class DeleteCategoryWithAssignment(MoonError):
    description = _("Cannot delete category with assignment ")
    code = 400
    title = 'Category With Assignment Error'
    logger = "Error"


class DeleteModelWithPolicy(MoonError):
    description = _("Cannot delete model with policy")
    code = 400
    title = 'Model With Policy Error'
    logger = "Error"


class DeletePolicyWithPdp(MoonError):
    description = _("Cannot delete policy with pdp")
    code = 400
    title = 'Policy With PDP Error'
    logger = "Error"


class DeletePolicyWithPerimeter(MoonError):
    description = _("Cannot delete policy with perimeter")
    code = 400
    title = 'Policy With Perimeter Error'
    logger = "Error"


class DeletePolicyWithData(MoonError):
    description = _("Cannot delete policy with data")
    code = 400
    title = 'Policy With Data Error'
    logger = "Error"


class DeletePolicyWithRules(MoonError):
    description = _("Cannot delete policy with rules")
    code = 400
    title = 'Policy With Rule Error'
    logger = "Error"


class DeleteMetaRuleWithModel(MoonError):
    description = _("Cannot delete meta rule with model")
    code = 400
    title = 'Meta rule With Model Error'
    logger = "Error"


class DeleteMetaRuleWithRule(MoonError):
    description = _("Cannot delete meta rule with rule")
    code = 400
    title = 'Meta rule With Model Error'
    logger = "Error"


class DataContentError(MoonError):
    description = _("The data Content Error.")
    code = 400
    title = 'Data Content Error'
    logger = "Error"


class DataUnknown(MoonError):
    description = _("The data unknown.")
    code = 400
    title = 'Data Unknown'
    logger = "Error"


class ValidationContentError(MoonError):
    description = _("The Content validation incorrect.")
    code = 400
    title = 'Invalid Content'
    logger = "Error"

    def __init__(self, message=""):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class ValidationKeyError(MoonError):
    description = _("The Key validation incorrect.")
    code = 400
    title = 'Invalid Key'
    logger = "Error"

    def __init__(self, message=""):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class ForbiddenOverride(MoonError):
    description = _("Forbidden override flag.")
    code = 500
    title = 'Forbidden override.'
    logger = "Error"


class InvalidJson(MoonError):
    description = _("Invalid Json")
    code = 400
    title = 'Invalid Json.'
    logger = "Error"


class UnknownName(MoonError):
    description = _("Name is Unknown")
    code = 400
    title = 'Unknown Name.'
    logger = "Error"


class UnknownId(MoonError):
    description = _("ID is Unknown")
    code = 400
    title = 'Unknown ID.'
    logger = "Error"


class MissingIdOrName(MoonError):
    description = _("Name or ID is missing")
    code = 400
    title = 'Missing ID or Name.'
    logger = "Error"


class UnknownField(MoonError):
    description = _("Field is Unknown")
    code = 400
    title = 'Unknown Field.'
    logger = "Error"


class DecryptError(MoonError):
    description = _("Cannot decrypt API key")
    code = 401
    title = 'API Key Error.'
    logger = "Error"


class EncryptError(MoonError):
    description = _("Cannot encrypt API key")
    code = 401
    title = 'API Key Error.'
    logger = "Error"


class AttributeUnknownError(MoonError):
    description = _("Cannot find attribute")
    code = 401
    title = 'Attribute Error.'
    logger = "Error"


class AttributeValueUnknownError(MoonError):
    description = _("Cannot find value for this attribute")
    code = 401
    title = 'Attribute Value Error.'
    logger = "Error"

