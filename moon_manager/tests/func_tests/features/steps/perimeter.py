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
# 1) Get all the existing subject preimeters in the system
# 2) Loop by id to unlink the policies attached
# 3) Then delete the perimeter itself
@Given('the system has no subject perimeter')
def step_impl(context):
    logger.info("Given the system has no subject perimeter")
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
    response = requests.get(apis_urls.serverURL + apis_urls.perimetersubjectAPI,headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.perimetersubjectAPI]) != 0:
        for ids in dict(response.json()[apis_urls.perimetersubjectAPI]).keys():
            policies_list = response.json()[apis_urls.perimetersubjectAPI][ids]['policy_list']
            for policy in policies_list:
                response_delete_policies = requests.delete(
                    apis_urls.serverURL + "policies/" + policy + "/" + apis_urls.perimetersubjectAPI + "/" + ids,
                    headers=apis_urls.auth_headers)
            response_delete = requests.delete(apis_urls.serverURL + apis_urls.perimetersubjectAPI + "/" + ids,
                                              headers=apis_urls.auth_headers)

    # exit(0)

# Step Definition Implementation:
# 1) Post subject perimeter using the policy id
@Given('the following subject perimeter exists')
def step_impl(context):
    logger.info("Given the following subject perimeter exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "subject perimeter name: '" + row["subjectperimetername"] + "' subject perimeter description: '" + row[
                "subjectperimeterdescription"]  # "' and subject perimeter email:'" + row[
            # "subjectperimeteremail"] + "' and subject perimeter password '" + row['subjectperimeterpassword']
            + "' and policies '" + row['policies'] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        policyid=""
        if (row['policies'] != ""):
            policyid = commonfunctions.get_policyid(row['policies'])
        data = {
            'name': row["subjectperimetername"],
            'description': row["subjectperimeterdescription"],
            # 'email': row['subjectperimeteremail'],
            # 'password': row['subjectperimeterpassword'],

        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimetersubjectAPI, headers=headers,
            data=json.dumps(data))

# Step Definition Implementation:
# 1) Get all the existing object preimeters in the system
# 2) Loop by id to unlink the policies attached
# 3) Then delete the perimeter itself
@Given('the system has no object perimeter')
def step_impl(context):
    logger.info("Given the system has no object perimeter")
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
    response = requests.get(apis_urls.serverURL + apis_urls.perimeterobjectAPI,headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.perimeterobjectAPI]) != 0:
        for ids in dict(response.json()[apis_urls.perimeterobjectAPI]).keys():
            policies_list = response.json()[apis_urls.perimeterobjectAPI][ids]['policy_list']
            for policy in policies_list:
                response_delete_policies = requests.delete(
                    apis_urls.serverURL + "policies/" + policy + "/" + apis_urls.perimeterobjectAPI + "/" + ids,
                    headers=headers)
            response_delete = requests.delete(apis_urls.serverURL + apis_urls.perimeterobjectAPI + "/" + ids,
                                              headers=apis_urls.auth_headers)

# Step Definition Implementation:
# 1) Post object perimeter using the policy id
@Given('the following object perimeter exists')
def step_impl(context):
    logger.info("Given the following object perimeter exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "object perimeter name: '" + row["objectperimetername"] + "' object perimeter description: '" + row[
                "objectperimeterdescription"] + "' and policies '" + row['policies'] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
        if (row['policies'] != ""):
            policyid = commonfunctions.get_policyid(row['policies'])

        data = {
            'name': row["objectperimetername"],
            'description': row["objectperimeterdescription"],

        }
        response = requests.post(apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimeterobjectAPI,
                                 headers=headers,
                                 data=json.dumps(data))

# Step Definition Implementation:
# 1) Get all the existing action preimeters in the system
# 2) Loop by id to unlink the policies attached
# 3) Then delete the perimeter itself
@Given('the system has no action perimeter')
def step_impl(context):
    logger.info("Given the system has no action perimeter")
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response = requests.get(apis_urls.serverURL + apis_urls.perimeteractionAPI,headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.perimeteractionAPI]) != 0:
        for ids in dict(response.json()[apis_urls.perimeteractionAPI]).keys():
            policies_list = response.json()[apis_urls.perimeteractionAPI][ids]['policy_list']
            for policy in policies_list:
                response_delete_policies = requests.delete(
                    apis_urls.serverURL + "policies/" + policy + "/" + apis_urls.perimeteractionAPI + "/" + ids,
                    headers=headers)
            response_delete = requests.delete(apis_urls.serverURL + apis_urls.perimeteractionAPI + "/" + ids,
                                              headers=apis_urls.auth_headers)


