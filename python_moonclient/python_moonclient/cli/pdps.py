import logging
from importlib.machinery import SourceFileLoader
from cliff.lister import Lister
from cliff.command import Command

from python_moonclient.core import models, policies, pdp
from python_moonclient.cli.parser import Parser
from python_moonclient.cli.projects import ProjectsUtils

LOGGER = logging.getLogger("moonclient.cli.pdps")


class PdpUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_pdp_id(pdp, parsed_id, parsed_name):
        pdps = pdp.check_pdp()
        for _pdp_key, _pdp_value in pdps["pdps"].items():
            if _pdp_key == parsed_id or _pdp_value['name'] == parsed_name:
                # LOGGER.info(
                # "Found pdp : [key='{}' , name='{}']".format(_pdp_key, _pdp_value['name']))
                return _pdp_key
        return None

    @staticmethod
    def get_pdp_name(pdp, parsed_id, parsed_name):
        pdps = pdp.check_pdp()
        for _pdp_key, _pdp_value in pdps["pdps"].items():
            if _pdp_key == parsed_id or _pdp_value['name'] == parsed_name:
                # LOGGER.info(
                # "Found pdp : [key='{}' , name='{}']".format(_pdp_key, _pdp_value['name']))
                return _pdp_value['name']
        return None


class Pdps(Lister):
    """show the list of existing pdps """

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

        pdps = pdp.check_pdp()

        return (('Key', 'Name', 'Project id'),
                ((_pdp_key, _pdp_value['name'], _pdp_value['keystone_project_id']) for
                 _pdp_key, _pdp_value in pdps["pdps"].items())
                )


class CreatePdp(Command):
    """create a new pdp from a json file and returns the newly created pdp id"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_filename_argument(parser)
        return parser

    def take_action(self, parsed_args):

        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = True

        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port
        # project_id = args.keystone_pid

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        if parsed_args.filename:
            LOGGER.info("Loading: {}".format(parsed_args.filename))
        m = SourceFileLoader("scenario", parsed_args.filename)
        scenario = m.load_module()

        _models = models.check_model()
        for _model_id, _model_value in _models['models'].items():
            if _model_value['name'] == scenario.model_name:
                model_id = _model_id
                meta_rule_list = _model_value['meta_rules']
                models.create_model(scenario, model_id)
                break
        else:
            model_id, meta_rule_list = models.create_model(scenario)
        policy_id = policies.create_policy(scenario, model_id, meta_rule_list)
        pdp_id = pdp.create_pdp(scenario, policy_id=policy_id)
        pdp_name = PdpUtils.get_pdp_name(pdp, pdp_id, None)
        LOGGER.info("Pdp created : [id='{}', name='{}']".format(pdp_id, pdp_name))


class DeletePdp(Command):
    """delete an existing pdp"""

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

        _search = PdpUtils.get_pdp_id(pdp, parsed_args.id, parsed_args.name)
        _pdp_key = _search
        if _pdp_key is None:
            LOGGER.error("Error pdp not found ")
            return

        # if parsed_args.id:
        #    logger.info("Deleting: {}".format(parsed_args.id))
        #    _search = parsed_args.id
        # if parsed_args.name:
        #    logger.info("Deleting: {}".format(parsed_args.name))
        #    _search = parsed_args.name

        # pdps = pdp.check_pdp()
        # for _pdp_key, _pdp_value in pdps["pdps"].items():
        #    if _pdp_key == _search or _pdp_value['name'] == _search:
        LOGGER.info("Found {}".format(_pdp_key))
        pdp.delete_pdp(_pdp_key)

        pdps = pdp.check_pdp()
        LOGGER.info("Listing all PDP:")
        for _pdp_key, _pdp_value in pdps["pdps"].items():
            if _pdp_key == _search:  # or _pdp_value['name'] == _search:
                LOGGER.error("Error in deleting {}".format(_search))

        return (('Key', 'Name', 'Project id'),
                ((_pdp_key, _pdp_value['name'], _pdp_value['keystone_project_id']) for
                 _pdp_key, _pdp_value in
                 pdps["pdps"].items())
                )


class MapPdp(Command):
    """map an existing pdp to a keystone project"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_id_or_name_pdp_argument(parser)
        Parser.add_id_or_name_project_argument(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        # _pdp_key = PdpUtils.get_pdp_id(pdp, parsed_args.id_pdp, parsed_args.name_pdp)
        _pdp_name = PdpUtils.get_pdp_name(pdp, parsed_args.id_pdp, parsed_args.name_pdp)
        if _pdp_name is None:
            LOGGER.error("Error pdp not found ")
            return

        # _project_key = ProjectsUtils.get_project_id(
        # pdp, parsed_args.id_project, parsed_args.name_project)
        _project_name = ProjectsUtils.get_project_name(pdp, parsed_args.id_project,
                                                       parsed_args.name_project)
        if _project_name is None:
            LOGGER.error("Error project not found ")
            return

        LOGGER.info("Mapping: {}=>{}".format(_pdp_name, _project_name))

        # pdp.map_to_keystone(pdp_id=parsed_args.id_pdp, keystone_project_id=parsed_args.id_project)
        pdp.map_to_keystone(pdp_id=_pdp_name, keystone_project_id=_project_name)
