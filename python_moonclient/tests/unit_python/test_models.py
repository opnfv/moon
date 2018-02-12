from python_moonclient.core.models import *


def test_models():
    check_model()
    model_id = add_model()
    check_model(model_id)
    delete_model(model_id)


def test_meta_data_subject():
    category_id = add_subject_category()
    check_subject_category(category_id)
    # TODO (asteroide): must implement the deletion of linked data
    # delete_subject_category(category_id)


def test_meta_data_object():
    category_id = add_object_category()
    check_object_category(category_id)
    # TODO (asteroide): must implement the deletion of linked data
    # delete_object_category(category_id)


def test_meta_data_action():
    category_id = add_action_category()
    check_action_category(category_id)
    # TODO (asteroide): must implement the deletion of linked data
    # delete_action_category(category_id)


def test_meta_rule():
    meta_rule_id, scat_id, ocat_id, acat_id = add_categories_and_meta_rule()
    check_meta_rule(meta_rule_id, scat_id, ocat_id, acat_id)
    delete_meta_rule(meta_rule_id)


