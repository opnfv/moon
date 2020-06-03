# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from behave import *
from Static_Variables import GeneralVariables
from common_functions import *
import requests
import json
import logging
import paramiko

apis_urls = GeneralVariables()
commonfunctions = commonfunctions()

logger = logging.getLogger(__name__)

# Step Definition Implementation: Incomplete Step
# 1) Connect to the server
# 2) Launch Moon Manager
# 3) Set the token in the global variables
@Given('the manager is configured')
def step_impl(context):
    logger.info("\n")
    logger.info("******************** Scenario: " + context.scenario.name + " ********************")
    logger.info("Given the manager is configured")
    api_responseflag = {'value': False}
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    # client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=apis_urls.serverIP, port=apis_urls.serverport, username=apis_urls.serverusername,
                   password=apis_urls.serverpassword)
    logger.info("before ")
    stdin, stdout, stderr = client.exec_command(

        "sudo nohup hug -m moon_manager.server &"
        " /usr/bin/python3 "
    )
    #stdin, stdout, stderr = client.exec_command(" sudo /usr/local/bin/moon_manager add_user alaa00 admin")
    #stdin, stdout, stderr = client.exec_command(" sudo /usr/local/bin/moon_manager get_key alaa00 admin ")
    #logger.info(stdout.readlines())
    #GeneralVariables.auth_headers['X-Api-Key'] = str(stdout.readlines())
    #logger.info("token: " + str(GeneralVariables.auth_headers['X-Api-Key']))
    #logger.info("after ")
   # client.close()

# Step Definition Implementation: Incomplete Step
# 1) Get all the moon slaves
# 2) Loop on the slave by id and delete them
@Given('no slave is created')
def step_impl(context):
    logger.info("\n")
    logger.info("******************** Scenario: " + context.scenario.name + " ********************")
    logger.info("Given no slave is created")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
    response = requests.get(apis_urls.serverURL + apis_urls.getslavesAPI, headers=apis_urls.auth_headers)
    if len(response.json()[apis_urls.getslavesAPI]) != 0:
        for ids in dict(response.json()[apis_urls.getslavesAPI]).keys():
            response = requests.delete(apis_urls.serverURL + apis_urls.slaveAPI + "/" + ids,
                                       headers=headers)

# Step Definition Implementation:
# 1) Create a slave by post request
# 2) Get the wrapper port id from the slave posting request & set it to the wrapperPort global variable
@Given('the slave is created')
def step_impl(context):
    logger.info("Given the slave is created")
    api_responseflag = {'value': False}
    headers = {"Content-Type": "application/json", "X-Api-Key": apis_urls.token}
    data = {
        'name': "default",
        'description': "description",
        'address': "111",
    }
    response = requests.post(apis_urls.serverURL + apis_urls.slaveAPI, headers=headers,
                             data=json.dumps(data))
    slaveid = list(response.json()[apis_urls.getslavesAPI])[0]
    GeneralVariables.wrapperPort['value'] = str(response.json()[apis_urls.getslavesAPI][slaveid]['extra']['port'])

# Step Definition Implementation: Incomplete Step
# 1) Check the Pipeline is up and running
@Given('the pipeline is running')
def step_impl(context):
    logger.info("Given the pipeline is running")

# Step Definition Implementation: Incomplete Step
# 1) Connect to the server
# 2) execute the authorization curl command using the wrapperPort
@Given('the following authorization request is granted through pipeline')
def step_impl(context):
    logger.info("Given the following authorization request is granted through pipeline")
    api_responseflag = {'value': False}
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=apis_urls.serverIP, port=apis_urls.serverport, username=apis_urls.serverusername,
                   password=apis_urls.serverpassword)
    for row in context.table:
        logger.info("curl http://" + str(
            apis_urls.serverIP) + ":" + GeneralVariables.pipelinePort['value'] + "/authz/"  + str(
            row["subjectperimetername"]) + "/" + str(row["objectperimetername"]) + "/" +
                    str(row["actionperimetername"]))
        stdin, stdout, stderr = client.exec_command("curl http://" + str(
            apis_urls.serverIP) + ":" + GeneralVariables.pipelinePort['value'] + "/authz/"  + str(
            row["subjectperimetername"]) + "/" + str(row["objectperimetername"]) + "/" +
                                                    str(row["actionperimetername"]))
        logger.info(stdout.readlines())
        GeneralVariables.actual_authresponse['value'] = str(stdout.readlines())

