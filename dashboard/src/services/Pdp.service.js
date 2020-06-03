import Vue from 'vue'
import util from './Util.service.js'
import config from '../config.js'

var host = config.host;

var pdpResource;
var policyResource;

var pdpsMap = {};
var pdps = [];
var policiesMap = {};
var policies = [];

function loadPdps() {
    pdpResource = Vue.resource(host + '/pdp{/id}', {}, {patch: {method: 'PATCH'}});
    policyResource = Vue.resource(host + '/policies{/id}', {});

    var queries = [
        pdpResource.query(),
        policyResource.query(),
    ]
    Promise.all(queries).then(function (result) {
        createPdps(result[0].body, result[1].body)
    })

}

function createPdps(pdpsData, policiesData) {
    pdps.splice(0, pdps.length);
    policies.splice(0, policies.length);
    util.cleanObject(pdpsMap);
    util.cleanObject(policiesMap);

    util.createInternal(policiesData.policies, policies, policiesMap);
    createPdpInternal(pdpsData.pdps);
}

function mapPdp(pdp) {
    util.mapIdToItem(pdp.security_pipeline, policiesMap);
    pdp.project = pdp.vim_project_id;
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

export default {
    initialize: loadPdps,
    createPdps: createPdps,
    pdps: pdps,
    policies: policies,
    createPdp: function createPdp(pdp) {
        pdpResource.save(null, pdp).then(success, util.displayErrorFunction('Unable to create PDP'));

        function success(data) {
            createPdpInternal(data.body.pdps);
            util.displaySuccess('PDP created');
        }
    },
    removePdp: function removePdp(pdp) {
        pdpResource.remove({ id: pdp.id }).then(success, util.displayErrorFunction('Unable to remove PDP'));

        function success() {
            removePdpInternal(pdp.id);
            util.displaySuccess('PDP removed');
        }
    },
    updatePdp: function updatePdp(pdp) {
        util.mapItemToId(pdp.security_pipeline);
        pdp.vim_project_id = pdp.project;
        pdpResource.patch({ id: pdp.id }, pdp).then(success, util.displayErrorFunction('Unable to update PDP'));

        function success(data) {
            updatePdpInternal(data.body.pdps)
            util.displaySuccess('PDP updated');
        }
    },
    getPolicy: function getPolicy(id) {
        return policiesMap[id];
    },
}


