/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('dataService', dataService);

    dataService.$inject = ['$resource', 'REST_URI', 'utilService'];

    function dataService($resource, REST_URI, utilService) {

        var data =  {

            subject: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/subject_data/:subject_id/:data_id', {}, {
                    get: {method: 'GET'},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },

            object: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/object_data/:object_id/:data_id', {}, {
                    get: {method: 'GET', isArray: false},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },

            action: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/action_data/:action_id/:data_id', {}, {
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

                        callback(utilService.transform(data['subject_data'][0], 'data'));

                    });

                },

                delete: function (subject, callbackSuccess, callbackError ) {

                    data.subject.perimeter.remove({subject_id: subject.id}, subject, callbackSuccess, callbackError);

                },

                add: function (subject, callbackSuccess, callbackError ) {

                    data.subject.perimeter.create({}, subject, callbackSuccess, callbackError);

                },

                data: {

                    findOne: function(policyId, subjectId, dataId, callback){

                        data.subject.policy.get({policy_id: policyId, subject_id: subjectId, data_id : dataId}).$promise.then(function(data) {

                            if(data['subject_data'][0]){

                                callback(utilService.transformOne(data['subject_data'][0], 'data'));

                            }else{

                                callback({ });

                            }

                        });

                    }
                }
            },

            object : {

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.object.policy.get({policy_id: policyId}).$promise.then(function(data) {

                        callback(utilService.transform(data['object_data'][0], 'data'));

                    });

                },

                delete: function (object, callbackSuccess, callbackError ) {

                    data.object.perimeter.remove({object_id: object.id}, object, callbackSuccess, callbackError);

                },

                add:function (object, callbackSuccess, callbackError ) {

                    data.object.perimeter.create({}, object, callbackSuccess, callbackError);

                },

                data: {

                    findOne: function(policyId, objectId, dataId, callback){

                        data.object.policy.get({policy_id: policyId, object_id: objectId, data_id : dataId}).$promise.then(function(data) {


                            if(data['object_data'][0]){

                                callback(utilService.transformOne(data['object_data'][0], 'data'));

                            }else{

                                callback({ });

                            }

                        });

                    }
                }
            },

            action : {

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.action.policy.get({policy_id: policyId}).$promise.then(function(data) {

                        callback(utilService.transform(data['action_data'][0], 'data'));

                    });

                },

                delete: function (action, callbackSuccess, callbackError ) {

                    data.action.perimeter.remove({action_id: action.id}, action, callbackSuccess, callbackError);

                },

                add:function (action, callbackSuccess, callbackError ) {

                    data.action.perimeter.create({}, action, callbackSuccess, callbackError);

                },


                data: {

                    findOne: function(policyId, actionId, dataId, callback){

                        data.action.policy.get({policy_id: policyId, action_id: actionId, data_id : dataId}).$promise.then(function(data) {

                            if(data['action_data'][0]){

                                callback(utilService.transformOne(data['action_data'][0], 'data'));

                            }else{

                                callback({ });

                            }

                        });

                    }
                }
            }

        };

    }
})();