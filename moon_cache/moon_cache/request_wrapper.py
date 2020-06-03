# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import sys
import requests
from moon_utilities import exceptions


def get(url, **kwarg):
    try:
        response = requests.get(url, **kwarg)
    except requests.exceptions.RequestException as _exc:
        raise exceptions.MoonError("request failure ", _exc)
    except Exception as _exc:
        raise exceptions.MoonError("Unexpected error ", _exc)
    return response


def put(url, json="", **kwarg):
    try:
        response = requests.put(url, json=json, **kwarg)
    except requests.exceptions.RequestException as _exc:
        raise exceptions.MoonError("request failure ", _exc)
    except Exception as _exc:
        raise exceptions.MoonError("Unexpected error ", _exc)
    return response
