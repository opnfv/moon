# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
import json


# def test_local_perimeter_get_subject():
#     from moon_manager.api import perimeter
#     subjects = perimeter.Subjects.get()
#     assert isinstance(subjects, dict)
#     assert "subjects" in subjects



# def test_http_perimeter_post_subject():
#     from moon_manager.api import perimeter
#     result = hug.test.post(perimeter, 'subjects/b34e5a2954944cc59356daa244b8c254',
#                            body={'name': 'ha'},
#                            headers={'Content-Type': 'application/json'})
#     assert result.status == hug.HTTP_200
#     assert isinstance(result.data, dict)
#     assert "subjects" in result.data
#
#
# def test_http_perimeter_get_subject_2():
#     from moon_manager.api import perimeter
#     result = hug.test.get(perimeter, 'subjects/b34e5a29-5494-4cc5-9356-daa244b8c254')
#     assert result.status == hug.HTTP_200
#     assert isinstance(result.data, dict)
#     assert "subjects" in result.data
#
# def test_http_perimeter_get_subject_3():
#     from moon_manager.api import perimeter
#     result = hug.test.get(perimeter, 'policies/b34e5a29-5494-4cc5-9356-daa244b8c254/subjects/')
#     assert result.status == hug.HTTP_200
#     assert isinstance(result.data, dict)
#     assert "subjects" in result.data
#
#
# def test_http_perimeter_get_subject_4():
#     from moon_manager.api import perimeter
#     result = hug.test.get(perimeter, 'policies/b34e5a29-5494-4cc5-9356-daa244b8c254/subjects/b34e5a29-5494-4cc5-9356-daa244b8c254')
#     assert result.status == hug.HTTP_200
#     assert isinstance(result.data, dict)
#     assert "subjects" in result.data
