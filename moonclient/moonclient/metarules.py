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
        algorithm = self.__get_aggregation_algorithm_from_id(data['content'])
        return (
            ("id", "name", "description"),
            ((data['content'], algorithm["name"], algorithm["description"]), )
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
            post_data={"aggregation_algorithm_id": parsed_args.aggregation_algorithm},
            authtoken=True)
        algorithm = self.__get_aggregation_algorithm_from_id(data['content'])
        return (
            ("id", "name", "description"),
            ((data['content'], algorithm["name"], algorithm["description"]), )
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

    def __get_subject_category_name(self, intraextension, category_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/subject_categories".format(intraextension),
                                authtoken=True)
        if category_id in data:
            return data[category_id]["name"]

    def __get_object_category_name(self, intraextension, category_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/object_categories".format(intraextension),
                                authtoken=True)
        if category_id in data:
            return data[category_id]["name"]

    def __get_action_category_name(self, intraextension, category_id):
        data = self.app.get_url("/v3/OS-MOON/intra_extensions/{}/action_categories".format(intraextension),
                                authtoken=True)
        if category_id in data:
            return data[category_id]["name"]

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
            'id',
            metavar='<sub_meta_rule-uuid>',
            help='Sub Meta Rule UUID (example: "12346")',
        )
        parser.add_argument(
            '--algorithm',
            metavar='<algorithm-str>',
            help='algorithm to use (example: "inclusion")',
        )
        parser.add_argument(
            '--name',
            metavar='<name-str>',
            help='name to set (example: "my new sub meta rule")',
        )
        parser.add_argument(
            '--subject_categories',
            metavar='<subject_categories-uuid>',
            help='subject_categories UUID (example: "12346,")',
        )
        parser.add_argument(
            '--action_categories',
            metavar='<action_categories-uuid>',
            help='action_categories UUID (example: "12346,0987654")',
        )
        parser.add_argument(
            '--object_categories',
            metavar='<object_categories-uuid>',
            help='object_categories UUID (example: "12346")',
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
        subject_categories = parsed_args.subject_categories
        if not subject_categories:
            subject_categories = ""
        object_categories = parsed_args.object_categories
        if not object_categories:
            object_categories = ""
        action_categories = parsed_args.action_categories
        if not action_categories:
            action_categories = ""
        subject_categories = map(lambda x: x.strip(), subject_categories.split(','))
        action_categories = map(lambda x: x.strip(), action_categories.split(','))
        object_categories = map(lambda x: x.strip(), object_categories.split(','))
        sub_meta_rule_id = parsed_args.id
        post_data = dict()
        post_data["sub_meta_rule_name"] = parsed_args.name
        post_data["sub_meta_rule_algorithm"] = parsed_args.algorithm
        post_data["sub_meta_rule_subject_categories"] = filter(lambda x: x, subject_categories)
        post_data["sub_meta_rule_object_categories"] = filter(lambda x: x, object_categories)
        post_data["sub_meta_rule_action_categories"] = filter(lambda x: x, action_categories)
        self.app.get_url("/v3/OS-MOON/intra_extensions/{}/sub_meta_rules/{}".format(parsed_args.intraextension, sub_meta_rule_id),
                         post_data=post_data,
                         method="POST",
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


