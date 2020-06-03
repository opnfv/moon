# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



__version__ = "0.8"


def get_api_key(url, user, password):
    import requests
    from requests.auth import HTTPBasicAuth
    _url = url + "/auth"
    req = requests.get(_url, auth=HTTPBasicAuth(user, password))
    if req.status_code != 200:
        raise Exception("Cannot authenticate on {} with {}".format(_url, user))
    return req.content.decode("utf-8").strip('"')


def serve(hostname="127.0.0.1", port=8080):
    import hug
    import moon_engine.server
    hug.API(moon_engine.server).http.serve(host=hostname, port=port, display_intro=False)
