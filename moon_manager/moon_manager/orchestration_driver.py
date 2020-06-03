# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
from moon_manager.api import configuration
from moon_manager.api.orchestration import slave, pipeline

logger = logging.getLogger("moon.manager.orchestration_driver")


SlaveManager = None
PipelineManager = None


class Driver:

    def __init__(self, driver_name, engine_name):
        self.name = driver_name
        self.plug = configuration.get_orchestration_driver()
        self.driver = self.plug.Connector(driver_name, engine_name)


class SlaveDriver(Driver):

    def __init__(self, driver_name, engine_name):
        super(SlaveDriver, self).__init__(driver_name, engine_name)
        self.engine = engine_name

    def update_slave(self, slave_id, data):
        raise NotImplementedError()  # pragma: no cover

    def delete_slave(self, slave_id):
        raise NotImplementedError()  # pragma: no cover

    def add_slave(self, slave_id=None, data=None):
        raise NotImplementedError()  # pragma: no cover

    def get_slaves(self, slave_id=None):
        raise NotImplementedError()  # pragma: no cover


class PipelineDriver(Driver):

    def __init__(self, driver_name, engine_name):
        super(PipelineDriver, self).__init__(driver_name, engine_name)
        self.engine = engine_name

    def update_pipeline(self, pipeline_id, data):
        raise NotImplementedError()  # pragma: no cover

    def delete_pipeline(self, pipeline_id):
        raise NotImplementedError()  # pragma: no cover

    def add_pipeline(self, pipeline_id=None, data=None):
        raise NotImplementedError()  # pragma: no cover

    def get_pipelines(self, slave_id=None, pipeline_id=None):
        raise NotImplementedError()  # pragma: no cover


def init():
    global SlaveManager, PipelineManager

    logger.info("Initializing driver")
    conf = configuration.get_configuration("orchestration")

    SlaveManager = slave.SlaveManager(
        SlaveDriver(conf['driver'], conf.get('url'))
    )
    PipelineManager = pipeline.PipelineManager(
        PipelineDriver(conf['driver'], conf.get('url'))
    )
