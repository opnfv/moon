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
# 1) Get all the existing rules by the policy id
# 2) Loop by assignment id and delete it
@Given('the system has no rules')
def step_impl(context):
    logger.info("Given the system has no rules")

    response_policies = requests.get(apis_urls.serverURL + apis_urls.policyAPI, headers=apis_urls.auth_headers)
    #logger.info(response_policies.json())
    if len(response_policies.json()[apis_urls.policyAPI]) != 0:
        apiruleid = []
        for policies_ids in dict(response_policies.json()[apis_urls.policyAPI]).keys():
            response = requests.get(
                apis_urls.serverURL + "policies/" + policies_ids + "/" + apis_urls.rulesAPI + "/", headers=apis_urls.auth_headers)
            if len(response.json()[apis_urls.rulesAPI]['rules']) != 0:
                for ids in range(len(response.json()[apis_urls.rulesAPI]['rules'])):
                    apiruleid.append(dict(response.json()[apis_urls.rulesAPI]['rules'][ids])['id'])
                for ruleid in apiruleid:
                    response = requests.delete(
                        apis_urls.serverURL + "policies/" + policies_ids + "/" + apis_urls.rulesAPI + "/" + ruleid, headers=apis_urls.auth_headers)

# Step Definition Implementation:
# 1) Add rule using the post request
@Given('the following rule exists')
def step_impl(context):
    logger.info("Given the following rule exists")
    api_responseflag = {'value': False}
    model = getattr(context, "model", None)
    for row in context.table:
        subjectcategoryidslist = []
        subjectdataidslist = []
        objectcategoryidslist = []
        objectdataidslist = []
        actioncategoryidslist = []
        actiondataidslist = []
        ruleidslist = []
        metaruleids = ""
        subjectindex = 0
        objectindex = 0
        actionindex = 0
        logger.info(
            "rule '" + row["rule"] + "' and metarule name:'" + row[
                "metarulename"] + "' and instructions: '" + row[
                "instructions"] + "' and policyname:'" + row[
                "policyname"] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['policyname']) > 25):
            policies_id = row['policyname']
        else:
            policies_id = commonfunctions.get_policyid(row['policyname'])

        ruleparameter = row["rule"].split(",")
        metarules_response = requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers)
        for metaruleids in dict(metarules_response.json()[apis_urls.metarulesAPI]).keys():
            if (metarules_response.json()[apis_urls.metarulesAPI][metaruleids]['name'] == row["metarulename"]):
                meta_rule_id = metaruleids
                subjectcategorieslist = \
                    requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                        metaruleids]['subject_categories']
                objectcategorieslist = \
                    requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                        metaruleids]['object_categories']
                actioncategorieslist = \
                    requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                        metaruleids]['action_categories']
                break

        index = 0
        for categoryid in subjectcategorieslist:
            data_response = requests.get(
                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.datasubjectAPI + "/" + categoryid, headers=apis_urls.auth_headers)
            if len(data_response.json()[apis_urls.datasubjectAPI]) != 0:
                for ids in data_response.json()[apis_urls.datasubjectAPI][0]['data']:
                    if (data_response.json()[apis_urls.datasubjectAPI][0]['data'][str(ids)]['name'] == ruleparameter[
                        index]):
                        ruleidslist.append(ids)
            index = index + 1

        for categoryid in objectcategorieslist:
            data_response = requests.get(
                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.dataobjectAPI + "/" + categoryid, headers=apis_urls.auth_headers)
            if len(data_response.json()[apis_urls.dataobjectAPI]) != 0:
                for ids in data_response.json()[apis_urls.dataobjectAPI][0]['data']:
                    if (data_response.json()[apis_urls.dataobjectAPI][0]['data'][str(ids)]['name'] == ruleparameter[
                        index]):
                        ruleidslist.append(ids)
            index = index + 1
        for categoryid in actioncategorieslist:
            data_response = requests.get(
                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.dataactionAPI + "/" + categoryid, headers=apis_urls.auth_headers)
            if len(data_response.json()[apis_urls.dataactionAPI]) != 0:
                for ids in data_response.json()[apis_urls.dataactionAPI][0]['data']:
                    if (data_response.json()[apis_urls.dataactionAPI][0]['data'][str(ids)]['name'] == ruleparameter[
                        index]):
                        ruleidslist.append(ids)
            index = index + 1

    data = {
        'meta_rule_id': meta_rule_id,
        'rule': ruleidslist,
        'instructions': [{"decision": row['instructions']}],
        'enabled': 'True'
    }
    rulesresponse = requests.post(apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.rulesAPI,
                                  headers=headers,
                                  data=json.dumps(data))


