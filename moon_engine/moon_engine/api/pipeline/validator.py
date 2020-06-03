# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from moon_cache.context import Context
from moon_utilities import exceptions
import itertools
import logging
import hug
from moon_cache.cache import Cache
from moon_engine.api.configuration import get_configuration

LOGGER = logging.getLogger("moon.authz.api." + __name__)


class Validator(object):
    __CACHE = None

    def __init__(self):

        self.__CACHE = Cache.getInstance(manager_url=get_configuration("manager_url"),
                                         incremental=get_configuration("incremental_updates"),
                                         manager_api_key=get_configuration("api_token"))
        self.context = None

    def authz(self, subject_name, object_name, action_name):

        ctx = {
            "pdp_id": get_configuration("uuid"),
            "subject_name": subject_name,
            "object_name": object_name,
            "action_name": action_name
        }
        self.context = Context(ctx, self.__CACHE)

        self.context.set_cache(self.__CACHE)
        self.context.increment_index()
        response = self.__authz_request()
        self.context.delete_cache()
        return response

    def __authz_request(self):

        LOGGER.debug("self.context.pdp_set={}".format(self.context.pdp_set))
        result, message = self.__check_rules()
        if result:
            if self.__exec_instructions(result):
                return hug.HTTP_204
        else:
            self.context.current_state = "deny"
        return hug.HTTP_403

    def __check_rules(self):

        scopes_list = list()
        current_header_id = self.context.headers[self.context.index]
        if not self.context.pdp_set:
            raise exceptions.PdpUnknown
        if current_header_id not in self.context.pdp_set:
            raise Exception('Invalid index')
        current_pdp = self.context.pdp_set[current_header_id]
        category_list = list()
        if 'meta_rules' not in current_pdp:
            raise exceptions.PdpContentError
        try:
            category_list.extend(current_pdp["meta_rules"]["subject_categories"])
            category_list.extend(current_pdp["meta_rules"]["object_categories"])
            category_list.extend(current_pdp["meta_rules"]["action_categories"])
        except Exception:
            raise exceptions.MetaRuleContentError
        if 'target' not in current_pdp:
            raise exceptions.PdpContentError
        for category in category_list:
            scope = list(current_pdp['target'][category])
            scopes_list.append(scope)
        if self.context.current_policy_id not in self.__CACHE.rules:
            raise exceptions.PolicyUnknown
        if 'rules' not in self.__CACHE.rules[self.context.current_policy_id]:
            raise exceptions.RuleUnknown

        for item in itertools.product(*scopes_list):
            req = list(item)
            for rule in self.__CACHE.rules[self.context.current_policy_id]["rules"]:
                if req == rule['rule']:
                    return rule['instructions'], ""
        if not list(itertools.product(*scopes_list)):
            LOGGER.error("There is an error in retrieved scopes ({})".format(scopes_list))
            cat_list = []
            categories = dict(self.__CACHE.subject_categories)
            categories.update(dict(self.__CACHE.object_categories))
            categories.update(dict(self.__CACHE.action_categories))
            for category in category_list:
                if category.startswith("attributes:"):
                    cat_list.append(category)
                else:
                    cat_list.append(categories[category].get('name'))
            LOGGER.error("Categories are ({})".format(", ".join(cat_list)))
            return False, "There is an error in retrieved scopes"
        LOGGER.warning("No rule match the request...")
        return False, "No rule match the request..."

    def __exec_instructions(self, instructions):

        for instruction in instructions:
            for key in instruction:
                if key == "decision":
                    if instruction["decision"] == "grant":
                        self.context.current_state = "grant"
                        LOGGER.info("__exec_instructions True {}".format(
                            self.context.current_state))
                        return True
                    else:
                        self.context.current_state = instruction["decision"].lower()

        LOGGER.info("__exec_instructions False {}".format(self.context.current_state))

        return False
