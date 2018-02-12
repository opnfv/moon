import logging
from cliff.command import Command
from cliff.lister import Lister

from python_moonclient.cli.parser import Parser

from python_moonclient.core import models, policies, pdp

logger = logging.getLogger("moonclient.cli.pdps")


class PoliciesUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_policy_id(policies, parsed_id, parsed_name):
        _policies = policies.check_policy()
        for  _policy_key, _policy_value in _policies["policies"].items():
            if _policy_key == parsed_id or _policy_value['name'] == parsed_name:
                #logger.info("Found {}".format(_policy_key))
                return _policy_key
        return None

    @staticmethod
    def get_policy_name(policies, parsed_id, parsed_name):
        _policies = policies.check_policy()
        for  _policy_key, _policy_value in _policies["policies"].items():
            if _policy_key == parsed_id or _policy_value['name'] == parsed_name:
                #logger.info("Found {}".format(_policy_key))
                return _policy_value['name']
        return None


class Policies(Lister):
    """show the list of existing policies"""
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)
        _policies = policies.check_policy()

        return (('Key' , 'Name'),
                   ((_policy_key,  _policy_value['name']) for _policy_key, _policy_value in _policies["policies"].items())
               )


class DeletePolicy(Command):
    """delete an existing policy"""
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_id_or_name_argument(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        policy_id = PoliciesUtils.get_policy_id(policies,parsed_args.id, parsed_args.name)
        policy_name = PoliciesUtils.get_policy_name(policies, parsed_args.id, parsed_args.name)

        logger.info("Deleting: {}".format(policy_name))
        pdp.delete_pdp(policy_id)

        _policies = policies.check_policy()
        #logger.info("Listing all Policies:")
        for _policy_key, _policy_value in _policies["policies"].items():
            #print("    {} {}".format(_policy_key, _policy_value['name']))
            if _policy_key == policy_id:
                logger.error("Error in deleting {}".format(policy_id))

        return (('Key', 'Value'),
                ((_policy_key, _policy_value) for _policy_key, _policy_value in _policies["policies"].items())
                )
