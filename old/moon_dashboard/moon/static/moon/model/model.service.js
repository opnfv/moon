(function () {

    'use strict';

    angular
        .module('moon')
        .factory('moon.model.service', modelService);

    modelService.$inject = ['moon.util.service', '$resource', 'moon.URI', '$q'];

    function modelService(util, $resource, URI, $q) {
        var host = URI.API;
        var modelResource = $resource(host + '/models/' + ':id', {}, {
            get: { method: 'GET' },
            query: { method: 'GET' },
            create: { method: 'POST' },
            remove: { method: 'DELETE' },
            update: { method: 'PATCH' }
        });

        var metaRuleResource = $resource(host + '/meta_rules/' + ':id', {}, {
            query: { method: 'GET' },
            get: { method: 'GET' },
            update: { method: 'PATCH' },
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        });

        var subjectCategoryResource = $resource(host + '/subject_categories/' + ':id', {}, {
            query: { method: 'GET' },
            get: { method: 'GET' },
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        });

        var objectCategoryResource = $resource(host + '/object_categories/' + ':id', {}, {
            query: { method: 'GET' },
            get: { method: 'GET' },
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        });

        var actionCategoryResource = $resource(host + '/action_categories/' + ':id', {}, {
            query: { method: 'GET' },
            get: { method: 'GET' },
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        });

        var modelsMap = {};
        var metaRulesMap = {};
        var subjectCategoriesMap = {};
        var objectCategoriesMap = {};
        var actionCategoriesMap = {};
        var models = [];
        var metaRules = [];
        var orphanMetaRules = [];
        var subjectCategories = [];
        var objectCategories = [];
        var actionCategories = [];
        var orphanSubjectCategories = [];
        var orphanObjectCategories = [];
        var orphanActionCategories = [];

        var categoryMap = {
            'subject': {
                resource: subjectCategoryResource,
                map: subjectCategoriesMap,
                list: subjectCategories,
                listName: 'subject_categories'
            },
            'object': {
                resource: objectCategoryResource,
                map: objectCategoriesMap,
                list: objectCategories,
                listName: 'object_categories'
            },
            'action': {
                resource: actionCategoryResource,
                map: actionCategoriesMap,
                list: actionCategories,
                listName: 'action_categories'
            }
        }

        function loadModels() {
            var queries = {
                subjectCategories: subjectCategoryResource.query().$promise,
                objectCategories: objectCategoryResource.query().$promise,
                actionCategories: actionCategoryResource.query().$promise,
                metaRules: metaRuleResource.query().$promise,
                models: modelResource.query().$promise,
            }

            var result = $q.all(queries).then(function (result) {
                createModels(result.models, result.metaRules, result.subjectCategories, result.objectCategories, result.actionCategories)
                console.log('moon', 'models initialized')
            })

            return result;
        }

        function createModels(modelsData, metarulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData) {
            util.cleanObject(modelsMap);
            util.cleanObject(metaRulesMap);
            util.cleanObject(subjectCategoriesMap);
            util.cleanObject(objectCategoriesMap);
            util.cleanObject(actionCategoriesMap);
            models.splice(0, models.length);
            metaRules.splice(0, metaRules.length);
            subjectCategories.splice(0, subjectCategories.length);
            objectCategories.splice(0, objectCategories.length);
            actionCategories.splice(0, actionCategories.length);
            if (subjectCategoriesData.subject_categories) createCategoryInternal('subject', subjectCategoriesData.subject_categories);
            if (objectCategoriesData.object_categories) createCategoryInternal('object', objectCategoriesData.object_categories);
            if (actionCategoriesData.action_categories) createCategoryInternal('action', actionCategoriesData.action_categories);
            if (metarulesData.meta_rules) createMetaRuleInternal(metarulesData.meta_rules);
            if (modelsData.models) createModelInternal(modelsData.models);
            updateOrphan();
        }

        function mapModel(model) {
            util.mapIdToItem(model.meta_rules, metaRulesMap);
        }

        function createModelInternal(data) {
            return util.createInternal(data, models, modelsMap, mapModel);
        }

        function updateModelInternal(data) {
            return util.updateInternal(data, modelsMap, mapModel);
        }

        function removeModelInternal(id) {
            return util.removeInternal(id, models, modelsMap);
        }

        function mapMetaRule(metaRule) {
            util.mapIdToItem(metaRule.subject_categories, subjectCategoriesMap);
            util.mapIdToItem(metaRule.object_categories, objectCategoriesMap);
            util.mapIdToItem(metaRule.action_categories, actionCategoriesMap);
        }

        function createMetaRuleInternal(data) {
            return util.createInternal(data, metaRules, metaRulesMap, mapMetaRule);
        }

        function updateMetaRuleInternal(data) {
            return util.updateInternal(data, metaRulesMap, mapMetaRule);
        }

        function removeMetaRuleInternal(id) {
            return util.removeInternal(id, metaRules, metaRulesMap);
        }

        function createCategoryInternal(type, data) {
            var categoryValue = categoryMap[type];
            return util.createInternal(data, categoryValue.list, categoryValue.map)
        }

        function removeCategoryInternal(type, id) {
            var categoryValue = categoryMap[type];
            return util.removeInternal(id, categoryValue.list, categoryValue.map);
        }

        function updateOrphan() {
            updateOrphanInternal(metaRules, orphanMetaRules, models, "meta_rules");
            updateOrphanInternal(subjectCategories, orphanSubjectCategories, metaRules, "subject_categories");
            updateOrphanInternal(objectCategories, orphanObjectCategories, metaRules, "object_categories");
            updateOrphanInternal(actionCategories, orphanActionCategories, metaRules, "action_categories");
        }

        function updateOrphanInternal(list, orphanList, parentList, childListName) {
            orphanList.splice(0, orphanList.length);
            util.pushAll(orphanList, list);
            for (var i = 0; i < parentList.length; i++) {
                var parent = parentList[i];
                var children = parent[childListName];
                if (children) {
                    for (var j = 0; j < children.length; j++) {
                        var child = children[j];
                        var notOrphanIndex = util.indexOf(orphanList, "id", child.id);
                        if (notOrphanIndex >= 0) {
                            orphanList.splice(notOrphanIndex, 1);
                        }
                    }
                }
            }
        }


        return {
            initialize: loadModels,
            createModels: createModels,
            models: models,
            metaRules: metaRules,
            orphanMetaRules: orphanMetaRules,
            orphanSubjectCategories: orphanSubjectCategories,
            orphanObjectCategories: orphanObjectCategories,
            orphanActionCategories: orphanActionCategories,
            subjectCategories: subjectCategories,
            objectCategories: objectCategories,
            actionCategories: actionCategories,
            getModel: function getModel(id) {
                return modelsMap[id];
            },
            createModel: function createModel(model) {
                model.meta_rules = [];
                modelResource.create(null, model, success, util.displayErrorFunction('Unable to create model'));

                function success(data) {
                    createModelInternal(data.models);
                    util.displaySuccess('Model created');
                }
            },
            removeModel: function removeModel(model) {
                modelResource.remove({ id: model.id }, null, success, util.displayErrorFunction('Unable to remove model'));

                function success(data) {
                    removeModelInternal(model.id);
                    updateOrphan();
                    util.displaySuccess('Model removed');
                }
            },
            updateModel: function updateModel(model) {
                util.mapItemToId(model.meta_rules)
                modelResource.update({ id: model.id }, model, success, util.displayErrorFunction('Unable to update model'));

                function success(data) {
                    updateModelInternal(data.models)
                    updateOrphan();
                    util.displaySuccess('Model updated');
                }
            },
            getMetaRule: function getMetaRule(id) {
                return metaRulesMap[id];
            },
            createMetaRule: function createMetaRule(metaRule) {
                metaRule.subject_categories = [];
                metaRule.object_categories = [];
                metaRule.action_categories = [];

                return metaRuleResource.create(null, metaRule).$promise.then(function (data) {
                    util.displaySuccess('Meta Rule created');
                    return createMetaRuleInternal(data.meta_rules)[0];
                }, util.displayErrorFunction('Unable to create meta rule'))
            },
            updateMetaRule: function updateMetaRule(metaRule) {
                util.mapItemToId(metaRule.subject_categories);
                util.mapItemToId(metaRule.object_categories);
                util.mapItemToId(metaRule.action_categories);
                metaRuleResource.update({ id: metaRule.id }, metaRule, success, util.displayErrorFunction('Unable to update meta rule'));

                function success(data) {
                    updateMetaRuleInternal(data.meta_rules);
                    updateOrphan();
                    util.displaySuccess('Meta Rule updated');
                }
            },
            removeMetaRule: function removeMetaRule(metaRule) {
                metaRuleResource.remove({ id: metaRule.id }, null, success, util.displayErrorFunction('Unable to remove meta rule'));

                function success(data) {
                    removeMetaRuleInternal(metaRule.id);
                    updateOrphan();
                    util.displaySuccess('Meta Rule removed');
                }
            },
            getCategory: function getCategory(type, id) {
                return categoryMap[type].map[id];
            },
            createCategory: function createCategory(type, category) {
                var categoryValue = categoryMap[type];
                return categoryValue.resource.create({}, category).$promise.then(function (data) {
                    util.displaySuccess('Category created');
                    return createCategoryInternal(type, data[categoryValue.listName])[0];
                }, util.displayErrorFunction('Unable to create category'))
            },
            removeCategory: function removeCategory(type, category) {
                var categoryValue = categoryMap[type];
                categoryValue.resource.remove({ id: category.id }, null, success, util.displayErrorFunction('Unable to remove category'));

                function success(data) {
                    removeCategoryInternal(type, category.id);
                    updateOrphan();
                    util.displaySuccess('Category removed');
                }
            },
        }
    }
})();