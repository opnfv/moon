import json

from python_moonclient.core import models, policies, pdp, json_export
from python_moonclient.cli.parser import Parser

from cliff.command import Command


class Export(Command):
    """dump the complete moon database into a json file"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_filename_argument(parser)
        Parser.add_common_options(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)
        json_export.init(consul_host, consul_port)
        res = json_export.export_to_json()
        if "content" in res:
            json_file = open(parsed_args.filename, "w")
            json.dump(res["content"], json_file)
            return "Export ok!"

        return "Unexpected results : the returned json does not have the correct syntax"
