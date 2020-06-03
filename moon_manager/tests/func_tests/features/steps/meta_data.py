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
api_subjectcategory = {'name': "", 'description': ""}
api_objectcategory = {'name': "", 'description': ""}
api_actioncategory = {'name': "", 'description': ""}

logger = logging.getLogger(__name__)


# Step Definition Implementation:
# 1) Get all the existing subject meta data in the system
# 2) Loop by id and delete them
@Given('the system has no subject categories')
def step_impl(context):
    logger.info("Given the system has no subject categories")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response = requests.get(apis_urls.serverURL + apis_urls.metadatasubjectcategoryAPI, headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.metadatasubjectcategoryAPI]) != 0:
        for ids in dict(response.json()[apis_urls.metadatasubjectcategoryAPI]).keys():
            response = requests.delete(apis_urls.serverURL + apis_urls.metadatasubjectcategoryAPI + "/" + ids,
                                       headers=headers)

# Step Definition Implementation:
# 1) Get all the existing action meta data in the system
# 2) Loop by id and delete them
@Given('the system has no action categories')
def step_impl(context):
    logger.info("Given the system has no action categories")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response = requests.get(apis_urls.serverURL + apis_urls.metadataactioncategoryAPI, headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.metadataactioncategoryAPI]) != 0:
        for ids in dict(response.json()[apis_urls.metadataactioncategoryAPI]).keys():
            response = requests.delete(apis_urls.serverURL + apis_urls.metadataactioncategoryAPI + "/" + ids,
                                       headers=headers)


# Step Definition Implementation:
# 1) Get all the existing object meta data in the system
# 2) Loop by id and delete them
@Given('the system has no object categories')
def step_impl(context):
    logger.info("Given the system has no object categories")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response = requests.get(apis_urls.serverURL + apis_urls.metadataobjectcategoryAPI, headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.metadataobjectcategoryAPI]) != 0:
        for ids in dict(response.json()[apis_urls.metadataobjectcategoryAPI]).keys():
            response = requests.delete(apis_urls.serverURL + apis_urls.metadataobjectcategoryAPI + "/" + ids,
                                       headers=headers)



# Step Definition Implementation:
# 1) Insert subject meta data using the post request
@Given('the following meta data subject category exists')
def step_impl(context):
    logger.info("Given the following meta data subject category exists")
    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        data = {
            'name': row["subjectmetadataname"],
            'description': row["subjectmetadatadescription"],
        }
        logger.info(
            "subject category name: '" + row["subjectmetadataname"] + "' and subject category description: '" + row[
                "subjectmetadatadescription"] + "'")
        response = requests.post(apis_urls.serverURL + apis_urls.metadatasubjectcategoryAPI, headers=headers,
                                 data=json.dumps(data))

# Step Definition Implementation:
# 1) Insert object meta data using the post request
@Given('the following meta data object category exists')
def step_impl(context):
    logger.info("Given the following meta data object category exists")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        data = {
            'name': row["objectmetadataname"],
            'description': row["objectmetadatadescription"],
        }
        logger.info(
            "object category name: '" + row["objectmetadataname"] + "' and object category description: '" + row[
                "objectmetadatadescription"] + "'")
        response = requests.post(apis_urls.serverURL + apis_urls.metadataobjectcategoryAPI, headers=headers,
                                 data=json.dumps(data))

# Step Definition Implementation:
# 1) Insert action meta data using the post request
@Given('the following meta data action category exists')
def step_impl(context):
    logger.info("Given the following meta data action category exists")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
        data = {
            'name': row["actionmetadataname"],
            'description': row["actionmetadatadescription"],
        }
        logger.info(
            "action category name: '" + row["actionmetadataname"] + "' and action category description: '" + row[
                "actionmetadatadescription"] + "'")
        response = requests.post(apis_urls.serverURL + apis_urls.metadataactioncategoryAPI, headers=headers,
                                 data=json.dumps(data))

# Step Definition Implementation:
# 1) Add subject meta data using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following meta data subject category')
def step_impl(context):
    logger.info("When the user sets to add the following meta data subject category")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
        data = {
            'name': row["subjectmetadataname"],
            'description': row["subjectmetadatadescription"],
        }
        logger.info(
            "subject category name: '" + row["subjectmetadataname"] + "' and subject category description: '" + row[
                "subjectmetadatadescription"] + "'")

        response = requests.post(apis_urls.serverURL + apis_urls.metadatasubjectcategoryAPI, headers=headers,
                                 data=json.dumps(data))

    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'


