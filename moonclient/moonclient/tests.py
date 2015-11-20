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
from uuid import uuid4
import os
import time
import subprocess


class TestsLaunch(Lister):
    """Tests launcher."""

    log = logging.getLogger(__name__)
    result_vars = dict()
    logfile_name = "/tmp/moonclient_test_{}.log".format(time.strftime("%Y%m%d-%H%M%S"))
    logfile = open(logfile_name, "w")

    def get_parser(self, prog_name):
        parser = super(TestsLaunch, self).get_parser(prog_name)
        parser.add_argument(
            'testfile',
            metavar='<filename>',
            help='Filename that contains tests to run',
        )
        return parser

    def __replace_var_in_str(self, data_str):
        self.log.debug("__replace_var_in_str " + data_str)
        for exp in re.findall("\$\w+", data_str):
            self.log.debug("--->" + exp + str(self.result_vars))
            if exp.replace("$", "") in self.result_vars:
                data_str = re.sub(exp.replace("$", "\$") + "(?!\w)", self.result_vars[exp.replace("$", "")], data_str)
        self.log.debug("__replace_var_in_str " + data_str)
        return data_str

    def __compare_results(self, expected, observed):
        match = re.search(expected, observed)
        if match:
            self.result_vars.update(match.groupdict())
            return True
        return False

    def take_action(self, parsed_args):
        self.log.info("Write tests output to {}".format(self.logfile_name))
        stdout_back = self.app.stdout
        if not parsed_args.testfile:
            self.log.error("You don't give a test filename.")
            raise Exception("Cannot execute tests.")
        tests_dict = json.load(open(parsed_args.testfile))
        self.log.debug("tests_dict = {}".format(tests_dict))
        global_command_options = ""
        if "command_options" in tests_dict:
            global_command_options = tests_dict["command_options"]
        data = list()
        for group_name, tests_list in tests_dict["tests_group"].iteritems():
            overall_result = True
            self.log.info("\n\033[1mgroup {}\033[0m".format(group_name))
            self.logfile.write("{}:\n\n".format(group_name))
            test_count = len(tests_list)
            for test in tests_list:
                result_str = ""
                error_str = ""
                if "auth_name" in test or "auth_password" in test or "auth_url" in test:
                    username = None
                    password = None
                    host = None
                    port = None
                    description = ""
                    if "auth_name" in test:
                        username = test["auth_name"]
                    if "auth_password" in test:
                        password = test["auth_password"]
                    if "auth_host" in test:
                        host = test["auth_host"]
                    if "auth_port" in test:
                        port = test["auth_port"]
                    if "description" in test:
                        description = test["description"]
                    self.app.auth_keystone(username, password, host, port)
                    title = "Change auth to "
                    if username:
                        title += username
                    if host:
                        title += "@" + host
                    if port:
                        title += ":" + port
                    title += "\n"
                    self.logfile.write(title + "\n")
                    self.log.info(title)
                    data_tmp = list()
                    data_tmp.append("")
                    data_tmp.append(title.strip())
                    data_tmp.append("\033[32mOK\033[m")
                    data_tmp.append(description.strip())
                    data.append(data_tmp)
                    continue
                data_tmp = list()
                tmp_filename = os.path.join("/tmp", uuid4().hex)
                tmp_filename_fd = open(tmp_filename, "w")
                self.log.debug("test={}".format(test))
                if "command" not in test:
                    if "external_command" in test:
                        ext_command = test["external_command"]
                    else:
                        ext_command = test["shell_command"]
                    ext_command = self.__replace_var_in_str(ext_command)
                    self.logfile.write("-----> {}\n".format(ext_command))
                    self.log.info("    \\-executing external \"{}\"".format(ext_command))
                    if "external_command" in test:
                        pipe = subprocess.Popen(shlex.split(ext_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    else:
                        # Note (asteroide): security hazard! Must reduce the possible commands here.
                        pipe = subprocess.Popen(ext_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    com = pipe.communicate()
                    result_str = com[0]
                    error_str = com[1]
                    self.logfile.write("stdout: {}\n".format(result_str))
                    self.logfile.write("stderr: {}\n".format(error_str))
                if "command" in test:
                    if "command_options" in test:
                        command = test["command"] + " " + test["command_options"]
                    else:
                        command = test["command"] + " " + global_command_options
                    command = self.__replace_var_in_str(command)
                    self.logfile.write("-----> {}\n".format(command))
                    self.log.info("    \\-executing {}".format(command))
                    self.app.stdout = tmp_filename_fd
                    result_id = self.app.run_subcommand(shlex.split(command))
                    tmp_filename_fd.close()
                    self.app.stdout = stdout_back
                    result_str = open(tmp_filename, "r").read()
                    self.logfile.write("{}".format(result_str))
                data_tmp.append(group_name)
                data_tmp.append(test["name"])
                compare = self.__compare_results(self.__replace_var_in_str(test["result"]), result_str)
                self.logfile.write("\\---->{}: {}\n\n".format(compare, self.__replace_var_in_str(test["result"])))
                if error_str:
                    if compare:
                        compare = "\033[33mTrue\033[m"
                        overall_result = overall_result and True
                    else:
                        compare = "\033[1m\033[31mFalse\033[m"
                        overall_result = overall_result and False
                else:
                    overall_result = overall_result and compare
                    if compare:
                        if overall_result:
                            compare = "\033[32mTrue\033[m"
                        else:
                            compare = "\033[mTrue\033[m"
                    else:
                        compare = "\033[1m\033[31mFalse\033[m"
                data_tmp.append(compare)
                data_tmp.append(test["description"])
                data.append(data_tmp)
            data_tmp = list()
            data_tmp.append("\033[1m" + group_name + "\033[m")
            data_tmp.append("\033[1mOverall results ({})\033[m".format(test_count))
            if overall_result:
                data_tmp.append("\033[1m\033[32mTrue\033[m")
            else:
                data_tmp.append("\033[1m\033[31mFalse\033[m")
            data_tmp.append(self.logfile_name)
            data.append(data_tmp)

        return (
            ("group_name", "test_name", "result", "description"),
            data
        )
