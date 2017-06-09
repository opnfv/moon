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

                policy: $resource(REST_URI.POLICIES + ':policy_id/subject_data/:subject_id/:category_id/:data_id', {}, {
                    get: {method: 'GET'},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },

            object: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/object_data/:object_id/:category_id/:data_id', {}, {
                    get: {method: 'GET', isArray: false},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'}
                })

            },

            action: {

                policy: $resource(REST_URI.POLICIES + ':policy_id/action_data/:action_id/:category_id/:data_id', {}, {
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

                findAllFromCategoriesWithCallback: function(policyId, categoryId, callback){

                    data.subject.policy.get({policy_id: policyId, category_id: categoryId}).$promise.then(function(data) {

                        if(data['subject_data'][0]) {

                            callback(utilService.transform(data['subject_data'][0], 'data'));

                        }else{

                            callback([])

                        }

                    });

                },

                delete: function (subject, policyId, categoryId, callbackSuccess, callbackError ) {

                    data.subject.policy.remove({policy_id: policyId, category_id: categoryId, data_id: subject.id}, subject, callbackSuccess, callbackError);

                },

                add: function (subject, policyId, categoryId, callbackSuccess, callbackError ) {

                    data.subject.policy.create({policy_id: policyId, category_id: categoryId}, subject, callbackSuccess, callbackError);

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

                findAllFromCategoriesWithCallback: function(policyId, categoryId, callback){

                    data.object.policy.get({policy_id: policyId, category_id: categoryId}).$promise.then(function(data) {

                        if(data['object_data'][0]) {

                            callback(utilService.transform(data['object_data'][0], 'data'));

                        }else{

                            callback([])

                        }

                    });

                },

                delete: function (object, policyId, categoryId, callbackSuccess, callbackError ) {

                    data.object.policy.remove({policy_id: policyId, category_id: categoryId, data_id: object.id}, object, callbackSuccess, callbackError);

                },

                add:function (object, policyId, categoryId, callbackSuccess, callbackError ) {

                    data.object.policy.create({policy_id: policyId, category_id: categoryId}, object, callbackSuccess, callbackError);

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

                findAllFromCategoriesWithCallback: function(policyId, categoryId, callback){

                    data.action.policy.get({policy_id: policyId, category_id: categoryId}).$promise.then(function(data) {

                        if(data['action_data'][0]) {

                            callback(utilService.transform(data['action_data'][0], 'data'));

                        }else{

                            callback([])

                        }

                    });

                },

                delete: function (action, policyId, categoryId, callbackSuccess, callbackError ) {

                    data.action.policy.remove({policy_id: policyId, category_id: categoryId, data_id: action.id}, action, callbackSuccess, callbackError);

                },

                add:function (action, policyId, categoryId, callbackSuccess, callbackError ) {

                    data.action.policy.create({policy_id: policyId, category_id: categoryId}, action, callbackSuccess, callbackError);

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