# Step Definition Implementation:
# 1) Add subject meta data using the post request
# 2) If the request code was 200 set the api response flag to true else false
@When('the user sets to add the following rules')
def step_impl(context):
    logger.info("When the user sets to add the following rules")
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
    api_responseflag = {'value': False}
    model = getattr(context, "model", None)
    for row in context.table:
        subjectcategoryidslist = []
        subjectdataidslist = []
        objectcategoryidslist = []
        objectdataidslist = []
        actioncategoryidslist = []
        actiondataidslist = []
        ruleidslist = []
        metaruleids = ""
        subjectindex = 0
        objectindex = 0
        actionindex = 0
        logger.info(
            "rule '" + row["rule"] + "' and metarule name:'" + row[
                "metarulename"] + "' and instructions: '" + row[
                "instructions"] + "' and policyname:'" + row[
                "policyname"] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if(row['policyname']=="" or row['policyname']=="000000000000000000000000000000000000000000000000000"):
            policyname="Stanford Policy"
        else:
            policyname=row['policyname']
        policies_id = commonfunctions.get_policyid(policyname)

        if(row["metarulename"]=="" or row["metarulename"]=="000000000000000000000000000000000000000000000000000"):
            mata_rule_name="metarule1"
        else:
            mata_rule_name = row['metarulename']


        if (row["rule"] != ""):
            ruleparameter = row["rule"].split(",")
            metarules_response = requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers)
            for metaruleids in dict(metarules_response.json()[apis_urls.metarulesAPI]).keys():
                if (metarules_response.json()[apis_urls.metarulesAPI][metaruleids]['name'] == mata_rule_name):
                    meta_rule_id = metaruleids
                    subjectcategorieslist = \
                        requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                            metaruleids]['subject_categories']
                    objectcategorieslist = \
                        requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                            metaruleids]['object_categories']
                    actioncategorieslist = \
                        requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                            metaruleids]['action_categories']
                    break

            index = 0
            for categoryid in subjectcategorieslist:
                if (index < len(ruleparameter)):
                    if (len(ruleparameter[index]) < 30):
                        if (ruleparameter[index] != ""):
                            data_response = requests.get(
                                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.datasubjectAPI + "/" + categoryid, headers=apis_urls.auth_headers)
                            if len(data_response.json()[apis_urls.datasubjectAPI]) != 0:
                                for ids in data_response.json()[apis_urls.datasubjectAPI][0]['data']:
                                    if (index < len(ruleparameter)):
                                        if (data_response.json()[apis_urls.datasubjectAPI][0]['data'][str(ids)][
                                            'name'] ==
                                                ruleparameter[
                                                    index]):
                                            ruleidslist.append(ids)
                                            index = index + 1
                                    else:
                                        break
                        else:
                            ruleidslist.append("")
                            index = index + 1
                    else:
                        ruleidslist.append(ruleparameter[index])
                        index = index + 1
            for categoryid in objectcategorieslist:
                if (index < len(ruleparameter)):
                    if (len(ruleparameter[index]) < 30):
                        if (ruleparameter[index] != ""):
                            data_response = requests.get(
                                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.dataobjectAPI + "/" + categoryid, headers=apis_urls.auth_headers)
                            if len(data_response.json()[apis_urls.dataobjectAPI]) != 0:
                                for ids in data_response.json()[apis_urls.dataobjectAPI][0]['data']:
                                    if (index < len(ruleparameter)):
                                        if (data_response.json()[apis_urls.dataobjectAPI][0]['data'][str(ids)][
                                            'name'] == ruleparameter[
                                            index]):
                                            ruleidslist.append(ids)
                                            index = index + 1
                                    else:
                                        break
                        else:
                            ruleidslist.append("")
                            index = index + 1
                    else:
                        ruleidslist.append(ruleparameter[index])
                        index = index + 1

            for categoryid in actioncategorieslist:
                if (index < len(ruleparameter)):
                    if (len(ruleparameter[index]) < 30):
                        if (ruleparameter[index] != ""):
                            data_response = requests.get(
                                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.dataactionAPI + "/" + categoryid, headers=apis_urls.auth_headers)
                            if len(data_response.json()[apis_urls.dataactionAPI]) != 0:
                                for ids in data_response.json()[apis_urls.dataactionAPI][0]['data']:
                                    if (index < len(ruleparameter)):
                                        if (data_response.json()[apis_urls.dataactionAPI][0]['data'][str(ids)][
                                            'name'] == ruleparameter[
                                            index]):
                                            ruleidslist.append(ids)
                                            index = index + 1
                                    else:
                                        break
                        else:
                            ruleidslist.append("")
                            index = index + 1
                    else:
                        ruleidslist.append(ruleparameter[index])
                        index = index + 1
            if(row["metarulename"]=="" or row["metarulename"] == "000000000000000000000000000000000000000000000000000"):
                meta_rule_id=row["metarulename"]
            if (row["policyname"] == "" or row["policyname"] == "000000000000000000000000000000000000000000000000000"):
                policies_id = row["policyname"]
            data = {
                'meta_rule_id': meta_rule_id,
                'rule': ruleidslist,
                'instructions': [{"decision": row['instructions']}],
                'enabled': 'True'
            }
        else:

            data = {
                'meta_rule_id': commonfunctions.get_metaruleid(mata_rule_name),
                'rule': [],
                'instructions': [{"decision": row['instructions']}],
                'enabled': 'True'
            }
        rulesresponse = requests.post(apis_urls.serverURL + "policies/" + str(policies_id) + "/" + apis_urls.rulesAPI,
                                      headers=headers,
                                      data=json.dumps(data))
        logger.info(rulesresponse.json())
        if rulesresponse.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the meta rule by get request
