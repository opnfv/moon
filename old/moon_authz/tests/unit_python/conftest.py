import pytest
import requests_mock
import mock_pods
import os
from utilities import CONTEXT


@pytest.fixture
def context():
    return CONTEXT


def set_env_variables():
    os.environ['UUID'] = "1111111111"
    os.environ['TYPE'] = "authz"
    os.environ['PORT'] = "8081"
    os.environ['PDP_ID'] = "b3d3e18abf3340e8b635fd49e6634ccd"
    os.environ['META_RULE_ID'] = "f8f49a779ceb47b3ac810f01ef71b4e0"
    os.environ['KEYSTONE_PROJECT_ID'] = CONTEXT['project_id']


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    set_env_variables()
    with requests_mock.Mocker(real_http=True) as m:
        mock_pods.register_pods(m)
        yield m
