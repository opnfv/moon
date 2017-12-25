import mock_repo.components_utilities as comp_util
import pytest
import requests_mock



def test_get_configuration_success():
    from python_moonutilities import configuration
    assert configuration.get_configuration("components/port_start")["components/port_start"] == comp_util.CONF["components"]["port_start"]

@requests_mock.Mocker(kw='mock')
def test_get_configuration_not_found(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components/port_start_wrong', json=[
    ], status_code=500)
    with pytest.raises(Exception) as exception_info:
        configuration.get_configuration("components/port_start_wrong")
    assert str(exception_info.value) == '500: Consul error'

# [TODO] this test used to test the invalid response
# it should be un commented and run after refactoring the related part
@requests_mock.Mocker(kw='mock')
def test_get_configuration_invalid_response(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components_port_start', json=[
        {"components_port_start":'components_port_start', 'Value': comp_util.get_b64_conf("components/port_start")}
    ])
    # with pytest.raises(Exception) as exception_info:
    # configuration.get_configuration("components_port_start")
    # assert str(exception_info.value) == '500: Consul error'

@requests_mock.Mocker(kw='mock')
def test_put_increment_port_failure(**kwargs):
    from python_moonutilities import configuration
    kwargs['mock'].put('http://consul:8500/v1/kv/components_port_start', json=[], status_code=400)
    kwargs['mock'].get('http://consul:8500/v1/kv/components_port_start', json=[
        {'Key': 'components_port_start', 'Value': comp_util.get_b64_conf("components/port_start")}
    ], status_code=200)
    with pytest.raises(Exception) as exception_info:
        configuration.increment_port()
    assert str(exception_info.value) == '400: Consul error'

def test_increment_port_success():
    from python_moonutilities import configuration
    cur_port = comp_util.CONF["components"]["port_start"]
    incremented_port = configuration.increment_port()
    assert incremented_port  == cur_port + 1


def test_get_components():
    from python_moonutilities import configuration
    assert isinstance(configuration.get_components(), dict)