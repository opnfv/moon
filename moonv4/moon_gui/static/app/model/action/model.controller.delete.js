/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .controller('ModelDeleteController', ModelDeleteController);

    ModelDeleteController.$inject = ['$scope', '$translate', 'alertService', 'modelService'];

    function ModelDeleteController($scope, $translate, alertService, modelService) {

        var del = this;

        /*
         *
         */

        del.model = $scope.model;
        del.loading = false;

        del.remove = deleteModel;

        activate();

        /**
         *
         */

        function activate(){

        }


        function deleteModel(){

            del.loading = true;

            modelService.delete(del.model, deleteSuccess, deleteError);

            function deleteSuccess(data) {

                $translate('moon.model.remove.success', { modelName: del.model.name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                del.loading = false;

                $scope.$emit('event:modelDeletedSuccess', del.model);

            }

            function deleteError(reason) {

                $translate('moon.model.remove.error', { modelName: del.model.name, errorCode: reason.data.error.code, message : reason.data.error.message } ).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                del.loading = false;

                $scope.$emit('event:modelDeletedError', del.model);

            }

        }
    }

})();
