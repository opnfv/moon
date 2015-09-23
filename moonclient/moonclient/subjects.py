# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class SubjectsList(Lister):
    """List all subjects."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectsList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(parsed_args.intraextension),
                                authtoken=True)
        return (
            ("id", "name", "Keystone ID"),
            ((_uuid, data[_uuid]["name"], data[_uuid]["keystone_id"]) for _uuid in data)
        )


class SubjectsAdd(Command):
    """add a new subject."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'subject_name',
            metavar='<subject-name>',
            help='Subject name',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        parser.add_argument(
            '--description',
            metavar='<description-str>',
            help='Subject description',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subjects".format(parsed_args.intraextension),
                                post_data={
                                    "subject_name": parsed_args.subject_name,
                                    "subject_description": parsed_args.description
                                    },
                                authtoken=True)
        return (
            ("id", "name", "Keystone ID"),
            ((_uuid, data[_uuid]["name"], data[_uuid]["keystone_id"]) for _uuid in data)
        )


class SubjectsDelete(Command):
    """Delete a subject."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'subject_id',
            metavar='<subject-uuid>',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subjects/{}".format(
            parsed_args.intraextension,
            parsed_args.subject_id
            ),
            method="DELETE",
            authtoken=True
        )