# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from keystone.common import dependency
from keystone.exception import Error
from keystone.i18n import _, _LW

@dependency.requires('moonlog_api')
class TenantError(Error):
    message_format = _("There is an error requesting this tenant"
                       " the server could not comply with the request"
                       " since it is either malformed or otherwise"
                       " incorrect. The client is assumed to be in error.")
    code = 400
    title = 'Tenant Error'
    logger = "ERROR"

    def __del__(self):
        if self.logger == "ERROR":
            self.moonlog_api.error(self.message_format)
        elif self.logger == "WARNING":
            self.moonlog_api.warning(self.message_format)
        elif self.logger == "CRITICAL":
            self.moonlog_api.critical(self.message_format)
        elif self.logger == "AUTHZ":
            self.moonlog_api.authz(self.message_format)
            self.moonlog_api.error(self.message_format)
        else:
            self.moonlog_api.info(self.message_format)



class TenantListEmptyError(TenantError):
    message_format = _("The tenant list mapping is empty, you must set the mapping first.")
    code = 400
    title = 'Tenant List Empty Error'


class TenantNotFoundError(TenantError):
    message_format = _("The tenant UUID was not found.")
    code = 400
    title = 'Tenant UUID Not Found Error'


class IntraExtensionError(TenantError):
    message_format = _("There is an error requesting this IntraExtension.")
    code = 400
    title = 'Extension Error'


class CategoryNotFound(IntraExtensionError):
    message_format = _("The category is unknown.")
    code = 400
    title = 'Extension Error'
    logger = "WARNING"


class IntraExtensionUnMapped(TenantError):
    message_format = _("The Extension is not mapped to a tenant.")
    code = 400
    title = 'Extension UUID Not Found Error'
    logger = "WARNING"


class IntraExtensionNotFound(IntraExtensionError):
    message_format = _("The Extension for that tenant is unknown.")
    code = 400
    title = 'Extension UUID Not Found Error'
    logger = "WARNING"


class IntraExtensionNotAuthorized(IntraExtensionError):
    message_format = _("User has no authorization for that action.")
    code = 400
    title = 'Authorization Error'
    logger = "AUTHZ"


class AdminIntraExtensionNotFound(IntraExtensionNotFound):
    message_format = _("The admin Extension for that tenant is unknown.")
    code = 400
    title = 'Admin Extension UUID Not Found Error'
    logger = "WARNING"


class AdminIntraExtensionCreationError(IntraExtensionError):
    message_format = _("The arguments for the creation of this admin Extension were malformed.")
    code = 400
    title = 'Admin Extension Creation Error'


class AdminIntraExtensionModificationNotAuthorized(IntraExtensionError):
    message_format = _("The modification of this admin Extension is not authorizaed.")
    code = 400
    title = 'Admin Extension Creation Error'
    logger = "AUTHZ"

class AuthIntraExtensionModificationNotAuthorized(IntraExtensionError):
    message_format = _("The modification of this authz Extension is not authorizaed.")
    code = 400
    title = 'Authz Extension Creation Error'
    logger = "AUTHZ"


class AuthzIntraExtensionNotFound(IntraExtensionNotFound):
    message_format = _("The authz Extension for that tenant is unknown.")
    code = 400
    title = 'Authz Extension UUID Not Found Error'
    logger = "WARNING"

