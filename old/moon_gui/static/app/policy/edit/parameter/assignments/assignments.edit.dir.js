(function () {

    'use strict';

    angular
        .module('moon')
        .directive('moonAssignmentsEdit', moonAssignmentsEdit);

    moonAssignmentsEdit.$inject = [];

    function moonAssignmentsEdit() {

        return {
            templateUrl: 'html/policy/edit/parameter/assignments/assignments-edit.tpl.html',
            bindToController: true,
            controller: moonAssignmentsEditController,
            controllerAs: 'edit',
            scope: {
                //Type can be 'ACTION', 'OBJECT', 'SUBJECT'
                assignmentsType: '=',
                policy: '='
            },
            restrict: 'E',
            replace: true
        };
    }

    angular
        .module('moon')
        .controller('moonAssignmentsEditController', moonAssignmentsEditController);

    moonAssignmentsEditController.$inject = ['$scope', 'assignmentsService', 'alertService', '$translate', 'formService',
        'policyService', 'utilService', 'perimeterService', 'ASSIGNMENTS_CST',
        'metaDataService', 'dataService'];

    function moonAssignmentsEditController($scope, assignmentsService, alertService, $translate, formService,
                                           policyService, utilService, perimeterService, ASSIGNMENTS_CST,
                                           metaDataService, dataService ) {

        var edit = this;

        edit.assignmentsType = $scope.edit.assignmentsType;
        edit.policy = $scope.edit.policy;

        edit.laoading = false;

        edit.form = {};

        edit.policyList = [];
        edit.loadingPolicies = true;

        edit.categoryList = [];
        edit.loadingCategories = true;

        edit.perimeterList = [];
        edit.loadingPerimeters = true;

        edit.dataList = [];
        edit.dataToBeSelected = [];
        edit.selectedDataList = [];
        edit.loadingData = true;

        edit.assignementsAttributeValid = true;

        edit.addSelectedData = addSelectedData;
        edit.removeSelectedData = removeSelectedData;
        edit.getName = getName;
        edit.create = createAssignments;

        activate();

        /*
         *
         */

        function activate() {

            edit.assignments = {id: null, category_id: null, data_id: null, policy_id: null};

            loadAllPolicies();
            loadAllCategories();

        }

        function createAssignments() {

            edit.assignementsAttributeValid = true;

            manageSelectedDataListy();

            if(formService.isInvalid(edit.form)) {

                formService.checkFieldsValidity(edit.form);

            }else if(edit.assignementsAttributeValid){

                startLoading();

                var throwEvent = false;
                edit.assignments.id = edit.selectedPerimeter.id;
                edit.assignments.category_id = edit.selectedCategory.id;
                edit.assignments.policy_id = edit.selectedPolicy.id;

                var selectedDataListTemp = angular.copy(edit.selectedDataList);

                _.each(selectedDataListTemp, function(elem){

                    edit.assignments.data_id = elem.id;

                    var assignmentsToSend = angular.copy(edit.assignments);

                    switch(edit.assignmentsType){

                        case ASSIGNMENTS_CST.TYPE.SUBJECT:

                            assignmentsService.subject.add(assignmentsToSend, edit.policy.id, createSuccess, createError);
                            break;

                        case ASSIGNMENTS_CST.TYPE.OBJECT:

                            assignmentsService.object.add(assignmentsToSend, edit.policy.id, createSuccess, createError);
                            break;

                        case ASSIGNMENTS_CST.TYPE.ACTION:

                            assignmentsService.action.add(assignmentsToSend, edit.policy.id, createSuccess, createError);
                            break;

                        default :

                            break;

                    }

                });

                throwEvent = true;

            }

            function createSuccess(data) {

                var created = {};

                switch(edit.assignmentsType){

                    case ASSIGNMENTS_CST.TYPE.SUBJECT:

                        created = utilService.transformOne(data, 'subject_assignments');
                        break;

                    case ASSIGNMENTS_CST.TYPE.OBJECT:

                        created = utilService.transformOne(data, 'object_assignments');
                        break;

                    case ASSIGNMENTS_CST.TYPE.ACTION:

                        created = utilService.transformOne(data, 'action_assignments');
                        break;

                    default:

                        break;

                }

                $translate('moon.policy.assignments.edit.create.success').then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                if(throwEvent && created.policy_id === edit.policy.id){

                    $scope.$emit('event:createAssignmentsFromAssignmentsEditSuccess', edit.assignmentsType);

                    activate();

                    stopLoading();

                }else if(throwEvent){

                    activate();

                    stopLoading();

                }

            }

            function createError(reason) {

                $translate('moon.policy.rules.edit.action.add.create.error').then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                stopLoading();

            }

        }

        $scope.$watch('edit.selectedPolicy', function(newValue){

            if(!_.isUndefined(newValue)){

                loadRelatedPerimeters();

            }

        });


        $scope.$watch('edit.selectedCategory', function(newValue){

            clearSelectedCategories();

            if(!_.isUndefined(newValue)){

                loadRelatedData(newValue.id);

            }

        });

        function loadAllPolicies() {

            edit.policyList = [];
            edit.loadingPolicies = true;

            policyService.findAllWithCallback( function(data) {

                _.each(data, function(element){

                    if(element.id === edit.policy.id){
                        edit.selectedPolicy = element;
                    }

                });

                edit.policyList = data;
                edit.loadingPolicies = false;

            });
        }

        function loadRelatedPerimeters(){

            edit.perimeterList = [];
            edit.loadingPerimeters = true;

            switch(edit.assignmentsType){

                case ASSIGNMENTS_CST.TYPE.SUBJECT:

                    perimeterService.subject.findAllFromPolicyWithCallback(edit.selectedPolicy.id, callBackList);
                    break;

                case ASSIGNMENTS_CST.TYPE.OBJECT:

                    perimeterService.object.findAllFromPolicyWithCallback(edit.selectedPolicy.id,callBackList);
                    break;

                case ASSIGNMENTS_CST.TYPE.ACTION:

                    perimeterService.action.findAllFromPolicyWithCallback(edit.selectedPolicy.id, callBackList);
                    break;

                default :

                    edit.perimeterList = [];
                    edit.loadingPerimeters = false;
                    break;

            }

            function callBackList(list){

                edit.perimeterList = list;

                edit.loadingPerimeters = false;

            }
        }

        function loadAllCategories(){

            edit.categoryList = [];
            edit.loadingCategories = true;

            switch(edit.assignmentsType){

                case ASSIGNMENTS_CST.TYPE.SUBJECT:

                    metaDataService.subject.findAllWithCallback(callBackList);
                    break;

                case ASSIGNMENTS_CST.TYPE.OBJECT:

                    metaDataService.object.findAllWithCallback(callBackList);
                    break;

                case ASSIGNMENTS_CST.TYPE.ACTION:

                    metaDataService.action.findAllWithCallback(callBackList);
                    break;

                default :

                    edit.categoryList = [];
                    edit.loadingCategories = false;
                    break;

            }

            function callBackList(list){

                edit.categoryList = list;
                edit.loadingCategories = false;

            }
        }

        function loadRelatedData(categoryId){

            edit.dataList = [];
            edit.dataToBeSelected = [];
            edit.selectedDataList = [];
            edit.loadingData = true;

            switch(edit.assignmentsType){

                case ASSIGNMENTS_CST.TYPE.SUBJECT:

                    dataService.subject.findAllFromCategoriesWithCallback(edit.selectedPolicy.id, categoryId, callBackList);
                    break;

                case ASSIGNMENTS_CST.TYPE.OBJECT:

                    dataService.object.findAllFromCategoriesWithCallback(edit.selectedPolicy.id, categoryId, callBackList);
                    break;

                case ASSIGNMENTS_CST.TYPE.ACTION:

                    dataService.action.findAllFromCategoriesWithCallback(edit.selectedPolicy.id, categoryId, callBackList);
                    break;

                default :

                    edit.loadingData = false;
                    break;

            }

            function callBackList(list){

                edit.dataList = list;
                edit.dataToBeSelected = angular.copy(edit.dataList);
                edit.selectedDataList = [];
                edit.loadingData = false;

            }

        }

        function addSelectedData(){

            edit.dataToBeSelected = _.without(edit.dataToBeSelected, edit.selectedData);
            edit.selectedDataList.push(edit.selectedData);
            clearSelectedCategories();

        }

        function removeSelectedData(data){

            edit.dataToBeSelected.push(data);
            edit.selectedDataList = _.without(edit.selectedDataList, data);

        }

        function clearSelectedCategories(){

            edit.selectedData = undefined;

        }

        function getName(assignment){

            if(_.isUndefined(assignment)) return '(None)';

            switch(edit.assignmentsType){

                case ASSIGNMENTS_CST.TYPE.SUBJECT:

                    return assignment.name;

                case ASSIGNMENTS_CST.TYPE.OBJECT:

                    return assignment.value.name;


                case ASSIGNMENTS_CST.TYPE.ACTION:

                    return assignment.value.name;

                default :

                    return assignment.name;

            }

        }

        function manageSelectedDataListy(){

            if (edit.selectedDataList.length >= 1 ){

                edit.assignementsAttributeValid = true;

            }else{

                edit.assignementsAttributeValid = false;

            }
        }

        function startLoading(){

            edit.loading = true;

        }

        function stopLoading(){

            edit.loading = false;

        }
    }

})();