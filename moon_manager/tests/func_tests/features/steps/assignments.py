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
# 2) Get subject assignment id using both the policy id, data id & the category id
# 3) Loop by assignment id and delete it
@Given('the system has no subject assignments')
def step_impl(context):
    logger.info("Given the system has no subject assignments")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response_policies = requests.get(apis_urls.serverURL + apis_urls.policyAPI, headers=apis_urls.auth_headers)
    if len(response_policies.json()[apis_urls.policyAPI]) != 0:
        for policies_ids in dict(response_policies.json()[apis_urls.policyAPI]).keys():
            # subjectcategoryidslist = []
            # subjectdataidslist = []
            # modelid = response_policies.json()[apis_urls.policyAPI][policies_ids]['model_id']
            # if (modelid != None and modelid != ""):
            #     metaruleslist = \
            #         requests.get(apis_urls.serverURL + apis_urls.modelAPI, headers=apis_urls.auth_headers).json()[apis_urls.modelAPI][modelid]['meta_rules']
            #     for metarule_ids in metaruleslist:
            #         categorieslist = \
            #             requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,
            #                          headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
            #                 metarule_ids]['subject_categories']
            #         for categoryid in categorieslist:
            #             if (categoryid not in subjectcategoryidslist):
            #                 subjectcategoryidslist.append(categoryid)
            #
            #     response_perimeters = requests.get(apis_urls.serverURL + apis_urls.perimetersubjectAPI,
            #                                        headers=apis_urls.auth_headers).json()[
            #         apis_urls.perimetersubjectAPI]
            #     for perimeterid in dict(response_perimeters).keys():
            #         for categoryid in subjectcategoryidslist:
            #             response_assignment = requests.get(
            #                 apis_urls.serverURL + "policies/" + policies_ids + "/" + apis_urls.assignementssubjectAPI + "/" +
            #                 perimeterid + "/" + categoryid, headers=apis_urls.auth_headers)
            #             if len(response_assignment.json()[apis_urls.assignementssubjectAPI]) != 0:
            #                 for ids in dict(response_assignment.json()[apis_urls.assignementssubjectAPI]).keys():
            #                     assignmentsid = response_assignment.json()[apis_urls.assignementssubjectAPI][str(ids)][
            #                         'assignments']
            #                     for dataid in assignmentsid:
            response = requests.delete(
                apis_urls.serverURL + "policies/" + policies_ids + "/" + apis_urls.assignementssubjectAPI , headers=headers)

# Step Definition Implementation:
# 1) Get all the existing object meta data in the system by getting the policies then their models then the model attached meta rules and then the categories
# 2) Get object assignment id using both the policy id, data id & the category id
# 3) Loop by assignment id and delete it
@Given('the system has no object assignments')
def step_impl(context):
    logger.info("Given the system has no object assignments")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response_policies = requests.get(apis_urls.serverURL + apis_urls.policyAPI, headers=apis_urls.auth_headers)
    if len(response_policies.json()[apis_urls.policyAPI]) != 0:
        for policies_ids in dict(response_policies.json()[apis_urls.policyAPI]).keys():
            # objectcategoryidslist = []
            # objectdataidslist = []
            # modelid = response_policies.json()[apis_urls.policyAPI][policies_ids]['model_id']
            # if (modelid != None and modelid != ""):
            #     metaruleslist = \
            #         requests.get(apis_urls.serverURL + apis_urls.modelAPI, headers=apis_urls.auth_headers).json()[
            #             apis_urls.modelAPI][modelid][
            #             'meta_rules']
            #     for metarule_ids in metaruleslist:
            #         categorieslist = \
            #             requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,
            #                          headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
            #                 metarule_ids]['object_categories']
            #         for categoryid in categorieslist:
            #             if (categoryid not in objectcategoryidslist):
            #                 objectcategoryidslist.append(categoryid)
            #
            #     response_perimeters = \
            #         requests.get(apis_urls.serverURL + apis_urls.perimeterobjectAPI,
            #                      headers=apis_urls.auth_headers).json()[
            #             apis_urls.perimeterobjectAPI]
            #     for perimeterid in dict(response_perimeters).keys():
            #         for categoryid in objectcategoryidslist:
            #             response_assignment = requests.get(
            #                 apis_urls.serverURL + "policies/" + policies_ids + "/" + apis_urls.assignementsobjectAPI + "/" +
            #                 perimeterid + "/" + categoryid, headers=apis_urls.auth_headers)
            #             if len(response_assignment.json()[apis_urls.assignementsobjectAPI]) != 0:
            #                 for ids in dict(response_assignment.json()[apis_urls.assignementsobjectAPI]).keys():
            #                     assignmentsid = response_assignment.json()[apis_urls.assignementsobjectAPI][str(ids)][
            #                         'assignments']
            #                     for dataid in assignmentsid:
            response = requests.delete(
                apis_urls.serverURL + "policies/" + policies_ids + "/" + apis_urls.assignementsobjectAPI , headers=headers)

