/**
 * service allowing the client to interact with pdp
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';

	angular
		.module('moon')
				.factory('pdpService', pdpService);

    pdpService.$inject = ['$q', '$resource','REST_URI', 'utilService'];
	
	function pdpService($q, $resource, REST_URI, utilService) {
		
		return {
			
			data: {

				pdp: $resource(REST_URI.PDP + ':pdp_id', {}, {
	     	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false },
	     	   		create: { method: 'POST' },
					update: { method:'PATCH'},
	     	   		remove: { method: 'DELETE' }
	    	   	})

			},

			findAll: function() {

                return this.data.pdp.query().$promise.then(function (data) {

                    return utilService.transform(data, 'pdps');

                });

	   		},

            findAllWithCallBack : function (callback){

                return this.data.pdp.query().$promise.then(function (data) {

                    callback( utilService.transform(data, 'pdps'));

                });

			},
	   		
	   		findOne: function(id) {

                return this.data.pdp.get({pdp_id: id}).$promise.then(function (data) {

                    return utilService.transformOne(data, 'pdps');

                });

	   		},

			unMap: function(pdp, callbackSuccess, callbackError){

            	pdp.keystone_project_id = null;

            	if(_.has(pdp, 'project')){
					delete pdp.project;
				}

                this.data.pdp.update({pdp_id: pdp.id}, pdp, callbackSuccess, callbackError);

            },

			map: function(pdp, projectId, callbackSuccess, callbackError){

				pdp.keystone_project_id = projectId;

                this.data.pdp.update({pdp_id: pdp.id}, pdp, callbackSuccess, callbackError);
			},

            update: function (pdp, callbackSuccess, callbackError) {

                this.data.pdp.update({pdp_id: pdp.id}, pdp, callbackSuccess, callbackError);

            },

            mapPdpsToProjects : mapPdpsToProjects,

            mapPdpsToProject : mapPdpsToProject
    	   	
		};

        /**
		 * Will assign each project to it related pdp
         * @param projects a list of Project, a new attribute pdp will be add, if the related pdp is existing in @param pdps
         * @param pdps a list of Pdp
         */
		function mapPdpsToProjects(projects, pdps){

            _.each(projects, function(project){

                return mapPdpsToProject(project, pdps);

            });
		}

		function mapPdpsToProject(project, pdps){

            if (_.isNull(project.keystone_project_id)){
                return false;
            }

            var index = _.findIndex(pdps, function(pdp){
                return project.id === pdp.keystone_project_id;
            });

            if(index === -1){
                return false;
            }

            project.pdp = pdps[index];

            return true;
		}
		
	}
	
})();
