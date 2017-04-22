(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonAssignmentsList', moonAssignmentsList);

    moonAssignmentsList.$inject = [];

    function moonAssignmentsList() {

        return {
            templateUrl : 'html/policy/edit/parameter/assignments/assignments-list.tpl.html',
            bindToController : true,
            controller : moonAssignmentsListController,
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
        .controller('moonAssignmentsListController', moonAssignmentsListController);

    moonAssignmentsListController.$inject = ['$scope', '$rootScope', 'assignmentService', '$translate', 'alertService', 'policyService', 'ASSIGNMENTS_CST', 'utilService', 'metaDataService', 'perimeterService', 'dataService'];

    function moonAssignmentsListController($scope, $rootScope, assignmentService, $translate, alertService, policyService, ASSIGNMENTS_CST, utilService, metaDataService, perimeterService, dataService){

        var list = this;

        list.policy = $scope.list.policy;
        list.editMode = $scope.list.editMode;

        list.typeOfSubject = ASSIGNMENTS_CST.TYPE.SUBJECT;
        list.typeOfObject = ASSIGNMENTS_CST.TYPE.OBJECT;
        list.typeOfAction = ASSIGNMENTS_CST.TYPE.ACTION;

        list.unMapSub = unMapSub;
        list.unMapObj = unMapObj;
        list.unMapAct = unMapAct;

        list.deleteSub = deleteSub;
        list.deleteObj = deleteObj;
        list.deleteAct = deleteAct;

        list.getSubjects = getSubjects;
        list.getObjects = getObjects;
        list.getActions = getActions;

        list.getCategoryFromAssignment = getCategoryFromAssignment;
        list.getPerimeterFromAssignment = getPerimeterFromAssignment;
        list.getDataFromAssignmentsIndex = getDataFromAssignmentsIndex;

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

            assignmentService.subject.findAllFromPolicyWithCallback(list.policy.id, function(data){

                console.log('subjects');
                console.log(data);
                list.subjects = data;
                list.loadingSub = false;

            });
        }

        function manageObjects(){

            list.loadingObj = true;

            assignmentService.object.findAllFromPolicyWithCallback(list.policy.id, function(data){

                console.log('objects');
                console.log(data);
                list.objects = data;
                list.loadingObj = false;

            });

        }

        function manageActions(){

            list.loadingAct = true;

            assignmentService.action.findAllFromPolicyWithCallback(list.policy.id, function(data){

                console.log('actions');
                console.log(data);
                list.actions = data;
                list.loadingAct = false;

            });

        }

        function getPerimeterFromAssignment(assignment, type) {

            if(_.has(assignment, 'perimeter')){
                return assignment.perimeter;
            }

            // if the call has not been made
            if(!_.has(assignment, 'callPerimeterInProgress')){

                assignment.callPerimeterInProgress = true;

                switch(type){

                    case ASSIGNMENTS_CST.TYPE.SUBJECT:
                        perimeterService.subject.findOneFromPolicyWithCallback(list.policy.id, assignment.subject_id, setPerimeterToAssignment);
                        break;

                    case ASSIGNMENTS_CST.TYPE.OBJECT:
                        perimeterService.object.findOneFromPolicyWithCallback(list.policy.id, assignment.object_id, setPerimeterToAssignment);
                        break;

                    case ASSIGNMENTS_CST.TYPE.ACTION:
                        perimeterService.action.findOneFromPolicyWithCallback(list.policy.id, assignment.action_id, setPerimeterToAssignment);
                        break;

                }

            }

            // if the call is in progress return false
            return false;

            function setPerimeterToAssignment(perimeter){

                assignment.callPerimeterInProgress = false;
                assignment.perimeter = perimeter;

            }
        }

        function getCategoryFromAssignment(data, type) {

            if(_.has(data, 'category')){
                return data.category;
            }

            // if the call has not been made
            if(!_.has(data, 'callCategoryInProgress')){

                data.callCategoryInProgress = true;

                switch(type){

                    case ASSIGNMENTS_CST.TYPE.SUBJECT:
                        metaDataService.subject.findOne(data.subject_cat_id, setCategoryToData);
                        break;

                    case ASSIGNMENTS_CST.TYPE.OBJECT:
                        metaDataService.object.findOne(data.object_cat_id, setCategoryToData);
                        break;

                    case ASSIGNMENTS_CST.TYPE.ACTION:
                        metaDataService.action.findOne(data.action_cat_id, setCategoryToData);
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
         * Prerequisite : meta Rule  should be completely loaded
         * @param index
         * @param assignment
         * @param type
         */
        function getDataFromAssignmentsIndex(index, assignment, type){

            if(!_.has(assignment, 'assignments_value')){
                // setting an array which will contains every value of the category
                assignment.assignments_value = Array.apply(null, new Array(assignment.assignments.length)).map(function(){
                    return {
                        data: {}
                    }
                });
            }

            if(_.has(assignment.assignments_value[index], 'callDataInProgress') && !assignment.assignments_value[index].callDataInProgress ){
                return assignment.assignments_value[index].data;
            }

            // if the call has not been made
            if(!_.has(assignment.assignments_value[index], 'callDataInProgress')){

                assignment.assignments_value[index].callDataInProgress = true;

                switch(type){

                    case ASSIGNMENTS_CST.TYPE.SUBJECT:
                        dataService.subject.data.findOne(list.policy.id, assignment.category_id, assignment.assignments[index], setDataToAssignment);
                        break;

                    case ASSIGNMENTS_CST.TYPE.OBJECT:
                        dataService.object.data.findOne(list.policy.id, assignment.category_id, assignment.assignments[index], setDataToAssignment);
                        break;

                    case ASSIGNMENTS_CST.TYPE.ACTION:
                        dataService.action.data.findOne(list.policy.id, assignment.category_id, assignment.assignments[index], setDataToAssignment);
                        break;

                }

            }

            // if the call is in progress return false
            return false;

            function setDataToAssignment(data){

                assignment.assignments_value[index].callDataInProgress = false;
                assignment.assignments_value[index].data = data;

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

            assignmentService.subject.delete(subject, deleteSubSuccess, deleteSubError);

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

            assignmentService.object.delete(object, deleteObjSuccess, deleteObjError);

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

            assignmentService.action.delete(action, deleteActSuccess, deleteActError);

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