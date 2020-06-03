# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Install the Moon platform
"""

import argparse
import logging
import os
import subprocess  # nosec
import sys
import getpass

try:
    import pytest
except ModuleNotFoundError:
    subprocess.call([sys.executable, "-m", "pip", "install", "pytest", "--upgrade"])  # nosec
    subprocess.call([sys.executable, "-m", "pip", "install", "pytest-cov", "--upgrade"])  # nosec
    subprocess.call([sys.executable, "-m", "pip", "install", "cliff", "--upgrade"])  # nosec
    subprocess.call([sys.executable, "-m", "pip", "install", "requests_mock", "--upgrade"])  # nosec
    import pytest
try:
    from git import Repo
except ModuleNotFoundError:
    subprocess.call([sys.executable, "-m", "pip", "install", "GitPython", "--upgrade"])  # nosec
    from git import Repo

COMPONENTS = {
    "moon_utilities": [],
    "moon_cache": [],
    "moon_manager": [],
    "moon_engine": [],
}

logger = logging.getLogger(__name__)


def init():
    """
    Initialize the application
    :return: argument given in the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", '-v', action='store_true', help='verbose mode')
    parser.add_argument("--debug", '-d', action='store_true', help='debug mode')
    parser.add_argument("--pre", '-p', action='store_true', help='install packages in dev mode')
    parser.add_argument("--git", '-g', action='store_true', help='install packages from source tree')
    parser.add_argument("--tests", '-t', action='store_true', help='run tests on each package')
    parser.add_argument("--username", '-u', help='set the username for the Gitlab server')
    parser.add_argument("--password", '-pa', help='set the password for the Gitlab server')
    parser.add_argument("--password-file", '-pf',
                        help='set the filename of the file containing all passwords for the '
                             'Gitlab server')
    parser.add_argument("--do-not-clean", '-dnc', action='store_true',
                        help='do not clean the dev environment')
    args = parser.parse_args()
    logging_format = "%(levelname)s: %(message)s"
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format=logging_format)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    else:
        logging.basicConfig(format=logging_format)

    if args.password_file:
        logger.info("Using {} as password file".format(args.password_file))
        for line in open(args.password_file):
            try:
                comp, user, password = line.split(":")
                if comp in COMPONENTS:
                    COMPONENTS[comp] = [user, password.strip()]
                else:
                    logger.error("Unknown component {} in password file".format(comp))
            except ValueError:
                # empty line
                pass
    return args


def install_from_pkg(package, args):
    logger.info(f"Installing from pkg {package}")
    command = [sys.executable, "-m", "pip", "install", package, "--upgrade"]
    if args.pre:
        command.append("--pre")
    subprocess.call(command)  # nosec


def install_from_src(package, args):
    logger.info(f"Installing {package} from source...")
    if os.path.isdir(os.path.join("src", package)):
        repo = Repo("src/" + package)
        repo.remote().pull()
    else:
        if args.password_file:
            Repo.clone_from("https://{}:{}@gitlab.forge.orange-labs.fr/moon/{}.git".format(
                COMPONENTS[package][0], COMPONENTS[package][1], package),
                to_path=os.path.join(os.getcwd(), "src", package))
        elif args.username:
            logger.info(f"installing with {args.username}")
            Repo.clone_from("https://{}:{}@gitlab.forge.orange-labs.fr/moon/{}.git".format(
                args.username, args.password, package),
                to_path=os.path.join(os.getcwd(), "src", package))
        else:
            Repo.clone_from("https://gitlab.forge.orange-labs.fr/moon/{}.git".format(package),
                            to_path=os.path.join(os.getcwd(), "src", package))

    # logger.info(f"Installing from source {package}")
    cur_dir = os.getcwd()
    os.chdir(os.path.join("src", package))
    command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    subprocess.call(command)  # nosec
    command = [sys.executable, "-m", "pip", "install", "."]
    subprocess.call(command)  # nosec

    if args.tests:
        pytest.main(["tests/unit_python"])

    os.chdir(cur_dir)


def clean_git():
    subprocess.call(["rm", "-rf", "src"])  # nosec


def main():
    args = init()
    if not args.git:
        for component in COMPONENTS:
            install_from_pkg(component, args)
    else:
        try:
            try:
                os.mkdir("src")
            except FileExistsError:
                pass
            if args.username and not args.password:
                args.password = getpass.getpass(f"Give the password for {args.username} Gitlab")
            for component in COMPONENTS:
                install_from_src(component, args)
        finally:
            if not args.do_not_clean:
                clean_git()


if __name__ == "__main__":
    main()
