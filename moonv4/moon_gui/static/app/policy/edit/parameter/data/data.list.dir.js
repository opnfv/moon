(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonDataList', moonDataList);

    moonDataList.$inject = [];

    function moonDataList() {

        return {
            templateUrl : 'html/policy/edit/parameter/data/data-list.tpl.html',
            bindToController : true,
            controller : moonDataListController,
            controllerAs : 'list',
            scope : {
                policy: '=',
                editMode : '='
            },
            restrict : 'E',
            replace : true
        };
    }

    angular
        .module('moon')
        .controller('moonDataListController', moonDataListController);

    moonDataListController.$inject = ['$scope', '$rootScope', 'dataService', '$translate', 'alertService', 'policyService', 'DATA_CST', 'utilService', 'metaDataService'];

    function moonDataListController($scope, $rootScope, dataService, $translate, alertService, policyService, DATA_CST, utilService, metaDataService){

        var list = this;

        list.policy = $scope.list.policy;
        list.editMode = $scope.list.editMode;

        list.typeOfSubject = DATA_CST.TYPE.SUBJECT;
        list.typeOfObject = DATA_CST.TYPE.OBJECT;
        list.typeOfAction = DATA_CST.TYPE.ACTION;

        list.unMapSub = unMapSub;
        list.unMapObj = unMapObj;
        list.unMapAct = unMapAct;

        list.deleteSub = deleteSub;
        list.deleteObj = deleteObj;
        list.deleteAct = deleteAct;

        list.getSubjects = getSubjects;
        list.getObjects = getObjects;
        list.getActions = getActions;

        list.getCategoryFromData = getCategoryFromData;

        activate();

        function activate(){

            manageSubjects();

            manageObjects();

            manageActions();

        }

        var rootListeners = {

            'event:deleteDataFromDataAddSuccess': $rootScope.$on('event:deleteDataFromDataAddSuccess', deletePolicy)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }


        function manageSubjects(){

            list.loadingSub = true;

            dataService.subject.findAllFromPolicyWithCallback(list.policy.id, function(data){

                console.log('subjects');
                console.log(data);
                list.subjects = data;
                list.loadingSub = false;

            });
        }

        function manageObjects(){

            list.loadingObj = true;

            dataService.object.findAllFromPolicyWithCallback(list.policy.id, function(data){

                console.log('objects');
                console.log(data);
                list.objects = data;
                list.loadingObj = false;

            });

        }

        function manageActions(){

            list.loadingAct = true;

            dataService.action.findAllFromPolicyWithCallback(list.policy.id, function(data){

                console.log('actions');
                console.log(data);
                list.actions = data;
                list.loadingAct = false;

            });

        }

        function getCategoryFromData(data, type) {

            if(_.has(data, 'category')){
                return data.category;
            }

            // if the call has not been made
            if(!_.has(data, 'callCategoryInProgress')){

                data.callCategoryInProgress = true;

                switch(type){

                    case DATA_CST.TYPE.SUBJECT:
                        metaDataService.subject.findOne(data.category_id, setCategoryToData);
                        break;

                    case DATA_CST.TYPE.OBJECT:
                        metaDataService.object.findOne(data.category_id, setCategoryToData);
                        break;

                    case DATA_CST.TYPE.ACTION:
                        metaDataService.action.findOne(data.category_id, setCategoryToData);
                        break;

                }

            }

            // if the call is in progress return false
            return false;

            function setCategoryToData(category){

                data.callCategoryInProgress = false;
                data.category = category;

            }
        }

        /**
         * UnMap
         */

        function unMapSub(subject){

            subject.loader = true;

            var policyToSend = angular.copy(list.policy);

            policyToSend.subject_categories = _.without(policyToSend.subject_categories, subject.id);

            policyService.update(policyToSend, updatePolicySuccess, updatePolicyError);

            function updatePolicySuccess(data){

                $translate('moon.policy.metarules.update.success', { policyName: list.policy.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                list.policy = policyService.findDataFromPolicy(utilService.transformOne(data, 'meta_rules'));

                activate();

                subject.loader = false;

            }

            function updatePolicyError(reason){

                $translate('moon.policy.metarules.update.error', { policyName: list.policy.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                subject.loader = false;

            }

        }

        function unMapObj(object){

            object.loader = true;

            var policyToSend = angular.copy(list.policy);

            policyToSend.object_categories = _.without(policyToSend.object_categories, object.id);

            policyService.update(policyToSend, updatePolicySuccess, updatePolicyError);

            function updatePolicySuccess(data){

                $translate('moon.policy.metarules.update.success', { policyName: list.policy.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                list.policy = policyService.findDataFromPolicy(utilService.transformOne(data, 'meta_rules'));

                activate();

                object.loader = false;

            }

            function updatePolicyError(reason){

                $translate('moon.policy.metarules.update.error', { policyName: list.policy.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                object.loader = false;

            }

        }

        function unMapAct(action){

            action.loader = true;

            var policyToSend = angular.copy(list.policy);

            policyToSend.action_categories = _.without(policyToSend.action_categories, action.id);

            policyService.update(policyToSend, updatePolicySuccess, updatePolicyError);

            function updatePolicySuccess(data){

                $translate('moon.policy.metarules.update.success', { policyName: list.policy.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                list.policy = policyService.findDataFromPolicy(utilService.transformOne(data, 'meta_rules'));

                activate();

                action.loader = false;

            }

            function updatePolicyError(reason){

                $translate('moon.policy.metarules.update.error', { policyName: list.policy.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                action.loader = false;

            }

        }

        /**
         * Delete
         */

        function deleteSub(subject){

            subject.loader = true;

            dataService.subject.delete(subject, deleteSubSuccess, deleteSubError);

            function deleteSubSuccess(data){

                $translate('moon.policy.perimeter.subject.delete.success', { subjectName: subject.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                removeSubFromSubList(subject);

                subject.loader = false;

            }

            function deleteSubError(reason){

                $translate('moon.policy.perimeter.subject.delete.error', { subjectName: subject.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                subject.loader = false;

            }
        }

        function deleteObj(object){

            object.loader = true;

            dataService.object.delete(object, deleteObjSuccess, deleteObjError);

            function deleteObjSuccess(data){

                $translate('moon.policy.perimeter.object.delete.success', { objectName: object.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                removeObjFromObjList(object);

                object.loader = false;

            }

            function deleteObjError(reason){

                $translate('moon.policy.perimeter.object.delete.error', { objectName: object.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                object.loader = false;
            }
        }

        function deleteAct(action){

            action.loader = true;

            dataService.action.delete(action, deleteActSuccess, deleteActError);

            function deleteActSuccess(data){

                $translate('moon.policy.perimeter.action.delete.success', { actionName: action.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                removeActFromActList(action);

                action.loader = false;

            }

            function deleteActError(reason){

                $translate('moon.policy.perimeter.action.delete.error', { actionName: action.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                action.loader = false;

            }
        }

        function getSubjects(){
            return list.subjects ? list.subjects : [];
        }

        function getObjects(){
            return list.objects ? list.objects : [];
        }

        function getActions(){
            return list.actions ? list.actions : [];
        }

        function removeSubFromSubList(subject){
            list.subjects = _.without(list.subjects, subject);
        }

        function removeObjFromObjList(object){
            list.objects = _.without(list.objects, object);
        }

        function removeActFromActList(action){
            list.actions = _.without(list.actions, action);
        }

        function deletePolicy( event, policy){

            list.policy = policy;

            activate();

        }

    }

})();