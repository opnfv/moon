/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('ruleService', ruleService);

    ruleService.$inject = ['$resource', 'REST_URI', 'utilService'];

    function ruleService($resource, REST_URI, utilService) {

        return {

            data: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/rules/:rule_id', {}, {
                    get: {method: 'GET'},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },

            findAllFromPolicyWithCallback: function(policyId, callback){

                this.data.policy.get({policy_id: policyId}).$promise.then(function(data) {

                    console.log('ruleService - findAllFromPolicyWithCallback()');
                    console.log(data);

                    var array = data['rules'];

                    console.log(JSON.stringify(array));
                    callback(utilService.transform(array, 'rules'));

                });

            }


        }

    }
})();