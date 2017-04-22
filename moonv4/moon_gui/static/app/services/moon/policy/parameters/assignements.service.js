/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('assignmentService', assignmentService);

    assignmentService.$inject = ['$resource', 'REST_URI', 'utilService'];

    function assignmentService($resource, REST_URI, utilService) {

        var data =  {

            subject: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/subject_assignments/:subject_id', {}, {
                    get: {method: 'GET'},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },


            object: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/object_assignments/:object_id', {}, {
                    get: {method: 'GET', isArray: false},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },

            action: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/action_assignments/:action_id', {}, {
                    get: {method: 'GET', isArray: false},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            }

        };

        return {

            subject : {

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.subject.policy.get({policy_id: policyId}).$promise.then(function(data) {

                       callback(utilService.transform(data, 'subject_assignments'));

                    });

                }
            },

            object : {

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.object.policy.get({policy_id: policyId}).$promise.then(function(data) {

                        callback(utilService.transform(data, 'object_assignments'));

                    });

                }
            },

            action : {

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.action.policy.get({policy_id: policyId}).$promise.then(function(data) {

                        callback(utilService.transform(data, 'action_assignments'));

                    });

                }
            }

        };

    }
})();