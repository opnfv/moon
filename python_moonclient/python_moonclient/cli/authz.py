import logging

from importlib.machinery import SourceFileLoader
from cliff.command import Command

from python_moonclient.core import models, policies, pdp, authz
from python_moonclient.cli.parser import Parser
from python_moonclient.cli.projects import ProjectsUtils

LOGGER = logging.getLogger("moonclient.cli.authz")


class SendAuthz(Command):
    """send authorizations to wrapper"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_filename_argument(parser)
        Parser.add_id_or_name_project_argument(parser)
        Parser.add_authz_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        if parsed_args.filename:
            LOGGER.info("Loading: {}".format(parsed_args.filename))
        m = SourceFileLoader("scenario", parsed_args.filename)
        scenario = m.load_module()

        keystone_project_id = ProjectsUtils.get_project_id(pdp, parsed_args.id_project,
                                                           parsed_args.name_project)
        if keystone_project_id is None:
            LOGGER.error("Project not found !")

        keystone_project_id = pdp.get_keystone_id(keystone_project_id)
        time_data = authz.send_requests(
            scenario,
            parsed_args.authz_host,
            parsed_args.authz_port,
            keystone_project_id,
            request_second=parsed_args.request_second,
            limit=parsed_args.limit,
            dry_run=parsed_args.dry_run,
            stress_test=parsed_args.stress_test,
            destination=parsed_args.destination
        )
        if not parsed_args.dry_run:
            authz.save_data(parsed_args.write, time_data)
