(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonPolicyEditBasic', moonPolicyEditBasic);

    moonPolicyEditBasic.$inject = [];

    function moonPolicyEditBasic() {

        return {
            templateUrl : 'html/policy/edit/policy-edit-basic.tpl.html',
            bindToController : true,
            controller : moonPolicyEditBasicController,
            controllerAs : 'edit',
            scope : {
                policy : '='
            },
            restrict : 'E',
            replace : true
        };
    }

    angular
        .module('moon')
        .controller('moonPolicyEditBasicController', moonPolicyEditBasicController);

    moonPolicyEditBasicController.$inject = ['$scope', 'policyService', 'formService', 'alertService', '$translate', 'utilService', 'modelService'];

    function moonPolicyEditBasicController($scope, policyService, formService, alertService, $translate, utilService, modelService){

        var edit = this;

        edit.editPolicy = editPolicy;
        edit.init = init;

        edit.form = {};
        edit.modelsLoading = true;


        activate();

        function activate(){

            edit.policy = $scope.edit.policy;

            edit.policyToEdit = angular.copy(edit.policy);

            console.log(edit.policyToEdit);

            resolveModels();

        }

        /*
         *
         */

        function resolveModels() {

            modelService.findAllWithCallBack(resolveModelsCallback);

        }

        function resolveModelsCallback(models) {

            edit.models = models;

            _.each(models, function(model){

                if(model.id === edit.policy.model_id){
                    edit.selectedModel = model;
                }

            });

            edit.modelsLoading = false;

        }


        function editPolicy(){

            if(formService.isInvalid(edit.form)) {

                formService.checkFieldsValidity(edit.form);

            }else{

                edit.loading = true;

                delete edit.policyToEdit.model;

                edit.policyToEdit.model_id = edit.selectedModel.id;

                policyService.update(edit.policyToEdit, updateSuccess, updateError);

            }

            function updateSuccess(data) {

                var updatedPolicy = utilService.transformOne(data, 'policies');

                $translate('moon.policy.edit.basic.success', { policyName: updatedPolicy.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                edit.loading = false;

                $scope.$emit('event:policyUpdatedSuccess', updatedPolicy);

            }

            function updateError(reason) {

                $translate('moon.policy.edit.basic.error', { policyName: edit.policy.name }).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                edit.loading = false;

            }
        }

        function init(){

            edit.policyToEdit = angular.copy(edit.policy);

        }
    }

})();
