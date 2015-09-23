# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class SubjectScopesList(Lister):
    """List all subject scopes."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectScopesList, self).get_parser(prog_name)
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

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_scopes/{}".format(
            parsed_args.intraextension,
            parsed_args.subject_category_id),
            authtoken=True)
        return (
            ("id", "name", "description"),
            ((_id, data[_id]["name"], data[_id]["description"]) for _id in data)
        )


class SubjectScopesAdd(Command):
    """Add a new subject scope."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectScopesAdd, self).get_parser(prog_name)
        parser.add_argument(
            'subject_category_id',
            metavar='<subject-category-uuid>',
            help='Subject category UUID',
        )
        parser.add_argument(
            'subject_scope_name',
            metavar='<subject-scope-str>',
            help='Subject scope Name',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_scopes/{}".format(
            parsed_args.intraextension, parsed_args.subject_category_id),
            post_data={
                "subject_scope_name": parsed_args.subject_scope_name,
                "subject_scope_description": parsed_args.description,
            },
            authtoken=True)
        return (
            ("id", "name", "description"),
            ((_id, data[_id]["name"], data[_id]["description"]) for _id in data)
        )


class SubjectScopesDelete(Command):
    """Delete a subject scope."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectScopesDelete, self).get_parser(prog_name)
        parser.add_argument(
            'subject_category_id',
            metavar='<subject-category-uuid>',
            help='Subject category  UUID',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_scopes/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.subject_category_id,
            parsed_args.subject_scope_id
        ),
            method="DELETE",
            authtoken=True
        )