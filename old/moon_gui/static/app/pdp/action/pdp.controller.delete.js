/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('PDPDeleteController', PDPDeleteController);
	
	PDPDeleteController.$inject = ['$scope', '$translate', 'alertService', 'pdpService'];
	
	function PDPDeleteController($scope, $translate, alertService, pdpService) {
		
		var del = this;
		
		/*
		 * 
		 */
		
		del.pdp = $scope.pdp;
		del.loading = false;
		del.remove = deletePDP;
		
		/*
		 * 
		 */
		
		function deletePDP() {
            del.loading = true;

			pdpService.data.pdp.remove({pdp_id: del.pdp.id}, deleteSuccess, deleteError);
			
			function deleteSuccess(data) {

				$translate('moon.pdp.remove.success', { pdpName: del.pdp.name })
					.then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });

                del.loading = false;

                $scope.$emit('event:pdpDeletedSuccess', del.pdp);
				
			}
			
			function deleteError(reason) {
				
				$translate('moon.pdp.remove.error', { pdpName: del.pdp.name })
					.then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });

                del.loading = false;

                $scope.$emit('event:pdpDeletedError', del.pdp);
				
			}
			
		}
		
	}
	
})();
