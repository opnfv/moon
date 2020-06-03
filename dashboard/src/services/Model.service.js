import Vue from 'vue'
import util from './Util.service.js'
import config from '../config.js'

var host = config.host;

var modelResource;
var metaRuleResource;
var subjectCategoryResource;
var objectCategoryResource;
var actionCategoryResource;
var attributesResource;

var modelsMap = {};
var metaRulesMap = {};
var subjectCategoriesMap = {};
var objectCategoriesMap = {};
var actionCategoriesMap = {};
var attributesMap = {};
var models = [];
var metaRules = [];
var orphanMetaRules = [];
var subjectCategories = [];
var objectCategories = [];
var actionCategories = [];
var attributes = [];
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
    },
    'attribute' : {
        resource: attributesResource,
        map: attributesMap,
        list: attributes,
        listName: 'attributes'
    }
}


function loadModels() {
    modelResource = Vue.resource(host + '/models{/id}', {}, {patch: {method: 'PATCH'}});
    metaRuleResource = Vue.resource(host + '/meta_rules{/id}', {}, {patch: {method: 'PATCH'}});
    categoryMap['subject'].resource = subjectCategoryResource = Vue.resource(host + '/subject_categories{/id}');
    categoryMap['object'].resource = objectCategoryResource = Vue.resource(host + '/object_categories{/id}');
    categoryMap['action'].resource = actionCategoryResource = Vue.resource(host + '/action_categories{/id}');
    categoryMap['attribute'].resource = attributesResource = Vue.resource(host + '/attributes{/id}');
    var queries = [
        modelResource.query(),
        metaRuleResource.query(),
        subjectCategoryResource.query(),
        objectCategoryResource.query(),
        actionCategoryResource.query(),
        attributesResource.query()
    ]

    var result = Promise.all(queries).then(function (result) {
        createModels(result[0].body, result[1].body, result[2].body, result[3].body, result[4].body, result[5].body)
    })

    return result;
}

function createModels(modelsData, metarulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData, attributesData) {
    util.cleanObject(modelsMap);
    util.cleanObject(metaRulesMap);
    util.cleanObject(subjectCategoriesMap);
    util.cleanObject(objectCategoriesMap);
    util.cleanObject(actionCategoriesMap);
    util.cleanObject(attributesMap);
    models.splice(0, models.length);
    metaRules.splice(0, metaRules.length);
    subjectCategories.splice(0, subjectCategories.length);
    objectCategories.splice(0, objectCategories.length);
    actionCategories.splice(0, actionCategories.length);
    attributes.splice(0, attributes.length);
    if (subjectCategoriesData.subject_categories) createCategoryInternal('subject', subjectCategoriesData.subject_categories);
    if (objectCategoriesData.object_categories) createCategoryInternal('object', objectCategoriesData.object_categories);
    if (actionCategoriesData.action_categories) createCategoryInternal('action', actionCategoriesData.action_categories);
    if (attributesData.attributes) createCategoryInternal('attribute', attributesData.attributes);
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

function mapIdToItemWithAttributes(categories, categoriesMap, attributes, attributesMap) {
    let categoriesToRemove = []
    if (categories) {
        var index2 = 0;
        for (var index = 0; index < categories.length; index++) {
            var id = categories[index];
            if (categoriesMap[id])
                categories[index] = categoriesMap[id];
            else {
                if(id.includes('attributes:')){
                    const newId = id.split(':')[1];
                    if (attributesMap[newId]){
                        attributes[index2++] = attributesMap[newId];
                    }
                    categoriesToRemove.push(index)
                }
            }
        }
        for (let i = categoriesToRemove.length - 1; i >= 0; i--){
            categories.splice(categoriesToRemove[i], 1);
        }
    }
}

function cleanCategoryByRemovingAttributes(categories, attributesMap){
    let categoriesToRemove = []
    if (categories) {
        for (let index = 0; index < categories.length; index++){
            var category = categories[index];
            if (attributesMap[category.name]){
                categoriesToRemove.push(index)
            }
        }
        for (let i = categoriesToRemove.length - 1; i >= 0; i--){
            categories.splice(categoriesToRemove[i], 1);
        }
    }
}

function mapMetaRule(metaRule) {
    metaRule.subjectAttributes = [];
    metaRule.objectAttributes = [];
    metaRule.actionAttributes = [];
    mapIdToItemWithAttributes(metaRule.subject_categories, subjectCategoriesMap, metaRule.subjectAttributes, attributesMap);
    mapIdToItemWithAttributes(metaRule.object_categories, objectCategoriesMap, metaRule.objectAttributes,attributesMap);
    mapIdToItemWithAttributes(metaRule.action_categories, actionCategoriesMap, metaRule.actionAttributes, attributesMap);
    cleanCategoryByRemovingAttributes(subjectCategories, attributesMap);
    cleanCategoryByRemovingAttributes(objectCategories, attributesMap);
    cleanCategoryByRemovingAttributes(actionCategories, attributesMap);
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
                if (child){
                    var notOrphanIndex = util.indexOf(orphanList, "id", child.id);
                    if (notOrphanIndex >= 0) {
                        orphanList.splice(notOrphanIndex, 1);
                    }
                    else{
                        for (var k = 0; k < attributes.length; k++){
                            const attr = attributes[k];
                            notOrphanIndex = util.indexOf(orphanList, "name", attr.id);
                            if (notOrphanIndex >= 0) {
                                orphanList.splice(notOrphanIndex, 1);
                            }
                        }
                    }

                }
            }
        }
    }
}

