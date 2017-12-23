import pytest
import requests_mock
import mock_pods
from utilities import CONTEXT


@pytest.fixture
def context():
    return CONTEXT


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    with requests_mock.Mocker(real_http=True) as m:
        mock_pods.register_pods(m)
        yield m