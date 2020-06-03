/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .controller('PolicyUnMapController', PolicyUnMapController);

    PolicyUnMapController.$inject = ['$scope', '$translate', 'alertService', 'pdpService', 'utilService'];

    function PolicyUnMapController($scope, $translate, alertService, pdpService, utilService) {

        var unmap = this;

        /*
         *
         */

        unmap.pdp = $scope.pdp;
        unmap.policy = $scope.policy;

        unmap.unMappingLoading = false;

        unmap.unmap = unMapPolicyToPdp;

        /*
         *
         */

        function unMapPolicyToPdp() {

            unmap.unMappingLoading = true;

            var pdpToUpdate = angular.copy(unmap.pdp);

            pdpToUpdate.security_pipeline = _.without(pdpToUpdate.security_pipeline, unmap.policy.id);

            pdpService.update(pdpToUpdate, unMapSuccess, unMapError);

            function unMapSuccess(data) {

                $translate('moon.policy.unmap.success', { pdpName: unmap.pdp.name, policyName: unmap.policy.name })
                    .then(function (translatedValue) {
                        alertService.alertSuccess(translatedValue);
                    });

                unmap.unMappingLoading = false;

                $scope.$emit('event:policyUnMappedToPdpSuccess',  utilService.transformOne(data, 'pdps'));

            }

            function unMapError(reason) {

                $translate('moon.policy.unmap.error', { pdpName: unmap.pdp.name, policyName: unmap.policy.name })
                    .then(function (translatedValue) {
                        alertService.alertError(translatedValue);
                    });

                unmap.unMappingLoading = false;

                $scope.$emit('event:policyUnMappedToPdpError');

            }

        }

    }

})();
