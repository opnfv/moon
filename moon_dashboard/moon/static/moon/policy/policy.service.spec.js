(function () {
    'use strict';

    describe('moon.policy.service', function () {
        var service, modelService, $httpBackend, URI;
        var policiesData;
        var modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData;
        var rulesData, subjectsData, objectsData, actionsData;


        function initData() {
            policiesData = {
                policies:
                    {
                        'policyId1': { name: 'policy1', description: 'pDescription1', genre: 'genre1', model_id: 'modelId1' },
                    }
            };

            modelsData = {
                models:
                    { 'modelId1': { name: 'model1', description: 'mDescription1', meta_rules: ['metaRuleId1'] } }
            };

            subjectCategoriesData = {
                subject_categories:
                    {
                        'subjectCategoryId1': { name: 'subjectCategory1', description: 'scDescription1' },
                        'subjectCategoryId2': { name: 'subjectCategory2', description: 'scDescription2' }
                    },
            };
            objectCategoriesData = {
                object_categories:
                    {
                        'objectCategoryId1': { name: 'objectCategory1', description: 'ocDescription1' },
                        'objectCategoryId2': { name: 'objectCategory2', description: 'ocDescription2' }
                    }
            };
            actionCategoriesData = {
                action_categories:
                    {
                        'actionCategoryId1': { name: 'actionCategory1', description: 'acDescription1' },
                        'actionCategoryId2': { name: 'actionCategory2', description: 'acDescription2' }
                    }
            };
            metaRulesData = {
                meta_rules:
                    {
                        'metaRuleId1': { name: 'metaRule1', description: 'mrDescription1', subject_categories: ['subjectCategoryId1'], object_categories: ['objectCategoryId1'], action_categories: ['actionCategoryId1'] },
                        'metaRuleId2': { name: 'metaRule2', description: 'mrDescription2', subject_categories: [], object_categories: [], action_categories: [] }
                    }
            };
        }

        function initRuleData() {
            rulesData = {
                rules: {
                    rules: [
                        { meta_rule_id: 'metaRuleId1', rule: ['subjectId1', 'objectId1', 'actionId1'], id: 'ruleId1', instructions: { test: 'test' } }
                    ]
                }
            };

            subjectsData = {
                subject_data:
                    [
                        {
                            data: {
                                'subjectId1': { name: 'subject1', description: 'sDescription1' },
                            }
                        }
                    ]
            };
            objectsData = {
                object_data:
                    [
                        {
                            data: {
                                'objectId1': { name: 'object1', description: 'oDescription1' },
                            }
                        }
                    ]
            };
            actionsData = {
                action_data:
                    [
                        {
                            data: {
                                'actionId1': { name: 'action1', description: 'aDescription1' },
                            }
                        }
                    ]
            };
        }

        beforeEach(module('horizon.app.core'));
        beforeEach(module('horizon.framework'));
        beforeEach(module('moon'));

        beforeEach(inject(function ($injector) {
            service = $injector.get('moon.policy.service');
            modelService = $injector.get('moon.model.service');
            $httpBackend = $injector.get('$httpBackend');
            URI = $injector.get('moon.URI');
        }));

        afterEach(function () {
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
        });

        it('should initialize', function () {
            initData();
            $httpBackend.expectGET(URI.API + '/policies').respond(200, policiesData);
            $httpBackend.expectGET(URI.API + '/subject_categories').respond(200, subjectCategoriesData);
            $httpBackend.expectGET(URI.API + '/object_categories').respond(200, objectCategoriesData);
            $httpBackend.expectGET(URI.API + '/action_categories').respond(200, actionCategoriesData);
            $httpBackend.expectGET(URI.API + '/meta_rules').respond(200, metaRulesData);
            $httpBackend.expectGET(URI.API + '/models').respond(200, modelsData);


            service.initialize();
            $httpBackend.flush();

            expect(service.policies.length).toBe(1);
            var policy = service.policies[0];
            expect(policy.id).toBe('policyId1');
            expect(policy.name).toBe('policy1');
            expect(policy.description).toBe('pDescription1');
            expect(policy.genre).toBe('genre1');
            expect(policy.model.id).toBe('modelId1');

        });



        it('should create policy', function () {
            initData();
            modelService.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);

            var policyCreatedData = {
                policies:
                    { 'policyId1': { name: 'policy1', description: 'pDescription1', genre: 'genre1', model_id: 'modelId1' } }
            };

            $httpBackend.expectPOST(URI.API + '/policies').respond(200, policyCreatedData);

            service.createPolicy({ name: 'policy1', description: 'pDescription1', genre: 'genre1', model: modelService.getModel('modelId1') });
            $httpBackend.flush();

            expect(service.policies.length).toBe(1);
            var policy = service.policies[0];
            expect(policy.id).toBe('policyId1');
            expect(policy.name).toBe('policy1');
            expect(policy.description).toBe('pDescription1');
            expect(policy.genre).toBe('genre1');
            expect(policy.model.id).toBe('modelId1');
        });

        it('should remove policy', function () {
            initData();
            modelService.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);
            service.createPolicies(policiesData);

            $httpBackend.expectDELETE(URI.API + '/policies/policyId1').respond(200);

            service.removePolicy({ id: 'policyId1' });
            $httpBackend.flush();

            expect(service.policies.length).toBe(0);
        });

        it('should update policy', function () {
            initData();
            var policyUpdatedData = {
                policies:
                    { 'policyId1': { name: 'policy2', description: 'pDescription2', genre: 'genre2', model_id: 'modelId1' } }
            };
            modelService.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);
            service.createPolicies(policiesData);

            $httpBackend.expectPATCH(URI.API + '/policies/policyId1').respond(200, policyUpdatedData);

            service.updatePolicy({ id: 'policyId1', name: 'policy2', description: 'pDescription2', genre: 'genre2', model: modelService.getModel('modelId1') });
            $httpBackend.flush();

            expect(service.policies.length).toBe(1);
            var policy = service.policies[0];
            expect(policy.id).toBe('policyId1');
            expect(policy.name).toBe('policy2');
            expect(policy.description).toBe('pDescription2');
            expect(policy.genre).toBe('genre2');
            expect(policy.model.id).toBe('modelId1');

        });


        it('should populate policy', function () {
            initData();
            initRuleData();
            modelService.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);
            service.createPolicies(policiesData);

            var policy = service.getPolicy('policyId1')

            $httpBackend.expectGET(URI.API + '/policies/policyId1/rules').respond(200, rulesData);
            $httpBackend.expectGET(URI.API + '/policies/policyId1/subject_data').respond(200, subjectsData);
            $httpBackend.expectGET(URI.API + '/policies/policyId1/object_data').respond(200, objectsData);
            $httpBackend.expectGET(URI.API + '/policies/policyId1/action_data').respond(200, actionsData);

            service.populatePolicy(policy);
            $httpBackend.flush();

            expect(policy.rules.length).toBe(1);
            var rule = policy.rules[0];
            expect(rule.id).toBe('ruleId1');
            expect(rule.metaRule.id).toBe('metaRuleId1');
            expect(rule.instructions.test).toBe('test');
            expect(rule.subjectData.length).toBe(1);
            expect(rule.subjectData[0].id).toBe('subjectId1');
            expect(rule.objectData.length).toBe(1);
            expect(rule.objectData[0].id).toBe('objectId1');
            expect(rule.actionData.length).toBe(1);
            expect(rule.actionData[0].id).toBe('actionId1');

            expect(policy.subjectData.length).toBe(1);
            var subjectData = policy.subjectData[0];
            expect(subjectData.id).toBe('subjectId1');
            expect(subjectData.name).toBe('subject1');
            expect(subjectData.description).toBe('sDescription1');

            expect(policy.objectData.length).toBe(1);
            var objectData = policy.objectData[0];
            expect(objectData.id).toBe('objectId1');
            expect(objectData.name).toBe('object1');
            expect(objectData.description).toBe('oDescription1');

            expect(policy.actionData.length).toBe(1);
            var actionData = policy.actionData[0];
            expect(actionData.id).toBe('actionId1');
            expect(actionData.name).toBe('action1');
            expect(actionData.description).toBe('aDescription1');

        });


        it('should add rule to policy', function () {
            initData();
            initRuleData();
            modelService.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);
            service.createPolicies(policiesData);


            var ruleCreatedData = {
                rules: {
                    'ruleId1': { meta_rule_id: 'metaRuleId1', rule: ['subjectId1', 'objectId1', 'actionId1'], instructions: { test: 'test' } }
                }
            };

            var policy = service.getPolicy('policyId1');

            service.createRules(policy, null, subjectsData, objectsData, actionsData);

            $httpBackend.expectPOST(URI.API + '/policies/policyId1/rules').respond(200, ruleCreatedData);

            service.addRuleToPolicy(policy, { meta_rule_id: 'metaRuleId1', rule: ['subjectId1', 'objectId1', 'actionId1'], instructions: { test: 'test' } });
            $httpBackend.flush();

            expect(policy.rules.length).toBe(1);
            var rule = policy.rules[0];
            expect(rule.id).toBe('ruleId1');
            expect(rule.metaRule.id).toBe('metaRuleId1');
            expect(rule.subjectData.length).toBe(1);
            expect(rule.subjectData[0].id).toBe('subjectId1');
            expect(rule.objectData.length).toBe(1);
            expect(rule.objectData[0].id).toBe('objectId1');
            expect(rule.actionData.length).toBe(1);
            expect(rule.actionData[0].id).toBe('actionId1');

        });

        it('should remove rule from policy', function () {
            initData();
            initRuleData();
            modelService.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);
            service.createPolicies(policiesData);

            var policy = service.getPolicy('policyId1');

            service.createRules(policy, rulesData, subjectsData, objectsData, actionsData);

            $httpBackend.expectDELETE(URI.API + '/policies/policyId1/rules/ruleId1').respond(200);

            service.removeRuleFromPolicy(policy, { id: 'ruleId1' });
            $httpBackend.flush();

            expect(policy.rules.length).toBe(0);
        });


        it('should create data', function () {
            initData();
            initRuleData();
            modelService.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);
            service.createPolicies(policiesData);


            var dataCreatedData = {
                subject_data: {
                    data: {
                        'subjectId1': { name: 'subject1', description: 'sDescription1' },
                    }
                }
            };

            var policy = service.getPolicy('policyId1');
            policy.subjectData = [];
            policy.subjectDataMap = {};

            $httpBackend.expectPOST(URI.API + '/policies/policyId1/subject_data/subjectCategoryId1').respond(200, dataCreatedData);

            service.createData('subject', policy, modelService.getCategory('subject', 'subjectCategoryId1'), { name: 'subject1', description: 'sDescription1' });
            $httpBackend.flush();

            expect(policy.subjectData.length).toBe(1);
            var subjectData = policy.subjectData[0];
            expect(subjectData.id).toBe('subjectId1');
            expect(subjectData.name).toBe('subject1');
            expect(subjectData.description).toBe('sDescription1');

        });


    });


})();