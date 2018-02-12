import logging
from python_moonclient.core import models, policies, pdp
from python_moonclient.cli.parser import Parser
from cliff.lister import Lister

logger = logging.getLogger("moonclient.cli.projects")


class ProjectsUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_project_id(pdp, parsed_id, parsed_name):
        projects = pdp.get_keystone_projects()
        for _project_value in projects['projects']:
            if _project_value['id'] == parsed_id or _project_value['name'] == parsed_name:
                #logger.info("Found project : [key='{}' , name='{}']".format(_project_value['id'], _project_value['name']))
                return _project_value['id']
        return None

    @staticmethod
    def get_project_name(pdp, parsed_id, parsed_name):
        projects = pdp.get_keystone_projects()
        for _project_value in projects['projects']:
            if _project_value['id'] == parsed_id or _project_value['name'] == parsed_name:
                #logger.info("Found project : [key='{}' , name='{}']".format(_project_value['id'], _project_value['name']))
                return _project_value['name']
        return None


class Projects(Lister):
    """show the list of projects"""

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

        projects = pdp.get_keystone_projects()

        return (('Id' , 'Name'),
                   ((_project['id'],  _project['name']) for _project in projects['projects'])
               )

        


