# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from falcon import HTTP_400, HTTP_401, HTTP_402, HTTP_403, HTTP_404, HTTP_405, \
    HTTP_406, HTTP_407, HTTP_408, HTTP_409, HTTP_500

ERROR_CODE = {
    400: HTTP_400,
    401: HTTP_401,
    402: HTTP_402,
    403: HTTP_403,
    404: HTTP_404,
    405: HTTP_405,
    406: HTTP_406,
    407: HTTP_407,
    408: HTTP_408,
    409: HTTP_409,
    500: HTTP_500
}
