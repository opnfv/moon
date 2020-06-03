# Copyright 2019 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Update policy files of an OpenStack platform
"""

import argparse
import logging
import os


COMPONENTS = [
    "cinder",
    "glance",
    "keystone",
    "neutron",
    "nova",
]


logger = logging.getLogger(__name__)


def init():
    """
    Initialize the application
    :return: argument given in the command line
    """
    global policy
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", '-v', action='store_true', help='verbose mode')
    parser.add_argument("--debug", '-d', action='store_true', help='debug mode')
    parser.add_argument("--dir",
                        help='directory containing policy files, defaults to /etc',
                        default="/etc")
    parser.add_argument("--exclude", "-x",
                        help="Exclude some components "
                             "(example: \"nova,neutron\")",
                        default="")
    parser.add_argument("--include", "-i",
                        help="Only include some components "
                             "(example: \"nova,neutron\")",
                        default="")
    args = parser.parse_args()
    logging_format = "%(levelname)s: %(message)s"
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format=logging_format)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    else:
        logging.basicConfig(format=logging_format)

    return args


def update_component(component, args):
    """
    
    :param component: 
    :return: 
    """
    filename = os.path.join(args.dir, component, "policy.json")
    logger.info(f"Updating {component} ({filename})")
    if not os.path.isfile(filename):
        logger.error(f"Cannot find {filename}")
        return
    
    
def main():
    args = init()
    if args.include:
        for component in args.include.split(","):
            update_component(component, args)
    else:
        excl_comp = args.exclude.split(",")
        for component in COMPONENTS:
            if component in excl_comp:
                continue
            update_component(component, args)


if __name__ == "__main__":
    main()
