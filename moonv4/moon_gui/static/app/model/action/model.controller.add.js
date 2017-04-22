(function() {

    'use strict';

    angular
        .module('moon')
        .controller('ModelAddController', ModelAddController);

    ModelAddController.$inject = ['$scope', 'modelService', 'alertService', '$translate', 'formService', 'utilService'];

    function ModelAddController($scope, modelService, alertService, $translate, formService, utilService) {

        var add = this;

        /*
         *
         */

        add.form = {};

        add.loading = false;

        add.model = { name: null, description: null, meta_rules : [] };

        add.create = createModel;

        function createModel() {

            if(formService.isInvalid(add.form)) {

                formService.checkFieldsValidity(add.form);

            } else {

                add.loading = true;

                modelService.data.create({}, add.model, createSuccess, createError);

            }

            function createSuccess(data) {

                var createdModel = utilService.transformOne(data, 'models');

                $translate('moon.model.add.success', { modelName: createdModel.name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                add.loading = false;

                $scope.$emit('event:modelCreatedSuccess', createdModel);

            }

            function createError(reason) {

                $translate('moon.model.add.error', { modelName: add.model.name }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                add.loading = false;

                $scope.$emit('event:modelCreatedError', add.project);

            }

        }

    }

})();
