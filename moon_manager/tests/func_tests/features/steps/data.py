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
# 1) Get all the existing subject meta data in the system by getting the policies then their models then the model attached meta rules and then the categories
# 2) Get subject data using both the policy id & the category id
# 3) Loop by data id and delete it
@Given('the system has no subject data')
def step_impl(context):
    logger.info("Given the system has no subject data")
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response_policies = requests.get(apis_urls.serverURL + apis_urls.policyAPI,headers=apis_urls.auth_headers)
    if len(response_policies.json()[apis_urls.policyAPI]) != 0:
        for policies_ids in dict(response_policies.json()[apis_urls.policyAPI]).keys():
            subjectcategoryidslist = []
            modelid = response_policies.json()[apis_urls.policyAPI][policies_ids]['model_id']
            if (modelid != None and modelid != ""):
                metaruleslist = \
                    requests.get(apis_urls.serverURL + apis_urls.modelAPI,headers=apis_urls.auth_headers).json()[apis_urls.modelAPI][modelid][
                        'meta_rules']
                for metarule_ids in metaruleslist:
                    categorieslist = \
                        requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                            metarule_ids]['subject_categories']
                    for categoryid in categorieslist:
                        if (categoryid not in subjectcategoryidslist):
                            subjectcategoryidslist.append(categoryid)

                for categoryid in subjectcategoryidslist:
                    response_data = requests.get(
                        apis_urls.serverURL + apis_urls.policyAPI + "/" + policies_ids + "/" + apis_urls.datasubjectAPI + "/" + categoryid,headers=apis_urls.auth_headers)
                    for ids in response_data.json()[apis_urls.datasubjectAPI][0]['data']:
                        data_id = response_data.json()[apis_urls.datasubjectAPI][0]['data'][str(ids)]['id']
                        requests.delete(
                            apis_urls.serverURL + apis_urls.policyAPI + "/" + policies_ids + "/" + apis_urls.datasubjectAPI + "/" + categoryid + "/" + data_id,
                            headers=headers)

# Step Definition Implementation:
# 1) Post subject data using the policy id & the category id
@Given('the following subject data exists')
def step_impl(context):
    logger.info("Given the following subject data exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "subject data name: '" + row["subjectdataname"] + "' subject data description: '" + row[
                "subjectdatadescription"] + "' and subject category: '" + row[
                "subjectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['policyname']) > 25):
            policies_id = row['policyname']
        else:
            policies_id = commonfunctions.get_policyid(row['policyname'])

        if (len(row['subjectcategory']) > 25):
            categories_id = row['subjectcategory']
        else:
            categories_id = commonfunctions.get_subjectcategoryid(row['subjectcategory'])

        data = {
            'name': row["subjectdataname"],
            'description': row["subjectdatadescription"],

        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.datasubjectAPI + "/" + str(
                categories_id), headers=headers, data=json.dumps(data))

# Step Definition Implementation:
# 1) Get all the existing object meta data in the system by getting the policies then their models then the model attached meta rules and then the categories
# 2) Get object data using both the policy id & the category id
# 3) Loop by data id and delete it
@Given('the system has no object data')
def step_impl(context):
    logger.info("Given the system has no object data")
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response_policies = requests.get(apis_urls.serverURL + apis_urls.policyAPI,headers=apis_urls.auth_headers)
    if len(response_policies.json()[apis_urls.policyAPI]) != 0:
        for policies_ids in dict(response_policies.json()[apis_urls.policyAPI]).keys():
            objectcategoryidslist = []
            modelid = response_policies.json()[apis_urls.policyAPI][policies_ids]['model_id']
            if (modelid != None and modelid != ""):
                metaruleslist = \
                    requests.get(apis_urls.serverURL + apis_urls.modelAPI,headers=apis_urls.auth_headers).json()[apis_urls.modelAPI][modelid][
                        'meta_rules']
                for metarule_ids in metaruleslist:
                    for categoryid in \
                            (requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,headers=apis_urls.auth_headers)).json()[apis_urls.metarulesAPI][
                                metarule_ids][
                                'object_categories']:
                        if (categoryid not in objectcategoryidslist):
                            objectcategoryidslist.append(categoryid)

                for categoryid in objectcategoryidslist:
                    response_data = requests.get(
                        apis_urls.serverURL + apis_urls.policyAPI + "/" + policies_ids + "/" + apis_urls.dataobjectAPI + "/" + categoryid,headers=apis_urls.auth_headers)
                    for ids in response_data.json()[apis_urls.dataobjectAPI][0]['data']:
                        data_id = response_data.json()[apis_urls.dataobjectAPI][0]['data'][str(ids)]['id']
                        requests.delete(
                            apis_urls.serverURL + apis_urls.policyAPI + "/" + policies_ids + "/" + apis_urls.dataobjectAPI + "/" + categoryid + "/" + data_id,
                            headers=headers)

