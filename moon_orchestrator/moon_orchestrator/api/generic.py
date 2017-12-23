# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Those API are helping API used to manage the Moon platform.
"""

from flask_restful import Resource, request
import logging
import moon_orchestrator.api
from python_moonutilities.security_functions import check_auth

__version__ = "0.1.0"

LOG = logging.getLogger("moon.orchestrator.api." + __name__)


class Status(Resource):
    """
    Endpoint for status requests
    """

    __urls__ = ("/status", "/status/", "/status/<string:component_id>")

    def get(self, component_id=None):
        """Retrieve status of all components

        :return: {
          "orchestrator": {
            "status": "Running"
          },
          "security_router": {
            "status": "Running"
          }
        }
        """
        raise NotImplemented


class Logs(Resource):
    """
    Endpoint for logs requests
    """

    __urls__ = ("/logs", "/logs/", "/logs/<string:component_id>")

    def get(self, component_id=None):
        """Get logs from the Moon platform

        :param component_id: the ID of the component your are looking for (optional)
        :return: [
            "2015-04-15-13:45:20
            "2015-04-15-13:45:21
            "2015-04-15-13:45:22
            "2015-04-15-13:45:23
        ]
        """
        filter_str = request.args.get('filter', '')
        from_str = request.args.get('from', '')
        to_str = request.args.get('to', '')
        event_number = request.args.get('event_number', '')
        try:
            event_number = int(event_number)
        except ValueError:
            event_number = None
        args = dict()
        args["filter"] = filter_str
        args["from"] = from_str
        args["to"] = to_str
        args["event_number"] = event_number

        raise NotImplemented


class API(Resource):
    """
    Endpoint for API requests
    """

    __urls__ = (
        "/api",
        "/api/",
        "/api/<string:group_id>",
        "/api/<string:group_id>/",
        "/api/<string:group_id>/<string:endpoint_id>")

    @check_auth
    def get(self, group_id="", endpoint_id="", user_id=""):
        """Retrieve all API endpoints or a specific endpoint if endpoint_id is given

        :param group_id: the name of one existing group (ie generic, ...)
        :param endpoint_id: the name of one existing component (ie Logs, Status, ...)
        :return: {
            "group_name": {
                "endpoint_name": {
                    "description": "a description",
                    "methods": {
                        "get": "description of the HTTP method"
                    },
                    "urls": ('/api', '/api/', '/api/<string:endpoint_id>')
                }
        }
        """
        __methods = ("get", "post", "put", "delete", "options", "patch")
        api_list = filter(lambda x: "__" not in x, dir(moon_orchestrator.api))
        api_desc = dict()
        for api_name in api_list:
            api_desc[api_name] = {}
            group_api_obj = eval("moon_interface.api.{}".format(api_name))
            api_desc[api_name]["description"] = group_api_obj.__doc__
            if "__version__" in dir(group_api_obj):
                api_desc[api_name]["version"] = group_api_obj.__version__
            object_list = list(filter(lambda x: "__" not in x, dir(group_api_obj)))
            for obj in map(lambda x: eval("moon_interface.api.{}.{}".format(api_name, x)), object_list):
                if "__urls__" in dir(obj):
                    api_desc[api_name][obj.__name__] = dict()
                    api_desc[api_name][obj.__name__]["urls"] = obj.__urls__
                    api_desc[api_name][obj.__name__]["methods"] = dict()
                    for _method in filter(lambda x: x in __methods, dir(obj)):
                        docstring = eval("moon_interface.api.{}.{}.{}.__doc__".format(api_name, obj.__name__, _method))
                        api_desc[api_name][obj.__name__]["methods"][_method] = docstring
                    api_desc[api_name][obj.__name__]["description"] = str(obj.__doc__)
        if group_id in api_desc:
            if endpoint_id in api_desc[group_id]:
                return {group_id: {endpoint_id: api_desc[group_id][endpoint_id]}}
            elif len(endpoint_id) > 0:
                LOG.error("Unknown endpoint_id {}".format(endpoint_id))
                return {"error": "Unknown endpoint_id {}".format(endpoint_id)}
            return {group_id: api_desc[group_id]}
        return api_desc
