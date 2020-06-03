# Software Name: MOON:

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

from __future__ import print_function
import logging

logger = logging.getLogger(__name__)

def before_feature(context, feature):
    handler = logging.FileHandler(filename='Logs/'+"Automation Testing Log- "+ feature.name + ".log")
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)


def before_all(context):
    logging.getLogger("requests").setLevel(logging.WARN)

