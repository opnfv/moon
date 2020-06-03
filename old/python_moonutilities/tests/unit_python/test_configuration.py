import mock_repo.components_utilities as comp_util
import pytest
import requests_mock


def test_get_configuration_success():
    from python_moonutilities import configuration
    assert configuration.get_configuration("components/port_start")["components/port_start"] == comp_util.CONF["components"]["port_start"]


@requests_mock.Mocker(kw='mock')
def test_get_configuration_mutliple_list_success(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components/port_start',
                       json=[
                           {'Key': 'port_start', 'Value': comp_util.get_b64_conf("components/port_start")},
                           {'Key': 'port_start', 'Value': comp_util.get_b64_conf("components/port_start")}
                             ]
                       )

    assert len(configuration.get_configuration("components/port_start")) == 2


@requests_mock.Mocker(kw='mock')
def test_get_configuration_mutliple_list_failure(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components/port_start',
                       json=[
                           {'Key': 'port_start', 'Value': comp_util.get_b64_conf("components/port_start")},
                           {'invalidKey': 'port_start', 'Value': comp_util.get_b64_conf("components/port_start")}
                             ]
                       )
    with pytest.raises(Exception) as exception_info:
        configuration.get_configuration("components/port_start")
    assert str(exception_info.value) == '500: Consul Content error'


@requests_mock.Mocker(kw='mock')
def test_get_configuration_not_found(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components/port_start_wrong', json=[
    ], status_code=500)
    with pytest.raises(Exception) as exception_info:
        configuration.get_configuration("components/port_start_wrong")
    assert str(exception_info.value) == '500: Consul error'


@requests_mock.Mocker(kw='mock')
def test_get_configuration_invalid_response(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components/port_start', json=[
        {"port_start":'port_start', 'Value': comp_util.get_b64_conf("components/port_start")}
    ])
    with pytest.raises(Exception) as exception_info:
        configuration.get_configuration("components/port_start")
    assert str(exception_info.value) == '500: Consul Content error'


################################ increment_port ####################################
@requests_mock.Mocker(kw='mock')
def test_put_increment_port_invalidkey_failure(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components/port_start', json=[
        {'Key': 'invalidkey', 'Value': comp_util.get_b64_conf("components/port_start")}
    ], status_code=200)
    with pytest.raises(Exception) as exception_info:
        configuration.increment_port()
    assert str(exception_info.value) == '500: Consul Content error'


@requests_mock.Mocker(kw='mock')
def test_put_increment_port_failure(**kwargs):
    from python_moonutilities import configuration
    kwargs['mock'].put('http://consul:8500/v1/kv/components/port_start', json=[], status_code=400)
    kwargs['mock'].get('http://consul:8500/v1/kv/components/port_start', json=[
        {'Key': 'port_start', 'Value': comp_util.get_b64_conf("components/port_start")}
    ], status_code=200)
    with pytest.raises(Exception) as exception_info:
        configuration.increment_port()
    assert str(exception_info.value) == '500: Consul Content error'


def test_increment_port_success():
    from python_moonutilities import configuration
    cur_port = comp_util.CONF["components"]["port_start"]
    incremented_port = configuration.increment_port()
    assert incremented_port == cur_port + 1


################################ plugin ####################################
def test_get_plugins_success():
    from python_moonutilities import configuration
    plugin = configuration.get_plugins()
    assert plugin is not None

def test_get_plugins_failure(no_requests):
    from python_moonutilities import configuration
    no_requests.register_uri(
        'GET', 'http://consul:8500/v1/kv/components/pipeline',
        json=[{'Key': 'components/pipeline', 'Value': 'eyJjb250YWluZXIiOiAid3Vrb25nc3VuL21vb25fYXV0aHo6djQuMyIsICJwb3J0IjogODA4MX0='}]
    )
    with pytest.raises(Exception) as exception_info:
        configuration.get_plugins()
    assert str(exception_info.value) == '500: Consul Content error'
################################ component ####################################
def test_get_components():
    from python_moonutilities import configuration
    assert isinstance(configuration.get_components(), dict)


@requests_mock.Mocker(kw='mock')
def test_get_components_mutliple_list_success(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components?recurse=true',
                       json=[
                           {'Key': 'components/c1', 'Value': 'eyJjb250YWluZXIiOiAid3Vrb25nc3VuL21vb25fYXV0aHo6djQuMyIsICJwb3J0IjogODA4MX0='},
                           {'Key': 'components/c2', 'Value': 'eyJjb250YWluZXIiOiAid3Vrb25nc3VuL21vb25fYXV0aHo6djQuMyIsICJwb3J0IjogODA4MX0='}
                             ]
                       )

    res = configuration.get_components()
    assert bool(res)


@requests_mock.Mocker(kw='mock')
def test_get_components_mutliple_list_failure(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components?recurse=true',
                       json=[
                           {'Key': 'components/c1', 'Value': "eyJjb250YWluZXIiOiAid3Vrb25"},
                           {'invalidKey': 'components/c2', 'Value': "eyJjb250YWluZXIiOiAid3Vrb25"}
                             ]
                       )
    with pytest.raises(Exception) as exception_info:
        configuration.get_components()
    assert str(exception_info.value) == '500: Consul Content error'


@requests_mock.Mocker(kw='mock')
def test_get_components_not_found(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components?recurse=true', json=[
    ], status_code=500)
    with pytest.raises(Exception) as exception_info:
        configuration.get_components()
    assert str(exception_info.value) == '400: Consul error'


@requests_mock.Mocker(kw='mock')
def test_get_components_invalid_response(**kwargs):
    from python_moonutilities import configuration

    kwargs['mock'].get('http://consul:8500/v1/kv/components?recurse=true', json=[
        {"invalidKey":'invalid', 'Value': "jb250"}
    ])
    with pytest.raises(Exception) as exception_info:
        configuration.get_components()
    assert str(exception_info.value) == '500: Consul Content error'
