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
import subprocess
import json
try:
    import http.client as client
except ImportError:
    import httplib as client

PORT_ODL = 8181
HOST_ODL = "localhost"

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
try:
    # Python3 version
    from urllib.request import urlopen, HTTPBasicAuthHandler, build_opener, install_opener
except ImportError:
    # Python2 version
    from urllib import urlopen
    from urllib2 import HTTPBasicAuthHandler, build_opener, install_opener


def __get_endpoint_url(name="keystone"):
    proc = subprocess.Popen(["openstack", "endpoint", "show", name, "-f", "yaml"], stdout=subprocess.PIPE)
    y = yaml.load(proc.stdout.read())
    url = y['publicurl']
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    host, port = url.split(":")
    port = port.split("/")[0]
    return host, port


def test_federation():

    username = "test_fede"
    password = "pass_fede"

    # Create a new user in OpenStack
    proc = subprocess.Popen(["openstack", "user", "create", "--password", password, username, "-f", "yaml"], stdout=subprocess.PIPE)
    logger.info("Create new user ({})".format(proc.stdout.read()))

    # Retrieve Moon token
    nhost, nport = __get_endpoint_url()
    auth_data = {'username': username, 'password': password}
    conn = client.HTTPConnection(nhost, nport)
    headers = {"Content-type": "application/json"}
    conn.request("POST", "/moon/auth/tokens", json.dumps(auth_data).encode('utf-8'), headers=headers)
    resp = conn.getresponse()
    if resp.status not in (200, 201, 202, 204):
        return False, "Not able to retrieve Moon token on {}:{} (error code: {}).".format(nhost, nport, resp.status)


    # Test ODL auth
    nhost, nport = __get_endpoint_url(name="neutron")
    nport = "8181"
    auth_data = {'username': 'admin', 'password': 'console'}

    # Get basic auth with curl
    proc = subprocess.Popen("curl -u {}:{} http://{}:{}/auth/v1/domains".format(
        auth_data["username"], auth_data["password"], nhost, nport),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _stdout = proc.stdout.read()
    _stderr = proc.stderr.read()
    if len(_stdout) > 0:
        _stdout_json = json.loads(_stdout)
        if _stdout_json['code'] not in (200, 201, 202, 204):
            return False, "Not able to retrieve ODL auth ({}).".format(_stdout)

    # Retrieve token from ODL
    # conn = client.HTTPConnection(nhost, "8181")
    # headers = {"Content-type": "application/json"}
    # conn.request("POST", "/auth/v1/domains", json.dumps(auth_data).encode('utf-8'), headers=headers)
    # resp = conn.getresponse()
    # if resp.status not in (200, 201, 202, 204):
    #     return False, "Not able to retrieve ODL token on {}:{} (error code: {}).".format(nhost, "8181", resp.status)

    # Retrieve basic auth from ODL
    # auth_handler = HTTPBasicAuthHandler()
    # auth_handler.add_password(realm='Moon',
    #                           uri='http://{host}:{port}/auth/v1/domains'.format(host=HOST_ODL, port=PORT_ODL),
    #                           user='admin',
    #                           passwd='console')
    # opener = build_opener(auth_handler)
    # install_opener(opener)
    # url = urlopen('http://{host}:{port}/auth/v1/domains'.format(host=HOST_ODL, port=PORT_ODL))
    # code = url.getcode()
    # if code not in (200, 201, 202, 204):
    #     return False, "Not able to retrieve ODL token (error code: {}).".format(code)
    return True, ""


def test_moon_openstack():
    log_filename = "moonclient_selftest.log"
    cmd = "moon test --password console --self --logfile {}".format(log_filename)

    ret_val = functest_utils.execute_command(cmd, exit_on_error=False)

    return ret_val, open(log_filename, "rt").read()


def main():
    start_time = time.time()

    result_os = test_moon_openstack()
    result_odl = test_federation()

    stop_time = time.time()
    duration = round(stop_time - start_time, 1)
    if result_os == 0 and result_odl[0]:
        logger.info("OS MOON PASSED")
        test_status = 'PASS'
    else:
        logger.info("OS MOON ERROR")
        test_status = 'FAIL'
        logger.info("Errors from OpenStack tests:")
        logger.info(result_os[1])
        logger.info("Errors from Federation tests:")
        logger.info(result_odl[1])

    details = {
        'timestart': start_time,
        'duration': duration,
        'status': test_status,
        'results': {
            'openstack': result_os,
            'opendaylight': result_odl
        }
    }

    functest_utils.logger_test_results("moon",
                                       "moon_authentication",
                                       test_status, details)
    if args.report:
        functest_utils.push_results_to_db("moon",
                                          "moon_authentication",
                                          start_time,
                                          stop_time,
                                          test_status,
                                          details)
        logger.info("Moon results pushed to DB")

    if result_os != 0 or not result_odl[0]:
        return False
    return True


if __name__ == '__main__':
    ret = main()
    if ret:
        sys.exit(0)
    sys.exit(1)
