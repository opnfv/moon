# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from behave import *
from Static_Variables import GeneralVariables
from astropy.table import Table
from common_functions import *
import requests
import json
import logging

apis_urls = GeneralVariables()
commonfunctions = commonfunctions()

logger = logging.getLogger(__name__)

# Step Definition Implementation:
# 1) Get all the existing pdps in the system
# 2) Loop by id and delete them
@Given('the system has no pdps')
def step_impl(context):
    logger.info("Given the system has no pdps")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response = requests.get(apis_urls.serverURL + apis_urls.pdpAPI, headers=apis_urls.auth_headers)
    pdpjason=apis_urls.pdpAPI+"s"
    if len(response.json()[pdpjason]) != 0:
        for ids in dict(response.json()[pdpjason]).keys():
            response = requests.delete(apis_urls.serverURL + apis_urls.pdpAPI + "/" + ids,
                                       headers=headers)

# Step Definition Implementation:
# 1) Get model id by calling the common funtion: get_policyid
# 2) create the pdp data jason then post it
@Given('the following pdp exists')
def step_impl(context):
    logger.info("Given the following pdp exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "pdp name: '" + row["pdpname"] + "' pdp description: '" + row[
                "pdpdescription"] + "' and keystone project:'" + row[
                "keystone_project_id"] + "' and security pipeline '" + row['security_pipeline'] + "'")
        policies_list = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['security_pipeline']) > 25):
            policies_list = row['security_pipeline']
        else:
            for policy in row["security_pipeline"].split(","):
                policies_list.append(commonfunctions.get_policyid(policy))

        data = {
            'name': row["pdpname"],
            'description': row["pdpdescription"],
            'vim_project_id': row['keystone_project_id'],
            'security_pipeline': policies_list
        }
        response = requests.post(apis_urls.serverURL + apis_urls.pdpAPI, headers=headers,
                                 data=json.dumps(data))

# Step Definition Implementation:
# 1) Get policy id by calling the common funtion: get_policyid
# 2) create the pdp jason then patch the policy after searching for it's id.
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following pdp')
def step_impl(context):
    logger.info("When the user sets to add the following pdp")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "pdp name: '" + row["pdpname"] + "' pdp description: '" + row[
                "pdpdescription"] + "' and keystone project:'" + row[
                "keystone_project_id"] + "' and security pipeline '" + row['security_pipeline'] + "'")

        policies_list = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
        if (row["security_pipeline"] != ""):
            if (len(row['security_pipeline']) > 25):
                policies_list = row['security_pipeline']
            else:
                for policy in row["security_pipeline"].split(","):
                    policies_list.append(commonfunctions.get_policyid(policy))
                data = {
                    'name': row["pdpname"],
                    'description': row["pdpdescription"],
                    'vim_project_id': row['keystone_project_id'],
                    'security_pipeline': policies_list
                }
        else:
            data = {
                'name': row["pdpname"],
                'description': row["pdpdescription"],
                'vim_project_id': row['keystone_project_id'],
                'security_pipeline': ""
            }
        response = requests.post(apis_urls.serverURL + apis_urls.pdpAPI, headers=headers,
                                 data=json.dumps(data))

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get model id by calling the common funtion: get_policyid
# 2) create the pdp data jason then patch it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to update the following pdp')
def step_impl(context):
    logger.info("When the user sets to update the following pdp")

    model = getattr(context, "model", None)
    policies_list=[]
    for row in context.table:
        logger.info(
            "pdp name: '" + row["pdpname"] + "' which will be updated to pdp name:" + row[
                "updatedpdpname"] + "' and pdp description: '" + row[
                "updatedpdpdescription"] + "' keystone_project: '" + row["updatedkeystone_project_id"] + "' security pipeline: '"+row["updatedsecurity_pipeline"]+"'")

        policies_list = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['updatedsecurity_pipeline']) > 25):
            policies_list = row['updatedsecurity_pipeline']
        else:
            for policy in row["updatedsecurity_pipeline"].split(","):
                policies_list.append(commonfunctions.get_policyid(policy))

        data = {
            'name': row["updatedpdpname"],
            'description': row["updatedpdpdescription"],
            'vim_project_id': row['updatedkeystone_project_id'],
            'security_pipeline': policies_list
        }

        response = requests.get(apis_urls.serverURL + apis_urls.pdpAPI,headers=apis_urls.auth_headers)
        logger.info(response.json())
        pdpjason = apis_urls.pdpAPI + "s"
        for ids in dict(response.json()[pdpjason]).keys():
            logger.info(str(response.json()[pdpjason][ids]['name']))
            if (response.json()[pdpjason][ids]['name'] == row["pdpname"]):
                logger.info(apis_urls.serverURL + apis_urls.pdpAPI+ '/' + ids)
                response = requests.patch(apis_urls.serverURL + apis_urls.pdpAPI+ '/' + ids, headers=headers,
                                          data=json.dumps(data))
                logger.info(response.json())

                if response.status_code==200:
                    GeneralVariables.api_responseflag['value'] = 'True'
                else:
                    GeneralVariables.api_responseflag['value'] = 'False'
                break

