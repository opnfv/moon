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
import numpy as np
import requests
import json
import logging

apis_urls = GeneralVariables()
commonfunctions = commonfunctions()

logger = logging.getLogger(__name__)

# Step Definition Implementation:
# 1) Get all the existing meta rule in the system
# 2) Loop by id and delete them
@Given('the system has no meta-rules')
def step_impl(context):
    logger.info("Given the system has no meta-rules")

    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response = requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.metarulesAPI]) != 0:
        for ids in dict(response.json()[apis_urls.metarulesAPI]).keys():
            response = requests.delete(apis_urls.serverURL + apis_urls.metarulesAPI + "/" + ids,
                                       headers=headers)

# Step Definition Implementation:
# 1) Get subject, object, action categories ids list by calling the common funtion: get_subjectcategoryid, get_objectcategoryid and get_actioncategoryid
# 2) create the meta rule data jason then post it
@Given('the following meta rule exists')
def step_impl(context):
    logger.info("Given the following meta rule exists")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "meta-rule name: '" + row["metarulename"] + "' and meta-rule description: '" + row[
                "metaruledescription"] + "' and subject categories:'" + row[
                "subjectmetadata"] + "' and object categories:'" + row["objectmetadata"] + "' and action categories:'" +
            row["actionmetadata"] + "'")
        subjectcategoryids = []
        objectcategoryids = []
        actioncategoryids = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row["subjectmetadata"]) < 40 and str(row["subjectmetadata"])!=""):
            if(str(row["subjectmetadata"]).find(",")!=-1):
                for category in row["subjectmetadata"].split(","):
                    subjectcategoryids.append(commonfunctions.get_subjectcategoryid(category))
            else:
                subjectcategoryids.append(commonfunctions.get_subjectcategoryid(row["subjectmetadata"]))
        else:
            if(str(row["subjectmetadata"])==""):
                subjectcategoryids=[]
            else:
                subjectcategoryids.append(row["subjectmetadata"])

        if (len(row["objectmetadata"]) < 40 and str(row["objectmetadata"])!=""):
            if(str(row["objectmetadata"]).find(",")!=-1):
                for category in row["objectmetadata"].split(","):
                    objectcategoryids.append(commonfunctions.get_objectcategoryid(category))
            else:
                objectcategoryids.append(commonfunctions.get_objectcategoryid(row["objectmetadata"]))
        else:
            if (str(row["objectmetadata"]) == ""):
                objectcategoryids = []
            else:
                objectcategoryids.append(row["objectmetadata"])

        if (len(row["actionmetadata"]) < 40 and str(row["actionmetadata"])!=""):
            if(str(row["actionmetadata"]).find(",")!=-1):
                for category in row["actionmetadata"].split(","):
                    actioncategoryids.append(commonfunctions.get_actioncategoryid(category))
            else:
                actioncategoryids.append(commonfunctions.get_actioncategoryid(row["actionmetadata"]))
        else:
            if(str(row["actionmetadata"]) == ""):
                actioncategoryids = []
            else:
                actioncategoryids.append(row["actionmetadata"])

        data = {
            'name': row["metarulename"],
            'description': row["metaruledescription"],
            'subject_categories': subjectcategoryids,
            'object_categories': objectcategoryids,
            'action_categories': actioncategoryids
        }
        response = requests.post(apis_urls.serverURL + apis_urls.metarulesAPI, headers=headers,
                                 data=json.dumps(data))