# Step Definition Implementation:
# 1) Get all the subject meta data by get request
# 2) Loop by ids and search for the matching subject meta data by name and delete it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following meta data subject category')
def step_impl(context):
    logger.info("When the user sets to delete the following meta data subject category")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
        logger.info("subject category name: '" + row["subjectmetadataname"] + "'")

        response = requests.get(apis_urls.serverURL + apis_urls.metadatasubjectcategoryAPI,
                                headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.metadatasubjectcategoryAPI]).keys():
            if (response.json()[apis_urls.metadatasubjectcategoryAPI][ids]['name'] == row["subjectmetadataname"]):
                response = requests.delete(apis_urls.serverURL + apis_urls.metadatasubjectcategoryAPI + "/" + ids,
                                           headers=headers)
    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Add object meta data using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following meta data object category')
def step_impl(context):
    logger.info("When the user sets to add the following meta data object category")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
        data = {
            'name': row["objectmetadataname"],
            'description': row["objectmetadatadescription"],
        }
        logger.info(
            "object category Name: '" + row["objectmetadataname"] + "' and object category description: '" + row[
                "objectmetadatadescription"] + "''")
        response = requests.post(apis_urls.serverURL + apis_urls.metadataobjectcategoryAPI, headers=headers,
                                 data=json.dumps(data))
    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the object meta data by get request
# 2) Loop by ids and search for the matching object meta data by name and delete it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following meta data object category')
def step_impl(context):
    logger.info("When the user sets to delete the following meta data object category")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
        logger.info("object category name: '" + row["objectmetadataname"] + "'")

        response = requests.get(apis_urls.serverURL + apis_urls.metadataobjectcategoryAPI,
                                headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.metadataobjectcategoryAPI]).keys():
            if (response.json()[apis_urls.metadataobjectcategoryAPI][ids]['name'] == row["objectmetadataname"]):
                response = requests.delete(apis_urls.serverURL + apis_urls.metadataobjectcategoryAPI + "/" + ids,
                                           headers=headers)
    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Add subject meta data using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following meta data action category')
def step_impl(context):
    logger.info("When the user sets to add the following meta data action category")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        data = {
            'name': row["actionmetadataname"],
            'description': row["actionmetadatadescription"],
        }
        logger.info(
            "action category name: '" + row["actionmetadataname"] + "' and action category description: '" + row[
                "actionmetadatadescription"] + "'")

        response = requests.post(apis_urls.serverURL + apis_urls.metadataactioncategoryAPI, headers=headers,
                                 data=json.dumps(data))
    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the action meta data by get request
# 2) Loop by ids and search for the matching action meta data by name and delete it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following meta data action category')
def step_impl(context):
    logger.info("When the user sets to delete the following meta data action category")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        logger.info("action category name: '" + row["actionmetadataname"] + "'")

        response = requests.get(apis_urls.serverURL + apis_urls.metadataactioncategoryAPI,
                                headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.metadataactioncategoryAPI]).keys():
            # logger.info(ids)
            if (response.json()[apis_urls.metadataactioncategoryAPI][ids]['name'] == row["actionmetadataname"]):
                response = requests.delete(apis_urls.serverURL + apis_urls.metadataactioncategoryAPI + "/" + ids,
                                           headers=headers)
                # logger.info(response.status_code)
    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the existing subject meta data by get request and put them into a table
# 2) Loop using both the expected and actual tables and assert the data row by row
@Then('the following meta data subject category should be existed in the system')
def step_impl(context):
    logger.info("Then the following meta data subject category should be existed in the system")

    model = getattr(context, "model", None)
    response = requests.get(apis_urls.serverURL + apis_urls.metadatasubjectcategoryAPI, headers=apis_urls.auth_headers)
    apiresult = Table(names=('subjectcategoryname', 'subjectcategorydescription'), dtype=('S100', 'S100'))
    if len(response.json()[apis_urls.metadatasubjectcategoryAPI]) != 0:
        for ids in dict(response.json()[apis_urls.metadatasubjectcategoryAPI]).keys():
            apisubjectcategoryname = response.json()[apis_urls.metadatasubjectcategoryAPI][ids]['name']
            apisubjectcategorydescription = response.json()[apis_urls.metadatasubjectcategoryAPI][ids]['description']
            apiresult.add_row(vals=(apisubjectcategoryname, apisubjectcategorydescription))
    else:
        apiresult.add_row(vals=("", ""))
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected subject category name: '" + str(
            row1["subjectmetadataname"]) + "' is the same as the actual existing '" + str(
            row2["subjectcategoryname"]) + "'")
        assert str(row1["subjectmetadataname"]) == str(
            row2["subjectcategoryname"]), "subject category name is not correct!"
        logger.info("assertion passed!")
        logger.info("asserting the expected subject category description: '" + str(
            row1["subjectmetadatadescription"]) + "' is the same as the actual existing '" + str(
            row2["subjectcategorydescription"]) + "'")
        assert str(row1["subjectmetadatadescription"]) == str(
            row2["subjectcategorydescription"]), "Subject meta-data category description is not correct!"
        logger.info("assertion passed!")

