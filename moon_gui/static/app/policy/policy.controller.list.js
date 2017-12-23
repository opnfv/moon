(function() {

    'use strict';

    angular
        .module('moon')
        .controller('PolicyListController', PolicyListController);

    PolicyListController.$inject = ['$scope', 'policies', 'NgTableParams', '$filter', '$modal', '$rootScope'];

    function PolicyListController($scope, policies, NgTableParams, $filter, $modal, $rootScope) {

        var list = this;

        list.policies = policies;

        list.getPolicies = getPolicies;
        list.hasPolicies = hasPolicies;
        list.addPolicy = addPolicy;
        list.refreshPolicies = refreshPolicies;
        list.deletePolicy = deletePolicy;

        list.table = {};

        list.search = { query: '',
            find: searchPolicy,
            reset: searchReset };

        list.add = { modal: $modal({ template: 'html/policy/action/policy-add.tpl.html', show: false }),
            showModal: showAddModal };

        list.del = { modal: $modal({ template: 'html/policy/action/policy-delete.tpl.html', show: false }),
            showModal: showDeleteModal };

        activate();

        function activate(){

            newPoliciesTable();

        }


        /*
         * ---- events
         */

        var rootListeners = {

            'event:policyCreatedSuccess': $rootScope.$on('event:policyCreatedSuccess', policyCreatedSuccess),
            'event:policyCreatedError': $rootScope.$on('event:policyCreatedError', policyCreatedError),

            'event:policyDeletedSuccess': $rootScope.$on('event:policyDeletedSuccess', policyDeletedSuccess),
            'event:policyDeletedError': $rootScope.$on('event:policyDeletedError', policyDeletedError)

        };

        for (var unbind in rootListeners) {
            $scope.$on('$destroy', rootListeners[unbind]);
        }

        function getPolicies() {
            return (list.policies) ? list.policies : [];
        }

        function hasPolicies() {
            return list.getPolicies().length > 0;
        }

        function newPoliciesTable() {

            list.table = new NgTableParams({

                page: 1,            // show first page
                count: 10,          // count per page
                sorting: {
                    name: 'asc',
                    genre: 'asc'
                }

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


        /*
         * ---- search
         */

        function searchPolicy(policy){
            return (policy.name.indexOf(list.search.query) !== -1 || policy.genre.indexOf(list.search.query) !== -1 || policy.description.indexOf(list.search.query) !== -1);
        }

        function searchReset() {
            list.search.query = '';
        }

        /*
         * ---- add
         */
        function showAddModal() {
            list.add.modal.$promise.then(list.add.modal.show);
        }

        function policyCreatedSuccess(event, pdp) {

            list.addPolicy(pdp);
            list.refreshPolicies();

            list.add.modal.hide();

        }

        function policyCreatedError(event, pdp) {
            list.add.modal.hide();
        }

        function addPolicy(policy) {
            list.policies.push(policy);
        }

        function refreshPolicies() {

            list.table.total(list.policies.length);
            list.table.reload();

        }

        /*
         * ---- delete
         */

        function showDeleteModal(policy) {

            list.del.modal.$scope.policy = policy;
            list.del.modal.$promise.then(list.del.modal.show);

        }

        function deletePolicy(policy) {

            list.policies = _.chain(list.policies).reject({id: policy.id}).value();

        }

        function policyDeletedSuccess(event, policy) {

            list.deletePolicy(policy);
            list.refreshPolicies();

            list.del.modal.hide();

        }

        function policyDeletedError(event, policy) {
            list.del.modal.hide();
        }


    }

})();
