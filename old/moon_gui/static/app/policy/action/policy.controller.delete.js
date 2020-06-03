
(function() {

    'use strict';

    angular
        .module('moon')
        .controller('PolicyDeleteController', PolicyDeleteController);

    PolicyDeleteController.$inject = ['$scope', '$translate', 'alertService', 'policyService'];

    function PolicyDeleteController($scope, $translate, alertService, policyService) {

        var del = this;

        /*
         *
         */

        del.policy = $scope.policy;
        del.loading = false;

        del.remove = deletePolicy;

        activate();

        /**
         *
         */

        function activate(){

        }


        function deletePolicy(){

            del.loading = true;

            policyService.delete(del.policy, deleteSuccess, deleteError);

            function deleteSuccess(data) {

                $translate('moon.policy.remove.success', { policyName: del.policy.name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                del.loading = false;

                $scope.$emit('event:policyDeletedSuccess', del.policy);

            }

            function deleteError(reason) {

                $translate('moon.policy.remove.error', { policyName: del.policy.name, errorCode: reason.data.error.code, message : reason.data.error.message } ).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                del.loading = false;

                $scope.$emit('event:policyDeletedError', del.policy);

            }

        }
    }

})();
