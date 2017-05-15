# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import hashlib
from oslo_config import cfg
from oslo_log import log as logging
# from moon_db.core import IntraExtensionRootManager
# from moon_db.core import ConfigurationManager
from moon_utilities.security_functions import call

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Containers(object):
    """
    Manage containers.
    """

    __version__ = "0.1.0"

    def __init__(self, docker_manager):
        self.docker_manager = docker_manager
        self.components = dict()
        for pdp_key, pdp_value in call("moon_manager", method="get_pdp",
                                       ctx={"user_id": "admin", "id": None})["pdps"].items():
            self.add_container(ctx={"id": pdp_key, "pipeline": pdp_value["security_pipeline"]})

            # for _ext_id, _ext_value in self.__get_pdp({"user_id": "admin"}, None)["intra_extensions"].items():
        #     self.docker_manager.load(component="policy", uuid=_ext_id)
        #     # FIXME (asteroide): there may be other security_function here (delegation, ...)
        #     LOG.info("ADDING Containers {}".format(_ext_value))
        #     self.docker_manager.load(component="function", uuid="{}_{}_{}".format("authz", "rbac_rule", _ext_id))

    # def __get_pdp(self, ctx, args=None):
    #     """Get information about all pdp
    #
    #     :param ctx: {
    #         "user_id": "uuid of a user",
    #         "id": "uuid of a tenant or an intra_extension"
    #     }
    #     :param args: {}
    #     :return: {
    #         "intra_extension_id": {
    #             "name": "name of the intra extension",
    #             "model": "model of the intra extension",
    #             "genre": "genre of the intra extension",
    #             "description": "description of the intra-extension"
    #         }
    #     }
    #     """
    #     # TODO (asteroide): check if ctx["id"] is a tenant UUID or an intra_extension UUID.
    #     _ext = IntraExtensionRootManager.get_intra_extensions_dict(ctx["user_id"])
    #     if ctx and "id" in ctx and ctx["id"]:
    #         if ctx["id"] in _ext:
    #             return {"pdp": {ctx["id"]: _ext[ctx["id"]]}}
    #         return {"error": "No pdp with id {}".format(ctx["id"])}
    #     return {"pdp": _ext}

    def get_container(self, ctx, args=None):
        uuid = ctx.get("id")
        keystone_project_id = ctx.get("keystone_project_id")
        # _containers = self.docker_manager.get_component(uuid=uuid)
        # LOG.info("containers={}".format(_containers))
        if uuid:
            return self.components[uuid]
        elif keystone_project_id:
            for container_id, container_value in self.components.items():
                if container_value['keystone_project_id'] == keystone_project_id:
                    return {container_id: container_value}
            else:
                return {}
        return {"containers": self.components}

    def add_container(self, ctx, args=None):
        """Add containers linked to an intra-extension

        :param ctx: {"id": "intra_extension_uuid"}
        :param args: {}
        :return: {
            "container_id1": {"status": True},
            "container_id2": {"status": True},
        }
        """
        LOG.info("add_container {}".format(ctx))
        pdp = call("moon_manager", method="get_pdp",
                   ctx={"user_id": "admin", "id": ctx["id"]},
                   args={})["pdps"]
        pdp_id = list(pdp.keys())[0]
        if not pdp[pdp_id]["keystone_project_id"]:
            return {"result": "False", "message": "Cannot find keystone_project_id in pdp"}
        keystone_project_id = pdp[pdp_id]["keystone_project_id"]
        self.components[ctx["id"]] = []
        for policy_key, policy_value in call("moon_manager", method="get_policies",
                                             ctx={"user_id": "admin", "id": None},
                                             args={})["policies"].items():
            if policy_key in ctx["pipeline"]:
                models = call("moon_manager", method="get_models",
                              ctx={"user_id": "admin", "id": None},
                              args={})["models"]
                for meta_rule in models[policy_value['model_id']]['meta_rules']:
                    genre = policy_value['genre']
                    pre_container_id = "pdp:{}_metarule:{}_project:{}".format(ctx["id"], meta_rule, keystone_project_id)
                    policy_component = self.docker_manager.load(component=genre,
                                                                uuid=pre_container_id)
                    self.components[ctx["id"]].append({
                        "meta_rule_id": meta_rule,
                        "genre": policy_value['genre'],
                        "keystone_project_id": keystone_project_id,
                        "container_id": policy_value['genre']+"_"+hashlib.sha224(pre_container_id.encode("utf-8")).hexdigest()
                    })
        return {"containers": self.components[ctx["id"]]}
        # function_components = []
        # for pdp in ctx['pdp_pipeline']:
        #     key, value = pdp.split(":")
        #     LOG.info("add_container {}:{}".format(key, value))
        #     function_components.append(self.docker_manager.load(component="function",
        #                                                         uuid="{}_{}_{}".format(key, value, ctx["id"])))
        # containers = dict()
        # containers[policy_component.id] = policy_component.get_status()
        # for component in function_components:
        #     containers[component.id] = component.get_status()
        # return {"containers": containers}

    def delete_container(self, ctx, args=None):
        """Delete a container

        :param ctx: {"id": "intra_extension_uuid"}
        :param args: {}
        :return: {}
        """
        try:
            self.docker_manager.kill(component_id="moon_secpolicy_"+ctx["id"])
            try:
                # FIXME (asteroide): need to select other security_function here
                self.docker_manager.kill(component_id="moon_secfunction_authz_"+ctx["id"])
            except Exception as e:
                LOG.error(e, exc_info=True)
                return {"result": True,
                        "error": {'code': 200, 'title': 'Moon Warning', 'description': str(e)},
                        "intra_extension_id": ctx["id"],
                        "ctx": ctx, "args": args}
        except Exception as e:
            LOG.error(e, exc_info=True)
            return {"result": False,
                    "error": {'code': 500, 'title': 'Moon Error', 'description': str(e)},
                    "intra_extension_id": ctx["id"],
                    "ctx": ctx, "args": args}
        return {"result": True}

