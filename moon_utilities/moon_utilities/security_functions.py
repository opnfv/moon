# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



import logging
from moon_utilities import exceptions
import html
import hug

LOGGER = logging.getLogger("moon.utilities." + __name__)


def enforce(action_names, object_name, **extra):
    """Fake version of the enforce decorator"""
    def wrapper_func(func):
        def wrapper_args(*args, **kwargs):
            # TODO: implement the enforce decorator
            return func(*args, **kwargs)
        return wrapper_args
    return wrapper_func


def validate_data(data):
    def __validate_string(string):
        temp_str = html.escape(string)
        if string != temp_str:
            raise exceptions.ValidationContentError('Forbidden characters in string')

    def __validate_list_or_tuple(container):
        for i in container:
            validate_data(i)

    def __validate_dict(dictionary):
        for key in dictionary:
            validate_data(dictionary[key])

    if isinstance(data, bool):
        return True
    if data is None:
        data = ""
    if isinstance(data, str):
        __validate_string(data)
    elif isinstance(data, list) or isinstance(data, tuple):
        __validate_list_or_tuple(data)
    elif isinstance(data, dict):
        __validate_dict(data)
    else:
        raise exceptions.ValidationContentError('Value is Not String or Container or Dictionary: {}'.format(data))


def validate_input(*validators):
    """Validation only succeeds if all passed in validators return no errors"""
    body_state = {"name", "id", "category_id", "data_id"}

    def validate_all_input(fields, **kwargs):
        try:
            for validator in validators:
                # errors = validator(fields)
                if validator not in fields:
                    raise exceptions.ValidationKeyError('Invalid Key :{} not found'.format(validator))

            for field in body_state:
                if field in fields:
                    try:
                        validate_data(fields[field])
                    except exceptions.ValidationContentError as e:
                        raise exceptions.ValidationContentError("Key: '{}', [{}]".format(field, str(e)))
        except Exception as e:
            LOGGER.exception(e)
            raise e
        return fields

    validate_all_input.__doc__ = " and ".join(validator.__doc__ for validator in validators)
    return validate_all_input
