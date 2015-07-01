# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ObjectCategoryScopeList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectCategoryScopeList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope".format(parsed_args.intraextension),
                                authtoken=True)
        if "object_category_scope" not in data:
            raise Exception("Error in command {}: {}".format("ObjectCategoryScopeList", data))
        return (
            ("object_category", "object_category_scope",),
            ((_val1, str(_val2)) for _val1, _val2 in data["object_category_scope"].items())
        )


class ObjectCategoryScopeAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectCategoryScopeAdd, self).get_parser(prog_name)
        parser.add_argument(
            'object_category',
            metavar='<object_category-uuid>',
            help='Object UUID',
        )
        parser.add_argument(
            'object_category_scope',
            metavar='<object_category_scope-uuid>',
            help='Object Scope UUID',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope".format(parsed_args.intraextension),
                                post_data={
                                    "object_category_id": parsed_args.object_category,
                                    "object_category_scope_id": parsed_args.object_category_scope,
                                },
                                authtoken=True)
        if "object_category_scope" not in data:
            raise Exception("Error in command {}".format(data))
        return (
            ("object_category", "object_category_scope",),
            ((_val1, str(_val2)) for _val1, _val2 in data["object_category_scope"].items())
        )


class ObjectCategoryScopeDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectCategoryScopeDelete, self).get_parser(prog_name)
        parser.add_argument(
            'object_category',
            metavar='<object_category-uuid>',
            help='Object UUID',
        )
        parser.add_argument(
            'object_category_scope',
            metavar='<object_category_scope-uuid>',
            help='Object Scope UUID',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_category_scope/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.object_category,
            parsed_args.object_category_scope
        ),
            method="DELETE",
            authtoken=True)