# 2) Loop by ids and search for the matching meta rule by name and delete it
# 3) If the request code was 200 set the api response flag to true else false
@When('the user sets to delete the following rules')
def step_impl(context):
    logger.info("When the user sets to delete the following rules")
    for row in context.table:
        subjectcategoryidslist = []
        subjectdataidslist = []
        objectcategoryidslist = []
        objectdataidslist = []
        actioncategoryidslist = []
        actiondataidslist = []
        ruleidslist = []
        metaruleids = ""
        subjectindex = 0
        objectindex = 0
        actionindex = 0
        logger.info(
            "rule '" + row["rule"] + "' and metarule name:'" + row[
                "metarulename"] + "' and policyname:'" + row[
                "policyname"] + "'")

        headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}

        if (len(row['policyname']) > 25):
            policies_id = row['policyname']
        else:
            policies_id = commonfunctions.get_policyid(row['policyname'])

        ruleparameter = row["rule"].split(",")
        metarules_response = requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers)
        for metaruleids in dict(metarules_response.json()[apis_urls.metarulesAPI]).keys():
            if (metarules_response.json()[apis_urls.metarulesAPI][metaruleids]['name'] == row["metarulename"]):
                meta_rule_id = metaruleids
                subjectcategorieslist = \
                    requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                        metaruleids]['subject_categories']
                objectcategorieslist = \
                    requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                        metaruleids]['object_categories']
                actioncategorieslist = \
                    requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                        metaruleids]['action_categories']
                break

        index = 0
        for categoryid in subjectcategorieslist:
            data_response = requests.get(
                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.datasubjectAPI + "/" + categoryid, headers=apis_urls.auth_headers)
            if len(data_response.json()[apis_urls.datasubjectAPI]) != 0:
                for ids in data_response.json()[apis_urls.datasubjectAPI][0]['data']:
                    if (data_response.json()[apis_urls.datasubjectAPI][0]['data'][str(ids)]['name'] == ruleparameter[
                        index]):
                        ruleidslist.append(ids)
            index = index + 1

        for categoryid in objectcategorieslist:
            data_response = requests.get(
                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.dataobjectAPI + "/" + categoryid, headers=apis_urls.auth_headers)
            if len(data_response.json()[apis_urls.dataobjectAPI]) != 0:
                for ids in data_response.json()[apis_urls.dataobjectAPI][0]['data']:
                    if (data_response.json()[apis_urls.dataobjectAPI][0]['data'][str(ids)]['name'] == ruleparameter[
                        index]):
                        ruleidslist.append(ids)
            index = index + 1
        for categoryid in actioncategorieslist:
            data_response = requests.get(
                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.dataactionAPI + "/" + categoryid, headers=apis_urls.auth_headers)
            if len(data_response.json()[apis_urls.dataactionAPI]) != 0:
                for ids in data_response.json()[apis_urls.dataactionAPI][0]['data']:
                    if (data_response.json()[apis_urls.dataactionAPI][0]['data'][str(ids)]['name'] == ruleparameter[
                        index]):
                        ruleidslist.append(ids)
            index = index + 1

        rulesresponse = requests.get(
            apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.rulesAPI + "/", headers=apis_urls.auth_headers)

        if len(rulesresponse.json()[apis_urls.rulesAPI]) != 0:
            for ids in range(len(rulesresponse.json()[apis_urls.rulesAPI]['rules'])):
                if (dict(rulesresponse.json()[apis_urls.rulesAPI]['rules'][ids])[
                    'rule'] == ruleidslist):
                    ruleid = dict(rulesresponse.json()[apis_urls.rulesAPI]['rules'][ids])['id']
                    rulesresponse = requests.delete(
                        apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.rulesAPI + "/" + ruleid,headers=apis_urls.auth_headers)

        if rulesresponse.status_code == 200:
            GeneralVariables.api_responseflag['value'] = 'True'
        else:
            GeneralVariables.api_responseflag['value'] = 'False'

