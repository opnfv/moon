/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.controller('FooterController', FooterController);
	
	FooterController.$inject = ['$modal', 'versionService'];
	
	function FooterController($modal, versionService) {
		
		var footer = this;
		
		footer.version = null;
		footer.browsersModal = null;
		footer.showBrowsersCompliance = showBrowsersCompliance;
		
		newBrowsersModal();
		currentVersion();
		
		function newBrowsersModal() {
			
			footer.browsersModal = $modal({ template: 'html/common/compatibility/compatibility.tpl.html', show: false });
			
			return footer.browsersModal;
			
		}
		
		function showBrowsersCompliance() {
			footer.browsersModal.$promise.then(footer.browsersModal.show);  
		}
		
		function currentVersion() {
			
			var _self = footer;
			
			versionService.version.get().$promise.then(function(data) {
				
				_self.version = (data.version) ? data.version : 'SNAPSHOT';
				
				return _self.version;
				
			});
			
		}
		
	}
	
})();