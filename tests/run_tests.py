#!/usr/bin/python

# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the
# 'Apache-2.0'license which can be found in the file 'LICENSE' in this
# package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import argparse
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
import os
import sys
import time
import yaml

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
args = parser.parse_args()

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

dirs = functest_yaml.get('general').get('directories')
FUNCTEST_REPO = dirs.get('dir_repo_functest')
COPPER_REPO = dirs.get('dir_repo_moon')
TEST_DB_URL = functest_yaml.get('results').get('test_db_url')

logger = ft_logger.Logger("moon").getLogger()


def main():
    cmd = "moon test --self"

    start_time = time.time()

    ret_val = functest_utils.execute_command(cmd, logger, exit_on_error=False)

    stop_time = time.time()
    duration = round(stop_time - start_time, 1)
    if ret_val == 0:
        logger.info("MOON PASSED")
        test_status = 'PASS'
    else:
        logger.info("MOON")
        test_status = 'FAIL'

    details = {
        'timestart': start_time,
        'duration': duration,
        'status': test_status,
    }

    functest_utils.logger_test_results(logger, "moon",
                                       "moon_authentication",
                                       test_status, details)
    if args.report:
        functest_utils.push_results_to_db("moon",
                                          "moon_authentication",
                                          logger,
                                          start_time,
                                          stop_time,
                                          test_status,
                                          details)
        logger.info("Moon results pushed to DB")

    if ret_val != 0:
        sys.exit(-1)

    sys.exit(0)

if __name__ == '__main__':
    main()
