# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ObjectAssignmentsList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectAssignmentsList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_assignments".format(parsed_args.intraextension),
                                authtoken=True)
        if "object_assignments" not in data:
            raise Exception("Error in command {}: {}".format("ObjectAssignmentsList", data))
        return (
            ("category", "value"),
            ((_cat, str(_val)) for _cat, _val in data["object_assignments"].items())
        )


class ObjectAssignmentsAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectAssignmentsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'object_id',
            metavar='<action-uuid>',
            help='Object UUID',
        )
        parser.add_argument(
            'object_category',
            metavar='<object_category>',
            help='Object Category',
        )
        parser.add_argument(
            'object_category_scope',
            metavar='<object_category_scope>',
            help='Object Category Scope',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_assignments".format(parsed_args.intraextension),
                                post_data={
                                    "object_id": parsed_args.object_id,
                                    "object_category": parsed_args.object_category,
                                    "object_category_scope": parsed_args.object_category_scope
                                },
                                authtoken=True)
        if "object_assignments" not in data:
            raise Exception("Error in command {}".format(data))
        return (
            ("category", "value"),
            ((_cat, str(_val)) for _cat, _val in data["object_assignments"].items())
        )


class ObjectAssignmentsDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectAssignmentsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'object_id',
            metavar='<action-uuid>',
            help='Object UUID',
        )
        parser.add_argument(
            'object_category',
            metavar='<object_category>',
            help='Object Category',
        )
        parser.add_argument(
            'object_category_scope',
            metavar='<object_category_scope>',
            help='Object Category Scope',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_assignments/{}/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.object_category,
            parsed_args.object_id,
            parsed_args.object_category_scope
        ),
            method="DELETE",
            authtoken=True)