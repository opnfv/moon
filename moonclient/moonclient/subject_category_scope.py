# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class SubjectCategoryScopeList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectCategoryScopeList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope".format(parsed_args.intraextension),
                                authtoken=True)
        if "subject_category_scope" not in data:
            raise Exception("Error in command {}: {}".format("SubjectCategoryScopeList", data))
        return (
            ("subject_category", "subject_category_scope",),
            ((_val1, str(_val2)) for _val1, _val2 in data["subject_category_scope"].items())
        )


class SubjectCategoryScopeAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectCategoryScopeAdd, self).get_parser(prog_name)
        parser.add_argument(
            'subject_category',
            metavar='<subject_category-uuid>',
            help='Subject UUID',
        )
        parser.add_argument(
            'subject_category_scope',
            metavar='<subject_category_scope-uuid>',
            help='Subject UUID',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope".format(parsed_args.intraextension),
                                post_data={
                                    "subject_category_id": parsed_args.subject_category,
                                    "subject_category_scope_id": parsed_args.subject_category_scope,
                                },
                                authtoken=True)
        if "subject_category_scope" not in data:
            raise Exception("Error in command {}".format(data))
        return (
            ("subject_category", "subject_category_scope",),
            ((_val1, str(_val2)) for _val1, _val2 in data["subject_category_scope"].items())
        )


class SubjectCategoryScopeDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectCategoryScopeDelete, self).get_parser(prog_name)
        parser.add_argument(
            'subject_category',
            metavar='<subject_category-uuid>',
            help='Subject UUID',
        )
        parser.add_argument(
            'subject_category_scope',
            metavar='<subject_category_scope-uuid>',
            help='Subject UUID',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_category_scope/{}/{}".format(
            parsed_args.intraextension,
            parsed_args.subject_category,
            parsed_args.subject_category_scope
        ),
            method="DELETE",
            authtoken=True)