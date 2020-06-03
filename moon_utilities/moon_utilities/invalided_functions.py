# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
import requests

logger = logging.getLogger("moon.utilities." + __name__)


def invalidate_assignment_in_slaves(slaves, policy_id, perimeter_id, category_id, data_id, type):
    """
    Send a request to one or more slaves to invalidate specific assignments
    :param slaves: list of slaves
    :param policy_id: the ID of the concerned policy
    :param perimeter_id: the ID of the concerned perimeter
    :param category_id: the ID of the concerned category
    :param data_id: the ID of the concerned data
    :return: None
    """

    hostname, port = "", ""
    uri = "update/assignment"
    result = []
    for key, value in slaves.get('slaves', {}).items():
        if value.get("extra", {}).get("status") != "up":
            continue
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            if policy_id and perimeter_id and category_id and data_id:
                update = requests.delete("http://{}:{}/{}/{}/{}/{}/{}/{}".format(
                    hostname, port, uri, policy_id, type, perimeter_id, category_id, data_id),
                    timeout=1
                )
            elif policy_id and perimeter_id and category_id:
                update = requests.delete("http://{}:{}/{}/{}/{}/{}/{}".format(
                    hostname, port, uri, policy_id, type, perimeter_id, category_id),
                    timeout=1
                )
            elif policy_id and perimeter_id:
                update = requests.delete("http://{}:{}/{}/{}/{}/{}".format(
                    hostname, port, uri, policy_id, type, perimeter_id),
                    timeout=1
                )
            elif policy_id:
                update = requests.delete("http://{}:{}/{}/{}/{}".format(
                    hostname, port, uri, policy_id, type),
                    timeout=1
                )

            logger.debug("result {} {}:{} = {}".format(
                update.status_code,
                hostname,
                port,
                update.text))
            result.append(value.get("name"))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))
    return result


def invalidate_data_in_slaves(slaves, policy_id, category_id, data_id, type):
    """
    Send a request to one or more slaves to invalidate specific data
    :param slaves: list of slaves
    :param policy_id: the ID of the concerned policy
    :param category_id: the ID of the concerned category
    :param data_id: the ID of the concerned data
    :return: None
    """

    hostname, port = "", ""
    uri = "update/data"
    result = []
    for key, value in slaves.get('slaves', {}).items():
        if value.get("extra", {}).get("status") != "up":
            continue
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            update = requests.delete("http://{}:{}/{}/{}/{}".format(
                hostname, port, uri, data_id, type),
                timeout=1
            )
            logger.debug("result {} {}:{} = {}".format(
                update.status_code,
                hostname,
                port,
                update.text))
            result.append(value.get("name"))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))
    return result


def invalidate_perimeter_in_slaves(slaves, policy_id, perimeter_id, type, data=None,
                                   is_delete=True):
    """
    Send a request to one or more slaves to invalidate specific perimeter
    :param slaves: list of slaves
    :param policy_id: the ID of the concerned policy
    :param perimeter_id: the ID of the concerned perimeter
    :return: None
    """

    hostname, port = "", ""
    uri = "update/perimeter"
    result = []
    for key, value in slaves.get('slaves', {}).items():
        if value.get("extra", {}).get("status") != "up":
            continue
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            if is_delete:
                update = requests.delete("http://{}:{}/{}/{}/{}/{}".format(
                    hostname, port, uri, perimeter_id, policy_id, type),
                    timeout=1
                )
            else:
                update = requests.put("http://{}:{}/{}/{}/{}/{}".format(
                    hostname, port, uri, perimeter_id, policy_id, type),
                    data=data,
                    timeout=1
                )
            logger.debug("result {} {}:{} = {}".format(
                update.status_code,
                hostname,
                port,
                update.text))
            result.append(value.get("name"))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))
    return result


def invalidate_pdp_in_slaves(slaves, pdp_id, is_delete=True, data=None):
    """
    Send a request to one or more slaves to invalidate specific PDPs
    :param slaves: list of slaves
    :param pdp_id: the ID of the concerned PDP
    :return: None
    """

    hostname, port = "", ""
    uri = "update/pdp"
    result = []
    for key, value in slaves.get('slaves', {}).items():
        if value.get("extra", {}).get("status") != "up":
            continue
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            if is_delete:
                update = requests.delete("http://{}:{}/{}/{}".format(
                    hostname, port, uri, pdp_id),
                    timeout=1
                )
            else:
                update = requests.put("http://{}:{}/{}/{}".format(
                    hostname, port, uri, pdp_id),
                    data=data,
                    timeout=1
                )
            logger.debug("result {} {}:{} = {}".format(
                update.status_code,
                hostname,
                port,
                update.text))
            result.append(value.get("name"))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))
    return result