# Step Definition Implementation:
# 1) Get all the existing action meta data in the system by getting the policies then their models then the model attached meta rules and then the categories
# 2) Get action assignment id using both the policy id, data id & the category id
# 3) Loop by assignment id and delete it
@Given('the system has no action assignments')
def step_impl(context):
    logger.info("Given the system has no action assignments")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    response_policies = requests.get(apis_urls.serverURL + apis_urls.policyAPI, headers=apis_urls.auth_headers)
    if len(response_policies.json()[apis_urls.policyAPI]) != 0:
        for policies_ids in dict(response_policies.json()[apis_urls.policyAPI]).keys():
            # actioncategoryidslist = []
            # actiondataidslist = []
            # modelid = response_policies.json()[apis_urls.policyAPI][policies_ids]['model_id']
            # if (modelid != None and modelid != ""):
            #     metaruleslist = \
            #         requests.get(apis_urls.serverURL + apis_urls.modelAPI, headers=apis_urls.auth_headers).json()[
            #             apis_urls.modelAPI][modelid][
            #             'meta_rules']
            #     for metarule_ids in metaruleslist:
            #         categorieslist = \
            #             requests.get(apis_urls.serverURL + apis_urls.metarulesAPI,
            #                          headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
            #                 metarule_ids]['action_categories']
            #         for categoryid in categorieslist:
            #             if (categoryid not in actioncategoryidslist):
            #                 actioncategoryidslist.append(categoryid)
            #
            #     response_perimeters = \
            #         requests.get(apis_urls.serverURL + apis_urls.perimeteractionAPI,
            #                      headers=apis_urls.auth_headers).json()[
            #             apis_urls.perimeteractionAPI]
            #     for perimeterid in dict(response_perimeters).keys():
            #         for categoryid in actioncategoryidslist:
            #             response_assignment = requests.get(
            #                 apis_urls.serverURL + "policies/" + policies_ids + "/" + apis_urls.assignementsactionAPI + "/" +
            #                 perimeterid + "/" + categoryid, headers=apis_urls.auth_headers)
            #             if len(response_assignment.json()[apis_urls.assignementsactionAPI]) != 0:
            #                 for ids in dict(response_assignment.json()[apis_urls.assignementsactionAPI]).keys():
            #                     assignmentsid = response_assignment.json()[apis_urls.assignementsactionAPI][str(ids)][
            #                         'assignments']
            #                     for dataid in assignmentsid:
            response = requests.delete(
                apis_urls.serverURL + "policies/" + policies_ids + "/" + apis_urls.assignementsactionAPI , headers=headers)

