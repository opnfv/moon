/**
 * Service providing access to the tenants
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';

	angular
		.module('moon')
				.factory('projectService', projectService);

    projectService.$inject = [ '$resource' , 'REST_URI' ];
	
	function projectService( $resource, REST_URI) {
	                                   	
		return {
			
			data: {

				projects: $resource(REST_URI.KEYSTONE + 'projects/:project_id', {}, {
					query: {method: 'GET', isArray: false},
                    get: { method: 'GET', isArray: false },
                    create: { method: 'POST' },
                    remove: { method: 'DELETE' }
                })

			},

			findOne: function(project_id, callback){

                return this.data.projects.get({project_id: project_id}).$promise.then(function(data) {

                    callback(data.project);

                });

			},

            findAll: function() {

                return this.data.projects.query().$promise.then(function(listProjects) {

                    var result = [];

                    _.each(listProjects['projects'], function(item){
                        result.push(item);
                    });

                    return result;
                });

            }
        
        };
    
    }
	
})();
