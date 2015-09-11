# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne


class IntraExtensionCreate(Command):
    """Create a new Intra_Extension."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(IntraExtensionCreate, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<intraextension-name>',
            help='New IntraExtension name',
        )
        parser.add_argument(
            '--policy_model',
            metavar='<policymodel-name>',
            help='Policy model name (Template for the new IntraExtension)',
        )
        parser.add_argument(
            '--description',
            metavar='<intraextension-description>',
            help='New IntraExtension description',
            default=""
        )
        return parser

    def take_action(self, parsed_args):
        post_data = {
            "intra_extension_name": parsed_args.name,
            "intra_extension_model": parsed_args.policy_model,
            "intra_extension_description": parsed_args.description
        }
        ie = self.app.get_url("/v3/OS-MOON/intra_extensions", post_data=post_data, authtoken=True)
        if "id" not in ie:
            raise Exception("Error in command {}".format(ie))
        self.app.stdout.write("IntraExtension created: {}\n".format(ie["id"]))
        return


class IntraExtensionList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(IntraExtensionList, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        ie = self.app.get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
        # if "intra_extensions" not in ie:
        #     raise Exception("Error in command {}".format(ie))
        return (
            ("id", "name", "model"),
            ((_id, ie[_id]["name"], ie[_id]["model"]) for _id in ie.keys())
        )


class IntraExtensionDelete(Command):
    """Delete an Intra_Extension."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(IntraExtensionDelete, self).get_parser(prog_name)
        parser.add_argument(
            'uuid',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        ie = self.app.get_url("/v3/OS-MOON/intra_extensions/{}".format(parsed_args.uuid),
                              method="DELETE",
                              authtoken=True)
        return


class IntraExtensionShow(ShowOne):
    """Show detail about one Intra_Extension."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(IntraExtensionShow, self).get_parser(prog_name)
        parser.add_argument(
            'uuid',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        ie = self.app.get_url("/v3/OS-MOON/intra_extensions/{}".format(parsed_args.uuid), authtoken=True)
        if "intra_extensions" not in ie:
            raise Exception("Error in command {}".format(ie))
        try:
            columns = (
                "id",
                "name",
                "description",
                "tenant",
                "enabled",
                "model",
                "genre"
            )
            data = (
                ie["intra_extensions"]["id"],
                ie["intra_extensions"]["name"],
                ie["intra_extensions"]["description"],
                ie["intra_extensions"]["tenant"],
                ie["intra_extensions"]["enabled"],
                ie["intra_extensions"]["model"],
                ie["intra_extensions"]["genre"]
            )
            return columns, data
        except Exception as e:
            self.app.stdout.write(str(e))


class TenantSet(Command):
    """Set the tenant for a intra_extension."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TenantSet, self).get_parser(prog_name)
        parser.add_argument(
            'intraextension_uuid',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        parser.add_argument(
            'tenant_name',
            metavar='<tenant-name>',
            help='Tenant Name',
        )
        return parser

    def take_action(self, parsed_args):
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/tenant".format(parsed_args.intraextension_uuid),
                         post_data={"tenant_id": parsed_args.tenant_name},
                         authtoken=True)

