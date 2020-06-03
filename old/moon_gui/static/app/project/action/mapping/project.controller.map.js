/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('ProjectMapController', ProjectMapController);
	
	ProjectMapController.$inject = ['$scope', '$translate', 'alertService', 'formService', 'pdpService'];
	
	function ProjectMapController($scope, $translate, alertService, formService, pdpService) {

		var map = this;
		
		/*
		 * 
		 */

		map.form = {};
		
		map.project = $scope.project;

		map.pdps = [];

		map.pdpsLoading = true;

		map.selectedPDP = null;
		
		map.map = mapProject;

        activate();

		function activate(){

            resolvePDPs();

        }

		/*
		 * 
		 */
		
		function resolvePDPs() {

            pdpService.findAllWithCallBack(resolveMappedProjects);

		}

        function resolveMappedProjects(pdps) {

            map.pdps = _.filter(pdps, function(pdp){
                return _.isNull(pdp.keystone_project_id);
            });

            map.pdpsLoading = false;

        }
		
		function mapProject() {
			
			if(formService.isInvalid(map.form)) {
        		
        		formService.checkFieldsValidity(map.form);
        	        	
        	} else {

				map.mappingLoading = true;

                pdpService.map( map.selectedPDP, map.project.id, mapSuccess, mapError);

    		}
			
			function mapSuccess(data) {
        		
				map.project.pdp = map.selectedPDP;
        		
        		$translate('moon.project.map.success', { projectName: map.project.name, pdpName: map.selectedPDP.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });

                map.mappingLoading = false;

        		$scope.$emit('event:projectMappedSuccess', map.project);
        		
        	}
        	
        	function mapError(response) {
        		
        		$translate('moon.project.map.error', { projectName: map.project.name, pdpName: map.selectedPDP.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });

                map.mappingLoading = false;
        		
        		$scope.$emit('event:projectMappedError', map.project);
        		
        	}
			
		}
		
	}
	
})();
