# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ActionAssignmentsList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionAssignmentsList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_assignments".format(parsed_args.intraextension),
                                authtoken=True)
        if "action_assignments" not in data:
            raise Exception("Error in command {}: {}".format("ActionAssignmentsList", data))
        return (
            ("category", "value"),
            ((_cat, str(_val)) for _cat, _val in data["action_assignments"].items())
        )


class ActionAssignmentsAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionAssignmentsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'action_id',
            metavar='<action-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            'action_category',
            metavar='<action_category>',
            help='Action Category',
        )
        parser.add_argument(
            'action_category_scope',
            metavar='<action_category_scope>',
            help='Action Category Scope',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_assignments".format(parsed_args.intraextension),
                                post_data={
                                    "action_id": parsed_args.action_id,
                                    "action_category": parsed_args.action_category,
                                    "action_category_scope": parsed_args.action_category_scope
                                },
                                authtoken=True)
        if "action_assignments" not in data:
            raise Exception("Error in command {}".format(data))
        return (
            ("category", "value"),
            ((_cat, str(_val)) for _cat, _val in data["action_assignments"].items())
        )


class ActionAssignmentsDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionAssignmentsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'action_id',
            metavar='<action-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            'action_category',
            metavar='<action_category>',
            help='Action Category',
        )
        parser.add_argument(
            'action_category_scope',
            metavar='<action_category_scope>',
            help='Action Category Scope',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_assignments/{}/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.action_category,
            parsed_args.action_id,
            parsed_args.action_category_scope
        ),
            method="DELETE",
            authtoken=True)