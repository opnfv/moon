# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
from moon_utilities.security_functions import call


class Status(object):
    """
    Retrieve the current status of all components.
    """

    __version__ = "0.1.0"

    def __get_status(self, ctx, args={}):
        return {"status": "Running"}

    def get_status(self, ctx, args={}):
        status = dict()
        if "component_id" in ctx and ctx["component_id"] == "security_router":
            return {"security_router": self.__get_status(ctx, args)}
        elif "component_id" in ctx and ctx["component_id"]:
            # TODO (dthom): check if component exist
            status[ctx["component_id"]] = call(ctx["component_id"], ctx, "get_status", args=args)
        else:
            # TODO (dthom): must get the status of all containers
            status["orchestrator"] = call("orchestrator", ctx, "get_status", args=args)
            status["security_router"] = self.__get_status(ctx, args)
        return status


class Logs(object):
    """
    Retrieve the current status of all components.
    """

    __version__ = "0.1.0"

    def get_logs(self, ctx, args={}):
        logs = dict()
        logs["orchestrator"] = call("orchestrator", ctx, "get_logs", args=args)
        # TODO (dthom): must get the logs of all containers
        logs["security_router"] = {"error": "Not implemented", "ctx": ctx, "args": args}
        return logs


