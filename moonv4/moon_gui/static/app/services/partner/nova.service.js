/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';

	angular
		.module('moon')
			.factory('novaService', novaService);
	
	novaService.$inject = ['$resource'];
	
	function novaService($resource) { 
	                                   	
        return {
            
        	data: {
        	
	            image: $resource('./pip/nova/images', {}, {
	            	query: {method: 'GET', isArray: false}
	     	   	}),
	     	   	
	     	   	flavor: $resource('./pip/nova/flavors', {}, {
	            	query: {method: 'GET', isArray: false}
	     	   	})
     	   	
        	}
        
        };
    
    }
	
})();
