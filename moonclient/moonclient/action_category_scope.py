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
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope".format(parsed_args.intraextension),
                                authtoken=True)
        if "action_category_scope" not in data:
            raise Exception("Error in command {}: {}".format("ActionCategoryScopeList", data))
        return (
            ("action_category", "action_category_scope",),
            ((_val1, str(_val2)) for _val1, _val2 in data["action_category_scope"].items())
        )


class ActionCategoryScopeAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionCategoryScopeAdd, self).get_parser(prog_name)
        parser.add_argument(
            'action_category',
            metavar='<action_category-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            'action_category_scope',
            metavar='<action_category_scope-uuid>',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope".format(parsed_args.intraextension),
                                post_data={
                                    "action_category_id": parsed_args.action_category,
                                    "action_category_scope_id": parsed_args.action_category_scope,
                                },
                                authtoken=True)
        if "action_category_scope" not in data:
            raise Exception("Error in command {}".format(data))
        return (
            ("action_category", "action_category_scope",),
            ((_val1, str(_val2)) for _val1, _val2 in data["action_category_scope"].items())
        )


class ActionCategoryScopeDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionCategoryScopeDelete, self).get_parser(prog_name)
        parser.add_argument(
            'action_category',
            metavar='<action_category-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            'action_category_scope',
            metavar='<action_category_scope-uuid>',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_category_scope/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.action_category,
            parsed_args.action_category_scope
        ),
            method="DELETE",
            authtoken=True)