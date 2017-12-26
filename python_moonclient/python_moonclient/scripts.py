import logging
from importlib.machinery import SourceFileLoader
from . import parse, models, policies, pdp, authz


logger = logging.getLogger("moonclient.scripts")


def get_keystone_projects():
    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    projects = pdp.get_keystone_projects()

    for _project in projects['projects']:
        print("{} {}".format(_project['id'], _project['name']))


def populate_values():
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = True

    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port
    project_id = args.keystone_pid

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    if args.filename:
        print("Loading: {}".format(args.filename[0]))
    m = SourceFileLoader("scenario", args.filename[0])
    scenario = m.load_module()

    _models = models.check_model()
    for _model_id, _model_value in _models['models'].items():
        if _model_value['name'] == scenario.model_name:
            model_id = _model_id
            meta_rule_list = _model_value['meta_rules']
            models.create_model(scenario, model_id)
            break
    else:
        model_id, meta_rule_list = models.create_model(scenario)
    policy_id = policies.create_policy(scenario, model_id, meta_rule_list)
    pdp_id = pdp.create_pdp(scenario, policy_id=policy_id, project_id=project_id)


def send_authz():
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
