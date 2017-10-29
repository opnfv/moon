# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import hashlib
from oslo_config import cfg
from oslo_log import log as logging
# from moon_db.core import IntraExtensionRootManager
# from moon_db.core import ConfigurationManager
# from moon_utilities.security_functions import call

LOG = logging.getLogger("moon.orchestrator.api.containers")
CONF = cfg.CONF


class Containers(object):
    """
    Manage containers.
    """

    __version__ = "0.1.0"

    def __init__(self, docker_manager):
        self.docker_manager = docker_manager
        self.components = dict()
        # for pdp_key, pdp_value in call("moon_manager", method="get_pdp",
        #                                ctx={"user_id": "admin", "id": None})["pdps"].items():
        #     self.add_container(ctx={"id": pdp_key, "pipeline": pdp_value["security_pipeline"]})

    def get_container(self, ctx, args=None):
        """Get containers linked to an intra-extension

        :param ctx: {
            "id": "intra_extension_uuid",
            "keystone_project_id": "Keystone Project UUID"
        }    
        :param args: {}
        :return: {
            "containers": {...},
        }
        """
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
        """Add containers

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
                    container_data = {"pdp": ctx["id"], "metarule": meta_rule, "project": keystone_project_id}
                    policy_component = self.docker_manager.load(component=genre,
                                                                uuid=pre_container_id,
                                                                container_data=container_data)
                    self.components[ctx["id"]].append({
                        "meta_rule_id": meta_rule,
                        "genre": policy_value['genre'],
                        "keystone_project_id": keystone_project_id,
                        "container_id": policy_value['genre']+"_"+hashlib.sha224(pre_container_id.encode("utf-8")).hexdigest()
                    })
        return {"containers": self.components[ctx["id"]]}

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