# Step Definition Implementation:
# 1) Get all the existing object meta data by get request and put them into a table
# 2) Loop using both the expected and actual tables and assert the data row by row
@Then('the following meta data object category should be existed in the system')
def step_impl(context):
    model = getattr(context, "model", None)
    logger.info("Then the following meta data object category should be existed in the system")
    response = requests.get(apis_urls.serverURL + apis_urls.metadataobjectcategoryAPI, headers=apis_urls.auth_headers)
    apiresult = Table(names=('objectcategoryname', 'objectcategorydescription'), dtype=('S100', 'S100'))

    if len(response.json()[apis_urls.metadataobjectcategoryAPI]) != 0:
        for ids in dict(response.json()[apis_urls.metadataobjectcategoryAPI]).keys():
            apiobjectcategoryname = response.json()[apis_urls.metadataobjectcategoryAPI][ids]['name']
            apiobjectcategorydescription = response.json()[apis_urls.metadataobjectcategoryAPI][ids]['description']
            apiresult.add_row(vals=(apiobjectcategoryname, apiobjectcategorydescription))
    else:
        apiresult.add_row(vals=("", ""))
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected object category description: '" + str(
            row1["objectmetadataname"]) + "' is the same as the actual existing '" + str(
            row2["objectcategoryname"]) + "'")
        assert str(row1["objectmetadataname"]) == str(
            row2["objectcategoryname"]), "object category name is not correct!"
        logger.info("assertion passed!")
        logger.info("asserting the expected object category description: '" + str(
            row1["objectmetadatadescription"]) + "' is the same as the actual existing '" + str(
            row2["objectcategorydescription"]) + "'")
        assert str(row1["objectmetadatadescription"]) == str(
            row2["objectcategorydescription"]), "object meta-data category description is not correct!"
        logger.info("assertion passed!")

# Step Definition Implementation:
# 1) Get all the existing action meta data by get request and put them into a table
# 2) Loop using both the expected and actual tables and assert the data row by row
@Then('the following meta data action category should be existed in the system')
def step_impl(context):
    logger.info("Then the following meta data action category should be existed in the system")

    model = getattr(context, "model", None)
    response = requests.get(apis_urls.serverURL + apis_urls.metadataactioncategoryAPI, headers=apis_urls.auth_headers)
    apiresult = Table(names=('actioncategoryname', 'actioncategorydescription'), dtype=('S100', 'S100'))
    if len(response.json()[apis_urls.metadataactioncategoryAPI]) != 0:
        for ids in dict(response.json()[apis_urls.metadataactioncategoryAPI]).keys():
            apiactioncategoryname = response.json()[apis_urls.metadataactioncategoryAPI][ids]['name']
            apiactioncategorydescription = response.json()[apis_urls.metadataactioncategoryAPI][ids]['description']
            apiresult.add_row(vals=(apiactioncategoryname, apiactioncategorydescription))
    else:
        apiresult.add_row(vals=("", ""))
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected action category description: '" + str(
            row1["actionmetadataname"]) + "' is the same as the actual existing '" + str(
            row2["actioncategoryname"]) + "'")

        assert str(row1["actionmetadataname"]) == str(
            row2["actioncategoryname"]), "action category name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected action category description: '" + str(
            row1["actionmetadatadescription"]) + "' is the same as the actual existing '" + str(
            row2["actioncategorydescription"]) + "'")

        assert str(row1["actionmetadatadescription"]) == str(
            row2["actioncategorydescription"]), "action meta-data category description is not correct!"
        logger.info("assertion passed!")

# Step Definition Implementation:
# Assert the saved api response flag with the expected flag
@Then('the system should reply the following')
def step_impl(context):
    logger.info("Then the system should reply the following:")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info("asserting the expected api response: '" + row["flag"] + "' and the actual response: '" +
                    GeneralVariables.api_responseflag['value'] + "'")
        assert row["flag"] == GeneralVariables.api_responseflag['value'], "Validation is not correct, Expected: " + row[
            "flag"] + " but the API response was: " + GeneralVariables.api_responseflag['value']
        logger.info("assertion passed!")
