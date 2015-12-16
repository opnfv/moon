# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ActionsList(Lister):
    """List all actions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionsList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/actions".format(parsed_args.intraextension),
                                authtoken=True)
        return (
            ("id", "name", "description"),
            ((_uuid, data[_uuid]['name'], data[_uuid]['description']) for _uuid in data)
        )


class ActionsAdd(Command):
    """Add a new action."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'action_name',
            metavar='<action-name>',
            help='Action name',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        parser.add_argument(
            '--description',
            metavar='<description-str>',
            help='Action description',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/actions".format(parsed_args.intraextension),  # TODO: check method POST?
                                post_data={
                                    "action_name": parsed_args.action_name,
                                    "action_description": parsed_args.description},
                                authtoken=True)
        return (
            ("id", "name", "description"),
            ((_uuid, data[_uuid]['name'], data[_uuid]['description']) for _uuid in data)
        )


class ActionsDelete(Command):
    """Delete an action."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ActionsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'action_id',
            metavar='<action-uuid>',
            help='Action UUID',
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
        self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/actions/{}".format(
            parsed_args.intraextension,
            parsed_args.action_id),
            method="DELETE",
            authtoken=True
        )