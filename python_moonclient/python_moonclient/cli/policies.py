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


class Subjects(Lister):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_id_or_name_argument(parser)
        Parser.add_policy_argument(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        _policies = policies.check_subject(parsed_args.id, parsed_args.policy_id)

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



class SubjectDatas(Lister):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_policy_argument(parser)
        Parser.add_category_argument(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        subject_datas = policies.check_subject_data(parsed_args.policy_id, None, parsed_args.category_id)
        if len(subject_datas["subject_data"]) == 0:
            return (('Key', 'Name'),())

        return (('Key', 'Name'),
                   ((_subject_key, subject_datas["subject_data"][0]["data"][_subject_key]['name']) for _subject_key in subject_datas["subject_data"][0]["data"].keys())
               )


class ObjectDatas(Lister):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_policy_argument(parser)
        Parser.add_category_argument(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        object_datas = policies.check_object_data(parsed_args.policy_id, None, parsed_args.category_id)

        if len(object_datas["object_data"]) == 0:
            return (('Key', 'Name'),())
        object_data = object_datas["object_data"][0]["data"]
        res =  (('Key', 'Name'),
                   ((_object_key, object_data[_object_key]["value"]['name']) for _object_key in list(object_data))
               )
        return res


class ActionDatas(Lister):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_policy_argument(parser)
        Parser.add_category_argument(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        action_datas = policies.check_action_data(parsed_args.policy_id, None, parsed_args.category_id)

        if len(action_datas["action_data"]) == 0:
            return (('Key', 'Name'),())
        action_data = action_datas["action_data"][0]["data"]
        res =  (('Key', 'Name'),
                   ((_action_key, action_data[_action_key]["value"]['name']) for _action_key in list(action_data))
               )
        return res


class MetaRules(Lister):
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

        metarule_datas = policies.check_meta_rule()

        if len(metarule_datas["meta_rules"]) == 0:
            return (('Key', 'Name'),())

        metarule_data = metarule_datas["meta_rules"]
        res =  (('Key', 'Name'),
                   ((_key, metarule_data[_key]['name']) for _key in list(metarule_data))
               )
        return res

class CreateSubjectData(Command):

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        Parser.add_common_options(parser)
        Parser.add_policy_argument(parser)
        Parser.add_category_argument(parser)
        Parser.add_name_argument(parser)
        return parser

    def take_action(self, parsed_args):
        consul_host = parsed_args.consul_host
        consul_port = parsed_args.consul_port

        models.init(consul_host, consul_port)
        policies.init(consul_host, consul_port)
        pdp.init(consul_host, consul_port)

        subject_data_id = policies.add_subject_data(parsed_args.policy_id, parsed_args.category_id, parsed_args.name)
        if subject_data_id is not None:
            print("Subject category created with id {}".format(subject_data_id))
        else:
            print("Error while creating subject category")
        subject_datas = policies.check_subject_data(parsed_args.policy_id, None, parsed_args.category_id)
        # subject_categories = models.check_subject_category(subject_category_id)