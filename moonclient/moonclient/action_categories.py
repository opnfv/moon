# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ActionCategoriesList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionCategoriesList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(parsed_args.intraextension),
                                authtoken=True)
        return (
            ("id", "name", "description"),
            ((_uuid, data[_uuid]["name"], data[_uuid]["description"]) for _uuid in data)
        )


class ActionCategoriesAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionCategoriesAdd, self).get_parser(prog_name)
        parser.add_argument(
            'action_category',
            metavar='<action_category-uuid>',
            help='Action UUID',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        parser.add_argument(
            '--description',
            metavar='<description-str>',
            help='Category description',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(parsed_args.intraextension),
                                post_data={
                                    "action_category_name": parsed_args.action_category,
                                    "action_category_description": parsed_args.description,
                                },
                                authtoken=True)
        return (
            ("id", "name", "description"),
            ((_uuid, data[_uuid]["name"], data[_uuid]["description"]) for _uuid in data)
        )


class ActionCategoriesDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionCategoriesDelete, self).get_parser(prog_name)
        parser.add_argument(
            'action_category',
            metavar='<action_category-uuid>',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_categories/{}".format(
            parsed_args.intraextension,
            parsed_args.action_category
        ),
            method="DELETE",
            authtoken=True)