# Step Definition Implementation:
# 1) Post action perimeter using the policy id
@Given('the following action perimeter exists')
def step_impl(context):
    logger.info("Given the following action perimeter exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "action perimeter name: '" + row["actionperimetername"] + "' action perimeter description: '" + row[
                "actionperimeterdescription"] + "' and policies '" + row['policies'] + "'")

        policyid=""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policies'] != ""):
            policyid = commonfunctions.get_policyid(row['policies'])
        data = {
            'name': row["actionperimetername"],
            'description': row["actionperimeterdescription"],

        }
        response = requests.post(apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimeteractionAPI,
                                 headers=headers,
                                 data=json.dumps(data))

# Step Definition Implementation:
# 1) Insert subject perimeter using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following subject perimeter')
def step_impl(context):
    logger.info("When the user sets to add the following subject perimeter")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "subject perimeter name: '" + row["subjectperimetername"] + "' subject perimeter description: '" + row[
                "subjectperimeterdescription"] +
            # "' and subject perimeter email:'" + row["subjectperimeteremail"] + "' and subject perimeter password '" + row['subjectperimeterpassword'] +
            "' and policies '" + row['policies'] + "'")

        policyid = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policies'] != ""):
            policyid = commonfunctions.get_policyid(row['policies'])
        data = {
                'name': row["subjectperimetername"],
                'description': row["subjectperimeterdescription"],
                # 'email': row['subjectperimeteremail'],
                # 'password': row['subjectperimeterpassword'],
        }
        response = requests.post(apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimetersubjectAPI, headers=headers,
                                     data=json.dumps(data))

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Search for the existing subject perimeter & get its id
# 2) create the new perimeter jason and patch it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to update the following subject perimeter')
def step_impl(context):
    logger.info("When the user sets to update the following subject perimeter")
    model = getattr(context, "model", None)
    policies_list = []
    for row in context.table:
        logger.info(
            "subject perimeter name: '" + row[
                'subjectperimetername'] + "' which will be updated to subject perimeter name:'" + row[
                "updatedsubjectperimetername"] + "' subject perimeter description: '" + row[
                "updatedsubjectperimeterdescription"] +
            # "' and subject perimeter email:'" + row["updatedsubjectperimeteremail"] + "' and subject perimeter password '" + row['updatedsubjectperimeterpassword']
            "' and policies '" + row['policies'] + "'")

        policyid = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policies'] != ""):
            policyid=commonfunctions.get_policyid(row['policies'])
        else:
            policyid=""
        data = {
                'name': row["updatedsubjectperimetername"],
                'description': row["updatedsubjectperimeterdescription"],
                # 'email': row['subjectperimeteremail'],
                # 'password': row['subjectperimeterpassword'],
        }
        response = requests.get(apis_urls.serverURL + apis_urls.perimetersubjectAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.perimetersubjectAPI]).keys():
            if (response.json()[apis_urls.perimetersubjectAPI][ids]['name'] == row["subjectperimetername"]):
                #print(apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimetersubjectAPI + '/' + ids)
                response = requests.patch(apis_urls.serverURL + apis_urls.perimetersubjectAPI + '/' + ids,
                    headers=headers,data=json.dumps(data))
                print(response)

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Search for the existing subject perimeter & get its id
# 2) Delete it without having the policy id in the request
@When('the user sets to delete the following subject perimeter')
def step_impl(context):
    logging.info("When the user sets to delete the following subject perimeter")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {
            'Content-Type': 'application/json',
        }
        logger.info("subject perimeter name:'" + row["subjectperimetername"] + "'")
        response = requests.get(apis_urls.serverURL + apis_urls.perimetersubjectAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.perimetersubjectAPI]).keys():
            if (response.json()[apis_urls.perimetersubjectAPI][ids]['name'] == row["subjectperimetername"]):
                response = requests.delete(apis_urls.serverURL + apis_urls.perimetersubjectAPI + "/" + ids,
                                           headers=apis_urls.auth_headers)

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Search for the existing subject perimeter & get its id
# 2) Delete it while having the policy id in the request
@When('the user sets to delete the following subject perimeter for a given policy')
def step_impl(context):
    logging.info("the user sets to delete the following subject perimeter for a given policy")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {
            'Content-Type': 'application/json',
        }
        logger.info("subject perimeter name:'" + row["subjectperimetername"] + "' and policy:"+ row["policies"]+"'")
        policyid = commonfunctions.get_policyid(row['policies'])
        response = requests.get(apis_urls.serverURL + apis_urls.perimetersubjectAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.perimetersubjectAPI]).keys():
            if (response.json()[apis_urls.perimetersubjectAPI][ids]['name'] == row["subjectperimetername"]):
                response = requests.delete(apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimetersubjectAPI + "/" + ids,
                                           headers=apis_urls.auth_headers)
            logger.info(response.json())
    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Insert object perimeter using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following object perimeter')
