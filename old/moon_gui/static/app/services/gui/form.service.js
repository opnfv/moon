/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.factory('formService', formService);
		
	function formService() {

        var service = {};

        service.isInvalid = isInvalid;
        service.checkFieldsValidity = checkFieldsValidity;

        return service;
		
		function isInvalid(form) {
			return form.$invalid;
		}
		
		function checkFieldsValidity(form) {
			
			var validationErrorKeys = _.keys(form.$error);
        	
    		_(validationErrorKeys).each(function(anErrorKey) {
    			
    			var formFields = _.values(form.$error[anErrorKey]);
    			
    			_(formFields).each(function(aFormField) {
    				
    				aFormField.$dirty = true;
    				aFormField.$setValidity(anErrorKey, false);
    				
    			});
    			
    		});
			
		}

	}

})();
