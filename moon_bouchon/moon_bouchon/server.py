# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
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
app = Flask(__name__)


@app.route("/interface/authz/grant/<string:project_id>/<string:subject_name>/"
           "<string:object_name>/<string:action_name>",
           methods=["GET"])
def interface_grant(project_id, subject_name, object_name, action_name):
    logger.info("Requesting interface authz on {} {} {} {}".format(
        project_id, subject_name, object_name, action_name))
    return json.dumps({
        "result": True,
        "context": {
            "project_id": project_id,
            "subject_name": subject_name,
            "object_name": object_name,
            "action_name": action_name
        }
    })


@app.route("/interface/authz/deny/<string:project_id>/<string:subject_name>/"
           "<string:object_name>/<string:action_name>",
           methods=["GET"])
def interface_deny(project_id, subject_name, object_name, action_name):
    logger.info("Requesting interface authz on {} {} {} {}".format(
        project_id, subject_name, object_name, action_name))
    return json.dumps({
        "result": False,
        "context": {
            "project_id": project_id,
            "subject_name": subject_name,
            "object_name": object_name,
            "action_name": action_name
        }
    })


@app.route("/interface/authz/<string:project_id>/<string:subject_name>/"
           "<string:object_name>/<string:action_name>",
           methods=["GET"])
def interface_authz(project_id, subject_name, object_name, action_name):
    logger.info("Requesting interface authz on {} {} {} {}".format(
        project_id, subject_name, object_name, action_name))
    return json.dumps({
        "result": random.choice((True, False)),
        "context": {
            "project_id": project_id,
            "subject_name": subject_name,
            "object_name": object_name,
            "action_name": action_name
        }
    })


def test_data():
    data = request.form
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


@app.route("/wrapper/authz/grant", methods=["POST"])
def wrapper_grant():
    logger.info("Requesting wrapper authz")
    try:
        test_data()
    except Exception as e:
        logger.exception(e)
        return str(e), 400
    response = flask.make_response("True")
    response.headers['content-type'] = 'application/octet-stream'
    return response


@app.route("/wrapper/authz/deny", methods=["POST"])
def wrapper_deny():
    logger.info("Requesting wrapper authz")
    try:
        test_data()
    except Exception as e:
        logger.exception(e)
        return str(e), 400
    response = flask.make_response("False")
    response.headers['content-type'] = 'application/octet-stream'
    return response


@app.route("/wrapper/authz", methods=["POST"])
def wrapper_authz():
    logger.info("Requesting wrapper authz")
    try:
        test_data()
    except Exception as e:
        logger.exception(e)
        return str(e), 400
    response = flask.make_response(random.choice(("True", "False")))
    response.headers['content-type'] = 'application/octet-stream'
    return response


def main():
    port = 31002
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error("Argument for Port in command line is not an integer")
            sys.exit(1)
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
