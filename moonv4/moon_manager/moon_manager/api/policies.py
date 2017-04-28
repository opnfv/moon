# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from oslo_log import log as logging
from oslo_config import cfg
from moon_db.core import PolicyManager

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Policies(object):

    def __init__(self):
        self.manager = PolicyManager

    def get_policies(self, ctx, args):
        try:
            data = self.manager.get_policies(user_id=ctx["user_id"], policy_id=ctx["id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"policies": data}

    def add_policy(self, ctx, args):
        try:
            data = self.manager.add_policy(user_id=ctx["user_id"], policy_id=ctx["id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"policies": data}

    def delete_policy(self, ctx, args):
        try:
            data = self.manager.delete_policy(user_id=ctx["user_id"], policy_id=ctx["id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def update_policy(self, ctx, args):
        try:
            data = self.manager.update_policy(user_id=ctx["user_id"], policy_id=ctx["id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"policies": data}


class Perimeter(object):

    def __init__(self):
        self.manager = PolicyManager

    def get_subjects(self, ctx, args):
        try:
            data = self.manager.get_subjects(user_id=ctx["user_id"], policy_id=ctx["id"], perimeter_id=args['perimeter_id'])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"subjects": data}

    def set_subject(self, ctx, args):
        try:
            if not ctx["perimeter_id"]:
                data = self.manager.get_subjects(user_id=ctx["user_id"], policy_id=None)
                for data_id, data_value in data.items():
                    if data_value['name'] == args['name']:
                        ctx["perimeter_id"] = data_id
                        break
            data = self.manager.add_subject(user_id=ctx["user_id"], policy_id=ctx["id"],
                                            perimeter_id=ctx["perimeter_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"subjects": data}

    def delete_subject(self, ctx, args):
        try:
            data = self.manager.delete_subject(user_id=ctx["user_id"], policy_id=ctx["id"], perimeter_id=args["perimeter_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def get_objects(self, ctx, args):
        try:
            data = self.manager.get_objects(user_id=ctx["user_id"], policy_id=ctx["id"], perimeter_id=args['perimeter_id'])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"objects": data}

    def set_object(self, ctx, args):
        try:
            data = self.manager.get_objects(user_id=ctx["user_id"], policy_id=None)
            for data_id, data_value in data.items():
                if data_value['name'] == args['name']:
                    ctx["perimeter_id"] = data_id
                    break
            data = self.manager.add_object(user_id=ctx["user_id"], policy_id=ctx["id"],
                                           perimeter_id=ctx["perimeter_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"objects": data}

    def delete_object(self, ctx, args):
        try:
            data = self.manager.delete_object(user_id=ctx["user_id"], policy_id=ctx["id"], perimeter_id=args["perimeter_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def get_actions(self, ctx, args):
        try:
            data = self.manager.get_actions(user_id=ctx["user_id"], policy_id=ctx["id"], perimeter_id=args['perimeter_id'])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"actions": data}

    def set_action(self, ctx, args):
        try:
            data = self.manager.get_actions(user_id=ctx["user_id"], policy_id=None)
            for data_id, data_value in data.items():
                if data_value['name'] == args['name']:
                    ctx["perimeter_id"] = data_id
                    break
            data = self.manager.add_action(user_id=ctx["user_id"], policy_id=ctx["id"],
                                           perimeter_id=ctx["perimeter_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"actions": data}

    def delete_action(self, ctx, args):
        try:
            data = self.manager.delete_action(user_id=ctx["user_id"], policy_id=ctx["id"], perimeter_id=args["perimeter_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}


class Data(object):

    def __init__(self):
        self.manager = PolicyManager

    def get_subject_data(self, ctx, args):
        try:
            data = self.manager.get_subject_data(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                 category_id=ctx["category_id"], data_id=args["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"subject_data": data}

    def add_subject_data(self, ctx, args):
        try:
            data = self.manager.set_subject_data(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                 category_id=ctx["category_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"subject_data": data}

    def delete_subject_data(self, ctx, args):
        try:
            data = self.manager.delete_subject_data(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                    data_id=["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def get_object_data(self, ctx, args):
        try:
            data = self.manager.get_object_data(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                category_id=ctx["category_id"], data_id=args["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"object_data": data}

    def add_object_data(self, ctx, args):
        try:
            data = self.manager.add_object_data(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                category_id=ctx["category_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"object_data": data}

    def delete_object_data(self, ctx, args):
        try:
            data = self.manager.delete_object_data(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                   data_id=["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def get_action_data(self, ctx, args):
        try:
            data = self.manager.get_action_data(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                category_id=ctx["category_id"], data_id=args["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"action_data": data}

    def add_action_data(self, ctx, args):
        try:
            data = self.manager.add_action_data(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                category_id=ctx["category_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"action_data": data}

    def delete_action_data(self, ctx, args):
        try:
            data = self.manager.delete_action_data(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                   data_id=["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}


class Assignments(object):

    def __init__(self):
        self.manager = PolicyManager

    def get_subject_assignments(self, ctx, args):
        try:
            data = self.manager.get_subject_assignments(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                        subject_id=ctx["perimeter_id"], category_id=ctx["category_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"subject_assignments": data}

    def update_subject_assignment(self, ctx, args):
        try:
            data = self.manager.add_subject_assignment(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                       subject_id=args["id"], category_id=args["category_id"],
                                                       data_id=args["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"subject_assignments": data}

    def delete_subject_assignment(self, ctx, args):
        try:
            data = self.manager.delete_subject_assignment(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                          subject_id=ctx["perimeter_id"], category_id=ctx["category_id"],
                                                          data_id=args["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def get_object_assignments(self, ctx, args):
        try:
            data = self.manager.get_object_assignments(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                       object_id=ctx["perimeter_id"], category_id=ctx["category_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"object_assignments": data}

    def update_object_assignment(self, ctx, args):
        try:
            data = self.manager.add_object_assignment(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                      object_id=args["id"], category_id=args["category_id"],
                                                      data_id=args["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"object_assignments": data}

    def delete_object_assignment(self, ctx, args):
        try:
            data = self.manager.delete_object_assignment(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                         object_id=ctx["perimeter_id"], category_id=ctx["category_id"],
                                                         data_id=args["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def get_action_assignments(self, ctx, args):
        try:
            data = self.manager.get_action_assignments(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                       action_id=ctx["perimeter_id"], category_id=ctx["category_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"action_assignments": data}

    def update_action_assignment(self, ctx, args):
        try:
            data = self.manager.add_action_assignment(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                      action_id=args["id"], category_id=args["category_id"],
                                                      data_id=args["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"action_assignments": data}

    def delete_action_assignment(self, ctx, args):
        try:
            data = self.manager.delete_action_assignment(user_id=ctx["user_id"], policy_id=ctx["id"],
                                                         action_id=ctx["perimeter_id"], category_id=ctx["category_id"],
                                                         data_id=args["data_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}


class Rules(object):

    def __init__(self):
        self.manager = PolicyManager

    def get_rules(self, ctx, args):
        try:
            data = self.manager.get_rules(user_id=ctx["user_id"],
                                          policy_id=ctx["id"],
                                          # meta_rule_id=ctx["meta_rule_id"],
                                          rule_id=ctx["rule_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"rules": data}

    def add_rule(self, ctx, args):
        try:
            data = self.manager.add_rule(user_id=ctx["user_id"],
                                         policy_id=ctx["id"],
                                         meta_rule_id=args["meta_rule_id"],
                                         value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"rules": data}

    def delete_rule(self, ctx, args):
        try:
            data = self.manager.delete_rule(user_id=ctx["user_id"], policy_id=ctx["id"], rule_id=ctx['rule_id'])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}
