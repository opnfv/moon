# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging.config
import requests
from python_moonutilities import configuration

__version__ = "1.4.3"

try:
    config = configuration.get_configuration("logging")
    logging.config.dictConfig(config['logging'])
except requests.exceptions.ConnectionError:
    pass
