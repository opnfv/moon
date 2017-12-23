/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('ProjectDeleteController', ProjectDeleteController);
	
	ProjectDeleteController.$inject = ['$scope', '$translate', 'alertService', 'projectService', 'pdpService'];
	
	function ProjectDeleteController($scope, $translate, alertService, projectService, pdpService) {
		
		var del = this;
		
		/*
		 * 
		 */
		
		del.project = $scope.project;
		del.loading = false;
		del.loadingPDP = true;
		del.remove = deleteProjectAndMapping;
		del.isProjectMapped = isProjectMapped;
        del.pdps = [];

        activate();

        /**
         *
         */

        function activate(){

            resolvePDPs();

        }

        function resolvePDPs() {

            pdpService.findAllWithCallBack(function(data){

                del.pdps = data;

                pdpService.mapPdpsToProject(del.project, del.pdps);

                del.loadingPDP = false;

            });

        }

        function isProjectMapped(){
            return _.has(del.project, 'pdp');
        }

        /*
         * ---- delete
         */


        function deleteProjectAndMapping() {

            del.loading = true;


            if(isProjectMapped() ) {

                removeMapping(deleteProject);

            }else{
                deleteProject();
            }

        }

        function removeMapping(callbackSuccess){


            var pdpName = unmap.project.pdp.name;

            pdpService.unMap(unmap.project, callbackSuccess, deleteMappingError);


            function deleteMappingError(reason) {

                $translate('moon.project.remove.mapping.remove.error', { pdpName: pdpName} ).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                del.loading = false;

                $scope.$emit('event:projectDeletedError', del.project);

            }


		}

        function deleteProject(){

            projectService.data.projects.remove({project_id: del.project.id}, deleteSuccess, deleteError);

            function deleteSuccess(data) {

                $translate('moon.project.remove.success', { projectName: del.project.name }).then(function (translatedValue) {
                    alertService.alertSuccess(translatedValue);
                });

                del.loading = false;

                $scope.$emit('event:projectDeletedSuccess', del.project);

            }

            function deleteError(reason) {

                $translate('moon.project.remove.error', { projectName: del.project.name, errorCode: reason.data.error.code, message : reason.data.error.message } ).then(function (translatedValue) {
                    alertService.alertError(translatedValue);
                });

                del.loading = false;

                $scope.$emit('event:projectDeletedError', del.project);

            }

        }
	}
	
})();
