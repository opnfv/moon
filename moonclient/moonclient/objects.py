# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command


class ObjectsList(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectsList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(parsed_args.intraextension),
                                authtoken=True)
        if "objects" not in data:
            raise Exception("Error in command {}: {}".format("ObjectsList", data))
        return (
            ("objects",),
            ((_uuid, ) for _uuid in data["objects"])
        )


class ObjectsAdd(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectsAdd, self).get_parser(prog_name)
        parser.add_argument(
            'object',
            metavar='<object-uuid>',
            help='Object UUID',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/objects".format(parsed_args.intraextension),
                                post_data={"object_id": parsed_args.object},
                                authtoken=True)
        if "objects" not in data:
            raise Exception("Error in command {}".format(data))
        return (
            ("objects",),
            ((_uuid, ) for _uuid in data["objects"])
        )


class ObjectsDelete(Command):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ObjectsDelete, self).get_parser(prog_name)
        parser.add_argument(
            'object',
            metavar='<object-uuid>',
            help='Object UUID',
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
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/objects/{}".format(
            parsed_args.intraextension,
            parsed_args.object
        ),
            method="DELETE",
            authtoken=True)