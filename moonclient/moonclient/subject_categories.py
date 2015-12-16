# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class SubjectCategoriesList(Lister):
    """List all subject categories."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectCategoriesList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/subject_categories".format(parsed_args.intraextension),
                                authtoken=True)
        return (
            ("id", "name", "description"),
            ((_uuid, data[_uuid]["name"], data[_uuid]["description"]) for _uuid in data)
        )


class SubjectCategoriesAdd(Command):
    """Add a new subject category."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectCategoriesAdd, self).get_parser(prog_name)
        parser.add_argument(
            'subject_category_name',
            metavar='<subject_category-name>',
            help='Subject category name',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        parser.add_argument(
            '--description',
            metavar='<description-str>',
            help='Subject category description',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/subject_categories".format(parsed_args.intraextension),
                                post_data={
                                    "subject_category_name": parsed_args.subject_category_name,
                                    "subject_category_description": parsed_args.description},
                                authtoken=True)
        return (
            ("id", "name", "description"),
            ((_uuid, data[_uuid]["name"], data[_uuid]["description"]) for _uuid in data)
        )


class SubjectCategoriesDelete(Command):
    """Delete a subject category."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubjectCategoriesDelete, self).get_parser(prog_name)
        parser.add_argument(
            'subject_category_id',
            metavar='<subject_category-uuid>',
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
        self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/subject_categories/{}".format(
            parsed_args.intraextension,
            parsed_args.subject_category_id),
            method="DELETE",
            authtoken=True
        )