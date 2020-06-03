(function() {

    'use strict';

    angular
        .module('moon')
        .controller('MetaRulesEditController', MetaRulesEditController);

    MetaRulesEditController.$inject = ['$scope', '$rootScope'];

    function MetaRulesEditController($scope, $rootScope) {

        var edit = this;

        edit.metaRule = $scope.metaRule;

        activate();

        function activate(){
        }


        /*
         * ---- events
         */
        var rootListeners = {

            'event:metaRuleBasicUpdatedSuccess': $rootScope.$on('event:metaRuleBasicUpdatedSuccess', metaRuleUpdatedSuccess)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }

        /**
         * When the MetaRule is updated, this function refresh the current metaRule with the new changes
         * @param event
         * @param metaRule
         */
        function metaRuleUpdatedSuccess(event, metaRule){

            angular.copy(metaRule, edit.metaRule);

        }

    }

})();
