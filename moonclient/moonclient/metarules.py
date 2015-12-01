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

    def __get_aggregation_algorithm_from_id(self, algorithm_id):
        algorithms = self.app.get_url("/v3/OS-MOON/configuration/aggregation_algorithms", authtoken=True)
        if algorithm_id in algorithms:
            return algorithms[algorithm_id]
        return dict()

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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithm".format(
            parsed_args.intraextension),
            authtoken=True)
        algorithm = self.__get_aggregation_algorithm_from_id(data['aggregation_algorithm'])
        return (
            ("id", "name", "description"),
            ((data['aggregation_algorithm'], algorithm["name"], algorithm["description"]), )
        )


class AggregationAlgorithmSet(Command):
    """Set the current aggregation algorithm."""

    log = logging.getLogger(__name__)

    def __get_aggregation_algorithm_from_id(self, algorithm_id):
        algorithms = self.app.get_url("/v3/OS-MOON/configuration/aggregation_algorithms", authtoken=True)
        if algorithm_id in algorithms:
            return algorithms[algorithm_id]
        return dict()

    def get_parser(self, prog_name):
        parser = super(AggregationAlgorithmSet, self).get_parser(prog_name)
        parser.add_argument(
            'aggregation_algorithm_id',
            metavar='<aggregation-algorithm-uuid>',
            help='Aggregation algorithm UUID',
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
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/aggregation_algorithm".format(
            parsed_args.intraextension),
            post_data={
                "aggregation_algorithm_id": parsed_args.aggregation_algorithm_id,
                "aggregation_algorithm_description": parsed_args.description},
            authtoken=True)
        algorithm = self.__get_aggregation_algorithm_from_id(data['aggregation_algorithm'])
        return (
            ("id",),
            (algorithm,)
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

    def __get_subject_category_name(self, intraextension, subject_category_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(intraextension),
                                authtoken=True)
        if subject_category_id in data:
            return data[subject_category_id]["name"]

    def __get_object_category_name(self, intraextension, object_category_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(intraextension),
                                authtoken=True)
        if object_category_id in data:
            return data[object_category_id]["name"]

    def __get_action_category_name(self, intraextension, action_category_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(intraextension),
                                authtoken=True)
        if action_category_id in data:
            return data[action_category_id]["name"]

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rules".format(parsed_args.intraextension),
                                authtoken=True)
        return (
            ("id", "name", "algorithm", "subject categories", "object categories", "action categories"),
            ((
                 key,
                 value["name"],
                 value["algorithm"],
                 ", ".join([self.__get_subject_category_name(parsed_args.intraextension, cat) for cat in value["subject_categories"]]),
                 ", ".join([self.__get_object_category_name(parsed_args.intraextension, cat) for cat in value["object_categories"]]),
                 ", ".join([self.__get_action_category_name(parsed_args.intraextension, cat) for cat in value["action_categories"]]),
             ) for key, value in data.iteritems())
        )


class SubMetaRuleSet(Command):
    """Set the current sub meta rule."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubMetaRuleSet, self).get_parser(prog_name)
        parser.add_argument(
            'submetarule_id',
            metavar='<sub-meta-rule-uuid>',
            help='Sub Meta Rule UUID (example: "12346")',
        )
        parser.add_argument(
            '--algorithm_name',
            metavar='<algorithm-str>',
            help='algorithm to use (example: "inclusion")',
        )
        parser.add_argument(
            '--name',
            metavar='<name-str>',
            help='name to set (example: "my new sub meta rule")',
        )
        parser.add_argument(
            '--subject_category_id',
            metavar='<subject-category-uuid>',
            help='subject category UUID (example: "12346,")',
        )
        parser.add_argument(
            '--object_category_id',
            metavar='<object-category-uuid>',
            help='object category UUID (example: "12346")',
        )
        parser.add_argument(
            '--action_category_id',
            metavar='<action-category-uuid>',
            help='action category UUID (example: "12346,0987654")',
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
        subject_category_id = parsed_args.subject_category_id
        if not subject_category_id:
            subject_category_id = ""
        object_category_id = parsed_args.object_category_id
        if not object_category_id:
            object_category_id = ""
        action_category_id = parsed_args.action_category_id
        if not action_category_id:
            action_category_id = ""
        subject_category_id = map(lambda x: x.strip(), subject_category_id.split(','))
        action_category_id = map(lambda x: x.strip(), action_category_id.split(','))
        object_category_id = map(lambda x: x.strip(), object_category_id.split(','))
        sub_meta_rule_id = parsed_args.submetarule_id
        post_data = dict()
        post_data["sub_meta_rule_name"] = parsed_args.name
        post_data["sub_meta_rule_algorithm"] = parsed_args.algorithm_name
        post_data["sub_meta_rule_subject_categories"] = filter(lambda x: x, subject_category_id)
        post_data["sub_meta_rule_object_categories"] = filter(lambda x: x, object_category_id)
        post_data["sub_meta_rule_action_categories"] = filter(lambda x: x, action_category_id)
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rules/{}".format(parsed_args.intraextension,
                                                                                    sub_meta_rule_id),
                         post_data=post_data,
                         method="POST",
                         authtoken=True)


