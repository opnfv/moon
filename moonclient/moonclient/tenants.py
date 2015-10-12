# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class TenantList(Lister):
    """List all tenants."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TenantList, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        tenants = self.app.get_url("/v3/OS-MOON/tenants", authtoken=True)
        self.log.debug(tenants)
        return (
            ("id", "name", "description", "intra_authz_extension_id", "intra_admin_extension_id"),
            ((
                tenant_id,
                tenants[tenant_id]["name"],
                tenants[tenant_id]["description"],
                tenants[tenant_id]["intra_authz_extension_id"],
                tenants[tenant_id]["intra_admin_extension_id"],
                )
                for tenant_id in tenants)
        )


class TenantAdd(Command):
    """Add a tenant."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TenantAdd, self).get_parser(prog_name)
        parser.add_argument(
            'tenant_name',
            metavar='<tenant-name>',
            help='Tenant name',
        )
        parser.add_argument(
            '--authz',
            metavar='<authz-intraextension-uuid>',
            help='Authz IntraExtension UUID',
        )
        parser.add_argument(
            '--admin',
            metavar='<admin-intraextension-uuid>',
            help='Admin IntraExtension UUID',
        )
        parser.add_argument(
            '--desc',
            metavar='<tenant-description-str>',
            help='Tenant description',
        )
        return parser

    def take_action(self, parsed_args):
        post_data = dict()
        post_data["tenant_name"] = parsed_args.tenant_name
        if parsed_args.authz:
            post_data["tenant_intra_authz_extension_id"] = parsed_args.authz
        if parsed_args.admin:
            post_data["tenant_intra_admin_extension_id"] = parsed_args.admin
        if parsed_args.desc:
            post_data["tenant_description"] = parsed_args.desc
        tenants = self.app.get_url("/v3/OS-MOON/tenants",
                                   post_data=post_data,
                                   authtoken=True)
        return (
            ("id", "name", "description", "intra_authz_extension_id", "intra_admin_extension_id"),
            ((
                tenant_id,
                tenants[tenant_id]["name"],
                tenants[tenant_id]["description"],
                tenants[tenant_id]["intra_authz_extension_id"],
                tenants[tenant_id]["intra_admin_extension_id"],
                )
             for tenant_id in tenants)
        )


class TenantShow(Command):
    """Show information of one tenant."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TenantShow, self).get_parser(prog_name)
        parser.add_argument(
            'tenant_name',
            metavar='<tenant-name>',
            help='Tenant name',
        )
        return parser

    def take_action(self, parsed_args):
        tenants = self.app.get_url("/v3/OS-MOON/tenants/{}".format(parsed_args.tenant_name),
                                   authtoken=True)
        return (
            ("id", "name", "description", "intra_authz_extension_id", "intra_admin_extension_id"),
            ((
                tenant_id,
                tenants[tenant_id]["name"],
                tenants[tenant_id]["description"],
                tenants[tenant_id]["intra_authz_extension_id"],
                tenants[tenant_id]["intra_admin_extension_id"],
                )
             for tenant_id in tenants)
        )


class TenantSet(Command):
    """Modify a tenant."""

    log = logging.getLogger(__name__)

    # TODO: could use a PATCH method also
    def get_parser(self, prog_name):
        parser = super(TenantSet, self).get_parser(prog_name)
        parser.add_argument(
            'tenant_id',
            metavar='<tenant-id>',
            help='Tenant UUID',
        )
        parser.add_argument(
            '--name',
            metavar='<tenant-name>',
            help='Tenant name',
        )
        parser.add_argument(
            '--authz',
            metavar='<authz-intraextension-uuid>',
            help='Authz IntraExtension UUID',
        )
        parser.add_argument(
            '--admin',
            metavar='<admin-intraextension-uuid>',
            help='Admin IntraExtension UUID',
        )
        parser.add_argument(
            '--desc',
            metavar='<tenant-description-str>',
            help='Tenant description',
        )
        return parser

    def take_action(self, parsed_args):
        post_data = dict()
        post_data["tenant_id"] = parsed_args.tenant_id
        if parsed_args.name:
            post_data["tenant_name"] = parsed_args.tenant_name
        if parsed_args.authz is not None:
            post_data["tenant_intra_authz_extension_id"] = parsed_args.authz
        if parsed_args.admin is not None:
            post_data["tenant_intra_admin_extension_id"] = parsed_args.admin
        if parsed_args.desc is not None:
            post_data["tenant_description"] = parsed_args.desc
        tenants = self.app.get_url("/v3/OS-MOON/tenants/{}".format(post_data["tenant_id"]),
                                   post_data=post_data,
                                   authtoken=True)
        return (
            ("id", "name", "description", "authz", "admin"),
            ((
                tenant_id,
                tenants[tenant_id]["name"],
                tenants[tenant_id]["description"],
                tenants[tenant_id]["intra_authz_extension_id"],
                tenants[tenant_id]["intra_admin_extension_id"],
                )
             for tenant_id in tenants)
        )


class TenantDelete(Command):
    """Delete a tenant."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TenantDelete, self).get_parser(prog_name)
        parser.add_argument(
            'tenant_id',
            metavar='<tenant-id>',
            help='Tenant UUID',
        )
        return parser

    def take_action(self, parsed_args):
        self.app.get_url("/v3/OS-MOON/tenants/{}".format(parsed_args.tenant_id),
                         method="DELETE",
                         authtoken=True)
