import logging
from cliff.lister import Lister
from cliff.command import Command
from importlib.machinery import SourceFileLoader

from python_moonclient.core import models, policies, pdp
from python_moonclient.cli.parser import Parser
from python_moonclient.cli.projects import ProjectsUtils

logger = logging.getLogger("moonclient.cli.pdps")


class ModelUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_model_id(model, parsed_id, parsed_name):
        modelz = models.check_model()
        for _model_key, _model_value in modelz["models"].items():
            if _model_key == parsed_id or _model_value['name'] == parsed_name:
                # logger.info("Found pdp : [key='{}' , name='{}']".format(_pdp_key, _pdp_value['name']))
                return _model_key
        return None

    @staticmethod
    def get_model_name(pdp, parsed_id, parsed_name):
        modelz = models.check_model()
        for _model_key, _model_value in modelz["models"].items():
            if _model_key == parsed_id or _model_value['name'] == parsed_name:
                # logger.info("Found pdp : [key='{}' , name='{}']".format(_pdp_key, _pdp_value['name']))
                return _model_value['name']
        return None


class Models(Lister):
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

        modelz = models.check_model()

        return (('Key', 'Name'),
                ((_model_key, _model_value['name']) for _model_key, _model_value in
                 modelz["models"].items())
                )


class SubjectCategories(Lister):
    """show the list of existing categories """

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

        subject_categories = models.check_subject_category()
        print(subject_categories)
        return (('Key', 'Name'),
                ((_model_key, _model_value['name']) for _model_key, _model_value in
                 subject_categories["subject_categories"].items())
                )


class ObjectCategories(Lister):
    """show the list of existing categories """

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

        object_categories = models.check_object_category()
        print(object_categories)
        return (('Key', 'Name'),
                ((_model_key, _model_value['name']) for _model_key, _model_value in
                 object_categories["object_categories"].items())
                )


class ActionCategories(Lister):
    """show the list of existing categories """

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

        action_categories = models.check_action_category()
        print(action_categories)
        return (('Key', 'Name'),
                ((_model_key, _model_value['name']) for _model_key, _model_value in
                 action_categories["action_categories"].items())
                )


class SubjectCategoryAdd(Command):
    """show the list of existing categories """

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_name_argument(parser)

        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        subject_category_id = models.add_subject_category(parsed_args.name)
        if subject_category_id is not None:
            print("Subject category created with id {}".format(subject_category_id))
        else:
            print("Error while creating subject category")
        # subject_categories = models.check_subject_category(subject_category_id)



