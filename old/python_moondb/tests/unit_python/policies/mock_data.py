import helpers.model_helper as model_helper
import helpers.meta_rule_helper as meta_rule_helper
import helpers.policy_helper as policy_helper
import helpers.category_helper as category_helper


def create_meta_rule(meta_rule_name="meta_rule1", category_prefix=""):
    meta_rule_value = {
        "name": meta_rule_name,
        "algorithm": "name of the meta rule algorithm",
        "subject_categories": [category_prefix + "subject_category_id1",
                               category_prefix + "subject_category_id2"],
        "object_categories": [category_prefix + "object_category_id1"],
        "action_categories": [category_prefix + "action_category_id1"]
    }
    return meta_rule_value


def create_model(meta_rule_id, model_name="test_model"):
    value = {
        "name": model_name,
        "description": "test",
        "meta_rules": [meta_rule_id]

    }
    return value


def create_policy(model_id, policy_name="policy_1"):
    value = {
        "name": policy_name,
        "model_id": model_id,
        "genre": "authz",
        "description": "test",
    }
    return value


def create_pdp(pdp_ids):
    value = {
        "name": "test_pdp",
        "security_pipeline": pdp_ids,
        "keystone_project_id": "keystone_project_id1",
        "description": "...",
    }
    return value


def get_policy_id(model_name="test_model", policy_name="policy_1", meta_rule_name="meta_rule1", category_prefix=""):
    category_helper.add_subject_category(
        category_prefix + "subject_category_id1",
        value={"name": category_prefix + "subject_category_id1",
               "description": "description 1"})
    category_helper.add_subject_category(
        category_prefix + "subject_category_id2",
        value={"name": category_prefix + "subject_category_id2",
               "description": "description 1"})
    category_helper.add_object_category(
        category_prefix + "object_category_id1",
        value={"name": category_prefix + "object_category_id1",
               "description": "description 1"})
    category_helper.add_action_category(
        category_prefix + "action_category_id1",
        value={"name": category_prefix + "action_category_id1",
               "description": "description 1"})
    meta_rule = meta_rule_helper.add_meta_rule(value=create_meta_rule(meta_rule_name, category_prefix))
    meta_rule_id = list(meta_rule.keys())[0]
    model = model_helper.add_model(value=create_model(meta_rule_id, model_name))
    model_id = list(model.keys())[0]
    value = create_policy(model_id, policy_name)
    policy = policy_helper.add_policies(value=value)
    assert policy
    policy_id = list(policy.keys())[0]
    return policy_id
