/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('ProjectUnMapController', ProjectUnMapController);
	
	ProjectUnMapController.$inject = ['$scope', '$translate', 'alertService', 'pdpService'];
	
	function ProjectUnMapController($scope, $translate, alertService, pdpService) {

		var unmap = this;
		
		/*
		 * 
		 */
		
		unmap.project = $scope.project;
		unmap.unMappingLoading = false;

		unmap.unmap = unMapProject;
		
		/*
		 * 
		 */
		
		function unMapProject() {
			

            unmap.unMappingLoading = true;

            var pdpName = unmap.project.pdp.name;

            pdpService.unMap(unmap.project.pdp, unMapSuccess, unMapError);

        	function unMapSuccess(data) {
        		
        		$translate('moon.project.unmap.success', { projectName: unmap.project.name, pdpName: pdpName })
					.then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });

                unmap.unMappingLoading = false;

				delete unmap.project.mapping;
                delete unmap.project.pdp;

                $scope.$emit('event:projectUnmappedSuccess', unmap.project);
        		
        	}
        	
        	function unMapError(reason) {
        		
        		$translate('moon.project.unmap.error', { projectName: unmap.project.name, pdpName: pdpName })
					.then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });

                unmap.unMappingLoading = false;

                $scope.$emit('event:projectUnmappedError', unmap.project);
        		
        	}
			
		}
		
	}
			
})();