def step_impl(context):
    logger.info("When the user sets to add the following object perimeter")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "object perimeter name: '" + row["objectperimetername"] + "' object perimeter description: '" + row[
                "objectperimeterdescription"] + "' and policies '" + row['policies'] + "'")

        policies_list = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policies'] != ""):
            policyid = commonfunctions.get_policyid(row['policies'])
        else:
            policyid=""
        data = {
                'name': row["objectperimetername"],
                'description': row["objectperimeterdescription"],
        }
        response = requests.post(apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimeterobjectAPI, headers=headers,
                                     data=json.dumps(data))

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Search for the existing object perimeter & get its id
# 2) create the new perimeter jason and patch it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to update the following object perimeter')
def step_impl(context):
    logger.info("When the user sets to update the following object perimeter")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "object perimeter name: '" + row[
                'objectperimetername'] + "' which will be updated to object perimeter name:" + row[
                "updatedobjectperimetername"] + "' object perimeter description: '" + row[
                "updatedobjectperimeterdescription"] + "' and policies '" + row['policies'] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policies'] != ""):
            policyid = commonfunctions.get_policyid(row['policies'])
        else:
            policyid=""
        data = {
                'name': row["updatedobjectperimetername"],
                'description': row["updatedobjectperimeterdescription"],
            }
        response = requests.get(apis_urls.serverURL + apis_urls.perimeterobjectAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.perimeterobjectAPI]).keys():
            if (response.json()[apis_urls.perimeterobjectAPI][ids]['name'] == row["objectperimetername"]):
                response = requests.patch(apis_urls.serverURL + apis_urls.perimeterobjectAPI + '/' + ids,
                                          headers=headers,data=json.dumps(data))

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Search for the existing object perimeter & get its id
# 2) Delete it without having the policy id in the request
@When('the user sets to delete the following object perimeter')
def step_impl(context):
    logging.info("When the user sets to delete the following object perimeter")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        logger.info("object perimeter name:'" + row["objectperimetername"] + "'")

        response = requests.get(apis_urls.serverURL + apis_urls.perimeterobjectAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.perimeterobjectAPI]).keys():
            if (response.json()[apis_urls.perimeterobjectAPI][ids]['name'] == row["objectperimetername"]):
                response = requests.delete(apis_urls.serverURL + apis_urls.perimeterobjectAPI + "/" + ids,
                                           headers=apis_urls.auth_headers)

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Search for the existing object perimeter & get its id
# 2) Delete it while having the policy id in the request
@When('the user sets to delete the following object perimeter for a given policy')
def step_impl(context):
    logging.info("the user sets to delete the following object perimeter for a given policy")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        logger.info("object perimeter name:'" + row["objectperimetername"] + "' and policy:"+ row["policies"]+"'")
        policyid = commonfunctions.get_policyid(row['policies'])
        response = requests.get(apis_urls.serverURL + apis_urls.perimeterobjectAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.perimeterobjectAPI]).keys():
            if (response.json()[apis_urls.perimeterobjectAPI][ids]['name'] == row["objectperimetername"]):
                response = requests.delete(apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimeterobjectAPI + "/" + ids,
                                           headers=apis_urls.auth_headers)

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Insert action perimeter using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following action perimeter')
def step_impl(context):
    logger.info("When the user sets to add the following action perimeter")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "action perimeter name: '" + row["actionperimetername"] + "' action perimeter description: '" + row[
                "actionperimeterdescription"] + "' and policies '" + row['policies'] + "'")

        policyid=""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policies'] != ""):
            policyid = commonfunctions.get_policyid(row['policies'])
        else:
            policyid=""
        data = {
                'name': row["actionperimetername"],
                'description': row["actionperimeterdescription"],

        }
        response = requests.post(
                apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimeteractionAPI, headers=headers,
                data=json.dumps(data))

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Search for the existing action perimeter & get its id
# 2) create the new perimeter jason and patch it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to update the following action perimeter')
def step_impl(context):
    logger.info("When the user sets to update the following action perimeter")

    model = getattr(context, "model", None)

    for row in context.table:

        logger.info(
            "action perimeter name: '" + row[
                'actionperimetername'] + "' which will be updated to action perimeter name:" + row[
                "updatedactionperimetername"] + "' action perimeter description: '" + row[
                "updatedactionperimeterdescription"] + "' and policies '" + row['policies'] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policies'] != ""):
            policyid = commonfunctions.get_policyid(row['policies'])
        else:
            policyid=""
        data = {
                'name': row["updatedactionperimetername"],
                'description': row["updatedactionperimeterdescription"],
            }
        response = requests.get(apis_urls.serverURL + apis_urls.perimeteractionAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.perimeteractionAPI]).keys():
            if (response.json()[apis_urls.perimeteractionAPI][ids]['name'] == row["actionperimetername"]):
                response = requests.patch(
                    apis_urls.serverURL +  apis_urls.perimeteractionAPI + '/' + ids,
                    headers=headers,data=json.dumps(data))

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Search for the existing action perimeter & get its id
# 2) Delete it without having the policy id in the request
@When('the user sets to delete the following action perimeter')
def step_impl(context):
    logging.info("When the user sets to delete the following action perimeter")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        logger.info("action perimeter name:'" + row["actionperimetername"] + "'")
        response = requests.get(apis_urls.serverURL + apis_urls.perimeteractionAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.perimeteractionAPI]).keys():
            if (response.json()[apis_urls.perimeteractionAPI][ids]['name'] == row["actionperimetername"]):
                response = requests.delete(apis_urls.serverURL + apis_urls.perimeteractionAPI + "/" + ids,
                                           headers=apis_urls.auth_headers)
    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Search for the existing action perimeter & get its id
