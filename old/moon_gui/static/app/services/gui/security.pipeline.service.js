(function() {

    'use strict';

    angular
        .module('moon')
        .factory('securityPipelineService', securityPipelineService);

    securityPipelineService.$inject = ['SECURITY_PIPELINE_CST','policyService'];

    function securityPipelineService(SECURITY_PIPELINE_CST, policyService) {
        var service = {};

        service.findAll = findAll;

        return service;

        function findAll(type){
            switch(type){
                case SECURITY_PIPELINE_CST.TYPE.POLICY :
                    return policyService.findAll();
                default :
                    return policyService.findAll();
            }

        }
    }

})();
