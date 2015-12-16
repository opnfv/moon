# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command
from cliff.show import ShowOne


class RulesList(Lister):
    """List all rules."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(RulesList, self).get_parser(prog_name)
        parser.add_argument(
            'submetarule_id',
            metavar='<submetarule-uuid>',
            help='Sub Meta Rule UUID',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def __get_subject_category_name(self, intraextension, category_id):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/subject_categories".format(intraextension),
                                authtoken=True)
        if category_id in data:
            return data[category_id]["name"]

    def __get_object_category_name(self, intraextension, category_id):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/object_categories".format(intraextension),
                                authtoken=True)
        if category_id in data:
            return data[category_id]["name"]

    def __get_action_category_name(self, intraextension, category_id):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/action_categories".format(intraextension),
                                authtoken=True)
        if category_id in data:
            return data[category_id]["name"]

    def __get_subject_scope_name(self, intraextension, category_id, scope_id):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/subject_scopes/{}".format(intraextension, category_id),
                                authtoken=True)
        if scope_id in data:
            return data[scope_id]["name"]
        return scope_id

    def __get_object_scope_name(self, intraextension, category_id, scope_id):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/object_scopes/{}".format(intraextension, category_id),
                                authtoken=True)
        if scope_id in data:
            return data[scope_id]["name"]
        return scope_id

    def __get_action_scope_name(self, intraextension, category_id, scope_id):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/action_scopes/{}".format(intraextension, category_id),
                                authtoken=True)
        if scope_id in data:
            return data[scope_id]["name"]
        return scope_id

    def __get_headers(self, intraextension, submetarule_id):
        headers = list()
        headers.append("")
        headers.append("id")
        self.sub_meta_rules = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/sub_meta_rules".format(intraextension),
                                               authtoken=True)
        for cat in self.sub_meta_rules[submetarule_id]["subject_categories"]:
            headers.append("s:" + self.__get_subject_category_name(intraextension, cat))
        for cat in self.sub_meta_rules[submetarule_id]["action_categories"]:
            headers.append("a:" + self.__get_action_category_name(intraextension, cat))
        for cat in self.sub_meta_rules[submetarule_id]["object_categories"]:
            headers.append("o:" + self.__get_object_category_name(intraextension, cat))
        headers.append("enabled")
        return headers

    def __get_data(self, intraextension, submetarule_id, data_dict):
        rules = list()
        cpt = 0
        for key in data_dict:
            sub_rule = list()
            sub_rule.append(cpt)
            cpt += 1
            sub_rule.append(key)
            rule_item = list(data_dict[key])
            for cat in self.sub_meta_rules[submetarule_id]["subject_categories"]:
                sub_rule.append(self.__get_subject_scope_name(intraextension, cat, rule_item.pop(0)))
            for cat in self.sub_meta_rules[submetarule_id]["action_categories"]:
                sub_rule.append(self.__get_action_scope_name(intraextension, cat, rule_item.pop(0)))
            for cat in self.sub_meta_rules[submetarule_id]["object_categories"]:
                sub_rule.append(self.__get_object_scope_name(intraextension, cat, rule_item.pop(0)))
            sub_rule.append(rule_item.pop(0))
            rules.append(sub_rule)
        return rules

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/rule/{}".format(
            parsed_args.intraextension,
            parsed_args.submetarule_id,
        ),
            authtoken=True)
        self.log.debug(data)
        headers = self.__get_headers(parsed_args.intraextension, parsed_args.submetarule_id)
        data_list = self.__get_data(parsed_args.intraextension, parsed_args.submetarule_id, data)
        return (
            headers,
            data_list
        )


class RuleAdd(Command):
    """Add a new rule."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(RuleAdd, self).get_parser(prog_name)
        parser.add_argument(
            'submetarule_id',
            metavar='<submetarule-uuid>',
            help='Sub Meta Rule UUID',
        )
        parser.add_argument(
            'rule',
            metavar='<argument-list>',
            help='Rule list (example: admin,start,servers) with that ordering: subject, action, object',
        )
        parser.add_argument(
            '--intraextension',
            metavar='<intraextension-uuid>',
            help='IntraExtension UUID',
        )
        return parser

    def __get_subject_scope_id(self, intraextension, category_id, scope_name):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/subject_scopes/{}".format(intraextension, category_id),
                                authtoken=True)
        self.log.debug("__get_subject_scope_id {}".format(data))
        for scope_id in data:
            if data[scope_id]["name"] == scope_name:
                return scope_id
        return scope_name

    def __get_object_scope_id(self, intraextension, category_id, scope_name):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/object_scopes/{}".format(intraextension, category_id),
                                authtoken=True)
        self.log.debug("__get_action_scope_id {}".format(data))
        for scope_id in data:
            if data[scope_id]["name"] == scope_name:
                return scope_id
        return scope_name

    def __get_action_scope_id(self, intraextension, category_id, scope_name):
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/action_scopes/{}".format(intraextension, category_id),
                                authtoken=True)
        self.log.debug("__get_object_scope_id {}".format(data))
        for scope_id in data:
            if data[scope_id]["name"] == scope_name:
                return scope_id
        return scope_name

    def take_action(self, parsed_args):
        if not parsed_args.intraextension:
            parsed_args.intraextension = self.app.intraextension
        self.sub_meta_rules = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/sub_meta_rules".format(
            parsed_args.intraextension),
            authtoken=True)
        new_rule = map(lambda x: x.strip(), parsed_args.rule.split(","))
        post = {
            "subject_categories": [],
            "object_categories": [],
            "action_categories": [],
            "enabled": True
        }
        for cat in self.sub_meta_rules[parsed_args.submetarule_id]["subject_categories"]:
            self.log.debug("annalysing s {}".format(cat))
            post["subject_categories"].append(self.__get_subject_scope_id(
                parsed_args.intraextension, cat, new_rule.pop(0))
            )
        for cat in self.sub_meta_rules[parsed_args.submetarule_id]["action_categories"]:
            self.log.debug("annalysing a {}".format(cat))
            post["action_categories"].append(self.__get_action_scope_id(
                parsed_args.intraextension, cat, new_rule.pop(0))
            )
        for cat in self.sub_meta_rules[parsed_args.submetarule_id]["object_categories"]:
            self.log.debug("annalysing o {}".format(cat))
            post["object_categories"].append(self.__get_object_scope_id(
                parsed_args.intraextension, cat, new_rule.pop(0))
            )
        data = self.app.get_url(self.app.url_prefix+"/intra_extensions/{}/rule/{}".format(
            parsed_args.intraextension, parsed_args.submetarule_id),
            post_data=post,
            authtoken=True)


class RuleDelete(Command):
    """Delete a new rule."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(RuleDelete, self).get_parser(prog_name)
        parser.add_argument(
            'submetarule_id',
            metavar='<submetarule-uuid>',
            help='Sub Meta Rule UUID',
        )
        parser.add_argument(
            'rule_id',
            metavar='<rule-uuid>',
            help='Rule UUID',
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
        self.app.get_url(
            self.app.url_prefix+"/intra_extensions/{intra_extensions_id}/rule/{submetarule_id}/{rule_id}".format(
                intra_extensions_id=parsed_args.intraextension,
                submetarule_id=parsed_args.submetarule_id,
                rule_id=parsed_args.rule_id
            ),
            method="DELETE",
            authtoken=True
        )
