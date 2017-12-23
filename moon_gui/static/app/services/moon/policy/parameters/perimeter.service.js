/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('perimeterService', perimeterService);

    perimeterService.$inject = ['$resource', 'REST_URI', '$q', 'utilService'];

    function perimeterService($resource, REST_URI, $q, utilService) {

        var data =  {

            subject: {

                perimeter: $resource(REST_URI.PERIMETERS.subject + ':subject_id', {}, {
                    get: {method: 'GET', isArray: false},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'},
                    update: { method: 'PATCH' }
                }),

                policy: $resource(REST_URI.POLICIES + ':policy_id/subjects/:subject_id', {}, {
                    get: {method: 'GET'},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'},
                    update: { method: 'PATCH' }
                })

            },

            object: {

                perimeter:  $resource(REST_URI.PERIMETERS.object + ':object_id', {}, {
                    get: {method: 'GET', isArray: false},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'},
                    update: { method: 'PATCH' }
                }),

                policy: $resource(REST_URI.POLICIES + ':policy_id/objects/:object_id', {}, {
                    get: {method: 'GET', isArray: false},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'},
                    update: { method: 'PATCH' }
                })

            },

            action: {

                perimeter:  $resource(REST_URI.PERIMETERS.action + ':action_id', {}, {
                    get: {method: 'GET', isArray: false},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'},
                    update: { method: 'PATCH' }
                }),

                policy: $resource(REST_URI.POLICIES + ':policy_id/actions/:action_id', {}, {
                    get: {method: 'GET', isArray: false},
                    create: {method: 'POST'},
                    remove: {method: 'DELETE'},
                    update: { method: 'PATCH' }
                })

            }

        };

        return {

            subject : {

                findOne: function(subjectId, callback){

                    data.subject.perimeter.get({subject_id: subjectId}).$promise.then(function(data) {

                        callback(utilService.transformOne(data, 'subjects'));

                    });

                },

                findOneReturningPromise: function (subjectId){

                    return  data.subject.perimeter.get({subject_id: subjectId}).$promise;

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

                            return utilService.transformOne(resource, 'subjects');

                        });

                    });

                },

                unMapPerimeterFromPolicy: function(policyId, subjectId, callbackSuccess, callbackError ){

                    data.subject.policy.remove({policy_id: policyId, subject_id: subjectId}, {}, callbackSuccess, callbackError);

                },

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.subject.policy.get({policy_id: policyId}).$promise.then(function(data) {

                        callback(utilService.transform(data, 'subjects'));

                    });

                },

                findOneFromPolicyWithCallback: function(policyId, subjectId, callback){

                    data.subject.policy.get({policy_id: policyId, subject_id: subjectId}).$promise.then(function(data) {

                        callback(utilService.transformOne(data, 'subjects'));

                    });

                },

                findAll: function(){

                    return data.subject.perimeter.get().$promise.then(function(data) {

                        return utilService.transform(data, 'subjects');

                    });
                },

                findAllWithCallback: function(callback){

                    return data.subject.perimeter.get().$promise.then(function(data) {

                        callback(utilService.transform(data, 'subjects'));

                    });

                },

                delete: function (subject, callbackSuccess, callbackError ) {

                    data.subject.perimeter.remove({subject_id: subject.id}, subject, callbackSuccess, callbackError);

                },

                add: function (subject, callbackSuccess, callbackError ) {

                    data.subject.perimeter.create({}, subject, callbackSuccess, callbackError);

                },

                update: function(subject, callbackSuccess, callbackError){

                    data.subject.perimeter.update({subject_id: subject.id}, subject, callbackSuccess, callbackError);

                }
            },

            object : {

                findOne: function(objectId, callback){

                    data.object.perimeter.get({object_id: objectId}).$promise.then(function(data) {

                        callback(utilService.transformOne(data, 'objects'));

                    });

                },

                findOneReturningPromise: function(objectId){

                    return  data.object.perimeter.get({object_id: objectId}).$promise;

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

                            return utilService.transformOne(resource, 'objects');

                        });

                    });

                },

                unMapPerimeterFromPolicy: function(policyId, objectId, callbackSuccess, callbackError ){

                    data.object.policy.remove({policy_id: policyId, object_id: objectId}, {}, callbackSuccess, callbackError);

                },

                findSomeWithCallback: function(objectListId, callback){

                    var _self = this;

                    if(objectListId.length === 0){
                        callback([]);
                    }

                    var promises = _(objectListId).map( function(subjectId) {

                        return _self.findOneReturningPromise(subjectId);

                    });

                    $q.all(promises).then( function(result) {

                        callback( _(result).map( function(resource) {

                            return utilService.transformOne(resource, 'objects');

                        }));

                    });

                },

                findAll : function(){

                    return data.object.perimeter.get().$promise.then(function(data) {

                        return utilService.transform(data, 'objects');

                    });

                },

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.object.policy.get({policy_id: policyId}).$promise.then(function(data) {

                        callback(utilService.transform(data, 'objects'));

                    });

                },

                findOneFromPolicyWithCallback: function(policyId, objectId, callback){


                    data.object.policy.get({policy_id: policyId, object_id: objectId}).$promise.then(function(data) {

                        callback(utilService.transformOne(data, 'objects'));

                    });

                },

                findAllWithCallback: function(callback){

                    return data.object.perimeter.get().$promise.then(function(data) {

                        callback(utilService.transform(data, 'objects'));

                    });

                },

                delete: function (object, callbackSuccess, callbackError ) {

                    data.object.perimeter.remove({object_id: object.id}, object, callbackSuccess, callbackError);

                },

                add:function (object, callbackSuccess, callbackError ) {

                    data.object.perimeter.create({}, object, callbackSuccess, callbackError);

                },

                update: function(object, callbackSuccess, callbackError){

                    data.object.perimeter.update({object_id: object.id}, object, callbackSuccess, callbackError);

                }
            },

            action : {

                findOne: function(actionId, callback){

                    data.action.perimeter.get({actionId: actionId}).$promise.then(function(data) {

                        callback(utilService.transformOne(data, 'actions'));

                    });

                },

                findOneReturningPromise: function(actionId){

                    return data.action.perimeter.get({actionId: actionId}).$promise;

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

                            return utilService.transformOne(resource, 'actions');

                        });

                    });

                },

                unMapPerimeterFromPolicy: function(policyId, actionId, callbackSuccess, callbackError){

                    data.action.policy.remove({policy_id: policyId, action_id: actionId}, {}, callbackSuccess, callbackError);

                },

                findSomeWithCallback: function(actionListId, callback){

                    var _self = this;

                    if(actionListId.length === 0){
                        callback([]);
                    }

                    var promises = _(actionListId).map( function(subjectId) {

                        return _self.findOneReturningPromise(subjectId);

                    });

                    $q.all(promises).then( function(result) {

                        callback( _(result).map( function(resource) {

                            return utilService.transformOne(resource, 'actions');

                        }));

                    });

                },

                findAll : function(){

                    return data.action.perimeter.get().$promise.then(function(data) {

                        return utilService.transform(data, 'actions');

                    });

                },

                findAllFromPolicyWithCallback: function(policyId, callback){

                    data.action.policy.get({policy_id: policyId}).$promise.then(function(data) {

                        callback(utilService.transform(data, 'actions'));

                    });

                },

                findOneFromPolicyWithCallback: function(policyId, actionId, callback){

                    data.action.policy.get({policy_id: policyId, action_id: actionId}).$promise.then(function(data) {

                        callback(utilService.transformOne(data, 'actions'));

                    });

                },

                findAllWithCallback: function(callback){

                    return data.action.perimeter.get().$promise.then(function(data) {

                        callback(utilService.transform(data, 'actions'));

                    });

                },

                delete: function (action, callbackSuccess, callbackError ) {

                    data.action.perimeter.remove({action_id: action.id}, action, callbackSuccess, callbackError);

                },

                add:function (action, callbackSuccess, callbackError ) {

                    data.action.perimeter.create({}, action, callbackSuccess, callbackError);

                },

                update: function(action, callbackSuccess, callbackError){

                    data.action.perimeter.update({action_id: action.id}, action, callbackSuccess, callbackError);

                }
            }

        };

    }
})();