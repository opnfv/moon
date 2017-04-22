(function() {

    'use strict';

    angular
        .module('moon')
        .controller('PolicyMapController', PolicyMapController);

    PolicyMapController.$inject = ['$scope', 'alertService', '$translate', 'formService', 'policyService', 'pdpService', 'utilService'];

    function PolicyMapController($scope, alertService, $translate, formService, policyService, pdpService,  utilService ) {

        var map = this;

        /*
         *
         */

        map.pdps = [];

        map.pdp = $scope.pdp;

        map.addPolicyToList = false;

        map.map = mapToPdp;

        activate();

        function activate() {

            resolvePolicies();

        }

        function resolvePolicies() {

            map.policiesLoading = true;

            policyService.findAllWithCallback(function(policies){
                    map.policies = policies;
                    map.policiesLoading = false;
                }
            );

        }

        function mapToPdp() {

            if (formService.isInvalid(map.form)) {

                formService.checkFieldsValidity(map.form);

            } else {

                map.mappingLoading = true;

                var pdpToSend = angular.copy(map.pdp);

                pdpToSend.security_pipeline.push(map.selectedPolicy.id);

                pdpService.update(pdpToSend, mapSuccess, mapError);

            }

            function mapSuccess(data) {

                var pdpReceived = utilService.transformOne(data, 'pdps');


                $translate('moon.policy.map.success', {pdpName: pdpReceived.name, policyName: map.selectedPolicy.name}).then(function (translatedValue) {

                    alertService.alertSuccess(translatedValue);

                });

                map.mappingLoading = false;

                $scope.$emit('event:policyMapToPdpSuccess', pdpReceived);

            }

            function mapError(response) {

                $translate('moon.policy.map.error', {

                    pdpName: map.pdp.name,
                    policyName: map.selectedPolicy.name

                }).then(function (translatedValue) {

                    alertService.alertError(translatedValue);

                });

                map.mappingLoading = false;

                $scope.$emit('event:policyMapToPdpError');

            }
        }



    }

})();