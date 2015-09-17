# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ActionCategoryScopeList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionCategoryScopeList, self).get_parser(prog_name)
        parser.add_argument(
            'category',
            metavar='<category-uuid>',
            help='Category UUID',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_scopes/{}".format(
            parsed_args.intraextension, parsed_args.category),
                                authtoken=True)
        self.log.debug(data)
        return (
            ("id", "name", "description"),
            ((_id, data[_id]["name"], data[_id]["description"]) for _id in data)
        )


class ActionCategoryScopeAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionCategoryScopeAdd, self).get_parser(prog_name)
        parser.add_argument(
            'category',
            metavar='<category-uuid>',
            help='Category UUID',
        )
        parser.add_argument(
            'scope_name',
            metavar='<scope-str>',
            help='Scope Name',
        )
        parser.add_argument(
            '--description',
            metavar='<description-str>',
            help='Description',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_scopes/{}".format(
            parsed_args.intraextension, parsed_args.category),
                                post_data={
                                    "action_scope_name": parsed_args.scope_name,
                                    "action_scope_description": parsed_args.description,
                                },
                                authtoken=True)
        return (
            ("id", "name", "description"),
            ((_id, data[_id]["name"], data[_id]["description"]) for _id in data)
        )


class ActionCategoryScopeDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionCategoryScopeDelete, self).get_parser(prog_name)
        parser.add_argument(
            'category',
            metavar='<category-uuid>',
            help='Category  UUID',
        )
        parser.add_argument(
            'scope_id',
            metavar='<scope-uuid>',
            help='Scope UUID',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_scopes/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.category,
            parsed_args.scope_id
        ),
            method="DELETE",
            authtoken=True)