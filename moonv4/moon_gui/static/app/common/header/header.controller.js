/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.controller('HeaderController', HeaderController);
	
	HeaderController.$inject = ['$translate', 'menuService', 'authenticationService', 'alertService'];
	
	function HeaderController($translate, menuService, authenticationService, alertService) {

		var header = this;

		/*
		 *
		 */

		header.isProjectTabActive = menuService.isProjectTabActive;
		header.isPDPTabActive = menuService.isPDPTabActive;
		header.isLogsTabActive = menuService.isLogsTabActive;
        header.isPolicyTabActive = menuService.isPolicyTabActive;
        header.isModelTabActive = menuService.isModelTabActive;
		header.changeLocale = changeLocale;
		header.logout = logout;
		header.currentLanguage = $translate.use();

		header.getUser = authenticationService.GetUser;

		/*
		 *
		 */

		function changeLocale(localeKey, event) {

            event.preventDefault();
            $translate.use(localeKey);
            $translate.preferredLanguage(localeKey);
            header.currentLanguage = localeKey;

        }

        function logout(){

            authenticationService.Logout();
            $translate('moon.logout.success').then( function(translatedValue) {
                alertService.alertSuccess(translatedValue);
            });

        }
	}
})();