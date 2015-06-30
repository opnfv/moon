# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
import os
import logging
import re
import time
from keystone import config
from oslo_log import log
# from keystone.contrib.moon.core import SuperExtensionDriver
from keystone.contrib.moon.core import LogDriver


CONF = config.CONF


class LogConnector(LogDriver):

    AUTHZ_FILE = '/var/log/moon/authz.log'
    TIME_FORMAT = '%Y-%m-%d-%H:%M:%S'

    def __init__(self):
        # Fixme (dthom): when logging from an other class, the %appname% in the event
        # is always keystone.contrib.moon.backends.flat
        super(LogConnector, self).__init__()
        # Configure Log to add new files in /var/log/moon/authz.log and /var/log/moon/system.log
        self.LOG = log.getLogger(__name__)
        self.AUTHZ_LOG = logging.getLogger("authz")
        self.AUTHZ_LOG.setLevel(logging.WARNING)
        fh = logging.FileHandler(self.AUTHZ_FILE)
        fh.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s ------ %(message)s', self.TIME_FORMAT)
        fh.setFormatter(formatter)
        self.AUTHZ_LOG.addHandler(fh)

    def authz(self, message):
        self.AUTHZ_LOG.warn(message)

    def debug(self, message):
        self.LOG.debug(message)

    def info(self, message):
        self.LOG.info(message)

    def warning(self, message):
        self.LOG.warning(message)

    def error(self, message):
        self.LOG.error(message)

    def critical(self, message):
        self.LOG.critical(message)

    def get_logs(self, options):
        options = options.split(",")
        self.info("Options of logs check : {}".format(options))
        event_number = None
        time_from = None
        time_to = None
        filter_str = None
        for opt in options:
            if "event_number" in opt:
                event_number = "".join(re.findall("\d*", opt.split("=")[-1]))
                try:
                    event_number = int(event_number)
                except ValueError:
                    event_number = None
            elif "from" in opt:
                time_from = "".join(re.findall("[\w\-:]*", opt.split("=")[-1]))
                try:
                    time_from = time.strptime(time_from, self.TIME_FORMAT)
                except ValueError:
                    time_from = None
            elif "to" in opt:
                time_to = "".join(re.findall("[\w\-:] *", opt.split("=")[-1]))
                try:
                    time_to = time.strptime(time_to, self.TIME_FORMAT)
                except ValueError:
                    time_to = None
            elif "filter" in opt:
                filter_str = "".join(re.findall("\w*", opt.split("=")[-1]))
        _logs = open(self.AUTHZ_FILE).readlines()
        if filter_str:
            _logs = filter(lambda x: filter_str in x, _logs)
        self.info("Options of logs check : {} {} {} {}".format(event_number, time_from, time_to, filter_str))
        if time_from:
            try:
                for log in _logs:
                    __logs = filter(lambda x: time_from <= time.strptime(x.split(" ")[0], self.TIME_FORMAT), _logs)
                    _logs = __logs
            except ValueError:
                self.error("Time format error")
        if time_to:
            try:
                for log in _logs:
                    __logs = filter(lambda x: time_to >= time.strptime(x.split(" ")[0], self.TIME_FORMAT), _logs)
                    _logs = __logs
            except ValueError:
                self.error("Time format error")
        if event_number:
            _logs = _logs[-event_number:]
        return list(_logs)


# class SuperExtensionConnector(SuperExtensionDriver):
#
#     def __init__(self):
#         super(SuperExtensionConnector, self).__init__()
#         # Super_Extension is loaded every time the server is started
#         self.__uuid = uuid4().hex
#         # self.__super_extension = Extension()
#         _policy_abs_dir = os.path.join(CONF.moon.super_extension_directory, 'policy')
#         # self.__super_extension.load_from_json(_policy_abs_dir)
#
#     def get_super_extensions(self):
#         return None
#
#     def admin(self, sub, obj, act):
#         # return self.__super_extension.authz(sub, obj, act)
#         return True