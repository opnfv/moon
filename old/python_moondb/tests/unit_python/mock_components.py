import utilities

COMPONENTS = (
    "logging",
    "openstack/keystone",
    "database",
    "slave",
    "components/manager",
    "components/orchestrator",
    "components/interface",
)


def register_components(m):
    for component in COMPONENTS:
        m.register_uri(
            'GET', 'http://consul:8500/v1/kv/{}'.format(component),
            json=[{'Key': component, 'Value': utilities.get_b64_conf(component)}]
        )

    m.register_uri(
        'GET', 'http://consul:8500/v1/kv/components?recurse=true',
        json=[
            {"Key": key, "Value": utilities.get_b64_conf(key)} for key in COMPONENTS
            ],
        # json={'Key': "components", 'Value': get_b64_conf("components")}
    )