/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .controller('MetaRulesUnMapController', MetaRulesUnMapController);

    MetaRulesUnMapController.$inject = ['$scope', '$translate', 'alertService', 'modelService'];

    function MetaRulesUnMapController($scope, $translate, alertService, modelService) {

        var unmap = this;

        /*
         *
         */

        unmap.model = $scope.model;
        unmap.metaRule = $scope.metaRule;

        unmap.unMappingLoading = false;

        unmap.unmap = unMapModelToMetaRule;

        /*
         *
         */

        function unMapModelToMetaRule() {

            unmap.unMappingLoading = true;

            var modelToUpdate = angular.copy(unmap.model);

            modelToUpdate.meta_rules = _.without(modelToUpdate.meta_rules, unmap.metaRule.id);

            modelService.update(modelToUpdate, unMapSuccess, unMapError);

            function unMapSuccess(data) {

                $translate('moon.model.metarules.unmap.success', { modelName: unmap.model.name, metaRuleName: unmap.metaRule.name })
                    .then(function (translatedValue) {
                        alertService.alertSuccess(translatedValue);
                    });

                unmap.unMappingLoading = false;

                $scope.$emit('event:metaRuleUnMappedToModelSuccess', modelToUpdate);

            }

            function unMapError(reason) {

                $translate('moon.model.metarules.unmap.error', { modelName: unmap.model.name, metaRuleName: unmap.metaRule.name })
                    .then(function (translatedValue) {
                        alertService.alertError(translatedValue);
                    });

                unmap.unMappingLoading = false;

                $scope.$emit('event:metaRuleUnMappedToModelError');

            }

        }

    }

})();
