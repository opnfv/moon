# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ObjectCategoriesList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectCategoriesList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(parsed_args.intraextension),
                                authtoken=True)
        return (
            ("id", "name", "description"),
            ((_uuid, data[_uuid]["name"], data[_uuid]["description"]) for _uuid in data)
        )


class ObjectCategoriesAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectCategoriesAdd, self).get_parser(prog_name)
        parser.add_argument(
            'object_category',
            metavar='<object_category-uuid>',
            help='Object UUID',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(parsed_args.intraextension),
                                post_data={
                                    "object_category_name": parsed_args.object_category,
                                    "object_category_description": parsed_args.description,
                                },
                                authtoken=True)
        return (
            ("id", "name", "description"),
            ((_uuid, data[_uuid]["name"], data[_uuid]["description"]) for _uuid in data)
        )


class ObjectCategoriesDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectCategoriesDelete, self).get_parser(prog_name)
        parser.add_argument(
            'object_category',
            metavar='<object_category-uuid>',
            help='Object UUID',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_categories/{}".format(
            parsed_args.intraextension,
            parsed_args.object_category
        ),
            method="DELETE",
            authtoken=True)