# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
from moon_manager.api import configuration
from moon_manager.api.db import model, policy, pdp, slave

logger = logging.getLogger("moon.manager.db_driver")


ModelManager = None
PolicyManager = None
PDPManager = None
SlaveManager = None


class Driver:

    def __init__(self, driver_name, engine_name):
        self.driver = configuration.get_db_driver()
        self.driver = self.driver.Connector(engine_name)


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

    def update_rule(self, rule_id, value):
        raise NotImplementedError()  # pragma: no cover

    def delete_rule(self, policy_id, rule_id):
        raise NotImplementedError()  # pragma: no cover


class PDPDriver(Driver):

    def __init__(self, driver_name, engine_name):
        super(PDPDriver, self).__init__(driver_name, engine_name)

    def update_pdp(self, pdp_id, value):
        raise NotImplementedError()  # pragma: no cover

    def delete_policy_from_pdp(self, pdp_id, policy_id):
        raise NotImplementedError()  # pragma: no cover

    def delete_pdp(self, pdp_id):
        raise NotImplementedError()  # pragma: no cover

    def add_pdp(self, pdp_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def get_pdp(self, pdp_id=None):
        raise NotImplementedError()  # pragma: no cover


class SlaveDriver(Driver):

    def __init__(self, driver_name, engine_name):
        super(SlaveDriver, self).__init__(driver_name, engine_name)

    def update_slave(self, slave_id, value):
        raise NotImplementedError()  # pragma: no cover

    def delete_slave(self, slave_id):
        raise NotImplementedError()  # pragma: no cover

    def add_slave(self, slave_id=None, value=None):
        raise NotImplementedError()  # pragma: no cover

    def get_slaves(self, slave_id=None):
        raise NotImplementedError()  # pragma: no cover


def init():
    global ModelManager, PolicyManager, PDPManager, SlaveManager

    conf = configuration.get_configuration("database")

    ModelManager = model.ModelManager(
        ModelDriver(conf['driver'], conf['url'])
    )

    PolicyManager = policy.PolicyManager(
        PolicyDriver(conf['driver'], conf['url'])
    )

    PDPManager = pdp.PDPManager(
        PDPDriver(conf['driver'], conf['url'])
    )

    SlaveManager = slave.SlaveManager(
        SlaveDriver(conf['driver'], conf['url'])
    )
