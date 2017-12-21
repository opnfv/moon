import pytest
import utilities


def test_authz_request():
    from python-moonclient import config
    conf_data = config.get_config_data(utilities.CONSUL_HOST, utilities.CONSUL_PORT)
    assert isinstance(conf_data, dict)