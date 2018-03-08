import json
import os
import logging
import argparse


FILES = [
    "cinder.policy.json",
    "glance.policy.json",
    "keystone.policy.json",
    "neutron.policy.json",
    "nova.policy.json",
]
policy = {
    "pdps": [{
        "name": "external_pdp",
        "keystone_project_id": "",
        "description": "",
        "policies": [{"name": "OpenStack RBAC Policy"}]}
    ],

    "policies": [{
        "name": "OpenStack RBAC Policy",
        "genre": "authz",
        "description": "A RBAC policy similar of what you can find through policy.json files",
        "model": {"name": "OPST_RBAC"}, "mandatory": True, "override": True}
    ],

    "models": [{"name": "OPST_RBAC", "description": "", "meta_rules": [{"name": "rbac"}], "override": True}],

    "subjects": [
        {"name": "admin", "description": "", "extra": {}, "policies": [{"name": "OpenStack RBAC Policy"}]},
        {"name": "demo", "description": "", "extra": {}, "policies": [{"name": "OpenStack RBAC Policy"}]}
    ],

    "subject_categories": [{ "name":"role", "description": "a role in OpenStack" }],

    "subject_data": [
        { "name": "admin", "description": "the admin role", "policy": {"name": "OpenStack RBAC Policy"}, "category": {"name": "role"}},
        { "name": "member", "description": "the member role", "policy": {"name": "OpenStack RBAC Policy"}, "category": {"name": "role"}}
    ],

    "subject_assignments": [
        {"subject": {"name": "admin"}, "category": {"name": "role"}, "assignments": [{"name": "admin"}, {"name": "member"}]},
        {"subject": {"name": "demo"}, "category": {"name": "role"}, "assignments": [{"name": "member"}]}
    ],

    "objects": [
        {
            "name": "all_vm",
            "description": "represents all virtual machines in this project",
            "extra": {},
            "policies": [{"name": "OpenStack RBAC Policy"}]
        }
    ],

    "object_categories": [{"name": "id", "description": "the UID of each virtual machine"}],

    "object_data": [],

    "object_assignments": [],

    "actions": [],

    "action_categories": [{"name": "action_id", "description": ""}],

    "action_data": [],

    "action_assignments": [],

    "meta_rules": [
        {
            "name": "rbac", "description": "",
            "subject_categories": [{"name": "role"}],
            "object_categories": [{"name": "id"}],
            "action_categories": [{"name": "action_id"}]
        }
    ],

    "rules": [],

}
logger = logging.getLogger(__name__)


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", '-v', action='store_true', help='verbose mode')
    parser.add_argument("--debug", '-d', action='store_true', help='debug mode')
    parser.add_argument("--dir", help='directory containing policy files', default="./policy.json.d")
    parser.add_argument("--indent", '-i', help='indent the output (default:None)', type=int, default=None)
    parser.add_argument("--output", '-o', help='output name', type=str, default="opst_default_policy.json")
    args = parser.parse_args()
    logging_format = "%(levelname)s: %(message)s"
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format=logging_format)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    else:
        logging.basicConfig(format=logging_format)
    return args


def get_rules(args):
    results = {}
    for f in FILES:
        _json_file = json.loads(open(os.path.join(args.dir, f)).read())
        keys = list(_json_file.keys())
        values = list(_json_file.values())
        for value in values:
            if value in keys:
                keys.remove(value)
        component = os.path.basename(f).split(".")[0]
        results[component] = keys
    return results


def build_dict(results):
    for key in results:
        for rule in results[key]:
            _output = {
                "name": rule,
                "description": "{} action for {}".format(rule, key),
                "extra": {"component": key},
                "policies": []
            }
            policy['actions'].append(_output)
            _output = {
                "name": rule,
                "description": "{} action for {}".format(rule, key),
                "policies": [],
                "category": {"name": "action_id"}
            }
            policy['action_data'].append(_output)
            _output = {
                "action": {"name": rule},
                "category": {"name": "action_id"},
                "assignments": [{"name": rule}, ]}
            policy['action_assignments'].append(_output)
            _output = {
                "meta_rule": {"name": "rbac"},
                "rule": {
                    "subject_data": [{"name": "admin"}],
                    "object_data": [{"name": "all_vm"}],
                    "action_data": [{"name": rule}]
                },
                "policy": {"name": "OpenStack RBAC Policy"},
                "instructions": {"decision": "grant"},
                "enabled": True
              }
            policy['rules'].append(_output)
            # TODO: add rules for member only
            # TODO: add rules for everyone


def write_dict(args):
    json.dump(policy, open(args.output, "w"), indent=args.indent)


def main():
    args = init()
    rules = get_rules(args)
    build_dict(rules)
    write_dict(args)


if __name__ == "__main__":
    main()