# Step Definition Implementation:
# 1) Get subject, object, action categories ids list by calling the common funtion: get_subjectcategoryid, get_objectcategoryid and get_actioncategoryid
# 2) create the meta rule data jason then post it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following meta-rule')
def step_impl(context):
    logger.info("When the user sets to add the following meta-rule")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "meta-rule name: '" + row["metarulename"] + "' and meta-rule description: '" + row[
                "metaruledescription"] + "' and subject categories:'" + row[
                "subjectmetadata"] + "' and object categories:'" + row["objectmetadata"] + "' and action categories:'" +
            row["actionmetadata"] + "'")

        subjectcategoryids = []
        objectcategoryids = []
        actioncategoryids = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row["subjectmetadata"]) < 40 and str(row["subjectmetadata"])!=""):
            if (str(row["subjectmetadata"]).find(",") != -1):
                for category in row["subjectmetadata"].split(","):
                    subjectcategoryids.append(commonfunctions.get_subjectcategoryid(category))
            else:
                subjectcategoryids.append(commonfunctions.get_subjectcategoryid(row["subjectmetadata"]))
        else:
            subjectcategoryids.append(row["subjectmetadata"])

        if (len(row["objectmetadata"]) < 40 and str(row["objectmetadata"])!=""):
            if (str(row["objectmetadata"]).find(",") != -1):
                for category in row["objectmetadata"].split(","):
                    objectcategoryids.append(commonfunctions.get_objectcategoryid(category))
            else:
                objectcategoryids.append(commonfunctions.get_objectcategoryid(row["objectmetadata"]))
        else:
            objectcategoryids.append(row["objectmetadata"])

        if (len(row["actionmetadata"]) < 40 and str(row["actionmetadata"])!=""):
            if (str(row["actionmetadata"]).find(",") != -1):
                for category in row["actionmetadata"].split(","):
                    actioncategoryids.append(commonfunctions.get_actioncategoryid(category))
            else:
                actioncategoryids.append(commonfunctions.get_actioncategoryid(row["actionmetadata"]))
        else:
            actioncategoryids.append(row["actionmetadata"])


        data = {
            'name': row["metarulename"],
            'description': row["metaruledescription"],
            'subject_categories': subjectcategoryids,
            'object_categories': objectcategoryids,
            'action_categories': actioncategoryids
        }

        response = requests.post(apis_urls.serverURL + apis_urls.metarulesAPI, headers=headers,
                                 data=json.dumps(data))
        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get subject, object, action categories ids list by calling the common funtion: get_subjectcategoryid, get_objectcategoryid and get_actioncategoryid
# 2) create the meta rule data jason then patch the meta rule after searching for it's id.
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to update the following meta-rule')
def step_impl(context):
    logger.info("When the user sets to update the following meta-rule")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "meta-rule name: '" + row["metarulename"] + "' which will be updated to metarule name:" + row[
                "updatedmetarulename"] + "' and meta-rule description: '" + row[
                "updatedmetaruledescription"] + "' and subject categories:'" + row[
                "updatedsubjectmetadata"] + "' and object categories:'" + row[
                "updatedobjectmetadata"] + "' and action categories:'" +
            row["updatedactionmetadata"] + "'")

        subjectcategoryids = []
        objectcategoryids = []
        actioncategoryids = []
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row["updatedsubjectmetadata"]) > 40):
            subjectcategoryids.append(row["updatedsubjectmetadata"])
        else:
            for category in row["updatedsubjectmetadata"].split(","):
                subjectcategoryids.append(commonfunctions.get_subjectcategoryid(category))

        if (len(row["updatedobjectmetadata"]) > 40):
            objectcategoryids.append(row["updatedobjectmetadata"])
        else:
            for category in row["updatedobjectmetadata"].split(","):
                objectcategoryids.append(commonfunctions.get_objectcategoryid(category))

        if (len(row["updatedactionmetadata"]) > 40):
            actioncategoryids.append(row["updatedactionmetadata"])
        else:
            for category in row["updatedactionmetadata"].split(","):
                actioncategoryids.append(commonfunctions.get_actioncategoryid(category))

        data = {
            'name': row["updatedmetarulename"],
            'description': row["updatedmetaruledescription"],
            'subject_categories': subjectcategoryids,
            'object_categories': objectcategoryids,
            'action_categories': actioncategoryids
        }

        response = requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.metarulesAPI]).keys():
            if (response.json()[apis_urls.metarulesAPI][ids]['name'] == row["metarulename"]):
                response = requests.patch(apis_urls.serverURL + apis_urls.metarulesAPI + '/' + ids, headers=headers,
                                          data=json.dumps(data))
                break
    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the meta rule by get request
# 2) Loop by ids and search for the matching meta rule by name and delete it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following meta-rule')
def step_impl(context):
    logger.info("When the user sets to delete the following meta-rule")

    model = getattr(context, "model", None)
    for row in context.table:
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        logger.info(
            "meta-rule name: '" + row["metarulename"] + "'")
        response = requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,headers=apis_urls.auth_headers)
        for ids in dict(response.json()[apis_urls.metarulesAPI]).keys():
            if (response.json()[apis_urls.metarulesAPI][ids]['name'] == row["metarulename"]):
                response = requests.delete(apis_urls.serverURL + apis_urls.metarulesAPI + "/" + ids,
                                           headers=headers)
    if response.status_code == 200:
        GeneralVariables.api_responseflag['value'] = 'True'
    else:
        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the existing action meta data by get request and put them into a table
