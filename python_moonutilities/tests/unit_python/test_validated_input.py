import pytest


def test_valid_string():
    from python_moonutilities.security_functions import validate_data
    validate_data("CorrectString")

def test_unvalid_string():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data("Notcorrect String")

    assert str(exception_info.value) == 'String contains space'

def test_empty_string():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data("")

    assert str(exception_info.value) == 'Empty String'


def test_none_value():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(None)

    assert str(exception_info.value) == 'Value is Not String or Container or Dictionary'


def test_int_value():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(1)

    assert str(exception_info.value) == 'Value is Not String or Container or Dictionary'


def test_float_value():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(1.23)

    assert str(exception_info.value) == 'Value is Not String or Container or Dictionary'


def test_correct_list():
    from python_moonutilities.security_functions import validate_data
    validate_data(["skjdnfa","dao","daosdjpw"])


def test_correct_list():
    from python_moonutilities.security_functions import validate_data
    validate_data(["skjdnfa"])


def test_correct_instead_list():
    from python_moonutilities.security_functions import validate_data
    validate_data([["skjdnfa","daswi"],[["daskdlw"],["daklwo"]],["dawl","afioa"],["dawno"]])


def test_empty_list():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data([])

    assert str(exception_info.value) == 'Empty Container'


def test_empty_list_inside_other_list():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(["dajiwdj",[]])

    assert str(exception_info.value) == 'Empty Container'


def test_incorrect_string_inside_list():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(["dajiwdj",["dakwe","daow awoepa"]])

    assert str(exception_info.value) == 'String contains space'


def test_empty_string_inside_list():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(["dajiwdj", ["dakwe", ""]])

    assert str(exception_info.value) == 'Empty String'


def test_correct_tuples():
    from python_moonutilities.security_functions import validate_data
    validate_data(("dasdw","dawdwa"))


def test_empty_tuples():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(())

    assert str(exception_info.value) == 'Empty Container'

def test_correct_tuple_of_tuple():
    from python_moonutilities.security_functions import validate_data
    validate_data(("gjosjefa",("diwajdi","oejfoea"),(("jwdi","fjia"),("nfioa","ifao"))))


def test_incorrect_tuple():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data(("djawo","dowa afw"))

    assert str(exception_info.value) == 'String contains space'


def test_correct_dictionary():
    from python_moonutilities.security_functions import validate_data
    validate_data({"daiwdw":"dwioajd"})


def test_incorrect_dictionary():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data({"daiwdw":"dwioa jd"})

    assert str(exception_info.value) == 'String contains space'

def test_empty_dictionary():
    from python_moonutilities.security_functions import validate_data
    with pytest.raises(Exception) as exception_info:
        validate_data({})

    assert str(exception_info.value) == 'Empty Dictionary'


def test_correct_function_pass():
    from python_moonutilities.security_functions import validate_input

    @validate_input()
    def temp_function(string,list,tuple):
        if string!="teststring" :
            raise ValueError("values which passed incorrect")

    temp_function("teststring",["teststring",["teststring"]],("teststring",("teststring")))

def test_incorrect_function_pass1():
    from python_moonutilities.security_functions import validate_input

    @validate_input()
    def temp_function(string, list, tuple):
        if string != "teststring":
            raise ValueError("values which passed incorrect")

    with pytest.raises(Exception) as exception_info:
        temp_function("teststring",list=["teststring", ["testst ring"]],tuple=("teststring", ("teststri ng")))

    assert str(exception_info.value) == 'String contains space'


def test_incorrect_function_pass2():
    from python_moonutilities.security_functions import validate_input

    @validate_input()
    def temp_function(string, list, dictionary):
        if string != "teststring":
            raise ValueError("values which passed incorrect")

    with pytest.raises(Exception) as exception_info:
        temp_function("teststring", ["teststring", ["teststri ng"]], {"teststring": ("teststring")})

    assert str(exception_info.value) == 'String contains space'


def test_incorrect_function_pass3():
    from python_moonutilities.security_functions import validate_input

    class x:
        @validate_input()
        def temp_function(string, list, dictionary):
            if string != "teststring":
                raise ValueError("values which passed incorrect")

    e=x;

    with pytest.raises(Exception) as exception_info:
        e.temp_function("teststring", ["teststring", ["teststri ng"]], {"teststring": ("teststring")})

    assert str(exception_info.value) == 'String contains space'
