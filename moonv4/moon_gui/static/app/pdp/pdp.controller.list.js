/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('PDPListController', PDPListController);
	
	PDPListController.$inject = [
		'$rootScope',
		'$scope',
		'$filter',
		'$modal',
		'NgTableParams',
		'pdps',
		'projectService'];

	function PDPListController($rootScope,
							   $scope,
							   $filter,
							   $modal,
							   NgTableParams,
							   pdps,
							   projectService) {
		
		var list = this;

		list.pdps = pdps;
        list.mappings = [];


        list.getPDPs = getPDPs;
		list.hasPDPs = hasPDPs;
		list.getPDPName = getPDPName;
		list.isMapped = isMapped;
		list.getProjectFromPDP = getProjectFromPDP;
		list.getidFromPDP = getidFromPDP;

		list.table = {};
		
		list.addPDP = addPDP;
		list.deletePDP = deletePDP;
		list.refreshPDPs = refreshPDPs;
		list.updatePDPs = updatePDPs;
		
		list.getMappedProjectName = getMappedProjectName;
		list.getSecPipelineFromPdp = getSecPipelineFromPdp;

		list.search = { query: '', 
						find: searchPDP,
						reset: searchReset };
		
		list.add = { modal: $modal({ template: 'html/pdp/action/pdp-add.tpl.html', show: false }),
				 	 showModal: showAddModal };
		
		list.del = { modal: $modal({ template: 'html/pdp/action/pdp-delete.tpl.html', show: false }),
				 	 showModal: showDeleteModal };

        activate();

		function activate(){
            newPDPsTable();
        }
		
		/*
		 * ---- events
		 */
		
		var rootListeners = {
				
				'event:pdpCreatedSuccess': $rootScope.$on('event:pdpCreatedSuccess', pdpCreatedSuccess),
				'event:pdpCreatedError': $rootScope.$on('event:pdpCreatedError', pdpCreatedError),
				
				'event:pdpDeletedSuccess': $rootScope.$on('event:pdpDeletedSuccess', pdpDeletedSuccess),
				'event:pdpDeletedError': $rootScope.$on('event:pdpDeletedError', pdpDeletedError),
				
		};

		_.each(rootListeners, function(unbind){
            $scope.$on('$destroy', rootListeners[unbind]);
        });

		/*
		 * 
		 */
		
		/**
		 * Function getting an array of PDP JSON
		 * @return An array of valid pdp.
		 */
		function getPDPs() {
		   return (list.pdps) ? list.pdps : [];
		}
		
		function hasPDPs() {
			return list.getPDPs().length > 0;
		}
		
		function addPDP(pdp) {
			list.pdps.push(pdp);
		}
		
		function deletePDP(pdp) {

			list.pdps = _.chain(list.pdps).reject({id: pdp.id}).value();

        }
		
		function refreshPDPs() {
			
			list.table.total(list.pdps.length);
			list.table.reload();
						
		}
		
		function updatePDPs(pdp) {
			
			_(_.values(list.getPDPs())).each(function(anPDP) {
        		if(anPDP.id === pdp.id) {
					//@todo: Determine what this code should have been designed to do
        			anPDP = _.clone(pdp);
        		}
        	});
			
			return list.pdps;
			
		}

		/**
		 * Get the id from an PDP
		 * @param pdp The inspected pdp
		 * @returns {*} Its UUID
		 */
		function getidFromPDP(pdp) {
			return pdp.id;
		}
		
		function getMappedProjectName(pdp) {
			return pdp.tenant.name;
		}

		/**
		 * Get the name of the PDP
		 * @param pdp The PDP to inspect
		 * @returns {*} Its name.
		 */
		function getPDPName(pdp) {
			return (pdp) ? pdp.name : '';
		}

		function isMapped(pdp) {
            return !_.isNull(pdp.keystone_project_id);
		}

        /**
		 * Prerequisite : before calling this method, isMapped should return true before
         * @param pdp
         * @returns false or {*}, false if the project is currently loading
         */
		function getProjectFromPDP(pdp) {

            if(_.has(pdp, 'project')){
                return pdp.project;
            }

            // if the call has not been made
            if(!_.has(pdp, 'callPdpInProgress')){

				pdp.callPdpInProgress = true;

                projectService.findOne(pdp.keystone_project_id, function(project){
                    pdp.callPdpInProgress = false;
                    pdp.project = project;
                    return pdp.project;
                });
			}

			// if the call is in progress return false
			return false;
		}

		/**
		 * Generate a table item, directly usable by the rendering engine
		 * @returns {{}|*} the table
		 */
		function newPDPsTable() {
			
			list.table = new NgTableParams({
			    
				page: 1,            // show first page
				count: 10,          // count per page
	   	
			}, {
		    	
				total: function () { return list.getPDPs().length; }, // length of data
				getData: function($defer, params) {
		        	
					var orderedData = params.sorting() ? $filter('orderBy')(list.getPDPs(), params.orderBy()) : list.getPDPs();
					$defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));

				},
				$scope: { $data: {} }
		        
			});
			
			return list.table;
			
		}


		/*
		 * --- search
		 */

		/**
		 * Indicate if an pdp having a specified name exists
		 * @param pdp Searched name
		 * @returns {boolean} True if a corresponding pdp is found, false otherwise
		 */
		function searchPDP(pdp){
			return list.getPDPName(pdp).indexOf(list.search.query) !== -1 || list.getSecPipelineFromPdp(pdp).indexOf(list.search.query) !== -1 ;
		}

		function getSecPipelineFromPdp(pdp){
			return (pdp.security_pipeline) ? pdp.security_pipeline : [];
		}

		/**
		 * Blank the search field
		 */
		function searchReset() {
			list.search.query = '';
		}
		
		/*
		 * ---- add
		 */
		
		function showAddModal() {
        	list.add.modal.$promise.then(list.add.modal.show);
        }
                
        function pdpCreatedSuccess(event, pdp) {
        	
        	list.addPDP(pdp);
        	list.refreshPDPs();
			
			list.add.modal.hide();
        	
        }
        
        function pdpCreatedError(event, pdp) {
        	list.add.modal.hide();
        }
        
        /*
         * ---- delete
         */
        
        function showDeleteModal(pdp) {
        	list.del.modal.$scope.pdp = pdp;
        	list.del.modal.$promise.then(list.del.modal.show);
        }
        
        function pdpDeletedSuccess(event, pdp) {
        	        	
        	list.deletePDP(pdp);
        	list.refreshPDPs();
			
			list.del.modal.hide();
        	
        }
        
        function pdpDeletedError() {
        	list.del.modal.hide();
        }
		
	}
		
})();
