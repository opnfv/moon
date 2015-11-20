# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne
import os


class IntraExtensionSelect(Command):
    """Select an Intra_Extension to work with."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(IntraExtensionSelect, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<intraextension-id>',
            help='IntraExtension UUID to select',
        )
        return parser

    def take_action(self, parsed_args):
        ie = self.app.get_url("/v3/OS-MOON/intra_extensions", authtoken=True)
        if parsed_args.id in ie.keys():
            self.app.intraextension = parsed_args.id
            self.app.stdout.write("Select {} IntraExtension.\n".format(self.app.intraextension))
        else:
            self.app.stdout.write("IntraExtension {} unknown.\n".format(parsed_args.id))
        return


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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}".format(parsed_args.uuid),
                         method="DELETE",
                         authtoken=True)


class IntraExtensionInit(Command):
    """Initialize the root Intra_Extension (if needed)."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(IntraExtensionInit, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.app.get_url("/v3/OS-MOON/intra_extensions/init",
                         method="GET",
                         authtoken=True)


class IntraExtensionShow(ShowOne):
    """Show detail about one Intra_Extension."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(IntraExtensionShow, self).get_parser(prog_name)
        parser.add_argument(
            'uuid',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID (put "selected" if you want to show the selected IntraExtension)',
            default="selected"
        )
        return parser

    def take_action(self, parsed_args):
        intra_extension_id = parsed_args.uuid
        if parsed_args.uuid == "selected":
            intra_extension_id = self.app.intraextension
        self.log.debug("self.app.intraextension={}".format(intra_extension_id))
        ie = self.app.get_url("/v3/OS-MOON/intra_extensions/{}".format(intra_extension_id), authtoken=True)
        self.log.debug("ie={}".format(ie))
        if "id" not in ie:
            self.log.error("Unknown intraextension {}".format(intra_extension_id))
            raise Exception()
        try:
            columns = (
                "id",
                "name",
                "description",
                "model",
                "genre"
            )
            data = (
                ie["id"],
                ie["name"],
                ie["description"],
                ie["model"],
                ie["genre"]
            )
            return columns, data
        except Exception as e:
            self.app.stdout.write(str(e))
