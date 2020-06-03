# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
This file is used only once to install the manager
"""

import os
import shutil
import sys


def setup():
    """Setup the manager

    :return: nothing
    """
    if os.name == "posix":
        if not os.path.exists(os.path.join("/etc", "moon")):
            print("Installing configuration file in /etc")
            shutil.copytree(os.path.abspath(sys.argv[0]+"/../../moon"), os.path.join("/etc/moon"))
        else:
            print('The directory "/etc/moon/" already exists.', file=sys.stderr)
