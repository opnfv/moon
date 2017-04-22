# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import os
import re
import types
import requests
from oslo_log import log as logging
from oslo_config import cfg
import oslo_messaging
from moon_utilities import exceptions
from oslo_config.cfg import ConfigOpts

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def get_uuid_from_name(name, elements, **kwargs):
    LOG.error("get_uuid_from_name {} {} {}".format(name, elements, kwargs))
    for element in elements:
        if type(elements[element]) is dict and elements[element].get('name') == name:
            if kwargs:
                for args in kwargs:
                    if elements[element].get(args) != kwargs[args]:
                        LOG.error("get_uuid_from_name2 {} {} {}".format(args, elements[element].get(args), kwargs[args]))
                        return
                else:
                    return element
            else:
                return element


def get_name_from_uuid(uuid, elements, **kwargs):
    for element in elements:
        if element == uuid:
            if kwargs:
                for args in kwargs:
                    if elements[element].get(args) != kwargs[args]:
                        return
                else:
                    return elements[element].get('name')
            else:
                return elements[element].get('name')

