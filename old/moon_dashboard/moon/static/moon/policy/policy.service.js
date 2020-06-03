(function () {

    'use strict';

    angular
        .module('moon')
        .factory('moon.policy.service', policyService);

    policyService.$inject = ['moon.util.service', 'moon.model.service', '$resource', 'moon.URI', '$q', 'horizon.framework.widgets.toast.service'];

    function policyService(util, modelService, $resource, URI, $q, toast) {
        var host = URI.API;

        var policyResource = $resource(host + '/policies/' + ':id', {}, {
            get: { method: 'GET' },
            query: { method: 'GET' },
            create: { method: 'POST' },
            remove: { method: 'DELETE' },
            update: { method: 'PATCH' }
        });

        var policyRulesResource = $resource(host + '/policies/' + ':policy_id' + '/rules/' + ':rule_id', {}, {
            get: { method: 'GET' },
            query: { method: 'GET' },
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        });

        var policySubjectDataResource = $resource(host + '/policies/' + ':policy_id' + '/subject_data/' + ':category_id' + '/' + ':data_id', {}, {
            query: {method: 'GET'},
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        })

        var policyObjectDataResource = $resource(host + '/policies/' + ':policy_id' + '/object_data/' + ':category_id' + '/' + ':data_id', {}, {
            query: {method: 'GET'},
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        })

        var policyActionDataResource = $resource(host + '/policies/' + ':policy_id' + '/action_data/' + ':category_id' + '/' + ':data_id', {}, {
            query: {method: 'GET'},
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        })

        var policySubjectPerimetersResource = $resource(host + '/policies/' + ':policy_id' + '/subjects/' + ':perimeter_id', {}, {
            query: {method: 'GET'},
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        })

        var policyObjectPerimetersResource = $resource(host + '/policies/' + ':policy_id' + '/objects/' + ':perimeter_id', {}, {
            query: {method: 'GET'},
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        })

        var policyActionPerimetersResource = $resource(host + '/policies/' + ':policy_id' + '/actions/' + ':perimeter_id', {}, {
            query: {method: 'GET'},
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        })

        var subjectPerimetersResource = $resource(host + '/subjects/' + ':perimeter_id', {}, {
            query: {method: 'GET'},
            update: { method: 'PATCH' }
        })

        var objectPerimetersResource = $resource(host + '/objects/' + ':perimeter_id', {}, {
            query: {method: 'GET'},
            update: { method: 'PATCH' }
        })

        var actionPerimetersResource = $resource(host + '/actions/' + ':perimeter_id', {}, {
            query: {method: 'GET'},
            update: { method: 'PATCH' }
        })

        var policySubjectAssignmentsResource = $resource(host + '/policies/' + ':policy_id' + '/subject_assignments/' + ':perimeter_id' + '/' + ':category_id' + '/' + ':data_id', {}, {
            query: {method: 'GET'},
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        })

        var policyObjectAssignmentsResource = $resource(host + '/policies/' + ':policy_id' + '/object_assignments/' + ':perimeter_id' + '/' + ':category_id' + '/' + ':data_id', {}, {
            query: {method: 'GET'},
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        })

        var policyActionAssignmentsResource = $resource(host + '/policies/' + ':policy_id' + '/action_assignments/' + ':perimeter_id' + '/' + ':category_id' + '/' + ':data_id', {}, {
            query: {method: 'GET'},
            create: { method: 'POST' },
            remove: { method: 'DELETE' }
        })


        var categoryMap = {
            'subject': {
                resource: policySubjectDataResource,
                arrayName: "subjectData",
                mapName: "subjectDataMap",
                responseName: "subject_data",
                policyPerimeterResource: policySubjectPerimetersResource,
                perimeterResource: subjectPerimetersResource,
                assignmentResource: policySubjectAssignmentsResource,
                perimeterResponseName: "subjects",
                assignmentResponseName: "subject_assignments",
                unusedArrayName: "unusedSubjectData",
            },
            'object': {
                resource: policyObjectDataResource,
                arrayName: "objectData",
                mapName: "objectDataMap",
                responseName: "object_data",
                policyPerimeterResource: policyObjectPerimetersResource,
                perimeterResource: objectPerimetersResource,
                assignmentResource: policyObjectAssignmentsResource,
                perimeterResponseName: "objects",
                assignmentResponseName: "object_assignments",
                unusedArrayName: "unusedObjectData",
            },
            'action': {
                resource: policyActionDataResource,
                arrayName: "actionData",
                mapName: "actionDataMap",
                responseName: "action_data",
                policyPerimeterResource: policyActionPerimetersResource,
                perimeterResource: actionPerimetersResource,
                assignmentResource: policyActionAssignmentsResource,
                perimeterResponseName: "actions",
                assignmentResponseName: "action_assignments",
                unusedArrayName: "unusedActionData",
            }
        }

        var policiesMap = {};
        var policies = [];

        function loadPolicies() {
            var queries = {
                policies: policyResource.query().$promise,
                models: modelService.initialize(),
            }

            $q.all(queries).then(function (result) {
                createPolicies(result.policies);
                console.log('moon', 'policies initialized')
            })
        }

        function createPolicies(policiesData) {
            policies.splice(0, policies.length);
            util.cleanObject(policiesMap);
            createPolicyInternal(policiesData.policies);
        }

        function mapPolicy(policy) {
            if (policy.model_id) {
                policy.model = modelService.getModel(policy.model_id);
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
            if (!policy.rules) {
                var queries = {
                    rules: policyRulesResource.query({ policy_id: policy.id }).$promise,
                    subjectData: policySubjectDataResource.query({ policy_id: policy.id }).$promise,
                    objectData: policyObjectDataResource.query({ policy_id: policy.id }).$promise,
                    actionData: policyActionDataResource.query({ policy_id: policy.id }).$promise,
                }
    
                $q.all(queries).then(function (result) {
                    createRules(policy, result.rules, result.subjectData, result.objectData, result.actionData);
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
                var notOrphanIndex = util.indexOf(orphanList, "id", data.id);
                if (notOrphanIndex >= 0) {
                    orphanList.splice(notOrphanIndex, 1);
                }
            }
        }

        function createRules(policy, rulesData, subjectsData, objectsData, actionsData) {
            policy.rules = rulesData ? rulesData.rules.rules : [];
            policy.subjectDataMap = subjectsData.subject_data.length > 0 ? subjectsData.subject_data[0].data : [];
            policy.subjectData = util.mapToArray(policy.subjectDataMap);
            policy.objectDataMap = objectsData.object_data.length > 0 ? objectsData.object_data[0].data : [];
            policy.objectData = util.mapToArray(policy.objectDataMap);
            policy.actionDataMap = actionsData.action_data.length > 0 ? actionsData.action_data[0].data : [];
            policy.actionData = util.mapToArray(policy.actionDataMap);
            policy.unusedSubjectData = [];
            policy.unusedObjectData = [];
            policy.unusedActionData = [];
            for (var i = 0; i < policy.rules.length; i++) {
                var rule = policy.rules[i];
                populateRule(policy, rule);
            }
        }

        function populateRule(policy, rule) {
            if (rule.meta_rule_id) {
                rule.metaRule = modelService.getMetaRule(rule.meta_rule_id);
            } 
            if (rule.metaRule) {
                var j = 0;
                var k, id;
                rule.subjectData = [];
                rule.objectData = [];
                rule.actionData = [];
                for (k = 0; k < rule.metaRule.subject_categories.length; k++) {
                    id = rule.rule[j + k];
                    rule.subjectData.push(policy.subjectDataMap[id]);
                }
                j += k;
                for (k = 0; k < rule.metaRule.object_categories.length; k++) {
                    id = rule.rule[j + k];
                    rule.objectData.push(policy.objectDataMap[id]);
                }
                j += k;
                for (k = 0; k < rule.metaRule.action_categories.length; k++) {
                    id = rule.rule[j + k];
                    rule.actionData.push(policy.actionDataMap[id]);
                }
            }
            return rule;
        }

        return {
            initialize: loadPolicies,
            createPolicies: createPolicies,
            policies: policies,
            getPolicy: function getPolicy(id) {
                return policiesMap[id];
            },
            createPolicy: function createPolicy(policy) {
                policyResource.create(null, policy, success, util.displayErrorFunction('Unable to create Policy'));

                function success(data) {
                    createPolicyInternal(data.policies);
                    util.displaySuccess('Policy created');
                }
            },
            removePolicy: function removePolicy(policy) {
                policyResource.remove({ id: policy.id }, null, success, util.displayErrorFunction('Unable to remove Policy'));

                function success(data) {
                    removePolicyInternal(policy.id);
                    util.displaySuccess('Policy removed');
                }
            },
            updatePolicy: function updatePolicy(policy) {
                policyResource.update({ id: policy.id }, policy, success, util.displayErrorFunction('Unable to update Policy'));

                function success(data) {
                    updatePolicyInternal(data.policies)
                    util.displaySuccess('Policy updated');
                }
            },
            populatePolicy: loadPolicyRule,
            createRules: createRules,
            addRuleToPolicy: function addRuleToPolicy(policy, rule) {
                policyRulesResource.create({ policy_id: policy.id }, rule, success, util.displayErrorFunction('Unable to create Rule'));

                function success(data) {
                    var rules = util.mapToArray(data.rules);
                    for (var i = 0; i < rules.length; i++) {
                        var rule = rules[i];
                        policy.rules.push(populateRule(policy, rule))
                    }
                    util.displaySuccess('Rule created');
                    updateUnusedData(policy);
                }
            },
            removeRuleFromPolicy: function removeRuleFromPolicy(policy, rule) {
                policyRulesResource.remove({ policy_id: policy.id, rule_id: rule.id }, null, success, util.displayErrorFunction('Unable to remove Rule'));

                function success(data) {
                    removeRuleInternal(policy, rule);
                    util.displaySuccess('Rule removed');
                }
            },
            createData: function createData(type, policy, category, dataCategory) {
                var categoryValue = categoryMap[type];
                return categoryValue.resource.create({ policy_id: policy.id, category_id: category.id }, dataCategory).$promise.then(
                    function (data) {
                        var result = util.createInternal(data[categoryValue.responseName].data, policy[categoryValue.arrayName], policy[categoryValue.mapName]);
                        util.displaySuccess('Data created');
                        util.pushAll(policy[categoryValue.unusedArrayName], result);
                        return result;
                    }, 
                    util.displayErrorFunction('Unable to create Data')
                );
            },
            removeData: function removeData(type, policy, data) {
                var categoryValue = categoryMap[type];
                return categoryValue.resource.remove({ policy_id: policy.id, category_id: data.category_id, data_id: data.id }).$promise.then(
                    function (data) {
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
                return categoryValue.policyPerimeterResource.create({ policy_id: policy.id }, perimeter).$promise.then(
                    function (data) {
                        util.displaySuccess('Perimeter created');
                        return util.mapToArray(data[categoryValue.perimeterResponseName]);
                    },
                    util.displayErrorFunction('Unable to create Perimeter')
                );
            },
            removePerimeterFromPolicy: function removePerimeterFromPolicy(type, policy, perimeter) {
                var categoryValue = categoryMap[type];

                return categoryValue.policyPerimeterResource.remove({ policy_id: policy.id, perimeter_id: perimeter.id }, null).$promise.then(
                    function (data) {
                        util.displaySuccess('Perimeter removed');
                        return perimeter;
                    },
                    util.displayErrorFunction('Unable to remove Perimeter')
                )
            },
            addPerimeterToPolicy: function addPerimeterToPolicy(type, policy, perimeter) {
                var categoryValue = categoryMap[type];
                perimeter.policy_list.push(policy.id); 

                return categoryValue.perimeterResource.update({ perimeter_id: perimeter.id }, perimeter).$promise.then(
                    function (data) {
                        util.displaySuccess('Perimeter added');
                    },
                    util.displayErrorFunction('Unable to add Perimeter')
                )
            },
            loadPerimetersAndAssignments: function loadPerimetersAndAssignments(type, policy) {
                var categoryValue = categoryMap[type];
                var queries = {
                    allPerimeters: categoryValue.perimeterResource.query().$promise,
                    perimeters: categoryValue.policyPerimeterResource.query({ policy_id: policy.id }).$promise,
                    assignments: categoryValue.assignmentResource.query({ policy_id: policy.id }).$promise,
                }
    
                return $q.all(queries).then(function (data) {
                    var result = {};
                    result.assignments = util.mapToArray(data.assignments[categoryValue.assignmentResponseName]);
                    result.perimetersMap = data.perimeters[categoryValue.perimeterResponseName];
                    result.perimeters = util.mapToArray(result.perimetersMap);
                    result.allPerimeters = util.mapToArray(data.allPerimeters[categoryValue.perimeterResponseName]);
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
                return categoryValue.assignmentResource.create({ policy_id: policy.id }, assignment).$promise.then(
                    function (data) {
                        util.displaySuccess('Assignment created');
                        return util.mapToArray(data[categoryValue.assignmentResponseName]);
                    },
                    util.displayErrorFunction('Unable to create Assignment')
                )
            },
            removeAssignment: function removeAssignment(type, policy, perimeter, data) {
                var categoryValue = categoryMap[type];

                return categoryValue.assignmentResource.remove({ policy_id: policy.id, perimeter_id: perimeter.id, category_id: data.category_id, data_id: data.id }, null).$promise.then(
                    function (data) {
                        util.displaySuccess('Assignment removed');
                    },
                    util.displayErrorFunction('Unable to remove Assignment')
                )
            },
        }
 
    }
})();