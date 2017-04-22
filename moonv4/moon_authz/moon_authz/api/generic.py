# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


class Status(object):
    """
    Retrieve the current status of all components.
    """

    __version__ = "0.1.0"

    def get_status(self, ctx, args):
        return {"status": "Running"}


class Logs(object):
    """
    Retrieve the current status of all components.
    """

    __version__ = "0.1.0"

    def get_logs(self, ctx, args):
        return {"error": "NotImplemented"}


