# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import logging
from moon_engine.api import configuration
from moon_engine.api.orchestration import pipeline

logger = logging.getLogger("moon.engine.orchestration_driver")


PipelineManager = None


class Driver:

    def __init__(self, driver_name, engine_name):
        self.name = driver_name
        self.plug = configuration.get_orchestration_driver()
        self.driver = self.plug.Connector(driver_name, engine_name)


class PipelineDriver(Driver):

    def __init__(self, driver_name, engine_name):
        super(PipelineDriver, self).__init__(driver_name, engine_name)
        self.engine = engine_name

    def update_pipeline(self, pipeline_id, data):
        """Update a pipeline

        :param pipeline_id: the ID of the pipeline
        :param data: a dictionary {
            "name": "the name of the pipeline",
            "description": "the description of the pipeline",
            "wrapper": {"url": "http://127.0.0.1:20000"},
            # "wrapper": {"url": "local"}  # if the pipeline should be configured inside the wrapper
            "plugins": ["moon_engine.plugins.authz", ]  # the first plugin is the default
        }
        :return: the pipeline updated
        """
        raise NotImplementedError()  # pragma: no cover

    def delete_pipeline(self, pipeline_id):
        """Delete the pipeline

        :param pipeline_id: the ID of the pipeline
        :return: True if the pipeline has been deleted
        """
        raise NotImplementedError()  # pragma: no cover

    def add_pipeline(self, pipeline_id=None, data=None):
        """Create a new pipeline

        :param pipeline_id: (optional) the ID of the pipeline to create
        :param data: a dictionary {
            "name": "the name of the pipeline",
            "description": "the description of the pipeline",
            "wrapper": {"url": "http://127.0.0.1:20000"},
            # "wrapper": {"url": "local"}  # if the pipeline should be configured inside the wrapper
            "plugins": ["moon_engine.plugins.authz", ]  # the first plugin is the default
        }
        :return: the pipeline created
        """
        raise NotImplementedError()  # pragma: no cover

    def get_pipelines(self, pipeline_id=None):
        """List one or more pipelines

        :param pipeline_id: (optional) the ID of the pipeline to list
        :return: a list of one or more pipelines
        """
        raise NotImplementedError()  # pragma: no cover

    def get_pipeline_api_key(self, pipeline_id):
        """Returns the api key of the pipeline with id pipeline_id

        :param pipeline_id: the ID of the pipeline to list
        :return: The api key of the pipeline
        """
        raise NotImplementedError()  # pragma: no cover


def init():
    global PipelineManager

    logger.info("Initializing driver")
    conf = configuration.get_configuration("orchestration")

    PipelineManager = pipeline.PipelineManager(
        PipelineDriver(conf['driver'], conf.get('url'))
    )