# 2) Delete it while having the policy id in the request
@When('the user sets to delete the following action perimeter for a given policy')
def step_impl(context):
    logging.info("the user sets to delete the following action perimeter for a given policy")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        logger.info("action perimeter name:'" + row["actionperimetername"] + "' and policy:"+ row["policies"]+"'")
        policyid = commonfunctions.get_policyid(row['policies'])
        response = requests.get(apis_urls.serverURL + apis_urls.perimeteractionAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.perimeteractionAPI]).keys():
            if (response.json()[apis_urls.perimeteractionAPI][ids]['name'] == row["actionperimetername"]):
                response = requests.delete(apis_urls.serverURL + "policies/" + policyid + "/" + apis_urls.perimeteractionAPI + "/" + ids,
                                           headers=apis_urls.auth_headers)

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the existing subject perimeter by get request and put them into a table
# 2) Sort the table by subject perimeter
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following subject perimeter should be existed in the system')
def step_impl(context):
    logger.info("Then the following subject perimeter should be existed in the system")

    response = requests.get(apis_urls.serverURL + apis_urls.perimetersubjectAPI,headers=apis_urls.auth_headers)
    apiresult = Table(
        names=('subjectperimetername', 'subjectperimeterdescription',
               # 'subjectperimeteremail',
               # 'subjectperimeterpassword',
               'policies'),
        dtype=('S100', 'S100', 'S100'))

    if len(response.json()[apis_urls.perimetersubjectAPI]) != 0:
        for ids in dict(response.json()[apis_urls.perimetersubjectAPI]).keys():
            apipoliciesid = []
            apipolicies = ""
            GeneralVariables.assignsubjectperimeterid['value']=ids
            apisubjectperimetername = response.json()[apis_urls.perimetersubjectAPI][ids]['name']
            apisubjectperimeterdescription = response.json()[apis_urls.perimetersubjectAPI][ids]['description']
            # apisubjectperimeteremail = response.json()[apis_urls.perimetersubjectAPI][ids]['email']
            # apisubjectperimeterpassword = response.json()[apis_urls.perimetersubjectAPI][ids]['password']
            if (len(response.json()[apis_urls.perimetersubjectAPI][ids]['policy_list']) != 0):
                for policies in response.json()[apis_urls.perimetersubjectAPI][ids]['policy_list']:
                    apipoliciesid.append(commonfunctions.get_policyname(str(policies)))
                apipolicies = ",".join(apipoliciesid)
            else:
                apipolicies = ""
            apiresult.add_row(vals=(
                apisubjectperimetername, apisubjectperimeterdescription,
                # apisubjectperimeteremail,# apisubjectperimeterpassword,
                apipolicies))
    else:
        apiresult.add_row(vals=("", "", ""))

    apiresult.sort('subjectperimetername')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected subject perimeter name: '" + str(
            row1["subjectperimetername"]) + "' is the same as the actual existing '" + str(
            row2["subjectperimetername"]) + "'")
        assert str(row1["subjectperimetername"]) == str(
            row2["subjectperimetername"]), "subject perimeter name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected subject perimeter description: '" + str(
            row1["subjectperimeterdescription"]) + "' is the same as the actual existing '" + str(
            row2["subjectperimeterdescription"]) + "'")
        assert str(row1["subjectperimeterdescription"]) == str(
            row2["subjectperimeterdescription"]), "subject perimeter description is not correct!"
        logger.info("assertion passed!")

        # logger.info("asserting the expected subject perimeter email: '" + str(
        #     row1["subjectperimeteremail"]) + "' is the same as the actual existing '" + str(
        #     row2["subjectperimeteremail"]) + "'")
        # assert str(row1["subjectperimeteremail"]) == str(
        #     row2["subjectperimeteremail"]), "subject perimeter email is not correct!"
        # logger.info("assertion passed!")
        #
        # logger.info("asserting the expected subject perimeter password: '" + str(
        #     row1["subjectperimeterpassword"]) + "' is the same as the actual existing '" + str(
        #     row2["subjectperimeterpassword"]) + "'")
        # assert str(row1["subjectperimeterpassword"]) == str(
        #     row2["subjectperimeterpassword"]), "subject perimeter password is not correct!"
        # logger.info("assertion passed!")

        if (str(row1["policies"]).find(',') == -1):
            logger.info("asserting the expected policies: '" + str(
                row1["policies"]) + "' is the same as the actual existing '" + str(
                row2["policies"]) + "'")
            logger.info("policies is not correct!")
            assert str(row1["policies"]) == str(row2["policies"]), " policies is not correct!"
        else:

            logger.info("asserting the expected policies: '" + ','.join(
                sorted(str(row1["policies"]).split(','), key=str.lower)) + "' is the same as the actual existing '" +
                        ','.join(sorted(str(row2["policies"]).split(','), key=str.lower)) + "'")
            logger.info("policies is not correct!")
            assert ','.join(sorted(str(row1["policies"]).split(','), key=str.lower)) == ','.join(
                sorted(str(row2["policies"]).split(','), key=str.lower)), " policies is not correct!"
        logger.info("assertion passed!")

