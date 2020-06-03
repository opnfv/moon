(function () {

    'use strict';

    angular
        .module('moon')
        .factory('moon.import.service', importService);

        importService.$inject = ['moon.util.service', '$resource', 'moon.URI'];

    function importService(util, $resource, URI) {
        var host = URI.API;
        var importResource = $resource(host + '/import/', {}, {
            create: { method: 'POST' },
        });

        return {
            importData: function importData(data) {
                return importResource.create(null, data).$promise.then(success, util.displayErrorFunction('Unable to import data'));

                function success(data) {
                    util.displaySuccess('Data imported');
                }
            }
        }
    }
})();