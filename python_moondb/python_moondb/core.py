# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
from stevedore.driver import DriverManager
from python_moonutilities import configuration
from python_moondb.api import model, policy, pdp, keystone

logger = logging.getLogger("moon.db")


class Driver(DriverManager):

    def __init__(self, driver_name, engine_name):
        logger.info("initialization of Driver {}".format(driver_name))
        super(Driver, self).__init__(
            namespace='moon_db.driver',
            name=driver_name,
            invoke_on_load=True,
            invoke_args=(engine_name,),
        )


class ModelDriver(Driver):

    def __init__(self, driver_name, engine_name):
        super(ModelDriver, self).__init__(driver_name, engine_name)

    def update_model(self, model_id, value):
        raise NotImplementedError()  # pragma: no cover

    def delete_model(self, model_id):
        raise NotImplementedError()  # pragma: no cover

    def add_model(self, model_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def get_models(self, model_id=None):
        raise NotImplementedError()  # pragma: no cover

    def set_meta_rule(self, meta_rule_id, value):
        raise NotImplementedError()  # pragma: no cover

    def get_meta_rules(self, meta_rule_id=None):
        raise NotImplementedError()  # pragma: no cover

    def delete_meta_rule(self, meta_rule_id=None):
        raise NotImplementedError()  # pragma: no cover

    def get_subject_categories(self, category_id=None):
        raise NotImplementedError()  # pragma: no cover

    def add_subject_category(self, name, description):
        raise NotImplementedError()  # pragma: no cover

    def delete_subject_category(self, category_id):
        raise NotImplementedError()  # pragma: no cover

    def get_object_categories(self, category_id):
        raise NotImplementedError()  # pragma: no cover

    def add_object_category(self, category_id, value):
        raise NotImplementedError()  # pragma: no cover

    def delete_object_category(self, category_id):
        raise NotImplementedError()  # pragma: no cover

    def get_action_categories(self, category_id):
        raise NotImplementedError()  # pragma: no cover

    def add_action_category(self, category_id, value):
        raise NotImplementedError()  # pragma: no cover

    def delete_action_category(self, category_id):
        raise NotImplementedError()  # pragma: no cover


class PolicyDriver(Driver):

    def __init__(self, driver_name, engine_name):
        super(PolicyDriver, self).__init__(driver_name, engine_name)

    def update_policy(self, policy_id, value):
        raise NotImplementedError()  # pragma: no cover

    def delete_policy(self, policy_id):
        raise NotImplementedError()  # pragma: no cover

    def add_policy(self, policy_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def get_policies(self, policy_id=None):
        raise NotImplementedError()  # pragma: no cover

    def get_subjects(self, policy_id, perimeter_id=None):
        raise NotImplementedError()  # pragma: no cover

    def set_subject(self, policy_id, perimeter_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def delete_subject(self, policy_id, perimeter_id):
        raise NotImplementedError()  # pragma: no cover

    def get_objects(self, policy_id, perimeter_id=None):
        raise NotImplementedError()  # pragma: no cover

    def set_object(self, policy_id, perimeter_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def delete_object(self, policy_id, perimeter_id):
        raise NotImplementedError()  # pragma: no cover

    def get_actions(self, policy_id, perimeter_id=None):
        raise NotImplementedError()  # pragma: no cover

    def set_action(self, policy_id, perimeter_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def delete_action(self, policy_id, perimeter_id):
        raise NotImplementedError()  # pragma: no cover

    def get_subject_data(self, policy_id, data_id=None, category_id=None):
        raise NotImplementedError()  # pragma: no cover

    def set_subject_data(self, policy_id, data_id=None, category_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def delete_subject_data(self, policy_id, data_id):
        raise NotImplementedError()  # pragma: no cover

    def get_object_data(self, policy_id, data_id=None, category_id=None):
        raise NotImplementedError()  # pragma: no cover

    def set_object_data(self, policy_id, data_id=None, category_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def delete_object_data(self, policy_id, data_id):
        raise NotImplementedError()  # pragma: no cover

    def get_action_data(self, policy_id, data_id=None, category_id=None):
        raise NotImplementedError()  # pragma: no cover

    def set_action_data(self, policy_id, data_id=None, category_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def delete_action_data(self, policy_id, data_id):
        raise NotImplementedError()  # pragma: no cover

    def get_subject_assignments(self, policy_id, subject_id=None, category_id=None):
        raise NotImplementedError()  # pragma: no cover

    def add_subject_assignment(self, policy_id, subject_id, category_id, data_id):
        raise NotImplementedError()  # pragma: no cover

    def delete_subject_assignment(self, policy_id, subject_id, category_id, data_id):
        raise NotImplementedError()  # pragma: no cover

    def get_object_assignments(self, policy_id, assignment_id=None):
        raise NotImplementedError()  # pragma: no cover

    def add_object_assignment(self, policy_id, subject_id, category_id, data_id):
        raise NotImplementedError()  # pragma: no cover

    def delete_object_assignment(self, policy_id, object_id, category_id, data_id):
        raise NotImplementedError()  # pragma: no cover

    def get_action_assignments(self, policy_id, assignment_id=None):
        raise NotImplementedError()  # pragma: no cover

    def add_action_assignment(self, policy_id, action_id, category_id, data_id):
        raise NotImplementedError()  # pragma: no cover

    def delete_action_assignment(self, policy_id, action_id, category_id, data_id):
        raise NotImplementedError()  # pragma: no cover

    def get_rules(self, policy_id, rule_id=None, meta_rule_id=None):
        raise NotImplementedError()  # pragma: no cover

    def add_rule(self, policy_id, meta_rule_id, value):
        raise NotImplementedError()  # pragma: no cover

    def delete_rule(self, policy_id, rule_id):
        raise NotImplementedError()  # pragma: no cover


class PDPDriver(Driver):

    def __init__(self, driver_name, engine_name):
        super(PDPDriver, self).__init__(driver_name, engine_name)

    def update_pdp(self, pdp_id, value):
        raise NotImplementedError()  # pragma: no cover

    def delete_pdp(self, pdp_id):
        raise NotImplementedError()  # pragma: no cover

    def add_pdp(self, pdp_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def get_pdp(self, pdp_id=None):
        raise NotImplementedError()  # pragma: no cover


class KeystoneDriver(Driver):

    def __init__(self, driver_name, engine_name):
        super(KeystoneDriver, self).__init__(driver_name, engine_name)


conf = configuration.get_configuration("database")['database']

KeystoneManager = keystone.KeystoneManager(
    KeystoneDriver(conf['driver'], conf['url'])
)

ModelManager = model.ModelManager(
    ModelDriver(conf['driver'], conf['url'])
)

PolicyManager = policy.PolicyManager(
    PolicyDriver(conf['driver'], conf['url'])
)

PDPManager = pdp.PDPManager(
    PDPDriver(conf['driver'], conf['url'])
)
