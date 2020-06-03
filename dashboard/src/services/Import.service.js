import Vue from 'vue'
import util from './Util.service.js'
import config from '../config.js'

var host = config.host;

export default {
    importData: async function importData(data) {
        var importResource = Vue.resource(host + '/import/', {});

         return importResource.save(null, data).then(success, util.displayErrorFunction('Unable to import data'));
        function success() {
            util.displaySuccess('Data imported');
        }
    }
}            