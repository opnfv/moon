
def test_get_components():
    from python_moonutilities import configuration
    assert isinstance(configuration.get_components(), dict)

