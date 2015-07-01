# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command
from cliff.show import ShowOne


class AggregationAlgorithmsList(Lister):
    """List all aggregation algorithms."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(AggregationAlgorithmsList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithms".format(
            parsed_args.intraextension),
            authtoken=True)
        if "aggregation_algorithms" not in data:
            raise Exception("Error in command {}: {}".format("AggregationAlgorithmsList", data))
        return (
            ("aggregation_algorithms",),
            ((_uuid, ) for _uuid in data["aggregation_algorithms"])
        )


class AggregationAlgorithmShow(ShowOne):
    """List the current aggregation algorithm."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(AggregationAlgorithmShow, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithm".format(
            parsed_args.intraextension),
            authtoken=True)
        if "aggregation_algorithm" not in data:
            raise Exception("Error in command {}: {}".format("AggregationAlgorithmList", data))
        return (
            ("aggregation_algorithm",),
            (data["aggregation_algorithm"],)
        )


class AggregationAlgorithmSet(ShowOne):
    """Set the current aggregation algorithm."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(AggregationAlgorithmSet, self).get_parser(prog_name)
        parser.add_argument(
            'aggregation_algorithm',
            metavar='<aggregation_algorithm-uuid>',
            help='Aggregation algorithm UUID',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithm".format(
            parsed_args.intraextension),
            post_data={"aggregation_algorithm": parsed_args.aggregation_algorithm},
            authtoken=True)
        if "aggregation_algorithm" not in data:
            raise Exception("Error in command {}: {}".format("AggregationAlgorithmSet", data))
        return (
            ("aggregation_algorithm",),
            (data["aggregation_algorithm"],)
        )


class SubMetaRuleShow(Lister):
    """Show the current sub meta rule."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubMetaRuleShow, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rule".format(parsed_args.intraextension),
                                authtoken=True)
        if "sub_meta_rule" not in data:
            raise Exception("Error in command {}".format(data))
        return (
            ("relation", "values"),
            ((key, value) for key, value in data["sub_meta_rule"].items())
        )


class SubMetaRuleSet(Command):
    """Set the current sub meta rule."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubMetaRuleSet, self).get_parser(prog_name)
        parser.add_argument(
            'relation',
            metavar='<relation-uuid>',
            help='relation UUID (example: "relation_super")',
        )
        parser.add_argument(
            'subject_categories',
            metavar='<subject_categories-uuid>',
            help='subject_categories UUID (example: "role,")',
        )
        parser.add_argument(
            'action_categories',
            metavar='<action_categories-uuid>',
            help='action_categories UUID (example: "compute_action,network_action")',
        )
        parser.add_argument(
            'object_categories',
            metavar='<object_categories-uuid>',
            help='object_categories UUID (example: "id,")',
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
        subject_categories = map(lambda x: x.strip(), parsed_args.subject_categories.split(','))
        action_categories = map(lambda x: x.strip(), parsed_args.action_categories.split(','))
        object_categories = map(lambda x: x.strip(), parsed_args.object_categories.split(','))
        relation = parsed_args.relation
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rule".format(parsed_args.intraextension),
                         post_data={
                             relation: {
                                 "subject_categories": subject_categories,
                                 "action_categories": action_categories,
                                 "object_categories": object_categories,
                             }
                         },
                         method="DELETE",
                         authtoken=True)


class SubMetaRuleRelationList(Lister):
    """List all sub meta rule relations."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubMetaRuleRelationList, self).get_parser(prog_name)
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rule_relations".format(
            parsed_args.intraextension),
            authtoken=True)
        if "sub_meta_rule_relations" not in data:
            raise Exception("Error in command {}: {}".format("AggregationAlgorithmList", data))
        return (
            ("sub_meta_rule_relations",),
            ((_uuid, ) for _uuid in data["sub_meta_rule_relations"])
        )


