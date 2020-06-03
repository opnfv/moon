# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from behave import *
from steps.Static_Variables import GeneralVariables
import requests
import json
import logging


logger = logging.getLogger(__name__)

class commonfunctions:
    apis_urls = GeneralVariables()

    def get_subjectcategoryid(self, subjectcategoryname):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.metadatasubjectcategoryAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.metadatasubjectcategoryAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.metadatasubjectcategoryAPI]).keys():
                if (response.json()[self.apis_urls.metadatasubjectcategoryAPI][ids]['name'] == subjectcategoryname):
                    return response.json()[self.apis_urls.metadatasubjectcategoryAPI][ids]['id']

    def get_objectcategoryid(self, objectcategoryname):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.metadataobjectcategoryAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.metadataobjectcategoryAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.metadataobjectcategoryAPI]).keys():
                if (response.json()[self.apis_urls.metadataobjectcategoryAPI][ids]['name'] == objectcategoryname):
                    return response.json()[self.apis_urls.metadataobjectcategoryAPI][ids]['id']

    def get_actioncategoryid(self, actioncategoryname):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.metadataactioncategoryAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.metadataactioncategoryAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.metadataactioncategoryAPI]).keys():
                if (response.json()[self.apis_urls.metadataactioncategoryAPI][ids]['name'] == actioncategoryname):
                    return response.json()[self.apis_urls.metadataactioncategoryAPI][ids]['id']

    def get_metaruleid(self, metarulename):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.metarulesAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.metarulesAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.metarulesAPI]).keys():
                if (response.json()[self.apis_urls.metarulesAPI][ids]['name'] == metarulename):
                    return ids

    def get_modelid(self, modelname):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.modelAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.modelAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.modelAPI]).keys():
                if (response.json()[self.apis_urls.modelAPI][ids]['name'] == modelname):
                    return ids

    def get_policyid(self, policyname):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.policyAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.policyAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.policyAPI]).keys():
                if (response.json()[self.apis_urls.policyAPI][ids]['name'] == policyname):
                    return ids

    def get_subjectperimeterid(self,subjectperimeter ):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.perimetersubjectAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.perimetersubjectAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.perimetersubjectAPI]).keys():
                if (response.json()[self.apis_urls.perimetersubjectAPI][ids]['name'] == subjectperimeter):
                    return ids

    def get_objectperimeterid(self,objectperimeter ):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.perimeterobjectAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.perimeterobjectAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.perimeterobjectAPI]).keys():
                if (response.json()[self.apis_urls.perimeterobjectAPI][ids]['name'] == objectperimeter):
                    return ids

    def get_actionperimeterid(self, actionperimeter):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.perimeteractionAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.perimeteractionAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.perimeteractionAPI]).keys():
                if (response.json()[self.apis_urls.perimeteractionAPI][ids]['name'] == actionperimeter):
                    return ids

    def get_subjectdataid(self,subjectdataname,subjectcategoryid,policyid ):
        response_data = requests.get(
            self.apis_urls.serverURL + "policies/" + policyid + "/" + self.apis_urls.datasubjectAPI + "/" + subjectcategoryid,headers=self.apis_urls.auth_headers)
        if(len(response_data.json()[self.apis_urls.datasubjectAPI]))!=0:
            subjectdataidslist = []
            matcheddataidslist = []
            dataids=response_data.json()[self.apis_urls.datasubjectAPI][0]['data']
            for ids in dataids:
                apisubjectdataid = response_data.json()[self.apis_urls.datasubjectAPI][0]['data'][str(ids)]['id']
                subjectdataidslist.append(apisubjectdataid)

            if ((str(subjectdataname)).find(",") != -1):
                datanameslist = subjectdataname.split(",")
                for dataname in datanameslist:
                    for data_id in subjectdataidslist:
                        if ((response_data.json()[self.apis_urls.datasubjectAPI][0]['data'][str(data_id)][
                            'name']) == dataname):
                            matcheddataidslist.append(data_id)
                return ",".join(matcheddataidslist)
            else:
                for data_id in subjectdataidslist:
                    if ((
                    response_data.json()[self.apis_urls.datasubjectAPI][0]['data'][str(data_id)]['name']) == subjectdataname):
                        return data_id

    def get_objectdataid(self,objectdataname,objectcategoryid,policyid ):
        response_data = requests.get(
            self.apis_urls.serverURL +  self.apis_urls.policyAPI + "/" + policyid + "/" +  self.apis_urls.dataobjectAPI + "/" + objectcategoryid,headers=self.apis_urls.auth_headers)
        if (len(response_data.json()[self.apis_urls.dataobjectAPI])) != 0:
            objectdataidslist = []
            matcheddataidslist=[]
            for ids in response_data.json()[ self.apis_urls.dataobjectAPI][0]['data']:
                apiobjectdataid = response_data.json()[ self.apis_urls.dataobjectAPI][0]['data'][str(ids)]['id']
                objectdataidslist.append(apiobjectdataid)
            if ((str(objectdataname)).find(",") != -1):
                datanameslist = objectdataname.split(",")
                for dataname in datanameslist:
                    for data_id in objectdataidslist:
                        if ((response_data.json()[self.apis_urls.dataobjectAPI][0]['data'][str(data_id)]['name']) == dataname):
                            matcheddataidslist.append(data_id)
                return ",".join(matcheddataidslist)

            else:
                for data_id in objectdataidslist:
                    if ((response_data.json()[self.apis_urls.dataobjectAPI][0]['data'][str(data_id)]['name']) == objectdataname):
                        return data_id

    def get_actiondataid(self,actiondataname,actioncategoryid,policyid ):
        response_data = requests.get(
            self.apis_urls.serverURL + self.apis_urls.policyAPI + "/" + policyid + "/" + self.apis_urls.dataactionAPI + "/" + actioncategoryid,headers=self.apis_urls.auth_headers)
        if (len(response_data.json()[self.apis_urls.dataactionAPI])) != 0:
            actiondataidslist = []
            matcheddataidslist = []
            for ids in response_data.json()[self.apis_urls.dataactionAPI][0]['data']:
                apiactiondataid = response_data.json()[self.apis_urls.dataactionAPI][0]['data'][str(ids)]['id']
                actiondataidslist.append(apiactiondataid)
                if ((str(actiondataname)).find(",") != -1):
                    datanameslist = actiondataname.split(",")
                    for dataname in datanameslist:
                        for data_id in actiondataidslist:
                            if ((response_data.json()[self.apis_urls.dataactionAPI][0]['data'][str(data_id)][
                                'name']) == dataname):
                                matcheddataidslist.append(data_id)
                    return ",".join(matcheddataidslist)
                else:
                    for data_id in actiondataidslist:
                        if ((response_data.json()[self.apis_urls.dataactionAPI][0]['data'][str(data_id)]['name']) == actiondataname):
                            return data_id

    def get_subjectcategoryname(self, subjectcategoryid):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.metadatasubjectcategoryAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.metadatasubjectcategoryAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.metadatasubjectcategoryAPI]).keys():
                if (response.json()[self.apis_urls.metadatasubjectcategoryAPI][ids]['id'] == subjectcategoryid):
                    return response.json()[self.apis_urls.metadatasubjectcategoryAPI][ids]['name']

    def get_objectcategoryname(self, objectcategoryid):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.metadataobjectcategoryAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.metadataobjectcategoryAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.metadataobjectcategoryAPI]).keys():
                if (response.json()[self.apis_urls.metadataobjectcategoryAPI][ids]['id'] == objectcategoryid):
                    return response.json()[self.apis_urls.metadataobjectcategoryAPI][ids]['name']

    def get_actioncategoryname(self, actioncategoryid):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.metadataactioncategoryAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.metadataactioncategoryAPI]) != 0:
            for ids in dict(response.json()[self.apis_urls.metadataactioncategoryAPI]).keys():
                if (response.json()[self.apis_urls.metadataactioncategoryAPI][ids]['id'] == actioncategoryid):
                    return response.json()[self.apis_urls.metadataactioncategoryAPI][ids]['name']

    def get_metarulename(self, metaruleid):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.metarulesAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.metarulesAPI]) != 0:
            for id in dict(response.json()[self.apis_urls.metarulesAPI]).keys():
                if (id == metaruleid):
                    return response.json()[self.apis_urls.metarulesAPI][id]['name']

    def get_modelname(self, modelid):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.modelAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.modelAPI]) != 0:
            for id in dict(response.json()[self.apis_urls.modelAPI]).keys():
                if (id == modelid):
                    return response.json()[self.apis_urls.modelAPI][id]['name']

    def get_policyname(self, policyid):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.policyAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.policyAPI]) != 0:
            for id in dict(response.json()[self.apis_urls.policyAPI]).keys():
                if (id == policyid):
                    return response.json()[self.apis_urls.policyAPI][id]['name']

    def get_subjectperimetername(self, subjectperimeterid):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.perimetersubjectAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.perimetersubjectAPI]) != 0:
            for id in dict(response.json()[self.apis_urls.perimetersubjectAPI]).keys():
                if (id == subjectperimeterid):
                    return response.json()[self.apis_urls.perimetersubjectAPI][id]['name']

    def get_objectperimetername(self, objectperimeterid):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.perimeterobjectAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.perimeterobjectAPI]) != 0:
            for id in dict(response.json()[self.apis_urls.perimeterobjectAPI]).keys():
                if (id == objectperimeterid):
                    return response.json()[self.apis_urls.perimeterobjectAPI][id]['name']

    def get_actionperimetername(self, actionperimeterid):
        response = requests.get(self.apis_urls.serverURL + self.apis_urls.perimeteractionAPI,headers=self.apis_urls.auth_headers)
        if len(response.json()[self.apis_urls.perimeteractionAPI]) != 0:
            for id in dict(response.json()[self.apis_urls.perimeteractionAPI]).keys():
                if (id == actionperimeterid):
                    return response.json()[self.apis_urls.perimeteractionAPI][id]['name']

    def get_subjectdataname(self, subjectdataids, subjectcategoryid, policyid):
        subjectdatanames=[]
        for subjectdataid in subjectdataids:
            response_data = requests.get(
            self.apis_urls.serverURL + "policies/" + policyid + "/" + self.apis_urls.datasubjectAPI + "/" + subjectcategoryid+"/"+subjectdataid,headers=self.apis_urls.auth_headers)

            subjectdataidslist = []
            if(response_data.status_code==200):
                for ids in response_data.json()[self.apis_urls.datasubjectAPI][0]['data']:
                    apisubjectdataid = response_data.json()[self.apis_urls.datasubjectAPI][0]['data'][str(ids)]['id']
                    subjectdataidslist.append(apisubjectdataid)

                for data_id in subjectdataidslist:
                    if (str((response_data.json()[self.apis_urls.datasubjectAPI][0]['data'][str(data_id)][
                    'id'])) == subjectdataid):
                        subjectdatanames.append(str(response_data.json()[self.apis_urls.datasubjectAPI][0]['data'][str(data_id)]['name']))
            else:
                subjectdataidslist = ""
        return subjectdatanames

    def get_objectdataname(self, objectdataids, objectcategoryid, policyid):
        objectdatanames = []
        for objectdataid in objectdataids:
            response_data = requests.get(
                self.apis_urls.serverURL + "policies/" + policyid + "/" + self.apis_urls.dataobjectAPI + "/" + objectcategoryid + "/" + objectdataid,headers=self.apis_urls.auth_headers)
            objectdataidslist = []
            if (response_data.status_code == 200):
                for ids in response_data.json()[self.apis_urls.dataobjectAPI][0]['data']:
                    apiobjectdataid = response_data.json()[self.apis_urls.dataobjectAPI][0]['data'][str(ids)]['id']
                    objectdataidslist.append(apiobjectdataid)
                for data_id in objectdataidslist:
                    if (str((response_data.json()[self.apis_urls.dataobjectAPI][0]['data'][str(data_id)][
                        'id'])) == objectdataid):
                        objectdatanames.append(
                            str(response_data.json()[self.apis_urls.dataobjectAPI][0]['data'][str(data_id)]['name']))
            else:
                objectdataidslist = ""
        return objectdatanames

    def get_actiondataname(self, actiondataids, actioncategoryid, policyid):
        actiondatanames = []
        for actiondataid in actiondataids:
            response_data = requests.get(
                self.apis_urls.serverURL + "policies/" + policyid + "/" + self.apis_urls.dataactionAPI + "/" + actioncategoryid + "/" + actiondataid,headers=self.apis_urls.auth_headers)
            #logger.info(response_data.json()[self.apis_urls.dataactionAPI][0])

            actiondataidslist = []
            if (response_data.status_code == 200):
                for ids in response_data.json()[self.apis_urls.dataactionAPI][0]['data']:
                    apiactiondataid = response_data.json()[self.apis_urls.dataactionAPI][0]['data'][str(ids)]['id']
                    actiondataidslist.append(apiactiondataid)
                    logging.info(actiondataidslist)
                for data_id in actiondataidslist:
                    if (str((response_data.json()[self.apis_urls.dataactionAPI][0]['data'][str(data_id)][
                        'id'])) == actiondataid):
                        actiondatanames.append(
                            str(response_data.json()[self.apis_urls.dataactionAPI][0]['data'][str(data_id)]['name']))
            else:
                actiondataidslist = ""
        return actiondatanames