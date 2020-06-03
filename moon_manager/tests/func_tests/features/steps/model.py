# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from behave import *
from Static_Variables import GeneralVariables
from astropy.table import Table, Column
from common_functions import *
import requests
import json
import logging

apis_urls = GeneralVariables()
commonfunctions = commonfunctions()

logger = logging.getLogger(__name__)

# Step Definition Implementation:
# 1) Get all the existing models in the system
# 2) Loop by id and delete them
@Given('the system has no models')
def step_impl(context):
    logger.info("Given the system has no models")

    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response = requests.get(apis_urls.serverURL + apis_urls.modelAPI, headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.modelAPI]) != 0:
        for ids in dict(response.json()[apis_urls.modelAPI]).keys():
            response = requests.delete(apis_urls.serverURL + apis_urls.modelAPI + "/" + ids,
                                       headers=headers)

# Step Definition Implementation:
# 1) Get meta rule ids list by calling the common funtion: get_metaruleid
# 2) create the model data jason then post it
@Given('the following model exists')
def step_impl(context):
    logger.info("Given the following model exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "model name: '" + row["modelname"] + "' model description: '" + row[
                "modeldescription"] + "' and meta-rules:'" + row[
                "metarule"]+"'")

        metarulesids = []

        if (len(row["metarule"]) > 35):
            metarulesids.append(row["metarule"])
        else:
            for metarule in row["metarule"].split(","):
                metarulesids.append(commonfunctions.get_metaruleid(metarule))

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        data = {
            'name': row["modelname"],
            'description': row["modeldescription"],
            'meta_rules': metarulesids
        }
        response = requests.post(apis_urls.serverURL + apis_urls.modelAPI, headers=headers,
                                 data=json.dumps(data))


# Step Definition Implementation:
# 1) Get meta rule ids list by calling the common funtion: get_metaruleid
# 2) create the model data jason then post it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following model')
def step_impl(context):
    logger.info("When the user sets to add the following model")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "model name: '" + row["modelname"] + "' model description: '" + row[
                "modeldescription"] + "' and meta-rules:'" + row[
                "metarule"] + "'")

        metarules = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if(row["metarule"]!=""):
            if (len(row["metarule"]) > 35):
                metarules.append(row["metarule"])
            else:
                for metarule in row["metarule"].split(","):
                    metarules.append(commonfunctions.get_metaruleid(metarule))

            data = {
                'name': row["modelname"],
                'description': row["modeldescription"],
                'meta_rules': metarules,
            }
        else:
            data = {
                'name': row["modelname"],
                'description': row["modeldescription"],
                'meta_rules': "",
            }
        response = requests.post(apis_urls.serverURL + apis_urls.modelAPI, headers=headers,
                                 data=json.dumps(data))

        if response.status_code==200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'


# Step Definition Implementation:
# 1) Get meta rule ids list by calling the common funtion: get_modelid
# 2) create the model jason then patch the model after searching for it's id.
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to update the following model')
def step_impl(context):
    logging.info("When the user sets to update the following model")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "model name: '" + row["modelname"] + "' which will be updated to model name:" + row[
                "updatedmodelname"] + "' and model description: '" + row[
                "updatedmodeldescription"] + "' meta-rules: '"+row["updatedmetarule"] + "'")

        metarules = []
        data={}
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
        if(row["updatedmetarule"]!=""):
            if (len(row["updatedmetarule"]) > 35):
                metarules.append(row["updatedmetarule"])
            else:
                for metarule in row["updatedmetarule"].split(","):
                    metarules.append(commonfunctions.get_metaruleid(metarule))
                data = {
                'name': row["updatedmodelname"],
                'description': row["updatedmodeldescription"],
                'meta_rules': metarules,
                }
        else:
            data = {
                'name': row["updatedmodelname"],
                'description': row["updatedmodeldescription"],
                'meta_rules': "",
            }
        response = requests.get(apis_urls.serverURL + apis_urls.modelAPI, headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.modelAPI]).keys():
            if (response.json()[apis_urls.modelAPI][ids]['name'] == row["modelname"]):
               response = requests.patch(apis_urls.serverURL + apis_urls.modelAPI+'/'+ids, headers=headers,
                                         data=json.dumps(data))

    if response.status_code==200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the model by get request
# 2) Loop by ids and search for the matching model by name and delete it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following model')
def step_impl(context):
    logging.info("When the user sets to delete the following model")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info("model name: '" + row["modelname"] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        logger.info("policy name:'" + row["modelname"] + "'")
        response = requests.get(apis_urls.serverURL + apis_urls.modelAPI, headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.modelAPI]).keys():
            if (response.json()[apis_urls.modelAPI][ids]['name'] == row["modelname"]):
                response = requests.delete(apis_urls.serverURL + apis_urls.modelAPI + "/" + ids,
                                           headers=headers)
    if response.status_code==200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the existing models by get request and put them into a table
# 2) Sort the table by model name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following model should be existed in the system')
def step_impl(context):
    logger.info("Then the following model should be existed in the system")
    response = requests.get(apis_urls.serverURL + apis_urls.modelAPI, headers=apis_urls.auth_headers)
    apimetarulesname=""
    apiresult = Table(
        names=('modelname', 'modeldescription', 'metarule'),
        dtype=('S100', 'S100', 'S100'))
    if len(response.json()[apis_urls.modelAPI]) != 0:
        for ids in dict(response.json()[apis_urls.modelAPI]).keys():
            apimetarulesname = []
            apimodelname = response.json()[apis_urls.modelAPI][ids]['name']
            apimodeldescription = response.json()[apis_urls.modelAPI][ids]['description']
            for metaruleid in response.json()[apis_urls.modelAPI][ids]['meta_rules']:
                   apimetarulesname.append(commonfunctions.get_metarulename(metaruleid))
            apiresult.add_row(vals=(
                apimodelname, apimodeldescription, ",".join(apimetarulesname)))
    else:
        apiresult.add_row(vals=("", "", ""))

    apiresult.sort('modelname')

    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected model name: '" + str(
            row1["modelname"]) + "' is the same as the actual existing '" + str(
            row2["modelname"]) + "'")
        assert str(row1["modelname"]) == str(row2["modelname"]), "model name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected model description: '" + str(
            row1["modeldescription"]) + "' is the same as the actual existing '" + str(
            row2["modeldescription"]) + "'")
        assert str(row1["modeldescription"]) == str(row2["modeldescription"]), "model description is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected meta rules: '" + str(
            row1["metarule"]) + "' is the same as the actual existing '" + str(
            row2["metarule"]) + "'")
        assert str(row1["metarule"]) == str(row2["metarule"]), "metarule is not correct!"
        logger.info("assertion passed!")
