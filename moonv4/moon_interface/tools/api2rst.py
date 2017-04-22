# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
import sys
import requests
import logging
import time
import json

os.unsetenv("http_proxy")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = "172.18.0.11"
PORT = 38001
COMPONENT = sys.argv[2] if len(sys.argv) > 1 else "Interface"
FILENAME = sys.argv[2] if len(sys.argv) > 2 else "api.rst"
CURRENT_TIME = time.strftime("%Y/%m/%d %H:%M:%S %Z")
REVISION = time.strftime("%Y%m%d_%H%M%S_%Z")
AUTHOR = "Thomas Duval <thomas.duval@orange.com>"

logger.info("Writing to {}".format(FILENAME))

toc = (
    "generic",
    "models",
    "policies",
    "pdp",
    "meta_rules",
    "meta_data",
    "perimeter",
    "data",
    "assignments",
    "rules",
    "authz",
)


def get_api_list():
    url = "http://{}:{}/api".format(HOST, PORT)
    cnx = requests.get(url)
    try:
        return cnx.json()
    except json.decoder.JSONDecodeError:
        logger.error("Error decoding JSON on {}\n{}".format(url, cnx.content))
        sys.exit(1)


def analyse_description(desc):
    result = ""
    if not desc:
        return "No description"
    for line in desc.splitlines():
        if line.strip().startswith(":"):
            if ":request body:" in line:
                result += ":request body:\n\n.. code-block:: json\n\n"
                result += line.replace(":request body: ", "") + "\n\n"
            elif ":return:" in line:
                result += ":return:\n\n.. code-block:: json\n\n"
                result += line.replace(":return: ", "") + "\n"
            else:
                result += line.strip() + "\n\n"
        else:
            result += line + "\n"
    return result


def filter_and_sort(list_group_api):
    results = list()
    keys = list_group_api.keys()
    for element in toc:
        if element in keys:
            results.append(element)
    for element in keys:
        if element not in results:
            results.append(element)
    return results


def main():
    list_group_api = get_api_list()

    _toc = filter_and_sort(list_group_api)

    file_desc = open(FILENAME, "w")
    length_of_title = len("Moon {component} API".format(component=COMPONENT))
    file_desc.write(HEADERS.format(
        component=COMPONENT,
        date=CURRENT_TIME,
        revision=REVISION,
        title_headers="="*length_of_title,
        author=AUTHOR
    ))

    for key in _toc:
        logger.info(key)
        file_desc.write("{}\n".format(key))
        file_desc.write("{}\n\n".format("="*len(key)))
        if "description" in list_group_api[key]:
            file_desc.write("{}\n\n".format(list_group_api[key]["description"]))
        version = "unknown"
        logger.debug(list_group_api.keys())
        if "version" in list_group_api[key]:
            version = list_group_api[key]["version"]
        file_desc.write("Version: {}\n\n".format(version))
        for api in list_group_api[key]:
            logger.info("\t{}".format(api))
            if api in ("description", "version"):
                continue
            file_desc.write("{}\n".format(api))
            file_desc.write("{}\n\n".format("-" * len(api)))

            file_desc.write("{}\n\n".format(list_group_api[key][api]["description"]))

            file_desc.write("URLs are:\n\n")
            for _url in list_group_api[key][api]["urls"]:
                file_desc.write("* {}\n".format(_url))

            file_desc.write("\nMethods are:\n\n")
            for _method in list_group_api[key][api]["methods"]:
                file_desc.write("→ {}\n".format(_method))
                file_desc.write("{}\n\n".format("~"*(len(_method) + 2)))
                file_desc.write("{}\n\n".format(analyse_description(list_group_api[key][api]["methods"][_method])))

HEADERS = """{title_headers}
Moon {component} API
{title_headers}

:Info: See <https://git.opnfv.org/cgit/moon/> for code.
:Author: {author}
:Date: {date}
:Revision: $Revision: {revision} $
:Description: List of the API served by the Moon {component} component

This document list all of the API connectors served by the Moon {component} component
Here are Moon API with some examples of posted data and returned data.
All requests must be prefixed with the host and port, for example: http://localhost:38001/authz/123456789/123456789/servers/list

"""

if __name__ == "__main__":
    main()
