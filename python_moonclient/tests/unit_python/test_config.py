import pytest
from . import utilities


def test_authz_request():
    from python_moonclient.core import config
    conf_data = config.get_config_data("consul", 8500)
    assert isinstance(conf_data, dict)
