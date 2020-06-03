# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



def test_get_attribute_success(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'mode'
    value = "run"
    cache_obj.set_attribute(name=name)
    assert cache_obj.attributes
    assert cache_obj.attributes.get(name)
    assert cache_obj.attributes.get(name) == "build"
    cache_obj.set_attribute(name=name, value=value)
    assert cache_obj.attributes
    assert cache_obj.attributes.get(name)
    # Note: it is the same value because the cache systematically request the Manager
    assert cache_obj.attributes.get(name) == "build"


def test_get_attribute_unknown(configuration):
    from moon_cache import cache
    cache_obj = cache.Cache.getInstance(manager_url=configuration["management"]["url"])
    name = 'test'
    assert cache_obj.attributes
    assert not cache_obj.attributes.get(name)

