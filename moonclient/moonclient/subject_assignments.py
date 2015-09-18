# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class SubjectAssignmentsList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectAssignmentsList, self).get_parser(prog_name)
        parser.add_argument(
            'subject_id',
            metavar='<subject-uuid>',
            help='Subject UUID',
        )
        parser.add_argument(
            'category_id',
            metavar='<category-uuid>',
            help='Category UUID',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def __get_scope_from_id(self, intraextension_id, category_id, scope_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_scopes/{}".format(
            intraextension_id, category_id),
            authtoken=True)
        if scope_id in data:
            return data[scope_id]

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_assignments/{}/{}".format(
            parsed_args.intraextension, parsed_args.subject_id, parsed_args.category_id),
            authtoken=True)
        return (
            ("id", "name"),
            ((_id, self.__get_scope_from_id(parsed_args.intraextension, parsed_args.category_id, _id)['name']) for _id in data)
        )


class SubjectAssignmentsAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectAssignmentsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'subject_id',
            metavar='<subject-uuid>',
            help='Subject UUID',
        )
        parser.add_argument(
            'subject_category',
            metavar='<subject_category-uuid>',
            help='Subject Category',
        )
        parser.add_argument(
            'subject_category_scope',
            metavar='<subject_category_scope-uuid>',
            help='Subject Category Scope',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def __get_scope_from_id(self, intraextension_id, category_id, scope_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_scopes/{}".format(
            intraextension_id, category_id),
            authtoken=True)
        if scope_id in data:
            return data[scope_id]

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_assignments".format(parsed_args.intraextension),
                                post_data={
                                    "subject_id": parsed_args.subject_id,
                                    "subject_category_id": parsed_args.subject_category,
                                    "subject_scope_id": parsed_args.subject_category_scope
                                },
                                authtoken=True)
        return (
            ("id", "name"),
            ((_id, self.__get_scope_from_id(parsed_args.intraextension, parsed_args.category_id, _id)['name']) for _id in data)
        )


class SubjectAssignmentsDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectAssignmentsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'subject_id',
            metavar='<subject-uuid>',
            help='Subject UUID',
        )
        parser.add_argument(
            'subject_category',
            metavar='<subject_category>',
            help='Subject Category',
        )
        parser.add_argument(
            'subject_category_scope',
            metavar='<subject_category_scope>',
            help='Subject Category Scope',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_assignments/{}/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.subject_id,
            parsed_args.subject_category,
            parsed_args.subject_category_scope
        ),
            method="DELETE",
            authtoken=True)