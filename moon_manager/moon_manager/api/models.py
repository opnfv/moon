# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.

"""
Models aggregate multiple meta rules
"""

import hug
import json
import logging
import requests
from moon_manager import db_driver as driver
from moon_utilities.security_functions import validate_input
from moon_utilities.auth_functions import api_key_authentication, connect_from_env
from moon_utilities.invalided_functions import invalidate_model_in_slaves
from moon_manager.api import slave as slave_class
from moon_manager.api import configuration


LOGGER = logging.getLogger("moon.manager.api." + __name__)


class Models(object):
    """
    Endpoint for model requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/models", requires=api_key_authentication)
    @hug.get("/models/{model_id}", requires=api_key_authentication)
    def get(model_id: hug.types.text = None, moon_user_id=None):
        """Retrieve all models

        :param model_id: uuid of the model
        :param moon_user_id: user ID who do the request
        :return: {
            "model_id1": {
                "name": "...",
                "description": "... (optional)",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: get_models
        """
        data = driver.ModelManager.get_models(moon_user_id=moon_user_id, model_id=model_id)
        return {"models": data}

    @staticmethod
    @hug.local()
    @hug.post("/models", requires=api_key_authentication)
    def post(body: validate_input("name"), moon_user_id=None):
        """Create model.

        :param body: body of the request
        :param moon_user_id: user ID who do the request
        :request body: {
            "name": "name of the model (mandatory)",
            "description": "description of the model (optional)",
            "meta_rules": ["meta_rule_id1", ]
        }
        :return: {
            "model_id1": {
                "name": "name of the model",
                "description": "description of the model (optional)",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: add_model
        """
        data = driver.ModelManager.add_model(
            moon_user_id=moon_user_id, value=body)

        return {"models": data}

    @staticmethod
    @hug.local()
    @hug.delete("/models/{model_id}", requires=api_key_authentication)
    def delete(model_id: hug.types.text, moon_user_id=None):
        """Delete a model

        :param model_id: uuid of the model to delete
        :param moon_user_id: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_model
        """

        driver.ModelManager.delete_model(moon_user_id=moon_user_id, model_id=model_id)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_model_in_slaves(slaves=slaves, model_id=model_id)

        return {"result": True}

    @staticmethod
    @hug.local()
    @hug.patch("/models/{model_id}", requires=api_key_authentication)
    def patch(body: validate_input("name"), model_id: hug.types.text, moon_user_id=None):
        """Update a model

        :param body: body of the request
        :param model_id: uuid of the model to update
        :param moon_user_id: user ID who do the request
        :return: {
            "model_id1": {
                "name": "name of the model",
                "description": "... (optional)",
                "meta_rules": ["meta_rule_id1", ]
            }
        }
        :internal_api: update_model
        """
        data = driver.ModelManager.update_model(
            moon_user_id=moon_user_id, model_id=model_id, value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_model_in_slaves(slaves=slaves, model_id=model_id, is_delete=False,
                                   data=data[model_id])

        return {"models": data}


ModelsAPI = hug.API(name='models', doc=Models.__doc__)


@hug.object(name='models', version='1.0.0', api=ModelsAPI)
class ModelsCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id="", human: bool = False):
        """
        List models from the database
        :return: JSON status output
        """
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        _models_req = requests.get("{}/models".format(db_conf.get("url")),
                               headers={"x-api-key": manager_api_key}
                               )
        if _models_req.status_code == 200:
            if name_or_id:
                _models = None
                if name_or_id in _models_req.json().get("models"):
                    _models = _models_req.json().get("models").get(name_or_id)
                else:
                    for _models_key in _models_req.json().get("models"):
                        _name = _models_req.json().get("models").get(_models_key).get("name")
                        if _name == name_or_id:
                            _models = _models_req.json().get("models").get(_models_key)
                            name_or_id = _models_key
                            break
                if not _models:
                    raise Exception("Cannot find model with name or ID {}".format(name_or_id))
                else:
                    if human:
                        result = {"models": {name_or_id: _models}}
                    else:
                        result = {"models": [{name_or_id: _models}]}
            else:
               result = _models_req.json()

            if human:
                return ModelsCLI.human_display(result)
            else:
                return result
        LOGGER.error('Cannot list Models {}'.format(_models_req.status_code))


    @staticmethod
    @hug.object.cli
    def add(name, meta_rule, description="", human: bool = False):
        """
        Add model in the database
        :return: JSON status output
        """
        from moon_manager.api import meta_rules

        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()

        _meta_rules = meta_rules.MetaRules.get()["meta_rules"]
        _meta_rules_by_name = {_meta_rules[i]["name"]: i for i in _meta_rules}

        if meta_rule in _meta_rules_by_name:
            meta_rule_id = _meta_rules_by_name[meta_rule]
        elif meta_rule in _meta_rules:
            meta_rule_id = meta_rule
        else:
            raise Exception("Cannot find meta_rule with name or ID {}".format(meta_rule))

        _models = requests.post(
            "{}/models".format(db_conf.get("url")),
            json={
                "name": name,
                "description": description,
                "meta_rules": [meta_rule_id]
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _models.status_code == 200:
            LOGGER.warning('Create {}'.format(_models.content))
            if human:
                return ModelsCLI.human_display(_models.json())
            else:
                return _models.json()
        LOGGER.error('Cannot create {}'.format(name, _models.content))

    @staticmethod
    @hug.object.cli
    def delete(name='default'):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = connect_from_env()
        _models = ModelsCLI.list()
        for _slave_id, _slave_value in _models.get("models").items():
            if _slave_value.get("name") == name:
                req = requests.delete(
                    "{}/models/{}".format(db_conf.get("url"), _slave_id),
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find model with name {}".format(name))
            return
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name))
            return True
        LOGGER.error("Cannot delete model with name {}".format(name))

    @staticmethod
    def human_display(models_json):
        human_result = "Models"
        for model in models_json.get("models"):
            human_result += "\n" + models_json.get("models").get(model).get("name") + " : \n"
            human_result += "\tname : " + models_json.get("models").get(model).get("name") + "\n"
            human_result += "\tid : " + model + "\n"
            human_result += "\tdescription : " + models_json.get("models").get(model).get("description") + "\n"
            human_result += "\tmeta_rules : \n"
            for meta_rule in models_json.get("models").get(model).get("meta_rules"):
                human_result += "\t\tid : " + meta_rule + "\n"
        return human_result
