/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.factory('versionService', versionService);
		
	versionService.$inject = ['$resource'];
				
	function versionService($resource) {
		
        return {
        	
        		version: $resource('version.json', {}, {
        			get: {method: 'GET', isArray: false}
     	   		})
     	   		
        };
		
	}
	
})();
