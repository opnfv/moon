(function() {

    'use strict';

    angular
        .module('moon')
        .directive('moonPolicyMappedList', moonPolicyMappedList);

    moonPolicyMappedList.$inject = [];

    function moonPolicyMappedList() {

        return {
            templateUrl : 'html/policy/policy-mapped-list.tpl.html',
            bindToController : true,
            controller : moonPolicyMappedListController,
            controllerAs : 'list',
            scope : {
                pdp : '='
            },
            restrict : 'E',
            replace : true
        };
    }

    angular
        .module('moon')
        .controller('moonPolicyMappedListController', moonPolicyMappedListController);

    moonPolicyMappedListController.$inject = ['$scope', '$rootScope', 'NgTableParams', '$modal', '$filter', 'policyService'];

    function moonPolicyMappedListController($scope, $rootScope, NgTableParams, $modal, $filter,  policyService){

        var list = this;

        list.table = {};


        list.pdp = $scope.list.pdp;

        list.getPolicies = getPolicies;
        list.hasPolicies = hasPolicies;
        list.refreshPolicies = refreshPolicies;

        list.loadingPolicies = true;

        list.policies = [];


        activate();

        function activate() {

            loadPolicices(false);

        }

        /**
         *
         * @param refresh boolean, if !refresh then newPolicYtable will be called, if refresh, then refreshPolicies is called
         */
        function loadPolicices(refresh){

            if(_.isUndefined( list.pdp.security_pipeline)){
                return;
            }
            list.policiesId = list.pdp.security_pipeline;

            policyService.findSomeWithCallback(list.policiesId, function(policies){

                list.policies = policies;

                list.loadingPolicies = false;

                if(refresh){

                    refreshPolicies();

                }else{

                    newMPolicyTable();

                }

            });

        }

        list.map = { modal: $modal({ template: 'html/policy/action/mapping/policy-map.tpl.html', show: false }),
            showModal: showMapModal };

        list.unmap = { modal: $modal({ template: 'html/policy/action/mapping/policy-unmap.tpl.html', show: false }),
            showModal: showUnmapModal };

        /*
         * ---- events
         */
        var rootListeners = {

            'event:policyMapToPdpSuccess': $rootScope.$on('event:policyMapToPdpSuccess', policyMapToPdpSuccess),
            'event:policyMapToPdpError': $rootScope.$on('event:policyMapToPdpError', policyMapToPdpError),

            'event:policyUnMappedToPdpSuccess': $rootScope.$on('event:policyUnMappedToPdpSuccess', policyUnmappedSuccess),
            'event:policyUnMappedToPdpError': $rootScope.$on('event:policyUnMappedToPdpError', policyUnmappedError)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }



        function newMPolicyTable() {

            list.table = new NgTableParams({

                page: 1,            // show first page
                count: 10         // count per page

            }, {

                total: function () { return list.getPolicies().length; }, // length of data
                getData: function($defer, params) {

                    var orderedData = params.sorting() ? $filter('orderBy')(list.getPolicies(), params.orderBy()) : list.getPolicies();
                    $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));

                },
                $scope: { $data: {} }

            });

            return list.table;

        }


        function getPolicies() {
            return (list.policies) ? list.policies : [];
        }

        function hasPolicies() {
            return list.getPolicies().length > 0;
        }

        function refreshPolicies(){

            list.table.total(list.getPolicies().length);
            list.table.reload();

        }

        function showMapModal(){
            list.map.modal.$scope.pdp = list.pdp;
            list.map.modal.$promise.then(list.map.modal.show);
        }

        function showUnmapModal(policy){

            list.unmap.modal.$scope.pdp = list.pdp;
            list.unmap.modal.$scope.policy = policy;

            list.unmap.modal.$promise.then(list.unmap.modal.show);

        }

        function policyMapToPdpSuccess(event, pdp){

            list.pdp = pdp;

            loadPolicices(true);

            list.map.modal.hide();

        }


        function policyMapToPdpError(event) {

            list.map.modal.hide();

        }

        function policyUnmappedSuccess(event, pdp) {

            list.pdp = pdp;

            loadPolicices(true);

            list.unmap.modal.hide();

        }

        function policyUnmappedError(event) {
            list.unmap.modal.hide();
        }


    }

})();
