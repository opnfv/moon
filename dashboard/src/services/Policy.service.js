import Vue from 'vue'
import util from './Util.service.js'
import ModelService from './Model.service.js'
import AttributeService from './Attribute.service'
import config from '../config.js'

var host = config.host;

var policyResource;
var policyRulesResource;

var categoryMap = {
    'subject': {
        arrayName: "subjectData",
        mapName: "subjectDataMap",
        responseName: "subject_data",
        perimeterResponseName: "subjects",
        assignmentResponseName: "subject_assignments",
        unusedArrayName: "unusedSubjectData",
    },
    'object': {
        arrayName: "objectData",
        mapName: "objectDataMap",
        responseName: "object_data",
        perimeterResponseName: "objects",
        assignmentResponseName: "object_assignments",
        unusedArrayName: "unusedObjectData",
    },
    'action': {
        arrayName: "actionData",
        mapName: "actionDataMap",
        responseName: "action_data",
        perimeterResponseName: "actions",
        assignmentResponseName: "action_assignments",
        unusedArrayName: "unusedActionData",
    }
}

var policiesMap = {};
var policies = [];

function loadPolicies() {
    policyResource = Vue.resource(host + '/policies{/id}', {}, {patch: {method: 'PATCH'}});
    categoryMap['subject'].policyPerimeterResource = Vue.resource(host + '/policies{/policy_id}/subjects{/perimeter_id}', {});
    categoryMap['object'].policyPerimeterResource = Vue.resource(host + '/policies{/policy_id}/objects{/perimeter_id}', {}, );
    categoryMap['action'].policyPerimeterResource = Vue.resource(host + '/policies{/policy_id}/actions{/perimeter_id}', {}, );
    categoryMap['subject'].perimeterResource = Vue.resource(host + '/subjects{/perimeter_id}', {}, {patch: {method: 'PATCH'}});
    categoryMap['object'].perimeterResource = Vue.resource(host + '/objects{/perimeter_id}', {}, {patch: {method: 'PATCH'}});
    categoryMap['action'].perimeterResource = Vue.resource(host + '/actions{/perimeter_id}', {}, {patch: {method: 'PATCH'}});
    categoryMap['subject'].assignmentResource = Vue.resource(host + '/policies{/policy_id}/subject_assignments{/perimeter_id}{/category_id}{/data_id}', {}, );
    categoryMap['object'].assignmentResource = Vue.resource(host + '/policies{/policy_id}/object_assignments{/perimeter_id}{/category_id}{/data_id}', {}, );
    categoryMap['action'].assignmentResource = Vue.resource(host + '/policies{/policy_id}/action_assignments{/perimeter_id}{/category_id}{/data_id}', {}, );
    var queries = [
        policyResource.query(),
        ModelService.initialize(),
        AttributeService.initialize()
    ]

    Promise.all(queries).then(function (result) {
        createPolicies(result[0].body);
    })
}

function createPolicies(policiesData) {
    policies.splice(0, policies.length);
    util.cleanObject(policiesMap);
    createPolicyInternal(policiesData.policies);
}

function mapPolicy(policy) {
    policy.rulesPopulated = false;
    policy.rules = [];
    policy.subjectData = [];
    policy.objectData = [];
    policy.actionData = [];
    policy.unusedSubjectData = [];
    policy.unusedObjectData = [];
    policy.unusedActionData = [];
    policy.attributes = [];
    if (policy.model_id) {
        policy.model = ModelService.getModel(policy.model_id);
        policy.attributes = ModelService.getAttributesForModelId(policy.model_id);
    }
}

function createPolicyInternal(data) {
    return util.createInternal(data, policies, policiesMap, mapPolicy);
}

function removePolicyInternal(id) {
    return util.removeInternal(id, policies, policiesMap);
}

function updatePolicyInternal(data) {
    return util.updateInternal(data, policiesMap, mapPolicy);
}

function removeRuleInternal(policy, rule) {
    policy.rules.splice(policy.rules.indexOf(rule), 1);
    updateUnusedData(policy);
}

