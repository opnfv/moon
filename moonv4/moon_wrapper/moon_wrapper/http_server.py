# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import requests
import json
from flask import Flask, request
import logging
from moon_utilities import configuration

logger = logging.getLogger("moon.wrapper.http")


def __get_subject(target, credentials):
    _subject = target.get("user_id", "")
    if not _subject:
        _subject = credentials.get("user_id", "")
    return _subject


def __get_object(target, credentials):
    try:
        # note: case of Glance
        return target['target']['name']
    except KeyError:
        pass

    # note: default case
    return target.get("project_id", "")


def __get_project_id(target, credentials):
    return target.get("project_id", "")


def HTTPServer(host, port):
    app = Flask(__name__)
    conf = configuration.get_configuration("components/wrapper")
    timeout = conf["components/wrapper"].get("timeout", 5)
    conf = configuration.get_configuration("components/interface")
    interface_hostname = conf["components/interface"].get("hostname", "interface")
    interface_port = conf["components/interface"].get("port", 80)
    conf = configuration.get_configuration("logging")
    try:
        debug = conf["logging"]["loggers"]['moon']['level'] == "DEBUG"
    except KeyError:
        debug = False

    @app.route("/", methods=['POST', 'GET'])
    def wrapper():
        try:
            target = json.loads(request.form.get('target', {}))
            credentials = json.loads(request.form.get('credentials', {}))
            rule = request.form.get('rule', "")
            _subject = __get_subject(target, credentials)
            _object = __get_object(target, credentials)
            _project_id = __get_project_id(target, credentials)
            logger.info("GET with args {} / {} - {} - {}".format(_project_id, _subject, _object, rule))
            _url = "http://{}:{}/{}/{}/{}/{}".format(
                interface_hostname,
                interface_port,
                _project_id,
                _subject,
                _object,
                rule
            )
            req = requests.get(url=_url, timeout=timeout)
            logger.info("req txt={}".format(req.text))
            if req.json()["result"] == True:
                return "True"
        except Exception as e:
            logger.exception("An exception occurred: {}".format(e))
        return "False"

    app.run(debug=debug, host=host, port=port)
