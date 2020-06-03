from python_moonclient.core.cli_exceptions import  MoonCliException


def test_authz_request():
    from python_moonclient.core import config
    conf_data = config.get_config_data("consul", 8500)
    if not isinstance(conf_data, dict):
        raise MoonCliException("Unexpected error : the conf data is not a dictionnary")
