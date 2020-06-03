# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


"""Update API"""
import hug
from moon_utilities.auth_functions import api_key_authentication
from moon_engine.api.pipeline.update_pipeline import Update


class PipelineUpdate(object):

    @staticmethod
    @hug.local()
    @hug.put("/update/slave/{slave_id}", requires=api_key_authentication)
    def update_slave(body, slave_id: hug.types.uuid, response):
        """Tell the moon_engine wrapper that its cache should be updated
        body may contain the attributes that the moon_engine should get from the manager
        body example:
        {
            "name": "...",
            "description": "..."
        }
        :return: 202 status code
        """
        update_pipeline = Update()
        response.status = update_pipeline.update_slaves(slave_id=str(slave_id).replace("-", ""), is_delete=False,
                                                        data=body)

    @staticmethod
    @hug.local()
    @hug.put("/update/pdp/{pdp_id}", requires=api_key_authentication)
    def update_pdp(body, pdp_id: hug.types.uuid, response):
        """Tell the moon_engine wrapper that its cache should be updated
        body may contain the attributes that the moon_engine should get from the manager
        if the attributes key is empty, all data should be retrieved
        body example:
        {
            "vim_project_id": "...",
            "security_pipeline": ["policy_id1", "policy_id2"],
            "attributes": ["subjects", "subject_assignments", "subject_categories"]
        }
        :return: 202 status code
        """

        # todo call wrapper to update its pdp at the cache
        update_pipeline = Update()
        response.status = update_pipeline.update_pdp(is_delete=False, pdp_id=str(pdp_id).replace("-", ""), data=body)

    @staticmethod
    @hug.local()
    @hug.delete("/update/pdp/{pdp_id}", requires=api_key_authentication)
    def delete_pdp(pdp_id: hug.types.uuid, response):
        """Tell the moon_engine wrapper that its cache should be updated
        body may contain the attributes that the moon_engine should get from the manager
        if the attributes key is empty, all data should be retrieved
        body example:
        {
            "vim_project_id": "...",
            "security_pipeline": ["policy_id1", "policy_id2"],
            "attributes": ["subjects", "subject_assignments", "subject_categories"]
        }
        :return: 202 status code
        """

        # todo call wrapper to update its pdp at the cache
        update_pipeline = Update()
        response.status = update_pipeline.update_pdp(is_delete=True, pdp_id=str(pdp_id).replace("-", ""))

    @staticmethod
    @hug.local()
    @hug.put("/update/policy/{policy_id}", requires=api_key_authentication)
    def update_policy(body, policy_id: hug.types.uuid, response):
        update_pipeline = Update()
        response.status = update_pipeline.update_policy(is_delete=False, policy_id=str(policy_id).replace("-", ""),
                                                        data=body)

    @staticmethod
    @hug.local()
    @hug.delete("/update/policy/{policy_id}", requires=api_key_authentication)
    def delete_policy(policy_id: hug.types.uuid, response):
        update_pipeline = Update()
        response.status = update_pipeline.update_policy(is_delete=True, policy_id=str(policy_id).replace("-", ""))

    @staticmethod
    @hug.local()
    @hug.delete("/update/assignment/{policy_id}/{type}/", requires=api_key_authentication)
    @hug.delete("/update/assignment/{policy_id}/{type}/{perimeter_id}",
                requires=api_key_authentication)
    @hug.delete("/update/assignment/{policy_id}/{type}/{perimeter_id}/{category_id}",
                requires=api_key_authentication)
    @hug.delete("/update/assignment/{policy_id}/{type}/{perimeter_id}/{category_id}/{data_id}",
                requires=api_key_authentication)
    def delete_assignment(response, policy_id: hug.types.uuid, type: hug.types.text,
                          perimeter_id: hug.types.uuid = None, category_id: hug.types.uuid = None,
                          data_id: hug.types.uuid = None, authed_user: hug.directives.user=None):
        update_pipeline = Update()
        response.status = update_pipeline.delete_assignment(type=type, policy_id=str(policy_id).replace("-", ""),
                                                            perimeter_id=str(perimeter_id).replace("-", ""),
                                                            category_id=str(category_id).replace("-", ""),
                                                            data_id=data_id)

    @staticmethod
    @hug.local()
    @hug.put("/update/perimeter/{perimeter_id}/{policy_id}/{type}", requires=api_key_authentication)
    def update_perimeter(body, perimeter_id: hug.types.uuid, policy_id: hug.types.uuid,
                         type: hug.types.text, response):
        update_pipeline = Update()
        response.status = update_pipeline.update_perimeter(is_delete=False, type=type,
                                                           perimeter_id=str(perimeter_id).replace("-", ""), data=body,
                                                           policy_id=str(policy_id).replace("-", ""))

    @staticmethod
    @hug.local()
    @hug.delete("/update/perimeter/{perimeter_id}/{policy_id}/{type}", requires=api_key_authentication)
    def delete_perimeter(perimeter_id: hug.types.uuid, policy_id: hug.types.uuid,
                         type: hug.types.text, response):
        update_pipeline = Update()
        response.status = update_pipeline.update_perimeter(is_delete=True, type=type,
                                                           perimeter_id=str(perimeter_id).replace("-", ""),
                                                           policy_id=str(policy_id).replace("-", ""))

    @staticmethod
    @hug.local()
    @hug.delete("/update/rule/{policy_id}/{rule_id}", requires=api_key_authentication)
    def delete_rule(policy_id: hug.types.uuid, rule_id: hug.types.uuid, response):
        update_pipeline = Update()
        response.status = update_pipeline.delete_rule(rule_id=str(rule_id).replace("-", ""), policy_id=str(policy_id).replace("-", ""))

    @staticmethod
    @hug.local()
    @hug.put("/update/model/{model_id}", requires=api_key_authentication)
    def update_model(body, model_id: hug.types.uuid, response):
        update_pipeline = Update()
        response.status = update_pipeline.update_model(model_id=str(model_id).replace("-", ""), is_delete=False,
                                                       data=body)

    @staticmethod
    @hug.local()
    @hug.delete("/update/model/{model_id}", requires=api_key_authentication)
    def delete_model(model_id: hug.types.uuid, response):
        update_pipeline = Update()
        response.status = update_pipeline.update_model(model_id=str(model_id).replace("-", ""), is_delete=True)

    @staticmethod
    @hug.local()
    @hug.delete("/update/meta_data/{category_id}/{type}", requires=api_key_authentication)
    def delete_category(category_id: hug.types.uuid, type: hug.types.text, response):
        update_pipeline = Update()
        response.status = update_pipeline.delete_category(category_id=str(category_id).replace("-", ""), type=type)

    @staticmethod
    @hug.local()
    @hug.put("/update/meta_rule/{meta_rule_id}", requires=api_key_authentication)
    def update_meta_rule(body, meta_rule_id: hug.types.uuid, response):
        update_pipeline = Update()
        response.status = update_pipeline.update_meta_rule(is_delete=False,
                                                           meta_rule_id=str(meta_rule_id).replace("-", ""), data=body)

    @staticmethod
    @hug.local()
    @hug.delete("/update/meta_rule/{meta_rule_id}", requires=api_key_authentication)
    def delete_meta_rule(meta_rule_id: hug.types.uuid, response):
        update_pipeline = Update()
        response.status = update_pipeline.update_meta_rule(is_delete=True,
                                                           meta_rule_id=str(meta_rule_id).replace("-", ""))

    @staticmethod
    @hug.local()
    @hug.delete("/update/data/{data_id}/{type}", requires=api_key_authentication)
    def delete_data(data_id: hug.types.uuid, type: hug.types.text, response):
        update_pipeline = Update()
        response.status = update_pipeline.delete_data(data_id=str(data_id).replace("-", ""), type=type)

    @staticmethod
    @hug.local()
    @hug.delete("/update/attributes/{name}", requires=api_key_authentication)
    def delete_data(name: hug.types.text, response):
        update_pipeline = Update()
        response.status = update_pipeline.delete_attributes(name=name)
