/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('metaDataService', metaDataService);

    metaDataService.$inject = ['$resource', 'REST_URI', '$q', 'utilService'];

    function metaDataService($resource, REST_URI, $q, utilService) {

        var data =  {

            subject: $resource(REST_URI.METADATA.subject + ':subject_id', {}, {
                get: {method: 'GET', isArray: false},
                create: {method: 'POST'},
                remove: {method: 'DELETE'}
            }),


            object:  $resource(REST_URI.METADATA.object + ':object_id', {}, {
                get: {method: 'GET', isArray: false},
                create: {method: 'POST'},
                remove: {method: 'DELETE'}
            }),

            action: $resource(REST_URI.METADATA.action + ':action_id', {}, {
                get: {method: 'GET', isArray: false},
                create: {method: 'POST'},
                remove: {method: 'DELETE'}
            })

        };

        return {

            subject : {

                findOne: function(subjectId, callback){

                    data.subject.get({subject_id: subjectId}).$promise.then(function(data) {

                        callback(utilService.transformOne(data, 'subject_categories'));

                    });

                },

                findOneReturningPromise: function (subjectId){

                    return  data.subject.get({subject_id: subjectId}).$promise;

                },

                findSome: function(subjectListId) {

                    var _self = this;

                    if(subjectListId.length === 0){
                        return [];
                    }

                    var promises = _(subjectListId).map( function(subjectId) {

                        return _self.findOneReturningPromise(subjectId);

                    });

                    return $q.all(promises).then( function(result) {

                        return _(result).map( function(resource) {

                            return utilService.transformOne(resource, 'subject_categories');

                        });

                    });

                },

                findSomeWithCallback: function(subjectListId, callback){

                    var _self = this;

                    if(subjectListId.length === 0){
                        callback([]);
                    }

                    var promises = _(subjectListId).map( function(subjectId) {

                        return _self.findOneReturningPromise(subjectId);

                    });

                    $q.all(promises).then( function(result) {

                        callback( _(result).map( function(resource) {

                            return utilService.transformOne(resource, 'subject_categories');

                        }));

                    });

                },

                findAll: function(){

                    return data.subject.get().$promise.then(function(data) {

                        return utilService.transform(data, 'subject_categories');

                    });
                },

                findAllWithCallback: function(callback){

                    return data.subject.get().$promise.then(function(data) {

                        callback(utilService.transform(data, 'subject_categories'));

                    });

                },
                
                delete: function (subject, callbackSuccess, callbackError ) {

                    data.subject.remove({subject_id: subject.id}, subject, callbackSuccess, callbackError);

                },

                add: function (subject, callbackSuccess, callbackError ) {

                    data.subject.create({}, subject, callbackSuccess, callbackError);

                }
            },

            object : {

                findOne: function(objectId, callback){

                    data.object.get({object_id: objectId}).$promise.then(function(data) {

                        callback(utilService.transformOne(data, 'object_categories'));

                    })

                },

                findOneReturningPromise: function(objectId){

                    return  data.object.get({object_id: objectId}).$promise;

                },

                findSome: function(objectListId) {


                    var _self = this;

                    if(objectListId.length === 0){
                        return [];
                    }

                    var promises = _(objectListId).map( function(objectId) {

                        return _self.findOneReturningPromise(objectId);

                    });

                    return $q.all(promises).then( function(result) {

                        return _(result).map( function(resource) {

                            return utilService.transformOne(resource, 'object_categories');

                        });

                    });

                },

                findSomeWithCallback: function(objectListId, callback){

                    var _self = this;

                    if(objectListId.length === 0){
                        callback([]);
                    }

                    var promises = _(objectListId).map( function(objectId) {

                        return _self.findOneReturningPromise(objectId);

                    });

                    $q.all(promises).then( function(result) {

                        callback( _(result).map( function(resource) {

                            return utilService.transformOne(resource, 'object_categories');

                        }));

                    });

                },

                findAll : function(){

                    return data.object.get().$promise.then(function(data) {

                        return utilService.transform(data, 'object_categories');

                    });

                },

                findAllWithCallback: function(callback){

                    return data.object.get().$promise.then(function(data) {

                        callback(utilService.transform(data, 'object_categories'));

                    });

                },

                delete: function (object, callbackSuccess, callbackError ) {

                    data.object.remove({object_id: object.id}, object, callbackSuccess, callbackError);

                },

                add:function (object, callbackSuccess, callbackError ) {

                    data.object.create({}, object, callbackSuccess, callbackError);

                }
            },

            action : {

                findOne: function(actionId, callback){

                    data.action.get({action_id: actionId}).$promise.then(function(data) {

                        callback(utilService.transformOne(data, 'action_categories'));

                    })

                },

                findOneReturningPromise: function(actionId){

                    return data.action.get({action_id: actionId}).$promise;

                },

                findSome: function(actionListId) {

                    var _self = this;

                    if(actionListId.length === 0){
                        return [];
                    }

                    var promises = _(actionListId).map( function(actionId) {

                        return _self.findOneReturningPromise(actionId);

                    });

                    return $q.all(promises).then( function(result) {

                        return _(result).map( function(resource) {

                            return utilService.transformOne(resource, 'action_categories');

                        });

                    });

                },

                findSomeWithCallback: function(actionListId, callback){

                    var _self = this;

                    if(actionListId.length === 0){
                        callback([]);
                    }

                    var promises = _(actionListId).map( function(actionId) {

                        return _self.findOneReturningPromise(actionId);

                    });

                    $q.all(promises).then( function(result) {

                        callback( _(result).map( function(resource) {

                            return utilService.transformOne(resource, 'action_categories');

                        }));

                    });

                },

                findAll : function(){

                    return data.action.get().$promise.then(function(data) {

                        return utilService.transform(data, 'action_categories');

                    });

                },

                findAllWithCallback: function(callback){

                    return data.action.get().$promise.then(function(data) {

                        callback(utilService.transform(data, 'action_categories'));

                    });

                },

                delete: function (action, callbackSuccess, callbackError ) {

                    data.action.remove({action_id: action.id}, action, callbackSuccess, callbackError);

                },

                add:function (action, callbackSuccess, callbackError ) {

                    data.action.create({}, action, callbackSuccess, callbackError);

                }
            }

        };

    }
})();