# Step Definition Implementation:
# 1) Post object data using the policy id & the category id
@Given('the following object data exists')
def step_impl(context):
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "subject data name: '" + row["objectdataname"] + "' object data description: '" + row[
                "objectdatadescription"] + "' and object category: '" + row[
                "objectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['policyname']) > 25):
            policies_id = row['policyname']
        else:
            policies_id = commonfunctions.get_policyid(row['policyname'])

        if (len(row['objectcategory']) > 25):
            categories_id = row['objectcategory']
        else:
            categories_id = commonfunctions.get_objectcategoryid(row['objectcategory'])

        data = {
            'name': row["objectdataname"],
            'description': row["objectdatadescription"],

        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.dataobjectAPI + "/" + str(
                categories_id), headers=headers, data=json.dumps(data))

# Step Definition Implementation:
# 1) Get all the existing action meta data in the system by getting the policies then their models then the model attached meta rules and then the categories
# 2) Get action data using both the policy id & the category id
# 3) Loop by data id and delete it
@Given('the system has no action data')
def step_impl(context):
    logger.info("Given the system has no action data")
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
    actioncategoryidslist = []
    response_policies = requests.get(apis_urls.serverURL + apis_urls.policyAPI,headers=apis_urls.auth_headers)
    if len(response_policies.json()[apis_urls.policyAPI]) != 0:
        for policies_ids in dict(response_policies.json()[apis_urls.policyAPI]).keys():
            actioncategoryidslist = []
            modelid = response_policies.json()[apis_urls.policyAPI][policies_ids]['model_id']
            if (modelid != None and modelid != ""):
                metaruleslist = \
                    requests.get(apis_urls.serverURL + apis_urls.modelAPI,headers=apis_urls.auth_headers).json()[apis_urls.modelAPI][modelid][
                        'meta_rules']
                for metarule_ids in metaruleslist:
                    for categoryid in \
                            (requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,headers=apis_urls.auth_headers)).json()[apis_urls.metarulesAPI][
                                metarule_ids][
                                'action_categories']:
                        if (categoryid not in actioncategoryidslist):
                            actioncategoryidslist.append(categoryid)

                for categoryid in actioncategoryidslist:
                    response_data = requests.get(
                        apis_urls.serverURL + apis_urls.policyAPI + "/" + policies_ids + "/" + apis_urls.dataactionAPI + "/" + categoryid,headers=apis_urls.auth_headers)
                    for ids in response_data.json()[apis_urls.dataactionAPI][0]['data']:
                        data_id = response_data.json()[apis_urls.dataactionAPI][0]['data'][str(ids)]['id']
                        requests.delete(
                            apis_urls.serverURL + apis_urls.policyAPI + "/" + policies_ids + "/" + apis_urls.dataactionAPI + "/" + categoryid + "/" + data_id,
                            headers=headers)