# Step Definition Implementation:
# 1) Get all the existing object perimeter by get request and put them into a table
# 2) Sort the table by subject perimeter
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following object perimeter should be existed in the system')
def step_impl(context):
    logger.info("Then the following object perimeter should be existed in the system")
    response = requests.get(apis_urls.serverURL + apis_urls.perimeterobjectAPI,headers=apis_urls.auth_headers)
    apiresult = Table(
        names=('objectperimetername', 'objectperimeterdescription', 'policies'),
        dtype=('S100', 'S100', 'S100'))
    if len(response.json()[apis_urls.perimeterobjectAPI]) != 0:
        for ids in dict(response.json()[apis_urls.perimeterobjectAPI]).keys():
            apipolicies = ""
            apipoliciesid = []
            apiobjectperimetername = response.json()[apis_urls.perimeterobjectAPI][ids]['name']
            apiobjectperimeterdescription = response.json()[apis_urls.perimeterobjectAPI][ids]['description']
            if (len(response.json()[apis_urls.perimeterobjectAPI][ids]['policy_list']) != 0):
                for policies in response.json()[apis_urls.perimeterobjectAPI][ids]['policy_list']:
                    apipoliciesid.append(commonfunctions.get_policyname(str(policies)))
                apipolicies = ",".join(apipoliciesid)
            else:
                apipolicies = ""
            apiresult.add_row(vals=(
                apiobjectperimetername, apiobjectperimeterdescription, apipolicies))
    else:
        apiresult.add_row(vals=("", "", ""))

    apiresult.sort('objectperimetername')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected object perimeter name: '" + str(
            row1["objectperimetername"]) + "' is the same as the actual existing '" + str(
            row2["objectperimetername"]) + "'")
        assert str(row1["objectperimetername"]) == str(
            row2["objectperimetername"]), "object perimeter name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected object perimeter description: '" + str(
            row1["objectperimeterdescription"]) + "' is the same as the actual existing '" + str(
            row2["objectperimeterdescription"]) + "'")
        assert str(row1["objectperimeterdescription"]) == str(
            row2["objectperimeterdescription"]), "object perimeter description is not correct!"
        logger.info("assertion passed!")

        if (str(row1["policies"]).find(',') == -1):
            logger.info("asserting the expected policies: '" + str(
                row1["policies"]) + "' is the same as the actual existing '" + str(
                row2["policies"]) + "'")
            logger.info("policies is not correct!")
            assert str(row1["policies"]) == str(row2["policies"]), " policies is not correct!"
        else:
            logger.info("asserting the expected policies: '" + ','.join(
                sorted(str(row1["policies"]).split(','), key=str.lower)) + "' is the same as the actual existing '" +
                        ','.join(sorted(str(row2["policies"]).split(','), key=str.lower)) + "'")
            logger.info("policies is not correct!")
            assert ','.join(sorted(str(row1["policies"]).split(','), key=str.lower)) == ','.join(
                sorted(str(row2["policies"]).split(','), key=str.lower)), " policies is not correct!"
        logger.info("assertion passed!")

