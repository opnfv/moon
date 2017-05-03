# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from oslo_log import log as logging
from oslo_config import cfg
from moon_db.core import ModelManager

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Models(object):

    def __init__(self):
        self.manager = ModelManager

    def get_models(self, ctx, args):
        try:
            data = self.manager.get_models(user_id=ctx["user_id"], model_id=ctx.get("id"))
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"models": data}

    def add_model(self, ctx, args):
        try:
            data = self.manager.add_model(user_id=ctx["user_id"], model_id=ctx.get("id"), value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"models": data}

    def delete_model(self, ctx, args):
        try:
            data = self.manager.delete_model(user_id=ctx["user_id"], model_id=ctx["id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def update_model(self, ctx, args):
        try:
            data = self.manager.update_model(user_id=ctx["user_id"], model_id=ctx["id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"models": data}


class MetaRules(object):

    def __init__(self):
        self.manager = ModelManager

    def add_meta_rules(self, ctx, args):
        try:
            data = self.manager.add_meta_rule(user_id=ctx["user_id"], meta_rule_id=None, value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"meta_rules": data}

    def delete_meta_rules(self, ctx, args):
        try:
            data = self.manager.delete_meta_rule(user_id=ctx["user_id"], meta_rule_id=ctx["meta_rule_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def get_meta_rules(self, ctx, args):
        try:
            data = self.manager.get_meta_rules(user_id=ctx["user_id"], meta_rule_id=ctx["meta_rule_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"meta_rules": data}

    def set_meta_rules(self, ctx, args):
        try:
            data = self.manager.set_meta_rule(user_id=ctx["user_id"], meta_rule_id=ctx["meta_rule_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"meta_rules": data}


class MetaData(object):

    def __init__(self):
        self.manager = ModelManager

    def get_subject_categories(self, ctx, args):
        try:
            data = self.manager.get_subject_categories(user_id=ctx["user_id"], category_id=args["category_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"subject_categories": data}

    def set_subject_category(self, ctx, args):
        try:
            data = self.manager.add_subject_category(user_id=ctx["user_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"subject_categories": data}

    def delete_subject_category(self, ctx, args):
        try:
            data = self.manager.delete_subject_category(user_id=ctx["user_id"], category_id=args["category_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def get_object_categories(self, ctx, args):
        try:
            data = self.manager.get_object_categories(user_id=ctx["user_id"], category_id=args["category_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"object_categories": data}

    def set_object_category(self, ctx, args):
        try:
            data = self.manager.add_object_category(user_id=ctx["user_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"object_categories": data}

    def delete_object_category(self, ctx, args):
        try:
            data = self.manager.delete_object_category(user_id=ctx["user_id"], category_id=args["category_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}

    def get_action_categories(self, ctx, args):
        try:
            data = self.manager.get_action_categories(user_id=ctx["user_id"], category_id=args["category_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"action_categories": data}

    def set_action_category(self, ctx, args):
        try:
            data = self.manager.add_action_category(user_id=ctx["user_id"], value=args)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"action_categories": data}

    def delete_action_category(self, ctx, args):
        try:
            data = self.manager.delete_action_category(user_id=ctx["user_id"], category_id=args["category_id"])
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": str(e),
                    "ctx": ctx, "args": args}
        return {"result": True}
