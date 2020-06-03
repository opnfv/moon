# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug


def test_status(benchmark):
    from moon_engine.api import status

    # Fixme: Add tests on enforce function to have a benchmark on enforce rapidity
    req = benchmark(hug.test.get, status, "/status")
    assert isinstance(req.data, dict)
