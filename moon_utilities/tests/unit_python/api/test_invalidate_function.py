# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import moon_utilities.invalided_functions


def test_invalidate_assignment_in_slaves(slaves):
    result = moon_utilities.invalided_functions.invalidate_assignment_in_slaves(
        slaves, "098764321", "098764321", "098764321", "098764321", 'subject')
    assert result
    assert "slave_test" in list(result)


def test_invalidate_data_in_slaves(slaves):
    result = moon_utilities.invalided_functions.invalidate_data_in_slaves(
        slaves, "__policy_id__", "__category_id__", "098764321", "subject")
    assert result
    assert "slave_test" in list(result)


def test_invalidate_perimeter_in_slaves(slaves):
    result = moon_utilities.invalided_functions.invalidate_perimeter_in_slaves(
        slaves, "098764321", "098764321", "subject", is_delete=False)
    assert result
    assert "slave_test" in list(result)


def test_invalidate_pdp_in_slaves(slaves):
    result = moon_utilities.invalided_functions.invalidate_pdp_in_slaves(
        slaves, "098764321", is_delete=False)
    assert result
    assert "slave_test" in list(result)


def test_invalidate_policy_in_slaves(slaves):
    result = moon_utilities.invalided_functions.invalidate_policy_in_slaves(
        slaves, "098764321", is_delete=False)
    assert result
    assert "slave_test" in list(result)


def test_invalidate_rules_in_slaves():
    pass


def test_invalidate_model_in_slaves():
    pass


def test_invalidate_meta_data_in_slaves():
    pass


def test_invalidate_meta_rule_in_slaves():
    pass
