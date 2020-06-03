# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


class GeneralVariables:
    serverURL="http://127.0.0.1:8000/"

    serverIP="10.237.71.141"

    serverport = "22"

    serverusername="ubuntu"

    serverpassword="ubuntu-007"

    token = "{{TOKEN}}"

    auth_headers = {"X-Api-Key": token}

    actual_authresponse = {'value': False}

    api_responseflag = {'value': False}

    pipelinePort = {'value': ""}

    wrapperPort = {'value': ""}

    projectAPI = ""

    slaveAPI="slave"

    getslavesAPI = "slaves"

    pdpAPI = "pdp"

    modelAPI = "models"

    policyAPI = "policies"

    assignpolicyid={'value': ""}

    assignsubjectperimeterid = {'value': ""}

    assignsubjectcategoryid = {'value': ""}

    assignobjectperimeterid = {'value': ""}

    assignobjectcategoryid = {'value': ""}

    assignactionperimeterid = {'value': ""}

    assignactioncategoryid = {'value': ""}

    metarulesAPI = "meta_rules"

    metadatasubjectcategoryAPI = "subject_categories"

    metadataobjectcategoryAPI = "object_categories"

    metadataactioncategoryAPI = "action_categories"

    perimetersubjectAPI = "subjects"

    perimeterobjectAPI = "objects"

    perimeteractionAPI = "actions"

    datasubjectAPI = "subject_data"

    dataobjectAPI = "object_data"

    dataactionAPI = "action_data"

    assignementssubjectAPI = "subject_assignments"

    assignementsobjectAPI = "object_assignments"

    assignementsactionAPI = "action_assignments"

    rulesAPI = "rules"