# Step Definition Implementation:
# 1) Get all the pdps by get request
# 2) Loop by ids and search for the matching pdp by name and delete it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following pdp')
def step_impl(context):
    logging.info("When the user sets to delete the following pdp")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        logger.info("pdp name:'" + row["pdpname"] + "'")

        response = requests.get(apis_urls.serverURL + apis_urls.pdpAPI,headers=apis_urls.auth_headers)
        pdpjason=apis_urls.pdpAPI+"s"
        for ids in dict(response.json()[pdpjason]).keys():
            if (response.json()[pdpjason][ids]['name'] == row["pdpname"]):
                response = requests.delete(apis_urls.serverURL + apis_urls.pdpAPI + "/" + ids,
                                           headers=headers)

    if response.status_code==200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the existing pdps by get request and put them into a table
# 2) Sort the table by pdp name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following pdp should be existed in the system')
def step_impl(context):
    logger.info("Then the following pdp should be existed in the system")

    response = requests.get(apis_urls.serverURL + apis_urls.pdpAPI,headers=apis_urls.auth_headers)
    apiresult = Table(
        names=('pdpname', 'pdpdescription', 'keystone_project_id','security_pipeline'),
        dtype=('S10', 'S100', 'S100','S100'))
    pdp_jason=apis_urls.pdpAPI+"s"
    if len(response.json()[pdp_jason]) != 0:
        for ids in dict(response.json()[pdp_jason]).keys():
            apipdppolicies = ""
            apipdpname = response.json()[pdp_jason][ids]['name']
            apipdpdescription = response.json()[pdp_jason][ids]['description']
            apipdpprojectid = response.json()[pdp_jason][ids]['vim_project_id']
            for policies in response.json()[pdp_jason][ids]['security_pipeline']:
                if(len(apipdppolicies)>2):
                    apipdppolicies = apipdppolicies +','+ commonfunctions.get_policyname(policies)
                else:
                    apipdppolicies=commonfunctions.get_policyname(policies)

            apiresult.add_row(vals=(
                apipdpname, apipdpdescription, apipdpprojectid,apipdppolicies))

    else:
        apiresult.add_row(vals=("", "", "",""))

    apiresult.sort('pdpname')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected pdp name: '" + str(
            row1["pdpname"]) + "' is the same as the actual existing '" + str(
            row2["pdpname"]) + "'")
        assert str(row1["pdpname"]) == str(row2["pdpname"]), "pdp name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected pdp description: '" + str(
            row1["pdpdescription"]) + "' is the same as the actual existing '" + str(
            row2["pdpdescription"]) + "'")

        assert str(row1["pdpdescription"]) == str(row2["pdpdescription"]), "pdp description is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected keystone project id description: '" + str(
            row1["keystone_project_id"]) + "' is the same as the actual existing '" + str(
            row2["keystone_project_id"]) + "'")
        assert str(row1["keystone_project_id"]) == str(row2["keystone_project_id"]), "project id is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected security pipeline description: '" + str(
            row1["security_pipeline"]) + "' is the same as the actual existing '" + str(
            row2["security_pipeline"]) + "'")
        assert str(row1["security_pipeline"]) == str(row2["security_pipeline"]), "security_pipeline policies is not correct!"
        logger.info("assertion passed!")