# Step Definition Implementation:
# 1) Get all the existing subject perimeter by get request and put them into a table
# 2) Sort the table by subject perimeter
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following action perimeter should be existed in the system')
def step_impl(context):
    logger.info("Then the following action perimeter should be existed in the system")
    response = requests.get(apis_urls.serverURL + apis_urls.perimeteractionAPI,headers=apis_urls.auth_headers)
    apiresult = Table(
        names=('actionperimetername', 'actionperimeterdescription', 'policies'),
        dtype=('S100', 'S100', 'S100'))
    if len(response.json()[apis_urls.perimeteractionAPI]) != 0:
        for ids in dict(response.json()[apis_urls.perimeteractionAPI]).keys():
            apipolicies = ""
            apipoliciesid = []
            apiactionperimetername = response.json()[apis_urls.perimeteractionAPI][ids]['name']
            apiactionperimeterdescription = response.json()[apis_urls.perimeteractionAPI][ids]['description']
            if (len(response.json()[apis_urls.perimeteractionAPI][ids]['policy_list']) != 0):
                for policies in response.json()[apis_urls.perimeteractionAPI][ids]['policy_list']:
                    apipoliciesid.append(commonfunctions.get_policyname(str(policies)))
                apipolicies = ",".join(apipoliciesid)
            else:
                apipolicies = ""
            apiresult.add_row(vals=(
                apiactionperimetername, apiactionperimeterdescription, apipolicies))
    else:
        apiresult.add_row(vals=("", "", ""))

    apiresult.sort('actionperimetername')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected action perimeter name: '" + str(
            row1["actionperimetername"]) + "' is the same as the actual existing '" + str(
            row2["actionperimetername"]) + "'")
        assert str(row1["actionperimetername"]) == str(
            row2["actionperimetername"]), "action perimeter name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected action perimeter description: '" + str(
            row1["actionperimeterdescription"]) + "' is the same as the actual existing '" + str(
            row2["actionperimeterdescription"]) + "'")
        assert str(row1["actionperimeterdescription"]) == str(
            row2["actionperimeterdescription"]), "action perimeter description is not correct!"
        logger.info("assertion passed!")

        if(str(row1["policies"]).find(',')==-1):
            logger.info("asserting the expected policies: '" + str(
            row1["policies"]) + "' is the same as the actual existing '" + str(
            row2["policies"]) + "'")
            logger.info("policies is not correct!")
            assert str(row1["policies"]) == str(row2["policies"]), " policies is not correct!"
        else:

            logger.info("asserting the expected policies: '" + ','.join(sorted(str(row1["policies"]).split(','),key=str.lower)) + "' is the same as the actual existing '" +
                        ','.join(sorted(str(row2["policies"]).split(','), key=str.lower)) + "'")
            logger.info("policies is not correct!")
            assert ','.join(sorted(str(row1["policies"]).split(','),key=str.lower)) == ','.join(sorted(str(row2["policies"]).split(','),key=str.lower)), " policies is not correct!"
        logger.info("assertion passed!")