# Step Definition Implementation:
# 1) Post action data using the policy id & the category id
@Given('the following action data exists')
def step_impl(context):
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "subject data name: '" + row["actiondataname"] + "' action data description: '" + row[
                "actiondatadescription"] + "' and action category: '" + row[
                "actioncategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['policyname']) > 25):
            policies_id = row['policyname']
        else:
            policies_id = commonfunctions.get_policyid(row['policyname'])

        if (len(row['actioncategory']) > 25):
            categories_id = row['actioncategory']
        else:
            categories_id = commonfunctions.get_actioncategoryid(row['actioncategory'])

        data = {
            'name': row["actiondataname"],
            'description': row["actiondatadescription"],

        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.dataactionAPI + "/" + str(
                categories_id), headers=headers, data=json.dumps(data))

# Step Definition Implementation:
# 1) Add subject data using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following subject data')
def step_impl(context):
    logger.info("When the user sets to add the following subject data")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "subject data name: '" + row["subjectdataname"] + "' subject data description: '" + row[
                "subjectdatadescription"] + "' and subject category: '" + row[
                "subjectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['policyname']) > 25):
            policies_id = row['policyname']
        else:
            policies_id = commonfunctions.get_policyid(row['policyname'])

        if (len(row['subjectcategory']) > 25):
            categories_id = row['subjectcategory']
        else:
            categories_id = commonfunctions.get_subjectcategoryid(row['subjectcategory'])

        data = {
            'name': row["subjectdataname"],
            'description': row["subjectdatadescription"],

        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.datasubjectAPI + "/" + str(
                categories_id), headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Delete subject data by policy id, subject data id, subject category id
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following subject data')
def step_impl(context):
    logging.info("When the user sets to delete the following subject data")

    model = getattr(context, "model", None)
    for row in context.table:

        logger.info("subject data name:'" + row["subjectdataname"] + "' and subject category name:'" + row[
            "subjectcategory"] + "' and policy name:'" + row["policyname"] + "'")

        policies_id = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        response_data = requests.delete(
            apis_urls.serverURL + apis_urls.policyAPI + "/" + commonfunctions.get_policyid(row[
                                                                                               "policyname"]) + "/" + apis_urls.datasubjectAPI + "/" + commonfunctions.get_subjectcategoryid(
                row["subjectcategory"]) + "/" + commonfunctions.get_subjectdataid(row["subjectdataname"],
                                                                                  commonfunctions.get_subjectcategoryid(
                                                                                      row["subjectcategory"]),
                                                                                  commonfunctions.get_policyid(
                                                                                      row["policyname"])),
            headers=headers)

        if response_data.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Add object data using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following object data')
def step_impl(context):
    logger.info("When the user sets to add the following object data")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "object data name: '" + row["objectdataname"] + "' object data description: '" + row[
                "objectdatadescription"] + "' and object category: '" + row[
                "objectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_list = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['policyname']) > 25):
            policies_id = row['policyname']
        else:
            policies_id = commonfunctions.get_policyid(row['policyname'])

        if (len(row['objectcategory']) > 25):
            categories_id = row['objectcategory']
        else:
            categories_id = commonfunctions.get_objectcategoryid(row['objectcategory'])

        data = {
            'name': row["objectdataname"],
            'description': row["objectdatadescription"],
        }

        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.dataobjectAPI + "/" + str(
                categories_id), headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Delete object data by policy id, object data id, object category id
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following object data')
def step_impl(context):
    logging.info("When the user sets to delete the following object data")
    model = getattr(context, "model", None)
    for row in context.table:

        logger.info("object data name:'" + row["objectdataname"] + "' and object category name:'" + row[
            "objectcategory"] + "' and policy name:'" + row["policyname"] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        response_data = requests.delete(
            apis_urls.serverURL + apis_urls.policyAPI + "/" + commonfunctions.get_policyid(row[
                                                                                               "policyname"]) + "/" + apis_urls.dataobjectAPI + "/" + commonfunctions.get_objectcategoryid(
                row["objectcategory"]) + "/" + commonfunctions.get_objectdataid(row["objectdataname"],
                                                                                commonfunctions.get_objectcategoryid(
                                                                                    row["objectcategory"]),
                                                                                commonfunctions.get_policyid(
                                                                                    row["policyname"])),
            headers=headers)

        if response_data.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Add action data using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following action data')
def step_impl(context):
    logger.info("When the user sets to add the following action data")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "action data name: '" + row["actiondataname"] + "' action data description: '" + row[
                "actiondatadescription"] + "' and action category: '" + row[
                "actioncategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['policyname']) > 25):
            policies_id = row['policyname']
        else:
            policies_id = commonfunctions.get_policyid(row['policyname'])

        if (len(row['actioncategory']) > 25):
            categories_id = row['actioncategory']
        else:
            categories_id = commonfunctions.get_actioncategoryid(row['actioncategory'])

        data = {
            'name': row["actiondataname"],
            'description': row["actiondatadescription"],

        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.dataactionAPI + "/" + str(
                categories_id), headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Delete action data by policy id, action data id, action category id
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following action data')
def step_impl(context):
    logging.info("When the user sets to delete the following action data")
    model = getattr(context, "model", None)
    for row in context.table:

        logger.info("action data name:'" + row["actiondataname"] + "' and action category name:'" + row[
            "actioncategory"] + "' and policy name:'" + row["policyname"] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        response_data = requests.delete(
            apis_urls.serverURL + apis_urls.policyAPI + "/" + commonfunctions.get_policyid(row[
                                                                                               "policyname"]) + "/" + apis_urls.dataactionAPI + "/" + commonfunctions.get_actioncategoryid(
                row["actioncategory"]) + "/" + commonfunctions.get_actiondataid(row["actiondataname"],
                                                                                commonfunctions.get_actioncategoryid(
                                                                                    row["actioncategory"]),
                                                                                commonfunctions.get_policyid(
                                                                                    row["policyname"])),
            headers=headers)

        if response_data.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the existing subject data by get request and put them into a table
# 2) Sort the table by policy name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following subject data should be existed in the system')
def step_impl(context):
    logger.info("Then the following subject data should be existed in the system")
    model = getattr(context, "model", None)
    apiresult = Table(names=('subjectdataname', 'subjectdatadescription', 'subjectcategory', 'policyname'),
                      dtype=('S100', 'S100', 'S100', 'S100'))
    for row in context.table:
        if (row['policyname'] != ""):
            response = requests.get(
                apis_urls.serverURL + "policies/" + commonfunctions.get_policyid(
                    row['policyname']) + "/" + apis_urls.datasubjectAPI + "/" +
                commonfunctions.get_subjectcategoryid(row['subjectcategory']),headers=apis_urls.auth_headers)

            if len(response.json()[apis_urls.datasubjectAPI]) != 0:
                for ids in response.json()[apis_urls.datasubjectAPI][0]['data']:
                    apipolicies = ""
                    apisubjectdataname = response.json()[apis_urls.datasubjectAPI][0]['data'][str(ids)]['name']
                    apisubjectdatadescription = response.json()[apis_urls.datasubjectAPI][0]['data'][str(ids)][
                        'description']
                    apisubjectcategory = commonfunctions.get_subjectcategoryname(
                        response.json()[apis_urls.datasubjectAPI][0]['data'][str(ids)]['category_id'])
                    apipolicies = commonfunctions.get_policyname(
                        response.json()[apis_urls.datasubjectAPI][0]['data'][str(ids)]['policy_id'])
                    apiresult.add_row(vals=(
                        apisubjectdataname, apisubjectdatadescription, apisubjectcategory, apipolicies))
            else:
                apiresult.add_row(vals=("", "", "", ""))

        else:
            apiresult.add_row(vals=("", "", "", ""))

    apiresult.sort('policyname')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected subject data name: '" + str(
            row1["subjectdataname"]) + "' is the same as the actual existing '" + str(
            row2["subjectdataname"]) + "'")
        assert str(row1["subjectdataname"]) == str(row2["subjectdataname"]), "subject data name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected subject data description: '" + str(
            row1["subjectdatadescription"]) + "' is the same as the actual existing '" + str(
            row2["subjectdatadescription"]) + "'")
        assert str(row1["subjectdatadescription"]) == str(
            row2["subjectdatadescription"]), "subject data description is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected subject data password: '" + str(
            row1["subjectcategory"]) + "' is the same as the actual existing '" + str(
            row2["subjectcategory"]) + "'")
        assert str(row1["subjectcategory"]) == str(
            row2["subjectcategory"]), "subject category is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected policies: '" + str(
            row1["policyname"]) + "' is the same as the actual existing '" + str(
            row2["policyname"]) + "'")
        assert str(row1["policyname"]) == str(row2["policyname"]), " policies is not correct!"
        logger.info("assertion passed!")

# Step Definition Implementation:
# 1) Get all the existing object data by get request and put them into a table
# 2) Sort the table by policy name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following object data should be existed in the system')
def step_impl(context):
    logger.info("Then the following object data should be existed in the system")
    model = getattr(context, "model", None)
    apiresult = Table(names=('objectdataname', 'objectdatadescription', 'objectcategory', 'policyname'),
                      dtype=('S100', 'S100', 'S100', 'S100'))

    for row in context.table:
        if (row['policyname'] != ""):
            response = requests.get(
                apis_urls.serverURL + "policies/" + commonfunctions.get_policyid(
                    row['policyname']) + "/" + apis_urls.dataobjectAPI + "/" +
                commonfunctions.get_objectcategoryid(row['objectcategory']),headers=apis_urls.auth_headers)

            if len(response.json()[apis_urls.dataobjectAPI]) != 0:
                for ids in response.json()[apis_urls.dataobjectAPI][0]['data']:
                    apipolicies = ""
                    apiobjectdataname = response.json()[apis_urls.dataobjectAPI][0]['data'][str(ids)]['name']
                    apiobjectdatadescription = response.json()[apis_urls.dataobjectAPI][0]['data'][str(ids)][
                        'description']
                    apiobjectcategory = commonfunctions.get_objectcategoryname(
                        response.json()[apis_urls.dataobjectAPI][0]['data'][str(ids)]['category_id'])
                    apipolicies = commonfunctions.get_policyname(
                        response.json()[apis_urls.dataobjectAPI][0]['data'][str(ids)]['policy_id'])

                    apiresult.add_row(vals=(
                        apiobjectdataname, apiobjectdatadescription, apiobjectcategory, apipolicies))
            else:
                apiresult.add_row(vals=("", "", "", ""))
        else:
            apiresult.add_row(vals=("", "", "", ""))

    apiresult.sort('policyname')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected object data name: '" + str(
            row1["objectdataname"]) + "' is the same as the actual existing '" + str(
            row2["objectdataname"]) + "'")
        assert str(row1["objectdataname"]) == str(row2["objectdataname"]), "subject data name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected object data description: '" + str(
            row1["objectdatadescription"]) + "' is the same as the actual existing '" + str(
            row2["objectdatadescription"]) + "'")
        assert str(row1["objectdatadescription"]) == str(
            row2["objectdatadescription"]), "object data description is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected object data category: '" + str(
            row1["objectcategory"]) + "' is the same as the actual existing '" + str(
            row2["objectcategory"]) + "'")
        assert str(row1["objectcategory"]) == str(
            row2["objectcategory"]), "object category is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected policies: '" + str(
            row1["policyname"]) + "' is the same as the actual existing '" + str(
            row2["policyname"]) + "'")
        assert str(row1["policyname"]) == str(row2["policyname"]), " policies is not correct!"
        logger.info("assertion passed!")

