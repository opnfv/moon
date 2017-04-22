(function() {

    'use strict';

    angular
        .module('moon')
        .controller('ModelViewController', ModelViewController);

    ModelViewController.$inject = ['$scope', 'metaRuleService'];

    function ModelViewController($scope, metaRuleService) {

        var view = this;

        /*
         *
         */

        view.model = $scope.model;

        view.meta_rules_values = false;

        activate();

        function activate(){

            if(view.model.meta_rules.length > 0 ){

                findMetaRules();

            }else{

                view.meta_rules_values = [];

            }

        }

        function findMetaRules(){

            metaRuleService.findSomeWithMetaData(view.model.meta_rules).then(function(metaRules){

                view.meta_rules_values = metaRules;

                view.model.meta_rules_values = metaRules;

            });

        }

    }

})();
