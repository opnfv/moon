import logging
from cliff.lister import Lister
from cliff.command import Command

from python_moonclient.core import models, policies, pdp, slaves
from python_moonclient.cli.parser import Parser

logger = logging.getLogger("moonclient.cli.slaves")


class SlavesUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_slave_name(slaves, parsed_name):
        _slaves = slaves.get_slaves()
        for _slave_value in _slaves['slaves']:
            if _slave_value['name'] == parsed_name:
                logger.info("Found {}".format(_slave_value['name']))
                return _slave_value['name']
        return None


class Slaves(Lister):
    """show the list of slaves"""
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        return parser

    def take_action(self, parsed_args):
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = True

        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)
        slaves.init(consul_host, consul_port)

        return (('Name', 'Configured'),
                ((value['name'], value['configured']) for value in slaves.get_slaves().get('slaves', dict()))
                )


class SetSlave(Command):
    """update an existing slave to a configured state"""
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_name_argument(parser)
        return parser

    def take_action(self, parsed_args):
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = True

        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)
        slaves.init(consul_host, consul_port)
        slave_name = SlavesUtils.get_slave_name(slaves, parsed_args.name)
        if slave_name is None:
            slave_name = "kubernetes-admin@kubernetes"

        #if parsed_args.name:
        #    slave_name = parsed_args.name
        print("    {} (configured=True)".format(slave_name))

        #for value in slaves.set_slave(slave_name).get('slaves', dict()):
        #    if value['configured']:
        #        print("    {} (configured)".format(value['name']))
        #    else:
        #        print("    {} (not configured)".format(value['name']))#


class DeleteSlave(Command):
    """update an existing slave to a unconfigured state"""
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_name_argument(parser)
        return parser

    def take_action(self, parsed_args):
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = True

        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)
        slaves.init(consul_host, consul_port)

        slave_name = SlavesUtils.get_slave_name(slaves, parsed_args.name)
        if slave_name is None:
            slave_name = "kubernetes-admin@kubernetes"

        slaves.delete_slave(slave_name)
        print("    {} (configured=False)".format(slave_name))