# Step Definition Implementation:
# 1) Get all the existing action data by get request and put them into a table
# 2) Sort the table by policy name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following action data should be existed in the system')
def step_impl(context):
    logger.info("Then the following action data should be existed in the system")
    model = getattr(context, "model", None)
    apiresult = Table(names=('actiondataname', 'actiondatadescription', 'actioncategory', 'policyname'),
                      dtype=('S100', 'S100', 'S100', 'S100'))
    for row in context.table:
        if (row['policyname'] != ""):
            response = requests.get(
                apis_urls.serverURL + "policies/" + commonfunctions.get_policyid(
                    row['policyname']) + "/" + apis_urls.dataactionAPI + "/" +
                commonfunctions.get_actioncategoryid(row['actioncategory']),headers=apis_urls.auth_headers)

            if len(response.json()[apis_urls.dataactionAPI]) != 0:
                for ids in response.json()[apis_urls.dataactionAPI][0]['data']:
                    apipolicies = ""
                    apiactiondataname = response.json()[apis_urls.dataactionAPI][0]['data'][str(ids)]['name']
                    apiactiondatadescription = response.json()[apis_urls.dataactionAPI][0]['data'][str(ids)][
                        'description']
                    apiactioncategory = commonfunctions.get_actioncategoryname(
                        response.json()[apis_urls.dataactionAPI][0]['data'][str(ids)]['category_id'])
                    apipolicies = commonfunctions.get_policyname(
                        response.json()[apis_urls.dataactionAPI][0]['data'][str(ids)]['policy_id'])

                    apiresult.add_row(vals=(
                        apiactiondataname, apiactiondatadescription, apiactioncategory, apipolicies))
            else:
                apiresult.add_row(vals=("", "", "", ""))

        else:
            apiresult.add_row(vals=("", "", "", ""))
    apiresult.sort('policyname')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected action data name: '" + str(
            row1["actiondataname"]) + "' is the same as the actual existing '" + str(
            row2["actiondataname"]) + "'")
        assert str(row1["actiondataname"]) == str(row2["actiondataname"]), "action data name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected action data description: '" + str(
            row1["actiondatadescription"]) + "' is the same as the actual existing '" + str(
            row2["actiondatadescription"]) + "'")
        assert str(row1["actiondatadescription"]) == str(
            row2["actiondatadescription"]), "action data description is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected action data category: '" + str(
            row1["actioncategory"]) + "' is the same as the actual existing '" + str(
            row2["actioncategory"]) + "'")
        assert str(row1["actioncategory"]) == str(
            row2["actioncategory"]), "action category is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected policies: '" + str(
            row1["policyname"]) + "' is the same as the actual existing '" + str(
            row2["policyname"]) + "'")
        assert str(row1["policyname"]) == str(row2["policyname"]), " policies is not correct!"
        logger.info("assertion passed!")