function loadPolicyRule(policy) {
    if (!policy.rulesPopulated) {
        policyRulesResource = Vue.resource(host + '/policies{/policy_id}/rules{/rule_id}', {}, {patch: {method: 'PATCH'}});
        categoryMap['subject'].resource = Vue.resource(host + '/policies{/policy_id}/subject_data{/category_id}{/data_id}', {});
        categoryMap['object'].resource = Vue.resource(host + '/policies{/policy_id}/object_data{/category_id}{/data_id}', {});
        categoryMap['action'].resource = Vue.resource(host + '/policies{/policy_id}/action_data{/category_id}{/data_id}', {});
        var queries = [
            policyRulesResource.query({ policy_id: policy.id }),
            categoryMap['subject'].resource.query({ policy_id: policy.id }),
            categoryMap['object'].resource.query({ policy_id: policy.id }),
            categoryMap['action'].resource.query({ policy_id: policy.id })
        ]

        Promise.all(queries).then(function (result) {
            createRules(policy, result[0].body, result[1].body, result[2].body, result[3].body);
            updateUnusedData(policy);
        }, util.displayErrorFunction('Unable to load rules'))
    }
}

function updateUnusedData(policy) {
    policy.unusedSubjectData.splice(0, policy.unusedSubjectData.length);
    util.pushAll(policy.unusedSubjectData, policy.subjectData);

    policy.unusedObjectData.splice(0, policy.unusedObjectData.length);
    util.pushAll(policy.unusedObjectData, policy.objectData);

    policy.unusedActionData.splice(0, policy.unusedActionData.length);
    util.pushAll(policy.unusedActionData, policy.actionData);

    for (var i = 0; i < policy.rules.length; i++) {
        var rule = policy.rules[i];
        removeUsedData(rule.subjectData, policy.unusedSubjectData);
        removeUsedData(rule.objectData, policy.unusedObjectData);
        removeUsedData(rule.actionData, policy.unusedActionData);
    }
}

function removeUsedData(list, orphanList) {
    for (var j = 0; j < list.length; j++) {
        var data = list[j];
        if (data) {
            var notOrphanIndex = util.indexOf(orphanList, "id", data.id);
            if (notOrphanIndex >= 0) {
                orphanList.splice(notOrphanIndex, 1);
            }
        }
    }
}

function transformData(list) {
    var result = {};
    for (var index = 0; index < list.length; index++) {
        var data = list[index].data;
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                result[key] = data[key];
            }
        }
    }
    return result;
}

function createRules(policy, rulesData, subjectsData, objectsData, actionsData) {
    policy.rules = rulesData ? rulesData.rules.rules : [];
    policy.subjectDataMap = transformData(subjectsData.subject_data);
    policy.subjectData = util.mapToArray(policy.subjectDataMap);
    policy.objectDataMap = transformData(objectsData.object_data);
    policy.objectData = util.mapToArray(policy.objectDataMap);
    policy.actionDataMap = transformData(actionsData.action_data);
    policy.actionData = util.mapToArray(policy.actionDataMap);
    for (var i = 0; i < policy.rules.length; i++) {
        var rule = policy.rules[i];
        populateRule(policy, rule);
    }
    policy.rulesPopulated = true;
}

function populateRule(policy, rule) {
    if (rule.meta_rule_id) {
        rule.metaRule = ModelService.getMetaRule(rule.meta_rule_id);
    }
    if (rule.metaRule) {
        var j = 0;
        var k, id;
        rule.subjectData = [];
        rule.objectData = [];
        rule.actionData = [];
        rule.attributeData = [];

        for (k = 0; k < rule.metaRule.subject_categories.length; k++) {
            id = rule.rule[j + k];
            if (policy.subjectDataMap[id])
                rule.subjectData.push(policy.subjectDataMap[id]);
        }
        j += k;
        for (k = 0; k < rule.metaRule.object_categories.length; k++) {
            id = rule.rule[j + k];
            if (policy.objectDataMap[id])
                rule.objectData.push(policy.objectDataMap[id]);
        }
        j += k;
        for (k = 0; k < rule.metaRule.action_categories.length; k++) {
                id = rule.rule[j + k];
                if (policy.actionDataMap[id]) {
                    rule.actionData.push(policy.actionDataMap[id]);
                }
        }

        for (const value of rule.rule.values()){
            if (value.includes("attributes:")){
                let attrName = value.split(':')[1];
                let attrId = AttributeService.getAttributeId(attrName);
                rule.attributeData.push({id: attrId, name: attrName});

            }
        }
    }
    return rule;
}

