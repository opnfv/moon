(function () {

    'use strict';

    angular
        .module('moon')
        .factory('moon.pdp.service', pdpService);

    pdpService.$inject = ['moon.util.service', '$resource', 'moon.URI', '$q', 'horizon.app.core.openstack-service-api.keystone'];

    function pdpService(util, $resource, URI, $q, keystone) {
        var host = URI.API;

        var pdpResource = $resource(host + '/pdp/' + ':id', {}, {
            get: { method: 'GET' },
            query: { method: 'GET' },
            create: { method: 'POST' },
            remove: { method: 'DELETE' },
            update: { method: 'PATCH' }
        });

        var policyResource = $resource(host + '/policies/' + ':id', {}, {
            query: { method: 'GET' },
        });

        var pdpsMap = {};
        var pdps = [];
        var policiesMap = {};
        var policies = [];
        var projectsMap = {};
        var projects = [];

        function loadPdps() {
            var queries = {
                pdps: pdpResource.query().$promise,
                policies: policyResource.query().$promise,
                projects: keystone.getProjects()
            }

            $q.all(queries).then(function (result) {
                createPdps(result.pdps, result.policies, result.projects.data)
                console.log('moon', 'pdps initialized', pdps)
            })
        }

        function createPdps(pdpsData, policiesData, projectsData) {
            pdps.splice(0, pdps.length);
            policies.splice(0, policies.length);
            projects.splice(0, projects.length);
            util.cleanObject(pdpsMap);
            util.cleanObject(policiesMap);
            util.cleanObject(projectsMap)

            util.createInternal(policiesData.policies, policies, policiesMap);
            util.pushAll(projects, projectsData.items);
            util.addToMap(projects, projectsMap);
            createPdpInternal(pdpsData.pdps);
        }

        function mapPdp(pdp) {
            util.mapIdToItem(pdp.security_pipeline, policiesMap);
            pdp.project = null;
            if (pdp.keystone_project_id) {
                pdp.project = projectsMap[pdp.keystone_project_id];
            }
        }

        function createPdpInternal(data) {
            return util.createInternal(data, pdps, pdpsMap, mapPdp);
        }

        function updatePdpInternal(data) {
            return util.updateInternal(data, pdpsMap, mapPdp);
        }

        function removePdpInternal(id) {
            return util.removeInternal(id, pdps, pdpsMap);
        }

        return {
            initialize: loadPdps,
            createPdps: createPdps,
            pdps: pdps,
            policies: policies,
            projects: projects,
            createPdp: function createPdp(pdp) {
                pdp.keystone_project_id = null;
                pdp.security_pipeline = [];
                pdpResource.create(null, pdp, success, util.displayErrorFunction('Unable to create PDP'));

                function success(data) {
                    createPdpInternal(data.pdps);
                    util.displaySuccess('PDP created');
                }
            },
            removePdp: function removePdp(pdp) {
                pdpResource.remove({ id: pdp.id }, null, success, util.displayErrorFunction('Unable to remove PDP'));

                function success(data) {
                    removePdpInternal(pdp.id);
                    util.displaySuccess('PDP removed');
                }
            },
            updatePdp: function updatePdp(pdp) {
                util.mapItemToId(pdp.security_pipeline);
                pdp.keystone_project_id = pdp.project ? pdp.project.id : null;
                pdpResource.update({ id: pdp.id }, pdp, success, util.displayErrorFunction('Unable to update PDP'));

                function success(data) {
                    updatePdpInternal(data.pdps)
                    util.displaySuccess('PDP updated');
                }
            },
            getPolicy: function getPolicy(id) {
                return policiesMap[id];
            },
            getProject: function getProject(id) {
                return projectsMap[id];
            },
        }
 
    }
})();