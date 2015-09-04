# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
import json
import shlex
import re
from cliff.lister import Lister
from cliff.command import Command


class TestsLaunch(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)
    result_vars = dict()

    def get_parser(self, prog_name):
        parser = super(TestsLaunch, self).get_parser(prog_name)
        parser.add_argument(
            '--testfile',
            metavar='<filename>',
            help='Filename that contains tests to run',
        )
        return parser

    def __replace_var_in_str(self, data_str):
        for exp in re.findall("\$\w+"):
            if exp.replace("$", "") in self.result_vars:
                data_str.replace(exp, self.result_vars[exp.replace("$", "")])
        return data_str

    def __compare_results(self, expected, observed):
        if expected in observed:
            return True
        return False

    def take_action(self, parsed_args):
        tests_dict = json.load(open(parsed_args.testfile))
        data = list()
        for group_name, tests_list in tests_dict.iteritems():
            for test in tests_list:
                data_tmp = list()
                command = self.__replace_var_in_str(test["command"])
                result = self.app.run_subcommand(shlex.split(command))
                data_tmp.append(test["name"])
                data_tmp.append(self.__compare_results(test["result"], result))
                data_tmp.append(test["description"])
                data.append(data_tmp)

        return (
            ("test_name", "result", "description"),
            data
        )
