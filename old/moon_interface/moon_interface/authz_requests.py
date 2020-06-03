# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
import itertools
import pickle
import requests
import sys
from python_moonutilities import exceptions
from python_moonutilities.context import Context
from python_moonutilities.cache import Cache

logger = logging.getLogger("moon.interface.authz_requests")


CACHE = Cache()
CACHE.update()


class AuthzRequest:

    result = None
    final_result = "Deny"
    req_max_delay = 2

    def __init__(self, ctx, args=None):
        self.context = Context(ctx, CACHE)
        self.args = args
        self.request_id = ctx["request_id"]
        if ctx['project_id'] not in CACHE.container_chaining:
            raise exceptions.KeystoneProjectError("Unknown Project ID {}".format(ctx['project_id']))
        self.container_chaining = CACHE.container_chaining[ctx['project_id']]

        if len(self.container_chaining) == 0 or not all(k in self.container_chaining[0] for k in ("container_id", "hostname", "hostip", "port")):
            raise exceptions.MoonError('Void container chaining')

        self.pdp_container = self.container_chaining[0]["container_id"]
        self.run()

    def run(self):
        self.context.delete_cache()
        req = None
        tries = 0
        success = False

        if "hostip" in self.container_chaining[0]:
            hostname = self.container_chaining[0]["hostip"]
        elif "hostname" in self.container_chaining[0]:
            hostname = self.container_chaining[0]["hostname"]
        else:
            raise exceptions.AuthzException(
                "error in address no hostname or hostip"
            )
        tried_hostnames = []
        while tries < 2:
            tried_hostnames.append(hostname)
            try:
                req = requests.post("http://{}:{}/authz".format(
                    hostname,
                    self.container_chaining[0]["port"],
                ), data=pickle.dumps(self.context))
                if req.status_code != 200:
                    raise exceptions.AuthzException(
                        "Receive bad response from Authz function "
                        "(with {} -> {})".format(hostname, req.status_code)
                    )
                success = True
            except requests.exceptions.ConnectionError:
                if tries > 1:
                    logger.error("Cannot connect to {}".format(
                        "http://[{}]:{}/authz".format(
                            ", ".join(tried_hostnames),
                            self.container_chaining[0]["port"]
                        )))
            except Exception as e:
                logger.exception(e)
            else:
                break
            hostname = self.container_chaining[0]["hostname"],
            tries += 1

        if not success:
            raise exceptions.AuthzException("Cannot connect to Authz function")

        self.context.set_cache(CACHE)
        if req and len(self.container_chaining) == 1:
            self.result = pickle.loads(req.content)

    # def __exec_next_state(self, rule_found):
    #     index = self.context.index
    #     current_meta_rule = self.context.headers[index]
    #     current_container = self.__get_container_from_meta_rule(current_meta_rule)
    #     current_container_genre = current_container["genre"]
    #     try:
    #         next_meta_rule = self.context.headers[index + 1]
    #     except IndexError:
    #         next_meta_rule = None
    #     if current_container_genre == "authz":
    #         if rule_found:
    #             return True
    #         pass
    #         if next_meta_rule:
    #             # next will be session if current is deny and session is unset
    #             if self.payload["authz_context"]['pdp_set'][next_meta_rule]['effect'] == "unset":
    #                 return notify(
    #                     request_id=self.payload["authz_context"]["request_id"],
    #                     container_id=self.__get_container_from_meta_rule(next_meta_rule)['container_id'],
    #                     payload=self.payload)
    #             # next will be delegation if current is deny and session is passed or deny and delegation is unset
    #             else:
    #                 LOG.error("Delegation is not developed!")
    #
    #         else:
    #             # else next will be None and the request is sent to router
    #             return self.__return_to_router()
    #     elif current_container_genre == "session":
    #         pass
    #         # next will be next container in headers if current is passed
    #         if self.payload["authz_context"]['pdp_set'][current_meta_rule]['effect'] == "passed":
    #             return notify(
    #                 request_id=self.payload["authz_context"]["request_id"],
    #                 container_id=self.__get_container_from_meta_rule(next_meta_rule)['container_id'],
    #                 payload=self.payload)
    #         # next will be None if current is grant and the request is sent to router
    #         else:
    #             return self.__return_to_router()
    #     elif current_container_genre == "delegation":
    #         LOG.error("Delegation is not developed!")
    #         # next will be authz if current is deny
    #         # next will be None if current is grant and the request is sent to router

    def set_result(self, result):
        self.result = result

    def is_authz(self):
        if not self.result:
            return False
        authz_results = []
        for key in self.result.pdp_set:
            if "effect" in self.result.pdp_set[key]:

                if self.result.pdp_set[key]["effect"] == "grant":
                    # the pdp is a authorization PDP and grant the request
                    authz_results.append(True)
                elif self.result.pdp_set[key]["effect"] == "passed":
                    # the pdp is not a authorization PDP (session or delegation) and had run normally
                    authz_results.append(True)
                elif self.result.pdp_set[key]["effect"] == "unset":
                    # the pdp is not a authorization PDP (session or delegation) and had not yep run
                    authz_results.append(True)
                else:
                    # the pdp is (or not) a authorization PDP and had run badly
                    authz_results.append(False)
        if list(itertools.accumulate(authz_results, lambda x, y: x & y))[-1]:
            self.result.pdp_set["effect"] = "grant"
        if self.result:
            if self.result.pdp_set["effect"] == "grant":
                self.final_result = "Grant"
                return True
        self.final_result = "Deny"
        return True