# Step Definition Implementation:
# 1) Get all the existing rules per a given policy, metarule using get request and put them into a table
# 2) Sort the table by policy name
# 3) Loop using both the expected and actual tables and assert the data row by row
@Then('the following rules should be existed in the system')
def step_impl(context):
    logger.info("Then the following rule should be existed in the system")
    model = getattr(context, "model", None)
    apiresult = Table(names=('rule', 'metarule', 'instructions', 'policyname'),
                      dtype=('S1000', 'S100', 'S100', 'S100'))

    expectedresult = Table(names=('rule', 'metarule', 'instructions', 'policyname'),
                           dtype=('S1000', 'S100', 'S100', 'S100'))

    for row in context.table:
        ruleidslist = []
        apirule = []
        if (len(row['policyname']) > 25):
            policies_id = row['policyname']
        else:
            policies_id = commonfunctions.get_policyid(row['policyname'])

        ruleparameter = row["rule"].split(",")
        metarules_response = requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers)
        for metaruleids in dict(metarules_response.json()[apis_urls.metarulesAPI]).keys():
            if (metarules_response.json()[apis_urls.metarulesAPI][metaruleids]['name'] == row["metarulename"]):
                meta_rule_id = metaruleids
                subjectcategorieslist = \
                    requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                        metaruleids]['subject_categories']
                objectcategorieslist = \
                    requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                        metaruleids]['object_categories']
                actioncategorieslist = \
                    requests.get(apis_urls.serverURL + apis_urls.metarulesAPI, headers=apis_urls.auth_headers).json()[apis_urls.metarulesAPI][
                        metaruleids]['action_categories']

        index = 0
        for categoryid in subjectcategorieslist:
            data_response = requests.get(
                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.datasubjectAPI + "/" + categoryid, headers=apis_urls.auth_headers)
            if len(data_response.json()[apis_urls.datasubjectAPI]) != 0:
                for ids in data_response.json()[apis_urls.datasubjectAPI][0]['data']:
                    if (data_response.json()[apis_urls.datasubjectAPI][0]['data'][ids]['name'] == ruleparameter[
                        index]):
                        ruleidslist.append(ids)
            index = index + 1

        for categoryid in objectcategorieslist:
            data_response = requests.get(
                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.dataobjectAPI + "/" + categoryid, headers=apis_urls.auth_headers)
            if len(data_response.json()[apis_urls.dataobjectAPI]) != 0:
                for ids in data_response.json()[apis_urls.dataobjectAPI][0]['data']:
                    if (data_response.json()[apis_urls.dataobjectAPI][0]['data'][ids]['name'] == ruleparameter[
                        index]):
                        ruleidslist.append(ids)
            index = index + 1

        for categoryid in actioncategorieslist:
            data_response = requests.get(
                apis_urls.serverURL + "policies/" + policies_id + "/" + apis_urls.dataactionAPI + "/" + categoryid, headers=apis_urls.auth_headers)
            if len(data_response.json()[apis_urls.dataactionAPI]) != 0:
                for ids in data_response.json()[apis_urls.dataactionAPI][0]['data']:
                    if (data_response.json()[apis_urls.dataactionAPI][0]['data'][ids]['name'] == ruleparameter[
                        index]):
                        ruleidslist.append(ids)
            index = index + 1
        expectedresult.add_row(vals=(','.join(ruleidslist), meta_rule_id, row['instructions'], policies_id))

        if (row['policyname'] != ""):
            apipolicyid = commonfunctions.get_policyid(
                row['policyname'])
            response = requests.get(
                apis_urls.serverURL + "policies/" + commonfunctions.get_policyid(
                    row['policyname']) + "/" + apis_urls.rulesAPI + "/", headers=apis_urls.auth_headers)

            if len(response.json()[apis_urls.rulesAPI]) != 0:
                for ids in range(len(response.json()[apis_urls.rulesAPI]['rules'])):
                    if (dict(response.json()[apis_urls.rulesAPI]['rules'][ids])[
                        'meta_rule_id'] == commonfunctions.get_metaruleid(row['metarulename'])):
                        apirule = dict(response.json()[apis_urls.rulesAPI]['rules'][ids])['rule']
                        #logger.info(dict(dict(response.json()[apis_urls.rulesAPI]['rules'][ids])['instructions'][0])['decision'])
                        apiinstructions = dict(dict(response.json()[apis_urls.rulesAPI]['rules'][ids])['instructions'][0])['decision']
                        apimetaruleid = dict(response.json()[apis_urls.rulesAPI]['rules'][ids])['meta_rule_id']
                        apiresult.add_row(vals=(','.join(apirule), apimetaruleid, apiinstructions, apipolicyid))

            else:
                apiresult.add_row(vals=("", "", "", ""))

        else:
            apiresult.add_row(vals=("", "", "", ""))

    apiresult.sort('policyname')
    expectedresult.sort('policyname')
    for row1, row2 in zip(expectedresult, apiresult):
        logger.info("asserting the expected rule: '" + str(
            row1["rule"]) + "' is the same as the actual existing '" + str(
            row2["rule"]) + "'")
        assert str(row1["rule"]) == str(row2["rule"]), "rule is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected instructions: '" + str(
            row1["instructions"]) + "' is the same as the actual existing '" + str(
            row2["instructions"]) + "'")
        assert str(row1["instructions"]) == str(row2["instructions"]), "instructions is not correct!"
        logger.info("assertion passed!")

        logger.info("asserting the expected metarule: '" + str(
            row1["metarule"]) + "' is the same as the actual existing '" + str(
            row2["metarule"]) + "'")
        assert str(row1["metarule"]) == str(row2["metarule"]), "metarule is not correct!"
        logger.info("assertion passed!")
