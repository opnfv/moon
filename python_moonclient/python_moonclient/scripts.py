import logging
from importlib.machinery import SourceFileLoader
from . import parse, models, policies, pdp, authz


logger = logging.getLogger("python_moonclient.scripts")


def get_keystone_projects():
    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    projects = pdp.get_keystone_projects()

    for _project in projects['projects']:
        print("    {} {}".format(_project['id'], _project['name']))


def create_pdp():
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = True

    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port
    # project_id = args.keystone_pid

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    if args.filename:
        logger.info("Loading: {}".format(args.filename[0]))
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
    pdp_id = pdp.create_pdp(scenario, policy_id=policy_id)


def send_authz_to_wrapper():
    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    if args.filename:
        logger.info("Loading: {}".format(args.filename[0]))
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


def get_pdp():
    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    pdps = pdp.check_pdp()
    for _pdp_key, _pdp_value in pdps["pdps"].items():
        print("    {} {} ({})".format(_pdp_key, _pdp_value['name'],
                                      _pdp_value['keystone_project_id']))


def delete_pdp():
    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    if args.filename:
        logger.info("Deleting: {}".format(args.filename[0]))
        _search = args.filename[0]
        pdps = pdp.check_pdp()
        for _pdp_key, _pdp_value in pdps["pdps"].items():
            if _pdp_key == _search or _pdp_value['name'] == _search:
                logger.info("Found {}".format(_pdp_key))
                pdp.delete_pdp(_pdp_key)
        pdps = pdp.check_pdp()
        logger.info("Listing all PDP:")
        for _pdp_key, _pdp_value in pdps["pdps"].items():
            print("    {} {}".format(_pdp_key, _pdp_value['name']))
            if _pdp_key == _search or _pdp_value['name'] == _search:
                logger.error("Error in deleting {}".format(_search))


def delete_policy():
    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    if args.filename:
        logger.info("Deleting: {}".format(args.filename[0]))
        _search = args.filename[0]
        _policies = policies.check_policy()
        for _policy_key, _policy_value in _policies["policies"].items():
            if _policy_key == _search or _policy_value['name'] == _search:
                logger.info("Found {}".format(_policy_key))
                pdp.delete_pdp(_policy_key)
        _policies = policies.check_policy()
        logger.info("Listing all Policies:")
        for _policy_key, _policy_value in _policies["policies"].items():
            print("    {} {}".format(_policy_key, _policy_value['name']))
            if _policy_key == _search or _policy_value['name'] == _search:
                logger.error("Error in deleting {}".format(_search))


def map_pdp_to_project():
    args = parse.parse()
    consul_host = args.consul_host
    consul_port = args.consul_port

    models.init(consul_host, consul_port)
    policies.init(consul_host, consul_port)
    pdp.init(consul_host, consul_port)

    if args.filename and len(args.filename) == 2:
        logger.info("Mapping: {}=>{}".format(args.filename[0], args.filename[1]))
        # TODO: check if pdp_id and keystone_project_id exist
        pdp.map_to_keystone(pdp_id=args.filename[0], keystone_project_id=args.filename[1])
