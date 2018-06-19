(function () {
    'use strict';

    describe('moon.model.service', function () {
        var service, $httpBackend, URI;
        var modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData;

        function initData() {
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

        beforeEach(module('horizon.app.core'));
        beforeEach(module('horizon.framework'));
        beforeEach(module('moon'));

        beforeEach(inject(function ($injector) {
            service = $injector.get('moon.model.service');
            $httpBackend = $injector.get('$httpBackend');
            URI = $injector.get('moon.URI');
        }));

        afterEach(function () {
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
        });

        it('should initialize', function () {
            initData();
            $httpBackend.expectGET(URI.API + '/subject_categories').respond(200, subjectCategoriesData);
            $httpBackend.expectGET(URI.API + '/object_categories').respond(200, objectCategoriesData);
            $httpBackend.expectGET(URI.API + '/action_categories').respond(200, actionCategoriesData);
            $httpBackend.expectGET(URI.API + '/meta_rules').respond(200, metaRulesData);
            $httpBackend.expectGET(URI.API + '/models').respond(200, modelsData);

            service.initialize();
            $httpBackend.flush();

            expect(service.models.length).toBe(1);
            var model = service.models[0];
            expect(model.id).toBe('modelId1');
            expect(model.name).toBe('model1');
            expect(model.description).toBe('mDescription1');

            expect(service.metaRules.length).toBe(2);
            expect(model.meta_rules.length).toBe(1);
            var metaRule = model.meta_rules[0];
            expect(metaRule.id).toBe('metaRuleId1');
            expect(metaRule.name).toBe('metaRule1');
            expect(metaRule.description).toBe('mrDescription1');

            expect(service.subjectCategories.length).toBe(2);
            expect(metaRule.subject_categories.length).toBe(1);
            var subjectCategory = metaRule.subject_categories[0];
            expect(subjectCategory.id).toBe('subjectCategoryId1');
            expect(subjectCategory.name).toBe('subjectCategory1');
            expect(subjectCategory.description).toBe('scDescription1');

            expect(service.objectCategories.length).toBe(2);
            expect(metaRule.object_categories.length).toBe(1);
            var objectCategory = metaRule.object_categories[0];
            expect(objectCategory.id).toBe('objectCategoryId1');
            expect(objectCategory.name).toBe('objectCategory1');
            expect(objectCategory.description).toBe('ocDescription1');

            expect(service.actionCategories.length).toBe(2);
            expect(metaRule.action_categories.length).toBe(1);
            var actionCategory = metaRule.action_categories[0];
            expect(actionCategory.id).toBe('actionCategoryId1');
            expect(actionCategory.name).toBe('actionCategory1');
            expect(actionCategory.description).toBe('acDescription1');

            expect(service.orphanMetaRules.length).toBe(1);
            metaRule = service.orphanMetaRules[0];
            expect(metaRule.id).toBe('metaRuleId2');
            expect(metaRule.name).toBe('metaRule2');
            expect(metaRule.description).toBe('mrDescription2');

            expect(service.orphanSubjectCategories.length).toBe(1);
            subjectCategory = service.orphanSubjectCategories[0];
            expect(subjectCategory.id).toBe('subjectCategoryId2');
            expect(subjectCategory.name).toBe('subjectCategory2');
            expect(subjectCategory.description).toBe('scDescription2');

            expect(service.orphanObjectCategories.length).toBe(1);
            objectCategory = service.orphanObjectCategories[0];
            expect(objectCategory.id).toBe('objectCategoryId2');
            expect(objectCategory.name).toBe('objectCategory2');
            expect(objectCategory.description).toBe('ocDescription2');

            expect(service.orphanActionCategories.length).toBe(1);
            actionCategory = service.orphanActionCategories[0];
            expect(actionCategory.id).toBe('actionCategoryId2');
            expect(actionCategory.name).toBe('actionCategory2');
            expect(actionCategory.description).toBe('acDescription2');

        });

        

        it('should create model', function () {
            var modelCreatedData = {
                models:
                    { 'modelId1': { name: 'model1', description: 'mDescription1', meta_rules: [] } }
            };

            $httpBackend.expectPOST(URI.API + '/models').respond(200, modelCreatedData);

            service.createModel({ name: 'model1', description: 'mDescription1' });
            $httpBackend.flush();

            expect(service.models.length).toBe(1);
            var model = service.models[0];
            expect(model.id).toBe('modelId1');
            expect(model.name).toBe('model1');
            expect(model.description).toBe('mDescription1');
        });

        it('should remove model', function () {
            initData();
            service.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);

            $httpBackend.expectDELETE(URI.API + '/models/modelId1').respond(200);

            service.removeModel({ id: 'modelId1' });
            $httpBackend.flush();

            expect(service.models.length).toBe(0);

            expect(service.orphanMetaRules.length).toBe(2);
        });

        it('should update model', function () {
            initData();
            var modelUpdatedData = {
                models:
                    { 'modelId1': { name: 'model2', description: 'mDescription2', meta_rules: ['metaRuleId2'] } }
            };
            service.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);

            $httpBackend.expectPATCH(URI.API + '/models/modelId1').respond(200, modelUpdatedData);

            service.updateModel({ id: 'modelId1', name: 'model2', description: 'mDescription2', meta_rules: service.getMetaRule('metaRuleId2') });
            $httpBackend.flush();

            expect(service.models.length).toBe(1);
            var model = service.models[0];
            expect(model.id).toBe('modelId1');
            expect(model.name).toBe('model2');
            expect(model.description).toBe('mDescription2');

            expect(model.meta_rules.length).toBe(1);
            var metaRule = model.meta_rules[0];
            expect(metaRule.id).toBe('metaRuleId2');

            expect(service.orphanMetaRules.length).toBe(1);
            metaRule = service.orphanMetaRules[0];
            expect(metaRule.id).toBe('metaRuleId1');
        });

        it('should create meta rule', function () {
            var metaRuleCreatedData = {
                meta_rules:
                    { 'metaRuleId1': { name: 'metaRule1', description: 'mrDescription1' } }
            };

            $httpBackend.expectPOST(URI.API + '/meta_rules').respond(200, metaRuleCreatedData);

            service.createMetaRule({ name: 'metaRule1', description: 'mrDescription1' });
            $httpBackend.flush();

            expect(service.metaRules.length).toBe(1);
            var metaRule = service.metaRules[0];
            expect(metaRule.id).toBe('metaRuleId1');
            expect(metaRule.name).toBe('metaRule1');
            expect(metaRule.description).toBe('mrDescription1');
        });

        it('should update meta rule', function () {
            initData();
            var metaRuleUpdatedData = {
                meta_rules:
                    { 'metaRuleId1': { name: 'metaRule2', description: 'mrDescription2', subject_categories: ['subjectCategoryId2'], object_categories: ['objectCategoryId2'], action_categories: ['actionCategoryId2'] } }
            };
            service.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);

            $httpBackend.expectPATCH(URI.API + '/meta_rules/metaRuleId1').respond(200, metaRuleUpdatedData);

            service.updateMetaRule({ id: 'metaRuleId1', name: 'metaRule2', description: 'mrDescription2', subject_categories: [service.getCategory('subject', 'subjectCategoryId2')], object_categories: [service.getCategory('object', 'objectCategoryId2')], action_categories: [service.getCategory('action','actionCategoryId2')] });
            $httpBackend.flush();

            var metaRule = service.getMetaRule('metaRuleId1');
            expect(metaRule.id).toBe('metaRuleId1');
            expect(metaRule.name).toBe('metaRule2');
            expect(metaRule.description).toBe('mrDescription2');

            expect(service.orphanSubjectCategories.length).toBe(1);
            var subjectCategory = service.orphanSubjectCategories[0];
            expect(subjectCategory.id).toBe('subjectCategoryId1');

            expect(service.orphanObjectCategories.length).toBe(1);
            var objectCategory = service.orphanObjectCategories[0];
            expect(objectCategory.id).toBe('objectCategoryId1');

            expect(service.orphanActionCategories.length).toBe(1);
            var actionCategory = service.orphanActionCategories[0];
            expect(actionCategory.id).toBe('actionCategoryId1');
        });

        it('should remove meta rule', function () {
            initData();
            service.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);

            $httpBackend.expectDELETE(URI.API + '/meta_rules/metaRuleId2').respond(200);

            service.removeMetaRule(service.getMetaRule('metaRuleId2'));
            $httpBackend.flush();

            expect(service.metaRules.length).toBe(1);
            expect(service.orphanMetaRules.length).toBe(0);
        });

        it('should create category', function () {
            var categoryCreatedData = {
                subject_categories:
                    { 'subjectCategoryId1': { name: 'subjectCategory1', description: 'scDescription1' } }
            };

            $httpBackend.expectPOST(URI.API + '/subject_categories').respond(200, categoryCreatedData);

            service.createCategory('subject', { name: 'subjectCategory1', description: 'scDescription1' });
            $httpBackend.flush();

            expect(service.subjectCategories.length).toBe(1);
            var subjectCategory = service.subjectCategories[0];
            expect(subjectCategory.id).toBe('subjectCategoryId1');
            expect(subjectCategory.name).toBe('subjectCategory1');
            expect(subjectCategory.description).toBe('scDescription1');
        });

        it('should remove category', function () {
            initData();
            service.createModels(modelsData, metaRulesData, subjectCategoriesData, objectCategoriesData, actionCategoriesData);

            $httpBackend.expectDELETE(URI.API + '/subject_categories/subjectCategoryId2').respond(200);

            service.removeCategory('subject', service.getCategory('subject', 'subjectCategoryId2'));
            $httpBackend.flush();

            expect(service.subjectCategories.length).toBe(1);
            expect(service.orphanSubjectCategories.length).toBe(0);
        });

    });


})();