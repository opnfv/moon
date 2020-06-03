# Copyright 2018 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import pytest


def test_valid_string():
    from python_moonutilities.security_functions import validate_data
    validate_data("CorrectString")
    validate_data("Correct String")
    validate_data("Correct String!")
    validate_data("Correct String@")
    validate_data(None)
    validate_data(True)


def test_invalid_string():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data("Notcorrect<a>String")

    assert str(exception_info.value) == 'Forbidden characters in string'


def test_none_value():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(object)

    assert 'Value is Not String or Container or Dictionary' in str(exception_info.value)


def test_numeric_value():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(1)
    assert 'Value is Not String or Container or Dictionary' in str(exception_info.value)

    with pytest.raises(Exception) as exception_info:
        validate_data(1.23)
    assert 'Value is Not String or Container or Dictionary' in str(exception_info.value)


def test_correct_list_one_element():
    from python_moonutilities.security_functions import validate_data
    validate_data(["test_1", "test_2", "test_3"])


def test_correct_list_multiple_element():
    from python_moonutilities.security_functions import validate_data
    validate_data(["test"])


def test_correct_nested_list():
    from python_moonutilities.security_functions import validate_data
    validate_data([["test_1", "test_2"], [["test_3"], ["test_4"]], ["test_5", "test_6"], ["test_7"]])


def test_incorrect_string_inside_list():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(["test_1", ["test_2", "forbidden<a>character"]])

    assert str(exception_info.value) == 'Forbidden characters in string'


def test_correct_tuples():
    from python_moonutilities.security_functions import validate_data
    validate_data(("test_1", "test_2"))


def test_correct_tuple_of_tuple():
    from python_moonutilities.security_functions import validate_data
    validate_data(("test_1", ("test_2", "test_3"), (("test_4", "test_5"), ("test_6", "test_7"))))


def test_incorrect_string_within_tuple():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(("test_1", "forbidden<a>character"))

    assert str(exception_info.value) == 'Forbidden characters in string'


def test_correct_dictionary():
    from python_moonutilities.security_functions import validate_data
    validate_data({"test_1": "test_2"})


def test_incorrect_string_within_dictionary():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data({"test_1": "forbidden<a>character"})

    assert str(exception_info.value) == 'Forbidden characters in string'


def test_correct_function_pass():
    from python_moonutilities.security_functions import validate_input

    @validate_input()
    def temp_function(string, list, tuple):
        if string != "teststring":
            raise ValueError("values which passed incorrect")

    temp_function("teststring", ["teststring", ["teststring"]], ("teststring", ("teststring", )))


def test_incorrect_validating_function_with_kwargs():
    from python_moonutilities.security_functions import validate_input

    @validate_input(kwargs_state=[True,True])
    def temp_function(string, list, tuple):
        if string != "teststring":
            raise ValueError("values which passed incorrect")

    with pytest.raises(Exception) as exception_info:
        temp_function("teststring", list=["teststring", ["testst<a>ring"]],tuple=("teststring", ("teststri<a>ng", )))

    assert str(exception_info.value) == 'Forbidden characters in string'


def test_incorrect_validating_function():
    from python_moonutilities.security_functions import validate_input

    @validate_input()
    def temp_function(string, list, dictionary):
        if string != "teststring":
            raise ValueError("values which passed incorrect")

    with pytest.raises(Exception) as exception_info:
        temp_function("teststring", ["teststring", ["teststri<a>ng"]], {"teststring": ("teststring", )})

    assert str(exception_info.value) == 'Forbidden characters in string'


def test_incorrect_validating_class_function():
    from python_moonutilities.security_functions import validate_input

    class Testclass:
        @validate_input()
        def temp_function(self, string, list, dictionary):
            if string != "teststring":
                raise ValueError("values which passed incorrect")

    e = Testclass()

    with pytest.raises(Exception) as exception_info:
        e.temp_function("teststring", ["teststring", ["teststri<a>ng"]], {"teststring": ("teststring", )})

    assert str(exception_info.value) == 'Forbidden characters in string'
