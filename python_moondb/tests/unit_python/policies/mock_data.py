def create_meta_rule():
    meta_rule_value = {
        "name": "meta_rule1",
        "algorithm": "name of the meta rule algorithm",
        "subject_categories": ["subject_category_id1",
                               "subject_category_id2"],
        "object_categories": ["object_category_id1"],
        "action_categories": ["action_category_id1"]
    }
    return meta_rule_value


def create_model(meta_rule_id):
    value = {
        "name": "test_model",
        "description": "test",
        "meta_rules": [meta_rule_id]

    }
    return value


def create_policy(model_id):
    value = {
        "name": "policy_1",
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


def get_policy_id():
    import policies.test_policies as test_policies
    import models.test_models as test_models
    import models.test_meta_rules as test_meta_rules
    meta_rule = test_meta_rules.add_meta_rule(value=create_meta_rule())
    meta_rule_id = list(meta_rule.keys())[0]
    model = test_models.add_model(value=create_model(meta_rule_id))
    model_id = list(model.keys())[0]
    value = create_policy(model_id)
    policy = test_policies.add_policies(value=value)
    assert policy
    policy_id = list(policy.keys())[0]
    return policy_id
