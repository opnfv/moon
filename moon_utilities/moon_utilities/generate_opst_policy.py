# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Generate a policy template from a list of OpenStack policy.json file
"""
import argparse
import json
import logging
import os
import re
import glob
import copy


FILES = [
    "cinder.policy.json",
    "glance.policy.json",
    "keystone.policy.json",
    "neutron.policy.json",
    "nova.policy.json",
]
policy_in = {
    "pdps": [
        {
            "name": "external_pdp",
            "keystone_project_id": "",
            "description": "",
            "policies": [{"name": "OpenStack RBAC Policy"}]
        }
    ],

    "policies": [
        {
            "name": "OpenStack RBAC Policy",
            "genre": "authz",
            "description": "A RBAC policy similar of what you can find through policy.json files",
            "model": {"name": "OPST_RBAC"}, "mandatory": True, "override": True
        }
    ],

    "models": [
        {
            "name": "OPST_RBAC",
            "description": "",
            "meta_rules": [{"name": "rbac"}],
            "override": True
        }
    ],

    "subjects": [
        {"name": "admin", "description": "", "extra": {},
         "policies": [{"name": "OpenStack RBAC Policy"}]}
    ],

    "subject_categories": [{"name": "role", "description": "a role in OpenStack"}],

    "subject_data": [
        {"name": "admin", "description": "the admin role",
         "policies": [], "category": {"name": "role"}},
        {"name": "member", "description": "the member role",
         "policies": [], "category": {"name": "role"}}
    ],

    "subject_assignments": [
        {"subject": {"name": "admin"}, "category": {"name": "role"},
         "assignments": [{"name": "admin"}, {"name": "member"}]},
    ],

    "objects": [
        {"name": "all", "description": "describe all element of a project", "extra": {},
         "policies": [{"name": "OpenStack RBAC Policy"}]},
    ],

    "object_categories": [{"name": "id", "description": "the UID of each virtual machine"}],

    "object_data": [
        {
            "name": "all",
            "description": "represents all virtual machines in this project",
            "policies": [],
            "category": {"name": "id"}},
    ],

    "object_assignments": [
        {"object": {"name": "all"}, "category": {"name": "id"}, "assignments": [{"name": "all"}]}
    ],

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

policy_out = copy.deepcopy(policy_in)

AUTO_EXCLUDE_KEYS = """
context_is_admin
admin_or_owner
admin_api
default
owner
context_is_advsvc
admin_or_network_owner
admin_owner_or_network_owner
admin_only
regular_user
admin_or_data_plane_int
shared
shared_subnetpools
shared_address_scopes
external
admin_required
cloud_admin
service_role
service_or_admin
admin_and_matching_domain_id
service_admin_or_owner
"""

logger = logging.getLogger(__name__)
__rules = []


def init():
    """
    Initialize the application
    :return: argument given in the command line
    """
    global policy_in, policy_out
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", '-v', action='store_true', help='verbose mode')
    parser.add_argument("--debug", '-d', action='store_true', help='debug mode')
    parser.add_argument("--dir",
                        help='directory containing policy files, defaults to ./policy.json.d',
                        default="./policy.json.d")
    parser.add_argument("--template", "-t",
                        help='use a specific template file, defaults to internal template',
                        default="")
    parser.add_argument("--indent", '-i', help='indent the output (default:None)', type=int,
                        default=None)
    parser.add_argument("--output", '-o', help='output name, defaults to opst_default_policy.json',
                        type=str, default="opst_default_policy.json")
    parser.add_argument("--exclude", "-x",
                        help="Exclude some attributes in output "
                             "(example: \"actions,*_categories\")",
                        default="")
    args = parser.parse_args()
    logging_format = "%(levelname)s: %(message)s"
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format=logging_format)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    else:
        logging.basicConfig(format=logging_format)
    if args.template:
        try:
            policy_in = json.loads(open(args.template).read())
            policy_out = copy.deepcopy(policy_in)
            logger.info("Using template {}".format(args.template))
            policy_out.pop('rules')
            policy_out['rules'] = []
            for cpt, item in enumerate(policy_in['rules']):
                if "templates" not in item:
                    policy_out['rules'].append(item)
            policy_out.pop('action_assignments')
            policy_out['action_assignments'] = []
            for cpt, item in enumerate(policy_in['action_assignments']):
                if "templates" not in item:
                    policy_out['action_assignments'].append(item)

        except json.decoder.JSONDecodeError as e:
            logger.error("Cannot decode template file {}".format(args.template))
            if args.debug:
                logger.exception(e)

    return args


def get_json(filename):
    """
    retrieve rule from a JSON file
    :param filename: url of the file
    :return: list of rules in this file
    """
    _json_file = json.loads(open(filename).read())
    keys = list(_json_file.keys())
    values = list(_json_file.values())
    for value in values:
        if value in keys:
            keys.remove(value)
    return keys


def get_flat(filename):
    """
    retrieve rule from a flat text file
    :param filename: url of the file
    :return: list of rules in this file
    """
    results = []
    for line in open(filename):
        key = line.split('"')[1]
        results.append(key)
    return results


def get_opst_rules(args):
    """
    Get all rules in each policy.json
    :param args: arguments given in the command line
    :return: all rules in a dict
    """
    results = {}
    for filename in glob.glob(os.path.join(args.dir, "**/*.json"), recursive=True):
        logger.info("Reading {}".format(filename))
        component = filename.replace("policy.json", "").strip("/")
        component = os.path.basename(component).split(".")[0]
        try:
            keys = get_json(filename)
        except json.decoder.JSONDecodeError:
            keys = get_flat(filename)
        for _key in AUTO_EXCLUDE_KEYS.splitlines():
            if _key in keys:
                keys.remove(_key)
        results[component] = keys
        logger.info("Adding {} definitions in {}".format(len(keys), component))
    return results


def get_policy_name():
    """
    Retrieve the policy name from the policy dict
    Useful if the policy data comes from a template
    """
    for _policy in policy_in.get("policies"):
        return _policy.get("name")


def get_meta_rule_name():
    """
    Retrieve the policy name from the policy dict
    Useful if the policy data comes from a template
    """
    for _policy in policy_in.get("meta_rules"):
        return _policy.get("name")


def get_default_data(data, category):
    """
    Find the default value from a list of data, return the first one if no default found
    :param data: the data to search in
    :param category: the category of the data
    :return: one name contained in data
    """
    for _data in data:
        if _data.get("category").get("name") == category:
            if _data.get("extra", {}).get("action") == "default":
                return _data.get("name")
    # default: return the first one
    for _data in data:
        if _data.get("category").get("name") == category:
            return _data.get("name")


def get_meta_rule(meta_rule_name=None):
    for meta_rule in policy_in['meta_rules']:
        if meta_rule_name == meta_rule.get('name'):
            return meta_rule
        else:
            return policy_in['meta_rules'][0]


def build_actions(opst_rule, component):
    _output = {
        "name": opst_rule,
        "description": "{} action for {}".format(opst_rule, component),
        "extra": {"component": component},
        "policies": []
    }
    policy_out['actions'].append(_output)


def build_action_data(opst_rule, component):
    _output = {
        "name": opst_rule,
        "description": "{} action for {}".format(opst_rule, component),
        "policies": [],
        "category": {"name": "action_id"}
    }
    policy_out['action_data'].append(_output)


def build_action_assignments_with_templates(opst_rule):
    for assignment in policy_in['action_assignments']:
        for template in assignment.get('templates', []):
            name = template.get('action', {}).get('name')
            new = None
            if "filter:" in name:
                if "*" == name.split(":")[-1].strip():
                    new = copy.deepcopy(template)
                    new['action']['name'] = opst_rule
                else:
                    for _str in name.split(":")[-1].strip().split(","):
                        if _str.strip() in opst_rule:
                            new = copy.deepcopy(template)
                            new['action']['name'] = opst_rule
            if new:
                policy_out['action_assignments'].append(new)


def build_action_assignments(opst_rule):
    _output = {
        "action": {"name": opst_rule},
        "category": {"name": "action_id"},
        "assignments": [{"name": opst_rule}, ]}
    policy_out['action_assignments'].append(_output)
    build_action_assignments_with_templates(opst_rule)


def add_rule(rule):
    # TODO: check rule before adding it
    if rule in __rules:
        # note: don't add the rule if already added
        return
    __rules.append(rule)
    _raw_rule = {
        "subject_data": [],
        "object_data": [],
        "action_data": []
    }
    cpt = 0
    for _ in get_meta_rule().get("subject_categories"):
        _raw_rule["subject_data"].append({"name": rule[cpt]})
        cpt += 1
    for _ in get_meta_rule().get("object_categories"):
        _raw_rule["object_data"].append({"name": rule[cpt]})
        cpt += 1
    for _ in get_meta_rule().get("action_categories"):
        _raw_rule["action_data"].append({"name": rule[cpt]})
        cpt += 1

    _output = {
        "meta_rule": {"name": get_meta_rule_name()},
        "rule": _raw_rule,
        "policy": {"name": get_policy_name()},
        "instructions": [{"decision": "grant"}],
        "enabled": True
    }
    policy_out['rules'].append(_output)


def check_filter_on_template(data_list, opst_rule):
    for cpt, _data in enumerate(data_list):
        if "filter:" in _data:
            filter_str = _data.partition(":")[-1]
            if filter_str == "*":
                data_list[cpt] = opst_rule
                add_rule(data_list)
            else:
                for _str in filter_str.split(","):
                    if _str.strip() in opst_rule:
                        data_list[cpt] = opst_rule
                        add_rule(data_list)
                        break


def build_rules_with_templates(rule, opst_rule):
    meta_rule = get_meta_rule()
    for template in rule.get("templates", []):
        data_list = []
        for cat in meta_rule.get("subject_categories"):
            for item in template.get("subject"):
                if item.get("category") == cat.get('name'):
                    data_list.append(item.get("name"))
                    break
        for cat in meta_rule.get("object_categories"):
            for item in template.get("object"):
                if item.get("category") == cat.get('name'):
                    data_list.append(item.get("name"))
                    break
        for cat in meta_rule.get("action_categories"):
            for item in template.get("action"):
                if item.get("category") == cat.get('name'):
                    data_list.append(item.get("name"))
                    break
        check_filter_on_template(data_list, opst_rule)


def build_rules(opst_rule):
    rules = policy_in.get("rules")
    for rule in rules:
        if isinstance(rule, dict):
            build_rules_with_templates(rule, opst_rule)
        else:
            add_rule(rule)


def build_dict(results):
    """
    Build the dictionary given the actions found in the policy.json files
    :param results: list of rule for each component
    :return: nothing
    """
    policy_out["rules"] = []
    for component in results:
        for opst_rule in results[component]:
            build_actions(opst_rule, component)
            build_action_data(opst_rule, component)
            build_action_assignments(opst_rule)
            build_rules(opst_rule)


def exclude_attrs(args):
    """
    Exclude attributes from the output JSON file
    :param args: arguments given in the command line
    :return: nothing
    """
    attrs_to_exclude = []
    if not args.exclude:
        return
    for excl_item in args.exclude.split(","):
        excl_item = excl_item.replace("*", ".*").strip()
        logger.debug("excl_item=%s", excl_item)
        for attr in policy_in:
            logger.debug("attr=%s", attr)
            if re.match(excl_item, attr):
                attrs_to_exclude.append(attr)
    for attr in attrs_to_exclude:
        logger.info("Deleting %s", attr)
        policy_out.pop(attr)


def write_tests(rules):
    if "admin" not in map(lambda x: x.get("name"), policy_in.get("subjects")):
        logger.warning("Don't write tests in output because, there is no 'admin' user")
        return
    if "all" not in map(lambda x: x.get("name"), policy_in.get("objects")):
        logger.warning("Don't write tests in output because, there is no 'all' object")
        return
    if "checks" not in policy_in:
        policy_out["checks"] = {"granted": [], "denied": []}
    if "granted" not in policy_in["checks"]:
        policy_out["checks"]["granted"] = []
    if "denied" not in policy_in["checks"]:
        policy_out["checks"]["denied"] = []
    for component in rules:
        for rule in rules.get(component):
            policy_out["checks"]["granted"].append(("admin", "all", rule))
    if "test_user" in map(lambda x: x.get("name"), policy_in.get("subjects")):
        for component in rules:
            for rule in rules.get(component):
                policy_out["checks"]["denied"].append(("test_user", "all", rule))


def write_dict(args):
    """
    Write the dictionary in the output filename given in command line
    :param args: arguments given in the command line
    :return: nothing
    """
    json.dump(policy_out, open(args.output, "w"), indent=args.indent)


def main():
    """
    Main end point
    :return: nothing
    """
    args = init()
    rules = get_opst_rules(args)
    build_dict(rules)
    write_tests(rules)
    exclude_attrs(args)
    write_dict(args)


if __name__ == "__main__":
    main()
