/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('ProjectListController', ProjectListController);

    ProjectListController.$inject = ['$rootScope', '$scope', '$filter', '$modal', 'ngTableParams', 'pdpService', 'projects'];
	
	function ProjectListController($rootScope, $scope, $filter, $modal, ngTableParams, pdpService, projects) {
		
		var list = this;
		
		/*
		 * 
		 */
		
		list.projects = projects;
		list.pdps = [];

		list.getProjects = getProjects;
		list.hasProjects = hasProjects;
		list.isProjectMapped = isProjectMapped;

		list.table = {};
		
		list.addProject = addProject;
		list.deleteProject = deleteProject;
		list.refreshProjects = refreshProjects;

		list.getMappedPDPName = getMappedPDPName;
		list.getPdpFromProject = getPdpFromProject;
		
		list.search = { query: '', 
						find: searchProject,
						reset: searchReset };
		
		list.add = { modal: $modal({ template: 'html/project/action/project-add.tpl.html', show: false }),
					 showModal: showAddModal };
		
		list.del = { modal: $modal({ template: 'html/project/action/project-delete.tpl.html', show: false }),
					 showModal: showDeleteModal };
		
		list.map = { modal: $modal({ template: 'html/project/action/mapping/project-map.tpl.html', show: false }),
					 showModal: showMapModal };
		
		list.unmap = { modal: $modal({ template: 'html/project/action/mapping/project-unmap.tpl.html', show: false }),
				 	   showModal: showUnmapModal };
		
		list.view = { modal: $modal({ template: 'html/project/action/project-view.tpl.html', show: false }),
			 	   	  showModal: showViewModal };

        activate();


        function activate(){

            list.loadingPDPs = true;

            newProjectsTable();

            pdpService.findAllWithCallBack(function(data){

                list.pdps = data;

                pdpService.mapPdpsToProjects(list.projects, list.pdps);

                list.loadingPDPs = false;

            });
        }


		/*
		 * ---- events
		 */
		
		var rootListeners = {
				
				'event:projectCreatedSuccess': $rootScope.$on('event:projectCreatedSuccess', projectCreatedSuccess),
				'event:projectCreatedError': $rootScope.$on('event:projectCreatedError', projectCreatedError),
				
				'event:projectDeletedSuccess': $rootScope.$on('event:projectDeletedSuccess', projectDeletedSuccess),
				'event:projectDeletedError': $rootScope.$on('event:projectDeletedError', projectDeletedError),
				
				'event:projectMappedSuccess': $rootScope.$on('event:projectMappedSuccess', projectMappedSuccess),
				'event:projectMappedError': $rootScope.$on('event:projectMappedError', projectMappedError),
				
				'event:projectUnmappedSuccess': $rootScope.$on('event:projectUnmappedSuccess', projectUnmappedSuccess),
				'event:projectUnmappedError': $rootScope.$on('event:projectUnmappedError', projectUnmappedError)
				
		};
		
		for (var unbind in rootListeners) {
			  $scope.$on('$destroy', rootListeners[unbind]);
		}
		
		/*
		 * ---- table
		 */

        /**
         * Get projects array from the Keystone Moon.
         * @return an array containing projects JSON
         */
        function getProjects() {
            return (list.projects) ? list.projects : [];
        }

		function hasProjects() {
			return list.getProjects().length > 0;
		}

		function isProjectMapped(project){
			return _.has(project, 'pdp');
		}

        /**
		 * Prerequisite, isProjectMapped should return true
         * @param project
         * @returns {*}
         */
		function getPdpFromProject(project){
			return project.pdp;
		}
		
		function addProject(project) {
			list.projects.push(project);
		}
		
		function deleteProject(project) {
			list.projects = _.chain(list.projects).reject({id: project.id}).value();
		}
		
		function refreshProjects() {
			
			list.table.total(list.projects.length);
			list.table.reload();
			
		}
		
		function newProjectsTable() {
			
			list.table = new ngTableParams({
			    
				page: 1,            // show first page
				count: 10,          // count per page
				sorting: {
					name: 'asc' // initial sorting
				}
	   	
			}, {
		    	
				total: function () { return list.getProjects().length; }, // length of data
				getData: function($defer, params) {
		        	
					var orderedData = params.sorting() ? $filter('orderBy')(list.getProjects(), params.orderBy()) : list.getProjects();
					$defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
		        	
				},
				$scope: { $data: {} }
		        
			});
			
			return list.table;
			
		}

        /**
		 *
         * @param project should have project.mapping.authz.pdp.name attribute
         */
		function getMappedPDPName(project) {
			return _.has(project, 'pdp') ? project.pdp.name : 'error';
		}
   			 
		/*
		 * ---- search
		 */
		 			    	
		function searchProject(project){
            return (project.name.indexOf(list.search.query) !== -1 || project.description.indexOf(list.search.query) !== -1);
		}
		
		function searchReset() {
			list.search.query = '';
		}
		
		/*
		 * ---- add
		 */
		
		function showAddModal() {
        	list.add.modal.$promise.then(list.add.modal.show);
        }
                
        function projectCreatedSuccess(event, project) {
        	
        	list.addProject(project);
        	list.refreshProjects();
			
			list.add.modal.hide();
        	
        }
        
        function projectCreatedError(event, project) {
        	list.add.modal.hide();
        }
        
        /*
         * ---- delete
         */
        
        function showDeleteModal(project) {
        	
        	list.del.modal.$scope.project = project;
        	list.del.modal.$promise.then(list.del.modal.show);
        	
        }
        
        function projectDeletedSuccess(event, project) {
        	        	
        	list.deleteProject(project);
        	list.refreshProjects();
			
			list.del.modal.hide();
        	
        }
        
        function projectDeletedError(event, project) {
        	list.del.modal.hide();
        }
        
        /*
         * ---- map
         */
        
        function showMapModal(project) {
        	
        	list.map.modal.$scope.project = project;
        	list.map.modal.$promise.then(list.map.modal.show);
        	
        }
        
        function projectMappedSuccess(event, project) {

            activate();
			list.map.modal.hide();
			
        }
        
        function projectMappedError(event, project) {
        	list.map.modal.hide();
        }
        
        /*
         * ---- unmap
         */
        
        function showUnmapModal(project) {
        	
        	list.unmap.modal.$scope.project = project;
        	list.unmap.modal.$promise.then(list.unmap.modal.show);
        	
        }
        
        function projectUnmappedSuccess(event, project) {


            var index = _.findIndex(list.projects, function(aProject){
                return project.id === aProject.id;
            });

            if(index === -1){
                list.unmap.modal.hide();
                return false;
            }

            list.projects[index] = project;

            list.refreshProjects();

            list.unmap.modal.hide();

        }
        
        function projectUnmappedError(event, project) {
        	list.unmap.modal.hide();        	
        }


        /*
         * ---- view
         */
        
        function showViewModal(project) {
        	
        	list.view.modal.$scope.project = project;
        	list.view.modal.$promise.then(list.view.modal.show);
        	
        }
		
	}
	
})();
