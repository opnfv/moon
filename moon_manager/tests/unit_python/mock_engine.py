# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



def register_engine(m):
    for port in range(20000, 20010):
        m.register_uri(
            'POST', 'http://127.0.0.1:{}/update'.format(port),
            json={}
        )
