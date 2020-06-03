/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('PDPAddController', PDPAddController);
	
	PDPAddController.$inject = ['$scope', '$translate', 'alertService', 'formService', 'pdpService', 'policyService', 'utilService'];

	function PDPAddController($scope, $translate, alertService, formService, pdpService, policyService, utilService) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		
		add.pdp = {};

		add.policies = [];

		add.selectedPolicy = null;

		add.loading = false;
		add.loadingPolicies = true;

		add.create = createPDP;
		
		resolvePolicies();
		
		/*
		 *  
		 */
		
		/**
		 * This function return an array of all policies/template ids
		 */
		function resolvePolicies() {

			policyService.findAllWithCallback(function(policies){

				add.policies = policies;
                add.loadingPolicies = false;
			});
			
		}
                
        function createPDP(pdp) {
        	
        	if(formService.isInvalid(add.form)) {
        		
        		formService.checkFieldsValidity(add.form);
        	        	
        	} else {

                add.loading = true;

        		pdpService.data.pdp.create({}, {

        			name: add.pdp.name,
					description: add.pdp.description,
					security_pipeline: [add.selectedPolicy.id],
					keystone_project_id: null

        		}, createSuccess, createError);
        			        	        	
    		}
        	
        	function createSuccess(data) {
    			
    			$translate('moon.pdp.add.success', { pdpName: pdp.name })
					.then(function (translatedValue) {
        				alertService.alertSuccess(translatedValue);
                });

                var createdPdp =  utilService.transformOne(data, 'pdps');

                add.loading = false;

    			$scope.$emit('event:pdpCreatedSuccess', createdPdp);
    			
    		}
    		
    		function createError(reason) {
    			
    			$translate('moon.pdp.add.error', { pdpName: pdp.name })
					.then(function (translatedValue) {
        				alertService.alertError(translatedValue);
                });

                add.loading = false;

    			$scope.$emit('event:pdpCreatedError');
    			
    		}
        	
        }
		
	}
	
})();
