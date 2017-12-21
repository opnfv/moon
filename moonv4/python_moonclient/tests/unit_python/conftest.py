import pytest
import requests_mock
from . import mock_config


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    with requests_mock.Mocker(real_http=True) as m:
        mock_config.register_consul(m)
        yield m
