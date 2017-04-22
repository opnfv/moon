# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
"""

import os
import sys
import glob
import argparse
import importlib
from oslo_config import cfg
from oslo_log import log as logging
from sqlalchemy import create_engine
from moon_db.migrate_repo import versions

# Note (dthom): The next line must be called before the next import
# aka before registering all the options
cfg.CONF.register_cli_opt(cfg.StrOpt('command', positional=True,
                                     help="The command to execute (upgrade, downgrade)"))
from moon_utilities import options  # noqa

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

engine = create_engine(CONF.database.url)


def format_data(ext):
    return ext.name, ext.obj.upgrade()


def run():
    files = glob.glob(versions.__path__[0] + "/[0-9][0-9][0-9]*.py")
    # args = set_options()
    for filename in files:
        filename = os.path.basename(filename).replace(".py", "")
        o = importlib.import_module("moon_db.migrate_repo.versions.{}".format(filename))
        LOG.info("Command is {}".format(CONF.command))
        if CONF.command in ("upgrade", "u", "up"):
            LOG.info("upgrading moon_db.migrate_repo.versions.{}".format(filename))
            o.upgrade(engine)
        elif CONF.command in ("downgrade", "d", "down"):
            LOG.info("downgrading moon_db.migrate_repo.versions.{}".format(filename))
            o.downgrade(engine)
        LOG.info("Done!")
