(function() {

    'use strict';

    angular
        .module('moon')
        .controller('moonMetaRulesMapController', moonMetaRulesMapController);

    moonMetaRulesMapController.$inject = ['$scope', '$rootScope', 'alertService', '$translate', 'formService', 'metaRuleService', 'modelService', 'utilService'];

    function moonMetaRulesMapController($scope, $rootScope, alertService, $translate, formService, metaRuleService, modelService, utilService ) {

        var map = this;

        /*
         *
         */

        map.metaRules = [];

        map.model = $scope.model;

        map.addMetaRuleToList = false;

        map.mapToModel = mapToModel;

        map.deleteMetaRule = deleteMetaRule;

        activate();

        function activate() {

            resolveMetaRules();

        }

        /*
         * ---- events
         */
        var rootListeners = {

            'event:metaRuleCreatedSuccess': $rootScope.$on('event:metaRuleCreatedSuccess', metaRuleCreatedSuccess),
            'event:metaRuleCreatedError': $rootScope.$on('event:metaRuleCreatedError', metaRuleCreatedError)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }


        /*
         *
         */

        function resolveMetaRules() {

            map.metaRulesLoading = true;

           metaRuleService.findAllWithCallback(
                function(metaRules){
                    map.metaRules = metaRules;
                    map.metaRulesLoading = false;
                }
            );

        }

        function mapToModel() {

            if (formService.isInvalid(map.form)) {

                formService.checkFieldsValidity(map.form);

            } else {

                map.mappingLoading = true;

                var modelToSend = angular.copy(map.model);

                modelToSend.meta_rules.push(map.selectedMetaRule.id);

                modelService.update(modelToSend, mapSuccess, mapError);

            }

            function mapSuccess(data) {

                var modelReceived = utilService.transformOne(data, 'models');

                metaRuleService.findSomeWithMetaData(modelReceived.meta_rules).then(function(metaRules){

                    modelReceived.meta_rules_values  = metaRules;

                    $translate('moon.model.metarules.map.success', {

                        modelName: modelReceived.name,
                        metaRuleName: map.selectedMetaRule.name

                    }).then(function (translatedValue) {

                        alertService.alertSuccess(translatedValue);

                    });

                    map.mappingLoading = false;

                    $scope.$emit('event:metaRuleMapToModelSuccess', modelReceived);

                });

            }

            function mapError(response) {

                $translate('moon.model.metarules.map.error', {

                    modelName: map.model.name,
                    metaRuleName: map.selectedMetaRule.name

                }).then(function (translatedValue) {

                    alertService.alertError(translatedValue);

                });

                map.mappingLoading = false;

            }
        }

        function cleanSelectedValue(){

            delete map.selectedMetaRule;

        }


        function deleteMetaRule(){

            if(!map.selectedMetaRule){

                return;

            }

            map.mappingLoading = true;

            var metaRuleTodelete = angular.copy(map.selectedMetaRule);

            metaRuleService.delete(metaRuleTodelete, deleteSuccess, deleteError);

            function deleteSuccess(data) {

                $translate('moon.model.metarules.delete.success', { metaRuleName: metaRuleTodelete.name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                cleanSelectedValue();

                map.mappingLoading = false;

                resolveMetaRules();

                // later this event will have to be catch, because the model can use the deleted MetaRule
                $scope.$emit('event:deleteMetaRule', metaRuleTodelete);

            }

            function deleteError(reason) {

                $translate('moon.model.metarules.delete.error', { metaRuleName: metaRuleTodelete.name }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                map.mappingLoading = false;

            }
        }






        /**
         * This function will add a metaRule to the current list of metaRules
         * @param event
         * @param metaRule {...} metaRule to add
         */
        function metaRuleCreatedSuccess(event, metaRule) {

            map.metaRules.push(metaRule);
            showList();

        }

        /**
         * This function hide the add MetaRule Modal
         * @param event
         */
        function metaRuleCreatedError(event) {

        }

        function showList(){
            map.addMetaRuleToList = false;
        }

    }


})();