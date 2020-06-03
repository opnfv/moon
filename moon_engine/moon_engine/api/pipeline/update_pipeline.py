# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import hug
from moon_cache.cache import Cache
from moon_engine.api.configuration import get_configuration
import logging

logger = logging.getLogger("moon.engine.api.pipeline.update_pipeline")


class Update(object):
    __CACHE = None

    def __init__(self):
        if not self.__CACHE:
            self.__CACHE = Cache.getInstance(manager_url=get_configuration("manager_url"),
                                 incremental=get_configuration("incremental_updates"),
                                 manager_api_key=get_configuration("api_token"))

    def update_policy(self, is_delete, policy_id, data=None):

        policies = self.__CACHE.policies
        if is_delete:
            if policy_id in policies:
                del policies[policy_id]
        else:
            if policy_id in policies:
                policies[policy_id] = data
            else:
                return hug.HTTP_208
        return hug.HTTP_202

    def update_pdp(self, is_delete, pdp_id, data=None):

        pdps = self.__CACHE.pdp
        if is_delete:
            if pdp_id in pdps:
                del pdps[pdp_id]
        else:
            if pdp_id in pdps:
                pdps[pdp_id] = data
            else:
                return hug.HTTP_208
        return hug.HTTP_202

    def delete_assignment(self, type, policy_id, perimeter_id=None, category_id=None, data_id=None):

        if type == "subject":
            assignments = self.__CACHE.subject_assignments
            if policy_id in assignments:
                for key in assignments[policy_id]:
                    if (perimeter_id is None or assignments[policy_id][key]['subject_id'] ==
                        perimeter_id) and (
                            category_id is None or assignments[policy_id][key]['category_id'] == category_id):
                        if data_id is None or data_id in assignments[policy_id][key]['assignments']:
                            assignments[policy_id][key]['assignments'].remove(data_id)
                            if len(assignments[policy_id][key]['assignments']) == 0:
                                del assignments[policy_id][key];
                        else:
                            del assignments[policy_id][key]
                        break

        elif type == "object":
            assignments = self.__CACHE.object_assignments
            if policy_id in assignments:
                for key in assignments[policy_id]:
                    if (perimeter_id is None or assignments[policy_id][key]['object_id'] ==
                        perimeter_id) and (
                            category_id is None or assignments[policy_id][key]['category_id'] == category_id):
                        if data_id is None or data_id in assignments[policy_id][key]['assignments']:
                            assignments[policy_id][key]['assignments'].remove(data_id)
                            if len(assignments[policy_id][key]['assignments']) == 0:
                                del assignments[policy_id][key];
                        else:
                            del assignments[policy_id][key]
                        break
        else:
            assignments = self.__CACHE.action_assignments
            if policy_id in assignments:
                for key in assignments[policy_id]:
                    if (perimeter_id is None or assignments[policy_id][key]['action_id'] ==
                        perimeter_id) and (
                            category_id is None or assignments[policy_id][key]['category_id'] == category_id):
                        if data_id is None or data_id in assignments[policy_id][key]['assignments']:
                            assignments[policy_id][key]['assignments'].remove(data_id)
                            if len(assignments[policy_id][key]['assignments']) == 0:
                                del assignments[policy_id][key];
                        else:
                            del assignments[policy_id][key]
                        break
        return hug.HTTP_202

    def update_perimeter(self, is_delete, type, perimeter_id, data=None, policy_id=None):

        if is_delete:
            if type == "subject":
                perimeters = self.__CACHE.subjects
                if policy_id in perimeters and perimeter_id in perimeters[policy_id] and \
                        policy_id in perimeters[policy_id][perimeter_id]['policy_list']:
                    del perimeters[policy_id][perimeter_id]
            elif type == "object":
                perimeters = self.__CACHE.objects
                if policy_id in perimeters and perimeter_id in perimeters[policy_id] and \
                        policy_id in perimeters[policy_id][perimeter_id]['policy_list']:
                    del perimeters[policy_id][perimeter_id]
            else:
                perimeters = self.__CACHE.actions
                if policy_id in perimeters and perimeter_id in perimeters[policy_id] and \
                        policy_id in perimeters[policy_id][perimeter_id]['policy_list']:
                    del perimeters[policy_id][perimeter_id]
        else:
            if type == "subject":
                perimeters = self.__CACHE.subjects
                if policy_id in perimeters and perimeter_id in perimeters[policy_id] and \
                        policy_id in perimeters[policy_id][perimeter_id]['policy_list']:
                    perimeters[policy_id][perimeter_id]['name'] = data['name']
                    perimeters[policy_id][perimeter_id]['description'] = data['description']
                else:
                    return hug.HTTP_208
            elif type == "object":
                perimeters = self.__CACHE.objects
                if policy_id in perimeters and perimeter_id in perimeters[policy_id] and \
                        policy_id in perimeters[policy_id][perimeter_id]['policy_list']:
                    perimeters[policy_id][perimeter_id]['name'] = data['name']
                    perimeters[policy_id][perimeter_id]['description'] = data['description']
                else:
                    return hug.HTTP_208
            else:
                perimeters = self.__CACHE.actions
                if policy_id in perimeters and perimeter_id in perimeters[policy_id] and \
                        policy_id in perimeters[policy_id][perimeter_id]['policy_list']:
                    perimeters[policy_id][perimeter_id]['name'] = data['name']
                    perimeters[policy_id][perimeter_id]['description'] = data['description']
                else:
                    return hug.HTTP_208
        return hug.HTTP_202

    def delete_rule(self, rule_id, policy_id):

        rules = self.__CACHE.rules
        if policy_id in rules and rule_id in rules[policy_id]:
            del rules[policy_id][rule_id]
        return hug.HTTP_202

    def update_model(self, model_id, is_delete, data=None):
        if is_delete:
            models = self.__CACHE.models
            if model_id in models:
                del models[model_id]
        else:
            models = self.__CACHE.models
            if model_id in models:
                models[model_id] = data
            else:
                return hug.HTTP_208
        return hug.HTTP_202

    def delete_category(self, category_id, type):

        if type == "subject":
            categories = self.__CACHE.subject_categories
            if category_id in categories:
                del categories[category_id]
        elif type == 'object':
            categories = self.__CACHE.object_categories
            if category_id in categories:
                del categories[category_id]
        else:
            categories = self.__CACHE.action_categories
            if category_id in categories:
                del categories[category_id]
        return hug.HTTP_202

    def update_meta_rule(self, is_delete, meta_rule_id, data=None):

        if is_delete:
            meta_rules = self.__CACHE.meta_rules
            if meta_rule_id in meta_rules:
                del meta_rules[meta_rule_id]
        else:
            meta_rules = self.__CACHE.meta_rules
            if meta_rule_id in meta_rules:
                meta_rules[meta_rule_id] = data
            else:
                return hug.HTTP_208
        return hug.HTTP_202

    def delete_data(self, data_id, type):

        if type == 'subject':
            data = self.__CACHE.subject_data
            if data_id in data:
                del data[data_id]
        elif type == 'object':
            data = self.__CACHE.object_data
            if data_id in data:
                del data[data_id]
        else:
            data = self.__CACHE.action_data
            if data_id in data:
                del data[data_id]

        return hug.HTTP_202

    def delete_attributes(self, name):

        attributes = self.__CACHE.attributes
        self.__CACHE.set_attribute(name)

        return hug.HTTP_202
