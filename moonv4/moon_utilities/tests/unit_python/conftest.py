import pytest
import requests_mock
import mock_components
import mock_keystone
import mock_cache


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    with requests_mock.Mocker(real_http=True) as m:
        mock_components.register_components(m)
        mock_keystone.register_keystone(m)
        mock_cache.register_cache(m)
        print("End registering URI")
        yield m