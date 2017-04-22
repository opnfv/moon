(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonPerimeterList', moonPerimeterList);

    moonPerimeterList.$inject = [];

    function moonPerimeterList() {

        return {
            templateUrl : 'html/policy/edit/parameter/perimeter/perimeter-list.tpl.html',
            bindToController : true,
            controller : moonPerimeterListController,
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
        .controller('moonPerimeterListController', moonPerimeterListController);

    moonPerimeterListController.$inject = ['$scope', '$rootScope', 'perimeterService', '$translate', 'alertService', 'policyService', 'PERIMETER_CST', 'utilService'];

    function moonPerimeterListController($scope, $rootScope, perimeterService, $translate, alertService, policyService, PERIMETER_CST, utilService){

        var list = this;

        list.policy = $scope.list.policy;
        list.editMode = $scope.list.editMode;

        list.typeOfSubject = PERIMETER_CST.TYPE.SUBJECT;
        list.typeOfObject = PERIMETER_CST.TYPE.OBJECT;
        list.typeOfAction = PERIMETER_CST.TYPE.ACTION;

        list.unMapSub = unMapSub;
        list.unMapObj = unMapObj;
        list.unMapAct = unMapAct;

        list.deleteSub = deleteSub;
        list.deleteObj = deleteObj;
        list.deleteAct = deleteAct;

        list.getSubjects = getSubjects;
        list.getObjects = getObjects;
        list.getActions = getActions;

        activate();

        function activate(){

            manageSubjects();

            manageObjects();

            manageActions();

        }

        var rootListeners = {

            'event:deletePerimeterFromPerimeterAddSuccess': $rootScope.$on('event:deletePerimeterFromPerimeterAddSuccess', deletePolicy)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }


        function manageSubjects(){

            list.loadingSub = true;

            perimeterService.subject.findAllFromPolicyWithCallback(list.policy.id, function(perimeters){

                list.subjects = perimeters;
                list.loadingSub = false;

            });
        }

        function manageObjects(){

            list.loadingObj = true;

            perimeterService.object.findAllFromPolicyWithCallback(list.policy.id, function(perimeters){

                console.log('objects');
                console.log(perimeters);
                list.objects = perimeters;
                list.loadingObj = false;

            });

        }

        function manageActions(){

            list.loadingAct = true;

            perimeterService.action.findAllFromPolicyWithCallback(list.policy.id, function(perimeters){

                console.log('actions');
                console.log(perimeters);
                list.actions = perimeters;
                list.loadingAct = false;

            });

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

                list.policy = policyService.findPerimeterFromPolicy(utilService.transformOne(data, 'meta_rules'));

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

                list.policy = policyService.findPerimeterFromPolicy(utilService.transformOne(data, 'meta_rules'));

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

                list.policy = policyService.findPerimeterFromPolicy(utilService.transformOne(data, 'meta_rules'));

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

            perimeterService.subject.delete(subject, deleteSubSuccess, deleteSubError);

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

            perimeterService.object.delete(object, deleteObjSuccess, deleteObjError);

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

            perimeterService.action.delete(action, deleteActSuccess, deleteActError);

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