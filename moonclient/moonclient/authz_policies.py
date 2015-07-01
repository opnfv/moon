# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging

from cliff.lister import Lister


class AuthzPolicies(Lister):
    """List all Intra_Extensions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(AuthzPolicies, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        policies = self.app.get_url("/v3/OS-MOON/authz_policies", authtoken=True)["authz_policies"]
        return (
            ("name",),
            ((_name, ) for _name in policies)
        )
