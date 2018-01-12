(function() {

    'use strict';

    angular
        .module('moon')
        .controller('PolicyEditController', PolicyEditController);

    PolicyEditController.$inject = ['$scope', '$rootScope', 'policy', 'modelService'];

    function PolicyEditController($scope, $rootScope, policy, modelService) {

        var edit = this;

        edit.policy = policy;

        edit.editBasic = false;

        edit.showPerimeters = false;
        edit.showData = false;
        edit.showRules = false;
        edit.showAssignments = false;

        edit.showPart = showPart;


        activate();

        function showPart(partName) {
            var state = edit[partName];

            edit.showPerimeters = false;
            edit.showData = false;
            edit.showRules = false;
            edit.showAssignments = false;

            edit[partName] = !state;
        }


        function activate(){

            manageModel();

        }

        function manageModel(){

            edit.loadingModel = true;

            modelService.findOneWithCallback( edit.policy.model_id, function(model){

                edit.loadingModel = false;
                edit.policy.model = model;

            });

        }

        /*
         * ---- events
         */
        var rootListeners = {

            'event:policyUpdatedSuccess': $rootScope.$on('event:policyUpdatedSuccess', policyUpdatedSuccess)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }

        /**
         * When the model is updated, this function refresh the current model with the new changes
         * @param event
         * @param policy
         */
        function policyUpdatedSuccess(event, policy){

            edit.policy = policy;

            manageModel();

        }

    }

})();