# 2) Sort the table by meta rule name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following meta-rules should be existed in the system')
def step_impl(context):
    logger.info("Then the following meta-rules should be existed in the system")
    response = requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,headers=apis_urls.auth_headers)
    apimetarulesubjectcategoryname = ""
    apimetaruleobjectcategoryname = ""
    apimetaruleactioncategoryname = ""
    apiresult = Table(
        names=('metarulename', 'metaruledescription', 'subjectmetadata', 'actionmetadata', 'objectmetadata'),
        dtype=('S10', 'S100', 'S100', 'S100', 'S100'))
    if len(response.json()[apis_urls.metarulesAPI]) != 0:
        for ids in dict(response.json()[apis_urls.metarulesAPI]).keys():
            apimetarulesubjectcategoryname = ""
            apimetaruleobjectcategoryname = ""
            apimetaruleactioncategoryname = ""
            apimetarulename = response.json()[apis_urls.metarulesAPI][ids]['name']
            apimetaruledescription = response.json()[apis_urls.metarulesAPI][ids]['description']
            for categoryid in response.json()[apis_urls.metarulesAPI][ids]['subject_categories']:
                if (len(apimetarulesubjectcategoryname) > 2):
                    apimetarulesubjectcategoryname = apimetarulesubjectcategoryname + ',' + commonfunctions.get_subjectcategoryname(
                        categoryid)
                else:
                    apimetarulesubjectcategoryname = commonfunctions.get_subjectcategoryname(categoryid)
            for categoryid in response.json()[apis_urls.metarulesAPI][ids]['object_categories']:
                if (len(apimetaruleobjectcategoryname) > 2):
                    apimetaruleobjectcategoryname = apimetaruleobjectcategoryname + ',' + commonfunctions.get_objectcategoryname(
                        categoryid)
                else:
                    apimetaruleobjectcategoryname = commonfunctions.get_objectcategoryname(categoryid)
            for categoryid in response.json()[apis_urls.metarulesAPI][ids]['action_categories']:
                if (len(apimetaruleactioncategoryname) > 2):
                    apimetaruleactioncategoryname = apimetaruleactioncategoryname + ',' + commonfunctions.get_actioncategoryname(
                        categoryid)
                else:
                    apimetaruleactioncategoryname = commonfunctions.get_actioncategoryname(categoryid)

            apiresult.add_row(vals=(
                apimetarulename, apimetaruledescription, apimetarulesubjectcategoryname, apimetaruleactioncategoryname,
                apimetaruleobjectcategoryname))

    else:
        apiresult.add_row(vals=("", "", "", "", ""))

    apiresult.sort('metarulename')

    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected meta rule name: '" + str(
            row1["metarulename"]) + "' is the same as the actual existing '" + str(
            row2["metarulename"]) + "'")
        assert str(row1["metarulename"]) == str(row2["metarulename"]), "meta-rule name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected meta rule description: '" + str(
            row1["metaruledescription"]) + "' is the same as the actual existing '" + str(
            row2["metaruledescription"]) + "'")
        assert str(row1["metaruledescription"]) == str(
            row2["metaruledescription"]), "meta-rule description is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected subject categories: '" + str(
            row1["subjectmetadata"]) + "' is the same as the actual existing '" + str(
            row2["subjectmetadata"]) + "'")
        assert str(row1["subjectmetadata"]) == str(row2["subjectmetadata"]), "subject category is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected object categories: '" + str(
            row1["objectmetadata"]) + "' is the same as the actual existing '" + str(
            row2["objectmetadata"]) + "'")
        assert str(row1["objectmetadata"]) == str(row2["objectmetadata"]), "object category is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected action categories: '" + str(
            row1["actionmetadata"]) + "' is the same as the actual existing '" + str(
            row2["actionmetadata"]) + "'")
        assert str(row1["actionmetadata"]) == str(row2["actionmetadata"]), "action category is not correct!"
        logger.info("assertion passed!")
