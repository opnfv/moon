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
from moon_engine.api.wrapper.update_wrapper import UpdateWrapper as UpdateWrapper


class WrapperUpdate(object):

    @staticmethod
    @hug.local()
    @hug.put("/update", requires=api_key_authentication)
    def update(body, response, authed_user: hug.directives.user):
        """Tell the moon_engine wrapper that its own data should be updated
        It simply reloads the conf file

        :return: 204 status code
        """

        # todo call wrapper to update its pdp at the cache
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.update_wrapper(data=body, moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.put("/update/pdp/{pdp_id}", requires=api_key_authentication)
    def update_pdp(body, pdp_id: hug.types.uuid, response, authed_user: hug.directives.user):
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
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.update_pdp(pdp_id=str(pdp_id).replace("-", ""), data=body, moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/pdp/{pdp_id}", requires=api_key_authentication)
    def delete_pdp(pdp_id: hug.types.uuid, response, authed_user: hug.directives.user):
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
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_pdp(pdp_id=str(pdp_id).replace("-", ""), moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.put("/update/policy/{policy_id}", requires=api_key_authentication)
    def update_policy(body, policy_id: hug.types.uuid, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.update_policy(policy_id=str(policy_id).replace("-", ""), data=body, moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/policy/{policy_id}", requires=api_key_authentication)
    def delete_policy(policy_id: hug.types.uuid, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_policy(policy_id=str(policy_id).replace("-", ""), moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/assignment/{policy_id}/{type}/", requires=api_key_authentication)
    @hug.delete("/update/assignment/{policy_id}/{type}/{perimeter_id}", requires=api_key_authentication)
    @hug.delete("/update/assignment/{policy_id}/{type}/{perimeter_id}/{category_id}", requires=api_key_authentication)
    @hug.delete("/update/assignment/{policy_id}/{type}/{perimeter_id}/{category_id}/{data_id}", requires=api_key_authentication)
    def delete_assignment(response, policy_id: hug.types.uuid, type: hug.types.text,
                          perimeter_id: hug.types.uuid = None, category_id: hug.types.uuid = None,
                          data_id: hug.types.uuid = None, authed_user: hug.directives.user=None):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_assignment(type=type, policy_id=str(policy_id).replace("-", ""),
                                                           perimeter_id=str(perimeter_id).replace("-", ""),
                                                           category_id=str(category_id).replace("-", ""),
                                                           data_id=data_id, moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.put("/update/perimeter/{perimeter_id}/{policy_id}/{type}", requires=api_key_authentication)
    def update_perimeter(body, perimeter_id: hug.types.uuid, policy_id: hug.types.uuid,
                         type: hug.types.text, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.update_perimeter( type=type,
                                                          perimeter_id=str(perimeter_id).replace("-", ""), data=body,
                                                          policy_id=str(policy_id).replace("-", ""), moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/perimeter/{perimeter_id}/{policy_id}/{type}", requires=api_key_authentication)
    def delete_perimeter(perimeter_id: hug.types.uuid, policy_id: hug.types.uuid,
                         type: hug.types.text, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_perimeter(type=type,
                                                          perimeter_id=str(perimeter_id).replace("-", ""),
                                                          policy_id=str(policy_id).replace("-", ""), moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/rule/{policy_id}/{rule_id}", requires=api_key_authentication)
    def delete_rule(policy_id: hug.types.uuid, rule_id: hug.types.uuid, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_rule(rule_id=str(rule_id).replace("-", ""), policy_id=str(policy_id).replace("-", ""), moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.put("/update/model/{model_id}", requires=api_key_authentication)
    def update_model(body, model_id: hug.types.uuid, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.update_model(model_id=str(model_id).replace("-", ""), data=body, moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/model/{model_id}", requires=api_key_authentication)
    def delete_model(model_id: hug.types.uuid, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_model(model_id=str(model_id).replace("-", ""), moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/meta_data/{category_id}/{type}", requires=api_key_authentication)
    def delete_category(category_id: hug.types.uuid, type: hug.types.text, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_category(category_id=str(category_id).replace("-", ""), type=type, moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.put("/update/meta_rule/{meta_rule_id}", requires=api_key_authentication)
    def update_meta_rule(body, meta_rule_id: hug.types.uuid, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.update_meta_rule(meta_rule_id=str(meta_rule_id).replace("-", ""), data=body, moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/meta_rule/{meta_rule_id}", requires=api_key_authentication)
    def delete_meta_rule(meta_rule_id: hug.types.uuid, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_meta_rule(meta_rule_id=str(meta_rule_id).replace("-", ""), moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/data/{data_id}/{type}", requires=api_key_authentication)
    def delete_data(data_id: hug.types.uuid, type: hug.types.text, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_data(data_id=str(data_id).replace("-", ""), type=type, moon_user_id=authed_user)

    @staticmethod
    @hug.local()
    @hug.delete("/update/attributes/{name}", requires=api_key_authentication)
    def delete_data(name: str, response, authed_user: hug.directives.user):
        update_wrapper = UpdateWrapper()
        response.status = update_wrapper.delete_attributes(name=name, moon_user_id=authed_user)