function updateRule(policy, rule, decision){
    return new Promise(resolveUpdateRule => {
        var body = {
            "instructions":[
                {"decision": decision}
            ]
        };

        policyRulesResource.patch({policy_id: policy.id, rule_id: rule.id}, body).then(success, util.displayErrorFunction('Unable to update Rule'));

        function success(data){
            resolveUpdateRule(data.body.rules[rule.id].instructions);
        }
    });
}

function filterRuleBySpecificItem(filteredRules, rule, items, filter){
    items.forEach(item => {
        if (item){
            if (filter == null || item.name.indexOf(filter) >= 0){
                if (!(filteredRules.includes(rule)))
                    filteredRules.push(rule)
            }
        }

    });
}

function interArray(array1, array2){
    let inter = [];


    for (let i = 0; i < array1.length; i++){
        for (let j = 0; j < array2.length; j++){
            if (array1[i] === array2[j])
                inter.push(array2[j]);
        }
    }
    return inter;
}


function filterByRules(rules, filters){
    let filteredRules = [];
    let filteredByWords = [];


    if (filters === ""){
        filteredRules = rules;
    } else {
        filters = filters.split(' ');
        filters.forEach( filter => {
            if (filter !== "") {
                let tmp = [];
                rules.forEach((rule) => {

                    filterRuleBySpecificItem(tmp, rule, rule.subjectData, filter);
                    filterRuleBySpecificItem(tmp, rule, rule.objectData, filter);
                    filterRuleBySpecificItem(tmp, rule, rule.actionData, filter);
                    filterRuleBySpecificItem(tmp, rule, rule.attributeData, filter);

                    filteredByWords.push(tmp);
                });

            }
        });

        filteredRules = filteredByWords[0];
        for (let i = 1; i < filteredByWords.length; i++){
            filteredRules = interArray(filteredRules, filteredByWords[i]);
        }
    }

    return filteredRules;
}

function policyRuleWithAttributes(policy){
    const meta_rules = policy.model.meta_rules;

    for (let i = 0; i < meta_rules.length; i++){
        const meta_rule = meta_rules[i];
        if (meta_rule.actionAttributes.length || meta_rule.subjectAttributes.length || meta_rule.objectAttributes.length)
            return true;
    }
    return false;
}

