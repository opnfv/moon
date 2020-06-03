/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.factory('alertService', alertService);
	
	alertService.$inject = [ 'toaster'];
	
	function alertService( toaster) {

        var service = {};

        service.alertError = alertError;
        service.alertSuccess = alertSuccess;
        service.alertInfo = alertInfo;

        return service;

        function alertError(msg){
        	toaster.pop('error', null, msg, 5000);
        }
        
        function alertSuccess(msg){
        	toaster.pop('success', null, msg, 5000);
        }
        
        function alertInfo(msg){
        	toaster.pop('note', null, msg, 5000);
        }
		
	}
	
})();
