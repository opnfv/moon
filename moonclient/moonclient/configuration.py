# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister


class TemplatesList(Lister):
    """List all policy templates."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TemplatesList, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        templates = self.app.get_url("/v3/OS-MOON/configuration/templates", authtoken=True)
        self.app.stdout.write(templates)
        self.app.stdout.write("\n")
        return (
            ("id", "name", "description"),
            ((template_id, templates[template_id]["name"], templates[template_id]["description"])
             for template_id in templates)
        )


class AggregationAlgorithmsList(Lister):
    """List all aggregation algorithms."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(AggregationAlgorithmsList, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        templates = self.app.get_url("/v3/OS-MOON/configuration/aggregation_algorithms", authtoken=True)
        self.app.stdout.write(templates)
        self.app.stdout.write("\n")
        return (
            ("id", "name", "description"),
            ((template_id, templates[template_id]["name"], templates[template_id]["description"])
             for template_id in templates)
        )


class SubMetaRuleAlgorithmsList(Lister):
    """List all aggregation algorithms."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SubMetaRuleAlgorithmsList, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        templates = self.app.get_url("/v3/OS-MOON/configuration/sub_meta_rule_algorithms", authtoken=True)
        self.app.stdout.write(templates)
        self.app.stdout.write("\n")
        return (
            ("id", "name", "description"),
            ((template_id, templates[template_id]["name"], templates[template_id]["description"])
             for template_id in templates)
        )


