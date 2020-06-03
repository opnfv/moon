(function() {

    'use strict';

    angular
        .module('moon')
        .controller('ModelEditController', ModelEditController);

    ModelEditController.$inject = ['$scope', '$rootScope', 'model', 'metaRuleService'];

    function ModelEditController($scope, $rootScope, model, metaRuleService) {

        var edit = this;

        edit.model = model;

        edit.editBasic = false;

        edit.editMetaRules = true;

        activate();

        function activate(){

        }

        /*
         * ---- events
         */
        var rootListeners = {

            'event:modelUpdatedSuccess': $rootScope.$on('event:modelUpdatedSuccess', modelUpdatedSuccess),

            'event:updateModelFromMetaRuleAddSuccess': $rootScope.$on('event:updateModelFromMetaRuleAddSuccess', modelUpdatedSuccess)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }

        /**
         * When the model is updated, this function refresh the current model with the new changes
         * @param event
         * @param model
         */
        function modelUpdatedSuccess(event, model){

            edit.model = model;

            metaRuleService.findSomeWithCallback(model.meta_rules, function(metaRules){

                edit.model.meta_rules_values = metaRules;

            });

        }

    }

})();
