/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('metaRuleService', metaRuleService);

    metaRuleService.$inject = ['$resource', 'REST_URI', 'metaDataService', '$q', 'utilService'];

    function metaRuleService($resource, REST_URI, metaDataService, $q, utilService) {

        return {

            data: $resource(REST_URI.METARULES + ':metarule_id', {}, {
                query: {method: 'GET' },
                get: {method: 'GET', isArray: false},
                update: {method: 'PATCH'},
                create: { method: 'POST' },
                remove: { method: 'DELETE' }
            }),


            findAll: function () {

                return this.data.query().$promise.then(function (data) {

                    return utilService.transform(data, 'meta_rules');

                });

            },

            findAllWithCallback : function (callback) {

                this.data.query().$promise.then(function (data) {

                    callback(utilService.transform(data, 'meta_rules'));

                });

            },

            findSomeWithMetaData : function(metaRuleListId){

                var _self = this;

                if(metaRuleListId.length === 0){
                    return [];
                }

                var promises = _(metaRuleListId).map(function(objectId) {

                    return _self.findOneReturningPromise(objectId);

                });

                return $q.all(promises).then(function(result) {

                    return _(result).map(function(resource) {

                        var metaRule = utilService.transformOne(resource, 'meta_rules');

                        metaRule = _self.findMetaDataFromMetaRule(metaRule);

                        return metaRule;

                    });

                });


            },

            findSomeWithCallback : function(metaRuleListId, callback){

                var _self = this;

                if(metaRuleListId.length === 0){
                    return callback([]);
                }

                var promises = _(metaRuleListId).map(function(objectId) {

                    return _self.findOneReturningPromise(objectId);

                });

                return $q.all(promises).then(function(result) {

                    callback( _(result).map(function(resource) {

                        return utilService.transformOne(resource, 'meta_rules');

                    }));

                });


            },

            findOneReturningPromise: function(metaRuleId){

                return this.data.get({metarule_id: metaRuleId}).$promise;

            },

            findOne : function(metaRuleId){

                return this.data.get({metarule_id: metaRuleId}).$promise.then(function(data) {

                    return utilService.transformOne(data, 'meta_rules');

                });

            },

            findOneWithCallback: function(metaRuleId, callback){

                this.data.get({metarule_id: metaRuleId}).$promise.then(function(data) {

                    callback(utilService.transformOne(data, 'meta_rules'));

                });

            },

            findOneWithMetaData: function(metaRuleId){

                var _self = this;

                return this.data.get({metarule_id: metaRuleId}).$promise.then(function(data) {

                    var metaRule = utilService.transformOne(data, 'meta_rules');

                    metaRule = _self.findMetaDataFromMetaRule(metaRule);

                    return metaRule;

                });

            },

            findMetaDataFromMetaRule : function (metaRule){

                if(metaRule.subject_categories.length > 0){

                    metaDataService.subject.findSome(metaRule.subject_categories).then(function(categories){
                        metaRule.subject_categories_values = categories;
                    });

                }else{

                    metaRule.subject_categories_values = [];

                }

                if(metaRule.object_categories.length > 0){

                    metaDataService.object.findSome(metaRule.object_categories).then(function(categories){
                        metaRule.object_categories_values = categories;
                    });

                }else{

                    metaRule.object_categories_values = [];

                }

                if(metaRule.action_categories.length > 0){

                    metaDataService.action.findSome(metaRule.action_categories).then(function(categories){
                        metaRule.action_categories_values = categories;
                    });


                }else{

                    metaRule.action_categories_values = [];

                }

                return metaRule;
            },

            delete: function (metaRule, callbackSuccess, callbackError ) {

                this.data.remove({metarule_id: metaRule.id}, metaRule, callbackSuccess, callbackError);

            },

            update: function(metaRule, callbackSuccess, callbackError){

                delete metaRule.subject_categories_values;
                delete metaRule.object_categories_values;
                delete metaRule.action_categories_values;

                this.data.update({metarule_id: metaRule.id}, metaRule, callbackSuccess, callbackError);

            }
        };

    }
})();