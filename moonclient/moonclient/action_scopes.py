# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ActionScopesList(Lister):
    """List all action scopes."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionScopesList, self).get_parser(prog_name)
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

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/action_scopes/{}".format(
            parsed_args.intraextension, parsed_args.action_category_id),
            authtoken=True)
        self.log.debug(data)
        return (
            ("id", "name", "description"),
            ((_id, data[_id]["name"], data[_id]["description"]) for _id in data)
        )


class ActionScopesAdd(Command):
    """Add a new action scope."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionScopesAdd, self).get_parser(prog_name)
        parser.add_argument(
            'action_category_id',
            metavar='<action-category-uuid>',
            help='Action category UUID',
        )
        parser.add_argument(
            'action_scope_name',
            metavar='<action-scope-name>',
            help='Action scope name',
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
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/action_scopes/{}".format(
            parsed_args.intraextension, parsed_args.action_category_id),
            post_data={
                "action_scope_name": parsed_args.action_scope_name,
                "action_scope_description": parsed_args.description,
            },
            authtoken=True)
        return (
            ("id", "name", "description"),
            ((_id, data[_id]["name"], data[_id]["description"]) for _id in data)
        )


class ActionScopesDelete(Command):
    """Delete an action scope."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionScopesDelete, self).get_parser(prog_name)
        parser.add_argument(
            'action_category_id',
            metavar='<action-category-uuid>',
            help='Action category  UUID',
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
        self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/action_scopes/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.action_category_id,
            parsed_args.action_scope_id
        ),
            method="DELETE",
            authtoken=True
        )