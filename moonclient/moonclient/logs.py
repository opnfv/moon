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

    @staticmethod
    def split_into_line(line, max_char=60):
        """ Split a long line into multiple lines

        :param line: the line to split
        :param max_char: maximal characters to have on one line
        :return: a string with new lines
        """
        words = line.split(" ")
        return_line = ""
        prev_modulo = 0
        while True:
            try:
                modulo = len(return_line) % max_char
                if modulo < prev_modulo:
                    return_line += "\n" + words.pop(0) + " "
                else:
                    return_line += words.pop(0) + " "
                prev_modulo = modulo
            except IndexError:
                return return_line

    def split_time_message(self, line):
        """Split a log string into a table (date, message)

        :param line: the line to split
        :return: a table (date, message)
        """
        _time, _blank, _message = line.split(" ", 2)
        return _time, self.split_into_line(_message)

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
        return (
            ("Time", "Message",),
            (self.split_time_message(log) for log in data)
        )

