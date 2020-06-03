import pytest
import requests_mock
import mock_repo


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """ Modify the response from Requests module
    """
    with requests_mock.Mocker(real_http=True) as m:
        mock_repo.register_cache(m)

        print("End registering URI")
        yield m