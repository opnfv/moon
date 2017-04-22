/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.factory('menuService', menuService);
	
	menuService.$inject = ['$state'];
	
	function menuService($state) {

        var service = {};

        service.isProjectTabActive = isProjectTabActive;
        service.isPDPTabActive = isPDPTabActive;
        service.isPolicyTabActive = isPolicyTabActive;
        service.isLogsTabActive = isLogsTabActive;
        service.isModelTabActive = isModelTabActive;

        return service;

		function isProjectTabActive() {
			return $state.includes('moon.project');
		}
			
		function isPDPTabActive() {
			return $state.includes('moon.pdp');
		}

        function isPolicyTabActive(){
            return $state.includes('moon.policy');
        }

		function isLogsTabActive(){
			return $state.includes('moon.logs');
		}

		function isModelTabActive(){
            return $state.includes('moon.model');
        }

	}
	
})();
