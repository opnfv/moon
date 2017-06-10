import argparse
import logging
from importlib.machinery import SourceFileLoader
from utils.pdp import *
from utils.models import *
from utils.policies import *

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='scenario filename', nargs=1)
parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
args = parser.parse_args()

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.WARNING)

logger = logging.getLogger(__name__)

if args.filename:
    print("Loading: {}".format(args.filename[0]))

m = SourceFileLoader("scenario", args.filename[0])

scenario = m.load_module()


def create_model(model_id=None):
    if args.verbose:
        logger.warning("Creating model {}".format(scenario.model_name))
    if not model_id:
        model_id = add_model(name=scenario.model_name)
    for cat in scenario.subject_categories:
        scenario.subject_categories[cat] = add_subject_category(name=cat)
    for cat in scenario.object_categories:
        scenario.object_categories[cat] = add_object_category(name=cat)
    for cat in scenario.action_categories:
        scenario.action_categories[cat] = add_action_category(name=cat)
    sub_cat = []
    ob_cat = []
    act_cat = []
    meta_rule_list = []
    for item_name, item_value in scenario.meta_rule.items():
        for item in item_value["value"]:
            if item in scenario.subject_categories:
                sub_cat.append(scenario.subject_categories[item])
            elif item in scenario.object_categories:
                ob_cat.append(scenario.object_categories[item])
            elif item in scenario.action_categories:
                act_cat.append(scenario.action_categories[item])
        meta_rules = check_meta_rule(meta_rule_id=None)
        for _meta_rule_id, _meta_rule_value in meta_rules['meta_rules'].items():
            if _meta_rule_value['name'] == item_name:
                meta_rule_id = _meta_rule_id
                break
        else:
            meta_rule_id = add_meta_rule(item_name, sub_cat, ob_cat, act_cat)
        item_value["id"] = meta_rule_id
        if meta_rule_id not in meta_rule_list:
            meta_rule_list.append(meta_rule_id)
    return model_id, meta_rule_list


