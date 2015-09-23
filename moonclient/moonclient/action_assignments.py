# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ActionAssignmentsList(Lister):
    """List all action assignments."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionAssignmentsList, self).get_parser(prog_name)
        parser.add_argument(
            'action_id',
            metavar='<action-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            'action_category_id',
            metavar='<action-category-uuid>',
            help='Action category UUID',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def __get_scope_from_id(self, intraextension_id, action_category_id, action_scope_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_scopes/{}".format(
            intraextension_id, action_category_id),
            authtoken=True)
        if action_scope_id in data:
            return data[action_scope_id]

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_assignments/{}/{}".format(
            parsed_args.intraextension, parsed_args.action_id, parsed_args.action_category_id),
            authtoken=True)
        return (
            ("id", "name"),
            ((_id, self.__get_scope_from_id(parsed_args.intraextension,
                                            parsed_args.action_category_id,
                                            _id)['name']) for _id in data)
        )


class ActionAssignmentsAdd(Command):
    """Add a new action assignment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionAssignmentsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'action_id',
            metavar='<action-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            'action_category_id',
            metavar='<action-category-uuid>',
            help='Action category UUID',
        )
        parser.add_argument(
            'action_scope_id',
            metavar='<action-scope-uuid>',
            help='Action scope UUID',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def __get_scope_from_id(self, intraextension_id, action_category_id, action_scope_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_scopes/{}".format(
            intraextension_id, action_category_id),
            authtoken=True)
        if action_scope_id in data:
            return data[action_scope_id]

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_assignments".format(parsed_args.intraextension),
                                post_data={
                                    "action_id": parsed_args.action_id,
                                    "action_category_id": parsed_args.action_category_id,
                                    "action_scope_id": parsed_args.action_scope_id},
                                authtoken=True)
        return (
            ("id", "name"),
            ((_id, self.__get_scope_from_id(parsed_args.intraextension,
                                            parsed_args.action_category_id,
                                            _id)['name']) for _id in data)
        )


class ActionAssignmentsDelete(Command):
    """Delete an action assignment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionAssignmentsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'action_id',
            metavar='<action-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            'action_category_id',
            metavar='<action-category-uuid>',
            help='Action category UUID',
        )
        parser.add_argument(
            'action_scope_id',
            metavar='<action-scope-uuid>',
            help='Action scope UUID',
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
            parsed_args.action_id,
            parsed_args.action_category_id,
            parsed_args.action_scope_id),
            method="DELETE",
            authtoken=True
        )