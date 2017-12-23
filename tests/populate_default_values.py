import logging
from importlib.machinery import SourceFileLoader
from python_moonclient import parse, models, policies, pdp

logger = logging.getLogger("moonforming")


if __name__ == "__main__":
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