function getAttributesForModelId(modelId) {
    let model = modelsMap[modelId];
    let attrs = []

    for (let i = 0; i < model.meta_rules.length; i++){
        let metaRule = model.meta_rules[i];
        let j;
        for (j = 0; j < metaRule.subjectAttributes.length; j++){
            attrs.push(metaRule.subjectAttributes[j])
        }
        for (j = 0; j < metaRule.objectAttributes.length; j++){
            attrs.push(metaRule.objectAttributes[j])
        }
        for (j = 0; j < metaRule.actionAttributes.length; j++){
            attrs.push(metaRule.actionAttributes[j])
        }
    }
    return attrs;
}

export default {
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
    getAttributesForModelId: getAttributesForModelId,
    createModel: function createModel(model) {
        model.meta_rules = [];
        modelResource.save(null, model).then(success, util.displayErrorFunction('Unable to create model'));

        function success(data) {
            createModelInternal(data.body.models);
            util.displaySuccess('Model created');
        }
    },
    removeModel: function removeModel(model) {
        modelResource.remove({ id: model.id }).then(success, util.displayErrorFunction('Unable to remove model'));

        function success() {
            removeModelInternal(model.id);
            updateOrphan();
            util.displaySuccess('Model removed');
        }
    },
    updateModel: function updateModel(model) {
        util.mapItemToId(model.meta_rules)
        modelResource.patch({ id: model.id }, model).then(success, util.displayErrorFunction('Unable to update model'));

        function success(data) {
            updateModelInternal(data.body.models);
            
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

        return metaRuleResource.save(null, metaRule).then(function (data) {
            util.displaySuccess('Meta Rule created');
            return createMetaRuleInternal(data.body.meta_rules)[0];
        }, util.displayErrorFunction('Unable to create meta rule'))
    },
    updateMetaRule: function updateMetaRule(metaRule) {
        util.mapItemToId(metaRule.subject_categories);
        util.mapItemToId(metaRule.object_categories);
        util.mapItemToId(metaRule.action_categories);
        metaRuleResource.patch({ id: metaRule.id }, metaRule).then(success, util.displayErrorFunction('Unable to update meta rule'));

        function success(data) {
            updateMetaRuleInternal(data.body.meta_rules);
            updateOrphan();
            util.displaySuccess('Meta Rule updated');
        }
    },
    removeMetaRule: function removeMetaRule(metaRule) {
        metaRuleResource.remove({ id: metaRule.id }).then(success, util.displayErrorFunction('Unable to remove meta rule'));

        function success() {
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
        return categoryValue.resource.save(null, category).then(function (data) {
            util.displaySuccess('Category created');
            return createCategoryInternal(type, data.body[categoryValue.listName])[0];
        }, util.displayErrorFunction('Unable to create category'))
    },
    removeCategory: function removeCategory(type, category) {
        var categoryValue = categoryMap[type];
        categoryValue.resource.remove({ id: category.id }).then(success, util.displayErrorFunction('Unable to remove category'));

        function success() {
            removeCategoryInternal(type, category.id);
            updateOrphan();
            util.displaySuccess('Category removed');
        }
    },
}