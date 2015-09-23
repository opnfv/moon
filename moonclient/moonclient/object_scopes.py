# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ObjectScopesList(Lister):
    """List all object scopes."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectScopesList, self).get_parser(prog_name)
        parser.add_argument(
            'object_category_id',
            metavar='<object-category-uuid>',
            help='Object category UUID',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_scopes/{}".format(
            parsed_args.intraextension, parsed_args.object_category_id),
            authtoken=True)
        self.log.debug(data)  # TODO: why log here?
        return (
            ("id", "name", "description"),
            ((_id, data[_id]["name"], data[_id]["description"]) for _id in data)
        )


class ObjectScopesAdd(Command):
    """Add a new object scope."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectScopesAdd, self).get_parser(prog_name)
        parser.add_argument(
            'object_category_id',
            metavar='<object-category-uuid>',
            help='Object category UUID',
        )
        parser.add_argument(
            'object_scope_name',
            metavar='<object-scope-str>',
            help='Object scope name',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        parser.add_argument(
            '--description',
            metavar='<description-str>',
            help='Description',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_scopes/{}".format(
            parsed_args.intraextension, parsed_args.object_category_id),
            post_data={
                "object_scope_name": parsed_args.object_scope_name,
                "object_scope_description": parsed_args.description,
                },
            authtoken=True)
        return (
            ("id", "name", "description"),
            ((_id, data[_id]["name"], data[_id]["description"]) for _id in data)
        )


class ObjectScopesDelete(Command):
    """Delete an object scope."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectScopesDelete, self).get_parser(prog_name)
        parser.add_argument(
            'object_category_id',
            metavar='<object-category-uuid>',
            help='Object category  UUID',
        )
        parser.add_argument(
            'object_scope_id',
            metavar='<object-scope-uuid>',
            help='Object scope UUID',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_scopes/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.object_category_id,
            parsed_args.object_scope_id
        ),
            method="DELETE",
            authtoken=True
        )