import Vue from 'vue'
import config from '../config.js'
import util from './Util.service'

var host = config.host;

var attributeResource;

var attributesMap = {};
var attributes = [];

function loadAttributes(){
    attributeResource = Vue.resource(host + '/attributes{/id}', {});

    attributeResource.query().then(res => {
        createAttributes(res.body);
    }, util.displayErrorFunction('Unable to load attributes'));
}

function createAttributes(attributesData){
    attributes.splice(0, attributes.length);
    util.cleanObject(attributesMap);
    util.createInternal(attributesData.attributes, attributes, attributesMap);
}

function getAttribute(id){
    return attributesMap[id];
}

function getAttributeId(name){
    for (let i = 0; i < attributes.length; i++){
        let attr = attributes[i];
        for (let j = 0; j < attr.values.length; j++){
            let value = attr.values[j];
            if (value === name){
                return attr.id;
            }
        }
    }
}

export default {
    initialize: loadAttributes,
    getAttribute: getAttribute,
    getAttributeId: getAttributeId
}