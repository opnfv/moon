# Copyright 2018 Orange
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import sys
import flask
from flask import Flask
from flask import request
import json
import logging
import random

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


def test_target(data, result):
    if "resource_id" in data:
        result["resource_id"] = data['object_id']
    if "object_id" in data:
        result["resource_id"] = data['object_id']
    if 'project_id' in data:
        result["project_id"] = data['project_id']
    if 'user_id' in data:
        result["user_id"] = data['user_id']


def test_credentials(data, result):
    if 'project_id' in data:
        result["project_id"] = data['project_id']
    if 'user_id' in data:
        result["user_id"] = data['user_id']
    if 'project_domain_id' in data:
        result["domain_id"] = data['project_domain_id']


def test_rule(data, result):
    result['action_name'] = data


def test_data():
    data = request.form
    result = {
        "user_id": "",
        "project_id": "",
        "action_name": "",
        "resource_id": "",
        "domain_id": "",
    }
    if not dict(request.form):
        data = json.loads(request.data.decode("utf-8"))
    try:
        target = json.loads(data.get('target', {}))
    except Exception:
        raise Exception("Error reading target")
    try:
        credentials = json.loads(data.get('credentials', {}))
    except Exception:
        raise Exception("Error reading credentials")
    try:
        rule = data.get('rule', "")
    except Exception:
        raise Exception("Error reading rule")
    test_target(target, result)
    test_credentials(credentials, result)
    test_rule(rule, result)
    return_value = True
    logger.info("Analysing request with {}".format(rule))
    for key in result:
        if not result[key] and key != "domain_id":
            return_value = False
            logger.error("Attribute {} is absent".format(key))
        if not result[key] and key == "domain_id":
            logger.warning("Attribute {} is missing.".format(key))
    return return_value


@app.route("/policy_checker", methods=["POST"])
def checker():
    information_is_complete = False
    try:
        information_is_complete = test_data()
    except Exception as e:
        logger.exception(e)
    if information_is_complete:
        response = flask.make_response("True")
        response.headers['content-type'] = 'application/octet-stream'
        return response
    else:
        response = flask.make_response("False")
        response.headers['content-type'] = 'application/octet-stream'
        return response, 403


def get_target():
    data = request.form
    if not dict(request.form):
        data = json.loads(request.data.decode("utf-8"))
    try:
        return json.loads(data.get('target', {}))
    except Exception:
        raise Exception("Error reading target")


@app.route("/authz/grant", methods=["POST"])
def wrapper_grant():
    logger.info("Requesting wrapper authz with {}".format(get_target()))
    response = flask.make_response("True")
    response.headers['content-type'] = 'application/octet-stream'
    return response


@app.route("/authz/deny", methods=["POST"])
def wrapper_deny():
    logger.info("Requesting wrapper authz with {}".format(get_target()))
    response = flask.make_response("False")
    response.headers['content-type'] = 'application/octet-stream'
    return response, 403


def main():
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error("Argument for Port in command line is not an integer")
            sys.exit(1)
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
