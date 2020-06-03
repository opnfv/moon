(function () {
    'use strict';

    describe('moon.pdp.service', function () {
        var service, $httpBackend, URI;
        var pdpsData, policiesData, projectsData;


        function initData() {
            pdpsData = {
                pdps:
                    { 'pdpId1': { name: 'pdp1', description: 'pdpDescription1', security_pipeline: ['policyId1'], keystone_project_id: 'projectId1' } }
            };

            policiesData = {
                policies:
                    {
                        'policyId1': { name: 'policy1', description: 'pDescription1' },
                        'policyId2': { name: 'policy2', description: 'pDescription2' }
                    }
            };

            projectsData = {
                items: [
                    { name: "project1", id: "projectId1" },
                    { name: "project2", id: "projectId2" }
                ]
            };

        }

        beforeEach(module('horizon.app.core'));
        beforeEach(module('horizon.framework'));
        beforeEach(module('moon'));

        beforeEach(inject(function ($injector) {
            service = $injector.get('moon.pdp.service');
            $httpBackend = $injector.get('$httpBackend');
            URI = $injector.get('moon.URI');
        }));

        afterEach(function () {
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
        });

        it('should initialize', function () {
            initData();
            $httpBackend.expectGET(URI.API + '/pdp').respond(200, pdpsData);
            $httpBackend.expectGET(URI.API + '/policies').respond(200, policiesData);
            $httpBackend.expectGET('/api/keystone/projects/').respond(200, projectsData);


            service.initialize();
            $httpBackend.flush();

            expect(service.pdps.length).toBe(1);
            var pdp = service.pdps[0];
            expect(pdp.id).toBe('pdpId1');
            expect(pdp.name).toBe('pdp1');
            expect(pdp.description).toBe('pdpDescription1');
            expect(pdp.security_pipeline.length).toBe(1);
            expect(pdp.security_pipeline[0].id).toBe('policyId1');
            expect(pdp.keystone_project_id).toBe('projectId1');
            expect(pdp.project.id).toBe('projectId1');

            expect(service.policies.length).toBe(2);
            var policy = service.policies[0];
            expect(policy.id).toBe('policyId1');
            expect(policy.name).toBe('policy1');
            expect(policy.description).toBe('pDescription1');


            expect(service.projects.length).toBe(2);
            var project = service.projects[0];
            expect(project.id).toBe('projectId1');
            expect(project.name).toBe('project1');

        });



        it('should create pdp', function () {
            var pdpCreatedData = {
                pdps:
                    { 'pdpId1': { name: 'pdp1', description: 'pdpDescription1', security_pipeline: [], keystone_project_id: null } }
            };

            $httpBackend.expectPOST(URI.API + '/pdp').respond(200, pdpCreatedData);

            service.createPdp({ name: 'pdp1', description: 'pdpDescription1' });
            $httpBackend.flush();

            expect(service.pdps.length).toBe(1);
            var pdp = service.pdps[0];
            expect(pdp.id).toBe('pdpId1');
            expect(pdp.name).toBe('pdp1');
            expect(pdp.description).toBe('pdpDescription1');
            expect(pdp.project).toBe(null);
            expect(pdp.security_pipeline.length).toBe(0);
        });

        it('should remove pdp', function () {
            initData();
            service.createPdps(pdpsData, policiesData, projectsData);

            $httpBackend.expectDELETE(URI.API + '/pdp/pdpId1').respond(200);

            service.removePdp({ id: 'pdpId1' });
            $httpBackend.flush();

            expect(service.pdps.length).toBe(0);
        });

        it('should update pdp', function () {
            initData();
            var pdpUpdatedData = {
                pdps:
                { 'pdpId1': { name: 'pdp2', description: 'pdpDescription2', security_pipeline: ['policyId2'], keystone_project_id: 'projectId2' } }
            };
            service.createPdps(pdpsData, policiesData, projectsData);

            $httpBackend.expectPATCH(URI.API + '/pdp/pdpId1').respond(200, pdpUpdatedData);

            service.updatePdp({ id: 'pdpId1', name: 'pdp2', description: 'pdpDescription2', security_pipeline: [service.getPolicy('policyId2')], project: service.getProject('projectId2') });
            $httpBackend.flush();

            expect(service.pdps.length).toBe(1);
            var pdp = service.pdps[0];
            expect(pdp.id).toBe('pdpId1');
            expect(pdp.name).toBe('pdp2');
            expect(pdp.description).toBe('pdpDescription2');
            expect(pdp.project.id).toBe('projectId2');
            expect(pdp.security_pipeline.length).toBe(1);
            expect(pdp.security_pipeline[0].id).toBe('policyId2');

        });


    });


})();