/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('assignmentsService', assignmentsService);

    assignmentsService.$inject = ['$resource', 'REST_URI', 'utilService'];

    function assignmentsService($resource, REST_URI, utilService) {

        var data =  {

            subject: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/subject_assignments/:perimeter_id/:category_id/:data_id', {}, {
                    get: {method: 'GET'},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },


            object: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/object_assignments/:perimeter_id/:category_id/:data_id', {}, {
                    get: {method: 'GET'},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },

            action: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/action_assignments/:perimeter_id/:category_id/:data_id', {}, {
                    get: {method: 'GET'},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            }

        };

        return {

            subject : {

                delete: function (policyId, perimeterId, categoryId, dataId, callbackSuccess, callbackError ) {

                    data.subject.policy.remove({policy_id: policyId, perimeter_id: perimeterId, category_id: categoryId, data_id: dataId}, {}, callbackSuccess, callbackError);

                },

                add:function (subject, policyId, callbackSuccess, callbackError ) {

                    data.subject.policy.create({policy_id: policyId}, subject, callbackSuccess, callbackError);

                },

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.subject.policy.get({policy_id: policyId}).$promise.then(function(data) {

                       callback(utilService.transform(data, 'subject_assignments'));

                    });

                }
            },

            object : {


                delete: function (policyId, perimeterId, categoryId, dataId, callbackSuccess, callbackError ) {

                    data.object.policy.remove({policy_id: policyId, perimeter_id: perimeterId, category_id: categoryId, data_id: dataId}, {}, callbackSuccess, callbackError);

                },

                add:function (object, policyId, callbackSuccess, callbackError ) {

                    data.object.policy.create({policy_id: policyId}, object, callbackSuccess, callbackError);

                },

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.object.policy.get({policy_id: policyId}).$promise.then(function(data) {

                        callback(utilService.transform(data, 'object_assignments'));

                    });

                }
            },

            action : {

                delete: function (policyId, perimeterId, categoryId, dataId, callbackSuccess, callbackError ) {

                    data.action.policy.remove({policy_id: policyId, perimeter_id: perimeterId, category_id: categoryId, data_id: dataId}, {}, callbackSuccess, callbackError);

                },

                add:function (action, policyId, callbackSuccess, callbackError ) {

                    data.action.policy.create({policy_id: policyId}, action, callbackSuccess, callbackError);

                },

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.action.policy.get({policy_id: policyId}).$promise.then(function(data) {

                        callback(utilService.transform(data, 'action_assignments'));

                    });

                }
            }

        };

    }
})();