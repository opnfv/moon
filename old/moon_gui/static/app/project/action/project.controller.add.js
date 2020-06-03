/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('ProjectAddController', ProjectAddController);
	
	ProjectAddController.$inject = ['$scope', '$translate', 'alertService', 'formService', 'projectService', 'DEFAULT_CST'];
	
	function ProjectAddController($scope, $translate, alertService, formService, projectService, DEFAULT_CST) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};

		add.loading = false;

		//@todo: verify if enable argument is understood serrver-side
		add.project = { project: {name: null, description: null, enabled: true, domain: DEFAULT_CST.DOMAIN.DEFAULT} };
		add.create= createProject;
		
		/*
		 * ---- create
		 */
		
		function createProject() {
        	
        	if(formService.isInvalid(add.form)) {
        		
        		formService.checkFieldsValidity(add.form);
        	        	
        	} else {

                add.loading = true;

	        	projectService.data.projects.create({}, add.project, createSuccess, createError);

    		}
        	
        	function createSuccess(data) {

				var created = data.project;
        		$translate('moon.project.add.success', { projectName: created.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });

                add.loading = false;
        		
        		$scope.$emit('event:projectCreatedSuccess', created);
        			        		
        	}
        	
        	function createError(reason) {
        		
        		$translate('moon.project.add.error', { projectName: add.project.project.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });

                add.loading = false;
        		
        		$scope.$emit('event:projectCreatedError', add.project);
        		
        	}
        	
        }
		
	}
	
})();
