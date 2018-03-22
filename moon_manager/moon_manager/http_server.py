# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
from flask import Flask, jsonify, Response, make_response
from flask_cors import CORS, cross_origin
from json import dumps
from flask_restful import Resource, Api
import logging
import sqlalchemy.exc
import time
from moon_manager import __version__
from moon_manager.api.generic import Status, Logs, API
from moon_manager.api.models import Models
from moon_manager.api.policies import Policies
from moon_manager.api.pdp import PDP
from moon_manager.api.slaves import Slaves
from moon_manager.api.meta_rules import MetaRules
from moon_manager.api.meta_data import SubjectCategories, ObjectCategories, ActionCategories
from moon_manager.api.perimeter import Subjects, Objects, Actions
from moon_manager.api.data import SubjectData, ObjectData, ActionData
from moon_manager.api.assignments import SubjectAssignments, ObjectAssignments, ActionAssignments
from moon_manager.api.rules import Rules
from moon_manager.api.json_import import JsonImport
from moon_manager.api.json_export import JsonExport
from python_moonutilities import configuration
from python_moondb.core import PDPManager


logger = logging.getLogger("moon.manager.http_server")

__API__ = (
    Status, Logs, API,
    MetaRules, SubjectCategories, ObjectCategories, ActionCategories,
    Subjects, Objects, Actions, Rules,
    SubjectAssignments, ObjectAssignments, ActionAssignments,
    SubjectData, ObjectData, ActionData,
    Models, Policies, PDP, Slaves, JsonImport, JsonExport
 )


class Server:
    """Base class for HTTP server"""

    def __init__(self, host="localhost", port=80, api=None, **kwargs):
        """Run a server

        :param host: hostname of the server
        :param port: port for the running server
        :param kwargs: optional parameters
        :return: a running server
        """
        self._host = host
        self._port = port
        self._api = api
        self._extra = kwargs

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, name):
        self._host = name

    @host.deleter
    def host(self):
        self._host = ""

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, number):
        self._port = number

    @port.deleter
    def port(self):
        self._port = 80

    def run(self):
        raise NotImplementedError()


class Root(Resource):
    """
    The root of the web service
    """
    __urls__ = ("/", )
    __methods = ("get", "post", "put", "delete", "options")

    def get(self):
        tree = {"/": {"methods": ("get",),
                      "description": "List all methods for that service."}}
        for item in __API__:
            tree[item.__name__] = {"urls": item.__urls__}
            _methods = []
            for _method in self.__methods:
                if _method in dir(item):
                    _methods.append(_method)
            tree[item.__name__]["methods"] = _methods
            tree[item.__name__]["description"] = item.__doc__.strip() if item.__doc__ else ""
        return {
            "version": __version__,
            "tree": tree
        }


class CustomApi(Api):

    @staticmethod
    def handle_error(e):
        try:
            error_message = dumps({'message': str(e), "code": getattr(e, "code", 500)})
            logger.error(error_message)
            return make_response(error_message, getattr(e, "code", 500))
        except Exception as e2:  # unhandled exception in the api...
            logger.error(str(e2))
            return make_response(error_message, 500)


class HTTPServer(Server):

    def __init__(self, host="localhost", port=80, **kwargs):
        super(HTTPServer, self).__init__(host=host, port=port, **kwargs)
        self.app = Flask(__name__)
        self.app.config['TRAP_HTTP_EXCEPTIONS'] = True
        conf = configuration.get_configuration("components/manager")
        self.manager_hostname = conf["components/manager"].get("hostname",
                                                               "manager")
        self.manager_port = conf["components/manager"].get("port", 80)
        # TODO : specify only few urls instead of *
        CORS(self.app)
        self.api = CustomApi(self.app)
        self.__set_route()

    def __set_route(self):
        self.api.add_resource(Root, '/')

        for _api in __API__:
            self.api.add_resource(_api, *_api.__urls__)

    @staticmethod
    def __check_if_db_is_up():
        first = True
        while True:
            try:
                PDPManager.get_pdp(user_id="admin", pdp_id=None)
            except (sqlalchemy.exc.ProgrammingError, sqlalchemy.exc.InternalError):
                time.sleep(1)
                if first:
                    logger.warning("Waiting for the database...")
                    first = False
            else:
                logger.warning("Database is up, resuming operations...")
                break

    def run(self):
        self.__check_if_db_is_up()
        self.app.run(host=self._host, port=self._port, threaded=True)  # nosec
