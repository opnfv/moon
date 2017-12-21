
def test_get_components():
    from moon_utilities import configuration
    assert isinstance(configuration.get_components(), dict)

