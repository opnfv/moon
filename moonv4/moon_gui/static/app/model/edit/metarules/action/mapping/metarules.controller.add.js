(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonMetaRulesAdd', moonMetaRulesAdd);

    moonMetaRulesAdd.$inject = [];

    function moonMetaRulesAdd() {

        return {
            templateUrl : 'html/model/edit/metarules/action/mapping/metarules-add.tpl.html',
            bindToController : true,
            controller : moonMetaRulesAddController,
            controllerAs : 'add',
            scope : {
                metaRules : '='
            },
            restrict : 'E',
            replace : true
        };
    }


    angular
        .module('moon')
        .controller('moonMetaRulesAddController', moonMetaRulesAddController);

    moonMetaRulesAddController.$inject = ['$scope', 'metaRuleService', 'alertService', '$translate', 'formService', 'utilService'];

    function moonMetaRulesAddController($scope, metaRuleService, alertService, $translate, formService, utilService) {

        var add = this;

        /*
         *
         */

        add.laoading = false;

        add.form = {};

        add.metaRule = { name: null, description: null, subject_categories : [], object_categories : [], action_categories : [] };

        add.create = createMetaRule;

        activate();

        function activate(){

        }

        function createMetaRule() {

            if(formService.isInvalid(add.form)) {

                formService.checkFieldsValidity(add.form);

            } else {

                add.loading = true;

                metaRuleService.data.create({}, add.metaRule, createSuccess, createError);

            }

            function createSuccess(data) {

                var createdMetaRule = utilService.transformOne(data, 'meta_rules');

                $translate('moon.model.metarules.add.success', { metaRuleName: createdMetaRule.name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                add.loading = false;

                $scope.$emit('event:metaRuleCreatedSuccess', createdMetaRule);

            }

            function createError(reason) {

                $translate('moon.model.metarules.add.error', { metaRuleName: add.metaRule.name }).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                add.loading = false;

                $scope.$emit('event:metaRuleCreatedError', add.project);

            }

        }

    }

})();
