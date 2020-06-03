# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Plugin to request OpenStack infrastructure:
- Keystone
- Nova
"""

import logging
import os
import atexit
import signal
import sys
import time
from moon_manager import pip_driver
from moon_manager import db_driver
from moon_manager.api import configuration
import hug.interface

LOGGER = logging.getLogger("moon.manager.plugins.daemon")

PLUGIN_TYPE = "daemon"

db_driver.init()


class OpenstackDaemon(object):

    @staticmethod
    def _update_subjects():
        k_users = []
        for manager in pip_driver.InformationManager["subjects"]:
            k_users += list(manager.get_items().values())[0]

        user_ids = {user["id"].replace("-", ""): user for user in k_users}

        moon_subjects = db_driver.PolicyManager.get_subjects(moon_user_id=None, policy_id=None)
        moon_subject_ids = moon_subjects.keys()

        for user_id in user_ids:
            if user_id not in moon_subject_ids:
                value = {"name": user_ids[user_id]["name"], "description": ""}
                db_driver.PolicyManager.add_subject(
                    moon_user_id=None, policy_id=None, value=value, perimeter_id=user_id)

    @staticmethod
    def _update_objects():
        k_objects = []
        for manager in pip_driver.InformationManager["objects"]:
            k_objects += list(manager.get_items().values())[0]

        object_ids = {object_["id"].replace("-", ""): object_ for object_ in k_objects}

        moon_objects = db_driver.PolicyManager.get_objects(moon_user_id=None, policy_id=None)
        moon_object_ids = moon_objects.keys()

        for object_id in object_ids:
            if object_id not in moon_object_ids:
                value = {"name": object_ids[object_id]["name"], "description": ""}
                db_driver.PolicyManager.add_object(
                    moon_user_id=None, policy_id=None, value=value, perimeter_id=object_id)

    @staticmethod
    def update():
        OpenstackDaemon._update_subjects()
        OpenstackDaemon._update_objects()


def daemonize(pidfile, logfile):
    try:
        with open(pidfile, 'r') as pf:
            pid = int(pf.read().strip())
    except IOError:
        pid = None

    if pid:
        message = "pidfile {0} already exist. " + \
                  "Daemon already running?\n"
        sys.stderr.write(message.format(pidfile))
        sys.exit(1)

    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('fork #1 failed: {0}\n'.format(err))
        sys.exit(1)

    # decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('fork #2 failed: {0}\n'.format(err))
        sys.exit(1)

        # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open(logfile, 'a+')
    se = open(logfile, 'a+')

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    # write pidfile
    atexit.register(os.remove, pidfile)

    pid = str(os.getpid())
    with open(pidfile, 'w+') as f:
        f.write(pid + '\n')


def kill_daemon(pidfile):
    """Stop the daemon."""

    # Get the pid from the pidfile
    try:
        with open(pidfile, 'r') as pf:
            pid = int(pf.read().strip())
    except IOError:
        pid = None

    if not pid:
        message = "pidfile {0} does not exist. " + \
                  "Daemon not running?\n"
        sys.stderr.write(message.format(pidfile))
        return  # not an error in a restart

    # Try killing the daemon process
    try:
        while 1:
            os.kill(pid, signal.SIGTERM)
            time.sleep(0.1)
    except OSError as err:
        e = str(err.args)
        if e.find("No such process") > 0:
            if os.path.exists(pidfile):
                os.remove(pidfile)
        else:
            print(str(err.args))
            sys.exit(1)

@hug.cli("start_daemon")
def run():
    """ start the auto-update service """
    daemon_conf = configuration.get_configuration("information").get("daemon")
    daemonize(daemon_conf["pid_file"], daemon_conf["log_file"])

    for category in pip_driver.InformationManager:
        for manager in pip_driver.InformationManager[category]:
            manager.set_auth()

    while True:
        OpenstackDaemon.update()
        time.sleep(1)

@hug.cli("stop_daemon")
def stop():
    """ stop the auto-update service """
    pid_file = configuration.get_configuration("information").get("daemon").get("pid_file")
    kill_daemon(pid_file)

