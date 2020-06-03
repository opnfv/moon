(function () {

    'use strict';

    angular
        .module('moon')
        .directive('moonAssignmentsList', moonAssignmentsList);

    moonAssignmentsList.$inject = [];

    function moonAssignmentsList() {

        return {
            templateUrl: 'html/policy/edit/parameter/assignments/assignments-list.tpl.html',
            bindToController: true,
            controller: moonAssignmentsListController,
            controllerAs: 'list',
            scope: {
                policy: '=',
                editMode: '='
            },
            restrict: 'E',
            replace: true
        };
    }

    angular
        .module('moon')
        .controller('moonAssignmentsListController', moonAssignmentsListController);

    moonAssignmentsListController.$inject = ['$scope', '$rootScope', 'assignmentsService', '$translate', 'alertService',
        'policyService', 'ASSIGNMENTS_CST', 'utilService', 'metaDataService', 'perimeterService', 'dataService'];

    function moonAssignmentsListController($scope, $rootScope, assignmentsService, $translate, alertService,
                                           policyService, ASSIGNMENTS_CST, utilService, metaDataService, perimeterService, dataService) {

        var list = this;

        list.policy = $scope.list.policy;
        list.editMode = $scope.list.editMode;

        list.typeOfSubject = ASSIGNMENTS_CST.TYPE.SUBJECT;
        list.typeOfObject = ASSIGNMENTS_CST.TYPE.OBJECT;
        list.typeOfAction = ASSIGNMENTS_CST.TYPE.ACTION;

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

        function activate() {

            manageSubjects();

            manageObjects();

            manageActions();

        }

        var rootListeners = {

            'event:createAssignmentsFromAssignmentsEditSuccess': $rootScope.$on('event:createAssignmentsFromAssignmentsEditSuccess', updateList)

        };

        _.each(rootListeners, function(unbind){
            $scope.$on('$destroy', rootListeners[unbind]);
        });

        function manageSubjects() {

            list.loadingSub = true;

            assignmentsService.subject.findAllFromPolicyWithCallback(list.policy.id, function (data) {

                list.subjects = data;
                list.loadingSub = false;

            });
        }

        function manageObjects() {

            list.loadingObj = true;

            assignmentsService.object.findAllFromPolicyWithCallback(list.policy.id, function (data) {

                list.objects = data;
                list.loadingObj = false;

            });

        }

        function manageActions() {

            list.loadingAct = true;

            assignmentsService.action.findAllFromPolicyWithCallback(list.policy.id, function (data) {

                list.actions = data;
                list.loadingAct = false;

            });

        }

        function getPerimeterFromAssignment(assignment, type) {

            if (_.has(assignment, 'perimeter')) {
                return assignment.perimeter;
            }

            // if the call has not been made
            if (!_.has(assignment, 'callPerimeterInProgress')) {

                assignment.callPerimeterInProgress = true;

                switch (type) {

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

            function setPerimeterToAssignment(perimeter) {

                assignment.callPerimeterInProgress = false;
                assignment.perimeter = perimeter;

            }
        }

        function getCategoryFromAssignment(data, type) {

            if (_.has(data, 'category')) {
                return data.category;
            }

            // if the call has not been made
            if (!_.has(data, 'callCategoryInProgress')) {

                data.callCategoryInProgress = true;

                switch (type) {

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

            function setCategoryToData(category) {

                data.callCategoryInProgress = false;
                data.category = category;

            }
        }

        /**
         * @param index
         * @param assignment
         * @param type
         */
        function getDataFromAssignmentsIndex(index, assignment, type) {

            if (!_.has(assignment, 'assignments_value')) {
                // setting an array which will contains every value of the category
                assignment.assignments_value = Array.apply(null, new Array(assignment.assignments.length)).map(function () {
                    return {
                        data: {}
                    };
                });
            }

            if (_.has(assignment.assignments_value[index], 'callDataInProgress') && !assignment.assignments_value[index].callDataInProgress) {
                return assignment.assignments_value[index].data;
            }

            // if the call has not been made
            if (!_.has(assignment.assignments_value[index], 'callDataInProgress')) {

                assignment.assignments_value[index].callDataInProgress = true;

                switch (type) {

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

            function setDataToAssignment(data) {

                assignment.assignments_value[index].callDataInProgress = false;
                assignment.assignments_value[index].data = data;

            }
        }

        /**
         * Delete
         */

        function deleteSub(subject, dataId) {

            subject.loader = true;

            assignmentsService.subject.delete(list.policy.id, subject.subject_id, subject.subject_cat_id, dataId, deleteSubSuccess, deleteSubError);

            function deleteSubSuccess(data) {

                $translate('moon.policy.assignments.subject.delete.success').then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                manageSubjects();

                subject.loader = false;

            }

            function deleteSubError(reason) {

                $translate('moon.policy.assignments.subject.delete.error', {
                    subjectName: subject.name,
                    reason: reason.message
                }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                subject.loader = false;

            }
        }

        function deleteObj(object, dataId) {

            object.loader = true;

            assignmentsService.object.delete(list.policy.id, object.object_id, object.object_cat_id, dataId, deleteObjSuccess, deleteObjError);

            function deleteObjSuccess(data) {

                $translate('moon.policy.assignments.object.delete.success').then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                manageObjects();

                object.loader = false;

            }

            function deleteObjError(reason) {

                $translate('moon.policy.assignments.object.delete.error', {
                    objectName: object.name,
                    reason: reason.message
                }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                object.loader = false;
            }
        }

        function deleteAct(action, dataId) {

            action.loader = true;

            assignmentsService.action.delete(list.policy.id, action.action_id, action.action_cat_id, dataId, deleteActSuccess, deleteActError);

            function deleteActSuccess(data) {

                $translate('moon.policy.assignments.action.delete.success').then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                manageActions();

                action.loader = false;

            }

            function deleteActError(reason) {

                $translate('moon.policy.assignments.action.delete.error', {
                    actionName: action.name,
                    reason: reason.message
                }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                action.loader = false;

            }
        }

        function getSubjects() {
            return list.subjects ? list.subjects : [];
        }

        function getObjects() {
            return list.objects ? list.objects : [];
        }

        function getActions() {
            return list.actions ? list.actions : [];
        }

        function updateList(event, type) {

            switch(type){

                case ASSIGNMENTS_CST.TYPE.SUBJECT:

                    manageSubjects();
                    break;

                case ASSIGNMENTS_CST.TYPE.OBJECT:

                    manageObjects();
                    break;

                case ASSIGNMENTS_CST.TYPE.ACTION:

                    manageActions();
                    break;

                default :

                    activate();
                    break;

            }

        }

    }

})();