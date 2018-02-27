
from python_moonclient.core import models, policies, pdp, json_import
from python_moonclient.cli.parser import Parser
from python_moonclient.cli.projects import ProjectsUtils

from cliff.command import Command


class Import(Command):
    """import a json file describing pdps """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_filename_argument(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)
        json_import.init(consul_host, consul_port)
        res = json_import.import_json(parsed_args.filename)
        if "message" in res:
            return res["message"]
        return res

