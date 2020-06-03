# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""Pipeline API"""
import hug
from moon_utilities.auth_functions import api_key_authentication
from moon_engine import orchestration_driver
from moon_utilities.security_functions import validate_input
from moon_engine.api import configuration
from moon_cache.cache import Cache

CACHE = Cache.getInstance(manager_url=configuration.get_configuration("manager_url"),
                          incremental=configuration.get_configuration("incremental_updates"),
                          manager_api_key=configuration.get_configuration("api_token"))


class Pipeline(object):
    """
    Endpoint for pipelines requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/pipelines", requires=api_key_authentication)
    @hug.get("/pipeline/{uuid}", requires=api_key_authentication)
    def get(uuid: hug.types.uuid=None, authed_user: hug.directives.user=None):
        """Retrieve all pipelines

        :param uuid: uuid of the pipeline
        :param authed_user: the name of the authenticated user
        :return: {
            "pipeline_id1": {
                "name": "...",
                "description": "... (optional)",
            }
        }
        """
        uuid = str(uuid).replace("-", "")
        orchestration_driver.init()
        data = orchestration_driver.PipelineManager.get_pipelines(moon_user_id=authed_user,
                                                                  pipeline_id=uuid)
        return {"pipelines": data}

    @staticmethod
    @hug.local()
    @hug.put("/pipeline/{uuid}", requires=api_key_authentication)
    def put(uuid: hug.types.uuid, body: validate_input("name"),
            authed_user: hug.directives.user = None):
        """
        Ask for the creation of a new pipeline
        :param uuid: uuid of the pipeline
        :param body: body of the request
        :param authed_user: the name of the authenticated user
        :return: {
            "name": "my_pdp",
            "description": "...",
            "vim_project_id": "an existing ID",
            "security_pipelines": ["an existing policy ID", ],
            "slave": ["name of a slave", ]
        }
        """
        uuid = str(uuid).replace("-", "")
        orchestration_driver.init()
        data = orchestration_driver.PipelineManager.add_pipeline(moon_user_id=authed_user,
                                                                 pipeline_id=uuid,
                                                                 data=body)
        CACHE.add_pipeline(uuid, data)
        return {"pipelines": data}

    @staticmethod
    @hug.local()
    @hug.delete("/pipeline/{uuid}", requires=api_key_authentication)
    def delete(uuid: hug.types.uuid, authed_user: hug.directives.user = None):
        """
        Ask for the deletion of a new pipeline
        :param uuid: uuid of the pipeline
        :param authed_user: the name of the authenticated user
        :return: {
            "name": "my_pdp",
            "description": "...",
            "vim_project_id": "an existing ID",
            "security_pipelines": ["an existing policy ID", ],
            "slave": ["name of a slave", ]
        }
        """
        uuid = str(uuid).replace("-", "")
        orchestration_driver.init()
        orchestration_driver.PipelineManager.delete_pipeline(moon_user_id=authed_user,
                                                             pipeline_id=uuid)
        CACHE.delete_pipeline(uuid)
        return True
