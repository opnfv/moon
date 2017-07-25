# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
"""

import os
import glob
import importlib
import argparse
import logging
from sqlalchemy import create_engine
from moon_db.migrate_repo import versions
from moon_utilities import configuration

parser = argparse.ArgumentParser()
parser.add_argument('command', help='command (upgrade or downgrade)', nargs=1)
parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
parser.add_argument("--debug", "-d", action='store_true', help="debug mode")
args = parser.parse_args()

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
if args.debug:
    logging.basicConfig(
        format=FORMAT,
        level=logging.DEBUG)
elif args.verbose:
    logging.basicConfig(
        format=FORMAT,
        level=logging.INFO)
else:
    logging.basicConfig(
        format=FORMAT,
        level=logging.WARNING)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARNING)
requests_log.propagate = True

logger = logging.getLogger("moon.db.manager")

db_conf = configuration.get_configuration("database")["database"]
engine = create_engine(db_conf['url'])


def format_data(ext):
    return ext.name, ext.obj.upgrade()


def run():
    files = glob.glob(versions.__path__[0] + "/[0-9][0-9][0-9]*.py")
    for filename in files:
        filename = os.path.basename(filename).replace(".py", "")
        o = importlib.import_module("moon_db.migrate_repo.versions.{}".format(filename))
        logger.info("Command is {}".format(args.command[0]))
        if args.command[0] in ("upgrade", "u", "up"):
            logger.info("upgrading moon_db.migrate_repo.versions.{}".format(filename))
            o.upgrade(engine)
        elif args.command[0] in ("downgrade", "d", "down"):
            logger.info("downgrading moon_db.migrate_repo.versions.{}".format(filename))
            o.downgrade(engine)
        else:
            logger.critical("Cannot understand the command!")
