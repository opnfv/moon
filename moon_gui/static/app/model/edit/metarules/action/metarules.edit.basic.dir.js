(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonMetaRulesEditBasic', moonMetaRulesEditBasic);

    moonMetaRulesEditBasic.$inject = [];

    function moonMetaRulesEditBasic() {

        return {
            templateUrl : 'html/model/edit/metarules/action/metarules-edit-basic.tpl.html',
            bindToController : true,
            controller : moonMetaRulesEditBasicController,
            controllerAs : 'edit',
            scope : {
                metaRule : '='
            },
            restrict : 'E',
            replace : true
        };

    }

    angular
        .module('moon')
        .controller('moonMetaRulesEditBasicController', moonMetaRulesEditBasicController);

    moonMetaRulesEditBasicController.$inject = ['$scope', 'metaRuleService', 'formService', 'alertService', '$translate', 'utilService'];

    function moonMetaRulesEditBasicController($scope, metaRuleService, formService, alertService, $translate, utilService){

        var edit = this;

        edit.editMetaRule = editMetaRule;
        edit.init = init;

        edit.form = {};

        activate();

        function activate(){

            edit.metaRule = $scope.edit.metaRule;

            edit.metaRuleToEdit = angular.copy(edit.metaRule);

        }

        function editMetaRule(){

            if(formService.isInvalid(edit.form)) {

                formService.checkFieldsValidity(edit.form);

            }else{

                edit.loading = true;

                metaRuleService.update(edit.metaRuleToEdit, updateSuccess, updateError);

            }

            function updateSuccess(data) {

                var updatedMetaRule = utilService.transformOne(data, 'meta_rules');

                angular.copy(updatedMetaRule, edit.metaRule);

                $translate('moon.model.metarules.edit.basic.success', { metaRuleName: updatedMetaRule.name }).then( function(translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                edit.loading = false;

                $scope.$emit('event:metaRuleBasicUpdatedSuccess', edit.metaRule);

            }

            function updateError(reason) {

                $translate('moon.model.edit.basic.error', { metaRuleName: edit.metaRule.name }).then( function(translatedValue) {
                    alertService.alertError(translatedValue);
                });

                edit.loading = false;

            }
        }

        function init(){

            edit.metaRuleToEdit = angular.copy(edit.metaRule);

        }
    }

})();