def create_policy(model_id, meta_rule_list):
    if args.verbose:
        logger.warning("Creating policy {}".format(scenario.policy_name))
    _policies = check_policy()
    for _policy_id, _policy_value in _policies["policies"].items():
        if _policy_value['name'] == scenario.policy_name:
            policy_id = _policy_id
            break
    else:
        policy_id = add_policy(name=scenario.policy_name, genre=scenario.policy_genre)

    update_policy(policy_id, model_id)

    for meta_rule_id in meta_rule_list:
        print("add_meta_rule_to_model {} {}".format(model_id, meta_rule_id))
        add_meta_rule_to_model(model_id, meta_rule_id)

    for subject_cat_name in scenario.subject_data:
        for subject_data_name in scenario.subject_data[subject_cat_name]:
            data_id = scenario.subject_data[subject_cat_name][subject_data_name] = add_subject_data(
                policy_id=policy_id,
                category_id=scenario.subject_categories[subject_cat_name], name=subject_data_name)
            scenario.subject_data[subject_cat_name][subject_data_name] = data_id
    for object_cat_name in scenario.object_data:
        for object_data_name in scenario.object_data[object_cat_name]:
            data_id = scenario.object_data[object_cat_name][object_data_name] = add_object_data(
                policy_id=policy_id,
                category_id=scenario.object_categories[object_cat_name], name=object_data_name)
            scenario.object_data[object_cat_name][object_data_name] = data_id
    for action_cat_name in scenario.action_data:
        for action_data_name in scenario.action_data[action_cat_name]:
            data_id = scenario.action_data[action_cat_name][action_data_name] = add_action_data(
                policy_id=policy_id,
                category_id=scenario.action_categories[action_cat_name], name=action_data_name)
            scenario.action_data[action_cat_name][action_data_name] = data_id

    for name in scenario.subjects:
        scenario.subjects[name] = add_subject(policy_id, name=name)
    for name in scenario.objects:
        scenario.objects[name] = add_object(policy_id, name=name)
    for name in scenario.actions:
        scenario.actions[name] = add_action(policy_id, name=name)

    for subject_name in scenario.subject_assignments:
        if type(scenario.subject_assignments[subject_name]) in (list, tuple):
            for items in scenario.subject_assignments[subject_name]:
                for subject_category_name in items:
                    subject_id = scenario.subjects[subject_name]
                    subject_cat_id = scenario.subject_categories[subject_category_name]
                    for data in scenario.subject_assignments[subject_name]:
                        subject_data_id = scenario.subject_data[subject_category_name][data[subject_category_name]]
                        add_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id)
        else:
            for subject_category_name in scenario.subject_assignments[subject_name]:
                subject_id = scenario.subjects[subject_name]
                subject_cat_id = scenario.subject_categories[subject_category_name]
                subject_data_id = scenario.subject_data[subject_category_name][scenario.subject_assignments[subject_name][subject_category_name]]
                add_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id)
        
    for object_name in scenario.object_assignments:
        if type(scenario.object_assignments[object_name]) in (list, tuple):
            for items in scenario.object_assignments[object_name]:
                for object_category_name in items:
                    object_id = scenario.objects[object_name]
                    object_cat_id = scenario.object_categories[object_category_name]
                    for data in scenario.object_assignments[object_name]:
                        object_data_id = scenario.object_data[object_category_name][data[object_category_name]]
                        add_object_assignments(policy_id, object_id, object_cat_id, object_data_id)
        else:
            for object_category_name in scenario.object_assignments[object_name]:
                object_id = scenario.objects[object_name]
                object_cat_id = scenario.object_categories[object_category_name]
                object_data_id = scenario.object_data[object_category_name][scenario.object_assignments[object_name][object_category_name]]
                add_object_assignments(policy_id, object_id, object_cat_id, object_data_id)

    for action_name in scenario.action_assignments:
        if type(scenario.action_assignments[action_name]) in (list, tuple):
            for items in scenario.action_assignments[action_name]:
                for action_category_name in items:
                    action_id = scenario.actions[action_name]
                    action_cat_id = scenario.action_categories[action_category_name]
                    for data in scenario.action_assignments[action_name]:
                        action_data_id = scenario.action_data[action_category_name][data[action_category_name]]
                        add_action_assignments(policy_id, action_id, action_cat_id, action_data_id)
        else:
            for action_category_name in scenario.action_assignments[action_name]:
                action_id = scenario.actions[action_name]
                action_cat_id = scenario.action_categories[action_category_name]
                action_data_id = scenario.action_data[action_category_name][scenario.action_assignments[action_name][action_category_name]]
                add_action_assignments(policy_id, action_id, action_cat_id, action_data_id)

    for meta_rule_name in scenario.rules:
        meta_rule_value = scenario.meta_rule[meta_rule_name]
        for rule in scenario.rules[meta_rule_name]:
            data_list = []
            _meta_rule = list(meta_rule_value["value"])
            for data_name in rule["rule"]:
                category_name = _meta_rule.pop(0)
                if category_name in scenario.subject_categories:
                    data_list.append(scenario.subject_data[category_name][data_name])
                elif category_name in scenario.object_categories:
                    data_list.append(scenario.object_data[category_name][data_name])
                elif category_name in scenario.action_categories:
                    data_list.append(scenario.action_data[category_name][data_name])
            instructions = rule["instructions"]
            add_rule(policy_id, meta_rule_value["id"], data_list, instructions)
    return policy_id


def create_pdp(policy_id=None):
    if args.verbose:
        logger.warning("Creating PDP {}".format(scenario.pdp_name))
    projects = get_keystone_projects()
    admin_project_id = None
    for _project in projects['projects']:
        if _project['name'] == "admin":
            admin_project_id = _project['id']
    assert admin_project_id
    pdps = check_pdp()["pdps"]
    for pdp_id, pdp_value in pdps.items():
        if scenario.pdp_name == pdp_value["name"]:
            update_pdp(pdp_id, policy_id=policy_id)
            logger.info("Found existing PDP named {} (will add policy {})".format(scenario.pdp_name, policy_id))
            return pdp_id
    _pdp_id = add_pdp(name=scenario.pdp_name, policy_id=policy_id)
    map_to_keystone(pdp_id=_pdp_id, keystone_project_id=admin_project_id)
    return _pdp_id

if __name__ == "__main__":
    _models = check_model()
    for _model_id, _model_value in _models['models'].items():
        if _model_value['name'] == scenario.model_name:
            model_id = _model_id
            meta_rule_list = _model_value['meta_rules']
            create_model(model_id)
            break
    else:
        model_id, meta_rule_list = create_model()
    policy_id = create_policy(model_id, meta_rule_list)
    pdp_id = create_pdp(policy_id)
