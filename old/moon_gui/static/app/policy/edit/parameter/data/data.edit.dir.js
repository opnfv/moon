(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonDataEdit', moonDataEdit);

    moonDataEdit.$inject = [];

    function moonDataEdit() {

        return {
            templateUrl : 'html/policy/edit/parameter/data/data-edit.tpl.html',
            bindToController : true,
            controller : moonDataEditController,
            controllerAs : 'edit',
            scope : {
                //Type can be 'ACTION', 'OBJECT', 'SUBJECT'
                mnDataType: '=',
                policy : '='
            },
            restrict : 'E',
            replace : true
        };

    }

    angular
        .module('moon')
        .controller('moonDataEditController', moonDataEditController);

    moonDataEditController.$inject = ['$scope', 'dataService', 'DATA_CST', 'alertService', '$translate',
        'formService', 'policyService', 'utilService', 'metaDataService', 'modelService', 'metaRuleService'];

    function moonDataEditController($scope, dataService, DATA_CST, alertService, $translate,
                                    formService, policyService, utilService, metaDataService, modelService, metaRuleService) {

        var edit = this;

        edit.dataType = $scope.edit.mnDataType;
        edit.policy = $scope.edit.policy;

        edit.fromList = false;

        edit.loading = false;

        edit.form = {};

        edit.data = { name: null, description: null};

        edit.list = [];
        edit.categoriesToBeSelected = [];

        edit.create = createData;

        activate();

        /*
         *
         */

        function activate(){

            loadAllCategories();

            switch(edit.dataType){

                case DATA_CST.TYPE.SUBJECT:

                    dataService.subject.findAllFromPolicyWithCallback(edit.policy.id, callBackList);
                    break;

                case DATA_CST.TYPE.OBJECT:

                    dataService.object.findAllFromPolicyWithCallback(edit.policy.id, callBackList);
                    break;

                case DATA_CST.TYPE.ACTION:

                    dataService.action.findAllFromPolicyWithCallback(edit.policy.id, callBackList);
                    break;

                default :

                    edit.list = [];
                    break;

            }

            function callBackList(list){

                // For each Data, there is a check about the mapping between the Data and the policy
                _.each(list, function (element) {
                    if (element.policy_id !== edit.policy.id) {

                        edit.list.push(element);

                    }
                });

            }

        }


        function loadAllCategories(){

            modelService.findOneWithCallback(edit.policy.model_id, function(model){

                metaRuleService.findSomeWithCallback(model.meta_rules, function(metaRules){

                    switch(edit.dataType){

                        case DATA_CST.TYPE.SUBJECT:
                            var subjectCategoryList = _.reduce(metaRules, function(result, metaRule) {
                                return result.concat(metaRule.subject_categories);
                            }, [])
                            metaDataService.subject.findSomeWithCallback(subjectCategoryList, callBackList);
                            break;
        
                        case DATA_CST.TYPE.OBJECT:
                            var objectCategoryList = _.reduce(metaRules, function(result, metaRule) {
                                return result.concat(metaRule.object_categories);
                            }, [])
                            metaDataService.object.findSomeWithCallback(objectCategoryList, callBackList);
                            break;
        
                        case DATA_CST.TYPE.ACTION:
                            var actionCategoryList = _.reduce(metaRules, function(result, metaRule) {
                                return result.concat(metaRule.action_categories);
                            }, [])
                            metaDataService.action.findSomeWithCallback(actionCategoryList, callBackList);
                            break;
        
                        default :
        
                            edit.categoriesToBeSelected = [];
                            break;
        
                    }
        
                    function callBackList(list){
        
                        edit.categoriesToBeSelected = list;
        
                    }
                });

            });

            
        }

        /**
         * Create
         */

        function createData() {

            if(formService.isInvalid(edit.form)) {

                formService.checkFieldsValidity(edit.form);

            } else {

                startLoading();

                var dataToSend = angular.copy(edit.data);

                switch(edit.dataType){

                    case DATA_CST.TYPE.SUBJECT:

                        dataService.subject.add(dataToSend, edit.policy.id, edit.selectedCategory.id, createSuccess, createError);
                        break;

                    case DATA_CST.TYPE.OBJECT:

                        dataService.object.add(dataToSend, edit.policy.id, edit.selectedCategory.id, createSuccess, createError);
                        break;

                    case DATA_CST.TYPE.ACTION:

                        dataService.action.add(dataToSend, edit.policy.id, edit.selectedCategory.id, createSuccess, createError);
                        break;
                }

            }

            /**
             * @param data
             */
            function createSuccess(data) {

                var created = {};
                var name = '';

                switch(edit.dataType){

                    case DATA_CST.TYPE.SUBJECT:

                        created = utilService.transformOne(data['subject_data'], 'data');
                        name = created.name;
                        break;

                    case DATA_CST.TYPE.OBJECT:

                        created = utilService.transformOne(data['object_data'], 'data');
                        name = created.value.name;
                        break;

                    case DATA_CST.TYPE.ACTION:

                        created = utilService.transformOne(data['action_data'], 'data');
                        name = created.value.name;
                        break;
                }

                $translate('moon.policy.data.edit.create.success', { name: name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                $scope.$emit('event:createDataFromDataEditSuccess', created, edit.dataType);

                stopLoading();

                edit.list.push(created);

            }

            function createError(reason) {

                $translate('moon.policy.data.edit.create.error', { name: dataToSend.name }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                stopLoading();

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