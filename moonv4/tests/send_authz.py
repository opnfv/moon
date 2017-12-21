from importlib.machinery import SourceFileLoader
from python_moonclient import config, parse, models, policies, pdp, authz


if __name__ == "__main__":
    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    if args.filename:
        print("Loading: {}".format(args.filename[0]))
    m = SourceFileLoader("scenario", args.filename[0])
    scenario = m.load_module()

    keystone_project_id = pdp.get_keystone_id(args.pdp)
    time_data = authz.send_requests(
        scenario,
        args.authz_host,
        args.authz_port,
        keystone_project_id,
        request_second=args.request_second,
        limit=args.limit,
        dry_run=args.dry_run,
        stress_test=args.stress_test,
        destination=args.destination
    )
    if not args.dry_run:
        authz.save_data(args.write, time_data)
