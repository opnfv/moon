from python_moonclient.core.policies import *
from python_moonclient.core.models import *


def test_policies():
    check_policy()
    policy_id = add_policy()
    check_policy(policy_id)
    delete_policy(policy_id)


def test_subjects():
    policy_id = add_policy()
    subject_id = add_subject()

    update_subject(subject_id=subject_id, policy_id=policy_id)

    check_subject(subject_id=subject_id, policy_id=policy_id)

    delete_subject(subject_id, policy_id=policy_id)
    delete_subject(subject_id)

    
def test_objects():
    policy_id = add_policy()
    object_id = add_object()

    update_object(object_id=object_id, policy_id=policy_id)
    check_object(object_id=object_id, policy_id=policy_id)

    delete_object(object_id=object_id, policy_id=policy_id)
    delete_object(object_id=object_id)

    
def test_actions():
    policy_id = add_policy()
    action_id = add_action()

    update_action(action_id=action_id, policy_id=policy_id)
    check_action(action_id=action_id, policy_id=policy_id)

    delete_action(action_id=action_id, policy_id=policy_id)
    delete_action(action_id=action_id)


def test_subject_data():
    policy_id = add_policy()

    model_id = add_model()

    update_policy(policy_id, model_id)

    meta_rule_id, subject_cat_id, object_cat_id, action_cat_id = add_categories_and_meta_rule()
    add_meta_rule_to_model(model_id, meta_rule_id)

    subject_data_id = add_subject_data(policy_id=policy_id, category_id=subject_cat_id)
    check_subject_data(policy_id=policy_id, data_id=subject_data_id, category_id=subject_cat_id)
    delete_subject_data(policy_id=policy_id, data_id=subject_data_id, category_id=subject_cat_id)


def test_object_data():
    policy_id = add_policy()

    model_id = add_model()

    update_policy(policy_id, model_id)

    meta_rule_id, object_cat_id, object_cat_id, action_cat_id = add_categories_and_meta_rule()
    add_meta_rule_to_model(model_id, meta_rule_id)

    object_data_id = add_object_data(policy_id=policy_id, category_id=object_cat_id)
    check_object_data(policy_id=policy_id, data_id=object_data_id, category_id=object_cat_id)
    delete_object_data(policy_id=policy_id, data_id=object_data_id, category_id=object_cat_id)


def test_action_data():
    policy_id = add_policy()

    model_id = add_model()

    update_policy(policy_id, model_id)

    meta_rule_id, action_cat_id, action_cat_id, action_cat_id = add_categories_and_meta_rule()
    add_meta_rule_to_model(model_id, meta_rule_id)

    action_data_id = add_action_data(policy_id=policy_id, category_id=action_cat_id)
    check_action_data(policy_id=policy_id, data_id=action_data_id, category_id=action_cat_id)
    delete_action_data(policy_id=policy_id, data_id=action_data_id, category_id=action_cat_id)


def test_assignments():
    policy_id = add_policy()

    model_id = add_model()

    update_policy(policy_id, model_id)

    meta_rule_id, subject_cat_id, object_cat_id, action_cat_id = add_categories_and_meta_rule()
    add_meta_rule_to_model(model_id, meta_rule_id)

    subject_data_id = add_subject_data(policy_id=policy_id, category_id=subject_cat_id)
    subject_data_id_bis = add_subject_data(policy_id=policy_id, category_id=subject_cat_id)
    object_data_id = add_object_data(policy_id=policy_id, category_id=object_cat_id)
    object_data_id_bis = add_object_data(policy_id=policy_id, category_id=object_cat_id)
    action_data_id = add_action_data(policy_id=policy_id, category_id=action_cat_id)
    action_data_id_bis = add_action_data(policy_id=policy_id, category_id=action_cat_id)

    subject_id = add_subject(policy_id)
    object_id = add_object(policy_id)
    action_id = add_action(policy_id)

    add_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id)
    add_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id_bis)
    add_object_assignments(policy_id, object_id, object_cat_id, object_data_id)
    add_object_assignments(policy_id, object_id, object_cat_id, object_data_id_bis)
    add_action_assignments(policy_id, action_id, action_cat_id, action_data_id)
    add_action_assignments(policy_id, action_id, action_cat_id, action_data_id_bis)

    check_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id)
    check_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id_bis)
    check_object_assignments(policy_id, object_id, object_cat_id, object_data_id)
    check_object_assignments(policy_id, object_id, object_cat_id, object_data_id_bis)
    check_action_assignments(policy_id, action_id, action_cat_id, action_data_id)
    check_action_assignments(policy_id, action_id, action_cat_id, action_data_id_bis)

    delete_subject_assignment(policy_id, subject_id, subject_cat_id, subject_data_id)
    delete_object_assignment(policy_id, object_id, object_cat_id, object_data_id)
    delete_action_assignment(policy_id, action_id, action_cat_id, action_data_id)


def test_rule():
    policy_id = add_policy()

    model_id = add_model()

    update_policy(policy_id, model_id)

    meta_rule_id, subject_cat_id, object_cat_id, action_cat_id = add_categories_and_meta_rule()
    add_meta_rule_to_model(model_id, meta_rule_id)

    subject_data_id = add_subject_data(policy_id=policy_id, category_id=subject_cat_id)
    object_data_id = add_object_data(policy_id=policy_id, category_id=object_cat_id)
    action_data_id = add_action_data(policy_id=policy_id, category_id=action_cat_id)

    subject_id = add_subject(policy_id)
    object_id = add_object(policy_id)
    action_id = add_action(policy_id)

    add_subject_assignments(policy_id, subject_id, subject_cat_id, subject_data_id)
    add_object_assignments(policy_id, object_id, object_cat_id, object_data_id)
    add_action_assignments(policy_id, action_id, action_cat_id, action_data_id)

    rule_id = add_rule(policy_id, meta_rule_id, [subject_data_id, object_data_id, action_data_id])
    check_rule(policy_id, meta_rule_id, rule_id, [subject_data_id, object_data_id, action_data_id])

    delete_rule(policy_id, rule_id)

