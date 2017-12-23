# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
import time
from python_moondb.core import LogDriver


class LogConnector(LogDriver):

    AUTHZ_FILE = '/var/log/moon/authz.log'
    SYS_FILE = '/var/log/moon/system.log'
    TIME_FORMAT = '%Y-%m-%d-%H:%M:%S'

    def __init__(self):
        # Fixme (dthom): when logging from an other class, the %appname% in the event
        # is always keystone.contrib.moon.backends.flat
        super(LogConnector, self).__init__()

        self.SYS_LOG = logging.getLogger(__name__)
        if not len(self.SYS_LOG.handlers):
            fh = logging.FileHandler(self.SYS_FILE)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s ------ %(message)s', self.TIME_FORMAT)
            fh.setFormatter(formatter)
            self.SYS_LOG.addHandler(fh)

        self.AUTHZ_LOG = logging.getLogger("authz")
        if not len(self.AUTHZ_LOG.handlers):
            fh = logging.FileHandler(self.AUTHZ_FILE)
            fh.setLevel(logging.WARNING)
            formatter = logging.Formatter('%(asctime)s ------ %(message)s', self.TIME_FORMAT)
            fh.setFormatter(formatter)
            self.AUTHZ_LOG.addHandler(fh)

    def authz(self, message):
        self.AUTHZ_LOG.warn(message)

    def debug(self, message):
        self.SYS_LOG.debug(message)

    def info(self, message):
        self.SYS_LOG.info(message)

    def warning(self, message):
        self.SYS_LOG.warning(message)

    def error(self, message):
        self.SYS_LOG.error(message)

    def critical(self, message):
        self.SYS_LOG.critical(message)

    def get_logs(self, logger="authz", event_number=None, time_from=None, time_to=None, filter_str=None):
        if logger == "authz":
            _logs = open(self.AUTHZ_FILE).readlines()
        else:
            _logs = open(self.SYS_FILE).readlines()
        if filter_str:
            _logs = filter(lambda x: filter_str in x, _logs)
        if time_from:
            if isinstance(time_from, str):
                time_from = time.strptime(time_from.split(" ")[0], self.TIME_FORMAT)
            try:
                __logs = []
                for log in _logs:
                    _log = time.strptime(log.split(" ")[0], self.TIME_FORMAT)
                    if time_from <= _log:
                        __logs.append(log)
                _logs = __logs
            except ValueError:
                self.error("Time format error")
        if time_to:
            try:
                if isinstance(time_to, str):
                    time_to = time.strptime(time_to.split(" ")[0], self.TIME_FORMAT)
                __logs = []
                for log in _logs:
                    _log = time.strptime(log.split(" ")[0], self.TIME_FORMAT)
                    if time_to >= _log:
                        __logs.append(log)
                _logs = __logs
            except ValueError:
                self.error("Time format error")
        if event_number:
            _logs = _logs[-event_number:]
        return list(_logs)
