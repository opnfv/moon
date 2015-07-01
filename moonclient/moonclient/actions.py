# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ActionsList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionsList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(parsed_args.intraextension),
                                authtoken=True)
        if "actions" not in data:
            raise Exception("Error in command {}: {}".format("ActionsList", data))
        return (
            ("actions",),
            ((_uuid, ) for _uuid in data["actions"])
        )


class ActionsAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'action',
            metavar='<action-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/actions".format(parsed_args.intraextension),
                                post_data={"action_id": parsed_args.action},
                                authtoken=True)
        if "actions" not in data:
            raise Exception("Error in command {}".format(data))
        return (
            ("actions",),
            ((_uuid, ) for _uuid in data["actions"])
        )


class ActionsDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'action',
            metavar='<action-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/actions/{}".format(
            parsed_args.intraextension,
            parsed_args.action
        ),
            method="DELETE",
            authtoken=True)