# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
import subprocess  # nosec
import os
import sys
import hug.interface
from moon_engine.api import configuration


LOGGER = logging.getLogger("moon.engine")


@hug.cli("start_server")
@hug.local()
def start_server(conf_file):
    """ Start the server of the engine """

    try:
        guni_conf_file = get_info(conf_file, "moon").strip('"\n')
        port = get_info(conf_file, "bind").split(":")[1].strip('"\n')
        log_dir = get_info(conf_file, "pid_file_dir").strip('"\n')
    except ValueError:
        return

    configuration.init_logging(guni_conf_file)
    LOGGER.setLevel(logging.ERROR)

    pid_filename = log_dir + port + ".pid"
    _command = ["gunicorn", "moon_engine.server:__hug_wsgi__", "-D", "-p", pid_filename, "-c", conf_file]
    subprocess.Popen(_command, stdout=subprocess.PIPE, close_fds=True)  # nosec


@hug.cli("stop_server")
@hug.local()
def stop_server(conf_file):
    """ Stop the server of the engine """

    try:
        guni_conf_file = get_info(conf_file, "moon").strip('"\n')
        port = get_info(conf_file, "bind").split(":")[1].strip('"\n')
        log_dir = get_info(conf_file, "pid_file_dir").strip('"\n')
    except ValueError:
        return

    configuration.init_logging(guni_conf_file)
    LOGGER.setLevel(logging.ERROR)

    pid_filename = log_dir + port + ".pid"

    try:
        pid_file = open(pid_filename, 'r')
    except FileNotFoundError:
        LOGGER.error(f"File {pid_filename} not found. Server on port {port} not running?")
        return

    try:
        pid = int(pid_file.read())
    except ValueError:
        LOGGER.error(f"The pid found in {pid_filename} is not valid")
        return

    os.kill(pid, 15)


def get_info(conf, key):
    with open(conf) as config:
        lines = config.readlines()
        for line in lines:
            if line.startswith(key):
                return line.split("=")[1].strip()
        LOGGER.error(f"Key \"{key}\" missing from Gunicorn configuration file")
        raise ValueError


def run():
    if len(sys.argv) > 1:

        command = sys.argv[1]
        sys.argv.pop(1)
        # if command == "conf":
        #     configuration.get_configuration.interface.cli()
        # elif command == "db":
        #     configuration.init_database.interface.cli()
        if command == "start":
            start_server.interface.cli()
        elif command == "stop":
            stop_server.interface.cli()
        else:
            LOGGER.critical("Unknown command {}".format(command))

    else:
        # TODO: update the command management by using argparse
        print("""Possible commands are:
        # - conf
        # - db
        - start
        - stop
        """)


if __name__ == "__main__":
    run()