def invalidate_policy_in_slaves(slaves, policy_id, is_delete=True, data=None):
    """
    Send a request to one or more slaves to invalidate specific policies
    :param slaves: list of slaves
    :param policy_id: the ID of the concerned policy
    :return: None
    """

    hostname, port = "", ""
    uri = "update/policy"
    result = []
    for key, value in slaves.get('slaves', {}).items():
        if value.get("extra", {}).get("status") != "up":
            continue
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            if is_delete:
                update = requests.delete("http://{}:{}/{}/{}".format(
                    hostname, port, uri, policy_id),
                    timeout=1
                )
            else:
                update = requests.put("http://{}:{}/{}/{}".format(
                    hostname, port, uri, policy_id),
                    data=data,
                    timeout=1
                )

            logger.debug("result {} {}:{} = {}".format(
                update.status_code,
                hostname,
                port,
                update.text))
            result.append(value.get("name"))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))
    return result


def invalidate_rules_in_slaves(slaves, policy_id, rule_id):
    """
    Send a request to one or more slaves to invalidate specific rules
    :param slaves: list of slaves
    :param policy_id: the ID of the concerned policy
    :param rule_id: the ID of the concerned rule
    :return: None
    """

    hostname, port = "", ""
    uri = "update/rule"
    result = []
    for key, value in slaves.get('slaves', {}).items():
        if value.get("extra", {}).get("status") != "up":
            continue
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            update = requests.delete("http://{}:{}/{}/{}/{}".format(
                hostname, port, uri, policy_id, rule_id),
                timeout=1
            )
            logger.debug("result {} {}:{} = {}".format(
                update.status_code,
                hostname,
                port,
                update.text))
            result.append(value.get("name"))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))
    return result


def invalidate_model_in_slaves(slaves, model_id, is_delete=True, data=None):
    """
    Send a request to one or more slaves to invalidate specific models
    :param slaves: list of slaves
    :param model_id: the ID of the concerned model
    :return: None
    """

    hostname, port = "", ""
    uri = "update/model"
    result = []
    for key, value in slaves.get('slaves', {}).items():
        if value.get("extra", {}).get("status") != "up":
            continue
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            if is_delete:
                update = requests.delete("http://{}:{}/{}/{}".format(
                    hostname, port, uri, model_id),
                    timeout=1
                )
            else:
                update = requests.put("http://{}:{}/{}/{}".format(
                    hostname, port, uri, model_id),
                    data=data,
                    timeout=1
                )
            logger.debug("result {} {}:{} = {}".format(
                update.status_code,
                hostname,
                port,
                update.text))
            result.append(value.get("name"))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))
    return result


def invalidate_meta_data_in_slaves(slaves, category_id, type):
    """
    Send a request to one or more slaves to invalidate specific meta data
    :param slaves: list of slaves
    :param category_id: the ID of the concerned category
    :return: None
    """

    hostname, port = "", ""
    uri = "update/meta_data"
    result = []
    for key, value in slaves.get('slaves', {}).items():
        if value.get("extra", {}).get("status") != "up":
            continue
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            update = requests.delete("http://{}:{}/{}/{}/{}".format(
                hostname, port, uri, category_id, type),
                data={
                    "category_id": category_id
                },
                timeout=1
            )
            logger.debug("result {} {}:{} = {}".format(
                update.status_code,
                hostname,
                port,
                update.text))
            result.append(value.get("name"))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))
    return result


def invalidate_meta_rule_in_slaves(slaves, meta_rule_id, is_delete=True, data=None):
    """
    Send a request to one or more slaves to invalidate specific meta rules
    :param slaves: list of slaves
    :param meta_rule_id: the ID of the concerned policy
    :return: None
    """

    hostname, port = "", ""
    uri = "update/meta_rule"
    result = []
    for key, value in slaves.get('slaves', {}).items():
        if value.get("extra", {}).get("status") != "up":
            continue
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            if is_delete:
                update = requests.delete("http://{}:{}/{}/{}".format(
                    hostname, port, uri, meta_rule_id),
                    timeout=1
                )
            else:
                update = requests.put("http://{}:{}/{}/{}".format(
                    hostname, port, uri, meta_rule_id),
                    data=data,
                    timeout=1
                )

            logger.debug("result {} {}:{} = {}".format(
                update.status_code,
                hostname,
                port,
                update.text))
            result.append(value.get("name"))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))


def invalidate_attributes_in_slaves(slaves, name, value=None):
    """
    Send a request to one or more slaves to invalidate specific data
    :param slaves: list of slaves
    :param name: the name of the attribute to invalidate
    :param value: the value that has changed
    :return: a list of updated slaves
    """

    hostname, port = "", ""
    uri = "update/attributes"
    result = []
    for key, value in slaves.items():
        try:
            hostname = value.get("extra", {}).get("server_ip")
            port = value.get("extra", {}).get("port")
            update = requests.delete("http://{}:{}/{}/{}".format(
                hostname, port, uri, name),
                headers={"x-api-key": value.get("extra", {}).get("api_key")},
                timeout=1
            )
            if update.status_code in (200, 202, 206, 208):
                result.append(value.get("name"))
            else:
                logger.warning("Error when updating {} ({})".format(key, update.status_code))
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Cannot reach {}:{}".format(hostname, port))
        except requests.models.InvalidURL:
            logger.warning(
                "Invalid URL {}:{}".format(hostname, port))
    return result


