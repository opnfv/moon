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
# 1) Get all the existing policies in the system
# 2) Loop by id and delete them
@Given('the system has no policies')
def step_impl(context):
    logger.info("Given the system has no policies")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response = requests.get(apis_urls.serverURL + apis_urls.policyAPI, headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.policyAPI]) != 0:
        for ids in dict(response.json()[apis_urls.policyAPI]).keys():
            response = requests.delete(apis_urls.serverURL + apis_urls.policyAPI + "/" + ids,
                                       headers=headers)


# Step Definition Implementation:
# 1) Get model id by calling the common funtion: get_modelid
# 2) create the policy data jason then post it
@Given('the following policy exists')
def step_impl(context):
    logger.info("Given the following policy exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "policy name: '" + row["policyname"] + "' policy description: '" + row[
                "policydescription"] + "' and model name:'" + row[
                "modelname"] + "' and genre '"+row['genre']+"'")
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        data = {
            'name': row["policyname"],
            'description': row["policydescription"],
            'model_id': commonfunctions.get_modelid(row['modelname']),
            'genre': row['genre']
        }
        response = requests.post(apis_urls.serverURL + apis_urls.policyAPI, headers=headers,
                                 data=json.dumps(data))


# Step Definition Implementation:
# 1) Get model id by calling the common funtion: get_modelid
# 2) create the policy data jason then post it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following policy')
def step_impl(context):
    logger.info("When the user sets to add the following policy")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "policy name: '" + row["policyname"] + "' policy description: '" + row[
                "policydescription"] + "' and model name:'" + row[
                "modelname"] + "' and genre '" + row['genre'] + "'")
        policymodel = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['modelname']) > 20):
            policymodel=row['modelname']
        else:
            policymodel=commonfunctions.get_modelid(row['modelname'])

        data = {
            'name': row["policyname"],
            'description': row["policydescription"],
            'model_id': policymodel,
            'genre': row['genre']
        }
        response = requests.post(apis_urls.serverURL + apis_urls.policyAPI, headers=headers,
                                 data=json.dumps(data))

        if response.status_code==200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'


# Step Definition Implementation:
# 1) Get model id by calling the common funtion: get_modelid
# 2) create the policy jason then patch the policy after searching for it's id.
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to update the following policy')
def step_impl(context):
    logger.info("When the user sets to update the following policy")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "policy name: '" + row["policyname"] + "' which will be updated to policy name:" + row[
                "updatedpolicyname"] + "' and policy description: '" + row[
                "updatedpolicydescription"] + "' model name: '" + row["updatedmodelname"] + "' and genre: '"+row["updatedgenre"]+"'")
        policymodel = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['updatedmodelname']) > 20):
            policymodel = row['updatedmodelname']
        else:
            policymodel = commonfunctions.get_modelid(row['updatedmodelname'])

        data = {
            'name': row["updatedpolicyname"],
            'description': row["updatedpolicydescription"],
            'model_id': policymodel,
            'genre': row['updatedgenre']
        }
        response = requests.get(apis_urls.serverURL + apis_urls.policyAPI, headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.policyAPI]).keys():
            if (response.json()[apis_urls.policyAPI][ids]['name'] == row["policyname"]):
                print(apis_urls.serverURL + apis_urls.policyAPI + '/' + ids)
                response = requests.patch(apis_urls.serverURL + apis_urls.policyAPI + '/' + ids, headers=headers,
                                          data=json.dumps(data))
                logger.info(response.json())
                logger.info(response.status_code)
                break
    if response.status_code==200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the policy by get request
# 2) Loop by ids and search for the matching policy by name and delete it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following policy')
def step_impl(context):
    logger.info("When the user sets to delete the following policy")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        logger.info("policy name:'" +row["policyname"]+"'")
        response = requests.get(apis_urls.serverURL + apis_urls.policyAPI, headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.policyAPI]).keys():
            if (response.json()[apis_urls.policyAPI][ids]['name'] == row["policyname"]):
                GeneralVariables.assignpolicyid['value']=ids
                response = requests.delete(apis_urls.serverURL + apis_urls.policyAPI + "/" + ids,
                                           headers=headers)
                break

    if response.status_code==200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the existing policies by get request and put them into a table
# 2) Sort the table by policy name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following policy should be existed in the system')
def step_impl(context):
    logger.info("Then the following policy should be existed in the system")
    response = requests.get(apis_urls.serverURL + apis_urls.policyAPI, headers=apis_urls.auth_headers)
    #print(response)
    apiresult = Table(
        names=('policyname', 'policydescription', 'modelname','genre'),
        dtype=('S100', 'S100', 'S100','S100'))
    if len(response.json()[apis_urls.policyAPI]) != 0:
        for ids in dict(response.json()[apis_urls.policyAPI]).keys():
            apipolicyname = response.json()[apis_urls.policyAPI][ids]['name']
            apipolicydescription = response.json()[apis_urls.policyAPI][ids]['description']
            apipolicymodel = commonfunctions.get_modelname(response.json()[apis_urls.policyAPI][ids]['model_id'])
            apipolicygenre=response.json()[apis_urls.policyAPI][ids]['genre']

            apiresult.add_row(vals=(
                apipolicyname, apipolicydescription, apipolicymodel,apipolicygenre))

    else:
        apiresult.add_row(vals=("", "", "",""))

    apiresult.sort('policyname')

    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected policy name: '" + str(
            row1["policyname"]) + "' is the same as the actual existing '" + str(
            row2["policyname"]) + "'")
        assert str(row1["policyname"]) == str(row2["policyname"]), "policy name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected policy description: '" + str(
            row1["policydescription"]) + "' is the same as the actual existing '" + str(
            row2["policydescription"]) + "'")
        assert str(row1["policydescription"]) == str(row2["policydescription"]), "policy description is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected genre: '" + str(
            row1["genre"]) + "' is the same as the actual existing '" + str(
            row2["genre"]) + "'")
        assert str(row1["genre"]) == str(row2["genre"]), "genre is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected model name: '" + str(
            row1["modelname"]) + "' is the same as the actual existing '" + str(
            row2["modelname"]) + "'")
        assert str(row1["modelname"]) == str(row2["modelname"]), "model name is not correct!"
        logger.info("assertion passed!")