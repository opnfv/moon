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

    moonDataListController.$inject = ['$scope', '$rootScope', 'dataService', '$translate', 'alertService', 'DATA_CST', 'metaDataService'];

    function moonDataListController($scope, $rootScope, dataService, $translate, alertService, DATA_CST, metaDataService){

        var list = this;

        list.policy = $scope.list.policy;
        list.editMode = $scope.list.editMode;

        list.typeOfSubject = DATA_CST.TYPE.SUBJECT;
        list.typeOfObject = DATA_CST.TYPE.OBJECT;
        list.typeOfAction = DATA_CST.TYPE.ACTION;

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

            'event:createDataFromDataEditSuccess': $rootScope.$on('event:createDataFromDataEditSuccess', addDataToList)

        };

        _.each(rootListeners, function(unbind){
            $scope.$on('$destroy', rootListeners[unbind]);
        });


        function manageSubjects(){

            list.loadingSub = true;

            dataService.subject.findAllFromPolicyWithCallback(list.policy.id, function(data){

                list.subjects = data;
                list.loadingSub = false;

            });
        }

        function manageObjects(){

            list.loadingObj = true;

            dataService.object.findAllFromPolicyWithCallback(list.policy.id, function(data){

                list.objects = data;
                list.loadingObj = false;

            });

        }

        function manageActions(){

            list.loadingAct = true;

            dataService.action.findAllFromPolicyWithCallback(list.policy.id, function(data){

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
         * Delete
         */

        function deleteSub(subject){

            subject.loader = true;

            dataService.subject.delete(subject, list.policy.id, subject.category_id, deleteSubSuccess, deleteSubError);

            function deleteSubSuccess(data){

                $translate('moon.policy.data.subject.delete.success', { subjectName: subject.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                removeSubFromSubList(subject);

                subject.loader = false;

            }

            function deleteSubError(reason){

                $translate('moon.policy.data.subject.delete.error', { subjectName: subject.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                subject.loader = false;

            }
        }

        function deleteObj(object){

            object.loader = true;

            dataService.object.delete(object, list.policy.id, object.category_id, deleteObjSuccess, deleteObjError);

            function deleteObjSuccess(data){

                $translate('moon.policy.data.object.delete.success', { objectName: object.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                removeObjFromObjList(object);

                object.loader = false;

            }

            function deleteObjError(reason){

                $translate('moon.policy.data.object.delete.error', { objectName: object.name, reason: reason.message}).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                object.loader = false;
            }
        }

        function deleteAct(action){

            action.loader = true;

            dataService.action.delete(action, list.policy.id, action.category_id, deleteActSuccess, deleteActError);

            function deleteActSuccess(data){

                $translate('moon.policy.data.action.delete.success', { actionName: action.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                removeActFromActList(action);

                action.loader = false;

            }

            function deleteActError(reason){

                $translate('moon.policy.data.action.delete.error', { actionName: action.name, reason: reason.message}).then( function(translatedValue) {
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

        function addDataToList( event, data, typeOfData){

            switch(typeOfData){

                case DATA_CST.TYPE.SUBJECT:

                    list.subjects.push(data);
                    break;

                case DATA_CST.TYPE.OBJECT:

                    list.objects.push(data);
                    break;

                case DATA_CST.TYPE.ACTION:

                    list.actions.push(data);
                    break;
            }

        }

    }

})();