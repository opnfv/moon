/**
 * @author Samy Abdallah
 */

(function() {

    'use strict';

    angular
        .module('moon')
        .factory('modelService', modelService);

    modelService.$inject = ['$resource', 'REST_URI', 'metaRuleService', 'utilService'];

    function modelService($resource, REST_URI, metaRuleService, utilService) {

        return {

            data: $resource(REST_URI.MODELS + ':model_id', {}, {
                get: {method: 'GET'},
                query: {method: 'GET'},
                create: {method: 'POST'},
                remove: {method: 'DELETE'},
                update: {method: 'PATCH'}
            }),

            findAll: function () {

                return this.data.query().$promise.then(function (data) {

                    return utilService.transform(data, 'models');

                });

            },


            findAllWithCallBack : function (callback){

                return this.data.query().$promise.then(function (data) {

                    callback( utilService.transform(data, 'models'));

                });

            },

            findOneWithCallback : function(modelId, callback){

                return this.data.get({model_id: modelId}).$promise.then(function (data) {

                    callback(utilService.transformOne(data, 'models'));

                });

            },

            findOneWithMetaRules: function (modelId) {

                return this.data.get({model_id: modelId}).$promise.then(function (data) {

                    var res = utilService.transformOne(data, 'models');

                    if(res.meta_rules.length > 0){

                        metaRuleService.findSomeWithMetaData(res.meta_rules).then(function(metaRules){

                            res.meta_rules_values  = metaRules;
                            res.id = modelId;

                            return res;

                        });

                    }else{

                        res.meta_rules_values = [];
                        res.id = modelId;

                    }

                    return res;

                });

            },

            delete: function (model, callbackSuccess, callbackError ) {

                delete model.meta_rules_values;

                this.data.remove({model_id: model.id}, model, callbackSuccess, callbackError);

            },

            update: function (model, callbackSuccess, callbackError) {

                delete model.meta_rules_values;
                this.data.update({model_id: model.id}, model, callbackSuccess, callbackError);

            }

        }
    }
})();