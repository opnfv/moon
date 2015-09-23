# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class SubjectAssignmentsList(Lister):
    """List all subject assignments."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectAssignmentsList, self).get_parser(prog_name)
        parser.add_argument(
            'subject_id',
            metavar='<subject-uuid>',
            help='Subject UUID',
        )
        parser.add_argument(
            'subject_category_id',
            metavar='<subject-category-uuid>',
            help='Subject category UUID',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def __get_scope_from_id(self, intraextension_id, subject_category_id, subject_scope_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_scopes/{}".format(
            intraextension_id, subject_category_id),
            authtoken=True)
        if subject_scope_id in data:
            return data[subject_scope_id]

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_assignments/{}/{}".format(
            parsed_args.intraextension, parsed_args.subject_id, parsed_args.subject_category_id),
            authtoken=True)
        return (
            ("id", "name"),
            ((_id, self.__get_scope_from_id(parsed_args.intraextension,
                                            parsed_args.subject_category_id,
                                            _id)['name']) for _id in data)
        )


class SubjectAssignmentsAdd(Command):
    """Add a new subject assignment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectAssignmentsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'subject_id',
            metavar='<subject-uuid>',
            help='Subject UUID',
        )
        parser.add_argument(
            'subject_category_id',
            metavar='<subject-category-uuid>',
            help='Subject category id',
        )
        parser.add_argument(
            'subject_scope_id',
            metavar='<subject-scope-uuid>',
            help='Subject scope UUID',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def __get_scope_from_id(self, intraextension_id, subject_category_id, subject_scope_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_scopes/{}".format(
            intraextension_id, subject_category_id),
            authtoken=True)
        if subject_scope_id in data:
            return data[subject_scope_id]

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_assignments".format(parsed_args.intraextension),
                                post_data={
                                    "subject_id": parsed_args.subject_id,
                                    "subject_category_id": parsed_args.subject_category_id,
                                    "subject_scope_id": parsed_args.subject_scope_id},
                                authtoken=True)
        return (
            ("id", "name"),
            ((_id, self.__get_scope_from_id(parsed_args.intraextension,
                                            parsed_args.subject_category_id,
                                            _id)['name']) for _id in data)
        )


class SubjectAssignmentsDelete(Command):
    """Delete a subject assignment."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectAssignmentsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'subject_id',
            metavar='<subject-uuid>',
            help='Subject UUID',
        )
        parser.add_argument(
            'subject_category_id',
            metavar='<subject-category-uuid>',
            help='Subject category UUID',
        )
        parser.add_argument(
            'subject_scope_id',
            metavar='<subject-scope-uuid>',
            help='Subject scope UUID',
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
            parsed_args.subject_category_id,
            parsed_args.subject_scope_id),
            method="DELETE",
            authtoken=True
        )