# Step Definition Implementation: Incomplete Step
# 1) Connect to the server
# 2) execute the authorization curl command using the wrapperPort
@Given('the following authorization request is granted through wrapper')
def step_impl(context):
    logger.info("Given the following authorization request is granted through wrapper")
    api_responseflag = {'value': False}
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=apis_urls.serverIP, port=apis_urls.serverport, username=apis_urls.serverusername,
                   password=apis_urls.serverpassword)
    for row in context.table:
        logger.info("curl http://" + str(
            apis_urls.serverIP) + ":" + GeneralVariables.wrapperPort['value'] + "/authz/" + str(row[
                                                                                                    "keystone_project_id"]) + "/" + str(
            row["subjectperimetername"]) + "/" + str(row["objectperimetername"]) + "/" +
                    str(row["actionperimetername"]))
        stdin, stdout, stderr = client.exec_command("curl http://" + str(
            apis_urls.serverIP) + ":" + GeneralVariables.wrapperPort['value'] + "/authz/" + str(row[
                                                                                                    "keystone_project_id"]) + "/" + str(
            row["subjectperimetername"]) + "/" + str(row["objectperimetername"]) + "/" +
                                                    str(row["actionperimetername"]))
        logger.info(stdout.readlines())
        GeneralVariables.actual_authresponse['value'] = str(stdout.readlines())

# Step Definition Implementation: Incomplete Step
# 1) Connect to the server
# 2) execute the authorization curl command using the pipelinePort
# 3) set the actual_authresponse global variable with the curl response
@When('the following authorization request is sent through pipeline')
def step_impl(context):
    logger.info("Given the following authorization request is sent through pipeline")
    api_responseflag = {'value': False}
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=apis_urls.serverIP, port=apis_urls.serverport, username=apis_urls.serverusername,
                   password=apis_urls.serverpassword)

    for row in context.table:
        logger.info("curl http://" + str(
            apis_urls.serverIP) + ":" + GeneralVariables.pipelinePort['value'] + "/authz/"  + str(
            row["subjectperimetername"]) + "/" + str(row["objectperimetername"]) + "/" +
                    str(row["actionperimetername"]))
        stdin, stdout, stderr = client.exec_command("curl http://" + str(
            apis_urls.serverIP) + ":" + GeneralVariables.pipelinePort['value'] + "/authz/" + str(
            row["subjectperimetername"]) + "/" + str(row["objectperimetername"]) + "/" +
                                                    str(row["actionperimetername"]))
        logger.info(stdout.readlines())
        GeneralVariables.actual_authresponse['value'] = str(stdout.readlines())

# Step Definition Implementation: Incomplete Step
# 1) Connect to the server
# 2) execute the authorization curl command using the pipelinePort
# 3) set the actual_authresponse global variable with the curl response
@When('the following authorization request is sent through wrapper')
def step_impl(context):
    logger.info("Given the following authorization request is sent through wrapper")
    api_responseflag = {'value': False}
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=apis_urls.serverIP, port=apis_urls.serverport, username=apis_urls.serverusername,
                   password=apis_urls.serverpassword)

    for row in context.table:
        logger.info("curl http://" + str(
            apis_urls.serverIP) + ":" + GeneralVariables.wrapperPort['value'] + "/authz/" + str(row[
                                                                                                    "keystone_project_id"]) + "/" + str(
            row["subjectperimetername"]) + "/" + str(row["objectperimetername"]) + "/" +
                    str(row["actionperimetername"]))
        stdin, stdout, stderr = client.exec_command("curl http://" + str(
            apis_urls.serverIP) + ":" + GeneralVariables.wrapperPort['value'] + "/authz/" + str(row[
                                                                                                    "keystone_project_id"]) + "/" + str(
            row["subjectperimetername"]) + "/" + str(row["objectperimetername"]) + "/" +
                                                    str(row["actionperimetername"]))
        logger.info(stdout.readlines())
        GeneralVariables.actual_authresponse['value'] = str(stdout.readlines())

# Step Definition Implementation: Untested Step
# 1) Assert that the actual authresponse is the same as the expected.
@Then('the authorization response should be the following')
def step_impl(context):
    logger.info("Then the authorization response should be the following")
    for row in context.table:
        logger.info("asserting the expected api response: '" + row["auth_response"] + "' and the actual response: '" +
                    GeneralVariables.actual_authresponse['value'] + "'")
        assert row["auth_response"] == GeneralVariables.actual_authresponse[
            'value'], "Validation is not correct, Expected: " + \
                      row[
                          "auth_response"] + " but the API response was: " + \
                      GeneralVariables.actual_authresponse['value']
        logger.info("assertion passed!")
