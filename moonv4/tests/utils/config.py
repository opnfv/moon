import yaml


def get_config_data(filename="moon.conf"):
    data_config = None
    for _file in (
            filename,
            "conf/moon.conf",
            "../moon.conf",
            "../conf/moon.conf",
            "/etc/moon/moon.conf",
    ):
        try:
            data_config = yaml.safe_load(open(_file))
        except FileNotFoundError:
            data_config = None
            continue
        else:
            break
    if not data_config:
        raise Exception("Configuration file not found...")
    return data_config
