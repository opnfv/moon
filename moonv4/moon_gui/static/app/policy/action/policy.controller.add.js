(function() {

    'use strict';

    angular
        .module('moon')
        .controller('PolicyAddController', PolicyAddController);

    PolicyAddController.$inject = ['$scope', '$translate', 'alertService', 'formService', 'policyService', 'utilService', 'modelService'];

    function PolicyAddController($scope, $translate, alertService, formService, policyService, utilService, modelService) {

        var add = this;

        /*
         *
         */

        add.loading = false;

        add.form = {};

        add.policy =  {name: null, genre: null, description: null, model_id: null};

        add.genres = ['admin', 'authz'];

        add.models = [];

        add.modelsLoading = true;

        add.create = createPolicy;


        activate();

        function activate(){

            resolveModels();

        }

        /*
         *
         */

        function resolveModels() {

            modelService.findAllWithCallBack(resolveModelsCallback);

        }

        function resolveModelsCallback(models) {

            add.models = models;

            add.modelsLoading = false;

        }


        function createPolicy() {

            if(formService.isInvalid(add.form)) {

                formService.checkFieldsValidity(add.form);

            } else {


                add.loading = true;

                policyService.data.policy.create({}, {

                    name: add.policy.name,
                    description: add.policy.description,
                    genre: [add.selectedGenre],
                    model_id: add.selectedModel.id

                }, createSuccess, createError);

            }

            function createSuccess(data) {

                var createdPolicy = utilService.transformOne(data, 'policies');

                $translate('moon.policy.add.success', { policyName: createdPolicy.name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                add.loading = false;

                $scope.$emit('event:policyCreatedSuccess', createdPolicy);

            }

            function createError(reason) {

                $translate('moon.policy.add.error', { policyName: add.model.name }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                add.loading = false;

                $scope.$emit('event:policyCreatedError', add.project);

            }

        }

    }

})();
