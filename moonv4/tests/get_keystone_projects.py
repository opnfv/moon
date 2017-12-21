from python_moonclient import parse, models, policies, pdp


if __name__ == "__main__":
    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    projects = pdp.get_keystone_projects()

    for _project in projects['projects']:
        print("{} {}".format(_project['id'], _project['name']))
