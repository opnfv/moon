# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Run tests from a Moon policy file.
"""

import json
import logging
import time
import requests
import hug
import sys
from moon_manager.api import configuration
from moon_manager.api import pdp

LOGGER = logging.getLogger("moon.manager.api." + __name__)
ChecksAPI = hug.API(name='checks', doc=__doc__)
if sys.version_info[0] == 2:
    raise Exception("Using Python2 is not secure enough!")


@hug.object(name='rules', version='1.0.0', api=ChecksAPI)
class ChecksCLI(object):
    """An example of command like calls via an Object"""

    verbose = False
    output_file = None
    pipeline_data = {}

    @staticmethod
    def launch_standalone_pipeline(endpoint, policy_file):
        LOGGER.info("Launching Engine for a self test...")
        from moon_engine.plugins import pyorchestrator
        from uuid import uuid4
        import subprocess  # nosec (command attribute is safe)
        host = endpoint.replace("http://", "").split(":")[0]
        port = endpoint.split(":")[2].split("/")[0]
        _uuid = uuid4().hex
        gunicorn_config = pyorchestrator.create_gunicorn_config(
            host, port, server_type="pipeline", uuid=_uuid)
        pyorchestrator.create_moon_config(_uuid, False, policy_file)
        pid_file = _uuid + ".pid"
        command = ["gunicorn", "moon_engine.server:__hug_wsgi__", "--threads", "10",
                   "-p", pid_file, "-D", "-c", gunicorn_config]
        LOGGER.info("Executing {}".format(" ".join(command)))
        subprocess.Popen(command, stdout=subprocess.PIPE, close_fds=True)  # nosec
        # (command attribute is safe)
        ChecksCLI.pipeline_data["pid_file"] = pid_file
        ChecksCLI.pipeline_data["gunicorn_config"] = gunicorn_config
        time.sleep(2)

    @staticmethod
    def kill_standalone_pipeline():
        import os
        pid = int(open(ChecksCLI.pipeline_data["pid_file"]).read())
        os.kill(pid, 15)

    @staticmethod
    def log(message, color="", force_console=False):
        """
        Send application logs to conole and output file
        :param message: the message to send
        :param color: optionally the color in the console
        :param force_console: if the message should be always send in the console
        :return: None
        """
        if ChecksCLI.verbose or force_console:
            if color:
                print("\033[" + color + "m" + message + "\033[m")
            else:
                print(message)
        if ChecksCLI.output_file:
            open(ChecksCLI.output_file, "a").write(message + "\n")

    @staticmethod
    def run_tests(endpoint, vim_project_id, test_list, status_code, test_number):
        """
        Run the tests given
        :param endpoint: the endpoint to send the requests
        :param vim_project_id: the tested project ID
        :param test_list: the list of tests to run
        :param status_code: the expected status code
        :param test_number: the number of tests to run
        :return:
        """
        cpt = 0
        bad_response = 0
        good_response = 0
        start_time = time.time()
        for test in test_list:
            if test_number and cpt > test_number:
                break
            if vim_project_id:
                url = "{endpoint}/{project_id}/{subject_name}/{object_name}/{action_name}".format(
                    endpoint=endpoint,
                    project_id=vim_project_id,
                    subject_name=test[0],
                    object_name=test[1],
                    action_name=test[2],
                )
            else:
                url = "{endpoint}/{subject_name}/{object_name}/{action_name}".format(
                    endpoint=endpoint,
                    subject_name=test[0],
                    object_name=test[1],
                    action_name=test[2],
                )
            req = requests.get(url)
            cpt += 1
            ChecksCLI.log("Contacting {}".format(url))
            if isinstance(status_code, str):
                status_code = (int(status_code), )
            if isinstance(status_code, int):
                status_code = (status_code, )
            if req.status_code in status_code:
                ChecksCLI.log("{} OK".format(", ".join(test)))
                good_response += 1
            else:
                ChecksCLI.log("{} KO ({}: {})".format(", ".join(test), req.status_code, req.text[:80]),
                              force_console=True)
                bad_response += 1
        end_time = time.time()
        return "Run {} tests ({} OK and {} KO) in {:.2f} seconds ({:.2f} req/s)".format(
            cpt, good_response, bad_response,
            end_time - start_time, cpt / (end_time - start_time))

    @staticmethod
    @hug.object.cli
    def run(policy_file,
            endpoint: str = "",
            test_number: int = None,
            verbose: bool = False,
            output_file: str = None,
            dont_kill_server: bool = False):
        """
        Run tests given in a policy file
        :param policy_file: the policy file which contains the tests
        :param endpoint: the endpoint to test
        :param test_number: the number of tests to run
        :param verbose: set the verbosity
        :param output_file: the name of the output file to send logs
        :param dont_kill_server: do we have to kill the engine before quitting
       :return: None
        """
        ChecksCLI.output_file = output_file
        ChecksCLI.verbose = verbose
        ChecksCLI.log("Tests run on " + time.strftime("%Y/%m/%d %H:%M:%S"),
                      force_console=True, color="1")
        if not endpoint:
            _conf = configuration.get_configuration(key='management')
            endpoint = "http://{}:10000/authz".format(
                _conf['url'].replace("http://", "").split(":")[0])
        need_standalone_pipeline = False
        try:
            requests.get(endpoint)
        except requests.exceptions.ConnectionError:
            need_standalone_pipeline = True
            ChecksCLI.launch_standalone_pipeline(endpoint, policy_file)
        try:
            _pdps = pdp.PDPCLI.list().get("pdps")
            vim_project_ids = []
            for _project in _pdps.values():
                if _project.get("vim_project_id", "").strip():
                    vim_project_ids.append(_project.get("vim_project_id", "").strip())
        except (requests.exceptions.ConnectionError, AttributeError):
            vim_project_id = ""
        else:
            if len(vim_project_ids) > 1:
                ChecksCLI.log("VIM Project ID:", force_console=True)
                for project in vim_project_ids:
                    ChecksCLI.log("    - {}".format(project), force_console=True)
                response = input("Choose a project ID in list: ")  # nosec
                # (forbidden use of Python2)
                vim_project_id = response
            else:
                vim_project_id = vim_project_ids[0]
        vim_project_id = vim_project_id.replace("/", "")
        ChecksCLI.log("Using '{}' as project ID".format(vim_project_id), force_console=True)
        ChecksCLI.log("Endpoint: {}".format(endpoint), force_console=True)
        policy = json.loads(open(policy_file).read())
        if "checks" not in policy:
            raise Exception("Cannot find checks attribute in {}".format(policy_file))
        endpoint = endpoint.strip('/')
        ChecksCLI.log("Run grant tests", color="32", force_console=True)
        output = ""
        output += ChecksCLI.run_tests(endpoint,
                                      vim_project_id,
                                      policy['checks'].get("granted", []),
                                      (200, 204),
                                      test_number)
        output += "\n"
        ChecksCLI.log("Run deny tests", color="32", force_console=True)
        output += ChecksCLI.run_tests(endpoint,
                                      vim_project_id,
                                      policy['checks'].get("denied", []),
                                      403,
                                      test_number)
        ChecksCLI.log(output, force_console=True, color="1")

        if need_standalone_pipeline and not dont_kill_server:
            ChecksCLI.kill_standalone_pipeline()

