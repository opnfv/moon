# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ObjectAssignmentsList(Lister):
    """List all object assignments."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectAssignmentsList, self).get_parser(prog_name)
        parser.add_argument(
            'object_id',
            metavar='<object-uuid>',
            help='Object UUID',
        )
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

    def __get_scope_from_id(self, intraextension_id, object_category_id, object_scope_id):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/object_scopes/{}".format(
            intraextension_id, object_category_id),
            authtoken=True)
        if object_scope_id in data:
            return data[object_scope_id]

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/object_assignments/{}/{}".format(
            parsed_args.intraextension, parsed_args.object_id, parsed_args.object_category_id),
            authtoken=True)
        return (
            ("id", "name"),
            ((_id, self.__get_scope_from_id(parsed_args.intraextension,
                                            parsed_args.object_category_id,
                                            _id)['name']) for _id in data)
        )


class ObjectAssignmentsAdd(Command):
    """Add a new object assignment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectAssignmentsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'object_id',
            metavar='<object-uuid>',
            help='Object UUID',
        )
        parser.add_argument(
            'object_category_id',
            metavar='<object-category-uuid>',
            help='Object category UUID',
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

    def __get_scope_from_id(self, intraextension_id, object_category_id, object_scope_id):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/object_scopes/{}".format(
            intraextension_id, object_category_id),
            authtoken=True)
        if object_scope_id in data:
            return data[object_scope_id]

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/object_assignments".format(parsed_args.intraextension),
                                post_data={
                                    "object_id": parsed_args.object_id,
                                    "object_category_id": parsed_args.object_category_id,
                                    "object_scope_id": parsed_args.object_scope_id},
                                authtoken=True)
        return (
            ("id", "name"),
            ((_id, self.__get_scope_from_id(parsed_args.intraextension,
                                            parsed_args.object_category_id,
                                            _id)['name']) for _id in data)
        )


class ObjectAssignmentsDelete(Command):
    """Delete an object assignment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectAssignmentsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'object_id',
            metavar='<object-uuid>',
            help='Object UUID',
        )
        parser.add_argument(
            'object_category_id',
            metavar='<object-category-id>',
            help='Object category UUID',
        )
        parser.add_argument(
            'object_scope_id',
            metavar='<object-scope-id>',
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
        self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/object_assignments/{}/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.object_id,
            parsed_args.object_category_id,
            parsed_args.object_scope_id),
            method="DELETE",
            authtoken=True
        )