# Step Definition Implementation:
# 1) Post subject assignment using the policy id, subject perimeter id, subject category, list of subject data ids
@Given('the following subject assignment exists')
def step_impl(context):
    logger.info("Given the following subject assignment exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "subject perimeter name: '" + row["subjectperimetername"] + "' subject data: '" + row[
                "subjectdata"] + "' and subject category: '" + row[
                "subjectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        perimeter_id = ""
        categoriesname = ""
        dataname = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        policies_id = commonfunctions.get_policyid(row['policyname'])
        perimeter_id = commonfunctions.get_subjectperimeterid(row['subjectperimetername'])
        categories_id = commonfunctions.get_subjectcategoryid(row['subjectcategory'])
        dataids = commonfunctions.get_subjectdataid(row['subjectdata'], categories_id, policies_id)
        data = {
            'id': perimeter_id,
            'category_id': categories_id,
            'data_id': dataids,
        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.assignementssubjectAPI,
            headers=headers, data=json.dumps(data))

        GeneralVariables.assignpolicyid['value'] = policies_id
        GeneralVariables.assignsubjectperimeterid['value'] = perimeter_id
        GeneralVariables.assignsubjectcategoryid['value'] = categories_id

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Post object assignment using the policy id, object perimeter id, object category, list of object data ids
@Given('the following object assignment exists')
def step_impl(context):
    logger.info("Given the following object assignment exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "object perimeter name: '" + row["objectperimetername"] + "' object data: '" + row[
                "objectdata"] + "' and object category: '" + row[
                "objectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        perimeter_id = ""
        categoriesname = ""
        dataname = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        policies_id = commonfunctions.get_policyid(row['policyname'])
        perimeter_id = commonfunctions.get_objectperimeterid(row['objectperimetername'])
        categories_id = commonfunctions.get_objectcategoryid(row['objectcategory'])
        dataids = commonfunctions.get_objectdataid(row['objectdata'], categories_id, policies_id)

        data = {
            'id': perimeter_id,
            'category_id': categories_id,
            'policy_id': policies_id,
            'data_id': dataids,
        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.assignementsobjectAPI,
            headers=headers, data=json.dumps(data))

        GeneralVariables.assignpolicyid['value'] = policies_id
        GeneralVariables.assignobjectperimeterid['value'] = perimeter_id
        GeneralVariables.assignobjectcategoryid['value'] = categories_id

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Post action assignment using the policy id, action perimeter id, action category, list of action data ids
@Given('the following action assignment exists')
def step_impl(context):
    logger.info("Given the following action assignment exists")
    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "action perimeter name: '" + row["actionperimetername"] + "' action data: '" + row[
                "actiondata"] + "' and action category: '" + row[
                "actioncategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        perimeter_id = ""
        categoriesname = ""
        dataname = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        policies_id = commonfunctions.get_policyid(row['policyname'])
        perimeter_id = commonfunctions.get_actionperimeterid(row['actionperimetername'])
        categories_id = commonfunctions.get_actioncategoryid(row['actioncategory'])
        dataids = commonfunctions.get_actiondataid(row['actiondata'], categories_id, policies_id)

        data = {
            'id': perimeter_id,
            'category_id': categories_id,
            'policy_id': policies_id,
            'data_id': dataids,
        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.assignementsactionAPI,
            headers=headers, data=json.dumps(data))

        GeneralVariables.assignpolicyid['value'] = policies_id
        GeneralVariables.assignactionperimeterid['value'] = perimeter_id
        GeneralVariables.assignactioncategoryid['value'] = categories_id

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Post action assignment using the policy id, action perimeter id, action category, list of action data ids
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following subject assignment')
def step_impl(context):
    logger.info("When the user sets to add the following subject assignment")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "subject perimeter name: '" + row["subjectperimetername"] + "' subject data: '" + row[
                "subjectdata"] + "' and subject category: '" + row[
                "subjectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        perimeter_id = ""
        categoriesname = ""
        dataids = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policyname'] == "" or row['policyname'] == "000000000000000000000000000000000000000000000000000"):
            policyname = "Stanford Policy"
        else:
            policyname = row['policyname']
        policies_id = commonfunctions.get_policyid(policyname)

        if (row["subjectperimetername"] == "" or row[
            "subjectperimetername"] == "000000000000000000000000000000000000000000000000000"):
            perimetername = "WilliamsJoeseph"
        else:
            perimetername = row["subjectperimetername"]
        perimeter_id = commonfunctions.get_subjectperimeterid(perimetername)

        if (row["subjectcategory"] == "" or row[
            "subjectcategory"] == "000000000000000000000000000000000000000000000000000"):
            categoriesname = "Affiliation:"
        else:
            categoriesname = row['subjectcategory']
        categories_id = commonfunctions.get_subjectcategoryid(categoriesname)

        if (row["subjectdata"] == "" or row["subjectdata"] == "000000000000000000000000000000000000000000000000000"):
            dataids = "Professor"
        else:
            dataids = row['subjectdata']
        dataids = commonfunctions.get_subjectdataid(dataids, categories_id, policies_id)

        if (dataids == None):
            dataids = ""

        if (row["policyname"] == "" or row["policyname"] == "000000000000000000000000000000000000000000000000000"):
            policies_id = row["policyname"]
        if (row["subjectperimetername"] == "" or row[
            "subjectperimetername"] == "000000000000000000000000000000000000000000000000000"):
            perimeter_id = row["subjectperimetername"]
        if (row["subjectcategory"] == "" or row[
            "subjectcategory"] == "000000000000000000000000000000000000000000000000000"):
            categories_id = row["subjectcategory"]
        if (row["subjectdata"] == "" or row["subjectdata"] == "000000000000000000000000000000000000000000000000000"):
            dataids = row['subjectdata']
        data = {
            'id': perimeter_id,
            'category_id': categories_id,
            'data_id': dataids,
        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.assignementssubjectAPI,
            headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Post action assignment using the policy id, action perimeter id, action category, list of action data ids
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following object assignment')
def step_impl(context):
    logger.info("When the user sets to add the following object assignment")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "object perimeter name: '" + row["objectperimetername"] + "' object data: '" + row[
                "objectdata"] + "' and object category: '" + row[
                "objectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        perimeter_id = ""
        categoriesname = ""
        dataids = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policyname'] == "" or row['policyname'] == "000000000000000000000000000000000000000000000000000"):
            policyname = "Stanford Policy"
        else:
            policyname = row['policyname']
        policies_id = commonfunctions.get_policyid(policyname)

        if (row["objectperimetername"] == "" or row[
            "objectperimetername"] == "000000000000000000000000000000000000000000000000000"):
            perimetername = "StudentsGradesSheet"
        else:
            perimetername = row["objectperimetername"]
        perimeter_id = commonfunctions.get_objectperimeterid(perimetername)

        if (row["objectcategory"] == "" or row[
            "objectcategory"] == "000000000000000000000000000000000000000000000000000"):
            categoriesname = "Clearance:"
        else:
            categoriesname = row['objectcategory']
        categories_id = commonfunctions.get_objectcategoryid(categoriesname)

        if (row["objectdata"] == "" or row["objectdata"] == "000000000000000000000000000000000000000000000000000"):
            dataids = "Confidential"
        else:
            dataids = row['objectdata']
        dataids = commonfunctions.get_objectdataid(dataids, categories_id, policies_id)

        if (dataids == None):
            dataids = ""

        if (row["policyname"] == "" or row["policyname"] == "000000000000000000000000000000000000000000000000000"):
            policies_id = row["policyname"]
        if (row["objectperimetername"] == "" or row[
            "objectperimetername"] == "000000000000000000000000000000000000000000000000000"):
            perimeter_id = row["objectperimetername"]
        if (row["objectcategory"] == "" or row[
            "objectcategory"] == "000000000000000000000000000000000000000000000000000"):
            categories_id = row["objectcategory"]
        if (row["objectdata"] == "" or row["objectdata"] == "000000000000000000000000000000000000000000000000000"):
            dataids = row['objectdata']
        data = {
            'id': perimeter_id,
            'category_id': categories_id,
            'data_id': dataids,
        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.assignementsobjectAPI,
            headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Post action assignment using the policy id, action perimeter id, action category, list of action data ids
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following action assignment')
def step_impl(context):
    logger.info("When the user sets to add the following action assignment")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "action perimeter name: '" + row["actionperimetername"] + "' action data: '" + row[
                "actiondata"] + "' and action category: '" + row[
                "actioncategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        perimeter_id = ""
        categoriesname = ""
        dataids = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (row['policyname'] == "" or row['policyname'] == "000000000000000000000000000000000000000000000000000"):
            policyname = "Stanford Policy"
        else:
            policyname = row['policyname']
        policies_id = commonfunctions.get_policyid(policyname)

        if (row["actionperimetername"] == "" or row[
            "actionperimetername"] == "000000000000000000000000000000000000000000000000000"):
            perimetername = "Read"
        else:
            perimetername = row["actionperimetername"]
        perimeter_id = commonfunctions.get_actionperimeterid(perimetername)

        if (row["actioncategory"] == "" or row[
            "actioncategory"] == "000000000000000000000000000000000000000000000000000"):
            categoriesname = "Action-Class:"
        else:
            categoriesname = row['actioncategory']
        categories_id = commonfunctions.get_actioncategoryid(categoriesname)

        if (row["actiondata"] == "" or row["actiondata"] == "000000000000000000000000000000000000000000000000000"):
            dataids = "Severe"
        else:
            dataids = row['actiondata']
        dataids = commonfunctions.get_actiondataid(dataids, categories_id, policies_id)

        if (dataids == None):
            dataids = ""

        if (row["policyname"] == "" or row["policyname"] == "000000000000000000000000000000000000000000000000000"):
            policies_id = row["policyname"]
        if (row["actionperimetername"] == "" or row[
            "actionperimetername"] == "000000000000000000000000000000000000000000000000000"):
            perimeter_id = row["actionperimetername"]
        if (row["actioncategory"] == "" or row[
            "actioncategory"] == "000000000000000000000000000000000000000000000000000"):
            categories_id = row["actioncategory"]
        if (row["actiondata"] == "" or row["actiondata"] == "000000000000000000000000000000000000000000000000000"):
            dataids = row['actiondata']
        data = {
            'id': perimeter_id,
            'category_id': categories_id,
            'policy_id': policies_id,
            'data_id': dataids,
        }
        response = requests.post(
            apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.assignementsactionAPI,
            headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Delete subject assignment by policy id,subject perimeter id, subject data id, subject category id
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following subject assignment')
def step_impl(context):
    logging.info("When the user sets to delete the following subject assignment")
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "subject perimeter name: '" + row["subjectperimetername"] + "' subject data list: '" + row[
                "subjectdata"] + "' and subject category: '" + row[
                "subjectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        perimeter_id = ""
        dataid = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        policies_id = commonfunctions.get_policyid(row['policyname'])
        perimeter_id = commonfunctions.get_subjectperimeterid(row['subjectperimetername'])
        categories_id = commonfunctions.get_subjectcategoryid(row['subjectcategory'])
        dataid = commonfunctions.get_subjectdataid(row["subjectdata"], categories_id, policies_id)

        response_assignment = requests.get(
            apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.assignementssubjectAPI + "/" +
            perimeter_id + "/" + categories_id, headers=apis_urls.auth_headers)
        logging.info(response_assignment.json()[apis_urls.assignementssubjectAPI])
        if len(response_assignment.json()[apis_urls.assignementssubjectAPI]) != 0:
            for ids in dict(response_assignment.json()[apis_urls.assignementssubjectAPI]).keys():
                assignmentsidlist = response_assignment.json()[apis_urls.assignementssubjectAPI][str(ids)][
                    'assignments']
                if dataid in assignmentsidlist:
                    response = requests.delete(
                        apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.assignementssubjectAPI + "/" +
                        perimeter_id + "/" + categories_id + "/" + dataid, headers=apis_urls.auth_headers)

                    if response.status_code == 200:
                        GeneralVariables.api_responseflag['value'] = 'True'
                    else:
                        GeneralVariables.api_responseflag['value'] = 'False'


# Step Definition Implementation:
# 1) Delete object assignment by policy id, object perimeter id, object data id, object category id
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following object assignment')
def step_impl(context):
    logging.info("When the user sets to delete the following object assignment")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "object perimeter name: '" + row["objectperimetername"] + "' object data list: '" + row[
                "objectdata"] + "' and object category: '" + row[
                "objectcategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        perimeter_id = ""
        datalistids = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        policies_id = commonfunctions.get_policyid(row['policyname'])
        perimeter_id = commonfunctions.get_objectperimeterid(row['objectperimetername'])
        categories_id = commonfunctions.get_objectcategoryid(row['objectcategory'])
        dataid = commonfunctions.get_objectdataid(row["objectdata"], categories_id, policies_id)

        response_assignment = requests.get(
            apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.assignementsobjectAPI + "/" +
            perimeter_id + "/" + categories_id, headers=apis_urls.auth_headers)
        if len(response_assignment.json()[apis_urls.assignementsobjectAPI]) != 0:
            for ids in dict(response_assignment.json()[apis_urls.assignementsobjectAPI]).keys():
                assignmentsidlist = response_assignment.json()[apis_urls.assignementsobjectAPI][str(ids)][
                    'assignments']
                if dataid in assignmentsidlist:
                    response = requests.delete(
                        apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.assignementsobjectAPI + "/" +
                        perimeter_id + "/" + categories_id + "/" + dataid, headers=headers)

                    if response.status_code == 200:
                        GeneralVariables.api_responseflag['value'] = 'True'
                    else:
                        GeneralVariables.api_responseflag['value'] = 'False'


# Step Definition Implementation:
# 1) Delete action assignment by policy id, action perimeter id, action data id, action category id
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following action assignment')
def step_impl(context):
    logging.info("When the user sets to delete the following action assignment")

    model = getattr(context, "model", None)
    for row in context.table:
        logger.info(
            "action perimeter name: '" + row["actionperimetername"] + "' action data list: '" + row[
                "actiondata"] + "' and action category: '" + row[
                "actioncategory"] + "' and policies: '" + row['policyname'] + "'")

        policies_id = ""
        perimeter_id = ""
        datalistids = ""
        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        policies_id = commonfunctions.get_policyid(row['policyname'])
        perimeter_id = commonfunctions.get_actionperimeterid(row['actionperimetername'])
        categories_id = commonfunctions.get_actioncategoryid(row['actioncategory'])
        dataid = commonfunctions.get_actiondataid(row["actiondata"], categories_id, policies_id)

        response_assignment = requests.get(
            apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.assignementsactionAPI + "/" +
            perimeter_id + "/" + categories_id, headers=apis_urls.auth_headers)
        if len(response_assignment.json()[apis_urls.assignementsactionAPI]) != 0:
            for ids in dict(response_assignment.json()[apis_urls.assignementsactionAPI]).keys():
                assignmentsidlist = response_assignment.json()[apis_urls.assignementsactionAPI][str(ids)][
                    'assignments']
                if dataid in assignmentsidlist:
                    response = requests.delete(
                        apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.assignementsactionAPI + "/" +
                        perimeter_id + "/" + categories_id + "/" + dataid, headers=apis_urls.auth_headers)

                    if response.status_code == 200:
                        GeneralVariables.api_responseflag['value'] = 'True'
                    else:
                        GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the existing subject assignment per a given policy, subject perimeter and subject category by get request and put them into a table
# 2) Sort the table by subject perimeter name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following subject assignment should be existed in the system')
def step_impl(context):
    logger.info("Then the following subject assignment should be existed in the system")
    model = getattr(context, "model", None)
    apiresult = Table(names=('subjectperimetername', 'subjectcategory', 'subjectdata', 'policyname'),
                      dtype=('S100', 'S100', 'S100', 'S100'))
    for row in context.table:
        logger.info(
            "subject perimeter name: '" + row["subjectperimetername"] + "' subject data list: '" + row[
                "subjectdata"] + "' and subject category: '" + row[
                "subjectcategory"] + "' and policies: '" + row['policyname'] + "'")
        if (row['policyname'] == "" or row['subjectperimetername'] == ""):
            response = requests.get(
                apis_urls.serverURL + "policies/" + GeneralVariables.assignpolicyid[
                    'value'] + "/" + apis_urls.assignementssubjectAPI + "/" +
                GeneralVariables.assignsubjectperimeterid['value'] + "/" +
                GeneralVariables.assignsubjectcategoryid['value'], headers=apis_urls.auth_headers)
        else:
            response = requests.get(
                apis_urls.serverURL + "policies/" + commonfunctions.get_policyid(
                    row['policyname']) + "/" + apis_urls.assignementssubjectAPI + "/" +
                commonfunctions.get_subjectperimeterid(row['subjectperimetername']) + "/" +
                commonfunctions.get_subjectcategoryid(row['subjectcategory']), headers=apis_urls.auth_headers)
        if len(response.json()[apis_urls.assignementssubjectAPI]) != 0:
            for ids in dict(response.json()[apis_urls.assignementssubjectAPI]).keys():
                apipolicies = ""
                apisubjectname = commonfunctions.get_subjectperimetername(
                    response.json()[apis_urls.assignementssubjectAPI][str(ids)]['subject_id'])
                apisubjectcategory = commonfunctions.get_subjectcategoryname(
                    response.json()[apis_urls.assignementssubjectAPI][str(ids)]['category_id'])
                apiassignments = commonfunctions.get_subjectdataname(
                    response.json()[apis_urls.assignementssubjectAPI][str(ids)]['assignments'],
                    response.json()[apis_urls.assignementssubjectAPI][str(ids)]['category_id'],
                    response.json()[apis_urls.assignementssubjectAPI][str(ids)]['policy_id'])
                apipolicies = commonfunctions.get_policyname(
                    response.json()[apis_urls.assignementssubjectAPI][str(ids)]['policy_id'])
                if ((row['policyname'] == "" or row['subjectperimetername'] == "") and "".join(apiassignments)==""):
                    apiresult.add_row(vals=("", "", "", ""))
                else:
                    apiresult.add_row(vals=(
                        apisubjectname, apisubjectcategory, apiassignments, apipolicies))
        else:
            apiresult.add_row(vals=("", "", "", ""))

    apiresult.sort('subjectperimetername')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected subject perimeter name: '" + str(
            row1["subjectperimetername"]) + "' is the same as the actual existing '" + str(
            row2["subjectperimetername"]) + "'")
        assert str(row1["subjectperimetername"]) == str(
            row2["subjectperimetername"]), "subject perimeter name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected subject data description: '" + str(
            row1["subjectcategory"]) + "' is the same as the actual existing '" + str(
            row2["subjectcategory"]) + "'")
        assert str(row1["subjectcategory"]) == str(
            row2["subjectcategory"]), "subject category is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected subject data password: '" + str(
            row1["subjectdata"]) + "' is the same as the actual existing '" + str(
            row2["subjectdata"]) + "'")
        assert str(row1["subjectdata"]) == str(
            row2["subjectdata"]), "subject data list is not correct!"
        logger.info("assertion passed!")

        #logger.info("asserting the expected policies: '" + str(
        #    row1["policyname"]) + "' is the same as the actual existing '" + str(
        #    row2["policyname"]) + "'")
        #assert str(row1["policyname"]) == str(row2["policyname"]), " policies is not correct!"
        #logger.info("assertion passed!")

# Step Definition Implementation:
# 1) Get all the existing object assignment per a given policy, object perimeter and object category by get request and put them into a table
# 2) Sort the table by object perimeter name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following object assignment should be existed in the system')
def step_impl(context):
    logger.info("Then the following object assignment should be existed in the system")
    model = getattr(context, "model", None)
    apiresult = Table(names=('objectperimetername', 'objectcategory', 'objectdata', 'policyname'),
                      dtype=('S100', 'S100', 'S400', 'S100'))
    for row in context.table:
        if (row['policyname'] == "" or row['objectperimetername'] == ""):
            response = requests.get(
                apis_urls.serverURL + "policies/" + GeneralVariables.assignpolicyid[
                    'value'] + "/" + apis_urls.assignementsobjectAPI + "/" +
                GeneralVariables.assignobjectperimeterid['value'] + "/" +
                GeneralVariables.assignobjectcategoryid['value'], headers=apis_urls.auth_headers)
        else:
            response = requests.get(
                apis_urls.serverURL + "policies/" + commonfunctions.get_policyid(
                    row['policyname']) + "/" + apis_urls.assignementsobjectAPI + "/" +
                commonfunctions.get_objectperimeterid(row['objectperimetername']) + "/" +
                commonfunctions.get_objectcategoryid(row['objectcategory']), headers=apis_urls.auth_headers)

        if len(response.json()[apis_urls.assignementsobjectAPI]) != 0:
            for ids in dict(response.json()[apis_urls.assignementsobjectAPI]).keys():
                apipolicies = ""
                apiobjectname = commonfunctions.get_objectperimetername(
                    response.json()[apis_urls.assignementsobjectAPI][str(ids)]['object_id'])
                apiobjectcategory = commonfunctions.get_objectcategoryname(
                    response.json()[apis_urls.assignementsobjectAPI][str(ids)]['category_id'])
                apiassignments = commonfunctions.get_objectdataname(
                    response.json()[apis_urls.assignementsobjectAPI][str(ids)]['assignments'],
                    response.json()[apis_urls.assignementsobjectAPI][str(ids)]['category_id'],
                    response.json()[apis_urls.assignementsobjectAPI][str(ids)]['policy_id'])
                apipolicies = commonfunctions.get_policyname(
                    response.json()[apis_urls.assignementsobjectAPI][str(ids)]['policy_id'])
                if ((row['policyname'] == "" or row['objectperimetername'] == "") and "".join(apiassignments) == ""):
                    apiresult.add_row(vals=("", "", "", ""))
                else:
                    apiresult.add_row(vals=(
                        apiobjectname, apiobjectcategory, ",".join(apiassignments), apipolicies))
        else:
            apiresult.add_row(vals=("", "", "", ""))

    apiresult.sort('objectperimetername')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected object perimeter name: '" + str(
            row1["objectperimetername"]) + "' is the same as the actual existing '" + str(
            row2["objectperimetername"]) + "'")
        assert str(row1["objectperimetername"]) == str(
            row2["objectperimetername"]), "object perimeter name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected object data description: '" + str(
            row1["objectcategory"]) + "' is the same as the actual existing '" + str(
            row2["objectcategory"]) + "'")
        assert str(row1["objectcategory"]) == str(
            row2["objectcategory"]), "object category is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected object data password: '" + str(
            row1["objectdata"]) + "' is the same as the actual existing '" + str(
            row2["objectdata"]) + "'")
        assert str(row1["objectdata"]) == str(
            row2["objectdata"]), "object data list is not correct!"
        logger.info("assertion passed!")

        #logger.info("asserting the expected policies: '" + str(
        #    row1["policyname"]) + "' is the same as the actual existing '" + str(
        #    row2["policyname"]) + "'")
        #assert str(row1["policyname"]) == str(row2["policyname"]), " policies is not correct!"
        #logger.info("assertion passed!")

# Step Definition Implementation:
# 1) Get all the existing action assignment per a given policy, action perimeter and action category by get request and put them into a table
# 2) Sort the table by action perimeter name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following action assignment should be existed in the system')
def step_impl(context):
    logger.info("Then the following action assignment should be existed in the system")
    model = getattr(context, "model", None)
    apiresult = Table(names=('actionperimetername', 'actioncategory', 'actiondata', 'policyname'),
                      dtype=('S100', 'S100', 'S100', 'S100'))
    for row in context.table:
        if (row['policyname'] == "" or row['actionperimetername'] == ""):
            response = requests.get(
                apis_urls.serverURL + "policies/" + GeneralVariables.assignpolicyid[
                    'value'] + "/" + apis_urls.assignementsactionAPI + "/" +
                GeneralVariables.assignactionperimeterid['value'] + "/" +
                GeneralVariables.assignactioncategoryid['value'], headers=apis_urls.auth_headers)
        else:
            response = requests.get(
                apis_urls.serverURL + "policies/" + commonfunctions.get_policyid(
                    row['policyname']) + "/" + apis_urls.assignementsactionAPI + "/" +
                commonfunctions.get_actionperimeterid(row['actionperimetername']) + "/" +
                commonfunctions.get_actioncategoryid(row['actioncategory']), headers=apis_urls.auth_headers)

        if len(response.json()[apis_urls.assignementsactionAPI]) != 0:
            for ids in dict(response.json()[apis_urls.assignementsactionAPI]).keys():
                apipolicies = ""
                apiactionname = commonfunctions.get_actionperimetername(
                    response.json()[apis_urls.assignementsactionAPI][str(ids)]['action_id'])
                apiactioncategory = commonfunctions.get_actioncategoryname(
                    response.json()[apis_urls.assignementsactionAPI][str(ids)]['category_id'])
                apiassignments = commonfunctions.get_actiondataname(
                    response.json()[apis_urls.assignementsactionAPI][str(ids)]['assignments'],
                    response.json()[apis_urls.assignementsactionAPI][str(ids)]['category_id'],
                    response.json()[apis_urls.assignementsactionAPI][str(ids)]['policy_id'])
                apipolicies = commonfunctions.get_policyname(
                    response.json()[apis_urls.assignementsactionAPI][str(ids)]['policy_id'])
                logger.info(apiassignments)
                if ((row['policyname'] == "" or row['actionperimetername'] == "") and "".join(apiassignments) == ""):
                    apiresult.add_row(vals=("", "", "", ""))
                else:
                    apiresult.add_row(vals=(
                        apiactionname, apiactioncategory, apiassignments, apipolicies))
        else:
            apiresult.add_row(vals=("", "", "", ""))

    apiresult.sort('actionperimetername')
    for row1, row2 in zip(context.table, apiresult):
        logger.info("asserting the expected action perimeter name: '" + str(
            row1["actionperimetername"]) + "' is the same as the actual existing '" + str(
            row2["actionperimetername"]) + "'")
        assert str(row1["actionperimetername"]) == str(
            row2["actionperimetername"]), "action perimeter name is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected action data description: '" + str(
            row1["actioncategory"]) + "' is the same as the actual existing '" + str(
            row2["actioncategory"]) + "'")
        assert str(row1["actioncategory"]) == str(
            row2["actioncategory"]), "action category is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected action data password: '" + str(
            row1["actiondata"]) + "' is the same as the actual existing '" + str(
            row2["actiondata"]) + "'")
        assert str(row1["actiondata"]) == str(
            row2["actiondata"]), "action data list is not correct!"
        logger.info("assertion passed!")

        #logger.info("asserting the expected policies: '" + str(
        #    row1["policyname"]) + "' is the same as the actual existing '" + str(
        #    row2["policyname"]) + "'")
        #assert str(row1["policyname"]) == str(row2["policyname"]), " policies is not correct!"
        #logger.info("assertion passed!")