export default {
    policyRuleWithAttributes: policyRuleWithAttributes,
    filterByRules: filterByRules,
    initialize: loadPolicies,
    createPolicies: createPolicies,
    policies: policies,
    getPolicy: function getPolicy(id) {
        return policiesMap[id];
    },
    createPolicy: function createPolicy(policy) {
        policyResource.save(null, policy).then(success, util.displayErrorFunction('Unable to create Policy'));

        function success(data) {
            createPolicyInternal(data.body.policies);
            util.displaySuccess('Policy created');
        }
    },
    removePolicy: function removePolicy(policy) {
        policyResource.remove({ id: policy.id }, null).then(success, util.displayErrorFunction('Unable to remove Policy'));

        function success() {
            removePolicyInternal(policy.id);
            util.displaySuccess('Policy removed');
        }
    },
    updatePolicy: function updatePolicy(policy) {
        policyResource.patch({ id: policy.id }, policy).then(success, util.displayErrorFunction('Unable to update Policy'));

        function success(data) {
            updatePolicyInternal(data.body.policies)
            util.displaySuccess('Policy updated');
        }
    },
    populatePolicy: loadPolicyRule,
    createRules: createRules,
    updateRule: updateRule,
    addRuleToPolicy: function addRuleToPolicy(policy, rule) {
        policyRulesResource.save({ policy_id: policy.id }, rule).then(success, util.displayErrorFunction('Unable to create Rule'));

        function success(data) {
            var rules = util.mapToArray(data.body.rules);
            for (var i = 0; i < rules.length; i++) {
                var rule = rules[i];
                policy.rules.push(populateRule(policy, rule))
            }
            util.displaySuccess('Rule created');
            updateUnusedData(policy);
        }
    },
    removeRuleFromPolicy: function removeRuleFromPolicy(policy, rule) {
        policyRulesResource.remove({ policy_id: policy.id, rule_id: rule.id }, null).then(success, util.displayErrorFunction('Unable to remove Rule'));

        function success() {
            removeRuleInternal(policy, rule);
            util.displaySuccess('Rule removed');
        }
    },
    createData: function createData(type, policy, categoryId, dataCategory) {
        var categoryValue = categoryMap[type];
        return categoryValue.resource.save({ policy_id: policy.id, category_id: categoryId }, dataCategory).then(
            function (data) {
                var result = util.createInternal(data.body[categoryValue.responseName].data, policy[categoryValue.arrayName], policy[categoryValue.mapName]);
                util.displaySuccess('Data created');
                util.pushAll(policy[categoryValue.unusedArrayName], result);
                return result;
            },
            util.displayErrorFunction('Unable to create Data')
        );
    },
    removeData: function removeData(type, policy, data) {
        var categoryValue = categoryMap[type];
        return categoryValue.resource.remove({ policy_id: policy.id, category_id: data.category_id, data_id: data.id }).then(
            function () {
                policy[categoryValue.arrayName].splice(policy.subjectData.indexOf(data), 1);
                policy[categoryValue.unusedArrayName].splice(policy.unusedSubjectData.indexOf(data), 1);
                delete policy[categoryValue.mapName][data.id];
                util.displaySuccess('Data removed');
            },
            util.displayErrorFunction('Unable to remove Data')
        );
    },
    createPerimeter: function createPerimeter(type, policy, perimeter) {
        var categoryValue = categoryMap[type];
        return categoryValue.policyPerimeterResource.save({ policy_id: policy.id }, perimeter).then(
            function (data) {
                util.displaySuccess('Perimeter created');
                return util.mapToArray(data.body[categoryValue.perimeterResponseName]);
            },
            util.displayErrorFunction('Unable to create Perimeter')
        );
    },
    removePerimeterFromPolicy: function removePerimeterFromPolicy(type, policy, perimeter) {
        var categoryValue = categoryMap[type];

        return categoryValue.policyPerimeterResource.remove({ policy_id: policy.id, perimeter_id: perimeter.id }, null).then(
            function () {
                util.displaySuccess('Perimeter removed');
                return perimeter;
            },
            util.displayErrorFunction('Unable to remove Perimeter')
        )
    },
    addPerimeterToPolicy: function addPerimeterToPolicy(type, policy, perimeter) {
        var categoryValue = categoryMap[type];
        perimeter.policy_list.push(policy.id);
        var perimeterClone = util.clone(perimeter);
        delete perimeterClone.policy_list;
        return categoryValue.policyPerimeterResource.save({ policy_id: policy.id }, perimeterClone).then(
            function () {
                util.displaySuccess('Perimeter added');
            },
            util.displayErrorFunction('Unable to add Perimeter')
        )
    },
    loadPerimetersAndAssignments: function loadPerimetersAndAssignments(type, policy) {
        var categoryValue = categoryMap[type];
        var queries = [
            categoryValue.perimeterResource.query(),
            categoryValue.policyPerimeterResource.query({ policy_id: policy.id }),
            categoryValue.assignmentResource.query({ policy_id: policy.id }),
        ]

        return Promise.all(queries).then(function (data) {
            var result = {};
            result.assignments = util.mapToArray(data[2].body[categoryValue.assignmentResponseName]);
            result.perimetersMap = data[1].body[categoryValue.perimeterResponseName];
            result.perimeters = util.mapToArray(result.perimetersMap);
            result.allPerimeters = util.mapToArray(data[0].body[categoryValue.perimeterResponseName]);
            return result;
        }, util.displayErrorFunction('Unable to load Perimeters'))

    },
    createAssignment: function createAssignment(type, policy, perimeter, data) {
        var categoryValue = categoryMap[type];
        var assignment = {
            "id": perimeter.id,
            "category_id": data.category_id,
            "data_id": data.id,
            "policy_id": policy.id
        }
        return categoryValue.assignmentResource.save({ policy_id: policy.id }, assignment).then(
            function (data) {
                util.displaySuccess('Assignment created');
                return util.mapToArray(data.body[categoryValue.assignmentResponseName]);
            },
            util.displayErrorFunction('Unable to create Assignment')
        )
    },
    removeAssignment: function removeAssignment(type, policy, perimeter, data) {
        var categoryValue = categoryMap[type];

        return categoryValue.assignmentResource.remove({ policy_id: policy.id, perimeter_id: perimeter.id, category_id: data.category_id, data_id: data.id }, null).then(
            function () {
                util.displaySuccess('Assignment removed');
            },
            util.displayErrorFunction('Unable to remove Assignment')
        )
    },
}

