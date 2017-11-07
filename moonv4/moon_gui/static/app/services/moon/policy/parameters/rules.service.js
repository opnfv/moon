/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('rulesService', rulesService);

    rulesService.$inject = ['$resource', 'REST_URI', 'utilService'];

    function rulesService($resource, REST_URI, utilService) {

        return {

            data: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/rules/:rule_id', {}, {
                    get: {method: 'GET'},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },

            add: function (rules, policyId, callbackSuccess, callbackError ) {

                this.data.policy.create({policy_id: policyId}, rules, callbackSuccess, callbackError);

            },

            delete: function (ruleId, policyId, callbackSuccess, callbackError ) {

                this.data.policy.remove({policy_id: policyId, rule_id: ruleId}, {}, callbackSuccess, callbackError);

            },

            findAllFromPolicyWithCallback: function(policyId, callback){

                this.data.policy.get({policy_id: policyId}).$promise.then(function(data) {

                    callback(data.rules.rules);
                    //callback(utilService.transform(data['rules'], 'rules'));

                });

            }


        }

    }
})();