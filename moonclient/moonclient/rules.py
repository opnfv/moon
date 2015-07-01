# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command
from cliff.show import ShowOne


class RulesList(ShowOne):
    """List all aggregation algorithms."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(RulesList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/sub_rules".format(
            parsed_args.intraextension),
            authtoken=True)
        if "sub_rules" not in data:
            raise Exception("Error in command {}: {}".format("RulesList", data))
        # TODO (dthom): a better view with a Lister
        return (
            ("sub_rules",),
            (data["sub_rules"],)
        )


class RuleAdd(ShowOne):
    """List the current aggregation algorithm."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(RuleAdd, self).get_parser(prog_name)
        parser.add_argument(
            'relation',
            metavar='<relation-uuid>',
            help='Relation UUID',
        )
        parser.add_argument(
            'rule',
            metavar='<argument-list>',
            help='Rule list (example: admin,vm_admin,servers)',
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
        rule = parsed_args.rule.split(",")
        post = {
            "rule": rule,
            "relation": parsed_args.relation
        }
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{intraextension}/sub_rules".format(
            intraextension=parsed_args.intraextension),
            post_data=post,
            authtoken=True)
        if "sub_rules" not in data:
            raise Exception("Error in command {}: {}".format("RuleAdd", data))
        return (
            ("sub_rules",),
            (data["sub_rules"],)
        )


class RuleDelete(ShowOne):
    """Set the current aggregation algorithm."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(RuleDelete, self).get_parser(prog_name)
        parser.add_argument(
            'relation',
            metavar='<relation-uuid>',
            help='Relation UUID',
        )
        parser.add_argument(
            'rule',
            metavar='<argument-list>',
            help='Rule list (example: admin,vm_admin,servers)',
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
        rule = "+".join(parsed_args.rule.split(","))
        data = self.app.get_url(
            "/v3/OS-MOON/intra_extensions/{intra_extensions_id}/sub_rules/{relation_name}/{rule}".format(
                intra_extensions_id=parsed_args.intraextension,
                relation_name=parsed_args.relation,
                rule=rule,
            ),
            method="DELETE",
            authtoken=True)
        if "sub_rules" not in data:
            raise Exception("Error in command {}: {}".format("RuleDelete", data))
        return (
            ("sub_rules",),
            (data["sub_rules"],)
        )
