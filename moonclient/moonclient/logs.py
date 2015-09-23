# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister
from cliff.command import Command
from cliff.show import ShowOne


class LogsList(Lister):
    """List all logs."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(LogsList, self).get_parser(prog_name)
        parser.add_argument(
            '--filter',
            metavar='<filter-str>',
            help='Filter strings (example: "OK" or "authz")',
        )
        parser.add_argument(
            '--fromdate',
            metavar='<from-date-str>',
            help='Filter logs by date (example: "2015-04-15-13:45:20")',
        )
        parser.add_argument(
            '--todate',
            metavar='<to-date-str>',
            help='Filter logs by date (example: "2015-04-15-13:45:20")',
        )
        parser.add_argument(
            '--number',
            metavar='<number-int>',
            help='Show only <number-int> logs',
        )
        return parser

    def take_action(self, parsed_args):
        filter_str = parsed_args.filter
        from_date = parsed_args.fromdate
        to_date = parsed_args.todate
        number = parsed_args.number
        options = list()
        if filter_str:
            options.append("filter={}".format(filter_str))
        if from_date:
            options.append("from={}".format(from_date))
        if to_date:
            options.append("to={}".format(to_date))
        if number:
            options.append("event_number={}".format(number))
        if len(options) > 0:
            url = "/v3/OS-MOON/logs/{}".format(",".join(options))
        else:
            url = "/v3/OS-MOON/logs"
        data = self.app.get_url(url, authtoken=True)
        if "logs" not in data:
            raise Exception("Error in command {}: {}".format("LogsList", data))
        return (
            ("Logs",),
            ((log, ) for log in data["logs"])
        )

