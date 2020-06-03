/**
 * Service providing access to the tenants
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('policyService', policyService);

    policyService.$inject = ['$resource', 'REST_URI', 'utilService', '$q'];

    function policyService($resource, REST_URI, utilService, $q) {

        return {

            data: {

                policy: $resource(REST_URI.POLICIES + ':policy_id', {}, {
                    query: {method: 'GET'},
                    create: { method: 'POST' },
                    update: { method: 'PATCH' },
                    remove: { method: 'DELETE' }
                })

            },

            findAll: function () {

                return this.data.policy.query().$promise.then(function (data) {

                    return utilService.transform(data, 'policies');

                });

            },

            findAllWithCallback: function (callback) {

                return this.data.policy.query().$promise.then(function (data) {

                    callback(utilService.transform(data, 'policies'));

                });

            },

            findOneReturningPromise: function(policyId){

                return this.data.policy.get({policy_id: policyId}).$promise;

            },

            findSomeWithCallback: function(policyListId, callback){

                var _self = this;

                if(policyListId.length === 0){
                    callback([]);
                }

                var promises = _(policyListId).map( function(policyId) {

                    return _self.findOneReturningPromise(policyId);

                });

                $q.all(promises).then( function(result) {

                    callback( _(result).map( function(resource) {

                        return utilService.transformOne(resource, 'policies');

                    }));

                });

            },

            findOne: function (policyId) {

                return this.data.policy.get({policy_id: policyId}).$promise.then(function (data) {

                    return utilService.transformOne(data, 'policies');

                });

            },

            update: function (policy, callbackSuccess, callbackError) {

                this.data.policy.update({policy_id: policy.id}, policy, callbackSuccess, callbackError);

            },

            delete: function (policy, callbackSuccess, callbackError ) {

                this.data.policy.remove({policy_id: policy.id}, policy, callbackSuccess, callbackError);

            }

        }
    }

})();
