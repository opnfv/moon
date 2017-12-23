(function() {

    'use strict';

    angular
        .module('moon')
        .controller('PDPEditController', PDPEditController);

    PDPEditController.$inject = ['$scope', '$rootScope', 'pdp', '$stateParams'];

    function PDPEditController($scope, $rootScope, pdp, $stateParams) {

        var edit = this;

        edit.pdp = pdp;

        edit.editBasic = false;

        activate();

        function activate(){

        }

        /*
         * ---- events
         */
        var rootListeners = {

            'event:pdpUpdatedSuccess': $rootScope.$on('event:pdpUpdatedSuccess', pdpUpdatedSuccess)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }

        /**
         * When the model is updated, this function refresh the current model with the new changes
         * @param event
         * @param pdp
         */
        function pdpUpdatedSuccess(event, pdp){

            edit.pdp = pdp;

        }
    }

})();
